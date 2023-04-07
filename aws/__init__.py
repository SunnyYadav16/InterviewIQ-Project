"""AWS"""

from django.conf.settings import PUBLISH_TO_SNS, S3, SES, SNS, SNS_PREFIX, SQS

from .exceptions import AWSException

__all__ = [
    "SNS_PREFIX",
    "PUBLISH_TO_SNS",
    "AWSException",
    "S3",
    "SES",
    "SNS",
    "SQS",
]
