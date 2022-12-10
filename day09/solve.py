from dataclasses import dataclass
from typing import List


@dataclass
class Point2D:
    i: int
    j: int

    def __add__(self, other: 'Point2D') -> 'Point2D':
        return Point2D(self.i + other.i, self.j + other.j)

    def __iadd__(self, other: 'Point2D') -> 'Point2D':
        return self.__add__(other)

    def __sub__(self, other: 'Point2D') -> 'Point2D':
        return Point2D(self.i - other.i, self.j - other.j)

    def __hash__(self) -> int:
        return hash((self.i, self.j))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point2D):
            return False
        return (
            (self is other) or
            (self.i == other.i and self.j == other.j))

    def __repr__(self) -> str:
        return f'({self.i}, {self.j})'

    def distance_to(self, other: 'Point2D') -> int:
        return max(abs(self.i - other.i), abs(self.j - other.j))


DIRECTIONS = {
    'L': Point2D(0, -1),
    'U': Point2D(-1, 0),
    'R': Point2D(0, 1),
    'D': Point2D(1, 0)
}


@dataclass
class Move:
    direction: Point2D
    amount: int

    @classmethod
    def from_input_line(cls, line: str) -> 'Move':
        direction, amount = line.split(' ')
        return Move(DIRECTIONS[direction], int(amount))

    @classmethod
    def from_input_lines(cls, lines: List[str]) -> List['Move']:
        return [Move.from_input_line(line) for line in lines]


class Rope:
    def __init__(self, size: int) -> None:
        self.knots = [Point2D(0, 0) for _ in range(size)]

    @property
    def head(self) -> Point2D:
        return self.knots[0]

    @property
    def tail(self) -> Point2D:
        return self.knots[-1]

    def _squish_number(self, coordinate: int) -> int:
        if coordinate > 0:
            return 1
        if coordinate < 0:
            return -1
        return 0

    def _squish_point(self, point: Point2D) -> Point2D:
        return Point2D(self._squish_number(point.i), self._squish_number(point.j))

    def pull(self, direction: Point2D) -> None:
        self.knots[0] += direction
        for i_prev_moved, i_cur in zip(range(0, len(self.knots)), range(1, len(self.knots))):
            if self.knots[i_prev_moved].distance_to(self.knots[i_cur]) > 1:
                self.knots[i_cur] += self._squish_point(self.knots[i_prev_moved] - self.knots[i_cur])


def read_file(file_name: str) -> List[str]:
    with open(file_name, 'r') as inpfile:
        return inpfile.read().splitlines()


def count_tail_positions_of_rope(rope: Rope, moves: List[Move]) -> int:
    visited_by_tail = {rope.tail}
    for move in moves:
        for _ in range(move.amount):
            rope.pull(move.direction)
            visited_by_tail.add(rope.tail)

    return len(visited_by_tail)


def part_1(lines: List[str]) -> int:
    return count_tail_positions_of_rope(
        Rope(2),
        Move.from_input_lines(lines))


def part_2(lines: List[str]) -> int:
    return count_tail_positions_of_rope(
        Rope(10),
        Move.from_input_lines(lines))


lines = read_file('input.txt')
print('part1', part_1(lines))
print('part2', part_2(lines))
