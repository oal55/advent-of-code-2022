from dataclasses import dataclass, field
from typing import Callable, ClassVar, Dict, List, Set

from utils import divide_into_chunks, read_file

import math
import re


@dataclass
class MonkaTest:
    divisible_by: int
    pass_id: int
    fail_id: int

    def run(self, value: int) -> int:
        if value % self.divisible_by:
            return self.fail_id
        return self.pass_id


@dataclass
class Monka:
    number_pattern: ClassVar[re.Pattern] = re.compile(r'(\d+)')
    id: int
    items: List[int]
    operation: str
    test: MonkaTest
    num_items_processed: int = field(init=False, default=0)

    @classmethod
    def bad_monka(cls, chunk: List[str]) -> None:
        raise SyntaxError(f'Bad Monka. {chunk}')

    @classmethod
    def validate(cls, chunk: List[str]) -> None:
        if not (chunk[0].startswith('Monkey ') and
                chunk[1].startswith('  Starting items:') and
                chunk[2].startswith('  Operation: ') and
                chunk[3].startswith('  Test: divisible by') and
                chunk[4].startswith('    If true: throw to monkey') and
                chunk[5].startswith('    If false: throw to monkey')):
            cls.bad_monka(chunk)

    @classmethod
    def get_int(cls, line: str) -> int:
        if match := cls.number_pattern.search(line):
            return int(match.group(1))
        raise SystemError(f'elp: {line}')

    @classmethod
    def from_monka_chunk(cls, chunk: List[str]) -> 'Monka':
        """Expects chunk size of at least 6. All later items after index 5 in chunk are ignored"""
        cls.validate(chunk)

        raw_operation = chunk[2][len('  Operation: '):].replace('=', ':=')
        return Monka(
            id=cls.get_int(chunk[0]),
            items=[int(match.group(1)) for match in Monka.number_pattern.finditer(chunk[1])],
            operation=f'({raw_operation})',
            test=MonkaTest(cls.get_int(chunk[3]), cls.get_int(chunk[4]), cls.get_int(chunk[5])))

    def __init__(self, id: int, items: List[int], operation: str, test: MonkaTest) -> None:
        self.id = id
        self.items = items
        self.operation = operation
        self.test = test
        self.num_items_processed = 0

    # empty items, and report result
    def process_items(self, worry_function: Callable[[int], int]) -> Dict[int, List[int]]:
        monkas_to_items: Dict[int, List[int]] = {
            self.test.pass_id: [],
            self.test.fail_id: []
        }

        for item in self.items:
            next_value = worry_function(self.process_item(item))
            monkas_to_items[self.test.run(next_value)].append(next_value)

        self.num_items_processed += len(self.items)
        self.items = []
        return monkas_to_items

    def process_item(self, item: int) -> int:
        old = item  # noqa
        return eval(self.operation)

    def receive_items(self, items: List[int]) -> None:
        self.items.extend(items)


def instantiate_monkas(lines: List[str]) -> Dict[int, Monka]:
    monka_chunks = divide_into_chunks(lines, 7)
    monkas = [Monka.from_monka_chunk(chunk) for chunk in monka_chunks]
    return {monka.id: monka for monka in monkas}


def play_round(monkas: Dict[int, Monka], worry_function: Callable[[int], int]) -> None:
    for monka in monkas.values():
        monka_id_to_items = monka.process_items(worry_function)
        for monka_id, items in monka_id_to_items.items():
            monkas[monka_id].receive_items(items)


def part_1(lines: List[str]) -> int:
    monkas = instantiate_monkas(lines)

    for _ in range(20):
        play_round(monkas, lambda x: x//3)

    sorted_monkas = sorted(monkas.values(), key=lambda x: x.num_items_processed, reverse=True)
    return sorted_monkas[0].num_items_processed * sorted_monkas[1].num_items_processed


def get_prime_factors(number: int) -> Set[int]:
    factors: Set[int] = set()
    while number % 2 == 0:
        factors.add(2)
        number //= 2

    for i in range(3, int(math.sqrt(number)) + 1, 2):
        while (number % i == 0):
            factors.add(i)
            number //= i

    return factors


def part_2(lines: List[str]) -> int:
    monkas = instantiate_monkas(lines)
    primes = get_prime_factors(math.prod(monka.test.divisible_by for monka in monkas.values()))
    mod = math.prod(primes)

    for _ in range(10_000):
        play_round(monkas, lambda x: x % mod)

    sorted_monkas = sorted(monkas.values(), key=lambda x: x.num_items_processed, reverse=True)
    return sorted_monkas[0].num_items_processed * sorted_monkas[1].num_items_processed


lines = read_file('day11/input.txt')
print('part1', part_1(lines))  # type: ignore
print('part2', part_2(lines))  # type: ignore
