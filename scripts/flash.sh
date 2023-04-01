#!/bin/bash

PORT=/dev/tty.usbserial-0001

esptool.py --chip esp32 --port $PORT --baud 460800 write_flash -z 0x1000 ../firmwares/speech-commands-firmware.bin
