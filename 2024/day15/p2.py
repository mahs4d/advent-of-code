from __future__ import annotations

import itertools
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
    BOX_LEFT = '['
    BOX_RIGHT = ']'
    EMPTY = '.'
    WALL = '#'

    @staticmethod
    def from_old_str(old_str: str) -> list[MapObject]:
        if old_str == 'O':
            return [MapObject.BOX_LEFT, MapObject.BOX_RIGHT]

        if old_str == '@':
            return [MapObject.ROBOT, MapObject.EMPTY]

        return [MapObject(old_str)] * 2


class Map(BaseModel):
    matrix: list[list[MapObject]]
    robot: Coordinates

    @staticmethod
    def from_map_lines(map_lines: list[str]) -> Map:
        matrix = [
            list(itertools.chain(*[MapObject.from_old_str(value) for value in row]))
            for row in map_lines
        ]

        robot = None
        for y, row in enumerate(matrix):
            for x, value in enumerate(row):
                if value == MapObject.ROBOT:
                    robot = Coordinates(x=x, y=y)
                    break

        return Map(matrix=matrix, robot=robot)

    def is_outside(self, x: int, y: int) -> bool:
        if y >= len(self.matrix) or y < 0:
            return True

        if x >= len(self.matrix[0]) or x < 0:
            return True

        return False

    def draw(self) -> None:
        output = []
        for row in self.matrix:
            output.append(''.join([str(v) for v in row]))

        print('\n'.join(output))

    def get_box_gps_value(self) -> int:
        result = 0
        for y, row in enumerate(self.matrix):
            for x, value in enumerate(row):
                if value != MapObject.BOX_LEFT:
                    continue

                result += Coordinates(x=x, y=y).get_gps_value()

        return result


class Solution:
    def __init__(self, map_lines: list[str], move_lines: list[str]) -> None:
        self.map = Map.from_map_lines(map_lines=map_lines)
        self.moves = Direction.from_move_lines(move_lines=move_lines)

    def get_p2_result(self) -> int:
        self.map.draw()
        for move in self.moves:
            self._move(
                coordinates=self.map.robot,
                direction=move,
            )

        self.map.draw()
        return self.map.get_box_gps_value()

    def _can_move(
            self,
            updates: dict[Coordinates, MapObject],
            coordinates: Coordinates,
            direction: Direction,
            prev_coordinates: Coordinates | None = None,
    ) -> bool:
        obj = self.map.matrix[coordinates.y][coordinates.x]
        if obj == MapObject.EMPTY:
            return True

        if obj == MapObject.WALL:
            return False

        linked_coordinates = None
        if obj == MapObject.BOX_LEFT:
            linked_coordinates = Coordinates(
                x=coordinates.x + 1,
                y=coordinates.y,
            )

        if obj == MapObject.BOX_RIGHT:
            linked_coordinates = Coordinates(
                x=coordinates.x - 1,
                y=coordinates.y,
            )

        next_coordinates = coordinates.get_next_coordinates(direction)
        can_move_next = self._can_move(
            updates=updates,
            coordinates=next_coordinates,
            direction=direction,
            prev_coordinates=coordinates,
        )

        if linked_coordinates is None or linked_coordinates == prev_coordinates:
            if can_move_next:
                if coordinates not in updates:
                    updates[coordinates] = MapObject.EMPTY
                updates[next_coordinates] = obj
                return True

            return False

        linked_obj = self.map.matrix[linked_coordinates.y][linked_coordinates.x]
        linked_next_coordinates = linked_coordinates.get_next_coordinates(direction)
        linked_can_move_next = self._can_move(
            updates=updates,
            coordinates=linked_next_coordinates,
            direction=direction,
            prev_coordinates=coordinates,
        )

        if can_move_next and linked_can_move_next:
            if coordinates not in updates:
                updates[coordinates] = MapObject.EMPTY
            updates[next_coordinates] = obj

            if linked_coordinates not in updates:
                updates[linked_coordinates] = MapObject.EMPTY
            updates[linked_next_coordinates] = linked_obj
            return True

        return False

    def _move(self, coordinates: Coordinates, direction: Direction) -> None:
        updates = {}
        can_move = self._can_move(
            updates=updates,
            coordinates=coordinates,
            direction=direction,
        )
        if not can_move:
            return

        for coordinates, value in updates.items():
            self.map.matrix[coordinates.y][coordinates.x] = value
            if value == MapObject.ROBOT:
                self.map.robot = coordinates


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
    result = solution.get_p2_result()

    return result


if __name__ == '__main__':
    sample_result = main(
        input_path=Path('data/sample.txt'),
    )
    print(f'Sample Result: {sample_result}')
    assert sample_result == 9021

    input_result = main(
        input_path=Path('data/input.txt'),
    )
    print(f'Input Result: {input_result}')
