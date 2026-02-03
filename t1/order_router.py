from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencias import get_sessao, verificar_token
from schemas import PedidoSchema
from models import Pedido, Usuario, db


order_router = APIRouter(prefix="/pedidos", tags=["orders"], dependencies=[Depends(verificar_token)])


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


@order_router.get("/pedido/cancelar/{pedido_id}")
async def cancelar_pedido(pedido_id: int, session: Session = Depends(get_sessao), usuario: Usuario = Depends(verificar_token)):
    """
    Docstring for cancelar_pedido
    """
    pedido = session.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=403, detail="Você não tem permissão para cancelar este pedido")
    if pedido_id is None:
        raise HTTPException(status_code=400, detail="ID do pedido é obrigatório")

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    pedido.status = "CANCELADO"
    session.commit()
    return {
            "message": f"Pedido {pedido_id} cancelado com sucesso.",
            "pedido": {
                "id": pedido.id,
                "status": pedido.status,
                "usuario": pedido.usuario,
                "preco": pedido.preco
            }
        }


@order_router.get("/listar")
async def listar_pedidos(session: Session = Depends(get_sessao), usuario: Usuario = Depends(verificar_token)):
    """
    Docstring for listar_pedidos
    """
    if not usuario.admin and usuario.ativo == False:
        raise HTTPException(status_code=403, detail="Usuário inativo não pode listar pedidos")
    else:
        pedidos = session.query(Pedido).all()
        user_pedidos = session.query(Pedido).filter(Pedido.usuario == usuario.id).all()
     
    return {"pedidos": pedidos}



@order_router.get("/listar_user")
async def listar_pedidos(session: Session = Depends(get_sessao), usuario: Usuario = Depends(verificar_token)):
    """
    Docstring for listar_pedidos
    """
    if not usuario.admin and usuario.ativo == False:
        raise HTTPException(status_code=403, detail="Usuário inativo não pode listar pedidos")
    else:
        user_pedidos = session.query(Pedido).filter(Pedido.usuario == usuario.id).all()
     
    return {"pedidos": user_pedidos}

