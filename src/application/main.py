import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from application.controllers.elastic_controller import ElasticController
from application.controllers.upload_file_http import UploadFileHttp
from application.enums.routing_keys import RoutingKeys
from application.handlers.clock_handler import ClockHandler
from application.services.rabbitmq_service import MessageBrokerService


@asynccontextmanager
async def lifespan(app: FastAPI):
    rabbitmq = await MessageBrokerService.init()
    await rabbitmq.consume(RoutingKeys.get_all_processors())

    event = asyncio.Event()

    send_events = asyncio.create_task(
        ClockHandler.send_events(rabbitmq=rabbitmq, event=event)
    )
    try:
        yield
    finally:
        event.set()
        await rabbitmq.disconnect()
        await send_events


app = FastAPI(lifespan=lifespan)

app.include_router(UploadFileHttp.router)
app.include_router(ElasticController.router)
