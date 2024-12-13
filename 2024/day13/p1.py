from __future__ import annotations

import re
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
                        x=int(match.group("prize_x")),
                        y=int(match.group("prize_y")),
                    )
                ),
            )

        self.puzzles = puzzles

    def get_p1_result(self) -> int:
        result = 0
        for puzzle in tqdm(self.puzzles):
            minimum_tokens = self._get_minimum_tokens(
                cache={},
                location=Location(x=0, y=0),
                puzzle=puzzle,
            )
            result += minimum_tokens if minimum_tokens else 0

        return result

    def _get_minimum_tokens(
            self,
            cache: dict[Location, int | None],
            location: Location,
            puzzle: Puzzle,
    ) -> int | None:
        if location in cache:
            return cache[location]

        if location.x == puzzle.prize.x and location.y == puzzle.prize.y:
            cache[location] = 0
            return 0

        if location.x > puzzle.prize.x or location.y > puzzle.prize.y:
            cache[location] = None
            return None

        next_steps_count = []
        for button in puzzle.buttons:
            minimum_tokens = self._get_minimum_tokens(
                cache=cache,
                location=Location(x=location.x + button.x_step, y=location.y + button.y_step),
                puzzle=puzzle,
            )
            if minimum_tokens is not None:
                next_steps_count.append(minimum_tokens + button.tokens)

        if not next_steps_count:
            cache[location] = None
            return None

        cache[location] = min(next_steps_count)
        return cache[location]


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
    assert sample_result == 480

    input_result = main(
        input_path=Path('data/input.txt'),
    )
    print(f'Input Result: {input_result}')
