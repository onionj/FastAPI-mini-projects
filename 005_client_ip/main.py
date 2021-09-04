from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
app = FastAPI(title="Get ip API", version="0.0.1",
              description="this app have one endpoint and just return your IP")


class Data(BaseModel):
    client_host: str = Field(..., example="127.0.0.1")
    client_port: int = Field(..., example=80)


@app.get("/", response_model=Data)
def get_ip(request: Request):
    return {
        "client_host": request.client.host,
        "client_port": request.client.port
    }
