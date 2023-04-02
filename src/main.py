from machine import Pin, I2S
import speech_model
import time
import gc

########## CONFIGURATION ##########

### DEBUG ###
DEBUG = True

### MIC ###
MIC_SD_PIN = 33
MIC_SCK_PIN = 32
MIC_WS_PIN = 25
MIC_MODE = I2S.MASTER_RX
MIC_DATA_FORMAT = I2S.B16
MIC_CHANNEL_FORMAT = I2S.ONLY_LEFT
MIC_SAMPLE_RATE = 16000
MIC_DMA_COUNT = 16
MIC_DMA_LEN = 256

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
    I2S.NUM0, sdin=Pin(MIC_SD_PIN), bck=Pin(MIC_SCK_PIN), ws=Pin(MIC_WS_PIN),
    mode=MIC_MODE, dataformat=MIC_DATA_FORMAT, channelformat=MIC_CHANNEL_FORMAT,
    samplerate=MIC_SAMPLE_RATE, dmacount=MIC_DMA_COUNT, dmalen=MIC_DMA_LEN
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
            print("DEBUG: label: ", label)
            print("DEBUG: prob: ", prob)

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
# mic.irq(mic_handler)
mic.readinto(mic_samples)

while True:

    mic.readinto(mic_samples)
    l, prob = speech_model.predict(mic_samples)
    gc.collect()
    if l == '[OTHER]' or prob <= 70:
        continue
    label = l
    speech_model.snapshot()
    if label == 'lumus':  # Replace with your own label.
        print('LUMUS', prob)
        relay.on()
    elif label == 'nox':  # Replace with your own label.
        print("NOX", prob)
        relay.off()
    # if state == ALWAYS_ON or state == ON:
    #     relay.on()
    # elif state == ALWAYS_OFF or state == OFF:
    #     relay.off()
    # elif state != AUTO:
    #     print("ERROR: Unknown state:", state)

    # mic_handler(None)
    # time.sleep(0.1)
