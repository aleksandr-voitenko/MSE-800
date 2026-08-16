import sqlite3

# Dates use ISO-8601 strings (YYYY-MM-DD)
STUDENTS = [
    ("S001", "Alice", "Johnson", "2002-04-18"),
    ("S002", "Ben", "Carter", "2001-11-02"),
    ("S003", "Chloe", "Wilson", "2003-01-25"),
    ("S004", "Daniel", "Kim", "2002-07-14"),
    ("S005", "Emma", "Brown", "2001-09-30"),
    ("S006", "Farah", "Ahmed", "2003-05-09"),
    ("S007", "George", "Miller", "2002-12-21"),
]

LECTURERS = [
    (1, "Maya", "Patel", "maya.patel@example.edu", "12 University Road"),
    (2, "Liam", "Chen", "liam.chen@example.edu", "8 College Avenue"),
    (3, "Sofia", "Martin", "sofia.martin@example.edu", "25 Campus Street"),
]

COURSES = [
    (
        "COMP101",
        "Introduction to Programming",
        15,
        "Programming fundamentals using Python.",
    ),
    (
        "DATA201",
        "Database Systems",
        15,
        "Relational modelling, SQL, normalization, and transactions.",
    ),
    (
        "NET202",
        "Computer Networks",
        15,
        "Network architecture, protocols, and troubleshooting.",
    ),
    (
        "WEB203",
        "Web Development",
        15,
        "Client-server web development and HTTP fundamentals.",
    ),
]

# course_code and lecturer_id are foreign keys, so the corresponding course
# and lecturer records must exist before these lecture rows are inserted.
LECTURES = [
    (1, "COMP101", 1, "Python Basics", "2026-08-20", "09:00"),
    (2, "COMP101", 1, "Functions and Modules", "2026-08-27", "09:00"),
    (3, "DATA201", 2, "Relational Modelling", "2026-08-21", "11:00"),
    (4, "DATA201", 2, "SQL Joins", "2026-08-28", "11:00"),
    (5, "NET202", 3, "Network Layers", "2026-08-22", "14:00"),
    (6, "WEB203", 1, "HTTP and Web Fundamentals", "2026-08-23", "10:00"),
]

# Several students intentionally have two or more enrollments so that the
# assignment's second aggregate query returns meaningful sample results.
ENROLLMENTS = [
    ("S001", "COMP101", "2026-08-01"),
    ("S001", "DATA201", "2026-08-01"),
    ("S002", "COMP101", "2026-08-02"),
    ("S003", "DATA201", "2026-08-02"),
    ("S003", "NET202", "2026-08-02"),
    ("S004", "COMP101", "2026-08-03"),
    ("S004", "DATA201", "2026-08-03"),
    ("S004", "WEB203", "2026-08-03"),
    ("S005", "NET202", "2026-08-04"),
    ("S006", "COMP101", "2026-08-04"),
    ("S006", "WEB203", "2026-08-04"),
    ("S007", "DATA201", "2026-08-05"),
]


def seed_database(conn: sqlite3.Connection) -> None:
    """Populate all tables with deterministic sample data."""

    # Parent tables are inserted first because foreign-key checking is enabled.
    # executemany() efficiently executes the same parameterized INSERT for all
    # tuples in each sample-data collection.
    conn.executemany(
        """
        INSERT INTO students (student_id, first_name, last_name, birth_date)
        VALUES (?, ?, ?, ?)
        """,
        STUDENTS,
    )

    conn.executemany(
        """
        INSERT INTO lecturers (lecturer_id, first_name, last_name, email, address)
        VALUES (?, ?, ?, ?, ?)
        """,
        LECTURERS,
    )

    conn.executemany(
        """
        INSERT INTO courses (course_code, course_name, units, description)
        VALUES (?, ?, ?, ?)
        """,
        COURSES,
    )

    # Lectures depend on both courses and lecturers.
    conn.executemany(
        """
        INSERT INTO lectures (
            lecture_id,
            course_code,
            lecturer_id,
            lecture_name,
            lecture_date,
            lecture_time
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        LECTURES,
    )

    # Enrollments are inserted last because they reference both students and
    # courses through their foreign keys.
    conn.executemany(
        """
        INSERT INTO enrollments (student_id, course_code, enrollment_date)
        VALUES (?, ?, ?)
        """,
        ENROLLMENTS,
    )
