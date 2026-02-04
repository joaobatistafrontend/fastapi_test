from pydantic import BaseModel
from typing import Optional, List


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


class ItemPedidoSchema(BaseModel):
    quantidade: int
    sabor: str
    tamanho: str
    preco_unitario: float

    class Config:
        from_attributes = True

class PedidoResponseSchema(BaseModel):
    id: int
    status: str
    preco: float
    itens: List[ItemPedidoSchema]

    class Config:
        from_attributes = True