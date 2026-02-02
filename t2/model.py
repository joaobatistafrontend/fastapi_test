from sqlalchemy.orm import declarative_base
import os
from sqlalchemy import Column, Integer, String, create_engine, LargeBinary
from sqlalchemy_utils.types import ChoiceType

db = create_engine("sqlite:///banco.db")
Base = declarative_base()

class Aticidades(Base):
    STATUS_ATIVIDADES = [
        ("PENDENTE", "Pendente"),
        ("EM_ANDAMENTO", "Em Andamento"),
        ("CONCLUIDA", "Concluída"),
    ]
    
    __tablename__ = "atividades"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    titulo = Column("titulo", String, nullable=False)
    descricao = Column("descricao", String, nullable=True)
    status = Column(String, nullable=False, default="PENDENTE")
    imagem = Column(LargeBinary, nullable=True) 

    def __init__(self, titulo, descricao=None, status="PENDENTE", img_path=None):
        self.titulo = titulo
        self.descricao = descricao
        self.status = status
        self.img_path = img_path