# PicoGrubKeyBoard
Pi Pico - CircuitPython Program to act as Keyboard for GRUB boot

A small Python script for Raspberry Pi Pico using CircuitPython and the ```adafruit_hid``` library
to provide keyboard input to the Linux GRUB bootloader. This is useful in my case because I'm using
Logi Mx Keys Bluetooth connected keyboard which is not active at that point in the boot sequence.

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
