from typing import List


def read_file(file_name: str) -> List[str]:
    with open(file_name, 'r') as inpfile:
        return inpfile.read().splitlines()


def part_1(lines: List[str]) -> None:
    pass


def part_2(lines: List[str]) -> None:
    pass


lines = read_file('input.txt')
print('part1', part_1(lines))  # type: ignore
print('part2', part_2(lines))  # type: ignore
