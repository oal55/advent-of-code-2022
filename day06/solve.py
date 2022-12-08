from typing import Dict

from collections import deque


class Window:

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.char_to_count: Dict[str, int] = {}
        self.q_characters: deque = deque()

    def number_of_unique_characters(self) -> int:
        return len(self.char_to_count)

    def push(self, char: str) -> None:
        if (len(self.q_characters) == self.capacity):
            oldest_element = self.q_characters.popleft()
            self.char_to_count[oldest_element] -= 1
            if self.char_to_count[oldest_element] == 0:
                self.char_to_count.pop(oldest_element)

        self.q_characters.append(char)
        self.char_to_count[char] = self.char_to_count.get(char, 0) + 1


def read_file(file_name: str) -> str:
    with open(file_name, 'r') as inpfile:
        return inpfile.read()


def find_start_of_packet(packet_line: str, num_unique_chars: int) -> int:
    window = Window(capacity=num_unique_chars)
    for i, character in enumerate(packet_line):
        window.push(character)
        if window.number_of_unique_characters() == num_unique_chars:
            return i + 1

    raise SystemError(f'never saw {num_unique_chars} unique characters in string: {packet_line}')


def part_1(line: str) -> int:
    return find_start_of_packet(line, 4)


def part_2(line: str) -> int:
    return find_start_of_packet(line, 14)


line = read_file('input.txt')
print('part1', part_1(line))  # type: ignore
print('part2', part_2(line))  # type: ignore
