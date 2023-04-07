"""AWS S3 service"""
import logging
import os
import zipfile
from io import BytesIO

from django.conf import settings

from aws.base import AWSBase


class AWSS3(AWSBase):
    """AWS S3 class"""

    def __init__(self):
        super().__init__(settings.S3)
        logging.info("AWS S3 ready")

    def generate_presigned_url(self, key):
        """Get presigned url

        Keyword arguments:
            key -- object name
        """
        logging.info("Generating AWS S3 signed get url for %s object", key)
        return self.client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": settings.AWS_BUCKET_NAME, "Key": str(key)},
        )

    def generate_presigned_post(self, key, is_public):
        """Get presigned post

        Keyword arguments:
            key -- object name
            is_public -- boolean flag if object should be public on s3
        """
        logging.info("Generating AWS S3 signed post url for %s object", key)
        fields = None
        conditions = None
        if is_public:
            logging.info("Object should be public")
            fields = {"acl": "public-read"}
            conditions = [{"acl": "public-read"}]

        return self.client.generate_presigned_post(
            Bucket=settings.AWS_BUCKET_NAME,
            Key=key,
            Fields=fields,
            Conditions=conditions,
        )

    def generate_presigned_put(self, key, obj_type, is_public):
        """Get presigned put

        Keyword arguments:
            key -- object name
            obj_type -- object type: jpeg, png
            is_public -- boolean flag if object should be public on s3
        """
        logging.info(
            "Generating AWS S3 signed put url for %s object with type %s", key, obj_type
        )

        params = {
            "Bucket": settings.AWS_BUCKET_NAME,
            "Key": key,
            "ContentType": obj_type,
        }
        if is_public:
            logging.info("Object should be public")
            params.update({"ACL": "public-read"})

        return self.client.generate_presigned_url(
            ClientMethod="put_object", Params=params
        )

    def delete_object(self, key):
        """Delete object from S3

        Keyword arguements:

        key -- full path to file
        """
        logging.info(
            "Removing object from S3 in bucket name: %s with key: %s",
            settings.AWS_BUCKET_NAME,
            key,
        )
        self.client.delete_object(Bucket=settings.AWS_BUCKET_NAME, Key=key)

    def delete_objects(self, keys):
        """Delete objects from S3

        Keyword arguements:

        keys -- list of full path to file
        """
        logging.info(
            "Removing objects from S3 in bucket name: %s and %d keys",
            settings.AWS_BUCKET_NAME,
            len(keys),
        )

        delete_objs = {}
        delete_objs["Objects"] = [{"Key": key} for key in keys]

        self.client.delete_objects(Bucket=settings.AWS_BUCKET_NAME, Delete=delete_objs)

    def get_object(self, key, bucket_name=settings.AWS_BUCKET_NAME):
        """Get brand affiliation object that will be used for seed
        brand affiliation types into database

        Keyword args:
            key - key for certain resource
            bucket_name - name of bucket
        """
        return self.client.get_object(Bucket=bucket_name, Key=key)

    def get_list_objects(self, key):
        """Get list of objects from specifi path.

        Keyword argument:
            key - path to folder inside bucket
        """
        logging.info("Get list of items from S3: %s", key)
        objects = self.client.list_objects(Bucket=settings.AWS_BUCKET_NAME, Prefix=key)

        return objects.get("Contents", [])

    def upload_file_content(
        self, data, file_path, bucket_name=settings.AWS_BUCKET_NAME
    ):
        """Upload file to S3 bucket"""
        logging.info("Uploading file to S3")

        file_obj = BytesIO()
        file_obj.write(data)
        file_obj.seek(0)

        self.client.upload_fileobj(
            file_obj,
            bucket_name,
            file_path,
            ExtraArgs={"ACL": "public-read", "ContentType": "text/xml"},
        )
        file_url = "{0}/{1}/{2}".format(
            self.client.meta.endpoint_url, bucket_name, file_path
        )

        return file_url

    def get_objects_and_save_to_zip(self, zip_path, keys, key_map):
        """Set files in zip using provided keys

        :zip_path: file path where to save downloaded files
        :keys: list of aws object keys
        :key_map: mapper for key file names
        """
        file_paths = []
        try:
            with zipfile.ZipFile(zip_path, "w") as zipf:
                for fpath in keys:
                    try:
                        # Take last part of file path as a name or read from
                        current_file = key_map.get(fpath, fpath.split("/")[-1])
                        file_paths.append(current_file)

                        # Read file from S3
                        file_obj = self.get_object(fpath)

                        # Write to the local file so zipfile object can read it
                        with open(current_file, "wb") as local_file:
                            local_file.write(file_obj["Body"].read())

                            # Write to zipfile object
                            zipf.write(current_file)

                            # We do not need this file anymore.
                            os.unlink(current_file)
                            file_paths.remove(current_file)
                    except Exception as ex:
                        logging.error(ex)
        finally:
            # In case of exception remove temp local files
            for file_path in file_paths:
                try:
                    os.unlink(file_path)
                except FileNotFoundError:
                    logging.warning("File not found %s", file_path)
