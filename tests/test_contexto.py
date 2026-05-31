from datetime import datetime
from src.contexto.contexto import Contexto


def test_contexto_creation():
    """
    Testa a criação de uma instância de Contexto com valores válidos,
    garantindo que se comporte como um dicionário Python padrão.
    """
    contexto = Contexto(data_hora_anterior=None, lista_id_canais=["canal_123"])
    assert contexto["data_hora_anterior"] is None
    assert contexto["lista_id_canais"] == ["canal_123"]


def test_contexto_with_datetime():
    """
    Testa a criação de uma instância de Contexto contendo um datetime
    no campo data_hora_anterior.
    """
    now = datetime.now()
    contexto = Contexto(data_hora_anterior=now, lista_id_canais=[])
    assert contexto["data_hora_anterior"] == now
    assert isinstance(contexto["lista_id_canais"], list)
    assert len(contexto["lista_id_canais"]) == 0
