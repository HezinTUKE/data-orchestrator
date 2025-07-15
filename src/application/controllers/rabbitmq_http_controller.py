from fastapi import APIRouter


class RabbitMQHttpController:
    name = "rabbitmq"
    router = APIRouter(tags=[name])

    @staticmethod
    @router.post(f"/{name}/receiver")
    async def message_receiver(routing_key: str, message: dict):
        pass

    @staticmethod
    async def process_messages(routing_key: str):
        pass
