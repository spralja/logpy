from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional, Self


@dataclass(frozen=True, order=True)
class Entry:
    start_time: datetime
    end_time: datetime
    category: str
    description: str = ''

    def __post_init__(self):
        """
        Check that the Entry object was initialized with valid start and end 
            times in UTC.

        Raises:
            ValueError: If the start_time or end_time is not in UTC, or if the 
            end_time is not after the start_time.
        """

        if self.start_time.tzinfo != timezone.utc:
            raise ValueError("start_time.tzinfo must be datetime.timezone.utc")

        if self.end_time.tzinfo != timezone.utc:
            raise ValueError("end_time.tzinfo must be datetime.timezone.utc")

        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        
    def intersection(
        self, 
        start_time: datetime, 
        end_time: datetime
    ) -> Optional[Self]:
        """
        Calculate the intersection between this Entry object and a time 
        interval defined by `start_time` and `end_time`. If the intersection 
        is empty, return `None`.

        Args:
            start_time (datetime): The start time of the interval to intersect 
            with.

            end_time (datetime): The end time of the interval to intersect 
            with.

        Returns:
            Optional[Self]: An Entry object representing the intersection 
            between this object and the given time interval, or None if the 
            intersection is empty.
        """

        if start_time.tzinfo != timezone.utc:
            raise ValueError("start_time.tzinfo must be datetime.timezone.utc")

        if end_time.tzinfo != timezone.utc:
            raise ValueError("end_time.tzinfo must be datetime.timezone.utc")

        if end_time <= start_time:
            raise ValueError("end_time must be after start_time")

        if start_time >= self.end_time: 
            return None

        if end_time <= self.start_time: 
            return None

        return Entry(
            max(self.start_time, start_time), 
            min(self.end_time, end_time), 
            self.category, 
            self.description
        )

    @property
    def duration(self) -> timedelta:
        """
        Returns the duration of this event as a timedelta object.
    
        The duration is computed as the difference between the end_time and 
        the start_time of the event. The result is a timedelta object that 
        represents the duration in days, seconds, and microseconds.
    
        Returns:
            A timedelta object representing the duration of the event.
        """
        return self.end_time - self.start_time
