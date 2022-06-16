# PicoGrubKeyBoard
Pi Pico - CircuitPython Program to act as Keyboard for GRUB boot

A small Python script for Raspberry Pi Pico using CircuitPython and the ```adafruit_hid``` library to provide keyboard input to
the Linux GRUB boot loader. This is uesful in my case because I'm using Logi Mx Keys Bluetooth connected keyboard which is not 
active at that point in the boot sequence.

This version uses a [Pimoroni Pico Display](https://shop.pimoroni.com/products/pico-display-pack?variant=32368664215635) for user interface and control.

## Requirements

* Circuitpython
* Adafruit libraries (.mpy)
  * adafruit_display_text
  * adafruit_hid 
  * adafruit_debouncer
  * adafruit_rgbled
  * adafruit_st7789
  * adafruit_ticks
  * simpleio
  * st7789

## Configuration
Configuration is managed by JSON data stored on the flash drive in ```/boot.json```. Here is a sample:
``` json
{
  "bootSet":
    [
      {"item": 0, "label": "Mate"},
      {"item": 2, "label": "Win10"}
    ],
   "bootSelect": 1
   "grubDelay": 5000
}
```

### ```bootSet```
The boot set is a list of OS entries that exist ind the host computer GRUB configuration that you wish to be able to selct from the Pico UI.
Each item on the list has two values:
* ```item``` - The index of the os in the GRUB configuration, begining at Zero.
* ```label``` - A text label to display on the Pico Display.

### ```bootSelect```
The boot select value is the intital index into ```bootSet``` when the Pico starts up. 

### ```grubDelay```
The number of milliseconds to wait after GRUB has established a USB keyboard connection to the Pico befor sending the keypress data to select boot
specification.
