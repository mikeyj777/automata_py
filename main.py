
import threading

from simulation.engine import SimulationEngine
from view.visualization_pyopengl import Visualization
from config import Config

import logging

num_nodes = 10
num_poles = 10

vis = Visualization()

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Simulation Engine
engine = SimulationEngine(bounds=(800, 600), num_nodes=num_nodes, num_poles=num_poles)
engine.initialize_agents(num_agents=Config.SIMULATION_PARAMS['num_agents'])

def simulation_thread():
    logging.info('Simulation thread started')
    while engine.running:

        engine.update()
        state = engine.get_state()

        for event in vis.pygame.event.get():
            if event.type == vis.pygame.QUIT:
                vis.pygame.quit()
                engine.running = False
                return

        vis.draw_agents(state)
        vis.pygame.display.flip()  # Update the display
        vis.pygame.time.wait(10)  # Add a short delay to control the frame rate
        # logging.debug(f'State retrieved\n\n\n')
        # Ensure state contains 'agents' and it's an array

        

if __name__ == '__main__':
    engine.running = True
    simulation_thread()
