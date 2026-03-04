"""Simple guitar effect processing in Python.

This script demonstrates basic algorithms for distortion and delay. You
can run it offline on a WAV file, or, if you install sounddevice, you can
hook it up to your soundcard for real-time processing (with higher
latency).

Usage (offline):
    python guitar_effects.py --in input.wav --out output.wav

Usage (realtime with sounddevice):
    python guitar_effects.py --realtime

Requirements:
    pip install numpy scipy soundfile sounddevice

Feel free to modify the parameters to hear different tones.
"""

import argparse
import numpy as np


def distort(x, gain=1.0, threshold=0.5):
    """Apply a simple hard-clipping distortion.

    * Multiply by `gain` first
    * Clip to [-threshold, threshold]
    * Optionally scale back to -1..1 range
    """
    y = x * gain
    y = np.clip(y, -threshold, threshold)
    # normalize so maximum absolute value is 1
    maxval = np.max(np.abs(y))
    if maxval > 0:
        y = y / maxval
    return y


def delay(signal, fs, delay_s=0.2, feedback=0.5, mix=0.5):
    """Simple single-tap delay implemented offline.

    Args:
        signal: numpy array, mono
        fs: sample rate
        delay_s: delay time in seconds
        feedback: amount of delayed signal fed back [0,1)
        mix: dry/wet mix [0,1]
    """
    n = len(signal)
    delay_samples = int(delay_s * fs)
    out = np.zeros(n + delay_samples)
    out[:n] += signal  # dry
    for i in range(n):
        out[i + delay_samples] += signal[i] * mix
        # feedback path builds up
        if i + delay_samples < len(out):
            out[i + delay_samples] += out[i] * feedback
    # trim to original length
    return out[:n]


# ---------------------------------------------------------------------------
# helpers for I/O -----------------------------------------------------------------


def process_offline(infile, outfile):
    import soundfile as sf

    data, fs = sf.read(infile, dtype="float32")
    # if stereo, take one channel
    if data.ndim > 1:
        data = data[:, 0]

    print(f"read {len(data)} samples at {fs} Hz")

    # apply effects chain
    y = distort(data, gain=5, threshold=0.3)
    y = delay(y, fs, delay_s=0.25, feedback=0.4, mix=0.3)

    sf.write(outfile, y, fs)
    print(f"wrote processed file to {outfile}")


# ---------------------------------------------------------------------------
# realtime sketch ------------------------------------------------------------------

def realtime_process():
    import sounddevice as sd

    fs = 44100
    # a very small buffer size increases CPU usage but reduces latency
    blocksize = 256

    # create a simple delay buffer
    max_delay_s = 1.0
    max_delay_samples = int(fs * max_delay_s)
    delay_buffer = np.zeros(max_delay_samples)
    write_idx = 0

    def callback(indata, outdata, frames, time, status):
        nonlocal write_idx
        if status:
            print(status)
        # work on the first channel
        x = indata[:, 0]
        y = np.zeros_like(x)
        for i in range(frames):
            # distortion first
            d = np.tanh(3.0 * x[i])  # soft clipping example
            # read delayed sample
            read_idx = (write_idx - int(0.25 * fs)) % max_delay_samples
            delayed = delay_buffer[read_idx]
            # mix
            y[i] = d * 0.7 + delayed * 0.3
            # write new sample with feedback
            delay_buffer[write_idx] = d + delayed * 0.4
            write_idx = (write_idx + 1) % max_delay_samples
        outdata[:, 0] = y
        outdata[:, 1] = y  # copy to stereo

    with sd.Stream(channels=2, callback=callback, samplerate=fs, blocksize=blocksize):
        print("Realtime processing started, press Ctrl+C to stop")
        try:
            while True:
                sd.sleep(1000)
        except KeyboardInterrupt:
            print("stopped")


# ---------------------------------------------------------------------------
# command line interface -------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description="Guitar effect demo")
    parser.add_argument("--in", dest="infile", help="input WAV file")
    parser.add_argument("--out", dest="outfile", help="output WAV file")
    parser.add_argument("--realtime", action="store_true", help="use realtime I/O")
    args = parser.parse_args()

    if args.realtime:
        realtime_process()
    elif args.infile and args.outfile:
        process_offline(args.infile, args.outfile)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
