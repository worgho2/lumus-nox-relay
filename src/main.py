from machine import Pin, I2S
import speech_model
import time
import gc

########## CONFIGURATION ##########

### DEBUG ###
DEBUG = False

### MIC ###
MIC_SD_PIN = 33
MIC_SCK_PIN = 32
MIC_WS_PIN = 25
MIC_MODE = I2S.RX
MIC_BITS = 16
MIC_FORMAT = I2S.MONO
MIC_RATE = 16000
MIC_IBUF = 7168

### SWITCHES ###
SWITCH_ON_PIN = 16
SWITCH_OFF_PIN = 17

### RELAY ###
RELAY_PIN = 27

### STATES ###
ALWAYS_ON = 0
ALWAYS_OFF = 1
AUTO = 2
ON = 3
OFF = 4

###################################

mic = I2S(
    0, sck=Pin(MIC_SCK_PIN), ws=Pin(MIC_WS_PIN), sd=Pin(MIC_SD_PIN),
    mode=MIC_MODE, bits=MIC_BITS, format=MIC_FORMAT, rate=MIC_RATE, ibuf=MIC_IBUF,
)

switch_on_pin = Pin(SWITCH_ON_PIN, Pin.IN)
switch_off_pin = Pin(SWITCH_OFF_PIN, Pin.IN)
relay = Pin(RELAY_PIN, Pin.OUT)

if DEBUG:
    print("")
    print("DEBUG: ON Switch: ", switch_on_pin.value())
    print("DEBUG: OFF Switch: ", switch_off_pin.value())
    print("DEBUG: Relay: ", relay.value())
    print("")

state = AUTO

if switch_on_pin.value() == 1:
    state = ALWAYS_ON
elif switch_off_pin.value() == 1:
    state = ALWAYS_OFF


def set_state(new_state):
    global state

    if DEBUG:
        print("DEBUG: State changed from ", state, " to ", new_state)

    state = new_state


def switch_handler(pin):
    global switch_on_pin, switch_off_pin

    if switch_on_pin.value() == 1:
        set_state(ALWAYS_ON)
    elif switch_off_pin.value() == 1:
        set_state(ALWAYS_OFF)
    else:
        set_state(AUTO)


def mic_handler(pin):
    global state, mic, mic_samples

    if DEBUG:
        print("DEBUG: mic_handler")

    if state == AUTO or state == ON or state == OFF:
        label, prob = speech_model.predict(mic_samples)

        if DEBUG:
            print(f"DEBUG: label: {label}, prob: {prob}")

        if label == '[OTHER]' or prob < 60:
            return
        elif label == 'lumus':
            set_state(ON)
        elif label == 'nox':
            set_state(OFF)
        else:
            print("ERROR: Unknown label: ", label)

    mic.readinto(mic_samples)


switch_off_pin.irq(
    trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING,
    handler=switch_handler
)
switch_on_pin.irq(
    trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING,
    handler=switch_handler
)

mic_samples = bytearray(7168)
mic.irq(mic_handler)
mic.readinto(mic_samples)

while True:
    if state == ALWAYS_ON or state == ON:
        relay.on()
    elif state == ALWAYS_OFF or state == OFF:
        relay.off()
    elif state != AUTO:
        print("ERROR: Unknown state:", state)

    time.sleep(0.1)
