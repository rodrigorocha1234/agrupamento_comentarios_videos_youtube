from datetime import datetime
from typing import TypedDict, List, Optional, Generator, Dict


class Contexto(TypedDict):
    data_hora_anterior: Optional[datetime]
    lista_id_canais: List[str]
    lista_videos: List[Generator[Dict, None, None]]
    lista_id_comentarios: List[tuple[str,str, str]]
