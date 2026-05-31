import os.path
from datetime import datetime, timezone
from itertools import chain
from typing import Generator, Final

from src.contexto.contexto import Contexto
from src.corrente.corrente import Corrente
from src.operacao.ioperacao import IOperacao
from src.servico.servico_api_youtube.iapi_youtube import IApiYoutube
from src.utils.servico_log.log_protocol import LogProtocol


class ObterListaRespostaComentariosCorrente(Corrente):
    def __init__(self, servico_log: LogProtocol, servico_youtube: IApiYoutube, servico_gravacao_dados: IOperacao):
        super().__init__(servico_log)
        self.__servico_youtube = servico_youtube
        self.__servico_gravacao_dados = servico_gravacao_dados
        self.__DATA_ATUAL: Final[datetime] = datetime.now()


    def executar_processo(self, contexto: Contexto) -> bool:
        try:
            lista_id_comentarios = contexto["lista_id_comentarios"]
            for id_canal, id_video, id_comentario in lista_id_comentarios:
                req_reposta_comentarios = self.__servico_youtube.obter_resposta_comentarios(id_comentario)
                for resposta_comentario in req_reposta_comentarios:
                    caminho_bucket = os.path.join('bronze', 'resposta_comentarios', f'id_canal={id_canal}',
                                                 f'id_video={id_video}',
                                                 f'id_comentario={id_comentario}',
                                                 f'id_resposta_comentario={resposta_comentario["id"]}',
                                                 f'comentario_{int(datetime.now(timezone.utc).timestamp())}.json')
                    self.__servico_gravacao_dados.salvar_dados(caminho=caminho_bucket, json_youtube=resposta_comentario)

            return True
        except:
            return False
