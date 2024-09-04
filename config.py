# backend/config.py
import numpy as np

class Config:
    SECRET_KEY = 'your_secret_key'
    SIMULATION_PARAMS = {
        'neighbor_distance': 10.0,
        'alignment_weight': 0.05,
        'cohesion_weight': 0.01,
        'separation_weight': 0.1,
        'max_speed': 2.0,
        'task_speed': 3.0,
        'task_threshold': 1.0,
        'reproduction_probability': 0.001,
        'max_age': 2000,
        'colors': [
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
            (255, 255, 0),
            (0, 255, 255),
            (255, 0, 255),
        ],
        'num_agents': 25,
        'agent_types': ['worker', 'idler'],
        'max_agents': np.inf,
        'resolution': (800, 800),
        'probability_return_home': 0.3
    }
