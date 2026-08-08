from dataclasses import dataclass

@dataclass
class Student:
  age: int
  name: str;
  surname: str;
  address: str;
  id: str;

def input_student_data() -> Student:
  name = input("Name: ")
  surname = input("Surname: ")
  age = int(input("Age: "))
  address = input("Address: ")
  student_id = input("Id: ")

  return Student(age=age, name=name, surname=surname, address=address, id=student_id)

def print_students(students: list[Student]):
  for s in students:
    print(s)

def main():
  students: list[Student] = [
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