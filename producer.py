# producer.py
import threading
import random
import time
import xml.etree.ElementTree as ET
from ITstudent import ITstudent
from buffer import SharedBuffer

# Global shared buffer (will be set from main)
shared_buffer = None

def generate_random_student():
    first = ['Andile', 'Thabani', 'Ngcebo', 'Mlungisi', 'Sthembiso', 'Msimisi', 'Sandile', 'Sengeto', 'Langelihle', 'Mphendulo']
    last  = ['Dlamini', 'Tsabedze', 'Mamba', 'Mabuza', 'Mamba', 'Dlamini', 'Dlamini', 'Mavuso', 'Nhlabatsi', 'Zwane']
    name = random.choice(first) + " " + random.choice(last)
    sid = ''.join(random.choices('0123456789', k=8))
    programmes = ['BSc in Computer Science Education', 'BSc in Information Technology', 'BSc in Information Science', 'Bachelor of Science']
    programme = random.choice(programmes)
    all_courses = ['MAT421', 'CSC423', 'CSC411', 'CSC413', 'MAT441', 'CSC400']
    courses = random.sample(all_courses, k=random.randint(4, 6))
    course_marks = [(c, random.randint(0, 100)) for c in courses]

    return ITstudent(name, sid, programme, course_marks)

def producer_thread():
    global shared_buffer
    for _ in range(20):  # Produce more than 10 to force waiting
        time.sleep(random.uniform(0.2, 0.8))

        # Choose a unique file number (1-10) that is not currently in buffer
        used = set(shared_buffer.buffer)
        available = [i for i in range(1, 11) if i not in used]
        if not available:  # Should never happen due to semaphores
            continue
        file_num = random.choice(available)

        student = generate_random_student()

        # Create XML
        root = ET.Element("student")
        ET.SubElement(root, "name").text = student.name
        ET.SubElement(root, "id").text = student.sid
        ET.SubElement(root, "programme").text = student.programme
        courses_elem = ET.SubElement(root, "courses")
        for cname, mark in student.courses:
            course_elem = ET.SubElement(courses_elem, "course")
            ET.SubElement(course_elem, "name").text = cname
            ET.SubElement(course_elem, "mark").text = str(mark)

        tree = ET.ElementTree(root)
        filename = f"student{file_num}.xml"
        tree.write(filename, encoding="utf-8", xml_declaration=True)

        # Put into buffer
        shared_buffer.produce(file_num)

    print("Producer finished.")