import boto3
from typing import Optional


def read_s3_file(
    bucket: str,
    key: str,
    aws_region: Optional[str] = None
) -> str:
    """
    Read file content from S3.
    """

    s3 = boto3.client("s3", region_name=aws_region)

    try:
        obj = s3.get_object(Bucket=bucket, Key=key)
        return obj["Body"].read().decode("utf-8", errors="ignore")
    except Exception:
        return ""
