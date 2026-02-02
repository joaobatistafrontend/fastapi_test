from fastapi import APIRouter, Depends, HTTPException
from models import Usuario, db
from sqlalchemy.orm import sessionmaker  
from dependencias import get_sessao
from crypt import brcrypt_context
from schemas import UsuarioSchemas
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def autenticar():
    """
    Docstring for autenticar
    """
    return {"message": "Autenticación exitosa", "autenticado": False}

@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchemas, session: Session = Depends(get_sessao)):
    """
    Docstring for criar_conta
    """
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
    if usuario:
        raise HTTPException(status_code=400, detail=f"message: Já existe um usuario com esse email: {usuario_schema.email}",)
    else:
        senha_criptografada = brcrypt_context.hash(usuario_schema.senha)
        noovo_usuario = Usuario(nome=usuario_schema.nome, email=usuario_schema.email, senha=senha_criptografada, ativo=usuario_schema.ativo, admin=usuario_schema.admin)
        session.add(noovo_usuario)
        session.commit()
        return {"message": "Usuario criado com sucesso", "cuenta_creada": True}

@auth_router.post("/login")
async def login(pedido_schema: PerdidoSchema, session: Session = Depends(get_sessao)):
    """
    Docstring for login
    """
    return {"message": "Login realizado com sucesso", "logado": True}

    