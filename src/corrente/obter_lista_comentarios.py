from itertools import chain
from typing import Generator, List, Dict

from src.contexto.contexto import Contexto
from src.corrente.corrente import Corrente
from src.servico.servico_api_youtube.iapi_youtube import IApiYoutube
from src.utils.servico_log.log_protocol import LogProtocol


class ObterListaComentarios(Corrente):
    def __init__(self, servico_log: LogProtocol, servico_youtube: IApiYoutube):
        super().__init__(servico_log)
        self.__servico_youtube = servico_youtube

    def __obter_comentarios(self, lista_videos: List[Generator[Dict, None, None]]):
        for video in chain.from_iterable(lista_videos):
            print(video['snippet']['channelId'], '-', video['snippet']['channelTitle'], '-', video['id']['videoId'],
                  '-', video['snippet']['title'])
            comentarios = self.__servico_youtube.obter_comentarios_youtube(id_video=video['id']['videoId'])
            for comentario in comentarios:
                print(comentario)

    def executar_processo(self, contexto: Contexto) -> bool:
        lista_video = contexto['lista_videos']
        self.__obter_comentarios(lista_video)
        return True
