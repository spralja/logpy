import unittest

from logpy.model import Entry

from datetime import datetime


class EntryIntersectionTestCase(unittest.TestCase):

    def test_entry_intersection0(self):
        """
        a1-a2-b1-b2 - no intersection
        """

        entry1 = Entry(datetime(2023, 2, 12, 18, 35), datetime(2023, 2, 12, 18, 40), 'Test')
        start_time = datetime(2023, 2, 12, 18, 45)
        end_time = datetime(2023, 2, 12, 18, 50)

        self.assertFalse(entry1.has_intersection(entry2))
    
    def test_entry_intersection1(self):
        """
        a1-b1-a2-b2 - intersection
        """

        entry1 = Entry(datetime(2023, 2, 12, 18, 40), datetime(2023, 2, 12, 18, 50), 'Test')
        entry2 = Entry(datetime(2023, 2, 12, 18, 45), datetime(2023, 2, 12, 18, 55), 'Test')

        self.assertTrue(entry1.has_intersection(entry2))

    def test_entry_intersection2(self):
        """
        a1-b1-b2-a2 - intersection
        """

        entry1 = Entry(datetime(2023, 2, 12, 18, 45), datetime(2023, 2, 12, 19), 'Test')
        entry2 = Entry(datetime(2023, 2, 12, 18, 50), datetime(2023, 2, 12, 18, 55), 'Test')

        self.assertTrue(entry1.has_intersection(entry2))

    def test_entry_intersection3(self):
        """
        b1-a1-a2-b2 - intersection
        """

        entry1 = Entry(datetime(2023, 2, 12, 18, 50), datetime(2023, 2, 12, 18, 55), 'Test')
        entry2 = Entry(datetime(2023, 2, 12, 18, 45), datetime(2023, 2, 12, 19), 'Test')

        self.assertTrue(entry1.has_intersection(entry2))

    def test_entry_intersection4(self):
        """
        b1-a1-b2-a2 - intersection
        """

        entry1 = Entry(datetime(2023, 2, 12, 18, 55), datetime(2023, 2, 12, 19, 5), 'Test')
        entry2 = Entry(datetime(2023, 2, 12, 18, 50), datetime(2023, 2, 12, 19), 'Test')

        self.assertTrue(entry1.has_intersection(entry2))

    def test_entry_intersection5(self):
        """
        b1-b2-a1-a2 - no intersection
        """

        entry1 = Entry(datetime(2023, 2, 12, 19), datetime(2023, 2, 12, 19, 5), 'Test')
        entry2 = Entry(datetime(2023, 2, 12, 18, 50), datetime(2023, 2, 12, 18, 55), 'Test')

        self.assertFalse(entry1.has_intersection(entry2))

    def test_entry_intersection6(self):
        """
        a1-a2 - no intersection (other is None)
        """
        
        entry1 = Entry(datetime(2023, 2, 12, 19, 30), datetime(2023, 2, 12, 19, 35), 'Test')
        entry2 = None

        self.assertFalse(entry1.has_intersection(entry2))
