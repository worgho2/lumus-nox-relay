from machine import Pin, I2S
import speech_model
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
SWITCH_ON_PIN = 18
SWITCH_OFF_PIN = 19

### RELAY ###
RELAY_PIN = 27

### STATES ###
ALWAYS_ON = 'ALWAYS_ON'
ALWAYS_OFF = 'ALWAYS_OFF'
AUTO = 'AUTO'
ON = 'ON'
OFF = 'OFF'

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


switch_off_pin.irq(
    trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING,
    handler=switch_handler
)
switch_on_pin.irq(
    trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING,
    handler=switch_handler
)


def mic_handler():
    global mic, mic_samples

    mic.readinto(mic_samples)
    label, prob = speech_model.predict(mic_samples)
    gc.collect()
    mic_samples = bytearray(7168)

    if label == '[OTHER]' or prob < 75:
        return
    elif label == 'lumus':
        if DEBUG:
            print("DEBUG: Lumus:", prob, "%")

        set_state(ON)
    elif label == 'nox':
        if DEBUG:
            print("DEBUG: Nox:", prob, "%")

        set_state(OFF)

    speech_model.snapshot()


mic_samples = bytearray(7168)
gc.collect()

while True:
    if state == ALWAYS_ON or state == ON:
        relay.off()  # Inverted due relay schematic
    elif state == ALWAYS_OFF or state == OFF:
        relay.on()  # Inverted due relay schematic

    if state == AUTO or state == ON or state == OFF:
        mic_handler()
