"""AWS SNS service"""
import json
import logging

from django.conf import settings

from .base import AWSBase
from .exceptions import AWSException


class AWSSNS(AWSBase):
    """AWS SNS class"""

    def __init__(self):
        super().__init__(settings.SNS)
        logging.info("AWS SNS ready")

    @classmethod
    def build_topic_arn(cls, topic_name):
        """Build topic arn"""
        if not topic_name:
            raise AWSException("topic_name must not be None or empty string")

        return "arn:aws:sns:{}:{}:{}".format(
            settings.AWS_DEFAULT_REGION, settings.AWS_ACCOUNT_ID, topic_name
        )

    def publish(self, topic_arn, message):
        """Publish message to SNS"""
        if not topic_arn:
            raise AWSException("topic_arn must not be None or empty string")

        if message is None:
            raise AWSException("message must not be None")

        try:
            logging.info("topic_arn: %s", topic_arn)
            return self.client.publish(TopicArn=topic_arn, Message=json.dumps(message))
        except Exception as ex:
            raise AWSException(ex)
