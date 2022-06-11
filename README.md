# PicoGrubKeyBoard
Pi Pico - CircuitPython Program to act as Keyboard for GRUB boot

A small Python script for Raspberry Pi Pico using CircuitPython and the ```adafruit_hid``` library to provide keyboard input to
the Linux GRUB boot loader. This is uesful in my case because I'm using Logi Mx Keys Bluetooth connected keyboard which is not 
active at that point in the boot sequence.

## Simple Implementation

This branch contains the code needed for a simple implementation consisiting of the Raspberry Pi Pico only. Selection of which
OS to bood is done through editing of the ```boot.json``` file on the Pico storage mounted on a currently running OS.
