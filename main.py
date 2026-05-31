from src.utils.servico_log.log_factory import LogFactory
from src.utils.servico_log.python_log import PythonLog

LogFactory.register("python", lambda **kwargs: PythonLog(**kwargs))

logger = LogFactory.create(logger_type="python", nome_arquivo="etl")


def registrar_log():
    logger.info("Processamento iniciado")
    logger.error("Processamento erro")


registrar_log()
