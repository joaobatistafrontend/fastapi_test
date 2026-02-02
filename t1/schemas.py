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
    usuario : int

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes = True