from typing import Callable

from src.utils.servico_log.log_protocol import LogProtocol


class LogFactory:

    _providers: dict[str, Callable[..., LogProtocol]] = {}

    @classmethod
    def register(
        cls,
        name: str,
        provider: Callable[..., LogProtocol]
    ) -> None:
        cls._providers[name] = provider

    @classmethod
    def create(
        cls,
        logger_type: str = "python",
        **kwargs
    ) -> LogProtocol:

        provider = cls._providers.get(logger_type)

        if provider is None:
            raise ValueError(
                f"Logger '{logger_type}' não registrado. "
                f"Disponíveis: {list(cls._providers.keys())}"
            )

        return provider(**kwargs)