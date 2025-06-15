from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Stock Market application backend is running!"}