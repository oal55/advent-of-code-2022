from typing import List

from utils import divide_into_chunks, read_file


def priority_of(char: str) -> int:
    if 'a' <= char <= 'z':
        return ord(char) - ord('a') + 1
    return ord(char) - ord('A') + 27


def find_priority_item_in_sack(sack: str) -> str:
    mid_point = len(sack)//2
    fi_half, se_half = sack[:mid_point], sack[mid_point:]

    intersection = set(fi_half).intersection(set(se_half))
    if len(intersection) != 1:
        print(sack, fi_half, se_half, intersection, sep='\n')
        raise SystemError('Weird intersection for sets?')
    return intersection.pop()


def find_priority_item_in_group(sack: List[str]) -> str:
    fi, se, th, = sack
    intersection = set.intersection(set(fi), set(se), set(th))
    if len(intersection) != 1:
        print(sack, fi, se, th, intersection, sep='\n')
        raise SystemError('Weird intersection for sets?')

    return intersection.pop()


def part_one(rucksacks: List[str]) -> int:
    priority_items = [find_priority_item_in_sack(sack) for sack in rucksacks]
    priorities = [priority_of(item) for item in priority_items]
    return sum(priorities)


def part_two(rucksacks: List[str]) -> int:
    chunks = divide_into_chunks(rucksacks, 3)
    priority_items = [find_priority_item_in_group(chunk) for chunk in chunks]
    priorities = [priority_of(item) for item in priority_items]
    return sum(priorities)


lines = read_file('day03/input.txt')
print('part1', part_one(lines))
print('part2', part_two(lines))
