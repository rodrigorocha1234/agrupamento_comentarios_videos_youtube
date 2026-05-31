import os
from typing import Final

from dotenv import load_dotenv

load_dotenv()


class Config:
    HOST_S3 = os.environ.get('MINIO_HOST')
    PORT_S3 = os.environ.get('MINIO_PORT')
    USER_S3 = os.environ.get('MINIO_ROOT_USER')
    PASSWORD_S3 = os.environ.get('MINIO_ROOT_PASSWORD')
    CHAVE_API_YOUTUBE: Final[str] = os.environ.get('CHAVE_API_YOUTUBE', "")

