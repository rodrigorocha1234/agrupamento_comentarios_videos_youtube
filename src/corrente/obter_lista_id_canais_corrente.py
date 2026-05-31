from typing import List

from src.contexto.contexto import Contexto
from src.corrente.corrente import Corrente
from src.servico.servico_api_youtube.iapi_youtube import IApiYoutube
from src.utils.servico_log.log_protocol import LogProtocol


class ObterListaIDCanaisCorrente(Corrente):
    def __init__(self, servico_log: LogProtocol, lista_canais: List[str], servico_youtube: IApiYoutube):
        super().__init__(servico_log)
        self.__lista_canais = lista_canais
        self.__servico_youtube = servico_youtube

    def __buscar_id_canais(self) -> List[str]:
        lista_id_canais: List[str] = []
        for canal in self.__lista_canais:
            resultado = self.__servico_youtube.obter_id_canal(canal)
            if resultado is None:
                continue
            canal_id, _ = resultado
            self._servico_log.info(f"Obtenido canal {canal_id}")
            lista_id_canais.append(canal_id)
        return lista_id_canais

    def executar_processo(self, contexto: Contexto) -> bool:
        try:
            lista_id_canais = self.__buscar_id_canais()
            contexto['lista_id_canais'] = lista_id_canais
            self._servico_log.info(f"Sucesso ao obter os canais")
            return True
        except:
            self._servico_log.error("Falha ao obter os canais")
            return False
