from datetime import datetime, timedelta
from unittest.mock import MagicMock
from src.contexto.contexto import Contexto
from src.corrente.corrente import Corrente
from src.corrente.obter_dia_anterior_corrente import ObterDiaAnteriorCorrente
from src.corrente.obter_lista_id_canais_corrente import ObterListaIDCanaisCorrente
from src.servico.servico_api_youtube.iapi_youtube import IApiYoutube
from src.utils.servico_log.log_protocol import LogProtocol


class MockLogger(LogProtocol):
    def __init__(self):
        self.info = MagicMock()
        self.error = MagicMock()
        self.warning = MagicMock()
        self.debug = MagicMock()
        self.critical = MagicMock()



# 1. Classe de Mock Concreto para testar a base abstrata Corrente
class DummyCorrente(Corrente):
    def __init__(self, servico_log, success=True):
        super().__init__(servico_log)
        self.success = success
        self.executed = False

    def executar_processo(self, contexto: Contexto) -> bool:
        self.executed = True
        return self.success


def test_corrente_chaining_and_execution_success():
    """
    Testa se o encadeamento e execução da corrente funcionam em caso de sucesso.
    """
    log_mock = MockLogger()
    c1 = DummyCorrente(log_mock, success=True)
    c2 = DummyCorrente(log_mock, success=True)

    # Verifica o retorno de set_proxima_corrente (fluent interface)
    returned = c1.set_proxima_corrente(c2)
    assert returned is c2
    assert c1._proxima_corrente is c2

    contexto = Contexto(data_hora_anterior=None, lista_id_canais=[])
    c1.corrente(contexto)

    # Ambos os handlers devem ser executados
    assert c1.executed is True
    assert c2.executed is True

    # Verifica os logs de informação gerados no fluxo
    log_mock.info.assert_any_call("Executando DummyCorrente")
    log_mock.info.assert_any_call("DummyCorrente -> Sucesso ao executar")
    log_mock.info.assert_any_call("DummyCorrente ->  Último handler da cadeia")


def test_corrente_chaining_interrupted_on_failure():
    """
    Testa se o pipeline de execução da corrente é interrompido em caso de falha de um handler.
    """
    log_mock = MockLogger()
    c1 = DummyCorrente(log_mock, success=False)
    c2 = DummyCorrente(log_mock, success=True)

    c1.set_proxima_corrente(c2)

    contexto = Contexto(data_hora_anterior=None, lista_id_canais=[])
    c1.corrente(contexto)

    # O primeiro handler executa e falha, o segundo não deve ser executado
    assert c1.executed is True
    assert c2.executed is False
    log_mock.warning.assert_called_with("DummyCorrente -> Falha, pipeline interrompido")


# 2. Testes para ObterDiaAnteriorCorrente
def test_obter_dia_anterior_corrente():
    """
    Testa se a corrente ObterDiaAnteriorCorrente calcula corretamente o dia anterior
    e o salva no dicionário de contexto.
    """
    log_mock = MockLogger()
    corrente = ObterDiaAnteriorCorrente(log_mock)

    contexto = Contexto(data_hora_anterior=None, lista_id_canais=[])
    result = corrente.executar_processo(contexto)

    assert result is True
    assert contexto["data_hora_anterior"] is not None
    assert isinstance(contexto["data_hora_anterior"], datetime)

    # Valida se a hora obtida está aproximadamente 24 horas no passado
    expected_time = datetime.now() - timedelta(days=1)
    diff = abs((contexto["data_hora_anterior"] - expected_time).total_seconds())
    assert diff < 10  # tolerância de 10 segundos para a execução do teste


# 3. Testes para ObterListaIDCanaisCorrente
def test_obter_lista_id_canais_corrente_success():
    """
    Testa se a obtenção de IDs de canais adiciona os resultados corretos ao contexto.
    """
    log_mock = MockLogger()
    youtube_mock = MagicMock(spec=IApiYoutube)
    
    # Mockando o método obter_id_canal para retornar uma tupla com (id, titulo)
    youtube_mock.obter_id_canal.side_effect = lambda canal: (f"{canal}_id", f"Titulo de {canal}")

    lista_canais = ["canalA", "canalB"]
    corrente = ObterListaIDCanaisCorrente(log_mock, lista_canais=lista_canais, servico_youtube=youtube_mock)

    contexto = Contexto(data_hora_anterior=None, lista_id_canais=[])
    result = corrente.executar_processo(contexto)

    assert result is True
    assert contexto["lista_id_canais"] == ["canalA_id", "canalB_id"]
    
    youtube_mock.obter_id_canal.assert_any_call("canalA")
    youtube_mock.obter_id_canal.assert_any_call("canalB")
    log_mock.info.assert_any_call("Obtenido canal canalA_id")
    log_mock.info.assert_any_call("Obtenido canal canalB_id")
    log_mock.info.assert_any_call("Sucesso ao obter os canais")


def test_obter_lista_id_canais_corrente_partial_success():
    """
    Testa o fluxo quando um dos canais não é encontrado (retorna None).
    """
    log_mock = MockLogger()
    youtube_mock = MagicMock(spec=IApiYoutube)
    
    # canalA é encontrado, canalB não (retorna None)
    youtube_mock.obter_id_canal.side_effect = lambda canal: (f"{canal}_id", "Titulo") if canal == "canalA" else None

    lista_canais = ["canalA", "canalB"]
    corrente = ObterListaIDCanaisCorrente(log_mock, lista_canais=lista_canais, servico_youtube=youtube_mock)

    contexto = Contexto(data_hora_anterior=None, lista_id_canais=[])
    result = corrente.executar_processo(contexto)

    assert result is True
    # Apenas o id de canalA deve estar presente
    assert contexto["lista_id_canais"] == ["canalA_id"]
    youtube_mock.obter_id_canal.assert_any_call("canalA")
    youtube_mock.obter_id_canal.assert_any_call("canalB")


def test_obter_lista_id_canais_corrente_exception_handling():
    """
    Testa se uma exceção disparada pelo serviço da API do YouTube é tratada corretamente,
    gerando log de erro e retornando False.
    """
    log_mock = MockLogger()
    youtube_mock = MagicMock(spec=IApiYoutube)
    youtube_mock.obter_id_canal.side_effect = Exception("Erro de Conexão na API")

    lista_canais = ["canalA"]
    corrente = ObterListaIDCanaisCorrente(log_mock, lista_canais=lista_canais, servico_youtube=youtube_mock)

    contexto = Contexto(data_hora_anterior=None, lista_id_canais=[])
    result = corrente.executar_processo(contexto)

    assert result is False
    assert contexto["lista_id_canais"] == []
    log_mock.error.assert_called_with("Falha ao obter os canais")
