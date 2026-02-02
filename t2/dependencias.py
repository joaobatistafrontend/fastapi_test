from sqlalchemy.orm import sessionmaker
from model import db

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=db
)

def get_sessao():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


# from sqlalchemy.orm import sessionmaker
# from model import db
# def get_sessao():
#     try:
#         Session = sessionmaker(bind=db) 
#         session = Session()
#         yield Session()
#     finally:
#         session.close()