import pyscreenshot
from datetime import datetime
import time

while True:
    img = pyscreenshot.grab()
    img.save(f"{datetime.now().strftime('%y-%d-%m-%H-%M-%S')}.png")
    #delay 3 detik
    time.sleep(3)