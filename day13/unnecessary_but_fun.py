from dataclasses import dataclass
from typing import List, Union

from utils import read_file, divide_into_chunks


@dataclass
class NestedList:
    value: Union[int, List]

    @property
    def is_number(self) -> bool:
        return isinstance(self.value, int)

    @property
    def is_list(self) -> bool:
        return isinstance(self.value, list)

    def __getitem__(self, index: int) -> Union[int, List]:
        if not isinstance(self.value, list):
            raise SystemError('Oh nein my value')
        return self.value[index]

    def __len__(self) -> int:
        if not isinstance(self.value, list):
            raise SystemError('Oh nein my value')
        return len(self.value)

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        if isinstance(self.value, int):
            return str(self.value)

        children = [str(element) for element in self.value]
        return f'[{", ".join(children)}]'

    def __lt__(self, other: 'NestedList') -> bool:
        return NestedList.compare(self, other) == -1

    @staticmethod
    def compare_ints(left: int, right: int) -> int:
        return (left > right) - (left < right)

    @staticmethod
    def compare(left: 'NestedList', right: 'NestedList') -> int:
        if left.is_number and right.is_number:
            return NestedList.compare_ints(left.value, right.value)  # type: ignore
        if left.is_number and right.is_list:
            return NestedList.compare(NestedList([left]), right)
        if left.is_list and right.is_number:
            return NestedList.compare(left, NestedList([right]))
        if left.is_list and right.is_list:
            for l_child, r_child in zip(left.value, right.value):  # type: ignore
                comparison = NestedList.compare(l_child, r_child)
                if comparison:
                    return comparison
            return NestedList.compare_ints(len(left), len(right))

        raise SystemError('whapzie')

    @classmethod
    def _from_reverse_tokens(cls, reversed_tokens: List[str]) -> 'NestedList':
        this = NestedList([])
        while reversed_tokens:
            token = reversed_tokens.pop()
            if token == '[':
                this.value.append(NestedList._from_reverse_tokens(reversed_tokens))  # type: ignore
            elif token.isdigit():
                this.value.append(NestedList(int(token)))  # type: ignore
            elif token == ']':
                return this
            else:
                raise SystemError(f'Unrecognized token: {token}')
        raise SystemError('Dead end. Huhahahihihuhohohia')

    @classmethod
    def _tokenize(cls, raw: str) -> List[str]:
        chars_to_replace = {
            '[': ' [ ',
            ']': ' ] ',
            ',': ' '
        }
        processed = raw
        for target, destination in chars_to_replace.items():
            processed = processed.replace(target, destination)
        return [token for token in processed.split(' ') if token]

    @classmethod
    def parse_str(cls, raw: str) -> 'NestedList':
        reversed_tokens = list(reversed(cls._tokenize(raw)))
        if reversed_tokens.pop() != '[':
            raise SystemError(f'Bad str: {raw}')
        return cls._from_reverse_tokens(reversed_tokens)


def part_1(lines: List[str]) -> int:
    tests = divide_into_chunks(lines, 3)
    package_tuples = ((NestedList.parse_str(t[0]), NestedList.parse_str(t[1])) for t in tests)
    return sum(i
               for i, [left, right] in enumerate(package_tuples, 1)
               if left < right)


def part_2(lines: List[str]) -> int:
    packages = list(sorted([NestedList.parse_str(line) for line in lines if line != '']))
    divider_1 = NestedList.parse_str("[[2]]")
    divider_2 = NestedList.parse_str("[[6]]")

    return (
        (len([p for p in packages if p < divider_1]) + 1) *
        (len([p for p in packages if p < divider_2]) + 2))


lines = read_file('day13/input.txt')

print('part1', part_1(lines))
print('part2', part_2(lines))
