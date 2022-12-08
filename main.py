import itertools
import random
from abaqus import *
from abaqusConstants import *
from driverUtils import *
import numpy as np


# Variables
# Simulation size: 300x300
simulation_width = 30
simulation_height = 10
# How many grain types there are
number_of_grain_types = 9
# How many nucleation sites (default 3% of whole simulation)
number_of_nucleation_sites = int((simulation_width * simulation_height * 0.03))
# Determines if neighbourhood should be accessed at random
random = False
# Neighbourhood types, stored as array of offsets from current cell (x, y)
von_neuman = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def cellular_automata():
    # 1. Simulation setup
    # Create empty simulation
    current_state = np.zeros((simulation_height, simulation_width), np.int8)
    # Choose neighbourhood to use
    neighbourhood = np.copy(von_neuman)
    
    # 2. Create random nucleation sites
    # TODO FIX change boundary conditions?
    created_seeds = 0
    while created_seeds != number_of_nucleation_sites:
        # Pick random index x and y index
        x_index = np.random.randint(0, simulation_width)
        y_index = np.random.randint(0, simulation_height)
        # Create new nucleation site in empty cell
        if current_state[y_index, x_index] == 0:
            current_state[y_index, x_index] = np.random.randint(1, number_of_grain_types + 1)
            created_seeds += 1

    # Copy current state to temporary array
    next_state = np.copy(current_state)

    print(current_state)

    # 3. Go through the simulation loop until all cells are filled
    while np.count_nonzero(current_state) != current_state.size:
        # Perform single step of the simulation
        # TODO FIX, omit boundaries then looping
        for y in range(simulation_height):
            for x in range(simulation_width):
                if current_state[y, x] == 0:
                    # TODO FIX IT, cell should pick value based on most popular neighbour,
                    #  if multiple have the same value, pick at random
                    # TODO modify it to be able to use different types of neighbourhoods
                    # If neighbourhood should be randomly accessed, shuffle the list
                    if random:
                        np.random.shuffle(neighbourhood)

                    # TODO Loop to check through whole neighbourhood
                        # TODO if we hit non 0 cell, increase its counter

                    # TODO pick the cell with the highest counter, if many have the same, pick at random
                        # TODO use map, where key is grain ID, value is number of occurrences
                        # TODO find max value from map
                        # TODO remove all entries where value is not max?
                        # TODO https://thispointer.com/delete-elements-from-a-numpy-array-by-value-or-conditions-in-python/
                    # # Check above
                    # if y != 0:
                    #     if current_state[y-1, x] != 0:
                    #         next_state[y, x] = current_state[y-1, x]
                    #         continue
                    # # Check to the right
                    # if x != simulation_width-1:
                    #     if current_state[y, x+1] != 0:
                    #         next_state[y, x] = current_state[y, x+1]
                    #         continue
                    # # Check below
                    # if y != simulation_height-1:
                    #     if current_state[y+1, x] != 0:
                    #         next_state[y, x] = current_state[y+1, x]
                    #         continue
                    # # Check to the left
                    # if x != 0:
                    #     if current_state[y, x-1] != 0:
                    #         next_state[y, x] = current_state[y, x-1]
                    #         continue

        # Advance to next step in simulation
        current_state = np.copy(next_state)

    # Display final result
    print("CA: \n", current_state)


def monte_carlo():
    # 1. Randomize initial structure
    current_state = np.random.randint(1, number_of_grain_types + 1, (simulation_height, simulation_width))
    # Copy initial simulation state
    next_state = np.copy(current_state)

    # Create list of index pairs (x,y)
    # TODO FIX, omit boundaries?
    indexes = list(itertools.product(np.arange(simulation_width), np.arange(simulation_height)))

    # TODO infinite loop here

    # Shuffle the list
    random.shuffle(indexes)
    # Go through the whole list
    for index in indexes:
        print(index)
        # TODO 3. Calculate cell energy
        # Calculate energy of the selected cell

        # TODO 4. Change cell state to random one from its neighbourhood

        # TODO 5. Calculate new energy

        # TODO 6. Decide to keep the change based on probability
        # Probability 1 if new energy is smaller
        # Probability exp(-energy diff/kt) if new energy is bigger

    current_state = np.copy(next_state)
    # TODO end of main loop here

    # Show to result
    print("MC: \n", current_state)


# --------------------------------- Main program  --------------------------------- #
cellular_automata()

# monte_carlo()
