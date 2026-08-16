import sqlite3

# Child tables are dropped before their parent tables. This order avoids
# conflicts with the foreign-key relationships when the schema is reset.

DROP_SCHEMA_SQL = """
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS lectures;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS lecturers;
"""

## SQLite has no dedicated DATE storage class, so ISO-8601 dates are kept
## as TEXT. YYYY-MM-DD also sorts correctly in chronological order.

CREATE_SCHEMA_SQL = """
CREATE TABLE students (
    student_id  TEXT PRIMARY KEY,
    first_name  TEXT NOT NULL,
    last_name   TEXT NOT NULL,
    birth_date  TEXT NOT NULL
);

CREATE TABLE lecturers (
    lecturer_id INTEGER PRIMARY KEY,
    first_name  TEXT NOT NULL,
    last_name   TEXT NOT NULL,
    email       TEXT NOT NULL UNIQUE,
    address     TEXT
);

CREATE TABLE courses (
    course_code TEXT PRIMARY KEY,
    course_name TEXT NOT NULL,
    units       INTEGER NOT NULL CHECK (units > 0),
    description TEXT
);

CREATE TABLE lectures (
    lecture_id    INTEGER PRIMARY KEY,
    course_code   TEXT NOT NULL,
    lecturer_id   INTEGER NOT NULL,
    lecture_name  TEXT NOT NULL,
    lecture_date  TEXT NOT NULL,
    lecture_time  TEXT NOT NULL,

    -- Each lecture belongs to one course. If the course code is renamed, the
    -- new value is propagated; deleting a course also deletes its lectures.
    FOREIGN KEY (course_code)
        REFERENCES courses(course_code)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    -- A lecturer cannot be deleted while lectures still reference that person.
    -- RESTRICT prevents accidentally leaving a lecture without a lecturer.
    FOREIGN KEY (lecturer_id)
        REFERENCES lecturers(lecturer_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE enrollments (
    student_id       TEXT NOT NULL,
    course_code      TEXT NOT NULL,
    enrollment_date  TEXT NOT NULL,

    -- Enrollment is the junction table for the many-to-many relationship
    -- between students and courses. The composite primary key also prevents
    -- one student from being enrolled in the same course more than once.
    PRIMARY KEY (student_id, course_code),

    -- Enrollment rows have no useful meaning after their student or course is
    -- deleted, so ON DELETE CASCADE removes those dependent rows automatically.
    FOREIGN KEY (student_id)
        REFERENCES students(student_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    FOREIGN KEY (course_code)
        REFERENCES courses(course_code)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);
"""


def reset_schema(conn: sqlite3.Connection) -> None:
    """Drop existing tables and recreate the schema."""

    # executescript() is used because each constant contains several SQL
    # statements; execute() accepts only one statement at a time.
    conn.executescript(DROP_SCHEMA_SQL)
    conn.executescript(CREATE_SCHEMA_SQL)
