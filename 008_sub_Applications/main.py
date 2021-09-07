from fastapi import FastAPI


app = FastAPI(title="main api")
#  http://127.0.0.1:8000/docs


@app.get("/main")
def read_main():
    return {"message": "Hello World from main app"}


subapi = FastAPI(title="sub api")
#  http://127.0.0.1:8000/subapi/docs


@subapi.get("/sub")
def read_sub():
    return {"message": "Hello World from sub API"}


app.mount("/subapi", subapi)
