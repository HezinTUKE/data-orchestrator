import asyncio

from sqlalchemy import select
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
        cls, rabbitmq: MessageBrokerService, delay: int = 10, batch_size: int = 100, session: AsyncSession = None
    ):
        while True:
            _query = (
                select(MetadataModel)
                .filter(MetadataModel.status == FileStatus.PENDING)
                .limit(batch_size)
                .offset(0)
            )

            result = await session.execute(_query)
            records = result.scalars().all()
            file_ids = [record.file_metadata_id for record in records]
            await rabbitmq.publish(
                routing_key=RoutingKeys.FILE_PROCESSOR,
                message={"file_metadata_ids": file_ids},
            )

            await asyncio.sleep(delay)
