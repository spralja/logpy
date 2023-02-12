import unittest

from logpy.model import Entry
from logpy.controller import Controller
from logpy.database import Database

from datetime import datetime
from typing import Optional


class MockDataBase(Database):

    def __init__(self):
        self.data = [
            Entry(datetime(2023, 12, 2, 12), datetime(2023, 12, 2, 13), 'Category A'),
            Entry(datetime(2023, 12, 2, 13), datetime(2023, 12, 2, 14), 'Category B'),
        ]

    def find_first_after(self, time: datetime) -> Optional[Entry]:
        for datum in self.data:
            if datum.start_time >= time:
                return datum

    def find_last_before(self, time: datetime) -> Optional[Entry]:
        for datum in reversed(self.data):
            if datum.start_time < time:
                return datum


class ControllerIntersectionTestCase(unittest.TestCase):

    def test_controller_intersection_test1(self):
        pass
