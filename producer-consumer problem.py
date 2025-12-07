import threading
import random
import xml.etree.ElementTree as ET
import time
import os

class ITstudent:
    def __init__(self, name='', sid='', programme='', courses=None):
        self.name = name
        self.sid = sid
        self.programme = programme
        self.courses = courses if courses else []  # list of tuples (course_name, mark)

# Shared resources
buffer = []
mutex = threading.Semaphore(1)
empty = threading.Semaphore(10)
full = threading.Semaphore(0)

def generate_random_student():
    first_names = ['Andile', 'Thabani', 'Ngcebo', 'Mlungisi', 'Sthembiso', 'Msimisi', 'Sandile', 'Sengeto', 'Langelihle', 'Mphendulo']
    last_names = ['Dlamini', 'Tsabedze', 'Mamba', 'Mabuza', 'Mamba', 'Dlamini', 'Dlamini', 'Mavuso', 'Nhlabatsi', 'Zwane']
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    sid = ''.join(str(random.randint(0, 9)) for _ in range(8))
    programmes = ['BSc in Computer Science Education', 'BSc in Information Technology', 'BSc in Information Science', 'Bachelor of Science']
    programme = random.choice(programmes)
    course_list = ['MAT421', 'CSC423', 'CSC411', 'CSC433', 'CSC413', 'CSC401', 'MAT441', 'CSC400']
    num_courses = random.randint(3, 6)
    courses = [(random.choice(course_list), random.randint(0, 100)) for _ in range(num_courses)]
    return ITstudent(name, sid, programme, courses)

def producer():
    for _ in range(15):  # Produce 15 students to demonstrate buffering
        time.sleep(random.uniform(0.1, 0.5))  # Simulate production time
        empty.acquire()
        mutex.acquire()
        available = set(range(1, 11)) - set(buffer)
        num = random.choice(list(available))
        student = generate_random_student()
        # Wrap into XML
        root = ET.Element('student')
        ET.SubElement(root, 'name').text = student.name
        ET.SubElement(root, 'id').text = student.sid
        ET.SubElement(root, 'programme').text = student.programme
        courses_elem = ET.SubElement(root, 'courses')
        for course_name, mark in student.courses:
            course_elem = ET.SubElement(courses_elem, 'course')
            ET.SubElement(course_elem, 'name').text = course_name
            ET.SubElement(course_elem, 'mark').text = str(mark)
        xml_data = ET.tostring(root, encoding='unicode')
        filename = f'student{num}.xml'
        with open(filename, 'w') as f:
            f.write(xml_data)
        buffer.append(num)
        print(f"Producer: Produced {filename} (buffer size: {len(buffer)})")
        mutex.release()
        full.release()

def consumer():
    for _ in range(15):  # Consume 15 students
        full.acquire()
        mutex.acquire()
        num = buffer.pop(0)
        filename = f'student{num}.xml'
        with open(filename, 'r') as f:
            xml_data = f.read()
        # Unwrap XML
        root = ET.fromstring(xml_data)
        name = root.find('name').text
        sid = root.find('id').text
        programme = root.find('programme').text
        courses = [(e.find('name').text, int(e.find('mark').text)) for e in root.find('courses')]
        student = ITstudent(name, sid, programme, courses)
        # Calculate average and pass/fail
        marks = [mark for _, mark in student.courses]
        average = sum(marks) / len(marks) if marks else 0
        result = 'Pass' if average >= 50 else 'Fail'
        # Print information
        print("\nConsumer: Consumed student information")
        print(f"Student Name: {student.name}")
        print(f"Student ID: {student.sid}")
        print(f"Programme: {student.programme}")
        print("Courses and Marks:")
        for course_name, mark in student.courses:
            print(f"  {course_name}: {mark}")
        print(f"Average: {average:.2f}")
        print(f"Result: {result}")
        # Delete the file
        os.remove(filename)
        print(f"Consumer: Deleted {filename} (buffer size: {len(buffer)})\n")
        mutex.release()
        empty.release()
        time.sleep(random.uniform(0.1, 0.5))  # Simulate consumption time

# Clean up existing files before starting
for i in range(1, 11):
    filename = f'student{i}.xml'
    if os.path.exists(filename):
        os.remove(filename)

# Start threads
producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)
producer_thread.start()
consumer_thread.start()
producer_thread.join()
consumer_thread.join()

print("Producer-Consumer completed.")