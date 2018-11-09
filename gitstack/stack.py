from typing import Iterable, List, Type
from types import TracebackType

from .branch import Branch
from .exceptions import GitStackException
from .git import GitInterface
from .store import StackStore


class GitStack:
    def __init__(self, store: StackStore, git: GitInterface) -> None:
        self.store = store
        self.git = git
        self.stack: List[Branch] = []

    def __enter__(self) -> None:
        self.stack = list(self.store.read())

    def __exit__(self, exc_type: Type, exc_value: Exception, 
                 exc_tb: TracebackType) -> bool:
        if exc_value:
            print(str(exc_value))

        self.__write()
        return True

    def __prune(self) -> Iterable[Branch]:
        return filter(self.git.have_branch, self.stack)

    def __write(self) -> None:
        self.store.write(self.__prune())

    def add(self, branch: str) -> None:
        branch_object: Branch = Branch(name=branch)

        if not self.git.have_branch(branch_object):
          raise GitStackException('branch does not exist') from None

        if branch in self.stack:
          raise GitStackException('branch already tracked') from None

        self.stack.append(branch_object)

    def add_current(self) -> None:
        current: Branch = self.git.current_branch()
 
        if current:
            self.add(current.name)

    def drop(self, index: int) -> None:
        try:
            del self.stack[index]
            self.__write()
        except IndexError:
            raise GitStackException('not tracking branch') from None

    def drop_current(self) -> None:
        current: Branch = self.git.current_branch()

        if current:
            self.drop(self.stack.index(current))

    def select(self, index: int) -> None:
        self.git.checkout(self.stack[index])

    def __tracked_branches(self) -> Iterable[Branch]:
        return sorted(
                [b for b in self.git.branches() if b in self.stack],
                key=lambda b: self.stack.index(b)
                )

    @staticmethod
    def __build_line(index: int, branch: Branch) -> str:
        marker: str = '├' if branch.selected else '│'
        return f'{marker} {index:>3}: {branch.name}'

    def show(self) -> str:
        to_line = lambda pair: self.__build_line(*pair)
        return '\n'.join(map(to_line, enumerate(self.__tracked_branches())))
