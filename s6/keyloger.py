from pynput import*

def on_press(key):
    print(f"press{key}.")


def on_release(key):
    if key == keyboard.Key.esc:
        exit()
    print(f"release{key}.")
    pass

#create thread
k= keyboard.Listener(on_press, on_release)
k.start()
k.join()