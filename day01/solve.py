from typing import List


def read_file(file_name: str) -> List[str]:
    with open(file_name, 'r') as inpfile:
        return inpfile.readlines()


def create_elf_calories(input_lines: List[str]) -> List[List[int]]:
    elf_calories: List[List[int]] = []
    running_ints: List[int] = []

    for line in input_lines:
        if line.strip() == '':
            elf_calories.append(running_ints)
            running_ints = []
        else:
            running_ints.append(int(line))

    return elf_calories


lines = read_file('./input.txt')
elf_calories = create_elf_calories(lines)

sums = [sum(calories) for calories in elf_calories]
print(sum(sorted(sums, reverse=True)[0:3]))
