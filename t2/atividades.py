from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import sessionmaker  
from dependencias import get_sessao
from sqlalchemy.orm import Session
from schemas import AtividadesSchema
from model import Aticidades
import os
from uuid import uuid4
from fastapi.responses import Response


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

atividades_router = APIRouter(prefix="/atividades", tags=["atividades"])
@atividades_router.get("/")
async def atividades():
    """
    Docstring for atividades
    """
    return {"message": "Atividades endpoint funcionando"}

@atividades_router.post("/criar_atividade")
async def criar_atividade(atividade_schema: AtividadesSchema, session: Session = Depends(get_sessao)):
    """
    Docstring for criar_atividade
    """
    {"message": "Atividade criada com sucesso"}
    nova_atividade = Aticidades(titulo=atividade_schema.titulo, descricao=atividade_schema.descricao, status=atividade_schema.status, img_path=atividade_schema.img_path)
    session.add(nova_atividade)
    session.commit()
    return {"message": "Atividade criada com sucesso"}

@atividades_router.get("/listar")
async def listar_atividades(session: Session = Depends(get_sessao)):
    return session.query(Aticidades).all()


@atividades_router.get("/{id}")
async def obter_atividade(id: int, session: Session = Depends(get_sessao)):
    atividade = session.query(Aticidades).filter(Aticidades.id == id).first()
    if not atividade:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")
    return atividade

@atividades_router.delete("/{id}")
async def deletar_atividade(id: int, session: Session = Depends(get_sessao)):
    atividade = session.query(Aticidades).filter(Aticidades.id == id).first()
    if not atividade:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")
    session.delete(atividade)
    session.commit()
    return {"message": "Atividade deletada com sucesso"}


@atividades_router.put("/{id}")
async def atualizar_atividade(
    id: int,
    titulo: str = Form(...),
    descricao: str = Form(None),
    status: str = Form(...),
    imagem: UploadFile = File(None),
    imagem_url: str = Form(None),
    session: Session = Depends(get_sessao)
):
    atividade = session.query(Aticidades).filter(Aticidades.id == id).first()

    if not atividade:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")

    atividade.titulo = titulo
    atividade.descricao = descricao
    atividade.status = status

    if imagem:
        ext = imagem.filename.split(".")[-1]
        nome = f"{uuid4()}.{ext}"
        path = f"uploads/{nome}"

        with open(path, "wb") as f:
            f.write(await imagem.read())

        atividade.img_path = path

    elif imagem_url:
        atividade.img_path = imagem_url  # salva URL direto

    session.commit()
    return {"message": "Atividade atualizada"}

# @atividades_router.put("/{id}")
# async def atualizar_atividade(id: int, atividade_schema: AtividadesSchema, session: Session = Depends(get_sessao)):
#     atividade = session.query(Aticidades).filter(Aticidades.id == id).first()
#     if not atividade:
#         raise HTTPException(status_code=404, detail="Atividade não encontrada")
    
#     atividade.titulo = atividade_schema.titulo
#     atividade.descricao = atividade_schema.descricao
#     atividade.status = atividade_schema.status
#     atividade.img_path = atividade_schema.img_path
    
#     session.commit()
#     return {"message": "Atividade atualizada com sucesso"}


@atividades_router.get("/{id}/imagem")
def obter_imagem(id: int, session: Session = Depends(get_sessao)):
    atividade = session.query(Aticidades).filter(Aticidades.id == id).first()

    if not atividade or not atividade.imagem:
        raise HTTPException(status_code=404, detail="Imagem não encontrada")

    return Response(content=atividade.imagem, media_type="image/jpeg")
