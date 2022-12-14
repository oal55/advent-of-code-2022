from dataclasses import dataclass
from typing import List

from utils import read_file


@dataclass
class Move:
    name: str
    score: int
    wins_against: 'Move' = None  # type: ignore
    loses_to: 'Move' = None  # type: ignore

    def __repr__(self) -> str:
        name_score = f'name: {self.name}, score: {self.score}'
        win_lose = f'wins_against: {self.wins_against.name}, loses_to: {self.loses_to.name}'
        return f'{{{name_score}, {win_lose}}}'


ROCK = Move('rock', 1)
PAPER = Move('paper', 2)
SCISSORS = Move('scissors', 3)
MOVES = [ROCK, PAPER, SCISSORS]

CODE_TO_MOVE = {
    'A': ROCK,
    'X': ROCK,
    'B': PAPER,
    'Y': PAPER,
    'C': SCISSORS,
    'Z': SCISSORS
}


def init_moves() -> None:
    len_moves = len(MOVES)
    for i, move in enumerate(MOVES):
        move.wins_against = MOVES[i - 1] if i else MOVES[len_moves - 1]
        move.loses_to = MOVES[(i + 1) % len_moves]


def eval_right_against_left(left: Move, right: Move) -> int:
    base_score = right.score
    if right.wins_against == left:
        return 6 + base_score
    if right == left:
        return 3 + base_score
    if right.loses_to == left:
        return base_score
    raise SystemError('shoudlnt happen')


def part_1(rounds: List[str]) -> int:
    total_score = 0
    for game_round in rounds:
        left_nazo, right_nazo = game_round.split(' ')
        total_score += eval_right_against_left(CODE_TO_MOVE[left_nazo], CODE_TO_MOVE[right_nazo])
    return total_score


def part_2(rounds: List[str]) -> int:
    total_score = 0
    for game_round in rounds:
        left_nazo, right_nazo = game_round.split(' ')
        left_move = CODE_TO_MOVE[left_nazo]
        right_move = None
        if right_nazo == 'X':
            right_move = left_move.wins_against
        elif right_nazo == 'Y':
            right_move = left_move
        elif right_nazo == 'Z':
            right_move = left_move.loses_to
        else:
            raise SystemError('shouldnt happen')

        total_score += eval_right_against_left(left_move, right_move)
    return total_score


init_moves()
lines = read_file('day02/input.txt')
print('part1', part_1(lines))
print('part2', part_2(lines))
