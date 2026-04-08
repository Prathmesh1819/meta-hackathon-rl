from fastapi import FastAPI

app = FastAPI()

@app.post("/reset")
async def reset():
    return {
        "observation": "start",
        "reward": 0.0,
        "done": False
    }

@app.post("/step")
async def step(action: dict):
    return {
        "observation": action.get("action", ""),
        "reward": 1.0,
        "done": True
    }