from fastapi import FastAPI
from routes.contato_routes import router as contato_router

app = FastAPI()

app.include_router(contato_router, prefix="/contatos", tags=["Contatos"])
