class MyEnvV4Action:
    def __init__(self, message):
        self.message = message


class Observation:
    def __init__(self, echoed_message):
        self.echoed_message = echoed_message


class Result:
    def __init__(self, message, step):
        self.observation = Observation(message)
        self.reward = len(message) * 0.1
        self.done = step >= 5


class MyEnvV4Env:
    def __init__(self):
        self.step_count = 0

    async def reset(self):
        self.step_count = 0
        return Result("start", 0)

    async def step(self, action):
        self.step_count += 1
        return Result(action.message, self.step_count)

    async def close(self):
        pass