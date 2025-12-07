# buffer.py
import threading

class SharedBuffer:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.buffer = []                    # holds integers 1–10 (file numbers)
        self.mutex = threading.Semaphore(1)
        self.empty = threading.Semaphore(capacity)
        self.full = threading.Semaphore(0)

    def produce(self, file_number):
        self.empty.acquire()       # Wait if buffer is full
        self.mutex.acquire()       # Mutual exclusion
        self.buffer.append(file_number)
        print(f"Producer: Added file #{file_number} | Buffer: {self.buffer}")
        self.mutex.release()
        self.full.release()        # Signal consumer

    def consume(self):
        self.full.acquire()        # Wait if buffer is empty
        self.mutex.acquire()
        file_number = self.buffer.pop(0)
        print(f"Consumer: Removed file #{file_number} | Buffer: {self.buffer}")
        self.mutex.release()
        self.empty.release()       # Signal producer
        return file_number