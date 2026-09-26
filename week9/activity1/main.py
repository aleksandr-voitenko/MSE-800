def main():
    STUDENTS_COUNT = 5
    students_dict = dict()

    for i in range (STUDENTS_COUNT):
        name = input("Name: ")
        mark = int(input("Mark: "))
        students_dict[name] = mark;

    average_mark = 0;
    for [name, mark] in students_dict.items():
        print(f"Student: {name} - {mark} - {'PASS' if mark >= 50 else 'FAIL'}")
        average_mark += mark
    average_mark /= STUDENTS_COUNT
    print(f"Average mark: {average_mark:.2f}")

if __name__ == "__main__":
    main()