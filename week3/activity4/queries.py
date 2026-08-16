import sqlite3

COURSE_REGISTRATION_COUNTS_SQL = """
SELECT
    c.course_code,
    c.course_name,
    COUNT(e.student_id) AS student_count
FROM courses AS c
LEFT JOIN enrollments AS e
    ON e.course_code = c.course_code
GROUP BY
    c.course_code
"""

MULTI_COURSE_STUDENTS_SQL = """
SELECT
    s.student_id,
    s.first_name,
    s.last_name,
    COUNT(DISTINCT e.course_code) AS course_count
FROM students AS s
JOIN enrollments AS e
    ON e.student_id = s.student_id
GROUP BY
    s.student_id
HAVING COUNT(DISTINCT e.course_code) > 1
"""

def get_course_registration_counts(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    """Return the number of registered students in every course."""
    return conn.execute(COURSE_REGISTRATION_COUNTS_SQL).fetchall()

def get_students_in_multiple_courses(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    """Return students who are enrolled in more than one course."""
    return conn.execute(MULTI_COURSE_STUDENTS_SQL).fetchall()
