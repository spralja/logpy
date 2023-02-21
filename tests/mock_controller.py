from logpy.controller import MutatorController
from logpy.model import Entry, Mutation

from datetime import timezone
from typing import Tuple

class MockController(MutatorController):
    def __init__(self, *data: Tuple[Entry]):
        self.data = data
        self.mutations = []

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

    def _publish_entry(self, entry):
        self.data += (entry,)
        self.mutations.append(Mutation(
            'creator',
            entry
        )) 
