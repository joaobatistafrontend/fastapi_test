from sqlalchemy.orm import sessionmaker
from models import db
def get_sessao():
    try:
        Session = sessionmaker(bind=db) 
        session = Session()
        yield Session()
    finally:
        session.close()