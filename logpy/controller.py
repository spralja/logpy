from .model import Entry

from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone
from typing import Tuple


class Controller(ABC):
    """
    An abstract base class for controllers 
    """

    @abstractmethod
    def _find_first_after(self, dt: datetime) -> Entry:
        """
        Finds the first entry that starts after or at the specfied time 

        Args:
            dt (datetime): The time to search for
        
        Returns:
            Entry: the first entry that starts after or at the specified time
        
        Raises:
            NotImplementedError: If the method is not implemented by a 
            subclass
        """
    
    @abstractmethod
    def _find_last_before(self, dt: datetime) -> Entry:
        """
        Finds that last entry that starts before or at the specified time

        Args:
            dt (datetime): The time to search for

        Returns:
            Entry: the first entry that starts after or at the specified time

        Raises:
            NotImplementedError: If the method is not implemented by a 
            subclass
        """

    def get_intersection(self, start_time, end_time) -> Tuple[Entry]:
        """
        Creates a tuple of entries that intersect with the interval

        Args:
            start_time (datetime): The start time of the interval
            end_time (datetime): The end time of the interval

        Returns:
            A tuple of entry intersections with the interval
        """
        
        # check that start_time is utc
        if start_time.tzinfo != timezone.utc:
            raise ValueError('start_time.tzinfo must be utc')

        # check that end_time is utc
        if end_time.tzinfo != timezone.utc:
            raise ValueError('end_time.tzinfo must be utcc')

        # the list of entries to be returned
        entries = []
        
        # start searching forwards

        # the pointer to the current datetime
        current_dt = start_time

        # the pointer to the current entry
        current_entry = self._find_first_after(current_dt)
        
        while (
            current_entry and 
            current_entry.start_time < end_time
        ):
            entry = current_entry.intersection(start_time, end_time)

            # check that an intersection exists
            if entry:
                entries.append(entry)

            current_dt = current_entry.end_time

            current_entry = self._find_first_after(current_dt)

        # start searching backwards
        current_dt = start_time - timedelta.resolution

        current_entry = self._find_last_before(current_dt)

        while (
            current_entry and
            current_entry.end_time >= start_time
        ):
            entry = current_entry.intersection(start_time, end_time)

            if entry:
                entries.append(entry)

            current_dt = current_entry.start_time - timedelta.resolution

            current_entry = self._find_last_before(current_dt)
        
        # convert the list to a tuple before returning
        return tuple(sorted(entries))
