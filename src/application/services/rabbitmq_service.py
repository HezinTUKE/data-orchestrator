import asyncio
import json

import aio_pika
from aio_pika.abc import (
    AbstractChannel,
    AbstractConnection,
    AbstractExchange,
    AbstractIncomingMessage,
)

from application.config import get_config_section
from application.enums.routing_keys import RoutingKeys
from application.handlers.rabbitmq_handler import RabbitMQHandler


class MessageBrokerService:
    rabbitmq_config = get_config_section("rabbitmq")

    def __init__(self, channel: AbstractChannel):
        self.channel = channel

    @classmethod
    async def init(cls, loop=None):
        loop = asyncio.get_running_loop() or loop
        config = cls.rabbitmq_config.get("connection")
        rabbitmq_url = "amqp://{login}:{password}@{host}:{port}/".format(**config)
        conn: AbstractConnection = await aio_pika.connect_robust(
            url=rabbitmq_url, loop=loop
        )
        channel: AbstractChannel = await conn.channel()
        await channel.set_qos(prefetch_count=10)
        return cls(channel)

    async def process_message(self, message: AbstractIncomingMessage):
        async with message.process():
            msg_body = json.loads(message.body.decode())
            await RabbitMQHandler.handler_mapping().get(message.routing_key)(msg_body)

    async def consume(self, routing_keys: list[str]):
        adapter_config = self.rabbitmq_config.get("adapter", {})
        exchange = await self._get_or_create_exchange(
            exchange_name=adapter_config.get("exchange", ""),
            exchange_type=adapter_config.get("exchange_type", ""),
        )
        queue = await self._get_or_create_queue(
            queue_name=adapter_config.get("queue", ""),
            durable=adapter_config.get("durable", True),
        )
        for routing_key in routing_keys:
            await queue.bind(exchange, routing_key=routing_key)
            await queue.consume(self.process_message)

    async def publish(self, routing_key: RoutingKeys, message: dict):
        adapter_config = self.rabbitmq_config.get("adapter", {})
        str_message = json.dumps(message).encode()
        exchange = await self._get_or_create_exchange(
            exchange_name=adapter_config.get("exchange", ""),
            exchange_type=adapter_config.get("exchange_type", ""),
        )
        await exchange.publish(
            aio_pika.Message(body=str_message), routing_key=routing_key.value
        )

    async def disconnect(self):
        await self.channel.close()

    async def _get_or_create_exchange(
        self, exchange_name: str, exchange_type: str
    ) -> AbstractExchange:
        exchange = await self.channel.get_exchange(exchange_name)
        if not exchange:
            return await self.channel.declare_exchange(
                exchange_name, type=exchange_type
            )
        return exchange

    async def _get_or_create_queue(self, queue_name: str, durable: bool):
        queue = await self.channel.get_queue(queue_name)
        if not queue:
            return await self.channel.declare_queue(queue_name, durable=durable)
        return queue
