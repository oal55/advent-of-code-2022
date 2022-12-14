from collections import deque
from dataclasses import dataclass, field
from typing import List, Optional

from utils import Point2D, read_file


class Grid:
    directions = [Point2D(1, 0), Point2D(0, 1), Point2D(-1, 0), Point2D(0, -1)]

    def __init__(self, matrix: List[str]) -> None:
        self.matrix: List[List[str]] = [[char for char in row] for row in matrix]
        self.I, self.J = len(matrix), len(matrix[0])

    def __getitem__(self, point: Point2D) -> str:
        return self.matrix[point.i][point.j]

    def __setitem__(self, point: Point2D, value: str) -> None:
        self.matrix[point.i][point.j] = value

    def contains_coordinate(self, point: Point2D) -> bool:
        return (
            (0 <= point.i < self.I) and
            (0 <= point.j < self.J))

    def neighboring_coordinates(self, point: Point2D) -> List[Point2D]:
        all_neighbors = (point + direction for direction in self.directions)
        return [neighbor for neighbor in all_neighbors if self.contains_coordinate(neighbor)]

    def find_all_points(self, key: str) -> List[Point2D]:
        return [Point2D(i, j) for i, row in enumerate(self.matrix) for j, char in enumerate(row) if char == key]

    def __str__(self) -> str:
        return '\n'.join([''.join(row) for row in self.matrix])


@dataclass
class QItem:
    coordinates: Point2D
    distance: int
    parent: Optional['QItem'] = field(default=None)

    def __hash__(self) -> int:
        return hash(self.coordinates)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, QItem):
            return False
        return (self is other) or (self.coordinates == other.coordinates)


def valid_transition(char_from: str, char_to: str) -> bool:
    return ord(char_from) - ord(char_to) > -2


def find_distance(grid: Grid, starting_items: List[QItem], target_point: Point2D) -> int:
    seen_items = set(starting_items)
    Q: deque[QItem] = deque(starting_items)

    while Q:
        item = Q.popleft()
        if item.coordinates == target_point:
            break

        for coords in grid.neighboring_coordinates(item.coordinates):
            next_item = QItem(coords, item.distance + 1, item)
            if (valid_transition(grid[item.coordinates], grid[next_item.coordinates]) and next_item not in seen_items):
                seen_items.add(next_item)
                Q.append(next_item)

    if item.coordinates != target_point:
        return -1
    return item.distance


def part_1(lines: List[str]) -> int:
    grid = Grid(lines)
    start_point, end_point = grid.find_all_points('S')[0], grid.find_all_points('E')[0]
    grid[start_point], grid[end_point] = 'a', 'z'
    return find_distance(grid, [QItem(start_point, 0)], end_point)


def part_2(lines: List[str]) -> int:
    grid = Grid(lines)
    start_point, end_point = grid.find_all_points('S')[0], grid.find_all_points('E')[0]
    grid[start_point], grid[end_point] = 'a', 'z'

    return find_distance(grid, [QItem(point, 0) for point in grid.find_all_points('a')], end_point)


lines = read_file('day12/input.txt')
print('part2', part_1(lines))  # type: ignore
print('part1', part_2(lines))  # type: ignore
