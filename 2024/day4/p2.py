from pathlib import Path

from tqdm import tqdm

X_DIRECTIONS = [
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1),
]
CENTRAL_KEY = "A"
WING_KEYS = {"M", "S"}


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
    if get_matrix_value(matrix, start_x, start_y) != CENTRAL_KEY:
        return 0

    if {
        get_matrix_value(matrix, start_x + 1, start_y - 1),
        get_matrix_value(matrix, start_x - 1, start_y + 1),
    } != WING_KEYS:
        return 0

    if {
        get_matrix_value(matrix, start_x - 1, start_y - 1),
        get_matrix_value(matrix, start_x + 1, start_y + 1),
    } != WING_KEYS:
        return 0

    return 1


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
    assert sample_result == 9

    input_result = main(
        input_path=Path('data/input.txt'),
    )
    print(f'Input Result: {input_result}')
