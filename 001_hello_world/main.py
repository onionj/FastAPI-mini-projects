from typing import Optional

from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def read_root(name: Optional[str] = None):
    if name:
        # http://127.0.0.1:8000/?name=onionj
        return {"message": f"Hello {name}"}

    # http://127.0.0.1:8000
    return {"message": "Hello World"}
