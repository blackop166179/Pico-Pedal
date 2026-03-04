import math
import random
#import RPi.GPIO as GPIO

import time

def run_loop(rate_hz, duration_sec):
    """
    Run a loop at a given rate (Hz) for a specific duration (seconds).
    """
    if rate_hz <= 0 or duration_sec <= 0:
        raise ValueError("Rate and duration must be positive numbers.")

    interval = 1.0 / rate_hz  # Time between iterations
    start_time = time.time()
    next_time = start_time

    iteration = 0
    while time.time() - start_time < duration_sec:
        iteration += 1
        current_time = time.time()

        # ---- Your task here ----
        ticks()
        # ------------------------

        # Schedule next iteration
        next_time += interval
        sleep_time = next_time - time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)  # Sleep to maintain rate
        else:
            # If we're behind schedule, skip sleeping
            next_time = time.time()


def ticks():
    Lambda = 20
    tic = -math.log(1.0 - random.random()) / Lambda
    if tic == 0: 
        print("go")
run_loop(rate_hz=96000, duration_sec=1)
    