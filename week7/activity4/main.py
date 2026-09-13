class Department:
    def __init__(self, name: str, head: str):
        self.name = name
        self.head = head

    def print(self):
        print(f"Department - name: {self.name}, head: {self.head}")

class University:
    def __init__(self, name: str):
        self.name = name
        self.departments: list[Department] = []

    def add_department(self, dep: Department):
        self.departments.append(dep)


    def print(self):
        print(f"University {self.name}")

        for d in self.departments:
            d.print()

def main():
    u: University = University("Boobee Colledge")
    u.add_department(Department("Computer Science", "Alice Altkinson"))
    u.add_department(Department("Bio engineering", "Bob Badlock"))
    u.add_department(Department("Social sciences", "Charlie Chin"))

    print("=== Printing Universiti info ===")
    u.print()

if __name__ == "__main__":
    main()