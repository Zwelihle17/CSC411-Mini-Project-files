# consumer_client.py
import socket
import pickle
import time
import os
import xml.etree.ElementTree as ET
from ITstudent import ITstudent

HOST = '127.0.0.1'
PORT = 9999

def consumer():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print("[CONSUMER] Connected to buffer server")

    for _ in range(15):
        time.sleep(random.uniform(1.0, 3.0))

        # Request to consume
        client.sendall(pickle.dumps({"type": "CONSUME"}))
        response = pickle.loads(client.recv(1024))
        file_num = response["file_num"]
        filename = f"student{file_num}.xml"

        if os.path.exists(filename):
            tree = ET.parse(filename)
            root = tree.getroot()

            name = root.find("name").text
            sid = root.find("id").text
            prog = root.find("programme").text
            courses = [(c.find("name").text, int(c.find("mark").text))
                       for c in root.find("courses")]

            student = ITstudent(name, sid, prog, courses)

            print("\n" + "="*60)
            print(f"CONSUMED student{file_num}.xml")
            print(student)
            print("="*60)

            os.remove(filename)
            print(f"Deleted {filename}\n")
        else:
            print(f"File {filename} not found!")

    client.close()
    print("[CONSUMER] Finished")

if __name__ == "__main__":
    consumer()