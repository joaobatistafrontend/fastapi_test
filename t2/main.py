from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite
    # allow_origins=["*"],  # se quiser liberar tudo (dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
from atividades import atividades_router
app.include_router(atividades_router)


# from fastapi import FastAPI
# from dotenv import load_dotenv
# import os

# app = FastAPI()

# from atividades import atividades_router
# app.include_router(atividades_router)