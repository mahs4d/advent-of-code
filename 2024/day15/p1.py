from __future__ import annotations

from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, ConfigDict


class Direction(StrEnum):
    RIGHT = '>'
    LEFT = '<'
    UP = '^'
    DOWN = 'v'

    @staticmethod
    def from_move_lines(move_lines: list[str]) -> list[Direction]:
        return [Direction(value) for value in ''.join(move_lines)]


class Coordinates(BaseModel):
    x: int
    y: int

    model_config = ConfigDict(frozen=True)

    def get_next_coordinates(self, direction: Direction) -> Coordinates:
        next_x, next_y = {
            Direction.DOWN: (self.x, self.y + 1),
            Direction.UP: (self.x, self.y - 1),
            Direction.RIGHT: (self.x + 1, self.y),
            Direction.LEFT: (self.x - 1, self.y),
        }[direction]
        return Coordinates(x=next_x, y=next_y)

    def get_gps_value(self) -> int:
        return (self.y * 100) + self.x


class MapObject(StrEnum):
    ROBOT = '@'
    BOX = 'O'
    EMPTY = '.'
    WALL = '#'


class Map(BaseModel):
    matrix: list[list[MapObject]]
    robot: Coordinates

    @staticmethod
    def from_map_lines(map_lines: list[str]) -> Map:
        matrix = []
        robot = None
        for y, map_line in enumerate(map_lines):
            row = []
            for x, value in enumerate(map_line):
                obj = MapObject(value)
                row.append(obj)
                if obj == MapObject.ROBOT:
                    robot = Coordinates(x=x, y=y)

            matrix.append(row)

        return Map(matrix=matrix, robot=robot)

    def is_outside(self, x: int, y: int) -> bool:
        if y >= len(self.matrix) or y < 0:
            return True

        if x >= len(self.matrix[0]) or x < 0:
            return True

        return False

    def move(self, coordinates: Coordinates, direction: Direction) -> bool:
        if self.is_outside(x=coordinates.x, y=coordinates.y):
            return False

        obj = self.matrix[coordinates.y][coordinates.x]

        if obj == MapObject.EMPTY:
            return True

        if obj == MapObject.WALL:
            return False

        next_coordinates = coordinates.get_next_coordinates(direction)
        is_move_allowed = self.move(
            coordinates=next_coordinates,
            direction=direction,
        )
        if not is_move_allowed:
            return False

        self.matrix[coordinates.y][coordinates.x] = MapObject.EMPTY
        self.matrix[next_coordinates.y][next_coordinates.x] = obj

        if obj == MapObject.ROBOT:
            self.robot = next_coordinates

        return True

    def draw(self) -> None:
        output = []
        for row in self.matrix:
            output.append(''.join([str(v) for v in row]))

        print('\n'.join(output))

    def get_box_gps_value(self) -> int:
        result = 0
        for y, row in enumerate(self.matrix):
            for x, value in enumerate(row):
                if value != MapObject.BOX:
                    continue

                result += Coordinates(x=x, y=y).get_gps_value()

        return result


class Solution:
    def __init__(self, map_lines: list[str], move_lines: list[str]) -> None:
        self.map = Map.from_map_lines(map_lines=map_lines)
        self.moves = Direction.from_move_lines(move_lines=move_lines)

    def get_p1_result(self) -> int:
        for move in self.moves:
            self.map.move(
                coordinates=self.map.robot,
                direction=move,
            )

        self.map.draw()
        return self.map.get_box_gps_value()


def main(input_path: Path) -> int:
    input_lines = input_path.read_text().splitlines()
    map_lines = []
    for i in range(len(input_lines)):
        if input_lines[i] == '':
            break
        map_lines.append(input_lines[i])

    move_lines = []
    for j in range(i + 1, len(input_lines)):
        move_lines.append(input_lines[j])

    solution = Solution(map_lines=map_lines, move_lines=move_lines)
    result = solution.get_p1_result()

    return result


if __name__ == '__main__':
    sample_result = main(
        input_path=Path('data/sample.txt'),
    )
    print(f'Sample Result: {sample_result}')
    assert sample_result == 10092

    input_result = main(
        input_path=Path('data/input.txt'),
    )
    print(f'Input Result: {input_result}')
