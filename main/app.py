from fastapi import FastAPI
from main.services.initial_data import InitialData
from fastapi.middleware.cors import CORSMiddleware

InitialData().execute()

app = FastAPI(
    title="Prize Wheel",
    version="1.0.0",
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from main.routes import router

app.include_router(router, prefix="/v1")
