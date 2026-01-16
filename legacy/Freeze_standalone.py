import pyautogui
from pynput import keyboard
import mouse
import time
import threading
import pynput

# Initialize variables
saved_coordinates = None
saved_coordinatesBefore = None
holding_keys = False
f3_pressed = False
spacebar_pressed = False

def press_spacebar():
    global spacebar_pressed
    while spacebar_pressed:
        keyboard.Controller().press(keyboard.Key.space)
        time.sleep(0.1)
        keyboard.Controller().release(keyboard.Key.space)
        time.sleep(0.1)

def on_press(key):
    global saved_coordinates, holding_keys, f3_pressed, spacebar_pressed
    try:
        if key.char.lower() == 'q' and saved_coordinates is None:
            # Save mouse coordinates when Q is pressed for the first time
            saved_coordinates = pyautogui.position()
            print(f"Saved coordinates: {saved_coordinates}")
    except AttributeError:
        if key == keyboard.Key.f3 and saved_coordinates is not None:
            # Toggle F3 key
            f3_pressed = not f3_pressed
            if f3_pressed:
                # Move mouse to saved coordinates and hold LMB and spacebar when F3 is pressed
                global saved_coordinatesBefore
                saved_coordinatesBefore = pyautogui.position()
                print("F3 key pressed")
                print("Freeze Toggle True")
                mouse.release('left')
                mouse.release('right')
                mouse.move(*saved_coordinates)
                mouse.press('left')
                spacebar_pressed = True
                threading.Thread(target=press_spacebar).start()
                global mouse_listener
                mouse_listener = pynput.mouse.Listener(suppress=True)
                mouse_listener.start()
                
                
            else:
                # Release LMB and spacebar when F3 is released
                print("F3 key pressed")
                print("Freeze Toggle False")
                spacebar_pressed = False
                mouse_listener.stop()
                mouse.release('left')
                mouse.move(*saved_coordinatesBefore)



# Prompt user to move mouse and press Q
print("Move the mouse to the desired location and press Q to save the coordinates.")

# Collect events until released

listener = keyboard.Listener(on_press=on_press)
listener.start()
listener.join()
