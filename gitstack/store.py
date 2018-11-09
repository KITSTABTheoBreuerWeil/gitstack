from operator import attrgetter
from os import path
from typing import Iterable, Optional, Tuple, Match
from functools import wraps

from .branch import Branch


class StackStore:
    """Handles persistence of the stack. Saves and retrieves information in a
    text file.
    """

    def __init__(self, filepath: str, sep: str='\n') -> None:
        self.filepath: str = filepath
        self.sep: str = sep

    def __open(self) -> str:
        """Contents of the file at the given filepath, or empty string."""
        if path.exists(self.filepath):
            with open(self.filepath) as source:
                return source.read()

        return ''

    def __read_raw(self) -> Iterable[str]:
        """Read store file and split by lines, removing any blank lines in the 
        process. If the file cannot be opened for whatever reason, return an 
        empty array.
        """
        raw: str = self.__open()
        return filter(bool, raw.split(self.sep)) if raw else []

    def read(self) -> Iterable[Branch]:
        """Read store file and return as list of Branch objects."""
        return map(lambda name: Branch(name=name), self.__read_raw())

    def __branches_to_text(self, branches: Iterable[Branch]) -> str:
        """Convert branches to a delimited string."""
        return self.sep.join(map(lambda b: b.name, branches))

    def write(self, stack: Iterable[Branch]) -> None:
        """Write an array to the given filepath."""
        with open(self.filepath, 'w') as destination:
            destination.write(self.__branches_to_text(stack))
