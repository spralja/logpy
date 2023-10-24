from .entry import Entry

from dataclasses import dataclass


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
