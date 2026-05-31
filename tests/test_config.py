import os
import importlib
from unittest.mock import patch
from src.config import config


def test_config_loads_environment_variable():
    """
    Testa se a classe Config carrega corretamente o valor de CHAVE_API_YOUTUBE
    quando a variável de ambiente correspondente está presente.
    """
    with patch("dotenv.load_dotenv"), patch.dict(os.environ, {"CHAVE_API_YOUTUBE": "chave_de_teste_123"}):
        importlib.reload(config)
        assert config.Config.CHAVE_API_YOUTUBE == "chave_de_teste_123"


def test_config_defaults_to_empty_string():
    """
    Testa se a classe Config assume uma string vazia como padrão
    caso a variável de ambiente CHAVE_API_YOUTUBE não esteja definida.
    """
    # Removemos temporariamente a variável do ambiente e mockamos load_dotenv
    # para que ele não leia o arquivo .env físico do disco durante o reload.
    with patch("dotenv.load_dotenv"), patch.dict(os.environ, {}, clear=True):
        importlib.reload(config)
        assert config.Config.CHAVE_API_YOUTUBE == ""
