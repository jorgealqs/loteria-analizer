from fastapi import FastAPI, Response
from app.routes.endpoints import router
from app.routes.password_key import router_password_key

app = FastAPI(
    title="Analizador de Lotería",
    description="API para analizar sorteos de lotería",
    version="1.0"
)

app.include_router(router)
app.include_router(router_password_key)


@app.get("/")
def home():
    return Response("<h1>Bienvenido al Analizador de Lotería</h1>")
