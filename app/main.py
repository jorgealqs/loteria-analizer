from fastapi import FastAPI, Response
from app.routes.endpoints import router

app = FastAPI(
    title="Analizador de Lotería",
    description="API para analizar sorteos de lotería",
    version="1.0"
)

app.include_router(router)


@app.get("/")
def home():
    return Response("<h1>Bienvenido al Analizador de Lotería</h1>")
