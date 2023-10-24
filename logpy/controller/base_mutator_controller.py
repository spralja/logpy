from ..model import Entry
from .base_controller import BaseController

from abc import abstractmethod


class BaseMutatorController(BaseController):
    """
    An abstract base class for (read-write) controllers
    """

    @abstractmethod
    def _publish_entry(self, entry: Entry):
        """
            Publishes the entry and mutation

            :param entry: the entry to publish
            :type entry: model.Entry
            :raise NotImplementedError: if the method is not implemented by a
                subclass
        """

    @abstractmethod
    def _retract_entry(self, entry: Entry):
        """
            Deletes the entry and publishes the respective mutation

            :param entry: the entry to be deleted
            :type entry: model.Entry
            :raise NotImplementedError: if the method is not implemented by a
                subclass
        """

    def create_entry(self, entry: Entry):
        """
            Tries to create an Entry

            :param entry: The Entry to create
            :type entry: model.Entry
            :raise KeyError: If there is an entry that conflicts with the entry
                to be created
        """

        conflicts = self.get_intersection(entry.start_time, entry.end_time)

        if conflicts:
            raise KeyError(f'{entry} conflicts with {conflicts}!')

        self._publish_entry(entry)

    def delete_entry(self, entry: Entry):
        """
        Tries to delete the provided entry

        :param entry: The Entry to be deleted
        :type entry: model.Entry
        :raise KeyError: If the entry that is to be deleted does not exist
        """

        if entry != self._find_first_after(entry.start_time):
            raise KeyError(f"{entry} does not exist!")

        self._retract_entry(entry)
