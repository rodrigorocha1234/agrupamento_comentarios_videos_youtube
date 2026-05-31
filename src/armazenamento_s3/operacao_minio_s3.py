import io
import json
import socket
from datetime import datetime, timezone
from typing import Any

from minio import Minio

from src.config.config import Config
from src.operacao.idb_config import IDbConfig


class OperacaoMInioS3:
    def __init__(self, conexao_s3: IDbConfig[Minio]):
        self.__conexao_s3 = conexao_s3
        self.__host = Config.HOST_S3
        self.__port = Config.PORT_S3
        self.__BUCKET = 'youtube'
        self.__DATA_ATUAL = datetime.now()

    def checar_conexao(self) -> bool:
        try:
            with socket.create_connection((self.__host, self.__port), timeout=10):
                return True
        except OSError:
            return False



    def salvar_dados(self, **kwargs: Any) -> None:
        json_youtube = kwargs['json_youtube']
        caminho = kwargs['caminho']

        driver = self.__conexao_s3.obter_driver()
        json_data = json.dumps(json_youtube, ensure_ascii=False)
        json_bytes = json_data.encode('utf-8')
        data_stream = io.BytesIO(json_bytes)
        driver.put_object(bucket_name=self.__BUCKET, object_name=caminho, data=io.BytesIO(json_bytes),
            length=len(json_bytes), content_type='application/json', )
