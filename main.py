import numpy as np
import random
import matplotlib.pyplot as plt

# Actions
STUDY = 0
SOCIAL = 1
SLEEP = 2
actions = [STUDY, SOCIAL, SLEEP]

# Q-table
Q = {}

def get_state(energy, focus, addiction, time):
    return (energy, focus, addiction, time)

def choose_action(state, epsilon=0.2):
    if random.uniform(0,1) < epsilon:
        return random.choice(actions)
    else:
        return np.argmax(Q.get(state, [0,0,0]))
def get_reward(state, action):
    energy, focus, addiction, time = state

    # Time effect
    if 6 <= time <= 12:   # Morning
        focus += 2
    elif time >= 22:      # Late night
        focus -= 2

    if action == STUDY:
        reward = 10 + focus - addiction

        # 🔥 Prevent over-studying (burnout)
        if energy == 0:
            reward -= 10

        return reward
    elif action == SOCIAL:
        if time >= 20:  # Night scrolling dangerous
            return 3 - addiction * 3
        return 2 - addiction * 2

    elif action == SLEEP:
        return 5 + (10 - energy)

def update_state(state, action):
    energy, focus, addiction, time = state

    if action == STUDY:
        energy -= 2
        focus += 2
        addiction -= 1

    elif action == SOCIAL:
        energy -= 1
        focus -= 2
        addiction += 2

    elif action == SLEEP:
        energy += 3
        focus += 1

    # Clamp values
    energy = max(0, min(10, energy))
    focus = max(0, min(10, focus))
    addiction = max(0, min(10, addiction))

    # Time moves forward
    time = (time + 1) % 24

    return (energy, focus, addiction, time)

# Training
episodes = 700

for _ in range(episodes):
    state = get_state(5,5,5,8)  # start at 8 AM

    for step in range(50):
        action = choose_action(state)

        reward = get_reward(state, action)
        next_state = update_state(state, action)

        if state not in Q:
            Q[state] = [0,0,0]

        if next_state not in Q:
            Q[next_state] = [0,0,0]

        lr = 0.1
        gamma = 0.9

        Q[state][action] += lr * (
            reward + gamma * max(Q[next_state]) - Q[state][action]
        )

        state = next_state

# TEST RUN + TRACKING
state = (5,5,5,8)

energy_list = []
focus_list = []
addiction_list = []
reward_list = []

print("\n--- AI DECISIONS ---\n")

for i in range(50):
    action = np.argmax(Q[state])

    reward = get_reward(state, action)

    energy, focus, addiction, time = state

    action_name = ["STUDY", "SOCIAL", "SLEEP"][action]

    print(f"[Hour {time}] → {action_name} | Energy:{energy} Focus:{focus} Addiction:{addiction} Reward:{reward}")

    energy_list.append(energy)
    focus_list.append(focus)
    addiction_list.append(addiction)
    reward_list.append(reward)

    state = update_state(state, action)

# 📊 GRAPH
plt.figure()

plt.plot(reward_list, label="Productivity (Reward)")
plt.plot(addiction_list, label="Addiction Level")
plt.plot(focus_list, label="Focus Level")

plt.title("AI Behavior Over Time")
plt.xlabel("Steps (Hours)")
plt.ylabel("Values")
plt.legend()

plt.show()