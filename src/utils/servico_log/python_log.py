import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

from src.utils.servico_log.log_protocol import LogProtocol


class PythonLog(LogProtocol):

    def __init__(
        self,
        nome_arquivo: str = "extracao",
        level_mensagem: int = logging.INFO,
    ):

        root_dir = Path(__file__).resolve().parent.parent.parent.parent
        log_dir = root_dir / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        logger = logging.getLogger(nome_arquivo)
        logger.setLevel(level_mensagem)

        if not logger.handlers:
            formatter = logging.Formatter(
                fmt=(
                    "%(asctime)s | "
                    "%(levelname)-8s | "
                    "module=%(module)s | "
                    "logger=%(name)s | "
                    "method=%(funcName)s | "
                    "line=%(lineno)d | "
                    "%(message)s"
                ),
                datefmt="%Y-%m-%d %H:%M:%S"
            )

            console = logging.StreamHandler()
            console.setFormatter(formatter)

            file = RotatingFileHandler(
                log_dir / f"{nome_arquivo}.log",
                maxBytes=10 * 1024 * 1024,
                backupCount=5,
                encoding="utf-8"
            )
            file.setFormatter(formatter)

            logger.addHandler(console)
            logger.addHandler(file)

        self._logger = logger

    def info(self, msg, *args, **kwargs):
        self._logger.info(msg, *args, stacklevel=2, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._logger.error(msg, *args, stacklevel=2, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._logger.warning(msg, *args, stacklevel=2, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self._logger.debug(msg, *args, stacklevel=2, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self._logger.critical(msg, *args, stacklevel=2, **kwargs)