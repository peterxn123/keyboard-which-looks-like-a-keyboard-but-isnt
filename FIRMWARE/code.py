import board
import digitalio
import time
import storage
import os
import sdcardio
import busio
import audiobusio
import audiocore
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.modules.layers import Layers

# Initialize keyboard
keyboard = KMKKeyboard()

# Add layers module
layers = Layers()
keyboard.modules.append(layers)

# Use only the first 12 pins for KMK (exclude layer buttons)
key_pins = [
    board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5, board.GP6,  # White keys (bottom row)
    board.GP7, board.GP8, board.GP9, board.GP10, board.GP11,  # Black keys (top row)
]

# Setup keyboard matrix with direct pins (excluding layer buttons)
keyboard.matrix = KeysScanner(
    pins=key_pins,
    value_when_pressed=False,
    pull=True,  # Enable pull-up resistors
)

# IMPORTANT: Define comprehensive keymap with multiple layers
keyboard.keymap = [
    # Layer 0: First set of letters (A-G) and common symbols
    [
        KC.A, KC.B, KC.C, KC.D, KC.E, KC.F, KC.G,               # White keys - letters A-G
        KC.EXCLAIM, KC.AT, KC.HASH, KC.DOLLAR, KC.PERCENT,      # Black keys - symbols !@#$%
    ],
    # Layer 1: Second set of letters (H-N) and more symbols
    [
        KC.H, KC.I, KC.J, KC.K, KC.L, KC.M, KC.N,               # White keys - letters H-N
        KC.CIRC, KC.AMPR, KC.ASTR, KC.LPRN, KC.RPRN,            # Black keys - symbols ^&*()
    ],
    # Layer 2: Third set of letters (O-U) and more symbols
    [
        KC.O, KC.P, KC.Q, KC.R, KC.S, KC.T, KC.U,               # White keys - letters O-U
        KC.MINUS, KC.EQUAL, KC.LBRC, KC.RBRC, KC.BSLS,          # Black keys - symbols -=[]\
    ],
    # Layer 3: Fourth set of letters (V-Z) and more symbols
    [
        KC.V, KC.W, KC.X, KC.Y, KC.Z, KC.COMM, KC.DOT,          # White keys - letters V-Z and ,. 
        KC.SCLN, KC.QUOT, KC.SLSH, KC.GRAVE, KC.TILD,           # Black keys - symbols ;'/`~
    ],
    # Layer 4: Numbers and arithmetic operators
    [
        KC.N1, KC.N2, KC.N3, KC.N4, KC.N5, KC.N6, KC.N7,        # White keys - numbers 1-7
        KC.N8, KC.N9, KC.N0, KC.PLUS, KC.ASTERISK,              # Black keys - numbers 8-0 and + *
    ],
    # Layer 5: Function keys
    [
        KC.F1, KC.F2, KC.F3, KC.F4, KC.F5, KC.F6, KC.F7,        # White keys - F1-F7
        KC.F8, KC.F9, KC.F10, KC.F11, KC.F12,                   # Black keys - F8-F12
    ],
    # Layer 6: Navigation and editing
    [
        KC.HOME, KC.END, KC.PGUP, KC.PGDN, KC.INS, KC.DEL, KC.BSPC,  # White keys - nav keys
        KC.TAB, KC.ENTER, KC.ESC, KC.SPACE, KC.CAPS,                 # Black keys - common keys
    ],
    # Layer 7: Arrow keys and modifiers
    [
        KC.LEFT, KC.RIGHT, KC.UP, KC.DOWN, KC.LSFT, KC.LCTL, KC.LALT,  # White keys - arrows & mods
        KC.LGUI, KC.LSFT, KC.LCTL, KC.LALT, KC.LGUI,                   # Black keys - modifiers
    ],
]

# Setup direct GPIO for layer buttons
layer_down_pin = digitalio.DigitalInOut(board.GP12)
layer_down_pin.direction = digitalio.Direction.INPUT
layer_down_pin.pull = digitalio.Pull.UP

layer_up_pin = digitalio.DigitalInOut(board.GP13)
layer_up_pin.direction = digitalio.Direction.INPUT
layer_up_pin.pull = digitalio.Pull.UP

# Start on layer 0
current_layer = 0
keyboard.active_layers = [0]

# For debouncing
layer_up_last_state = True  # Pulled up = True when not pressed
layer_down_last_state = True
last_layer_change = time.monotonic()
DEBOUNCE_DELAY = 0.2  # 200ms debounce delay

# Set up the SD card - using original pin configuration
sd_spi = busio.SPI(board.GP18, MOSI=board.GP19, MISO=board.GP16)
try:
    # Use the original pin configuration
    sdcard = sdcardio.SDCard(sd_spi, board.GP17)
    vfs = storage.VfsFat(sdcard)
    storage.mount(vfs, "/sd")
    print("SD card mounted at /sd")
except Exception as e:
    print(f"Error mounting SD card: {e}")

# Setup the I2S audio output - using original pin configuration
# Enable the amplifier first
amp_enable = digitalio.DigitalInOut(board.GP26)
amp_enable.direction = digitalio.Direction.OUTPUT
amp_enable.value = True

# Create I2S audio output with original pin assignments
try:
    # Using original pin configuration
    audio = audiobusio.I2SOut(bit_clock=board.GP21, word_select=board.GP22, data=board.GP20)
    print("I2S audio initialized")
except Exception as e:
    print(f"Error initializing I2S audio: {e}")
    audio = None

# Function to switch to a specific layer
def switch_to_layer(layer_num):
    global current_layer
    total_layers = len(keyboard.keymap)
    # Ensure the layer is within valid range
    layer_num = layer_num % total_layers
    current_layer = layer_num
    keyboard.active_layers = [layer_num]
    print(f"Switched to layer {layer_num}")

# Function to check and handle layer button presses
def check_layer_buttons():
    global layer_up_last_state, layer_down_last_state, last_layer_change, current_layer
    
    # Get current button states (False = pressed because of pull-up)
    layer_down_current = layer_down_pin.value
    layer_up_current = layer_up_pin.value
    
    # Check for button state changes (with debouncing)
    current_time = time.monotonic()
    
    # Handle layer down button (False = pressed)
    if layer_down_current == False and layer_down_last_state == True:
        # Button just pressed
        if current_time - last_layer_change > DEBOUNCE_DELAY:
            print("Layer down button pressed")
            new_layer = (current_layer - 1) % len(keyboard.keymap)
            switch_to_layer(new_layer)
            last_layer_change = current_time
    
    # Handle layer up button (False = pressed)
    if layer_up_current == False and layer_up_last_state == True:
        # Button just pressed
        if current_time - last_layer_change > DEBOUNCE_DELAY:
            print("Layer up button pressed")
            new_layer = (current_layer + 1) % len(keyboard.keymap)
            switch_to_layer(new_layer)
            last_layer_change = current_time
    
    # Update last states
    layer_down_last_state = layer_down_current
    layer_up_last_state = layer_up_current



# Main loop
while True:
    try:
        # Check for layer button presses directly
        check_layer_buttons()
        
        # Let KMK handle the rest of the keyboard
        keyboard.go()
        
        # Small delay to prevent excessive CPU usage
        time.sleep(0.01)
    except Exception as e:
        print(f"Error in main loop: {e}")
        time.sleep(1)  # Prevent rapid error messages