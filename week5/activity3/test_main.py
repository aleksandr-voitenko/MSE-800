"""Tests for the university people OOP example."""

import unittest
from decimal import Decimal

from main import Academic, GeneralStaff


class AcademicTests(unittest.TestCase):
    def test_publication_count(self) -> None:
        lecturer = Academic(
            "P001",
            "Dr Aroha Williams",
            "AC101",
            "123-456-789",
            ["Publication one", "Publication two"],
        )

        lecturer.add_publication("Publication three")

        self.assertEqual(lecturer.calculate_publication_count(), 3)


class GeneralStaffTests(unittest.TestCase):
    def test_hourly_pay_rate(self) -> None:
        staff_member = GeneralStaff(
            "P002",
            "James Chen",
            "GS201",
            "987-654-321",
            Decimal("52000"),
        )

        self.assertEqual(staff_member.calculate_pay_rate(), Decimal("25"))

    def test_invalid_working_hours(self) -> None:
        with self.assertRaises(ValueError):
            GeneralStaff(
                "P002",
                "James Chen",
                "GS201",
                "987-654-321",
                Decimal("52000"),
                standard_hours_per_week=Decimal("0"),
            )


if __name__ == "__main__":
    unittest.main()
