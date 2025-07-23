import asyncio

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from application.enums.file_status import FileStatus
from application.enums.routing_keys import RoutingKeys
from application.models import MetadataModel
from application.models.base import with_session
from application.services.rabbitmq_service import MessageBrokerService


class ClockHandler:
    @classmethod
    @with_session(retries=1)
    async def send_events(
        cls,
        rabbitmq: MessageBrokerService,
        delay: int = 5,
        batch_size: int = 100,
        session: AsyncSession = None,
        event: asyncio.Event = None,
    ):
        while not event.is_set():
            # await asyncio.sleep(delay)

            _query = (
                select(MetadataModel)
                .filter(
                    or_(
                        MetadataModel.status == FileStatus.PENDING,
                        MetadataModel.status == FileStatus.FAILED,
                    )
                )
                .order_by(MetadataModel.updated_at)
                .limit(batch_size)
                .offset(0)
            )

            result = await session.execute(_query)
            records = result.scalars().all()

            if not records:
                continue

            await rabbitmq.publish(
                routing_key=RoutingKeys.FILE_PROCESSOR,
                message={
                    "file_metadata_ids": [record.file_metadata_id for record in records]
                },
            )
