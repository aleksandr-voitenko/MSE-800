from db import get_connection
from queries import get_course_registration_counts, get_students_in_multiple_courses
from schema import reset_schema
from seed import seed_database


def print_course_registration_counts(rows) -> None:
    print("1. Students registered in each course")
    print("-" * 60)
    for row in rows:
        print(
            f"{row['course_code']:<8} "
            f"{row['course_name']:<32} "
            f"{row['student_count']}"
        )


def print_multi_course_students(rows) -> None:
    print("\n2. Students enrolled in more than one course")
    print("-" * 60)
    for row in rows:
        full_name = f"{row['first_name']} {row['last_name']}"
        print(f"{row['student_id']:<6} {full_name:<28} {row['course_count']} courses")


def main() -> None:
    print()
    print()
    conn = get_connection()

    try:
        # Rebuild the database on every run so the demonstration is repeatable:
        # running the program twice produces exactly the same sample dataset.
        reset_schema(conn)
        seed_database(conn)

        # Ensuring all the changes are written properly
        conn.commit()

        course_counts = get_course_registration_counts(conn)
        multi_course_students = get_students_in_multiple_courses(conn)

        print_course_registration_counts(course_counts)
        print_multi_course_students(multi_course_students)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
