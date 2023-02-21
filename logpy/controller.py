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
        Creates a sorted tuple of entries that intersect with the interval

        Args:
            start_time (datetime): The start time of the interval (must be utc)
            end_time (datetime): The end time of the interval (must be utc)

        Returns:
            A sorted tuple of entry intersections with the interval
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


class MutatorController(Controller):
    @abstractmethod
    def _publish_entry(self, entry: Entry):
        """
            Publishes the entry and mutation

            Args:
                entry: the entry to publish

            Raises:
                NotImplementedError: if the method is not implemented by a 
                subclass
        """
    
    def create_entry(self, entry: Entry):
        """
            Tries to create an Entry

            Args:
                entry: the entry to create
            
            Raises:
                KeyError: If there entry that conflicts with the entry to be 
                created
        """

        conflicts = self.get_intersection(entry.start_time, entry.end_time)

        if conflicts:
            raise KeyError(f'{entry} conflicts with {conflicts}!')
        
        self._publish_entry(entry)
    