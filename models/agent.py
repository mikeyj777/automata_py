# backend/models/agent.py

import numpy as np
import uuid
import random
from config import Config

class Agent:
    def __init__(self, position, velocity):
        self.id = str(uuid.uuid4())
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.state = 'idle'  # or 'carrying'
        self.type = random.choice(Config.SIMULATION_PARAMS['agent_types'])
        self.task = None  # e.g., {'type': 'carry', 'destination': (x, y)}
        self.reproduction_probability = Config.SIMULATION_PARAMS['reproduction_probability']
        self.set_color()
        self.age = 0
        self.lifespan = random.random() * Config.SIMULATION_PARAMS['max_age']
    
    def set_color(self):
        colors = Config.SIMULATION_PARAMS['colors']
        self.color = random.choice(colors)
        self.color = np.array(self.color, dtype=float)
        self.color /= 255

    def update_position(self, bounds):
        self.position += self.velocity
        # Simple boundary conditions
        for i in range(2):
            if self.position[i] < 0 or self.position[i] > bounds[i]:
                self.velocity[i] *= -1
                self.position[i] = max(0, min(self.position[i], bounds[i]))

    def apply_flocking(self, agents, params):
        # Boids algorithm: alignment, cohesion, separation
        alignment = np.zeros(2)
        cohesion = np.zeros(2)
        separation = np.zeros(2)
        total = 0
        for agent in agents:
            if agent.id == self.id:
                continue
            distance = np.linalg.norm(agent.position - self.position)
            if distance < params['neighbor_distance']:
                alignment += agent.velocity
                cohesion += agent.position
                separation_factor = 1e-4
                if (agent.color == self.color).all():
                    separation_factor /= 10
                separation += (self.position - agent.position) / (distance + separation_factor)
                total += 1
        if total > 0:
            alignment /= total
            alignment = (alignment / np.linalg.norm(alignment)) * params['max_speed']
            cohesion = (cohesion / total - self.position)
            if np.linalg.norm(cohesion) != 0:
                cohesion = (cohesion / np.linalg.norm(cohesion)) * params['max_speed']
            separation = separation / total
            if np.linalg.norm(separation) != 0:
                separation = (separation / np.linalg.norm(separation)) * params['max_speed']
            # Update velocity
            self.velocity += params['alignment_weight'] * (alignment - self.velocity)
            self.velocity += params['cohesion_weight'] * cohesion
            self.velocity += params['separation_weight'] * separation
            # Limit speed
            speed = np.linalg.norm(self.velocity)
            if speed > params['max_speed']:
                self.velocity = (self.velocity / speed) * params['max_speed']

    def reproduce(self, agents, params):
        if random.random() < self.reproduction_probability:
            # Simple reproduction: create a new agent near the parent
            offset = np.random.uniform(-1, 1, size=2)
            new_position = self.position + offset
            new_velocity = np.random.uniform(-1, 1, size=2)
            new_agent = Agent(new_position, new_velocity)
            return new_agent
        return None

    def assign_task(self, nodes, poles, params):
        if self.state == 'idle' and self.type != 'non existent type':
            # Assign a new task based on some condition
            if len(nodes) > 0 and len(poles) > 0:
                node_idx = np.random.choice(len(nodes))
                target_node = nodes[node_idx]
                pole_idx = np.random.choice(len(poles))
                target_pole = poles[pole_idx]
                self.task = {
                    'type': 'carry',
                    'from': target_node,
                    'to': target_pole
                }
                self.state = 'carrying'

    def perform_task(self, nodes, poles, params):
        if self.state == 'carrying' and self.task:
            # Simple task: move towards destination
            destination = np.array(self.task['to'], dtype=float)
            direction = destination - self.position
            distance = np.linalg.norm(direction)
            if distance > 0:
                direction = direction / distance
                self.velocity = direction * params['task_speed']
                if distance < params['task_threshold']:
                    # Task completed
                    if random.random() < params['probability_return_home']:
                        self.task['from'], self.task['to'] = self.task['to'], self.task['from']
                        return
                    self.state = 'idle'
                    self.assign_task(nodes, poles, params)
                    
                    