from pathlib import Path

from tqdm import tqdm

ALL_DIRECTIONS = [
    (1, 0),
    (1, 1),
    (1, -1),
    (-1, 0),
    (-1, 1),
    (-1, -1),
    (0, 1),
    (0, -1),
]
KEY = "XMAS"


def get_matrix(lines: list[str]) -> list[list[str]]:
    result = []
    for row in lines:
        result.append(list(row))

    return result


def get_matrix_value(matrix: list[list[str]], x: int, y: int) -> str | None:
    if x < 0 or y < 0 or y >= len(matrix) or x >= len(matrix[0]):
        return None

    return matrix[y][x]


def get_xmas_count(matrix: list[list[str]], start_x: int, start_y: int) -> int:
    result = 0
    for direction in ALL_DIRECTIONS:
        state = 0
        x, y = start_x, start_y
        while state < len(KEY):
            value = get_matrix_value(matrix=matrix, x=x, y=y)
            if value != KEY[state]:
                break

            x, y = x + direction[0], y + direction[1]
            state += 1

        if state == len(KEY):
            result += 1

    return result


def main(input_path: Path) -> int:
    lines = input_path.read_text().splitlines()
    matrix = get_matrix(lines=lines)

    result = 0
    for y in tqdm(range(len(matrix))):
        for x in range(len(matrix[y])):
            xmas_count = get_xmas_count(matrix=matrix, start_x=x, start_y=y)
            result += xmas_count

    return result


if __name__ == '__main__':
    sample_result = main(
        input_path=Path('data/sample.txt'),
    )
    print(f'Sample Result: {sample_result}')
    assert sample_result == 18

    input_result = main(
        input_path=Path('data/input.txt'),
    )
    print(f'Input Result: {input_result}')
