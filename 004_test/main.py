from fastapi import FastAPI

app = FastAPI(title='testing')


@app.get("/")
async def read_main():
    return {"msg": "hello world"}
