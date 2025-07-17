import datetime
import os.path

from pyspark.sql import DataFrame
from sqlalchemy import exists, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from application.data_classes.metadata_dc import MetadataBaseDC
from application.enums.allowed_extensions import AllowedExtensions
from application.enums.file_status import FileStatus
from application.models import MetadataModel
from application.models.base import with_session
from application.services.store_file_service import StoreFileService


class FileManagerHandler:
    @classmethod
    @with_session(retries=1)
    async def store_metadata(
        cls, file_content: bytes, file_name: str, overwrite: bool, session: AsyncSession
    ) -> bool:
        file_path = os.path.join("uploaded-data", str(datetime.datetime.now().year))

        can_overwrite, dc_model = await cls._overwrite_policy(
            overwrite=overwrite,
            storage_path=file_path,
            file_name=file_name,
            session=session,
        )

        if not can_overwrite:
            return False

        metadata_dc: MetadataBaseDC | None = await StoreFileService.upload_file(
            file_name=file_name, file_content=file_content, file_path=file_path
        )

        if not metadata_dc:
            return False

        if dc_model:
            _query = (
                update(MetadataModel)
                .filter(MetadataModel.file_metadata_id == dc_model.file_metadata_id)
                .values(updated_at=dc_model.updated_at)
            )
            await session.execute(_query)
        else:
            model = MetadataModel(**metadata_dc.model_dump())
            session.add(model)

        return True

    @classmethod
    @with_session(retries=1)
    async def process_files(cls, file_metadata_ids: list[str], session: AsyncSession):
        await cls._batch_update(
            file_metadata_ids=file_metadata_ids,
            new_status=FileStatus.PROCESSING,
            session=session,
        )

        for file_metadata_id in file_metadata_ids:
            _query = select(MetadataModel).filter(
                MetadataModel.file_metadata_id == file_metadata_id
            )
            _query_result = await session.execute(_query)
            record: MetadataModel | None = _query_result.scalar_one_or_none()

            if not record:
                continue

            success_processed = await cls._process_particular_file(
                file_name=record.file_name,
                storage_path=record.storage_path,
                file_type=record.file_type,
            )

            await cls._batch_update(
                file_metadata_ids=file_metadata_ids,
                new_status=(
                    FileStatus.PROCESSED if success_processed else FileStatus.FAILED
                ),
                session=session,
            )

        return True

    @classmethod
    async def _process_particular_file(
        cls, file_name: str, storage_path: str, file_type: AllowedExtensions
    ) -> bool:
        try:
            file_data_frame: DataFrame = await StoreFileService.read_file(
                file_name=file_name,
                file_path=storage_path,
                file_type=file_type,
            )
            return True
        except Exception as ex:
            print(ex)
            return False

    @staticmethod
    async def _overwrite_policy(
        overwrite: bool, storage_path: str, file_name: str, session: AsyncSession
    ) -> tuple[bool, MetadataBaseDC | None]:
        if not overwrite:
            _query = select(
                exists().where(
                    MetadataModel.storage_path == storage_path,
                    MetadataModel.file_name == file_name,
                )
            )
            _query_result = await session.execute(_query)
            exists_ = _query_result.scalar()
            return not exists_, None
        else:
            _query = select(MetadataModel).filter(
                MetadataModel.storage_path == storage_path,
                MetadataModel.file_name == file_name,
            )
            _query_result = await session.execute(_query)
            record = _query_result.scalar_one_or_none()
            return True, MetadataBaseDC.model_validate(record) if record else None

    @staticmethod
    async def _batch_update(
        file_metadata_ids: list[str], new_status: FileStatus, session: AsyncSession
    ):
        update_query = (
            update(MetadataModel)
            .filter(MetadataModel.file_metadata_id.in_(file_metadata_ids))
            .values(status=new_status)
        )

        await session.execute(update_query)
        await session.commit()
