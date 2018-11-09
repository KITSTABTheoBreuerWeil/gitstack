from typing import Iterable, List, Optional 
from subprocess import run, PIPE

from .branch import Branch, branch_object_from_string
from .exceptions import GitStackException

# exit code for successful operations
SUCCESS: int = 0


def _raw_branches() -> str:
    """Get output of `git branch` command."""
    return run(['git', 'branch'], stdout=PIPE).stdout.decode()


def _is_selected(branch: Branch) -> bool:
    """Check if branch is selected."""
    return branch.selected


class GitInterface:
    """Interface to git command line. Used to get information about active
    branches and to check branches out.
    """

    def branches(self) -> Iterable[Branch]:
        """Get all branches as Branch objects."""
        return map(branch_object_from_string, _raw_branches().split('\n'))

    def current_branch(self) -> Branch:
        """Get Branch object corresponding to current branch."""
        branches: List[Branch] = list(filter(_is_selected, self.branches()))
        
        if len(branches) != 1:
            raise GitStackException('found more than 1 master branch')

        return branches.pop()

    def have_branch(self, branch: Branch) -> bool:
        """Check if we track a branch corresponding to a branch object."""
        return any(map(lambda b: b.name == branch.name, self.branches()))

    @staticmethod
    def checkout(branch: Branch) -> bool:
        """Checkout a branch, returning boolean indicating success."""
        return run(['git', 'checkout', branch.name]).returncode == SUCCESS
