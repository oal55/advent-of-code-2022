from typing import List

from .point2d import Point2D


def read_file(file_name: str) -> List[str]:
    with open(file_name, 'r') as inpfile:
        return inpfile.read().splitlines()


def divide_into_chunks(items: List, chunk_size: int) -> List[List]:
    return [
        items[i:i + chunk_size]
        for i in range(0, len(items), chunk_size)]


__all__ = ['Point2D']
