from __future__ import annotations

import re
from collections import defaultdict
from enum import StrEnum, auto
from pathlib import Path

from pydantic import BaseModel, ConfigDict
from tqdm import tqdm

ROBOT_PATTERN = re.compile(
    pattern=r"^p=(?P<pos_x>[\-]*\d+),(?P<pos_y>[\-]*\d+) v=(?P<vel_x>[\-]*\d+),(?P<vel_y>[\-]*\d+)$",
)


class Coordinates(BaseModel):
    x: int
    y: int

    model_config = ConfigDict(frozen=True)


class Quadrant(StrEnum):
    TOP_RIGHT = auto()
    TOP_LEFT = auto()
    BOTTOM_RIGHT = auto()
    BOTTOM_LEFT = auto()
    MID_LINE = auto()


class Robot(BaseModel):
    id: int
    position: Coordinates
    velocity: Coordinates


class Solution:
    def __init__(self, input_lines: list[str], width: int, height: int, steps: int) -> None:
        self.robots: list[Robot]

        self.width: int = width
        self.height: int = height
        self.steps: int = steps

        self.setup_robots(input_lines=input_lines)

    def setup_robots(self, input_lines: list[str]) -> None:
        robots = []
        for i, line in enumerate(input_lines):
            match = ROBOT_PATTERN.match(line)
            robot = Robot(
                id=i,
                position=Coordinates(
                    x=int(match.group("pos_x")),
                    y=int(match.group("pos_y")),
                ),
                velocity=Coordinates(
                    x=int(match.group("vel_x")),
                    y=int(match.group("vel_y")),
                )
            )
            robots.append(robot)

        self.robots = robots

    def get_p1_result(self) -> int:
        final_coordinate_counts = defaultdict(list)
        for robot in tqdm(self.robots):
            final_coordinates = self._get_final_coordinates(robot=robot)
            quadrant = self._get_quadrant(coordinates=final_coordinates)
            final_coordinate_counts[quadrant].append(final_coordinates)

        result = 1
        for quadrant, robot_coordinates in final_coordinate_counts.items():
            if quadrant == Quadrant.MID_LINE:
                continue

            result *= len(robot_coordinates)

        return result

    def _get_final_coordinates(
            self,
            robot: Robot,
    ) -> Coordinates:
        final_x = (robot.position.x + (robot.velocity.x * self.steps)) % self.width
        final_y = (robot.position.y + (robot.velocity.y * self.steps)) % self.height
        return Coordinates(
            x=final_x,
            y=final_y,
        )

    def _get_quadrant(self, coordinates: Coordinates) -> Quadrant:
        mid_x = self.width // 2
        mid_y = self.height // 2

        if coordinates.x == mid_x or coordinates.y == mid_y:
            return Quadrant.MID_LINE

        if coordinates.x < mid_x and coordinates.y < mid_y:
            return Quadrant.TOP_LEFT

        if coordinates.x > mid_x and coordinates.y < mid_y:
            return Quadrant.TOP_RIGHT

        if coordinates.x < mid_x and coordinates.y > mid_y:
            return Quadrant.BOTTOM_LEFT

        if coordinates.x > mid_x and coordinates.y > mid_y:
            return Quadrant.BOTTOM_RIGHT


def main(input_path: Path) -> int:
    input_lines = input_path.read_text().splitlines()

    width = int(input_lines[0].split()[0])
    height = int(input_lines[0].split()[1])
    solution = Solution(input_lines=input_lines[1:], width=width, height=height, steps=100)
    result = solution.get_p1_result()

    return result


if __name__ == '__main__':
    sample_result = main(
        input_path=Path('data/sample.txt'),
    )
    print(f'Sample Result: {sample_result}')
    assert sample_result == 12

    input_result = main(
        input_path=Path('data/input.txt'),
    )
    print(f'Input Result: {input_result}')
