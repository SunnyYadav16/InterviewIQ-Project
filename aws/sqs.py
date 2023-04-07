"""AWS SQS service"""
import abc
import json
import logging
import sys
import traceback

from api.settings import SQS

from common.processors import ProcessorWorkManager

from .base import AWSBase


class AWSSQS(AWSBase):
    """AWS SNS class"""

    def __init__(self):
        super().__init__(SQS)
        logging.info("AWS SQS ready")


class SqsProcessor(abc.ABC):
    """Sqs abstract worker"""

    @abc.abstractmethod
    def process(self, message: dict) -> bool:
        """Process SQS message.

        :returns: True if messages sucesfully processed
        """
        pass


class SqsWorkManager(ProcessorWorkManager):
    """Sqs work manager"""

    def __init__(self, processor: SqsProcessor, queue_name: str, batch_size: int = 10):
        self._sqs = AWSSQS()
        self._processor = processor
        self._batch_size = batch_size
        self._wait_time_seconds = 20

        self._sqs.open()
        self._queue = self._sqs.resource.get_queue_by_name(QueueName=queue_name)

    def run(self):
        """Run Sqs manager"""
        messages = self._queue.receive_messages(
            MaxNumberOfMessages=self._batch_size,
            WaitTimeSeconds=self._wait_time_seconds,
        )
        for message in messages:
            try:
                message_body = json.loads(message.body)
                self._processor.process(message_body)
                message.delete()
            except Exception:
                logging.error(traceback.format_exception(*sys.exc_info()))

    def stop(self):
        self._sqs.close()
