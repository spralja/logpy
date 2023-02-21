from logpy.controller import Controller
from logpy.model import Entry

from datetime import timezone
from typing import Tuple

class MockController(Controller):
    def __init__(self, *data: Tuple[Entry]):
        self.data = data

    def _find_first_after(self, dt):
        if dt.tzinfo != timezone.utc:
            raise ValueError('dt.tzinfo must be utc')
        
        for datum in self.data:
            if datum.start_time >= dt:
                return datum
            
        return None

    def _find_last_before(self, dt):
        if dt.tzinfo != timezone.utc:
            raise ValueError('dt.tzinfo must be utc')

        for datum in reversed(self.data):
            if datum.start_time <= dt:
                return datum

        return None