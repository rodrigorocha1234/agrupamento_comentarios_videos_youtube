from src.contexto.contexto import Contexto
from src.corrente.obter_dia_anterior_corrente import ObterDiaAnteriorCorrente
from src.utils.servico_log.log_factory import LogFactory
from src.utils.servico_log.python_log import PythonLog

LogFactory.register("python", lambda **kwargs: PythonLog(**kwargs))

logger = LogFactory.create(logger_type="python", nome_arquivo="etl")

contexto = Contexto(data_hora_anterior="")

id_canal = ""

p1 = ObterDiaAnteriorCorrente(servico_log=logger)
p1.corrente(contexto=contexto)