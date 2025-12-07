# consumer.py
import threading
import time
import os
import xml.etree.ElementTree as ET
from ITstudent import ITstudent
from buffer import SharedBuffer

shared_buffer = None

def consumer_thread():
    global shared_buffer
    while True:
        try:
            file_num = shared_buffer.consume()
        except:
            break

        filename = f"student{file_num}.xml"
        time.sleep(random.uniform(0.3, 1.0))

        try:
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

            print("\n" + "="*50)
            print(f"CONSUMED: student{file_num}.xml")
            print(student)
            print("="*50 + "\n")

            # Delete the file
            os.remove(filename)
            print(f"Deleted {filename}\n")

        except Exception as e:
            print(f"Error processing {filename}: {e}")

    print("Consumer finished.")