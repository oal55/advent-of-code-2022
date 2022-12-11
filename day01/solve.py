from typing import List

from utils import read_file


def create_elf_calories(input_lines: List[str]) -> List[int]:
    elf_calories: List[int] = []

    sum_for_elf = 0
    for line in input_lines:
        if line == '':
            elf_calories.append(sum_for_elf)
            sum_for_elf = 0
        else:
            sum_for_elf += int(line)

    return elf_calories


def part_1(lines: List[str]) -> int:
    elf_calories = create_elf_calories(lines)
    return max(elf_calories)


def part_2(lines: List[str]) -> int:
    elf_calories = create_elf_calories(lines)
    return sum(sorted(elf_calories, reverse=True)[0:3])


lines = read_file('day01/input.txt')
print('part1', part_1(lines))  # type: ignore
print('part2', part_2(lines))  # type: ignore
