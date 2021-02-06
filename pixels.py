import time
import board
import neopixel
from PIL import ImageFont

WIDTH = 8
HEIGHT = 8
BRIGHTNESS = 0.03
NEOPIXEL_PIN = board.D18

OFF = (0, 0, 0)
ON = (255, 255, 255)

FONT = ImageFont.truetype("PxPlus_IBM_BIOS.ttf", size=HEIGHT)
PIXELS = neopixel.NeoPixel(
    NEOPIXEL_PIN,
    HEIGHT * WIDTH,
    auto_write=False,
    brightness=BRIGHTNESS
)

COLOURS = {
    "white": ON,
    "red": (255, 0, 0),
    "blue": (0, 0, 255),
    "green": (0, 255, 0),
}

REPLACEMENTS = {
    "❤️": chr(0x2665),
    "🙂": chr(0x263A),
}


def subs(char):
    return REPLACEMENTS.get(char, char)


def get_forced_colour(char, x, y):
    if char == chr(0x2665):
        return COLOURS["red"]


def cleantext(text):
    text = text.strip()
    for find, replace in REPLACEMENTS.items():
        text = text.replace(find, replace)
    return text


def scrolltext(text, colour=None, delay=0.05):
    data = []

    if colour == "rainbow":
        rainbow_idx = 0
    else:
        override_colour = COLOURS.get(colour)
        fill_colour = override_colour if override_colour else ON

    for _ in range(WIDTH):
        col = []
        for _ in range(HEIGHT):
            col.append(OFF)
        data.append(col)

    for char in text:
        mask = FONT.getmask(char)
        char_width, char_height = mask.size
        char_y_offset = FONT.getoffset(char)[1]
        for x in range(char_width):
            if colour == "rainbow":
                fill_colour = rainbow(rainbow_idx % 256)
                rainbow_idx += 1
            col = []
            for _ in range(char_y_offset):
                col.append(OFF)
            for y in range(char_height):
                forced_colour = get_forced_colour(char, x, y)
                actual_colour = forced_colour if forced_colour else fill_colour
                col.append(actual_colour if mask.getpixel((x, y)) else OFF)
            while len(col) < HEIGHT:
                col.append(OFF)
            data.append(col)

    for _ in range(WIDTH):
        col = []
        for _ in range(HEIGHT):
            col.append(OFF)
        data.append(col)

    for idx in range(len(data) - WIDTH):
        for x in range(WIDTH):
            for y in range(HEIGHT):
                PIXELS[y * HEIGHT + x] = data[idx + x][y]
        PIXELS.show()
        time.sleep(delay)

    PIXELS.fill(OFF)
    PIXELS.show()


def displaychar(char, colour=None):
    PIXELS.fill(OFF)
    mask = FONT.getmask(char)
    char_width, char_height = mask.size
    char_y_offset = FONT.getoffset(char)[1]

    override_colour = COLOURS.get(colour)
    fill_colour = override_colour if override_colour else ON

    for x in range(char_width):
        for y in range(char_height):
            forced_colour = get_forced_colour(char, x, y)
            actual_colour = forced_colour if forced_colour else fill_colour
            PIXELS[(y + char_y_offset) * HEIGHT + x] = actual_colour if mask.getpixel((x, y)) else OFF
    PIXELS.show()


def rainbow(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b)
