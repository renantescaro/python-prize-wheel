from fastapi import FastAPI
from main.services.initial_data import InitialData

InitialData().execute()

app = FastAPI(
    title="Prize Wheel",
    version="1.0.0",
)

from main.routes import router

app.include_router(router, prefix="/v1")
