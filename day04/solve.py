from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Range:
    start: int
    end: int

    def contains(self, other: 'Range') -> bool:
        return self.start <= other.start and other.end <= self.end

    def overlaps_with(self, other: 'Range') -> int:
        sml, big = sorted([self, other], key=lambda x: x.start)
        return big.start <= sml.end

    def __post_init__(self) -> None:
        if self.start > self.end:
            print(self.start, self.end)
            raise SystemError('bad range?')


def read_file(file_name: str) -> List[str]:
    with open(file_name, 'r') as inpfile:
        return inpfile.read().splitlines()


def get_ends(range_description: str) -> Tuple[int, int]:
    start, end = range_description.split('-')
    return (
        int(start),
        int(end))


def create_ranges(line: str) -> Tuple[Range, Range]:
    left, right = line.split(',')
    return (
        Range(*get_ends(left)),
        Range(*get_ends(right)))


def part_1(lines: List[str]) -> int:
    num_fully_contained = 0
    for line in lines:
        left, right = create_ranges(line)
        if left.contains(right) or right.contains(left):
            num_fully_contained += 1
    return num_fully_contained


def part_2(lines: List[str]) -> int:
    overlaps = 0
    for line in lines:
        left, right = create_ranges(line)
        if right.overlaps_with(left):
            overlaps += 1
    return overlaps


lines = read_file('input.txt')
print('part1', part_1(lines))
print('part2', part_2(lines))
