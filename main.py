from src.contexto.contexto import Contexto
from src.corrente.obter_dia_anterior_corrente import ObterDiaAnteriorCorrente
from src.corrente.obter_lista_id_canais_corrente import ObterListaIDCanaisCorrente
from src.servico.servico_api_youtube.api_youtube import YoutubeAPI
from src.utils.servico_log.log_factory import LogFactory
from src.utils.servico_log.python_log import PythonLog

LogFactory.register("python", lambda **kwargs: PythonLog(**kwargs))

logger = LogFactory.create(logger_type="python", nome_arquivo="etl")

contexto = Contexto(data_hora_anterior="", lista_id_canais=[])
servico_youtube = YoutubeAPI(servico_log=logger)
lista_id_canais = ['@jogatinaepica']

p1 = ObterDiaAnteriorCorrente(servico_log=logger)
p2 = ObterListaIDCanaisCorrente(servico_log=logger, lista_canais=lista_id_canais, servico_youtube=servico_youtube)
p1.set_proxima_corrente(p2)
p1.corrente(contexto=contexto)