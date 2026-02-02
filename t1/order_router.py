from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencias import get_sessao
from schemas import PedidoSchema
from models import Pedido, db
order_router = APIRouter(prefix="/pedidos", tags=["orders"])
@order_router.get("/")
async def pedidosGet():
    """
    Docstring for pedidosGet
    """
    return {"message": "Lista de pedidos"}

@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(get_sessao)):
    """
    Docstring for criar_pedido
    """
    novo_pedido = Pedido(usuario=pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    return {"message": f"Pedido criado com sucesso. ID do pedido: {novo_pedido.id}"}


