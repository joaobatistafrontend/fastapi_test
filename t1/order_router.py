from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencias import get_sessao, verificar_token
from schemas import PedidoSchema, ItemPedidoSchema
from models import Pedido, Usuario, db, ItemPedido


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


@order_router.post("/pedido/add/{id_pedido}")
async def adicionar_item_pedido(
            id_pedido: int,
            item_pedido_schema: ItemPedidoSchema,
            session: Session = Depends(get_sessao),
            usuario: Usuario = Depends(verificar_token)
        ):
    
    """
    Docstring for adicionar_item_pedido
    """
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()

    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=403, detail="Você não tem permissão para adicionar itens a este pedido")
    if id_pedido is None:
        raise HTTPException(status_code=400, detail="ID do pedido é obrigatório")
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    item_pedido = ItemPedido(
        pedido_id = id_pedido,
        quantidade=item_pedido_schema.quantidade,
        sabor=item_pedido_schema.sabor,
        tamanho=item_pedido_schema.tamanho,
        preco_unitario=item_pedido_schema.preco_unitario,
    )
    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        "message": f"Item adicionado ao pedido {id_pedido} com sucesso.",
        "item_pedido": item_pedido.id,
        "preco_pedido": pedido.preco,
        "id_pedido": id_pedido    
    }
    


@order_router.post("/pedido/remove/{id_item_pedido}")
async def remover_item_pedido(
            id_item_pedido: int,
            session: Session = Depends(get_sessao),
            usuario: Usuario = Depends(verificar_token)
        ):
    
    """
    Docstring for remover_item_pedido
    """

    item_pedido = session.query(ItemPedido).filter(ItemPedido.id == id_item_pedido).first()
    if not item_pedido:
        raise HTTPException(status_code=404, detail="Item do pedido não encontrado")

    item_pedido = session.query(ItemPedido).filter(ItemPedido.id == id_item_pedido).first()
    pedido = session.query(Pedido).filter(Pedido.id == item_pedido.pedido_id).first()

    if not item_pedido:
        raise HTTPException(status_code=404, detail="Item do pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=403, detail="Você não tem permissão para remover itens deste pedido")
   
    session.delete(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        "message": f"Item {id_item_pedido} removido do pedido com sucesso.",
        "preco_pedido": pedido.preco,
        "id_pedido": pedido.id,
        "item_removido": {"id": id_item_pedido, "status": "removido"},
        "item_removido_details": {
                "id": id_item_pedido,
                "quantidade": item_pedido.quantidade,
                "sabor": item_pedido.sabor,
                "tamanho": item_pedido.tamanho,
                "preco_unitario": item_pedido.preco_unitario
            },
        }
    