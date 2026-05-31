from datetime import datetime
from typing import List, Generator

from src.contexto.contexto import Contexto
from src.corrente.corrente import Corrente
from src.servico.servico_api_youtube.iapi_youtube import IApiYoutube
from src.utils.servico_log.log_protocol import LogProtocol


class ObterListaVideosCorrente(Corrente):
    def __init__(self, servico_log: LogProtocol, servico_youtube: IApiYoutube):
        super().__init__(servico_log=servico_log)
        self.__servico_youtube = servico_youtube

    def __buscar_dados_videos_corrente(self, contexto: Contexto) -> List[Generator[dict, None, None]] | None:
        lista_id_canais = contexto['lista_id_canais']
        data_hora_busca = contexto['data_hora_anterior']
        if isinstance(data_hora_busca, datetime):
            lista_videos = [self.__servico_youtube.obter_video_por_data(id_canal=id_canal, data_inicio=data_hora_busca)
                for id_canal in lista_id_canais]
            return lista_videos
        return None

    def executar_processo(self, contexto: Contexto) -> bool:
        gerador_videos = self.__buscar_dados_videos_corrente(contexto)
        if gerador_videos:
            contexto['lista_videos'] = gerador_videos
            return True
        return False
