from fastapi import FastAPI
from dotenv import load_dotenv
import os


app = FastAPI()

from auth_router import  auth_router
from order_router import order_router

app.include_router(auth_router)
app.include_router(order_router)


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")



# uvicorn main:app --reload