from datetime import datetime
from unittest.mock import patch, MagicMock
import pytest
from src.servico.servico_api_youtube.api_youtube import YoutubeAPI
from src.utils.servico_log.log_protocol import LogProtocol


class MockLogger(LogProtocol):
    def __init__(self):
        self.info = MagicMock()
        self.error = MagicMock()
        self.warning = MagicMock()
        self.debug = MagicMock()
        self.critical = MagicMock()



# 1. Testes para obter_id_canal
@patch("src.servico.servico_api_youtube.api_youtube.build")
def test_youtube_api_obter_id_canal_success(mock_build):
    """
    Testa se obter_id_canal retorna o ID e Título corretos do canal
    quando a resposta da API do YouTube é bem-sucedida.
    """
    mock_youtube = MagicMock()
    mock_build.return_value = mock_youtube

    # Configura a resposta mockada da API
    mock_response = {
        "items": [
            {
                "id": {"channelId": "UC_CANAL_ID_123"},
                "snippet": {"title": "Canal de Teste"}
            }
        ]
    }
    mock_youtube.search().list().execute.return_value = mock_response

    log_mock = MockLogger()
    api = YoutubeAPI(servico_log=log_mock)

    result = api.obter_id_canal("canal_busca")
    
    assert result == ("UC_CANAL_ID_123", "Canal de Teste")
    
    # Garante que os parâmetros de consulta corretos foram passados à API do YouTube
    mock_youtube.search().list.assert_called_with(
        part="snippet",
        q="canal_busca",
        type="channel",
        maxResults=1
    )
    log_mock.info.assert_called()


@patch("src.servico.servico_api_youtube.api_youtube.build")
def test_youtube_api_obter_id_canal_not_found(mock_build):
    """
    Testa se obter_id_canal retorna None se nenhum canal for encontrado.
    """
    mock_youtube = MagicMock()
    mock_build.return_value = mock_youtube

    mock_response = {"items": []}
    mock_youtube.search().list().execute.return_value = mock_response

    log_mock = MockLogger()
    api = YoutubeAPI(servico_log=log_mock)

    result = api.obter_id_canal("canal_invisivel")
    
    assert result is None


@patch("src.servico.servico_api_youtube.api_youtube.build")
def test_youtube_api_obter_id_canal_exception(mock_build):
    """
    Testa se obter_id_canal trata exceções retornando None e registrando no log de erros.
    """
    mock_youtube = MagicMock()
    mock_build.return_value = mock_youtube

    # Configura para lançar uma exceção genérica de API
    mock_youtube.search().list().execute.side_effect = Exception("Erro interno de rede")

    log_mock = MockLogger()
    api = YoutubeAPI(servico_log=log_mock)

    result = api.obter_id_canal("canal_excecao")
    
    assert result is None
    log_mock.error.assert_called()


# 2. Testes para obter_video_por_data (Gerador)
@patch("src.servico.servico_api_youtube.api_youtube.build")
def test_youtube_api_obter_video_por_data_pagination(mock_build):
    """
    Testa se obter_video_por_data gera corretamente a lista de vídeos
    percorrendo a paginação através do nextPageToken.
    """
    mock_youtube = MagicMock()
    mock_build.return_value = mock_youtube

    # Simula duas páginas: a primeira tem nextPageToken, a segunda não tem
    page1 = {
        "items": [{"id": {"videoId": "vid1"}, "snippet": {"title": "Vídeo 1"}}],
        "nextPageToken": "token_proxima_pagina"
    }
    page2 = {
        "items": [{"id": {"videoId": "vid2"}, "snippet": {"title": "Vídeo 2"}}]
    }

    mock_youtube.search().list().execute.side_effect = [page1, page2]

    log_mock = MockLogger()
    api = YoutubeAPI(servico_log=log_mock)

    # Coleta todos os itens do gerador
    videos = list(api.obter_video_por_data("UC_CANAL_ID", datetime(2026, 5, 30)))

    assert len(videos) == 2
    assert videos[0]["id"]["videoId"] == "vid1"
    assert videos[1]["id"]["videoId"] == "vid2"

    # Verifica se os requests foram chamados com o formato de data correto
    mock_youtube.search().list.assert_any_call(
        part="snippet",
        channelId="UC_CANAL_ID",
        order="date",
        publishedAfter="2026-05-30T00:00:00Z",
        pageToken=""
    )
    mock_youtube.search().list.assert_any_call(
        part="snippet",
        channelId="UC_CANAL_ID",
        order="date",
        publishedAfter="2026-05-30T00:00:00Z",
        pageToken="token_proxima_pagina"
    )


# 3. Testes para obter_comentarios_youtube (Gerador)
@patch("src.servico.servico_api_youtube.api_youtube.build")
def test_youtube_api_obter_comentarios_youtube(mock_build):
    """
    Testa se obter_comentarios_youtube gera os comentários corretamente
    gerenciando a paginação e finalizando ao não receber mais nextPageToken ou se a lista for vazia.
    """
    mock_youtube = MagicMock()
    mock_build.return_value = mock_youtube

    page1 = {
        "items": [{"id": "c1", "snippet": {"textDisplay": "Ótimo conteúdo"}}],
        "nextPageToken": "token_comment_2"
    }
    page2 = {
        "items": [{"id": "c2", "snippet": {"textDisplay": "Gostei muito"}}],
        # sem token de próxima página
    }

    mock_youtube.commentThreads().list().execute.side_effect = [page1, page2]

    log_mock = MockLogger()
    api = YoutubeAPI(servico_log=log_mock)

    comments = list(api.obter_comentarios_youtube("vid_id_123"))

    assert len(comments) == 2
    assert comments[0]["id"] == "c1"
    assert comments[1]["id"] == "c2"

    # Verifica se a chamada foi parametrizada corretamente
    mock_youtube.commentThreads().list.assert_any_call(
        part="snippet",
        videoId="vid_id_123",
        pageToken=None,
        textFormat="plainText"
    )
    mock_youtube.commentThreads().list.assert_any_call(
        part="snippet",
        videoId="vid_id_123",
        pageToken="token_comment_2",
        textFormat="plainText"
    )


@patch("src.servico.servico_api_youtube.api_youtube.build")
def test_youtube_api_obter_comentarios_youtube_exception(mock_build):
    """
    Testa se obter_comentarios_youtube lida corretamente com exceções
    da API interrompendo o gerador e gerando log de erro.
    """
    mock_youtube = MagicMock()
    mock_build.return_value = mock_youtube
    mock_youtube.commentThreads().list().execute.side_effect = Exception("Erro de Quota Excedida")

    log_mock = MockLogger()
    api = YoutubeAPI(servico_log=log_mock)

    comments = list(api.obter_comentarios_youtube("vid_id_error"))

    assert len(comments) == 0
    log_mock.error.assert_called()


# 4. Testes para obter_resposta_comentarios (Gerador)
@patch("src.servico.servico_api_youtube.api_youtube.build")
def test_youtube_api_obter_resposta_comentarios(mock_build):
    """
    Testa se obter_resposta_comentarios gera as respostas aos comentários
    percorrendo páginas de forma iterativa via nextPageToken.
    """
    mock_youtube = MagicMock()
    mock_build.return_value = mock_youtube

    page1 = {
        "items": [{"id": "reply_1", "snippet": {"textDisplay": "Obrigado"}}],
        "nextPageToken": "token_reply_2"
    }
    page2 = {
        "items": [{"id": "reply_2", "snippet": {"textDisplay": "Sim, concordo"}}],
    }

    mock_youtube.comments().list().execute.side_effect = [page1, page2]

    log_mock = MockLogger()
    api = YoutubeAPI(servico_log=log_mock)

    replies = list(api.obter_resposta_comentarios("comentario_principal_id"))

    assert len(replies) == 2
    assert replies[0]["id"] == "reply_1"
    assert replies[1]["id"] == "reply_2"

    mock_youtube.comments().list.assert_any_call(
        part="snippet",
        parentId="comentario_principal_id",
        maxResults=100,
        textFormat="plainText",
        pageToken=None
    )
    mock_youtube.comments().list.assert_any_call(
        part="snippet",
        parentId="comentario_principal_id",
        maxResults=100,
        textFormat="plainText",
        pageToken="token_reply_2"
    )


@patch("src.servico.servico_api_youtube.api_youtube.build")
def test_youtube_api_obter_resposta_comentarios_exception(mock_build):
    """
    Testa se obter_resposta_comentarios trata exceções na API,
    interrompendo a geração e gerando log de erro.
    """
    mock_youtube = MagicMock()
    mock_build.return_value = mock_youtube
    mock_youtube.comments().list().execute.side_effect = Exception("Erro desconhecido")

    log_mock = MockLogger()
    api = YoutubeAPI(servico_log=log_mock)

    replies = list(api.obter_resposta_comentarios("comentario_error_id"))

    assert len(replies) == 0
    log_mock.error.assert_called()
