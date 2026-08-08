from dataclasses import dataclass

@dataclass
class Student:
  age: int
  name: str;
  surname: str;
  id: str;

def input_student_data() -> Student:
  name = input("Name: ")
  surname = input("Surname: ")
  age = int(input("Age: "))
  student_id = input("Id: ")

  return Student(age=age, name=name, surname=surname, id=student_id)

def print_single_student(s: Student):
  print(f"Name: {s.name} {s.surname}, age: {s.age}, id: {s.id}")

def print_students(students: list[Student]):
  for s in students:
    print_single_student(s)

def main():
  students: list[Student] = [
    # Student(age=40, name="Alice", surname="Smith", id="s001"),
    # Student(age=33, name="Bob", surname="Jones", id="s002"),
    # Student(age=22, name="Charles", surname="Stone", id="s007"),
    # Student(age=34, name="Yan", surname="Bobbs", id="s005"),
    # Student(age=20, name="Harvey", surname="Davidson", id="s003"),
  ]

  while True:
    s = input_student_data();
    continue_input = input("Continue? (y/n) ")
    students.append(s);
    if continue_input != "y":
      break;

  students.sort(key=lambda x: x.age)
  print()
  print("List of students:")
  print_students(students)


if __name__ == "__main__":
  main()