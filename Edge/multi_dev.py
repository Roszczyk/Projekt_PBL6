from main import run
import sys
from threading import Thread
from time import sleep

amount_of_devices = int(sys.argv[1])
threads = []

for i in range(amount_of_devices):
    threads.append(Thread(target=run, args=(f"{i}",), daemon=True))

print(f"Running {amount_of_devices} devices")

for thread in threads:
    thread.start()
    sleep(1)

for thread in threads:
    thread.join()