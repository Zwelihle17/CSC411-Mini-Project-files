# ITstudent.py
class ITstudent:
    def __init__(self, name="", sid="", programme="", courses=None):
        self.name = name
        self.sid = sid
        self.programme = programme
        self.courses = courses or []  # list of (course_name, mark)

    def calculate_average(self):
        if not self.courses:
            return 0.0
        marks = [mark for _, mark in self.courses]
        return sum(marks) / len(marks)

    def get_result(self):
        return "Pass" if self.calculate_average() >= 50 else "Fail"

    def __str__(self):
        course_str = "\n".join([f"    {c}: {m}" for c, m in self.courses])
        return (f"Name: {self.name}\n"
                f"ID: {self.sid}\n"
                f"Programme: {self.programme}\n"
                f"Courses & Marks:\n{course_str}\n"
                f"Average: {self.calculate_average():.2f}\n"
                f"Result: {self.get_result()}")