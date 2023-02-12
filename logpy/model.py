from dataclasses import dataclass
from datetime import datetime
from typing import Self


@dataclass(frozen=True)
class Entry:
    start_time: datetime
    end_time: datetime
    category: str
    description: str = ''

    def __post_init__(self):
        if self.end_time <= self.start_time:
            raise ValueError("End time must be after start time")

    def has_intersection(self, other: Self) -> bool:
        """
        Returns True if there is an intersection between self and other and False otherwise
        """
        return self.start_time < other.end_time and self.end_time > other.start_time
