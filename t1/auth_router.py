from fastapi import APIRouter, Depends, HTTPException
from models import Usuario, db
from sqlalchemy.orm import sessionmaker  
from dependencias import *
from crypt import brcrypt_context
from schemas import *
from sqlalchemy.orm import Session
from models import Usuario
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordRequestForm


auth_router = APIRouter(prefix="/auth", tags=["auth"])

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALFORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))



def criar_token(id_usuario: str, duracao_token=ACCESS_TOKEN_EXPIRE_MINUTES):
    """
    Docstring for criar_token
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=duracao_token)
    payload = {
        "sub": str(id_usuario),
        "exp": expire
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALFORITHM)
    return token


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


@auth_router.post("/login-form")
async def login_form(dados_form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_sessao)):
    """
    Docstring for login
    """
    usuario = autenticar_usuario(dados_form.username, dados_form.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Email ou senha incorretos ou credenciais inválidas")
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=60 * 24 * 7)  # 7 dias

        return {
                "access_token": access_token, 
                "token_type": "bearer"
            }
        


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
        refresh_token = criar_token(usuario.id, duracao_token=60 * 24 * 7)  # 7 dias

        return {
                "access_token": access_token, 
                "refresh_token": refresh_token,
                "token_type": "bearer"
            }
        


@auth_router.get("/refresh")
async def  refresh_token(usuario: Usuario = Depends(verificar_token)):
    """
    Docstring for refresh_token
    """
    access_token = criar_token(usuario.id)
    return {
            "access_token": access_token,
             "refresh_token": refresh_token,
             "token_type": "bearer"
            }