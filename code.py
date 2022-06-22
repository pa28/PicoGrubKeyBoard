"""
adapted from http://helloraspberrypi.blogspot.com/2021/01/raspberry-pi-picocircuitpython-st7789.html
"""

import os
import board
import time
import json
import terminalio
import displayio
import digitalio
import busio
import usb_hid
import supervisor
import adafruit_rgbled
from adafruit_display_text import label
from adafruit_debouncer import Debouncer
from adafruit_ticks import ticks_ms, ticks_add, ticks_less
from adafruit_hid.mouse import Mouse
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
import adafruit_st7789


led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = False

# Pin the Red LED is connected to
RED_LED = board.GP6

# Pin the Green LED is connected to
GREEN_LED = board.GP7

# Pin the Blue LED is connected to
BLUE_LED = board.GP8

# Create a RGB LED object
rgbled = adafruit_rgbled.RGBLED(RED_LED, GREEN_LED, BLUE_LED, invert_pwm = True)
rgbled.color = (0, 0, 0)

def progressMark(color):
    for n in range(3):
        rgbled.color = color
        time.sleep(0.1)
        rgbled.color = (0, 0, 0)
        time.sleep(0.1)

def keyPress(state, keyCode):
    state.keyboard.press(keyCode)
    state.keyboard.release_all()

def defineSwitch(switch_pin):
    pin = digitalio.DigitalInOut(switch_pin)
    pin.direction = digitalio.Direction.INPUT
    pin.pull = digitalio.Pull.UP
    switch = Debouncer(pin)
    return switch

class State:
    def __init__(self):
        self.setBoot()

    def setBoot(self):
        self.state = 0
        self.delay = 0
        self.hidConfig = False
        self.mouse = 0
        self.keyboard = 0
        self.keyboard_layout = 0
    
    def configHid(self):
        if not self.hidConfig:
            self.mouse = Mouse(usb_hid.devices)
            self.keyboard = Keyboard(usb_hid.devices)
            self.keyboard_layout = KeyboardLayoutUS(self.keyboard)  # We're in the US :)
            self.hidConfig = True

    def isBoot(self):
        return self.state == 0
    
    def setNoHost(self):
        self.state = 1
    
    def isNoHost(self):
        return self.state == 1
    
    def setConnected(self):
        self.configHid()
        self.state = 2
    
    def isConnected(self):
        return self.state == 2
    
    def setGrub(self):
        self.configHid()
        self.state = 3
    
    def isGrub(self):
        return self.state == 3
    
print("==============================")
print(os.uname())
print("Hello Raspberry Pi Pico/CircuitPython ST7789 SPI IPS Display")
print(adafruit_st7789.__name__ + " version: " + adafruit_st7789.__version__)
print()

time.sleep(2)

runState = State()
if supervisor.runtime.usb_connected:
    runState.setConnected()
else:
    runState.setNoHost()

# Read the boot configuration data
bootStrm = open("/boot.json")
bootJson = json.load(bootStrm)
bootStrm.close()

print("Boot items: ", len(bootJson["bootSet"]))

# Release any resources currently in use for the displays
displayio.release_displays()

tft_cs = board.GP17
tft_dc = board.GP16
#tft_res = board.GP23
spi_mosi = board.GP19
spi_clk = board.GP18

"""
classbusio.SPI(clock: microcontroller.Pin,
                MOSI: Optional[microcontroller.Pin] = None,
                MISO: Optional[microcontroller.Pin] = None)
"""
spi = busio.SPI(spi_clk, MOSI=spi_mosi)

#display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_res)
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
#I get the parameters by guessing and trying
#display = ST7789(display_bus, width=135, height=240, rowstart=40, colstart=53)
display = adafruit_st7789.ST7789(display_bus,
                    width=135, height=240,
                    rowstart=40, colstart=53)
display.rotation = 0

SxA = defineSwitch(board.GP12)
SxB = defineSwitch(board.GP13)
SxX = defineSwitch(board.GP14)
SxY = defineSwitch(board.GP15)

switches = [SxA, SxB, SxX, SxY]
switchLabels = ["a", "b", "x", "y"]

# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(135, 240, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x00FF00

bg_sprite = displayio.TileGrid(color_bitmap,
                               pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(133, 238, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x0000FF
inner_sprite = displayio.TileGrid(inner_bitmap,
                                  pixel_shader=inner_palette, x=1, y=1)
splash.append(inner_sprite)

# Draw a label
text_group1 = displayio.Group(scale=1, x=20, y=40)
text1 = "Grub Boot"
text_area1 = label.Label(terminalio.FONT, text=text1, color=0x00FF00)
text_group1.append(text_area1)  # Subgroup for text scaling
# Draw a label
text_group2 = displayio.Group(scale=1, x=20, y=60)
text2 = "CircuitPython"
text_area2 = label.Label(terminalio.FONT, text=text2, color=0xFFFFFF)
text_group2.append(text_area2)  # Subgroup for text scaling

# Draw a label
text_group3 = displayio.Group(scale=1, x=20, y=100)
text3 = adafruit_st7789.__name__
text_area3 = label.Label(terminalio.FONT, text=text3, color=0x0000000)
text_group3.append(text_area3)  # Subgroup for text scaling
# Draw a label
text_group4 = displayio.Group(scale=4, x=10, y=160)
text4 = bootJson["bootSet"][bootJson["bootSelect"]]["label"]
text_area4 = label.Label(terminalio.FONT, text=text4, color=0x000000)
text_group4.append(text_area4)  # Subgroup for text scaling

splash.append(text_group1)
splash.append(text_group2)
splash.append(text_group3)
splash.append(text_group4)

while True:
    time.sleep(.01)
    
    for sx in switches:
        sx.update()
        if sx.fell:
            idx = switches.index(sx)
            if switchLabels[idx] == "a":
                bootJson["bootSelect"] = (bootJson["bootSelect"] + 1) % len(bootJson["bootSet"])
                text_area4.text = bootJson["bootSet"][bootJson["bootSelect"]]["label"]

            elif runState.isConnected() and len(bootJson[switchLabels[idx]]) > 0:
                runState.keyboard_layout.write(bootJson[switchLabels[idx]])

    if runState.isConnected():
        text_area1.text = "Host"
        rgbled.color = (0, 16, 0)
        if not supervisor.runtime.usb_connected:
            runState.setNoHost()
        else:
            pass        
    elif runState.isNoHost():
        text_area1.text = "No Host"
        rgbled.color = (16, 0, 0)
        if supervisor.runtime.usb_connected:
            runState.setGrub()
            runState.delay = ticks_add(ticks_ms(), bootJson["grubDelay"])
        else:
            pass
    
    elif runState.isGrub():
        rgbled.color = (0, 0, 16)
        text_area1.text = "GRUB"
        if not ticks_less(ticks_ms(), runState.delay):
            # Step to the top of the GRUB menu in case there is a default OS
            for n in range(bootJson["bootMaxLines"]):
                keyPress(runState, Keycode.UP_ARROW)
            
            # Step to the requested OS and boot
            for n in range(bootJson["bootSet"][bootJson["bootSelect"]]["item"]):
                keyPress(runState, Keycode.DOWN_ARROW)
            keyPress(runState, Keycode.ENTER)
            
            # Wait for GRUB to release the USB
            while supervisor.runtime.usb_connected:
                time.sleep(0.1)
            
            # Wait for selected OS to boot
            while not supervisor.runtime.usb_connected:
                time.sleep(0.1)
            
            runState.setConnected()
            
        else:
            pass
