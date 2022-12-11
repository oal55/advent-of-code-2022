from collections import deque
from enum import Enum
from pathlib import PurePath
from typing import List, Optional

from utils import read_file

import re


class NodeType(Enum):
    DIRECTORY = 0
    FILE = 1


class Node:
    def __init__(self, name: str, type_: NodeType, parent: Optional['Node'], size: int) -> None:
        self.name: str = name
        self.type: NodeType = type_
        self.parent: Optional['Node'] = parent
        self.size: int = size
        self.total_size: int = 0
        self.children: dict[str, 'Node'] = {}
        if type_ == NodeType.DIRECTORY and size:
            raise SystemError('directory with non-zero size')

    def absolute_path(self) -> str:
        parent_names = [parent.name for parent in reversed(self.all_parents())]
        return str(PurePath('/', '/'.join(parent_names), self.name))

    def all_parents(self) -> List['Node']:
        parent = self.parent
        all_parents = []
        while parent:
            all_parents.append(parent)
            parent = parent.parent
        return all_parents

    def get_or_create_child(self, name: str, node_type: NodeType, size: int) -> 'Node':
        if (name == '/'):
            return self

        if name not in self.children:
            self.children[name] = Node(name, node_type, self, size)

        return self.children[name]


class FileTree:

    def __init__(self) -> None:
        self.root = Node('', NodeType.DIRECTORY, None, 0)
        self.current_dir: 'Node' = self.root

    def mkdir(self, name: str) -> None:
        self.current_dir.get_or_create_child(name, NodeType.DIRECTORY, 0)

    def touch_file(self, name: str, size: int) -> None:
        self.current_dir.get_or_create_child(name, NodeType.FILE, size)

    def cd(self, path_str: str) -> None:
        if path_str == '..':
            if self.current_dir.parent is None:
                raise SystemError('Stairway to heaven')
            self.current_dir = self.current_dir.parent
            return

        path = PurePath(path_str)
        iter_node = self.root if path.is_absolute() else self.current_dir
        for path_segment in path.parts:
            iter_node = iter_node.get_or_create_child(path_segment, NodeType.DIRECTORY, 0)

        self.current_dir = iter_node

    def pwd(self) -> str:
        return self.current_dir.absolute_path()

    def collect_all_nodes(self) -> List[Node]:
        node_q: deque[Node] = deque()
        node_q.append(self.root)

        all_nodes = []
        while node_q:
            node = node_q.pop()
            all_nodes.append(node)
            if node.type == NodeType.DIRECTORY:
                for child in node.children.values():
                    node_q.append(child)

        return all_nodes


def process_ls_output(file_tree: 'FileTree', commands: List[str]) -> None:
    while commands and not commands[-1].startswith('$'):
        output_line = commands.pop()
        if output_line.startswith('dir'):
            file_tree.mkdir(output_line[4:])
        elif re.fullmatch(r'\d+ \S+', output_line):
            size_str, name = output_line.split(' ')
            file_tree.touch_file(name, int(size_str))
        else:
            SystemError('ls output format not recognized')


def build_file_tree(commands_and_outputs: List[str]) -> 'FileTree':
    file_tree = FileTree()

    cd_pattern = re.compile(r'\$ cd (.*)')
    while commands_and_outputs:
        cmd = commands_and_outputs.pop()
        if cd_match := cd_pattern.match(cmd):
            file_tree.cd(cd_match.group(1))
        elif cmd == '$ ls':
            process_ls_output(file_tree, commands_and_outputs)
        else:
            print(cmd)
            raise SystemError('debug me')

    return file_tree


def calculate_node_sizes(node: Node) -> int:
    if node.type == NodeType.FILE:
        node.total_size = node.size
        return node.size

    for child in node.children.values():
        node.total_size += calculate_node_sizes(child)

    return node.total_size


def part_1(lines: List[str]) -> int:
    tree = build_file_tree(list(reversed(lines)))
    calculate_node_sizes(tree.root)
    nodes = tree.collect_all_nodes()
    return sum(
        node.total_size
        for node in nodes
        if node.type == NodeType.DIRECTORY and node.total_size <= 100000)


def part_2(lines: List[str]) -> int:
    TOTAL_DISK_SPACE = 70_000_000
    REQUIRED_SPACE = 30_000_000

    tree = build_file_tree(list(reversed(lines)))
    calculate_node_sizes(tree.root)

    space_to_free_up = REQUIRED_SPACE - (TOTAL_DISK_SPACE - tree.root.total_size)
    candidate_dirs_to_delete = [
        node for node in tree.collect_all_nodes()
        if node.type == NodeType.DIRECTORY and node.total_size >= space_to_free_up]

    candidate_dirs_to_delete.sort(key=lambda node: node.total_size)
    return candidate_dirs_to_delete[0].total_size


lines = read_file('day07/input.txt')
print('part1', part_1(lines))  # type: ignore
print('part2', part_2(lines))  # type: ignore
