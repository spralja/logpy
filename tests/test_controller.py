import unittest

from .mock_controller import MockController

from logpy.model import Entry, Mutation

from datetime import datetime, timezone

class ControllerTestCase(unittest.TestCase):

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

    def test_get_intersection_not_utc(self):
        interval = (datetime(2021, 1, 1), datetime(2023, 1, 1))

        with self.assertRaises(ValueError):
            self.controller.get_intersection(*interval)


    def test_get_intersection_all(self):
        interval = (
            datetime(2021, 1, 1, tzinfo=timezone.utc),
            datetime(2023, 1, 1, tzinfo=timezone.utc)
        )

        entries = self.controller.get_intersection(*interval)

        expected = (
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

        self.assertEqual(entries, expected)

    def test_get_intersection_all_truncated(self):
        interval = (
            datetime(2022, 1, 1, 0, 30, tzinfo=timezone.utc),
            datetime(2022, 1, 6, 15, tzinfo=timezone.utc)   
        )

        entries = self.controller.get_intersection(*interval)

        expected = (
            Entry(
                datetime(2022, 1, 1, 0, 30, tzinfo=timezone.utc), 
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
                datetime(2022, 1, 6, 15, 0, tzinfo=timezone.utc), 
                'Personal'
            )
        )

        self.assertEqual(entries, expected)

    def test_get_intersection_none(self):
        interval = (
            datetime(2020, 1, 1, tzinfo=timezone.utc),
            datetime(2021, 1, 1, tzinfo=timezone.utc)
        )

        entries = self.controller.get_intersection(*interval)

        expected = ()

        self.assertEqual(entries, expected)

    def test_intersection_one(self):
        interval = (
            datetime(2022, 1, 1, 0, 30, tzinfo=timezone.utc), 
            datetime(2022, 1, 1, 1, 0, tzinfo=timezone.utc), 
        )

        entries = self.controller.get_intersection(*interval)

        expected = (
            Entry(
                datetime(2022, 1, 1, 0, 30, tzinfo=timezone.utc), 
                datetime(2022, 1, 1, 1, 0, tzinfo=timezone.utc), 
                'Work'
            ),
        )

        self.assertEqual(entries, expected)

    def test_get_intersection_one_truncated(self):
        interval = (
            datetime(2022, 1, 2, 0, 30, tzinfo=timezone.utc), 
            datetime(2022, 1, 2, 1, 15, tzinfo=timezone.utc), 
        )

        entries = self.controller.get_intersection(*interval)
        
        expected = (
            Entry(
                datetime(2022, 1, 2, 0, 30, tzinfo=timezone.utc), 
                datetime(2022, 1, 2, 1, 15, tzinfo=timezone.utc), 
                'Personal'
            ),
        )

        self.assertEqual(entries, expected)


class MutattorController(unittest.TestCase):
    
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

    def test_create_entry_conflict_within(self):
        entry = Entry(
            datetime(2022, 1, 1, 0, 15, tzinfo=timezone.utc),
            datetime(2022, 1, 1, 0, 45, tzinfo=timezone.utc),
            'Category'
        )

        with self.assertRaises(KeyError):
            self.controller.create_entry(entry)

    def test_create_entry_conflict_right_overlap(self):
        entry = Entry(
            datetime(2021, 12, 31, 23, tzinfo=timezone.utc),
            datetime(2022, 2, 1, tzinfo=timezone.utc),
            'Category'
        )

        with self.assertRaises(KeyError):
            self.controller.create_entry(entry)

    def test_create_entry_conflict_right_overlap(self):
        entry = Entry(
            datetime(2022, 1, 1, 0, 30, tzinfo=timezone.utc),
            datetime(2023, 1, 1, tzinfo=timezone.utc),
            'Cat'
        )

        with self.assertRaises(KeyError):
            self.controller.create_entry(entry)

    def test_create_entry_conflict_without(self):
        entry = Entry(
            datetime(2021, 1, 1, tzinfo=timezone.utc),
            datetime(2023, 1, 1, tzinfo=timezone.utc),
            'Cats'
        )

        with self.assertRaises(KeyError):
            self.controller.create_entry(entry)

    def test_create_entry_no_conflict_tight(self):
        entry = Entry(
            datetime(2022, 1, 1, 1, tzinfo=timezone.utc),
            datetime(2022, 1, 2, 0, tzinfo=timezone.utc),
            'Catter'
        )

        expected_data = (
            Entry(
                datetime(2022, 1, 1, 0, 0, tzinfo=timezone.utc), 
                datetime(2022, 1, 1, 1, 0, tzinfo=timezone.utc), 
                'Work'
            ),
            Entry(
                datetime(2022, 1, 1, 1, tzinfo=timezone.utc),
                datetime(2022, 1, 2, 0, tzinfo=timezone.utc),
                'Catter'
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

        expected_mutations = [
            Mutation(
                'creator',
                entry
            )
        ]

        self.controller.create_entry(entry)

        self.assertEqual(self.controller.data, expected_data)
        
        self.assertEqual(self.controller.mutations, expected_mutations)
