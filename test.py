import numpy as np

def calculate_trajectory(bot_pos: tuple, base_pos: tuple):
    bot = np.array(bot_pos)
    base = np.array(base_pos)
    dist = base - bot
    dist = dist / np.linalg.norm(dist)
    dist = -dist * 0.2
    dist += bot_pos

    return tuple(dist)

print(calculate_trajectory((1,1), (0,0)))