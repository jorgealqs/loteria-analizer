from fastapi import FastAPI
from os import environ as env

app = FastAPI()


@app.get("/")
def root():
    return {"message": f"Hello {env['PORT']}"}
