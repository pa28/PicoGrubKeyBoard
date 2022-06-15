import time
import json
import usb_hid
import supervisor
from adafruit_hid.mouse import Mouse
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
import board
import digitalio

def keyPress(keyCode):
    led.value = True

    keyboard.press(keyCode)
    keyboard.release_all()
    
    time.sleep(.05)
    led.value = False
    time.sleep(.05)
    
led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT

while True:
    # Read the boot configuration data
    bootStrm = open("/boot.json")
    bootJson = json.load(bootStrm)
    bootStrm.close()
    bootConnected = supervisor.runtime.usb_connected
    
    # Test for USB connection to PICO
    if not bootConnected:
        # Wait for the host to connect to the pico USB
        # Flash LED 4 times per second.
        while not supervisor.runtime.usb_connected:
            led.value = True
            time.sleep(0.125)
            led.value = False
            time.sleep(0.125)
    
    #Configure HID devices
    mouse = Mouse(usb_hid.devices)
    keyboard = Keyboard(usb_hid.devices)
    keyboard_layout = KeyboardLayoutUS(keyboard)  # We're in the US :)

    # If PICO booted not connected run GRUB interaction
    if not bootConnected:
        led.value = True
        time.sleep(5)
        led.value = False
        time.sleep(1)
        
        # Move to the top to undo GRUB default
        for n in range(10):
            keyPress(Keycode.UP_ARROW)

        # Select OS to boot
        for n in range(bootJson["bootSet"][bootJson["bootSelect"]]["item"]):
            keyPress(Keycode.DOWN_ARROW)
        keyPress(Keycode.ENTER)

        # Wait for GRUB to release the USB
        while supervisor.runtime.usb_connected:
            time.sleep(0.1)
        
        # Wait for selected OS to boot
        while not supervisor.runtime.usb_connected:
            time.sleep(0.1)
    
    # Post boot action loop.
    while supervisor.runtime.usb_connected:
        # For now just wait for USB disconnect.
        led.value = True
        time.sleep(1)
        led.value = False
        time.sleep(1)
