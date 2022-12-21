import PySimpleGUI as gui

# Define the window's contents
layout = [[gui.Text("What's your name?")],
          [gui.Input(key='-INPUT-')],
          [gui.Text(size=(40, 1), key='-OUTPUT-')],
          [gui.Button('Ok'), gui.Button('Quit')]]

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
