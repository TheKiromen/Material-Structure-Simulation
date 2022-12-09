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
# Determine if random nucleation sites should be used
random_nucleation_sites = True
# Determine if edges should be absorbing or periodic
absorbing = False
# Neighbourhood types, stored as array of offsets from current cell (x, y)
neighbourhood_type = "VN"
von_neuman = [(0, -1), (1, 0), (0, 1), (-1, 0)]
hexagonal = [[(0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1)], [(-1, -1), (0, -1), (-1, 0), (1, 0), (0, 1), (1, 1)]]


def cellular_automata():
    # 1. Simulation setup
    # Create empty simulation
    current_state = np.zeros((simulation_height, simulation_width), np.int8)
    # Determine area to traverse based on edge type
    if absorbing:
        start_x = 1
        start_y = 1
        end_x = simulation_width-1
        end_y = simulation_height-1
    else:
        start_x = 0
        start_y = 0
        end_x = simulation_width
        end_y = simulation_height

    # Choose neighbourhood to use
    if neighbourhood_type == "Hex":
        neighbourhood = np.copy(hexagonal)
        random_neighbourhood = True
    else:
        neighbourhood = np.copy(von_neuman)
        random_neighbourhood = False

    # 2. Create random nucleation sites
    # Generate random nucleation sites
    if random_nucleation_sites:
        created_seeds = 0
        while created_seeds != number_of_nucleation_sites:
            # Pick random index x and y index
            x_index = np.random.randint(start_x, end_x)
            y_index = np.random.randint(start_y, end_y)
            # Create new nucleation site in empty cell
            if current_state[y_index, x_index] == 0:
                current_state[y_index, x_index] = np.random.randint(1, number_of_grain_types + 1)
                created_seeds += 1

    # Generate periodic nucleation sites
    else:
        for y in range(1, simulation_height-1, 3):
            for x in range(1, int(simulation_width/3), 3):
                current_state[y, x] = np.random.randint(1, number_of_grain_types + 1)

    # Copy current state to temporary array
    next_state = np.copy(current_state)

    print(current_state)

    # 3. Go through eth simulation loop until all cells are filled
    # Determine the end goal
    if absorbing:
        # If boundaries are absorbing, the goal is to have non-zero values everywhere but at the edges
        # TODO check if it calculates properly
        goal = current_state.size - (simulation_width*2 + (simulation_height-1)*2)
    else:
        # If boundaries are periodic, the goal is to have full simulation filled, that is no zeros at all
        goal = current_state.size

    # Go through the simulation
    while np.count_nonzero(current_state) != goal:
        # Perform single step of the simulation
        # TODO FIX, omit boundaries then looping
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
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
                    # Check above
                    if y != 0:
                        if current_state[y-1, x] != 0:
                            next_state[y, x] = current_state[y-1, x]
                            continue
                    # Check to the right
                    if x != simulation_width-1:
                        if current_state[y, x+1] != 0:
                            next_state[y, x] = current_state[y, x+1]
                            continue
                    # Check below
                    if y != simulation_height-1:
                        if current_state[y+1, x] != 0:
                            next_state[y, x] = current_state[y+1, x]
                            continue
                    # Check to the left
                    if x != 0:
                        if current_state[y, x-1] != 0:
                            next_state[y, x] = current_state[y, x-1]
                            continue

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
