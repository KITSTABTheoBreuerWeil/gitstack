import sys
from enum import IntEnum
from typing import Dict, Iterable, List

from gitstack.exceptions import GitStackException
from gitstack.git import GitInterface
from gitstack.store import StackStore
from gitstack.stack import GitStack

store: StackStore = StackStore('/Users/theobreuer-weil/.stack.txt')
stack: GitStack = GitStack(store=store, git=GitInterface())

class Commands(IntEnum):
    SHOW = 0
    ADD = 1
    DROP = 2
    SELECT = 3

COMMAND_MAPPING: Dict[str, Commands] = {
        'show': Commands.SHOW,
        'add': Commands.ADD,
        'drop': Commands.DROP,
        'select': Commands.SELECT
        }

cmd: Commands

if len(sys.argv) == 1:
    cmd = Commands.SHOW
    args: List[str] = []
else:
    script, cmd_name, *args = sys.argv
    if cmd_name in COMMAND_MAPPING.keys():
        cmd = COMMAND_MAPPING[cmd_name]
    else:
        commands: str = ', '.join(COMMAND_MAPPING.keys())
        command_error: str = f'unrecognised command "{cmd_name}"'
        available: str = 'available commands: {}'.format(commands)
        print(f'{command_error} | {available}')
        sys.exit(1)


def validate_arguments(args: List[str], lower: int=None, upper: int=None,
                       message: str='') -> None:
    numargs: int = len(args)

    if not lower and not upper:
        return

    within_limits: bool = any([
        lower and lower <= numargs,
        upper and numargs > upper
        ])

    if not within_limits:
        raise GitStackException(message)

with stack:
    if cmd == Commands.SHOW:
        validate_arguments(args, 0, message='usage: gitstack show')

    elif cmd == Commands.ADD:
        validate_arguments(args, 0, 1, message='usage: gitstack add [name]')
        if len(args):
            stack.add(args[0])
        else:
            stack.add_current()

    elif cmd == Commands.DROP:
        validate_arguments(args, 0, 1, 'usage: gitstack drop [name]')
        if len(args):
            try:
                index = int(args[0])
            except ValueError:
                raise GitStackException('required integer index')
        else:
            stack.drop_current()

    elif cmd == Commands.SELECT:
        validate_arguments(args, 1, message='usage: gitstack select <index>')
        try:
            index = int(args[0])
        except ValueError:
            raise GitStackException('required integer index')
        stack.select(index)

    print(stack.show())
