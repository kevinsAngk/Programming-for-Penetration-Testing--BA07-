from pynput import mouse
from pynput import keyboard

def on_release(key):
    if key == keyboard.Key.esc:
        exit()
    print(f"release{key}.")
    pass

def on_move(x,y):
    # print(f"print mouse position : {x}, {y}")

    pass

def on_click(x,y,btn,click):
    if not click and btn == mouse.Button.middle:
        return False

    print(f"print mouse{'clickerd' if click == True else 'released'} at position : {x}, {y} with {'left' if btn == mouse.Button.left  else'right'}")
    
    
    pass

def on_scroll(x,y,dx,dy):
    # mouse.scroll(0.2)
    print(f"print mouse is scrolled : {'up' if dy >0 else 'down'}to {x},{y}")
    pass


m = mouse.Listener(on_move, on_click, on_scroll)
m.start()
m.join()