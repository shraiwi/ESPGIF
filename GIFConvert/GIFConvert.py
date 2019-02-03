from PIL import Image
import sys
import os

import tkinter as tk
import tkinter.filedialog as filedialog

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

text = open('out.txt', mode='w', newline=None)

def send(msg):
    text.write(msg)

def to565(color):
    r, g, b = color
    return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | ((b & 0xF8) >> 3)

def string565(color):
    return hex(to565(color))

linelen = 30;

resolution = (128, 128)

root = tk.Tk()
root.withdraw()

path = filedialog.askopenfilename(title = "Select GIF")

im = Image.open(path)

palette = im.getpalette()

send("/* Converted using GIF2BYTE <3\n")
send(" * Copy this text into your program!*/\n")

send("\n#define NUM_FRAMES " + str(im.n_frames))

delay = 2000 / im.n_frames - (im.n_frames * 40)

if delay < 0:
    delay = 0;
    print("The GIF will not play at native speed, but at the max possible framerate.")

send("\n#define DELAY " + str(delay) + "\n\n")

colors = list(chunks(palette, 3))

print("generating palette...")

send("const uint16_t palette[] PROGMEM = {\n")

counter = 0

for value in colors:
    send(string565(value) + ",\t")
    
    counter += 1
    
    if counter == linelen:
        counter = 0
        send("\n")

send("\n};")

kb = (resolution[0] * resolution[1] * 1 * im.n_frames + 255) / 1024

print("size: " + str(kb) + " KiB.")

large = False

if kb > 700:
    large = True
    print("warning: might not fit into ESP8266 flash")

send("\nconst uint8_t frameData[][" + str(resolution[0] * resolution[1]) + "] PROGMEM = {\n")

for n in range(im.n_frames):

    im.seek(n)

    '''
    crop = (0, 0, 0, 0)

    if im.width > im.height:
        crop = (0,
                (im.height - resolution[0]) / 2,
                im.width,
                (im.height + resolution[1]) / 2)
    else:
        crop = ((im.width - resolution[0]) / 2,
                0,
                (im.width + resolution[1]) / 2,
                im.height)

    frame = im.crop(crop)
    '''
    
    frame = im.resize(resolution)

    frame = frame.transpose(Image.FLIP_LEFT_RIGHT)
    frame = frame.transpose(Image.ROTATE_90)
    
    # frame.save('frames/img' + str(n) + '.png')

    print("converting frame" + str(n))

    send("/* Frame " + str(n) + " */\n{\n")

    counter = 0
    
    for x in range(resolution[0]):
        for y in range(resolution[1]):
            send(str(frame.getpixel((x, y))) + ",\t")
            counter += 1
            if counter == linelen:
                counter = 0
                send("\n")
            

    send("},\n")

send("\n};")

text.close()

os.startfile('out.txt')

print("complete!")

