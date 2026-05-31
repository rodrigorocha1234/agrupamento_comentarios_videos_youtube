from typing import Protocol, Any, List


class IOperacao(Protocol):

    def checar_conexao(self) -> bool:
        ...

    def salvar_dados(self, **kwargs: Any) -> None:
        ...

    def consultar_dados(self) -> List[str]:
        ...
