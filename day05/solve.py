from dataclasses import dataclass, field
from typing import ClassVar, Dict, List

import re


@dataclass
class Operation:
    operation_extractor: ClassVar[re.Pattern] = re.compile('(move)|(from)|(to)')
    raw_operation: str
    amount: int = field(default=0, init=False)
    source_stack: str = field(default='', init=False)
    target_stack: str = field(default='', init=False)

    def __post_init__(self) -> None:
        amount, src, dst = Operation.operation_extractor.sub('', self.raw_operation).split()
        self.amount = int(amount)
        self.source_stack = src
        self.target_stack = dst


def read_file(file_name: str) -> List[str]:
    with open(file_name, 'r') as inpfile:
        return inpfile.read().splitlines()


def create_initial_stacks(stack_lines: List[str]) -> Dict[str, List[str]]:
    largest_stack_num = int(stack_lines.pop().split()[-1])
    stacks: Dict[str, List[str]] = {str(i): [] for i in range(1, largest_stack_num + 1)}
    item_pattern = re.compile(r"\[(\w)\]")
    for line in reversed(stack_lines):
        for match in item_pattern.finditer(line):
            stacks[str(match.start() // 4 + 1)].append(match.group(1))
    return stacks


def apply_operation_part_2(op: Operation, stacks: Dict[str, List[str]]) -> None:
    stacks[op.target_stack].extend(stacks[op.source_stack][-op.amount:])
    stacks[op.source_stack] = stacks[op.source_stack][:-op.amount]


def apply_operation_part_1(op: Operation, stacks: Dict[str, List[str]]) -> None:
    stacks[op.target_stack].extend(reversed(stacks[op.source_stack][-op.amount:]))
    stacks[op.source_stack] = stacks[op.source_stack][:-op.amount]


def read_stack_tops(stacks: Dict[str, List[str]]) -> str:
    return ''.join([group[-1] if group else '' for group in stacks.values()])


def part_1(lines: List[str]) -> str:
    image_end_index = lines.index('')
    stacks = create_initial_stacks(lines[:image_end_index])
    operations = [Operation(line) for line in lines[image_end_index + 1:]]
    for operation in operations:
        apply_operation_part_1(operation, stacks)
    return read_stack_tops(stacks)


def part_2(lines: List[str]) -> str:
    image_end_index = lines.index('')
    stacks = create_initial_stacks(lines[:image_end_index])
    operations = [Operation(line) for line in lines[image_end_index + 1:]]
    for operation in operations:
        apply_operation_part_2(operation, stacks)
    return read_stack_tops(stacks)


lines = read_file('dinput.txt')

print('part1', part_1(lines))
print('part2', part_2(lines))
