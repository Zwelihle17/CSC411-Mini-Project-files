# producer_client.py
import socket
import pickle
import random
import time
import xml.etree.ElementTree as ET
from ITstudent import ITstudent

HOST = '127.0.0.1'
PORT = 9999

def generate_student():
    names = ['Andile', 'Thabani', 'Ngcebo', 'Mlungisi', 'Sthembiso', 'Msimisi', 'Sandile', 'Sengeto', 'Langelihle', 'Mphendulo']
    sid = ''.join(random.choices('0123456789', k=8))
    prog = random.choice(['BSc in Computer Science Education', 'BSc in Information Technology', 'BSc in Information Science', 'Bachelor of Science'])
    courses = [('MAT421', random.randint(30,95)), ('CSC423', random.randint(40,98)),
               ('CSC411', random.randint(35,99)), ('CSC413', random.randint(20,100)), ('MAT441', random.randint(15,92)), ('CSC400', random.randint(10,90))]
    return ITstudent(random.choice(names), sid, prog, courses)

def producer():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print("[PRODUCER] Connected to buffer server")

    used_files = set()

    for i in range(15):
        time.sleep(random.uniform(0.5, 2.0))

        # Find available file slot (1-10)
        available = [n for n in range(1, 11) if n not in used_files]
        if not available:
            print("  [PRODUCER] Waiting for free slot...")
            time.sleep(2)
            continue

        file_num = random.choice(available)
        student = generate_student()

        # Generate XML
        root = ET.Element("student")
        ET.SubElement(root, "name").text = student.name
        ET.SubElement(root, "id").text = student.sid
        ET.SubElement(root, "programme").text = student.programme
        courses_el = ET.SubElement(root, "courses")
        for c, m in student.courses:
            ce = ET.SubElement(courses_el, "course")
            ET.SubElement(ce, "name").text = c
            ET.SubElement(ce, "mark").text = str(m)

        ET.ElementTree(root).write(f"student{file_num}.xml", encoding="utf-8", xml_declaration=True)

        # Send to server
        request = {"type": "PRODUCE", "file_num": file_num}
        client.sendall(pickle.dumps(request))
        response = pickle.loads(client.recv(1024))
        if response["status"] == "OK":
            used_files.add(file_num)
            print(f"  [PRODUCER] → Produced student{file_num}.xml")

    client.close()
    print("[PRODUCER] Finished")

if __name__ == "__main__":
    producer()