Youtube demo: https://youtube.com/shorts/1oemrpsrQag?si=syYRnnjexHgY6y_N

We have built an innovative, groundbreaking keyboard that looks like a keyboard but is actually a keyboard and not a keyboard.

![1000067192](https://github.com/user-attachments/assets/458848ef-0a0e-447b-a98f-394459a75e68)


**About**

We always thought traditional keyboards are too boring. We also thought it was funny how electronic pianos and the tools we use to type share a name. So we decided to cross these two, and create this ultimate design! You can only type a choice of 7 letters at a time, as our keyboard only has one octave. Can you make do with only the keys provided to you by the original keyboard - the piano?

**Bill of Materials**

- 1x Orpheus Pico or other RP2040 microcontroller with the same pinout
- 14x Cherry MX style keyswitches
- At least 2m of wire, to connect all components together
- 3d printed keycaps:
    - 2x leftwhitekey.stl
    - 2x rightwhitekey.stl
    - 3x smallwhitekey.stl
    - 5x blackkey.stl
- 2x Regular XDA Cherry MX keycaps - for the octave switching switches
- Cardboard and tools, like hot glue, to create case out of cardboard
- 1x 40mm 8 ohm 2 watt speaker
- 1x MAX98357A speaker amplifier
- 1x Micro SD card reader module

The firmware was built using kmk and CircuitPython, with audiobusio and audiocore for the playback of WAVs on the connected speaker.

Wiring:

                 ┌────────────────────────────────────────────────┐
                 │                Raspberry Pi Pico                │
                 │                                                │
                 │ GP0  ──┐ C key                                 │
                 │ GP1  ──┤ D key                                 │
                 │ GP2  ──┤ E key                                 │
                 │ GP3  ──┤ F key                                 │
                 │ GP4  ──┤ G key                                 │
                 │ GP5  ──┤ A key                                 │
                 │ GP6  ──┤ B key                                 │
                 │ GP7  ──┤ Db key                                │
                 │ GP8  ──┤ Eb key                                │
                 │ GP9  ──┤ Gb key                                │
                 │ GP10 ──┤ Ab key                                │
                 │ GP11 ──┤ Bb key                                │
                 │ GP12 ──┤ Octave Down button                    │
                 │ GP13 ──┤ Octave Up button                      │
                 │                                                │
                 │ GP20 ──► I2S DIN  (MAX98357A)                  │
                 │ GP21 ──► I2S BCLK (MAX98357A)                  │
                 │ GP22 ──► I2S LRC  (MAX98357A)                  │
                 │ GP26 ──► AMP SD (enable HIGH)                  │
                 │ 3V3  ──► AMP VIN, AMP GAIN (for max vol)       │
                 │ GND  ──┴─► AMP GND                              │
                 │                                                │
                 │ GP16 ◄── SD MISO                               │
                 │ GP17 ─── SD CS                                 │
                 │ GP18 ─── SD SCK                                │
                 │ GP19 ─── SD MOSI                               │
                 │ 3V3  ─── SD VCC                                │
                 │ GND  ─── SD GND                                │
                 └────────────────────────────────────────────────┘

 All key switch *other legs* (GND legs on the cherry MX switches) → shared GND rail → Pico GND.


**Please note, the WAVs of piano notes provided are converted from MP3s available on a repository here on GitHub. In respect to the original license, this project has been shared with an MIT license as well. You can find the original repository here: https://github.com/fuhton/piano-mp3**







