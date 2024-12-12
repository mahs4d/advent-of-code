from __future__ import annotations

from collections import deque
from enum import StrEnum, auto
from pathlib import Path
from uuid import UUID
from uuid import uuid4

from pydantic import BaseModel

MATRIX_TYPE = list[list[str]]
POINT_TYPE = tuple[int, int]
REGION_MAPPING = dict[POINT_TYPE, 'Region']


class Direction(StrEnum):
    RIGHT = auto()
    LEFT = auto()
    TOP = auto()
    BOTTOM = auto()


class Region(BaseModel):
    id: UUID
    points: set[POINT_TYPE]


class Solution:
    def __init__(self, raw_lines: list[str]) -> None:
        self.matrix: MATRIX_TYPE
        self.regions: list[Region]
        self.region_mapping: REGION_MAPPING

        self.setup_matrix(raw_lines=raw_lines)
        self.setup_regions()

    def setup_matrix(self, raw_lines: list[str]) -> None:
        matrix = []
        for row in raw_lines:
            matrix.append([x for x in row])

        self.matrix = matrix

    def setup_regions(self):
        self.regions = []
        self.regions_mapping = {}
        for y in range(len(self.matrix)):
            for x in range(len(self.matrix[0])):
                if (x, y) in self.regions_mapping:
                    continue

                region = Region(
                    id=uuid4(),
                    points=self._navigate_matrix(x, y, self.matrix[y][x])
                )
                self.regions.append(region)
                for point in region.points:
                    self.regions_mapping[point] = region

    def _navigate_matrix(self, start_x: int, start_y: int, region_code: str) -> set[POINT_TYPE]:
        visited_points: set[POINT_TYPE] = set()
        queue = deque([(start_x, start_y)])
        while queue:
            x, y = queue.pop()
            if (x, y) in visited_points:
                continue

            if self._is_outside(x, y):
                continue

            if self.matrix[y][x] != region_code:
                continue

            visited_points.add((x, y))
            queue.append((x + 1, y))
            queue.append((x - 1, y))
            queue.append((x, y + 1))
            queue.append((x, y - 1))

        return visited_points

    def get_p1_result(self) -> int:
        result = 0
        for region in self.regions:
            result += self._get_region_area(region) * self._get_region_perimeter(region)

        return result

    def get_p2_result(self) -> int:
        result = 0
        for region in self.regions:
            result += self._get_region_area(region) * self._get_region_sides(region)

        return result

    @staticmethod
    def _get_region_area(region: Region) -> int:
        return len(region.points)

    @staticmethod
    def _get_region_perimeter(region: Region) -> int:
        result = 0
        for x, y in region.points:
            for neighbor_x, neighbor_y in [
                (x, y - 1),
                (x + 1, y),
                (x, y + 1),
                (x - 1, y),
            ]:
                if (neighbor_x, neighbor_y) in region.points:
                    continue
                result += 1

        return result

    def _get_region_sides(self, region: Region) -> int:
        sides: set[UUID] = set()
        cache: dict[tuple[POINT_TYPE, Direction], UUID | None] = {}
        for x, y in region.points:
            for direction in Direction:
                side = self._get_region_point_side(
                    cache=cache,
                    region=region,
                    x=x,
                    y=y,
                    direction=direction,
                )
                if side != None:
                    sides.add(side)

        return len(sides)

    def _get_region_point_side(
            self,
            cache: dict[tuple[POINT_TYPE, Direction], UUID | None],
            region: Region,
            x: int,
            y: int,
            direction: Direction,
    ) -> UUID | None:
        if ((x, y), direction) in cache:
            return cache[((x, y), direction)]

        check_neighbor_mapping = {
            Direction.RIGHT: (x + 1, y),
            Direction.LEFT: (x - 1, y),
            Direction.TOP: (x, y - 1),
            Direction.BOTTOM: (x, y + 1),
        }
        prev_neighbor_mapping = {
            Direction.RIGHT: (x, y - 1),
            Direction.LEFT: (x, y - 1),
            Direction.TOP: (x - 1, y),
            Direction.BOTTOM: (x - 1, y),
        }

        check_x, check_y = check_neighbor_mapping[direction]
        if (check_x, check_y) in region.points:
            cache[((x, y), direction)] = None
            return None

        prev_x, prev_y = prev_neighbor_mapping[direction]
        if (prev_x, prev_y) in region.points:
            prev_side = self._get_region_point_side(
                cache=cache,
                region=region,
                x=prev_x,
                y=prev_y,
                direction=direction,
            )

            if prev_side is not None:
                cache[((x, y), direction)] = prev_side
                return prev_side

        new_side = uuid4()
        cache[((x, y), direction)] = new_side
        return new_side





    def _is_outside(self, x: int, y: int) -> bool:
        if y >= len(self.matrix) or y < 0:
            return True

        if x >= len(self.matrix[0]) or x < 0:
            return True

        return False


def main(input_path: Path) -> int:
    lines = input_path.read_text().splitlines()

    solution = Solution(raw_lines=lines)
    result = solution.get_p2_result()

    return result


if __name__ == '__main__':
    sample_result = main(
        input_path=Path('data/sample2.txt'),
    )
    print(f'Sample Result: {sample_result}')
    assert sample_result == 368

    input_result = main(
        input_path=Path('data/input.txt'),
    )
    print(f'Input Result: {input_result}')
