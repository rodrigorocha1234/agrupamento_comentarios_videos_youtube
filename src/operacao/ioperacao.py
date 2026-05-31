from typing import Protocol, Any


class IOperacao(Protocol):

    def checar_conexao(self) -> bool:
        ...

    def salvar_dados(self, **kwargs: Any) -> None:
        ...