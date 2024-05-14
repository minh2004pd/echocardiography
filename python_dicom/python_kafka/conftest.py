import json
from datetime import datetime
import random
import asyncio
from consumer import KafkaEventConsumer
from producer import KafkaEventProducer
import uuid

consumer = KafkaEventConsumer(
    bootstrap_servers=["localhost:9092"],
    topics=["test_topic"],
    group="consumer_1"
)

producer = KafkaEventProducer(
    bootstrap_servers=["localhost:9092"],
    topic=["test_topic","test_topic_1"]
)

async def handle_message(message):
    offset = message.offset
    topic = message.topic
    partition = message.partition
    data = json.loads(message.value)
    print(offset, topic, partition, data)

    data = {
        "task_id": data["task_id"], 
        "service_type": "abc",
        "annotation": {}
    }
    await producer.flush(data, "test_topic_1")

    await consumer.commit(topic=topic, partition=partition, offset=offset)

async def main():
    await producer.start()
    data = {
        "task_id": str(uuid.uuid4()), 
        "image_type": "segmentation",
        "image_url": "url",
        "time": datetime.now().isoformat()
    }
    await producer.flush(data, "test_topic")

    consumer.handle = handle_message
    await consumer.start()
    
    await consumer.stop()
    await producer.stop()

asyncio.run(main())