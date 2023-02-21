import unittest

from logpy.model import Entry, Mutation

from datetime import datetime, timedelta, timezone


class EntryTestCase(unittest.TestCase):
    def test_validation(self):
        # end_time <= start_time
        with self.assertRaises(ValueError):
            Entry(
                datetime(2023, 20, 2, 23, 40, tzinfo=timezone.utc),
                datetime(2023, 20, 2, 23, 30, tzinfo=timezone.utc),
                'Category'
            )

        # start_time and end_time are not UTC
        with self.assertRaises(ValueError):
            Entry(
                datetime(2023, 20, 2, 23, 40),
                datetime(2023, 20, 2, 23, 45),
                'Category'
            )

    def test_duration(self):
        entry = Entry(
            datetime(2023, 2, 21, 14, 40, tzinfo=timezone.utc),
            datetime(2023, 2, 21, 14, 45, tzinfo=timezone.utc),
            'Category'
        )

        self.assertEqual(entry.duration, timedelta(seconds=300))
            

class EntryIntersectionTestCase(unittest.TestCase):
    def setUp(self):
        self.entry = Entry(
            datetime(2023, 2, 20, 23, 10, tzinfo=timezone.utc),
            datetime(2023, 2, 20, 23, 15, tzinfo=timezone.utc),
            'Category'
        )

    def test_intersection_validation(self):
        # start_time and end_time are not utc
        with self.assertRaises(ValueError):
            self.entry.intersection(
                datetime(2023, 2, 20, 23),
                datetime(2023, 2, 20, 23)
            )

        # start_time >= end_time
        with self.assertRaises(ValueError):
            self.entry.intersection(
                datetime(2023, 2, 20, 23, 15, tzinfo=timezone.utc),
                datetime(2023, 2, 20, 23, 10, tzinfo=timezone.utc)
            )
    
    def test_intersection_T1_T2_E1_E2(self):
        start_time = datetime(2023, 2, 20, 23, 5, tzinfo=timezone.utc)
        end_time = datetime(2023, 2, 20, 23, 10, tzinfo=timezone.utc)
        interval = (start_time, end_time)

        expected = None

        self.assertEqual(self.entry.intersection(*interval), expected)

    def test_intersection_T1_E1_T2_E2(self):
        start_time = datetime(2023, 2, 20, 23, 5, tzinfo=timezone.utc)
        end_time = datetime(2023, 2, 20, 23, 12, tzinfo=timezone.utc)
        interval = (start_time, end_time)

        expected = Entry(
            datetime(2023, 2, 20, 23, 10, tzinfo=timezone.utc),
            datetime(2023, 2, 20, 23, 12, tzinfo=timezone.utc),
            'Category'
        )

        self.assertEqual(self.entry.intersection(*interval), expected)

    def test_intersection_E1_T1_T2_E2(self):
        start_time = datetime(2023, 2, 20, 23, 12, tzinfo=timezone.utc)
        end_time = datetime(2023, 2, 20, 23, 14, tzinfo=timezone.utc)
        interval = (start_time, end_time)

        expected = Entry(
            datetime(2023, 2, 20, 23, 12, tzinfo=timezone.utc),
            datetime(2023, 2, 20, 23, 14, tzinfo=timezone.utc),
            'Category'
        )

        self.assertEqual(self.entry.intersection(*interval), expected)

    def test_intersection_E1_T1_E2_T2(self):
        start_time = datetime(2023, 2, 20, 23, 12, tzinfo=timezone.utc)
        end_time = datetime(2023, 2, 20, 23, 16, tzinfo=timezone.utc)
        interval = (start_time, end_time)

        expected = Entry(
            datetime(2023, 2, 20, 23, 12, tzinfo=timezone.utc),
            datetime(2023, 2, 20, 23, 15, tzinfo=timezone.utc),
            'Category'
        )

        self.assertEqual(self.entry.intersection(*interval), expected)

    def test_intersection_E1_E2_T1_T2(self):
        start_time = datetime(2023, 2, 20, 23, 45, tzinfo=timezone.utc)
        end_time = datetime(2023, 2, 20, 23, 50, tzinfo=timezone.utc)
        interval = (start_time, end_time)

        expected = None

        self.assertEqual(self.entry.intersection(*interval), expected)

    def test_intersection_T1_E1_E2_T2(self):
        start_time = datetime(2023, 2, 20, 23, 5, tzinfo=timezone.utc)
        end_time = datetime(2023, 2, 20, 23, 20, tzinfo=timezone.utc)
        interval = (start_time, end_time)

        expected = Entry(
            datetime(2023, 2, 20, 23, 10, tzinfo=timezone.utc),
            datetime(2023, 2, 20, 23, 15, tzinfo=timezone.utc),
            'Category'
        )

        self.assertEqual(self.entry.intersection(*interval), expected)


class MutationTestCase(unittest.TestCase):
    def test_validation(self):
        mutation_class = 'test'
        entry = Entry(
            datetime(2023, 2, 21, 18, 35, tzinfo=timezone.utc),
            datetime(2023, 2, 21, 18, 40, tzinfo=timezone.utc),
            'Category'
        )

        with self.assertRaises(ValueError):
            Mutation(mutation_class, entry)
            