from pydantic import BaseModel
from enum import Enum
from typing import Optional

class StatusAtividade(str, Enum):
    PENDENTE = "PENDENTE"
    EM_ANDAMENTO = "EM_ANDAMENTO"
    CONCLUIDA = "CONCLUIDA"

class AtividadesSchema(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    status: StatusAtividade
    img_path: Optional[str] = None

    class Config:
        from_attributes = True
