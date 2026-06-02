from src.armazenamento_s3.db_config_minio import ConfigS3Minio
from src.armazenamento_s3.operacao_minio_s3 import OperacaoMInioS3
from src.contexto.contexto import Contexto
from src.corrente.obter_dia_anterior_corrente import ObterDiaAnteriorCorrente
from src.corrente.obter_lista_comentarios import ObterListaComentarios
from src.corrente.obter_lista_id_canais_corrente import ObterListaIDCanaisCorrente
from src.corrente.obter_lista_resposta_comentarios_corrente import ObterListaRespostaComentariosCorrente
from src.corrente.obter_lista_videos_corrente import ObterListaVideosCorrente
from src.servico.servico_api_youtube.api_youtube import YoutubeAPI
from src.utils.servico_log.log_factory import LogFactory
from src.utils.servico_log.python_log import PythonLog

LogFactory.register("python", lambda **kwargs: PythonLog(**kwargs))

logger = LogFactory.create(logger_type="python", nome_arquivo="etl")

contexto = Contexto(data_hora_anterior=None, lista_id_canais=[], lista_videos=[], lista_id_comentarios=[])
servico_youtube = YoutubeAPI(servico_log=logger)
lista_id_canais = [
    '@jogatinaepica', # x
    '@CKXgameplay',
    '@PalaDinXPG',
    '@CanaldoVoid',
    '@ChratosGameplay',
    '@cmdrleonerd',
    '@100choro-Belém-Brasil',
    '@RenatoAugustoTech',
    '@GutoGalego'

]
dias_anterior = 7

conexao_s3 = ConfigS3Minio()

operacao_s3 = OperacaoMInioS3(conexao_s3=conexao_s3)


p1 = ObterDiaAnteriorCorrente(servico_log=logger, dias_anterior=dias_anterior)
p2 = ObterListaIDCanaisCorrente(servico_log=logger, lista_canais=lista_id_canais, servico_youtube=servico_youtube)
p3 = ObterListaVideosCorrente(servico_log=logger, servico_youtube=servico_youtube)
p4 = ObterListaComentarios(servico_log=logger, servico_youtube=servico_youtube, servico_gravacao_dados=operacao_s3)
p5 = ObterListaRespostaComentariosCorrente(servico_log=logger, servico_youtube=servico_youtube, servico_gravacao_dados=operacao_s3)
p1.set_proxima_corrente(p2) \
    .set_proxima_corrente(p3) \
    .set_proxima_corrente(p4)
    # .set_proxima_corrente(p5)
p1.corrente(contexto=contexto)

