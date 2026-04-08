from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class StepRequest(BaseModel):
    action: str

@app.post("/reset")
async def reset():
    return {"status": "ok"}

@app.post("/step")
async def step(req: StepRequest):
    return {
        "observation": req.action,
        "reward": 1.0,
        "done": True
    }