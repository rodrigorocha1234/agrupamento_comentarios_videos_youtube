from typing import Any, Protocol


class LogProtocol(Protocol):

    def debug(self, msg: Any, *args: Any, **kwargs: Any) -> None:
        ...

    def info(self, msg: Any, *args: Any, **kwargs: Any) -> None:
        ...

    def warning(self, msg: Any, *args: Any, **kwargs: Any) -> None:
        ...

    def error(self, msg: Any, *args: Any, **kwargs: Any) -> None:
        ...

    def critical(self, msg: Any, *args: Any, **kwargs: Any) -> None:
        ...
