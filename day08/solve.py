from typing import List, Set, Tuple
from dataclasses import dataclass

import math


@dataclass
class Point2D:
    i: int
    j: int

    def __add__(self, other: 'Point2D') -> 'Point2D':
        return Point2D(self.i + other.i, self.j + other.j)

    def in_bounding_box(self, north_west: 'Point2D', south_east: 'Point2D') -> bool:
        return (
            (north_west.i <= self.i <= south_east.i) and
            (north_west.j <= self.j <= south_east.j))


def read_file(file_name: str) -> List[List[int]]:
    with open(file_name, 'r') as inpfile:
        str_lines = inpfile.read().splitlines()

    return [[int(char) for char in row] for row in str_lines]


def get_visibility_of_array_from_left(trees: List[int]) -> Set[int]:
    max_length_so_far = -1
    indices: Set[int] = set()
    for i, tree_length in enumerate(trees):
        if tree_length > max_length_so_far:
            max_length_so_far = tree_length
            indices.add(i)
    return indices


def get_visibility_of_array(trees: List[int]) -> Set[int]:
    len_trees = len(trees)
    visible_trees_from_left = get_visibility_of_array_from_left(trees)
    visible_trees_from_rite = {
        (len_trees - i - 1)
        for i in get_visibility_of_array_from_left(list(reversed(trees)))}

    return set.union(visible_trees_from_left, visible_trees_from_rite)


def transpose(matrix: List[List]) -> List[List]:
    if not matrix:
        return []
    num_cols = len(matrix[0])
    return [[row[i] for row in matrix] for i in range(num_cols)]


def get_horizontal_visibility_of_array_matrix(forest: List[List[int]]) -> Set[Tuple[int, int]]:
    visible_trees: Set[Tuple[int, int]] = set()

    for i, trees in enumerate(forest):
        linear_indices = get_visibility_of_array(trees)
        for index in linear_indices:
            visible_trees.add((i, index))

    return visible_trees


def part_1(forest: List[List[int]]) -> Set[Tuple[int, int]]:
    visible_trees_from_sides = get_horizontal_visibility_of_array_matrix(forest)
    visible_trees_from_updown = {
        (y, x) for x, y in get_horizontal_visibility_of_array_matrix(transpose(forest))}

    return set.union(
        visible_trees_from_sides,
        visible_trees_from_updown)


def count_in_direction(forest: List[List[int]], from_location: Point2D, direction: Point2D) -> int:
    reference_value = forest[from_location.i][from_location.j]
    current_location = from_location + direction
    visible_tree_count = 0

    while (current_location.in_bounding_box(NORTH_WEST, SOUTH_EAST)):
        visible_tree_count += 1
        if forest[current_location.i][current_location.j] >= reference_value:
            break
        current_location += direction

    return visible_tree_count


def part_2(forest: List[List[int]]) -> int:
    directions = [Point2D(1, 0), Point2D(0, 1), Point2D(-1, 0), Point2D(0, -1)]
    best_score = (0-0)
    for i in range(I):
        for j in range(J):
            score = math.prod([
                count_in_direction(forest, Point2D(i, j), direction)
                for direction in directions])

            best_score = max(score, best_score)

    return best_score


forest = read_file('input.txt')
NORTH_WEST, SOUTH_EAST = Point2D(0, 0), Point2D(len(forest) - 1, len(forest[0]) - 1)
I, J = len(forest), len(forest[0])

print('part1', len(part_1(forest)))
print('part2', part_2(forest))
