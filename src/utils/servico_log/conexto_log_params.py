import logging


class ContextoLogFilter(logging.Filter):

    def filter(self, record : logging.LogRecord) -> bool:
        record.descricao = getattr(record, "descricao", "")
        record.url = getattr(record, "url", "")
        record.codigo = getattr(record, "codigo", "")
        record.requisicao = getattr(record, "requisicao", "")
        return True
