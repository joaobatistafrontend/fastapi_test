from fastapi import APIRouter, Depends, HTTPException
from models import Usuario, db
from sqlalchemy.orm import sessionmaker  
from dependencias import get_sessao
from crypt import brcrypt_context
from schemas import *
from sqlalchemy.orm import Session
from models import Usuario
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os



auth_router = APIRouter(prefix="/auth", tags=["auth"])

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALFORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


#jwt simples
# def criar_token(id_usuario: str):
#     """
#     Docstring for criar_token
#     """
#     token = f"vdsdvvsdvds{id_usuario}"
#     return token

def criar_token(id_usuario: str):
    """
    Docstring for criar_token
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(id_usuario),
        "exp": expire
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALFORITHM)
    return token


#jwt avançado
# def criar_token(id_usuario: str):
#     """
#     Docstring for criar_token
#     """
#     payload = {
#         "sub": id_usuario
#     }
#     token = jwt.encode(payload, "segredo_super_secreto", algorithm="HS256")
#     return token


def autenticar_usuario(email: str, senha: str, session: Session):
    """
    Docstring for autenticar_usuario
    """
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    #verify ela recebe a senha e o hash da senha verifica se é a msm coisa
    if not brcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario


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
async def login(login_schema: LoginSchema, session: Session = Depends(get_sessao)):
    """
    Docstring for login
    """
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Email ou senha incorretos ou credenciais inválidas")
    else:
        access_token = criar_token(usuario.id)
        return {"access_token": access_token, "token_type": "bearer"}
        
    # if not brcrypt_context.verify(login_schema.senha, Usuario.senha):
    #     raise HTTPException(status_code=400, detail="Email ou senha incorretos")
    