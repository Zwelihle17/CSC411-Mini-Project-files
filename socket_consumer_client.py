# consumer_client.py
import socket
import pickle
import time
import os
import random          # <-- THIS WAS MISSING
import xml.etree.ElementTree as ET
from ITstudent import ITstudent

HOST = '127.0.0.1'
PORT = 9999

def consumer():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
        print("[CONSUMER] Connected to buffer server")
    except Exception as e:
        print(f"[CONSUMER] Could not connect to server: {e}")
        return

    consumed_count = 0
    while consumed_count < 20:   # Try to consume 20 items (adjust as needed)
        # Random delay to simulate real processing time
        time.sleep(random.uniform(0.8, 2.5))

        try:
            # Request one file number from the buffer server
            client.sendall(pickle.dumps({"type": "CONSUME"}))

            # Receive response (timeout to avoid hanging forever)
            client.settimeout(5.0)
            data = client.recv(4096)
            client.settimeout(None)

            if not data:
                print("[CONSUMER] Server closed connection")
                break

            response = pickle.loads(data)
            file_num = response["file_num"]
            filename = f"student{file_num}.xml"

            print(f"[CONSUMER] Received file number: {file_num}")

            if os.path.exists(filename):
                # Parse XML
                tree = ET.parse(filename)
                root = tree.getroot()

                name = root.find("name").text
                sid = root.find("id").text
                programme = root.find("programme").text
                courses = []
                for c in root.find("courses"):
                    cname = c.find("name").text
                    mark = int(c.find("mark").text)
                    courses.append((cname, mark))

                student = ITstudent(name, sid, programme, courses)

                print("\n" + "="*60)
                print(f"CONSUMED student{file_num}.xml")
                print(student)
                print("="*60 + "\n")

                # Delete the file after processing
                os.remove(filename)
                print(f"Deleted {filename}\n")
            else:
                print(f"Warning: {filename} not found on disk!")

            consumed_count += 1

        except socket.timeout:
            print("[CONSUMER] Timeout waiting for server response")
            break
        except Exception as e:
            print(f"[CONSUMER] Error during consumption: {e}")
            break

    client.close()
    print("[CONSUMER] Finished and disconnected.")

if __name__ == "__main__":
    consumer()
