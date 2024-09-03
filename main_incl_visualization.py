
import threading

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from simulation.engine import SimulationEngine
from view.visualization_pyopengl import Visualization
from config import Config

import logging

num_nodes = 2
num_poles = 1


pygame.init()
display = Config.SIMULATION_PARAMS['resolution']
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

gluPerspective(30, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)
# glTranslatef(-1.0, -1.0, -2)  # Move the camera closer to the agents


# Set point size for better visibility
glPointSize(10)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Simulation Engine
engine = SimulationEngine(bounds=display, num_nodes=num_nodes, num_poles=num_poles)
engine.initialize_agents(num_agents=Config.SIMULATION_PARAMS['num_agents'])


logging.info('Simulation thread started')

engine.running = True
while engine.running:

    engine.update()
    agents = engine.get_state()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear the screen
    glBegin(GL_POINTS)
    for agent in agents:
        glColor3f(*agent['color'])
        x, y = agent['position']
        x = (x / display[0]) * 2 - 1
        y = (y / display[1]) * 2 - 1
        glVertex3f(x, y, 0)
    glEnd()

    pygame.display.flip()
    pygame.time.wait(10)  # Add a short delay to control the frame rate
    # logging.debug(f'State retrieved\n\n\n')
    # Ensure state contains 'agents' and it's an array

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            engine.running = False
            break
