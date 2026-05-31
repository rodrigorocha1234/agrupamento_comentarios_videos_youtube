from datetime import datetime
from typing import TypedDict, List, Optional


class Contexto(TypedDict):
    data_hora_anterior: Optional[datetime]
    lista_id_canais: List[str]
