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


@order_router.get("/pedido/finalizar/{pedido_id}")
async def finalizar_pedido(pedido_id: int, session: Session = Depends(get_sessao), usuario: Usuario = Depends(verificar_token)):
    """
    Docstring for finalizar_pedido
    """
    pedido = session.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=403, detail="Você não tem permissão para cancelar este pedido")
    if pedido_id is None:
        raise HTTPException(status_code=400, detail="ID do pedido é obrigatório")

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    pedido.status = "FINALIZADO"
    session.commit()
    return {
            "message": f"Pedido {pedido_id} finalizado com sucesso.",
            "pedido": {
                "id": pedido.id,
                "status": pedido.status,
                "usuario": pedido.usuario,
                "preco": pedido.preco
            }
        }


@order_router.get("/pedido/{pedido_id}")
async def obter_pedido(pedido_id: int, session: Session = Depends(get_sessao), usuario: Usuario = Depends(verificar_token)):
    """
    Docstring for obter_pedido
    """
    pedido = session.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=403, detail="Você não tem permissão para visualizar este pedido")

    return {
            "quantidade_itens": len(pedido.itens),
            "pedido": {
                "id": pedido.id,
                "status": pedido.status,
                "usuario": pedido.usuario,
                "preco": pedido.preco,
                "itens": [
                    {
                        "id": item.id,
                        "quantidade": item.quantidade,
                        "sabor": item.sabor,
                        "tamanho": item.tamanho,
                        "preco_unitario": item.preco_unitario
                    } for item in pedido.itens
                ]
            }
        }


@order_router.get("/pedido/finalizados/listar")
async def listar_pedidos_finalizados(session: Session = Depends(get_sessao), usuario: Usuario = Depends(verificar_token)):
    """
    Docstring for listar_pedidos_finalizados
    """
    if not usuario.admin and usuario.ativo == False:
        raise HTTPException(status_code=403, detail="Usuário inativo não pode listar pedidos")
    else:
        pedidos_finalizados = session.query(Pedido).filter(Pedido.status == "FINALIZADO").all()
     
    return {"pedidos_finalizados": pedidos_finalizados}

@order_router.get("/pedido/cancelados/listar")
async def listar_pedidos_cancelados(session: Session = Depends(get_sessao), usuario: Usuario = Depends(verificar_token)):
    """
    Docstring for listar_pedidos_cancelados
    """
    if not usuario.admin and usuario.ativo == False:
        raise HTTPException(status_code=403, detail="Usuário inativo não pode listar pedidos")
    else:
        pedidos_cancelados = session.query(Pedido).filter(Pedido.status == "CANCELADO").all()
     
    return {"pedidos_cancelados": pedidos_cancelados}

@order_router.get("/pedido/pedentes/listar")
async def listar_pedidos_pendentes(session: Session = Depends(get_sessao), usuario: Usuario = Depends(verificar_token)):
    """
    Docstring for listar_pedidos_pendentes
    """
    if not usuario.admin and usuario.ativo == False:
        raise HTTPException(status_code=403, detail="Usuário inativo não pode listar pedidos")
    else:
        pedidos_pendentes = session.query(Pedido).filter(Pedido.status == "PENDENTE").all()
     
    return {"pedidos_pendentes": pedidos_pendentes}

@order_router.post("/pedido/resumo/finalizados")
async def resumo_pedidos_finalizados(session: Session = Depends(get_sessao), usuario: Usuario = Depends(verificar_token)):
    """
    Docstring for resumo_pedidos_finalizados
    """
    if not usuario.admin:
        raise HTTPException(status_code=403, detail="Apenas administradores podem acessar o resumo de pedidos finalizados")
    
    pedidos_finalizados = session.query(Pedido).filter(Pedido.status == "FINALIZADO").all()
    total_finalizados = len(pedidos_finalizados)
    receita_total = sum(pedido.preco for pedido in pedidos_finalizados)

    return {
        "total_pedidos_finalizados": total_finalizados,
        "receita_total": receita_total
    }