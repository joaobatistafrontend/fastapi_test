from pydantic import BaseModel
from typing import Optional


class UsuarioSchemas(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    #serve para converter os modelos do sqlalchemy em schemas do pydantic
    class Config:
        from_attributes = True


class PedidoSchema(BaseModel):
    id_usuario : int

    class Config:
        from_attributes = True