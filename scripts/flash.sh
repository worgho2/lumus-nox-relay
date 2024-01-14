#!/bin/bash

PORT=/dev/tty.usbserial-0001

# esptool.py --chip esp32 --port $PORT --baud 460800 write_flash -z 0x1000 ../firmwares/speech-commands-firmware.bin


esptool.py --chip auto --port $PORT --baud 115200 --before default_reset --after hard_reset write_flash -z --flash_mode dio --flash_freq 40m --flash_size 4MB 0x0 ../firmwares/ESP32-WROOM-32-V3.2.0.0/factory/factory_WROOM-32.bin