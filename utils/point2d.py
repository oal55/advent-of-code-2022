from dataclasses import dataclass


@dataclass
class Point2D:
    i: int
    j: int

    def __add__(self, other: 'Point2D') -> 'Point2D':
        return Point2D(self.i + other.i, self.j + other.j)

    def __iadd__(self, other: 'Point2D') -> 'Point2D':
        return self.__add__(other)

    def __sub__(self, other: 'Point2D') -> 'Point2D':
        return Point2D(self.i - other.i, self.j - other.j)

    def __hash__(self) -> int:
        return hash((self.i, self.j))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point2D):
            return False
        return (
            (self is other) or
            (self.i == other.i and self.j == other.j))

    def __repr__(self) -> str:
        return f'({self.i}, {self.j})'

    # Chebyshev distance
    def distance_to(self, other: 'Point2D') -> int:
        return max(abs(self.i - other.i), abs(self.j - other.j))

    def in_bounding_box(self, north_west: 'Point2D', south_east: 'Point2D') -> bool:
        return (
            (north_west.i <= self.i <= south_east.i) and
            (north_west.j <= self.j <= south_east.j))
