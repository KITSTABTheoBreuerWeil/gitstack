import re
from typing import Optional, Match


class Branch:
    """Represents a single branch in a git repository."""

    def __init__(self, name: str, selected: bool=False) -> None:
        self.name = name
        self.selected = selected

    def __repr__(self) -> str:
        return f'Branch({self.name}, {self.selected})'

    def __eq__(self, other) -> bool:
        """Branches compare equal if names match."""
        return self.name == other.name if type(other) == Branch else False


def __get_branch_name(line: str) -> str:
    """Parse a branch name from the end of a string."""
    match: Optional[Match[str]] = re.search('[_\w\-/]+$', line)
    return match.group() if match else ''


def __is_current(branch: str) -> bool:
    """Check if a branch is currently selected, based on the presence of a star
    character on the front of the string.
    """
    return bool(re.match('^\* ', branch))


def branch_object_from_string(line: str) -> Branch:
    """Create Branch object from a string. Expects a string in the format that
    `git branch` generates.
    """
    return Branch(name=__get_branch_name(line), selected=__is_current(line))
