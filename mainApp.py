import os
import time
from threading import Thread
from generateMesh import generateMesh
from generateMicrostructure import generate_microstructure
import PySimpleGUI as gui

# Simulation variables
algorithm = "CA"
from_empty_simulation = True
step_limit = 50
absorbing = False
random_nucleation_sites = True
neighbourhood_type = "VN"
number_of_grain_types = 5
number_of_nucleation_sites = 100

# Set app theme
gui.theme('dark grey 11')


# Display popup without window frame
def popup(message):
    gui.theme('Black')
    content = [[gui.Text(message)]]
    return gui.Window('Message', content, no_titlebar=True, keep_on_top=True, finalize=True)


# Check for existing data files
# Microstructure files
if os.path.exists("output/Input.png") & os.path.exists("output/Output.png"):
    input_path = "output/Input.png"
    output_path = "output/Output.png"
else:
    input_path = "blank.png"
    output_path = "blank.png"

# Mesh files
if os.path.exists("output/mesh.png"):
    mesh_path = "output/mesh.png"
else:
    mesh_path = "blank.png"

# Define the window's contents
layout = [
    # Images
    [gui.Text("Initial state                                                     "),
     gui.Text("Finished microstructure                                           "),
     gui.Text("Generated Mesh")],
    [gui.Image(input_path, key="input_img"),
     gui.Image(output_path, key="output_img"),
     gui.Image(mesh_path, key="mesh_img")],

    # Menu
    [gui.HSeparator(pad=((20, 20), (20, 10)))],
    [gui.Text("Simulation configuration:", font=('Arial', 14, 'bold'))],
    [gui.Text("Simulation type: "), gui.Combo(
        ["Cellular Automata", "Monte Carlo"],
        default_value="Cellular Automata",
        readonly=True,
        key="sim_type",
        enable_events=True
    )],
    [gui.Checkbox("Create from empty simulation", default=True, disabled=True, key="empty_sim")],
    [gui.Text("Steps limit ", pad=((0, 0), (20, 0))),
     gui.Slider((10, 150), 50, 1, orientation="horizontal")],
    [gui.Checkbox("Absorbing boundary ")],
    [gui.Checkbox("Periodic seeding ")],
    [gui.Text("Neighbourhood type "), gui.Combo(
        ["Von Neumann", "Random Hexagonal"],
        default_value="Von Neumann",
        readonly=True,
        key="neighbour_type",
        enable_events=True
    )],
    [gui.Text("Number of grain types ", pad=((0, 0), (20, 0))),
     gui.Slider((2, 9), 5, 1, orientation="horizontal")],
    [gui.Text("Number of seeds ", pad=((0, 0), (20, 0))),
     gui.Slider((10, 250), 100, 1, orientation="horizontal")],

    # Buttons
    [gui.HSeparator(pad=(0, 20))],
    [gui.Button("Generate microstructure", key="microstructure_button",
                pad=((10, 10), (0, 20)), font=('Arial', 12, 'bold')),
     gui.Button("Generate mesh", key="mesh_button",
                disabled=not (os.path.exists("output/Input.png") & os.path.exists("output/Output.png")),
                pad=((10, 10), (0, 20)), font=('Arial', 12, 'bold'))]
]

# Create the window
window = gui.Window('Dominik Kruczek | Microstructure generator', layout, element_justification='c')

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == gui.WINDOW_CLOSED or event == 'Quit':
        break
    # Generate microstructure
    elif event == 'microstructure_button':
        
        tmp = popup("Processing...")
        generate_microstructure(algorithm, random_nucleation_sites, absorbing, neighbourhood_type,
                                from_empty_simulation, number_of_nucleation_sites, number_of_grain_types, step_limit)
        window['input_img'].update(filename='output/Input.png')
        window['output_img'].update(filename='output/Output.png')
        window['mesh_button'].update(disabled=False)
        # tmp.close()
    # Generate mesh from microstructure
    elif event == 'mesh_button':
        tmp = popup("Processing...")
        generateMesh()
        window['mesh_img'].update(filename='output/mesh.png')
    # Change options visibility
    elif event == 'sim_type':
        if values['sim_type'] == "Monte Carlo":
            window['empty_sim'].update(disabled=False)
        elif values['sim_type'] == "Cellular Automata":
            window['empty_sim'].update(disabled=True)

# Finish up by removing from the screen
window.close()
