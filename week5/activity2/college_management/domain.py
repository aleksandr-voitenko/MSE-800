"""Core object-oriented domain model for the college management demo."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


def utc_now() -> datetime:
    """Return an aware UTC timestamp."""

    return datetime.now(timezone.utc)


class EnrollmentStatus(str, Enum):
    ACTIVE = "active"
    WITHDRAWN = "withdrawn"


class AssignmentStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    CLOSED = "closed"


class SubmissionStatus(str, Enum):
    SUBMITTED = "submitted"
    MARKED = "marked"


@dataclass
class User(ABC):
    """Shared information for all system users."""

    name: str
    email: str
    user_id: UUID = field(default_factory=uuid4, init=False)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("A user must have a name.")
        if "@" not in self.email:
            raise ValueError("A valid email address is required.")

    @property
    @abstractmethod
    def role(self) -> str:
        """Return the user's role in the system."""


@dataclass
class Student(User):
    student_number: str
    enrollments: list[Enrollment] = field(default_factory=list, init=False, repr=False)
    submissions: list[Submission] = field(default_factory=list, init=False, repr=False)

    @property
    def role(self) -> str:
        return "student"

    def enroll(self, course: Course) -> Enrollment:
        """Enrol in a course or return the existing active enrolment."""

        return course.enroll(self)

    def is_enrolled_in(self, course: Course) -> bool:
        return any(
            enrollment.course is course
            and enrollment.status is EnrollmentStatus.ACTIVE
            for enrollment in self.enrollments
        )

    def submit(
        self,
        assignment: Assignment,
        file_url: str,
        submitted_at: Optional[datetime] = None,
    ) -> Submission:
        """Submit or replace work before the assignment deadline."""

        return assignment.receive_submission(
            student=self,
            file_url=file_url,
            submitted_at=submitted_at or utc_now(),
        )

    def view_published_marks(self) -> list[Mark]:
        """Return only marks that have been released to the student."""

        return [
            submission.mark
            for submission in self.submissions
            if submission.mark is not None and submission.mark.is_published
        ]


@dataclass
class Lecturer(User):
    employee_number: str
    courses: list[Course] = field(default_factory=list, init=False, repr=False)

    @property
    def role(self) -> str:
        return "lecturer"

    def create_course(self, code: str, title: str, description: str) -> Course:
        return Course(code=code, title=title, description=description, lecturer=self)

    def update_course(
        self,
        course: Course,
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> None:
        self._require_owned_course(course)
        course.update_details(title=title, description=description)

    def schedule_lecture(
        self,
        course: Course,
        topic: str,
        scheduled_at: datetime,
        room: str,
    ) -> Lecture:
        self._require_owned_course(course)
        return Lecture(
            course=course,
            topic=topic,
            scheduled_at=scheduled_at,
            room=room,
        )

    def create_assignment(
        self,
        course: Course,
        title: str,
        instructions: str,
        due_at: datetime,
        max_mark: float,
    ) -> Assignment:
        self._require_owned_course(course)
        return Assignment(
            course=course,
            title=title,
            instructions=instructions,
            due_at=due_at,
            max_mark=max_mark,
        )

    def record_mark(
        self,
        submission: Submission,
        score: float,
        feedback: str,
    ) -> Mark:
        """Create a draft mark, or update the existing draft mark."""

        self._require_owned_course(submission.assignment.course)
        if submission.mark is not None:
            submission.mark.update(score=score, feedback=feedback)
            return submission.mark
        return Mark(
            submission=submission,
            lecturer=self,
            score=score,
            feedback=feedback,
        )

    def publish_mark(self, mark: Mark) -> None:
        if mark.lecturer is not self:
            raise PermissionError("Only the lecturer who recorded a mark may publish it.")
        mark.publish()

    def _require_owned_course(self, course: Course) -> None:
        if course.lecturer is not self:
            raise PermissionError("The lecturer is not assigned to this course.")


@dataclass
class Course:
    code: str
    title: str
    description: str
    lecturer: Lecturer
    course_id: UUID = field(default_factory=uuid4, init=False)
    enrollments: list[Enrollment] = field(default_factory=list, init=False, repr=False)
    lectures: list[Lecture] = field(default_factory=list, init=False, repr=False)
    assignments: list[Assignment] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self) -> None:
        if not self.code.strip() or not self.title.strip():
            raise ValueError("A course requires a code and title.")
        self.lecturer.courses.append(self)

    def update_details(
        self,
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> None:
        if title is not None:
            if not title.strip():
                raise ValueError("The course title cannot be empty.")
            self.title = title
        if description is not None:
            self.description = description

    def enroll(self, student: Student) -> Enrollment:
        for enrollment in self.enrollments:
            if enrollment.student is student:
                if enrollment.status is EnrollmentStatus.WITHDRAWN:
                    enrollment.reactivate()
                return enrollment

        enrollment = Enrollment(student=student, course=self)
        self.enrollments.append(enrollment)
        student.enrollments.append(enrollment)
        return enrollment

    def enrolled_students(self) -> list[Student]:
        return [
            enrollment.student
            for enrollment in self.enrollments
            if enrollment.status is EnrollmentStatus.ACTIVE
        ]

    def published_assignments(self) -> list[Assignment]:
        return [
            assignment
            for assignment in self.assignments
            if assignment.status is AssignmentStatus.PUBLISHED
        ]


@dataclass
class Enrollment:
    student: Student
    course: Course
    enrolled_at: datetime = field(default_factory=utc_now)
    status: EnrollmentStatus = EnrollmentStatus.ACTIVE
    enrollment_id: UUID = field(default_factory=uuid4, init=False)

    def withdraw(self) -> None:
        self.status = EnrollmentStatus.WITHDRAWN

    def reactivate(self) -> None:
        self.status = EnrollmentStatus.ACTIVE
        self.enrolled_at = utc_now()


@dataclass
class Lecture:
    course: Course
    topic: str
    scheduled_at: datetime
    room: str
    lecture_id: UUID = field(default_factory=uuid4, init=False)

    def __post_init__(self) -> None:
        if not self.topic.strip() or not self.room.strip():
            raise ValueError("A lecture requires a topic and room.")
        self.course.lectures.append(self)

    def reschedule(self, scheduled_at: datetime, room: str) -> None:
        self.scheduled_at = scheduled_at
        self.room = room


@dataclass
class Assignment:
    course: Course
    title: str
    instructions: str
    due_at: datetime
    max_mark: float
    assignment_id: UUID = field(default_factory=uuid4, init=False)
    status: AssignmentStatus = field(default=AssignmentStatus.DRAFT, init=False)
    submissions: list[Submission] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("An assignment requires a title.")
        if self.max_mark <= 0:
            raise ValueError("The maximum mark must be greater than zero.")
        self.course.assignments.append(self)

    def publish(self) -> None:
        if self.status is AssignmentStatus.CLOSED:
            raise ValueError("A closed assignment cannot be published again.")
        self.status = AssignmentStatus.PUBLISHED

    def close(self) -> None:
        self.status = AssignmentStatus.CLOSED

    def is_open(self, at: Optional[datetime] = None) -> bool:
        moment = at or utc_now()
        return self.status is AssignmentStatus.PUBLISHED and moment <= self.due_at

    def receive_submission(
        self,
        student: Student,
        file_url: str,
        submitted_at: datetime,
    ) -> Submission:
        if not student.is_enrolled_in(self.course):
            raise PermissionError("The student is not actively enrolled in this course.")
        if not self.is_open(submitted_at):
            raise ValueError("The assignment is not open for submissions.")
        if not file_url.strip():
            raise ValueError("A submission file is required.")

        for submission in self.submissions:
            if submission.student is student:
                submission.replace_file(file_url, submitted_at)
                return submission

        submission = Submission(
            assignment=self,
            student=student,
            file_url=file_url,
            submitted_at=submitted_at,
        )
        self.submissions.append(submission)
        student.submissions.append(submission)
        return submission


@dataclass
class Submission:
    assignment: Assignment
    student: Student
    file_url: str
    submitted_at: datetime
    submission_id: UUID = field(default_factory=uuid4, init=False)
    status: SubmissionStatus = field(default=SubmissionStatus.SUBMITTED, init=False)
    mark: Optional[Mark] = field(default=None, init=False, repr=False)

    def replace_file(self, file_url: str, submitted_at: datetime) -> None:
        if self.mark is not None:
            raise ValueError("A marked submission cannot be replaced.")
        if not self.assignment.is_open(submitted_at):
            raise ValueError("The assignment is not open for resubmission.")
        self.file_url = file_url
        self.submitted_at = submitted_at


@dataclass
class Mark:
    submission: Submission
    lecturer: Lecturer
    score: float
    feedback: str
    mark_id: UUID = field(default_factory=uuid4, init=False)
    recorded_at: datetime = field(default_factory=utc_now, init=False)
    published_at: Optional[datetime] = field(default=None, init=False)

    def __post_init__(self) -> None:
        if self.submission.mark is not None:
            raise ValueError("This submission already has a mark.")
        self._validate_score(self.score)
        self.submission.mark = self
        self.submission.status = SubmissionStatus.MARKED

    @property
    def is_published(self) -> bool:
        return self.published_at is not None

    def update(self, score: float, feedback: str) -> None:
        if self.is_published:
            raise ValueError("A published mark cannot be changed in this demo.")
        self._validate_score(score)
        self.score = score
        self.feedback = feedback
        self.recorded_at = utc_now()

    def publish(self) -> None:
        self.published_at = utc_now()

    def _validate_score(self, score: float) -> None:
        if not 0 <= score <= self.submission.assignment.max_mark:
            raise ValueError(
                f"Score must be between 0 and {self.submission.assignment.max_mark}."
            )
