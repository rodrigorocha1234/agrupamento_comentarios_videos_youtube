import logging
import pytest
from unittest.mock import patch, MagicMock
from src.utils.servico_log.conexto_log_params import ContextoLogFilter
from src.utils.servico_log.log_factory import LogFactory
from src.utils.servico_log.log_protocol import LogProtocol
from src.utils.servico_log.python_log import PythonLog


# 1. Testes para o ContextoLogFilter
def test_contexto_log_filter_adds_missing_attributes():
    """
    Testa se o filtro adiciona os atributos padrão ('descricao', 'url', 'codigo',
    'requisicao') com valores vazios quando eles não estão presentes no registro.
    """
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test_path.py",
        lineno=10,
        msg="Teste de mensagem",
        args=(),
        exc_info=None
    )
    
    # Verifica que antes do filtro os atributos não existem
    assert not hasattr(record, "descricao")
    assert not hasattr(record, "url")
    assert not hasattr(record, "codigo")
    assert not hasattr(record, "requisicao")

    filter_instance = ContextoLogFilter()
    result = filter_instance.filter(record)

    # Verifica se o filtro retornou True e os atributos foram adicionados
    assert result is True
    assert record.descricao == ""
    assert record.url == ""
    assert record.codigo == ""
    assert record.requisicao == ""


def test_contexto_log_filter_preserves_existing_attributes():
    """
    Testa se o filtro preserva os valores de atributos de contexto já existentes.
    """
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="test_path.py",
        lineno=10,
        msg="Teste de mensagem",
        args=(),
        exc_info=None
    )
    # Define valores explícitos
    record.descricao = "Operação de teste"
    record.url = "https://api.youtube.com"
    record.codigo = 200
    record.requisicao = {"param": "value"}

    filter_instance = ContextoLogFilter()
    result = filter_instance.filter(record)

    assert result is True
    assert record.descricao == "Operação de teste"
    assert record.url == "https://api.youtube.com"
    assert record.codigo == 200
    assert record.requisicao == {"param": "value"}


# 2. Testes para LogFactory
class MockLogger(LogProtocol):
    """Logger mockado para testar a fábrica."""
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def debug(self, msg, *args, **kwargs) -> None: pass
    def info(self, msg, *args, **kwargs) -> None: pass
    def warning(self, msg, *args, **kwargs) -> None: pass
    def error(self, msg, *args, **kwargs) -> None: pass
    def critical(self, msg, *args, **kwargs) -> None: pass


def test_log_factory_register_and_create():
    """
    Testa o registro de novos providers de logger na fábrica e a criação de instâncias.
    """
    LogFactory.register("mock_type", lambda **kwargs: MockLogger(**kwargs))
    
    logger = LogFactory.create("mock_type", custom_param="hello")
    
    assert isinstance(logger, MockLogger)
    assert logger.kwargs == {"custom_param": "hello"}


def test_log_factory_raises_error_when_unregistered():
    """
    Testa se um ValueError é lançado ao tentar obter um logger de tipo não registrado.
    """
    with pytest.raises(ValueError) as excinfo:
        LogFactory.create("invalid_type")
    
    assert "Logger 'invalid_type' não registrado" in str(excinfo.value)


# 3. Testes para PythonLog
@patch("src.utils.servico_log.python_log.RotatingFileHandler")
@patch("src.utils.servico_log.python_log.logging.StreamHandler")
def test_python_log_initialization_and_methods(mock_stream_handler, mock_rotating_handler):
    """
    Testa se a inicialização do PythonLog configura os handlers e delega 
    corretamente as chamadas de log para o logger interno da biblioteca padrão.
    """
    mock_logger = MagicMock()
    # Simula que o logger não possui nenhum handler cadastrado
    mock_logger.handlers = []

    with patch("src.utils.servico_log.python_log.logging.getLogger", return_value=mock_logger):
        python_log = PythonLog(nome_arquivo="teste_unitario", level_mensagem=logging.DEBUG)

        # Verifica se o nível do logger foi configurado
        mock_logger.setLevel.assert_called_with(logging.DEBUG)

        # Verifica se os handlers de console e arquivo rotativo foram anexados
        mock_logger.addHandler.assert_any_call(mock_stream_handler.return_value)
        mock_logger.addHandler.assert_any_call(mock_rotating_handler.return_value)
        mock_logger.addFilter.assert_called_once()

        # Testa a delegação das chamadas de log de diferentes níveis
        python_log.info("Teste de info")
        mock_logger.info.assert_called_with("Teste de info", stacklevel=2)

        python_log.error("Teste de erro")
        mock_logger.error.assert_called_with("Teste de erro", stacklevel=2)

        python_log.warning("Teste de aviso")
        mock_logger.warning.assert_called_with("Teste de aviso", stacklevel=2)

        python_log.debug("Teste de depuração")
        mock_logger.debug.assert_called_with("Teste de depuração", stacklevel=2)

        python_log.critical("Teste crítico")
        mock_logger.critical.assert_called_with("Teste crítico", stacklevel=2)
