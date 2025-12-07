# main.py
import threading
from buffer import SharedBuffer
from producer import producer_thread, shared_buffer as prod_buffer
from consumer import consumer_thread, shared_buffer as cons_buffer

# Clean old XML files
import os
for i in range(1, 11):
    f = f"student{i}.xml"
    if os.path.exists(f):
        os.remove(f)

# Create shared buffer
buffer = SharedBuffer(capacity=10)

# Inject buffer into producer & consumer modules
prod_buffer = buffer
cons_buffer = buffer

# Start threads
producer = threading.Thread(target=producer_thread, daemon=True)
consumer = threading.Thread(target=consumer_thread, daemon=True)

print("Starting Producer-Consumer Simulation...\n")
producer.start()
consumer.start()

# Let them run
producer.join()
consumer.join(timeout=2)  # Give consumer time to finish remaining items

print("Completed.")