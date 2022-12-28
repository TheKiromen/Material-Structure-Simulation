import os

import PySimpleGUI as gui

# Set app theme
gui.theme('dark grey 11')

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
         gui.Image(output_path,  key="output_img"),
         gui.Image(mesh_path,  key="mesh_img")],

        # Menu
        [gui.HSeparator(pad=((20, 20), (20, 10)))],
        [gui.Text("Simulation configuration:", font=('Arial', 14, 'bold'))],
        [gui.Text("Simulation type: "), gui.Combo(
            ["Cellular Automata", "Monte Carlo"],
            default_value="Cellular Automata",
            readonly=True,
            key="sim_type"
        )],
        [gui.Checkbox("Create from empty simulation", default=True, disabled=True)],
        [gui.Text("Steps limit ", pad=((0, 0), (20, 0))),
         gui.Slider((10, 150), 50, 1, orientation="horizontal")],
        [gui.Checkbox("Absorbing boundary ")],
        [gui.Checkbox("Periodic seeding ")],
        [gui.Text("Neighbourhood type "),  gui.Combo(
            ["Von Neumann", "Random Hexagonal"],
            default_value="Von Neumann",
            readonly=True,
            key="neighbour_type"
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
        # TODO
        window['input_img'].update(filename='output/Input.png')
        window['output_img'].update(filename='output/Output.png')
        window['mesh_button'].update(disabled=False)
    # Generate mesh from microstructure
    elif event == 'mesh_button':
        # TODO
        window['mesh_img'].update(filename='output/mesh.png')

# Finish up by removing from the screen
window.close()
