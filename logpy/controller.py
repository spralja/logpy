from .model import Entry

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List


class Controller(ABC):
    """
    An abstract base class for controllers 
    """

    @abstractmethod
    def _find_first_after(dt: datetime) -> Entry:
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
    def _find_last_before(dt: datetime) -> Entry:
        """
        Finds that last entry that starts before the specified time

        Args:
            dt (datetime): The time to search for

        Returns:
            Entry: the first entry that starts after or at the specified time

        Raises:
            NotImplementedError: If the method is not implemented by a 
            subclass
        """

    def get_intersection(self, start_time, end_time) -> List[Entry]:
        """
        Creates a list of entries that intersect with the interval

        Args:
            start_time (datetime): The start time of the interval
            end_time (datetime): The end time of the interval

        Returns:
            A list of entry intersections with the interval
        """