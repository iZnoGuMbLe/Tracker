import json

import aio_pika
from app.core import Settings
from app.broker import get_amqp_connection

class RabbitMQProducer:

    def __init__(self):
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await get_amqp_connection()
        self.channel = await self.connection.channel()


    async def publish_message(self,queue_name:str,message_body: dict):
        await self.channel.declare_queue(
            queue_name,
            durable=True
        )

        message = aio_pika.Message(
            body= json.dumps(message_body).encode(),
        )

        await self.channel.default_exchange.publish(
            message=message,
            routing_key=queue_name
        )

    async def close(self):
        if self.connection:
            await self.connection.close()


producer = RabbitMQProducer()

