import os.path
from datetime import datetime, timezone
from itertools import chain
from typing import Generator, Final, Dict, List, Tuple, Any

import pandas as pd

from src.contexto.contexto import Contexto
from src.contexto.video_youtube import VideoYoutube
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

    def __obter_comentarios(self, id_video: str) -> Generator[dict, None, None]:
        comentarios = self.__servico_youtube.obter_comentarios_youtube(id_video=id_video)
        yield from comentarios

    def __gravar_comentarios(self, id_canal: str, id_video: str, comentario: Dict, id_comentario: str):

        caminho_bucket = os.path.join('bronze', 'comentarios', f'ano={self.__DATA_ATUAL.year}',
                                      f'mes={self.__DATA_ATUAL.month}', f'dia={self.__DATA_ATUAL.day}',
                                      f'id_canal={id_canal}', f'id_video={id_video}', f'id_comentario={id_comentario}',
                                      f'comentario_{int(datetime.now(timezone.utc).timestamp())}.json')
        comentario['data_hora_insercao'] = self.__DATA_ATUAL.strftime("%d/%m/%Y %H:%M:%S")
        self.__servico_gravacao_dados.salvar_dados(json_youtube=comentario, caminho=caminho_bucket)

    def varrer_comentarios_nao_gravados(self, contexto: Contexto) -> list[Tuple[str, str, str, str, str]]:
        lista_id_comentarios = []
        lista_videos = contexto['lista_videos']
        for video in chain.from_iterable(lista_videos):
            try:

                id_video = video["id"]["videoId"]
                titulo_video = video["snippet"]["title"]
                id_canal = video["snippet"]["channelId"]
                nome_canal = video["snippet"]["channelTitle"]
                print(video)

                comentarios = self.__obter_comentarios(id_video)
                for comentario in comentarios:
                    id_comentario = comentario["snippet"]["topLevelComment"]["id"]
                    comentario['nome_canal'] = nome_canal
                    comentario['titulo_video'] = titulo_video
                    self.__gravar_comentarios(id_canal=id_canal, comentario=comentario, id_video=id_video,
                                              id_comentario=id_comentario)
                    lista_id_comentarios.append((id_canal, nome_canal, id_video, titulo_video, id_comentario))
                return lista_id_comentarios
            except:
                continue
        return []

    def varrer_comentarios_gravados(self, dataframe: pd.DataFrame) -> List[Tuple[str, str, str, str, str]]:
        lista_id_comentarios = []
        for linha in dataframe.itertuples(index=False, name=None):
            video = VideoYoutube(*linha)
            id_canal = video.id_canal
            id_video = video.id_video
            titulo_video = video.titulo_video
            nome_canal = video.nome_canal
            print(id_video)
            comentarios = self.__obter_comentarios(id_video)

            for comentario in comentarios:
                print(comentario)
                id_comentario = comentario["snippet"]["topLevelComment"]["id"]
                self.__gravar_comentarios(id_canal=id_canal, id_video=id_video, id_comentario=id_comentario,
                                          comentario=comentario)
                lista_id_comentarios.append((id_canal, nome_canal, id_video, titulo_video, id_comentario))
        return lista_id_comentarios

    def executar_processo(self, contexto: Contexto) -> bool | None:
        lista_id_comentarios = self.varrer_comentarios_nao_gravados(contexto)
        print(f'lista_id_comentarios: {lista_id_comentarios}')
        try:


            if len(lista_id_comentarios) > 0:
                consulta = """
                SELECT DISTINCT   snippet.channelId as id_canal,  snippet.videoId as id_video, nome_canal, titulo_video
                FROM read_json_auto('s3://youtube/bronze/comentarios/ano=*/mes=*/dia=*/id_canal=*/id_video=*/id_comentario=*/comentario*.json');
                """

                try:
                    dataframe = self.__servico_gravacao_dados.consultar_dados(consulta)
                except Exception as e:
                    print(e)

                    dataframe = pd.DataFrame()

                if not dataframe.empty:
                    lista_id_comentarios_gravados = self.varrer_comentarios_gravados(dataframe)
                    lista_id_comentarios_completa = lista_id_comentarios_gravados + lista_id_comentarios
                    lista_id_comentarios_completa = list(set(lista_id_comentarios_completa))
                else:
                    lista_id_comentarios_completa = lista_id_comentarios
                contexto['lista_id_comentarios'] = lista_id_comentarios_completa
                return True
        except Exception as e:
            print(f'{e} _> erro ao recuperar comentáros ')

