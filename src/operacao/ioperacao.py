from typing import Protocol, Any

import pandas as pd


class IOperacao(Protocol):

    def checar_conexao(self) -> bool:
        ...

    def salvar_dados(self, **kwargs: Any) -> None:
        ...

    def consultar_dados(self, consulta: str) -> pd.DataFrame:
        ...
