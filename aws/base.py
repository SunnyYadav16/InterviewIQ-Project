"""AWS Base"""
import logging

import boto3
import botocore
from django.conf import settings


class AWSBase:
    """AWS base class"""

    def __init__(self, connection_type):
        """Initialize AWS S3 class with connection to s3

        Keyword arguments:
            connection_type -- Connection type to AWS: s3, ses, sns
        """
        self.connection_type = connection_type
        self.client = None
        self.resource = None

    def _set_aws_region(self):
        """Set AWS region based on connection type"""
        if self.connection_type == settings.S3:
            return settings.AWS_REGION_S3
        if self.connection_type == settings.SES:
            return settings.AWS_REGION_SES

        return settings.AWS_DEFAULT_REGION

    def _build_aws_config(self) -> dict:
        """Build AWS Config"""
        aws_region = self._set_aws_region()
        aws_endpoint_url = settings.AWS_ENDPOINT_URLS.get(self.connection_type)

        connection_defualts = {"region_name": aws_region}

        if aws_endpoint_url:
            connection_defualts["endpoint_url"] = aws_endpoint_url

        return connection_defualts

    def open(self):
        """Open connection"""
        connection_defualts = self._build_aws_config()
        logging.info(
            "Opening connection to AWS %s for region %s",
            self.connection_type,
            connection_defualts["region_name"],
        )

        self._set_resource(connection_defualts)
        self._set_client(connection_defualts)

    def _set_resource(self, connection_defualts):
        """Set boto3 resource"""
        if not self._connection_type_has_resource():
            return

        self.resource = boto3.resource(
            self.connection_type,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            config=botocore.client.Config(None, signature_version="s3v4"),
            **connection_defualts
        )

    def _set_client(self, connection_defualts):
        """Set boto3 client"""
        if self.resource:
            self.client = self.resource.meta.client
        else:
            self.client = boto3.client(
                self.connection_type,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                config=botocore.client.Config(None, signature_version="s3v4"),
                **connection_defualts
            )

    def _connection_type_has_resource(self):
        """Connection type has resource obj"""
        return self.connection_type not in [settings.SES]

    def close(self):
        """Close connection"""
        logging.info("Close connection to AWS %s", self.connection_type)
        self.resource = None
        self.client = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *args):
        self.close()
