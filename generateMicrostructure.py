import itertools
# from abaqus import *
# from abaqusConstants import *
# from driverUtils import *
from PIL import Image
import numpy as np

global initial_simulation


def generate_microstructure(algorithm, random_nucleation_sites, absorbing, neighbourhood_type, from_empty_simulation):
    # Image color schema in RGB format
    colors = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (255, 255, 0), (0, 255, 255),
              (0, 0, 255), (255, 0, 255), (125, 125, 255), (125, 255, 125), (255, 125, 125)]
    # Variables
    # Simulation size: 300x300
    simulation_width = 100
    simulation_height = 100
    # Simulation step limit for Monte Carlo method
    step_limit = 30
    # Constant for cell change probability
    kt = 0.2
    # How many grain types there are
    number_of_grain_types = 5
    # How many nucleation sites (default 3% of whole simulation)
    number_of_nucleation_sites = int((simulation_width * simulation_height * 0.01))
    # Spacing for periodic generation
    seed_step = int(simulation_height * 0.2)
    # Determine if random nucleation sites should be used
    random_nucleation_sites = random_nucleation_sites
    # Determine if edges should be absorbing or periodic
    absorbing = absorbing
    # Neighbourhood types, stored as array of offsets from current cell (x, y)
    # Possible neighbourhoods are: VN = Von Neuman, Hex = Random Hexagonal
    neighbourhood_type = neighbourhood_type
    von_neuman = [[(0, -1), (1, 0), (0, 1), (-1, 0)]]
    hexagonal = [[(0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1)],
                 [(-1, -1), (0, -1), (-1, 0), (1, 0), (0, 1), (1, 1)]]
    global initial_simulation
    initial_simulation = np.zeros((simulation_height, simulation_width), np.int8)

    def cellular_automata():
        # 1. Simulation setup
        # Create empty simulation
        current_state = np.zeros((simulation_height, simulation_width), np.int8)
        # Determine area to traverse based on edge type
        if absorbing:
            start_x = 1
            start_y = 1
            end_x = simulation_width - 1
            end_y = simulation_height - 1
        else:
            start_x = 0
            start_y = 0
            end_x = simulation_width
            end_y = simulation_height

        # Choose neighbourhood to use
        if neighbourhood_type == "Hex":
            neighbourhood = np.copy(hexagonal)
        else:
            neighbourhood = np.copy(von_neuman)

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
            for y in range(1, simulation_height - 1, seed_step):
                for x in range(1, simulation_width, seed_step):
                    current_state[y, x] = np.random.randint(1, number_of_grain_types + 1)

        # Copy current state to temporary array
        next_state = np.copy(current_state)
        # Save input state
        global initial_simulation
        initial_simulation = np.copy(current_state)

        # 3. Go through eth simulation loop until all cells are filled
        # Determine the end goal
        if absorbing:
            # If boundaries are absorbing, the goal is to have non-zero values everywhere but at the edges
            goal = (simulation_width - 2) * (simulation_height - 2)
        else:
            # If boundaries are periodic, the goal is to have full simulation filled, that is no zeros at all
            goal = current_state.size

        # Go through the simulation
        while np.count_nonzero(current_state) != goal:
            # Perform single step of the simulation
            for y in range(start_y, end_y):
                for x in range(start_x, end_x):
                    if current_state[y, x] == 0:

                        # Initialize the counter
                        counter = np.zeros(number_of_grain_types + 1, np.int8)

                        # Randomize the neighbourhood
                        current_neighbourhood = neighbourhood[np.random.randint(0, len(neighbourhood))]

                        # Loop through the neighbourhood
                        for offset in current_neighbourhood:
                            # Calculate neighbour coordinates
                            new_x = x + offset[0]
                            new_y = y + offset[1]

                            # Check for boundaries
                            if new_x < 0:
                                new_x = new_x + simulation_width
                            if new_x >= simulation_width:
                                new_x = 0
                            if new_y < 0:
                                new_y = new_y + simulation_height
                            if new_y >= simulation_height:
                                new_y = 0

                            # Increase the counter
                            counter[current_state[new_y, new_x]] += 1

                        # Clear out the zero's
                        counter[0] = 0
                        # Get number of most occurrences
                        maximum = np.amax(counter)
                        # Find what are the most common neighbours
                        if maximum != 0:
                            indexes = np.where(counter == maximum)[0]
                        else:
                            indexes = [0]
                        # Pick one at random
                        np.random.shuffle(indexes)
                        next_state[y, x] = indexes[0]

            # Advance to next step in simulation
            current_state = np.copy(next_state)

        return current_state

    def monte_carlo(initial_state):
        # 1. Simulation setup
        # Start from initial state
        current_state = np.copy(initial_state)
        # Determine area to traverse based on edge type
        if absorbing:
            start_x = 1
            start_y = 1
            end_x = simulation_width - 1
            end_y = simulation_height - 1
        else:
            start_x = 0
            start_y = 0
            end_x = simulation_width
            end_y = simulation_height

        # Create indexes for all cells in the simulation
        indexes = list(itertools.product(np.arange(start_x, end_x), np.arange(start_y, end_y)))

        # Choose neighbourhood to use
        if neighbourhood_type == "Hex":
            neighbourhood = np.copy(hexagonal)
        else:
            neighbourhood = np.copy(von_neuman)

        # 2. If empty simulation, Create random nucleation sites
        if np.count_nonzero(current_state) == 0:
            # Generate random nucleation sites
            if random_nucleation_sites:
                current_state = np.random.randint(1, number_of_grain_types + 1, (simulation_height, simulation_width))

            # Generate periodic nucleation sites
            else:
                i = 0
                for y in range(simulation_height):
                    for x in range(simulation_width):
                        current_state[y, x] = (i % number_of_grain_types) + 1
                        i += 1

        # Determine the border type
        if absorbing:
            current_state[0, :] = 0
            current_state[simulation_height - 1, :] = 0
            current_state[:, 0] = 0
            current_state[:, simulation_width - 1] = 0

        # Copy current state to temporary array
        next_state = np.copy(current_state)
        # Save input state
        global initial_simulation
        initial_simulation = np.copy(current_state)

        # Go through the simulation
        for step in range(step_limit):
            # Randomise index order
            np.random.shuffle(indexes)
            # Loop through the whole simulation
            for index in indexes:
                # Initialize the counter
                counter = np.zeros(number_of_grain_types + 1, np.int8)

                # Randomize the neighbourhood
                current_neighbourhood = neighbourhood[np.random.randint(0, len(neighbourhood))]

                # Loop through the neighbours
                for offset in current_neighbourhood:
                    # Calculate neighbour coordinates
                    new_x = index[0] + offset[0]
                    new_y = index[1] + offset[1]

                    # Check for boundaries
                    if new_x < 0:
                        new_x = new_x + simulation_width
                    if new_x >= simulation_width:
                        new_x = 0
                    if new_y < 0:
                        new_y = new_y + simulation_height
                    if new_y >= simulation_height:
                        new_y = 0

                    # Increase the counter
                    counter[current_state[new_y, new_x]] += 1

                # Check if current cell has different neighbours
                if counter[current_state[index[1], index[0]]] == current_neighbourhood.size:
                    continue
                # Clear out the zero's
                counter[0] = 0
                # Get energy for current cell
                current_energy = current_neighbourhood.size - counter[current_state[index[1], index[0]]]
                # Remove all elements that are not in neighbourhood
                candidates = np.where(counter != 0)[0]
                # Get new energy for random cell change
                candidate = candidates[np.random.randint(0, candidates.size)]
                new_energy = current_neighbourhood.size - counter[candidate]
                # Calculate energy difference
                energy_difference = new_energy - current_energy

                # Pick new cell based on energy
                if energy_difference > 0:
                    probability = np.exp(-energy_difference / kt)
                    if np.random.random() < probability:
                        next_state[index[1], index[0]] = candidate
                else:
                    next_state[index[1], index[0]] = candidate

            # Advance to next step in simulation
            current_state = np.copy(next_state)
        return current_state

    # --------------------------------- Main program  --------------------------------- #
    # Determine what algorithm to use
    # Cellular Automata
    if algorithm == "CA":
        output = cellular_automata()
    # Monte Carlo
    elif algorithm == "MC":
        # Determine if there should be input to Monte Carlo method
        # Generate empy simulation
        if from_empty_simulation:
            input_state = np.zeros((simulation_height, simulation_width), np.int8)
        # Generate simulation from CA input
        else:
            # Generate the input
            input_state = cellular_automata()
        # Perform the MC simulation
        output = monte_carlo(input_state)
    else:
        print("Invalid algorithm")
        return

    # Generate images
    if absorbing:
        border_offset = 1
    else:
        border_offset = 0
    output_image = Image.new("RGB", (simulation_width - (border_offset * 2), simulation_height - (border_offset * 2)))
    output_pixels = output_image.load()
    initial_image = Image.new("RGB", (simulation_width - (border_offset * 2), simulation_height - (border_offset * 2)))
    initial_pixels = initial_image.load()
    # Loop through the whole image
    for img_y in range(simulation_height - (border_offset * 2)):
        for img_x in range(simulation_width - (border_offset * 2)):
            # Assign color to each pixel
            output_pixels[img_x, img_y] = colors[output[img_y + border_offset, img_x + border_offset]]
            initial_pixels[img_x, img_y] = colors[initial_simulation[img_y + border_offset, img_x + border_offset]]
    # Save resulting images
    output_image.save("output/mesh_src.png")
    output_image = output_image.resize((simulation_width * 3, simulation_height * 3), Image.NEAREST)
    output_image.save('output/Output.png')
    initial_image = initial_image.resize((simulation_width * 3, simulation_height * 3), Image.NEAREST)
    initial_image.save('output/Input.png')


# Arguments:
# Type of simulation: "CA" or "MC"
# Random nucleation sites: True/False
# Absorbing boundary conditions: True/False
# Neighbourhood type: "VN" or "Hex"
# Create from empty simulation: True/False
generate_microstructure("CA", True, True, "Hex", False)
