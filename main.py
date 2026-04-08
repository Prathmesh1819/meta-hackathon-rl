from fastapi import FastAPI
from pydantic import BaseModel
import os

from my_env_v4 import MyEnvV4Env, MyEnvV4Action

app = FastAPI()

env = None
IMAGE_NAME = os.getenv("IMAGE_NAME")

class StepRequest(BaseModel):
    action: str

@app.post("/reset")
async def reset():
    global env
    env = await MyEnvV4Env.from_docker_image(IMAGE_NAME)
    result = await env.reset()
    return {"observation": result.observation.echoed_message}

@app.post("/step")
async def step(req: StepRequest):
    global env
    result = await env.step(MyEnvV4Action(message=req.action))
    return {
        "observation": result.observation.echoed_message,
        "reward": result.reward,
        "done": result.done
    }