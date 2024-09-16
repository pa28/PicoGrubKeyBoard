# PicoGrubKeyBoard
Pi Pico - CircuitPython Program to act as Keyboard for GRUB boot.
[Adapted from Hello Raspberry Pi](http://helloraspberrypi.blogspot.com/2021/01/raspberry-pi-picocircuitpython-st7789.html)

A small Python script for Raspberry Pi Pico using CircuitPython and the ```adafruit_hid``` library
to provide keyboard input to the Linux GRUB bootloader. This is useful in my case because I'm using
Logi Mx Keys Bluetooth connected keyboard which is not active at that point in the boot sequence.

### Hardware
* Pi Pico
* Pimoroni picodisplay
  * A small display board that mounts to a Pi Pico
  * Four buttons: A, B, X, Y
    * A is used to select the OS to boot.
    * B, X and Y can be programed with "hardcoded" text in boot.json
    * Pressing the X button while the Pico is in GRUB mode will switch it to host mode. 
  * One RGB LED
    * Solid Read: Not connected to the machne. No USB keyboard service active.
    * Solid Blue: GRUB connected. Wait period before sending keybord codes to boot the sekected OS.
    * Flashing Blue: Boot key sequence sent, waiting for GRUB to disconnect.
    * Flashing Green: GRUB disconnected, waiting booted host OS to connect.
    * Solid Green: Connected to the host OS.
    * Flashing Yellow: Error.

### Persistence

This version supports persistence of the selected boot image. This requires installing the included
```boot.py``` file which makes the storage __READ ONLY__ via the USB interface. This can be
disabled using a _REPL_ connection such as that provided by the [Mu editor](https://codewith.mu/) and
entering the following commands:
```python
import os
os.listdir("/")
os.rename("/boot.py","/boot.bak")
```

### Required Libraries
* adafruit_display_text
* adafruit_hid
* adafruit_debouncer.mpy
* adafruit_rgbled.mpy
* adafruit_st7789.mpy
* adafruit_ticks.mpy
* simpleio.mpy
