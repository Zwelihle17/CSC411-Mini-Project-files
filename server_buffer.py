# server_buffer.py
import socket
import threading
import pickle

HOST = '127.0.0.1'
PORT = 9999

class SocketBuffer:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.buffer = []
        self.mutex = threading.Semaphore(1)
        self.empty = threading.Semaphore(capacity)
        self.full = threading.Semaphore(0)
        self.lock = threading.Lock()

    def produce(self, item):
        self.empty.acquire()
        with self.mutex:
            self.buffer.append(item)
            print(f"[BUFFER] Produced {item} → Buffer: {self.buffer}")
        self.full.release()

    def consume(self):
        self.full.acquire()
        with self.mutex:
            item = self.buffer.pop(0)
            print(f"[BUFFER] Consumed {item} → Buffer: {self.buffer}")
        self.empty.release()
        return item

buffer = SocketBuffer()

def handle_client(conn, addr):
    print(f"[SERVER] Connected by {addr}")
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            request = pickle.loads(data)

            if request["type"] == "PRODUCE":
                buffer.produce(request["file_num"])
                conn.sendall(pickle.dumps({"status": "OK"}))

            elif request["type"] == "CONSUME":
                file_num = buffer.consume()
                conn.sendall(pickle.dumps({"file_num": file_num}))

        except Exception as e:
            print(f"Client {addr} disconnected or error: {e}")
            break
    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[SERVER] Buffer server running on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    print("Starting Socket-Based Producer-Consumer Buffer Server...")
    start_server()