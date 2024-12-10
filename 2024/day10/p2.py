from pathlib import Path


def get_matrix(lines: list[str]) -> list[list[int]]:
    result = []
    for row in lines:
        result.append([int(x) for x in row])

    return result


def is_outside(matrix: list[list[int]], x: int, y: int) -> bool:
    if y >= len(matrix) or y < 0:
        return True

    if x >= len(matrix[0]) or x < 0:
        return True

    return False


def get_reachable_paths(
        cache: dict[tuple[int, int], int],
        matrix: list[list[int]],
        x: int,
        y: int,
) -> int:
    if (x, y) in cache:
        return cache[(x, y)]

    if matrix[y][x] == 9:
        cache[(x, y)] = 1
        return cache[(x, y)]

    result = 0
    for next_x, next_y in [
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1),
    ]:
        if is_outside(matrix=matrix, x=next_x, y=next_y):
            continue

        if matrix[next_y][next_x] != matrix[y][x] + 1:
            continue

        next_reachable_paths = get_reachable_paths(
            cache=cache,
            matrix=matrix,
            x=next_x,
            y=next_y,
        )
        result += next_reachable_paths

    cache[(x, y)] = result
    return cache[(x, y)]


def main(input_path: Path) -> int:
    lines = input_path.read_text().splitlines()
    matrix = get_matrix(lines=lines)

    result = 0
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            if matrix[y][x] != 0:
                continue

            reachable_nines = get_reachable_paths(
                cache={},
                matrix=matrix,
                x=x,
                y=y,
            )
            result += reachable_nines

    return result


if __name__ == '__main__':
    sample_result = main(
        input_path=Path('data/sample.txt'),
    )
    print(f'Sample Result: {sample_result}')
    assert sample_result == 81

    input_result = main(
        input_path=Path('data/input.txt'),
    )
    print(f'Input Result: {input_result}')
