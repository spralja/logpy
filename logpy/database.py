from abc import ABC, abstractmethod


class Database(ABC):
    @abstractmethod
    def find_first_after(self, time: datetime) -> Optional[Entry]:
        """
            Returns the entry with the smallest start_time value that is greater or equal to time or None if there is no Entry
        """

    @abstractmethod
    def find_last_before(self, time: datetime) -> Optional[Entry]:
        """
            Returns the entry with the largest start_time value that is less to time or None if there is no Entry
        """
