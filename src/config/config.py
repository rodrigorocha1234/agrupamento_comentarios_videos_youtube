import os
from typing import Final

from dotenv import load_dotenv

load_dotenv()


class Config:
    CHAVE_API_YOUTUBE: Final[str] = os.environ.get('CHAVE_API_YOUTUBE', "")

