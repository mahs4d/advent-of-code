from __future__ import annotations

from collections import deque
from pathlib import Path


def get_static_corruption_map(input_lines: list[str], min_steps: int) -> dict[tuple[int, int], int]:
    result = {}
    for i in range(min_steps):
        x, y = input_lines[i].split(',')
        x, y = int(x), int(y)
        result[x, y] = 0
    return result


def is_outside(x: int, y: int, width: int, height: int) -> bool:
    return not (0 <= x <= width and 0 <= y <= height)


def get_best_path(
        corruption_map: dict[tuple[int, int], int],
        width: int,
        height: int,
) -> list[tuple[int, int]] | None:
    visited = set()
    queue = deque([[(0, 0)]])
    while queue:
        path = queue.popleft()
        x, y = path[-1]

        if (x, y) == (width, height):
            return path

        for next_x, next_y in [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
        ]:
            if is_outside(next_x, next_y, width, height):
                continue

            if (next_x, next_y) in visited:
                continue

            if (next_x, next_y) in corruption_map:
                continue

            queue.append(path + [(next_x, next_y)])
            visited.add((next_x, next_y))

    return None


def get_p2_result(input_lines: list[str], width: int, height: int) -> int:
    low_bound = 0
    high_bound = len(input_lines) - 1
    while low_bound <= high_bound:
        min_steps = low_bound + ((high_bound - low_bound) // 2)
        corruption_map = get_static_corruption_map(input_lines=input_lines, min_steps=min_steps)
        best_path = get_best_path(
            corruption_map=corruption_map,
            width=width,
            height=height,
        )

        if best_path is None:
            high_bound = min_steps - 1
        else:
            low_bound = min_steps + 1

    print(f'min_steps: {min_steps}, low_bound: {low_bound}, high_bound: {high_bound}')
    return high_bound


def main(input_path: Path, width: int, height: int) -> str:
    input_lines = input_path.read_text().splitlines()
    result = get_p2_result(input_lines=input_lines, width=width, height=height)
    return input_lines[result]


if __name__ == '__main__':
    sample_result = main(
        input_path=Path('data/sample.txt'),
        width=6,
        height=6,
    )
    print(f'Sample Result: {sample_result}')
    assert sample_result == '6,1'

    input_result = main(
        input_path=Path('data/input.txt'),
        width=70,
        height=70,
    )
    assert input_result == '52,5'
    print(f'Input Result: {input_result}')
