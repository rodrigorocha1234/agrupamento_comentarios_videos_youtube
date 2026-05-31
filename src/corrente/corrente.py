from abc import ABC, abstractmethod
from typing import Optional

from src.contexto.contexto import Contexto
from src.utils.servico_log.log_protocol import LogProtocol


class Corrente(ABC):
    def __init__(self, servico_log: LogProtocol) -> None:
        self._proxima_corrente: Optional["Corrente"] = None
        self._servico_log = servico_log

    def set_proxima_corrente(self, corrente: "Corrente") -> "Corrente":
        """
        Define a próxima corrente da pipeline.
        Retorna a corrente passada para permitir encadeamento.
        :param corrente: Recebe a corrente que ser executada.
        :return: Retorna a próxima corrente passada para permitir encadeamento.
        """
        self._proxima_corrente = corrente
        return corrente

    def corrente(self, contexto: Contexto):
        """
        Executa o processo desta corrente.
        Se houver sucesso, passa para a próxima corrente (se existir).

        :param contexto: Classe de transporte que o pipeline vai usar

        """
        self._servico_log.info(f'Executando {self.__class__.__name__}')
        if self.executar_processo(contexto):
            self._servico_log.info(f'{self.__class__.__name__} -> Sucesso ao executar')
            if self._proxima_corrente:
                self._proxima_corrente.corrente(contexto)
            else:
                self._servico_log.info(f'{self.__class__.__name__} ->  Último handler da cadeia')
        else:
            self._servico_log.warning(f'{self.__class__.__name__} -> Falha, pipeline interrompido')


    @abstractmethod
    def executar_processo(self, contexto: Contexto) -> bool:
        """
        Deve ser implementado em cada corrente concreta.
        Retorna True se o processo foi bem-sucedido, False caso contrário.
        :param contexto:
        :return:
        """
        pass
