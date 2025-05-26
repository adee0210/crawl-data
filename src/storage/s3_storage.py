import boto3
from botocore.exceptions import ClientError
from src.utils.logger import get_logger

logger = get_logger(__name__)


def upload_to_s3(file_path, bucket_name):
    try:
        s3_client = boto3.client("s3")
        file_name = file_path.split("/")[-1]
        s3_client.upload_file(file_path, bucket_name, f"football-data/{file_name}")
        logger.info(f"Uploaded {file_name} to S3 bucket {bucket_name}")
    except ClientError as e:
        logger.error(f"Error uploading to S3: {str(e)}")
        raise
