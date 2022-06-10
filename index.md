# Pico GRUB Keyboard

Provides for automated selection of boot OS during GRUB boot. Using the ```adafruit_hid``` library the Pico monitors USB connections from the host
to determine the progress through the boot process to emulate OS selection. The OS to boot is indicated by an index into the GRUB configuration
stored in a JSON file on the Pico.
