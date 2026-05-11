from fastapi import FastAPI
from src import base


app = FastAPI()
app.include_router(base.base_router)