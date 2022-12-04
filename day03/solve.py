from typing import List


def read_file(file_name: str) -> List[str]:
    with open(file_name, 'r') as inpfile:
        return inpfile.read().splitlines()


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


def divide_chunks(items: List, chunk_size: int) -> List[List]:
    return [
        items[i:i + chunk_size]
        for i in range(0, len(items), chunk_size)]


def part_one(rucksacks: List[str]) -> int:
    priority_items = [find_priority_item_in_sack(sack) for sack in rucksacks]
    priorities = [priority_of(item) for item in priority_items]
    return sum(priorities)


def part_two(rucksacks: List[str]) -> int:
    chunks = divide_chunks(rucksacks, 3)
    priority_items = [find_priority_item_in_group(chunk) for chunk in chunks]
    priorities = [priority_of(item) for item in priority_items]
    return sum(priorities)


lines = read_file('input.txt')
chunks = divide_chunks(lines, 3)
# q = part_one(lines)
q = part_two(lines)
print(q)
