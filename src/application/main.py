from contextlib import asynccontextmanager

from fastapi import FastAPI

from application.controllers.upload_file_http import UploadFileHttp
from application.enums.routing_keys import RoutingKeys
from application.handlers.clock_handler import ClockHandler
from application.services.rabbitmq_service import MessageBrokerService


@asynccontextmanager
async def lifespan(app: FastAPI):
    rabbitmq = await MessageBrokerService.init()
    await rabbitmq.consume(
        RoutingKeys.get_all_processors()
    )
    await ClockHandler.send_events()
    yield
    await rabbitmq.disconnect()

app = FastAPI(lifespan=lifespan)

app.include_router(UploadFileHttp.router)
