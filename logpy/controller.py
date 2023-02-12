from .database import Database, ComplexDatabase
from .model import Entry


from datetime import datetime
from typing import List


class Controller:
    database: Database
    
    def __init__(self, database):
        self.database = database
    
    def intersection(self, start_time: datetime, end_time: datetime) -> List[Entry]:
        if(isinstance(self.database, ComplexDatabase)):
            return self.database.get_intersection(start_time, end_time)

        entries = []

        time = start_time
        next_entry = self.database.find_first_after(time)
        while entry.has_intersection(next_entry):
            entries.append(next_entry)
            time = next_entry.end_time

        time = start_time
        previous_entry = self.database.find_last_before(time)
        while entry.has_intersection(previous_entry):
            entries.append(previous_entry)
            time = previous_entry.start_time
        
        return entries
