import unittest

from logpy.model import Entry

from .mock_controller import MockController

from datetime import datetime, timezone


class MockControllerTestCase(unittest.TestCase):

    def setUp(self):
        self.controller = MockController(
            Entry(
                datetime(2022, 1, 1, 0, 0, tzinfo=timezone.utc), 
                datetime(2022, 1, 1, 1, 0, tzinfo=timezone.utc), 
                'Work'
            ),
            Entry(
                datetime(2022, 1, 2, 0, 0, tzinfo=timezone.utc), 
                datetime(2022, 1, 2, 1, 30, tzinfo=timezone.utc), 
                'Personal'
            ),
            Entry(
                datetime(2022, 1, 3, 9, 0, tzinfo=timezone.utc), 
                datetime(2022, 1, 3, 10, 0, tzinfo=timezone.utc), 
                'Work'
            ),
            Entry(
                datetime(2022, 1, 4, 10, 0, tzinfo=timezone.utc), 
                datetime(2022, 1, 4, 12, 0, tzinfo=timezone.utc), 
                'Personal'
            ),
            Entry(
                datetime(2022, 1, 5, 13, 0, tzinfo=timezone.utc), 
                datetime(2022, 1, 5, 14, 0, tzinfo=timezone.utc), 
                'Work'
            ),
            Entry(
                datetime(2022, 1, 6, 14, 0, tzinfo=timezone.utc), 
                datetime(2022, 1, 6, 15, 30, tzinfo=timezone.utc), 
                'Personal'
            )
        )

    def test_find_first_after_timezone_not_utc(self):
        with self.assertRaises(ValueError):
            self.controller._find_first_after(datetime(2022, 2, 2))

    def test_find_last_before_timezone_not_utc(self):
        with self.assertRaises(ValueError):
            self.controller._find_last_before(datetime(2023, 2, 3))

    def test_find_first_after_there_is_none(self):
        entry = self.controller._find_first_after(
            datetime(2023, 1, 1, tzinfo=timezone.utc)
        )

        expected = None

        self.assertEqual(entry, expected)

    def test_find_first_after_the_time_is_during_another_entry(self):
        entry = self.controller._find_first_after(
            datetime(2022, 1, 1, 0, 30, tzinfo=timezone.utc)
        )

        expected = Entry(
            datetime(2022, 1, 2, 0, 0, tzinfo=timezone.utc),
            datetime(2022, 1, 2, 1, 30, tzinfo=timezone.utc),
            'Personal'
        )

        self.assertEqual(entry, expected)

    def test_find_first_after_the_time_is_at_start_of_the_entry(self):
        entry = self.controller._find_first_after(
            datetime(2022, 1, 4, 10, 0, tzinfo=timezone.utc)
        )

        expected = Entry(
                datetime(2022, 1, 4, 10, 0, tzinfo=timezone.utc), 
                datetime(2022, 1, 4, 12, 0, tzinfo=timezone.utc), 
                'Personal'
        )

        self.assertEqual(entry, expected)

    def test_find_first_after_the_time_is_before_the_start_of_the_entry(self):
        entry = self.controller._find_first_after(
            datetime(2022, 1, 5, 12, tzinfo=timezone.utc)
        )

        expected = Entry(
            datetime(2022, 1, 5, 13, 0, tzinfo=timezone.utc), 
            datetime(2022, 1, 5, 14, 0, tzinfo=timezone.utc), 
            'Work'
        )

        self.assertEqual(entry, expected)
