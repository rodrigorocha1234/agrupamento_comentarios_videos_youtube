from typing import Any, Dict, Tuple, Type, Callable

from minio import Minio

from src.config.config import Config
from src.operacao.idb_config import IDbConfig


class ConfigS3Minio(IDbConfig):

    def obter_driver(self) -> Minio:
        return Minio(
            self.obter_parametros_conexao()[0][0],
            **self.obter_parametros_conexao()[1],

        )
    def obter_parametros_conexao(self) -> Tuple[Tuple[Any, ...], Dict[str, Any]]:
        endpoint = f"{Config.HOST_S3}:{Config.PORT_S3}"

        return (
            (endpoint,),  # args
            {
                "access_key": Config.USER_S3,
                "secret_key": Config.PASSWORD_S3,
                "secure": False
            }
        )

if __name__ == "__main__":
    config = ConfigS3Minio()
    driver = config.obter_driver()
    a = driver.bucket_exists('youtube')
    print(a)