from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"msg": "ok"}

@app.post("/reset")
def reset():
    return {"observation": "start", "reward": 0.0, "done": False}

@app.post("/step")
def step(data: dict):
    return {"observation": "ok", "reward": 1.0, "done": True}