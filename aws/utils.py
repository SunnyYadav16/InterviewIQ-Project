""" AWS utility functions """

from decouple import config


def get_url_for_aws_object(*filename):
    """Generate object url to AWS S3"""
    storage_bucket = config("AWS_STORAGE_BUCKET_NAME")
    aws_region = config("AWS_REGION_S3")
    return "https://{0}.s3-{1}.amazonaws.com/{2}".format(
        storage_bucket, aws_region, "/".join(filename)
    )
