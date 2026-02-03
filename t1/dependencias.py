from sqlalchemy.orm import sessionmaker
from models import db
from sqlalchemy.orm import Session
from models import Usuario
from fastapi import Depends
from jose import jwt, JWTError
from dotenv import load_dotenv
import os
from fastapi import APIRouter, Depends, HTTPException
from dependencias import *
from crypt import oauth2_scheme   
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALFORITHM = os.getenv("ALGORITHM")



def get_sessao():
    try:
        Session = sessionmaker(bind=db) 
        session = Session()
        yield Session()
    finally:
        session.close()


def verificar_token(token: str = Depends(oauth2_scheme), session: Session = Depends(get_sessao)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALFORITHM])
        id_usuario: str = payload.get("sub")
    except JWTError:
            raise HTTPException(status_code=401, detail="Token inválido, verifique a validade do token")
    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso inválido")
    return usuario
