from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_utils.types import ChoiceType

#criar a conexão com o banco de dados
db = create_engine("sqlite:///banco.db")
#criar a base de modelos
Base = declarative_base()


class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String,)
    email = Column("email", String(100), nullable=False, unique=True)
    senha = Column("senha", String(100), nullable=False)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

class Pedido(Base):
    __tablename__ = "pedidos"
    
    # STATUS_PEDIDOS = [
    #     ("PENDENTE", "Pendente"),
    #     ("CANCELADO", "Cancelado"),
    #     ("FINALIZADO", "Finalizado"),
    # ]

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String)  #ChoiceType(STATUS_PEDIDOS)
    usuario = Column("usuario_id", ForeignKey("usuarios.id"))
    preco = Column("preco", Float)
    itens = relationship("ItemPedido", cascade="all, delete-orphan")

    def __init__(self, usuario, status="PENDENTE", preco=0):
        self.status = status
        self.usuario = usuario
        self.preco = preco

    def calcular_preco(self):
        for item in self.itens:
            self.preco += item.preco_unitario * item.quantidade
        return self.preco
        

class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade = Column("quantidade", Integer)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float, nullable=False)
    pedido_id = Column("pedido_id", ForeignKey("pedidos.id"))

    def __init__(self, pedido_id, quantidade, sabor, tamanho, preco_unitario):
        self.pedido_id = pedido_id
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario


#criar as tabelas no db
#alembic init alembic    para inicializar o alembic
#alembic revision --autogenerate -m "initial migrate"  para criar a migration inicial
#alembic upgrade head para aplicar as migrations
# executar a criacao dos metadados do seu db(criar efetvamente o db)

#criar porta
#uvicorn main:app --reload --port 8001
