import asyncio
import json

from aiokafka import AIOKafkaConsumer
from aiokafka.structs import TopicPartition
from ports.event_consumer import EventConsumer


class KafkaEventConsumer(EventConsumer):

    def __init__(
        self,
        bootstrap_servers,
        topics,
        group,
        log_service=None,
        service=None,
        listeners=None,
    ):
        super().__init__(
            log_service=log_service,
            service=service,
            listeners=listeners
        )

        self.bootstrap_servers = bootstrap_servers
        self.topics = topics
        self.group = group

        self.consumer_connected = False
        self.consumer_stopped = False
        self.consumer = None
        self.consuming = False

    async def handle(self, message):
        """
        Handle a message.
        """
        message = json.loads(message.value)
        print(message)

        # await super().handle(message)

    async def commit(self, topic, partition, offset):
        metadata = "Some utf-8 metadata"
        tp = TopicPartition(topic, partition)

        await self.consumer.commit({tp: (offset+1, metadata)})

    async def start(self):
        await self._create_consumer()
        await self._connect()
        await self._start_consuming()

    async def stop(self):
        print("Stop consuming!")
        await self._stop_consuming()
        await self._disconnect()

    async def _create_consumer(self):
        self.consumer = \
            AIOKafkaConsumer(
                *self.topics,
                loop=asyncio.get_event_loop(),
                bootstrap_servers=self.bootstrap_servers,
                group_id=self.group,
                enable_auto_commit=False,
                auto_offset_reset="earliest"
            )

    async def _connect(self):

        created = False
        error = None
        backoff = 6
        retries = 0
        max_retries = 3

        while (not created) and (retries < max_retries):
            try:
                await self.consumer.start()
                self.consumer_connected = True
                created = True
                print("Consumer connected!")

            except Exception as e:
                # self.log_service.error(
                #     (
                #         "{} failed to connect to: {} "
                #         "(retrying in {} secs..), exception: {}"
                #     ).format(
                #         "Kafka Event Adapter",
                #         self.bootstrap_servers,
                #         backoff,
                #         str(e)
                #     )
                # )
                print(e)
                error = str(e)
                retries += 1
                await asyncio.sleep(backoff)

        if not created:
            raise Exception(
                (
                    "{} failed to connect to: {} "
                    "after {} retries, error: {}."
                ).format(
                    "Kafka Event Adapter",
                    self.bootstrap_servers,
                    retries,
                    error
                )
            )

        await self._wait_for_connect()

    async def _wait_for_connect(self, timeout=60):
        
        waited = 0

        while not self.consumer_connected:
            
            await asyncio.sleep(1)
            waited = waited + 1

            if waited > timeout:
                raise Exception(
                    "Couldn't connect to kafka, timed out after {} secs".
                    format(
                        timeout
                    )
                )

    async def _start_consuming(self):
        # Schedule in a new task on the event loop to prevent blocking
        await asyncio.get_event_loop().create_task(
            self._consume()
        )

    async def _consume(self):
        self.consuming = True
        print("start comsuming!")
        self.consumer_stopped = False
        while not self.consumer_stopped:
            try:
                message = await asyncio.wait_for(
                    self.consumer.__anext__(),
                    timeout=10.0
                )
                try:
                    await self.handle(message)
                except Exception as e:
                    # self.log_service.error(
                    #     f"Kafka Event Adapter got exception when "
                    #     f"delegating call to service: '{str(e)}'.",
                    #     exc_info=True,
                    # )
                    print("error: ", e)
                # await self.consumer.commit()
            except asyncio.TimeoutError:
                # break
                pass
        self.consuming = False

    async def _stop_consuming(self):
        self.consumer_stopped = True
        await self.wait_for_consumption_to_stop()

    async def wait_for_consumption_to_stop(self, timeout=60):
        
        waited = 0

        while self.consuming:

            await asyncio.sleep(1)
            waited = waited + 1

            if waited > timeout:
                raise Exception(
                    (
                        "Failed waiting for consumption to stop, "
                        "timed out after {} secs"
                    ).format(
                        timeout
                    )
                )

    async def _disconnect(self):
        # Will leave consumer group; perform autocommit if enabled.
        await self.consumer.stop()

        self.consumer_connected = False

    async def _wait_for_disconnect(self, timeout=60):
        
        waited = 0

        while self.consumer_connected:

            await asyncio.sleep(1)
            
            waited = waited + 1
            
            if waited > timeout:
                raise Exception(
                    (
                        "Couldn't disconnect from kafka, timed out "
                        "after {} secs"
                    ).format(
                        timeout
                    )
                )