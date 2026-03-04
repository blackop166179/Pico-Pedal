# Pico-Pedal

This repository is a starting point for building audio effects for guitar signals. It contains a simple Python demo script and space for future C++ code (the `Radioactive_Guitar.cpp` file is currently empty).

## Python Demo

A Python example (`guitar_effects.py`) shows how to implement basic effects such as distortion and delay. It can operate offline on WAV files or, if you install `sounddevice`, in real time using your audio interface.

**Usage (offline processing):**

```bash
python guitar_effects.py --in input.wav --out output.wav
```

**Usage (realtime):**

```bash
python guitar_effects.py --realtime
```

Install requirements with:

```bash
pip install numpy scipy soundfile sounddevice
```

Feel free to modify the script to experiment with different effects and parameters.

this is the code that will run the raspberry pi pico guitar pedal.
