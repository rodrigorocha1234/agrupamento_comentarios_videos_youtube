import os.path
from datetime import datetime, timezone
from itertools import chain
from typing import Generator, Final

from src.contexto.contexto import Contexto
from src.corrente.corrente import Corrente
from src.operacao.ioperacao import IOperacao
from src.servico.servico_api_youtube.iapi_youtube import IApiYoutube
from src.utils.servico_log.log_protocol import LogProtocol


class ObterListaComentarios(Corrente):
    def __init__(self, servico_log: LogProtocol, servico_youtube: IApiYoutube, servico_gravacao_dados: IOperacao):
        super().__init__(servico_log)
        self.__servico_youtube = servico_youtube
        self.__servico_gravacao_dados = servico_gravacao_dados
        self.__DATA_ATUAL: Final[datetime] = datetime.now()

    def __obter_comentarios(self, id_video: str):
        comentarios = self.__servico_youtube.obter_comentarios_youtube(id_video=id_video)
        yield from comentarios

    def __gravar_comentarios(self, caminho_gravacao: str, comentarios: Generator[dict, None, None]):
        for comentario in comentarios:
            print(comentario)
            comentario['data_hora_insercao'] = self.__DATA_ATUAL.strftime("%d/%m/%Y %H:%M:%S")
            self.__servico_gravacao_dados.salvar_dados(json_youtube=comentario, caminho=caminho_gravacao)
            self.__gravar_comentarios(caminho_gravacao=caminho_gravacao, comentarios=comentarios)

    def executar_processo(self, contexto: Contexto) -> bool:
        try:
            lista_videos = contexto['lista_videos']
            for video in chain.from_iterable(lista_videos):
                caminho_bucket = os.path.join('bronze', 'comentarios', f'id_canal={video["snippet"]["channelId"]}',
                    f'id_video={video["id"]["videoId"]}',
                    f'comentario_{int(datetime.now(timezone.utc).timestamp())}.json')

                print(video['snippet']['channelId'], '-', video['snippet']['channelTitle'], '-', video['id']['videoId'],
                      '-', video['snippet']['title'])
                comentarios = self.__obter_comentarios(video['id']['videoId'])
                self.__gravar_comentarios(caminho_gravacao=caminho_bucket, comentarios=comentarios)
            return True
        except:
            return False
