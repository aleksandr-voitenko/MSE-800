"""Scripted console demonstration of the domain model."""

from datetime import timedelta

from .domain import Lecturer, Student, utc_now


def heading(number: int, text: str) -> None:
    print(f"\n{number}. {text}")
    print("-" * (len(text) + 3))


def run_demo() -> None:
    print("=" * 58)
    print("       COLLEGE MANAGEMENT SYSTEM — OOP DEMO")
    print("=" * 58)

    lecturer = Lecturer(
        name="Mohammad Norouzifard",
        email="Mohammad.Norouzifard@yoobeecolleges.com",
        employee_number="L-104",
    )
    student = Student(
        name="Aleksandr Voitenko",
        email="a.v@lol.com",
        student_number="S-2026-017",
    )

    heading(1, "Lecturer creates a course")
    course = lecturer.create_course(
        code="MSE-800",
        title="Software Engineering",
        description="Object-oriented analysis and software design.",
    )
    lecture = lecturer.schedule_lecture(
        course=course,
        topic="Object-oriented modelling",
        scheduled_at=utc_now() + timedelta(days=1),
        room="Lab 2",
    )
    print(f"Created {course.code}: {course.title}")
    print(f"Scheduled lecture: {lecture.topic} in {lecture.room}")

    heading(2, "Student enrols in the course")
    enrollment = student.enroll(course)
    print(f"{student.name} is now {enrollment.status.value} in {course.code}")
    print("Enrolled students:", ", ".join(s.name for s in course.enrolled_students()))

    heading(3, "Lecturer creates and publishes an assignment")
    assignment = lecturer.create_assignment(
        course=course,
        title="UML to Python demonstration",
        instructions="Submit a small object-oriented Python program.",
        due_at=utc_now() + timedelta(days=7),
        max_mark=100,
    )
    print(f"Initial status: {assignment.status.value}")
    assignment.publish()
    print(f"Published: {assignment.title} (maximum {assignment.max_mark:g} marks)")

    heading(4, "Student views and submits the assignment")
    for available_assignment in course.published_assignments():
        print(f"Available: {available_assignment.title}")
    submission = student.submit(assignment, "submissions/ari-patel-demo.zip")
    print(f"Submission accepted: {submission.file_url}")
    print(f"Submission status: {submission.status.value}")

    heading(5, "Lecturer records a draft mark")
    mark = lecturer.record_mark(
        submission=submission,
        score=84,
        feedback="Clear class design and a well-structured demonstration.",
    )
    print(f"Draft recorded: {mark.score:g}/{assignment.max_mark:g}")
    print(f"Marks visible to student: {len(student.view_published_marks())}")

    heading(6, "Lecturer publishes the mark later")
    lecturer.publish_mark(mark)
    for published_mark in student.view_published_marks():
        print(
            f"{assignment.title}: {published_mark.score:g}/{assignment.max_mark:g}"
        )
        print(f"Feedback: {published_mark.feedback}")

    print("\nDemo completed successfully.")


if __name__ == "__main__":
    run_demo()
