from datetime import datetime, UTC, timedelta

from src.contexto.contexto import Contexto
from src.corrente.corrente import Corrente
from src.utils.servico_log.log_protocol import LogProtocol


class ObterDiaAnteriorCorrente(Corrente):
    def __init__(self, servico_log: LogProtocol):
        super().__init__(servico_log=servico_log)

    @staticmethod
    def __obter_dia_anterior() -> datetime:
        data_hora_anterior = datetime.now() - timedelta(days=1)

        return data_hora_anterior

    def executar_processo(self, contexto: Contexto) -> bool:
        data_hora_anterior = self.__obter_dia_anterior()
        self._servico_log.info(f"Dia anterior: {data_hora_anterior}")
        contexto['data_hora_anterior'] = data_hora_anterior
        return True
