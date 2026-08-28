"""Simple OOP example based on a university people hierarchy."""

from decimal import Decimal


class Person:
    """Base class for every person at the university."""

    def __init__(self, person_id: str, name: str) -> None:
        self.person_id = person_id
        self.name = name


class Student(Person):
    """A university student."""

    def __init__(self, person_id: str, name: str, student_number: str) -> None:
        super().__init__(person_id, name)
        self.student_number = student_number


class Staff(Person):
    """Base class for university staff members."""

    def __init__(
        self,
        person_id: str,
        name: str,
        staff_number: str,
        tax_number: str,
    ) -> None:
        super().__init__(person_id, name)
        self.staff_number = staff_number
        self.tax_number = tax_number


class Academic(Staff):
    """An academic staff member, such as a lecturer."""

    def __init__(
        self,
        person_id: str,
        name: str,
        staff_number: str,
        tax_number: str,
        publications: list[str] | None = None,
    ) -> None:
        super().__init__(person_id, name, staff_number, tax_number)
        self.publications = list(publications) if publications else []

    def add_publication(self, title: str) -> None:
        """Add a publication to the academic's publication list."""
        self.publications.append(title)

    def calculate_publication_count(self) -> int:
        """Return the number of publications written by the academic."""
        return len(self.publications)


class GeneralStaff(Staff):
    """A non-academic staff member paid from an annual salary."""

    def __init__(
        self,
        person_id: str,
        name: str,
        staff_number: str,
        tax_number: str,
        annual_salary: Decimal,
        standard_hours_per_week: Decimal = Decimal("40"),
        working_weeks_per_year: int = 52,
    ) -> None:
        super().__init__(person_id, name, staff_number, tax_number)

        if annual_salary < 0:
            raise ValueError("Annual salary cannot be negative.")
        if standard_hours_per_week <= 0 or working_weeks_per_year <= 0:
            raise ValueError("Working hours and weeks must be greater than zero.")

        self.annual_salary = annual_salary
        self.standard_hours_per_week = standard_hours_per_week
        self.working_weeks_per_year = working_weeks_per_year

    def calculate_pay_rate(self) -> Decimal:
        """Calculate and return the staff member's hourly pay rate."""
        annual_hours = (
            self.standard_hours_per_week * self.working_weeks_per_year
        )
        return self.annual_salary / annual_hours


def main() -> None:
    """Create example objects and display the requested calculations."""
    lecturer = Academic(
        person_id="P001",
        name="Dr Aroha Williams",
        staff_number="AC101",
        tax_number="123-456-789",
        publications=[
            "Responsible Artificial Intelligence",
            "Machine Learning in Education",
            "Ethics of Automated Decision Making",
        ],
    )

    general_staff_member = GeneralStaff(
        person_id="P002",
        name="James Chen",
        staff_number="GS201",
        tax_number="987-654-321",
        annual_salary=Decimal("52000"),
    )

    publication_count = lecturer.calculate_publication_count()
    pay_rate = general_staff_member.calculate_pay_rate()

    print("UNIVERSITY STAFF INFORMATION")
    print("----------------------------")
    print(f"Lecturer: {lecturer.name}")
    print(f"Number of publications: {publication_count}")
    print()
    print(f"General staff member: {general_staff_member.name}")
    print(f"Calculated pay rate: ${pay_rate:.2f} per hour")


if __name__ == "__main__":
    main()
