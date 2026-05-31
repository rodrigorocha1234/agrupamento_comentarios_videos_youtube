from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Tuple, Dict, Any


TDriver = TypeVar("TDriver")


class IDbConfig(ABC, Generic[TDriver]):

    @abstractmethod
    def obter_driver(self) -> TDriver:
        raise NotImplementedError

    @abstractmethod
    def obter_parametros_conexao(self) -> Tuple[Tuple[Any, ...], Dict[str, Any]]:
        raise NotImplementedError