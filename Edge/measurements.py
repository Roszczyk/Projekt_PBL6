import numpy as np

def add_random(rng):
    return np.random.randint(-rng*100000, rng*100000)/100000

def measure_temp():
    meas = 25 + add_random(2)
    return round(meas, 2)

def measure_humidity():
    meas = 30 + add_random(3)
    return round(meas,2)

def measure_gps():
    meas = {
        "latitude" : f"{round(37.7749 + add_random(0.001), 4)}",
        "longitude" : f"{round(-122.4193 + add_random(0.001), 4)}"
    }
    return meas

def random_digital_in(prob):
    if np.random.choice([True, False], p=[prob,1-prob]):
        return np.random.randint(0,100)
    else:
        return None

def measure_digital_ins():
    meas = {
        "digital_in_0" : random_digital_in(0.4),
        "digital_in_1" : random_digital_in(0.3),
        "digital_in_2" : random_digital_in(0.2)
    }
    return meas

