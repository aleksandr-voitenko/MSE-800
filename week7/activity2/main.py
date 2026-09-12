"""a simple university system.

Hierarchical inheritance: Student and Lecturer inherit from Person.
Multilevel inheritance: PostgraduateStudent inherits from Student and Person.
See class_diagram.drawio for the class diagram.
"""


class Person:
    def __init__(self, name):
        self.name = name

    def display_details(self):
        print(f"Name: {self.name}")


class Student(Person):
    def __init__(self, name, student_id, course):
        super().__init__(name)
        self.student_id = student_id
        self.course = course

    def display_details(self):
        super().display_details()
        print(f"Student ID: {self.student_id}")
        print(f"Course: {self.course}")

    def study(self):
        print(f"{self.name} is studying {self.course}.")


class Lecturer(Person):
    def __init__(self, name, subject):
        super().__init__(name)
        self.subject = subject

    def display_details(self):
        super().display_details()
        print(f"Subject: {self.subject}")

    def teach(self):
        print(f"{self.name} is teaching {self.subject}.")


class PostgraduateStudent(Student):
    def __init__(self, name, student_id, course, thesis_topic):
        super().__init__(name, student_id, course)
        self.thesis_topic = thesis_topic

    def display_details(self):
        super().display_details()
        print(f"Thesis topic: {self.thesis_topic}")

    def research(self):
        print(f"{self.name} is researching {self.thesis_topic}.")


def main():
    person = Person("Alex Smith")
    student = Student("Emma Wilson", "S1001", "Software Engineering")
    lecturer = Lecturer("Dr James Brown", "Python Programming")
    postgraduate = PostgraduateStudent(
        "Olivia Chen", "S2001", "Software Engineering", "AI in Education"
    )

    print("University System")
    for member in (person, student, lecturer, postgraduate):
        print(f"\n--- {type(member).__name__} ---")
        member.display_details()

    print("\n--- Activities ---")
    student.study()
    lecturer.teach()
    postgraduate.study()  # Inherited directly from Student.
    postgraduate.research()

    print("\n--- Hierarchical inheritance ---")
    print(f"Student is a Person: {isinstance(student, Person)}")
    print(f"Lecturer is a Person: {isinstance(lecturer, Person)}")

    print("\n--- Multilevel inheritance ---")
    print(f"PostgraduateStudent is a Student: {isinstance(postgraduate, Student)}")
    print(f"PostgraduateStudent is a Person: {isinstance(postgraduate, Person)}")


if __name__ == "__main__":
    main()
