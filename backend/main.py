from fastapi import FastAPI

app = FastAPI()

@app.get("/merge")
def merge_files():
    return {"Hello": "World"}