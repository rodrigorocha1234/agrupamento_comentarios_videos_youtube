import os
from typing import Final


class Config:
    CHAVE_API_YOUTUBE : Final[str] = os.environ.get('CHAVE_API_YOUTUBE', "")