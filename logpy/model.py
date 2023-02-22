from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional, Self, Union


@dataclass(frozen=True, order=True)
class Entry:
    """
    Frozen dataclass for log entries

    :param start_time: the start time of the entry (must be utc)
    :type start_time: datetime.datetime
    :param end_time: the end time of the entry (must be utc)
    :type end_time: datetime.datetime
    :param category: the category of the entry
    :type category: str
    :param description: the description of the entry, defaults to ''
    :type description: str
    :raise ValueError: if the `start_time` or `end_time` are not UTC
    """
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

        :param start_time: The start time of the inerval to intersect with 
            (must be utc)
        :type start_time: datetime.datetime
        :param end_time: The end time of the interval to intersect with
            (must be utc)
        :type end_time: datetime.datetime
        :raise ValueError: if the `start_time` or `end_time` are not UTC
        :return: An Entry object representing the intersection between this 
            object and the given time interval, or None if the intersection
            is empty.
        :rtype: Entry or None
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
        The duration of this event as a timedelta object.
    
        The duration is computed as the difference between the end_time and 
        the start_time of the event. The result is a timedelta object that 
        represents the duration in days, seconds, and microseconds.
    
        :return: the duration of the event
        :rtype: datetime.timedelta
        """
        return self.end_time - self.start_time


@dataclass(frozen=True)
class Mutation:
    """
    Forzen dataclass representing a mutation (an action that modifies the log)
    
    :param mutation_class: the class of the mutation
    :type mutation_class: 'creator' or 'destoryer'
    :param entry: The entry that is created or destoryerd
    :type entry: model.Entry
    :raise ValueError: if `mutation_class` is any other value 
        (not 'creator' nor 'destroyer')
    """
    mutation_class: str
    entry: Entry

    def __post_init__(self):
        if self.mutation_class not in {'creator', 'destroyer'}:
            raise ValueError(
                'mutation_class must be \'creator\' or \'destroyer\''
            )
