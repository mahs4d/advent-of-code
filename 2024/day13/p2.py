from __future__ import annotations

import re
from collections import deque
from pathlib import Path

from pydantic import BaseModel, ConfigDict
from tqdm import tqdm

PUZZLE_PATTERN = re.compile(
    pattern=r"Button (?P<button_name_1>.+): X\+(?P<button_x_step_1>\d+), Y\+(?P<button_y_step_1>\d+)\nButton (?P<button_name_2>.+): X\+(?P<button_x_step_2>\d+), Y\+(?P<button_y_step_2>\d+)\nPrize: X=(?P<prize_x>\d+), Y=(?P<prize_y>\d+)",
)

BUTTON_TOKENS_MAPPING = {
    "A": 3,
    "B": 1,
}

DRIFT = 10000000000000


class Button(BaseModel):
    name: str
    tokens: int
    x_step: int
    y_step: int


class Location(BaseModel):
    x: int
    y: int

    model_config = ConfigDict(frozen=True)


class Puzzle(BaseModel):
    buttons: list[Button]
    prize: Location


class Solution:
    def __init__(self, input_text: str) -> None:
        self.puzzles: list[Puzzle]

        self.setup_puzzles(input_text=input_text)

    def setup_puzzles(self, input_text: str) -> None:
        puzzles = []

        matches = PUZZLE_PATTERN.finditer(input_text)
        for match in matches:
            puzzles.append(
                Puzzle(
                    buttons=[
                        Button(
                            name=match.group("button_name_1"),
                            tokens=BUTTON_TOKENS_MAPPING[match.group("button_name_1")],
                            x_step=match.group("button_x_step_1"),
                            y_step=match.group("button_y_step_1"),
                        ),
                        Button(
                            name=match.group("button_name_2"),
                            tokens=BUTTON_TOKENS_MAPPING[match.group("button_name_2")],
                            x_step=match.group("button_x_step_2"),
                            y_step=match.group("button_y_step_2"),
                        ),
                    ],
                    prize=Location(
                        x=int(match.group("prize_x")) + DRIFT,
                        y=int(match.group("prize_y")) + DRIFT,
                    )
                ),
            )

        self.puzzles = puzzles

    def get_p1_result(self) -> int:
        result = 0
        for puzzle in tqdm(self.puzzles):
            minimum_tokens = self._get_minimum_tokens(
                puzzle=puzzle,
            )
            result += minimum_tokens if minimum_tokens else 0

        return result

    def _get_minimum_tokens(
            self,
            puzzle: Puzzle,
    ) -> int | None:
        """
        (a*x0) + (b*x1) = xt
        (a*y0) + (b*y1) = yt

        x0y1a + x1y1b = y1xt
        x1y0a + x1y1b = x1yt

        (x0y1 - x1y0a) = y1xt - x1yt

        a = (xt * y1) / ((x0 * y1) - (y0 * x1))
        """
        xt = puzzle.prize.x
        yt = puzzle.prize.y
        x0 = puzzle.buttons[0].x_step
        y0 = puzzle.buttons[0].y_step
        x1 = puzzle.buttons[1].x_step
        y1 = puzzle.buttons[1].y_step

        d = (x0 * y1) - (y0 * x1)
        if d == 0:
            return None

        a = ((xt * y1) - (x1 * yt)) / d
        b = (yt - (a * y0)) / y1

        if int(a + b) != a + b:
            return None

        return int((3 * a) + b)


def main(input_path: Path) -> int:
    input_text = input_path.read_text()

    solution = Solution(input_text=input_text)
    result = solution.get_p1_result()

    return result


if __name__ == '__main__':
    sample_result = main(
        input_path=Path('data/sample.txt'),
    )
    print(f'Sample Result: {sample_result}')
    assert sample_result == 875318608908

    input_result = main(
        input_path=Path('data/input.txt'),
    )
    print(f'Input Result: {input_result}')
