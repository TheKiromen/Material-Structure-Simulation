import PySimpleGUI as gui

# Set app theme
gui.theme('dark grey 11')

# Define the window's contents
layout = [
        [gui.Text("Initial state                                                          "),
         gui.Text("Finished microstructure                                        "),
         gui.Text("Generated Mesh")],
        [gui.Image(r'blank.png'), gui.Image(r'blank.png'), gui.Image(r'blank.png')],
        [gui.HSeparator()],
        ]

# TODO
# Add input fields:
# Simulation type - combo box
# If "MC" selected, activate check box for "Generate from empty simulation"
# Neighbourhood type - combo box
# Checkboxes for randomNucleationSites and absorbing boundary condition
# Sliders for NumberOfNucleationSites and NumberOfGrainTypes


# Create the window
window = gui.Window('Window Title', layout)

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == gui.WINDOW_CLOSED or event == 'Quit':
        break
    # Output a message to the window
    window['-OUTPUT-'].update('Hello ' + values['-INPUT-'] + "! Thanks for trying PySimpleGUI")

# Finish up by removing from the screen
window.close()
