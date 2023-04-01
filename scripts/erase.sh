#!/bin/bash

PORT=/dev/tty.usbserial-0001

esptool.py --chip esp32 --port $PORT erase_flash
