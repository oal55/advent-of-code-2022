from typing import List, Union

from utils import read_file, divide_into_chunks
from functools import cmp_to_key

import json
import math


def compare_ints(left: int, right: int) -> int:
    return (left > right) - (left < right)


def compare(left: Union[int, list], right: Union[int, list]) -> int:
    if isinstance(left, int) and isinstance(right, int):
        return compare_ints(left, right)

    if isinstance(left, int) and isinstance(right, list):
        return compare([left], right)

    if isinstance(left, list) and isinstance(right, int):
        return compare(left, [right])

    if isinstance(left, list) and isinstance(right, list):
        for l_child, r_child in zip(left, right):
            comparison = compare(l_child, r_child)
            if comparison:
                return comparison
        return compare_ints(len(left), len(right))

    raise SystemError('wopsie')


def part_1(lines: List[str]) -> int:
    tests = divide_into_chunks(lines, 3)
    package_tuples = ((json.loads(t[0]), json.loads(t[1])) for t in tests)
    return sum(i
               for i, [left, right] in enumerate(package_tuples, 1)
               if compare(left, right) == -1)


def part_2(lines: List[str]) -> int:
    dividers = [json.loads("[[2]]"), json.loads("[[6]]")]
    packages_unordered = [json.loads(line) for line in lines if line != '']
    packages_ordered = list(sorted(dividers + packages_unordered, key=cmp_to_key(compare)))

    return math.prod([i for i, package in enumerate(packages_ordered, 1) if package in dividers])


lines = read_file('day13/input.txt')
tests = divide_into_chunks(lines, 3)
print('part1', part_1(lines))
print('part2', part_2(lines))
