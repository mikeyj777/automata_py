# backend/simulation/engine.py

import time
import threading
from models.agent import Agent
import numpy as np
import random
from config import Config

class SimulationEngine:
    def __init__(self, bounds=(100, 100), num_nodes = 5, num_poles = 3, params=None):
        self.bounds = bounds
        self.agents = []
        self.running = False
        self.params = params
        if self.params is None:
            self.params = Config.SIMULATION_PARAMS
        self.generate_nodes_and_poles(num_nodes, num_poles)
        self.lock = threading.Lock()


    def generate_nodes_and_poles(self, num_nodes=5, num_poles=3):
        self.nodes = []
        self.poles = []
        # for _ in range(num_nodes):
        #     self.nodes.append((random.randint(0, self.bounds[0]), random.randint(0, self.bounds[1])))
        # for _ in range(num_poles):
        #     self.poles.append((random.randint(0, self.bounds[0]), random.randint(0, self.bounds[1])))

        #hard coding star shaped pattern
        self.nodes = [(386, 29), (132,190), (568, 190)]
        self.poles = [(568, 461), (568, 190), (132,190)]

    def initialize_agents(self, num_agents=50):
        for _ in range(num_agents):
            position = np.random.uniform(0, self.bounds[0], size=2)
            angle = random.uniform(0, 2 * np.pi)
            velocity = np.array([np.cos(angle), np.sin(angle)]) * self.params['max_speed']
            agent = Agent(position, velocity)
            self.agents.append(agent)

    def update(self):
        with self.lock:
            if len(self.agents) < 0.1* self.params['num_agents']:
                self.initialize_agents(num_agents= int(0.5 *self.params['num_agents']))
            new_agents = []
            i = 0
            while i < len(self.agents):
                agent:Agent = self.agents[i]
                agent.age += 1
                if agent.age > self.params['max_age']:
                    self.agents.pop(i)
                    continue
                agent.apply_flocking(self.agents, self.params)
                agent.update_position(self.bounds)
                if len(self.agents) < Config.SIMULATION_PARAMS['max_agents']:
                    new_agent = agent.reproduce(self.agents, self.params)
                    if new_agent:
                        new_agents.append(new_agent)
                agent.assign_task(self.nodes, self.poles, self.params)
                agent.perform_task(self.params)
                i += 1
            self.agents.extend(new_agents)

    def get_state(self):
        with self.lock:
            # return {
            #     'agents': self.agents
            # }

            # the statement below returns a list of dictionaries based on the agent properties.  however, rest of app is expecting list of agents.
            return [
                {
                    'id': agent.id,
                    'position': agent.position.tolist(),
                    'velocity': agent.velocity.tolist(),
                    'state': agent.state,
                    'task': agent.task,
                    'color': agent.color,
                }
                for agent in self.agents
            ]

    def run(self, update_interval=0.1):
        self.running = True
        while self.running:
            self.update()
            # time.sleep(update_interval)

    def stop(self):
        self.running = False
