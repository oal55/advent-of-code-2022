from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from utils import divide_into_chunks, read_file


class OpName(Enum):
    NOOP = 0
    ADDX = 1


@dataclass
class Operation:
    remaining_cycles: int
    name: OpName
    arg: int

    @classmethod
    def from_line(cls, operation_description: str) -> 'Operation':
        if operation_description == 'noop':
            return Operation(1, OpName.NOOP, 0)

        op_name, arg = operation_description.split(' ')
        if op_name == 'addx':
            return Operation(2, OpName.ADDX, int(arg))

        raise SystemError('I am confusion?!@#')


class CPU:

    def __init__(self, operations: List[Operation]) -> None:
        self.operations: List[Operation] = list(reversed(operations))
        self.clock = 0
        self.register_x = 1
        self.current_operation: Optional[Operation] = Operation(1, OpName.NOOP, 0)
        self.last_drawn_char = '.'

    def tick(self) -> bool:
        if not self.current_operation:
            return False

        self.current_operation.remaining_cycles -= 1
        self.clock += 1

        if not self.current_operation.remaining_cycles:
            self.register_x += self.current_operation.arg
            self.current_operation = self._next_op()
        return True

    def _next_op(self) -> Optional[Operation]:
        if self.operations:
            return self.operations.pop()
        return None


def read_file(file_name: str) -> List[str]:
    with open(file_name, 'r') as inpfile:
        return inpfile.read().splitlines()


def interesting_cycle(clock: int) -> bool:
    return (clock - 20) % 40 == 0


def calculate_signal_strength(cpu: CPU) -> int:
    return cpu.clock * cpu.register_x


def part_1(lines: List[str]) -> int:
    cpu = CPU([Operation.from_line(line) for line in lines])
    signal_strength = 0

    while cpu.tick():
        if interesting_cycle(cpu.clock):
            signal_strength += calculate_signal_strength(cpu)

    return signal_strength


def get_last_drawn(cpu: CPU) -> str:
    row_index = (cpu.clock - 1) // 40
    if abs(cpu.clock - 1 - row_index * 40 - cpu.register_x) < 2:
        return '#'
    return '.'


def part_2(lines: List[str]) -> str:
    cpu = CPU([Operation.from_line(line) for line in lines])

    chars: List[str] = []
    while cpu.tick():
        chars.append(get_last_drawn(cpu))

    rows = divide_into_chunks(chars, 40)
    return '\n'.join([''.join(row) for row in rows])


lines = read_file('day10/input.txt')
print('part1', part_1(lines))
print('part2', part_2(lines), sep=':\n')

"""

###..#.....##..####.#..#..##..####..##..
#..#.#....#..#.#....#.#..#..#....#.#..#.
#..#.#....#....###..##...#..#...#..#....
###..#....#.##.#....#.#..####..#...#.##.
#....#....#..#.#....#.#..#..#.#....#..#.
#....####..###.#....#..#.#..#.####..###.

"""
