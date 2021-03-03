import numpy as np
import time
from PIL import Image
from ppadb.client import Client

# Automating android Game Stick Hero

# Checking available devices via ADB
adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()
if(len(devices) == 0):
    print('no device attached ! \n')
    quit()
device = devices[0]
# Taking screenshot and storing it as png file
while True:
    transitions = []
    image = device.screencap()
    with open('screen.png', 'wb') as f:
        f.write(image)
    image = Image.open('screen.png')
    # Converting image to 2d Array
    image = np.array(image, dtype=np.uint8)
    # print(image[2000])
    ignore = True
    black = True
    # Getting list of pixels on 200th row,approximated by testing
    # Removing the 4th value(channel value)
    pixels = [list(i[:3]) for i in image[2000]]
    for i, pixel in enumerate(pixels):
        r, g, b = [int(i) for i in pixel]
        # Ignoring the initial pixels which may not be black
        if ignore and r+g+b != 0:
            continue
        ignore = False
        # If black is true but color is not black,we get our starting point
        if black and r+g+b != 0:
            black = not black
            transitions.append(i)
            continue
        # Again if we see color but the sum results into black,we have reached the pillar
        if not black and r+g+b == 0:
            black = not black
            transitions.append(i)
            continue
    # Getting the positions
    start, pillar1, pillar2 = transitions
    # Calculating distances
    gap = pillar1-start
    width = pillar2-pillar1
    # Adjusting to get PERFECT everytime
    distance = (gap+width/2)*0.98
    # ADB command to interact with android, here distance and frame time is almost same,so we can use distance
    device.shell(f'input touchscreen swipe 500 500 500 500 {int(distance)}')
    # Wait for the next turn
    time.sleep(2.3)
