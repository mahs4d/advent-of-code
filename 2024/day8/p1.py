from collections import defaultdict
from pathlib import Path


def get_matrix(lines: list[str]) -> list[list[str]]:
    result = []
    for row in lines:
        result.append(list(row))

    return result


def is_antenna(value: str) -> bool:
    return value.isalnum()


def is_outside(matrix: list[list[str]], x: int, y: int) -> bool:
    if y >= len(matrix) or y < 0:
        return True

    if x >= len(matrix[0]) or x < 0:
        return True

    return False


def get_antennas_dict(matrix: list[list[str]]) -> dict[str, list[tuple[int, int]]]:
    result = defaultdict(list)
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            if not is_antenna(value):
                continue

            result[value].append((j, i))

    return result


def get_two_antenna_antinodes(
        matrix: list[list[str]],
        antenna_location1: tuple[int, int],
        antenna_location2: tuple[int, int],
) -> set[tuple[int, int]]:
    x1, y1 = antenna_location1
    x2, y2 = antenna_location2

    dy = y2 - y1
    dx = x2 - x1

    result = set()
    for antinode_x, antinode_y in [
        (x1 - dx, y1 - dy),
        (x2 + dx, y2 + dy),
    ]:
        if is_outside(matrix=matrix, x=antinode_x, y=antinode_y):
            continue

        result.add((antinode_x, antinode_y))

    return result


def get_antinodes(matrix: list[list[str]]) -> set[tuple[int, int]]:
    antennas_dict = get_antennas_dict(matrix=matrix)

    result = set()
    for antenna_key in antennas_dict.keys():
        antenna_locations = antennas_dict[antenna_key]
        for i in range(len(antenna_locations)):
            for j in range(i + 1, len(antenna_locations)):
                antinodes = get_two_antenna_antinodes(
                    matrix=matrix,
                    antenna_location1=antenna_locations[i],
                    antenna_location2=antenna_locations[j],
                )
                result = result.union(antinodes)

    return result


def main(input_path: Path) -> int:
    lines = input_path.read_text().splitlines()
    matrix = get_matrix(lines=lines)
    antinodes = get_antinodes(matrix=matrix)
    return len(antinodes)


if __name__ == '__main__':
    sample_result = main(
        input_path=Path('data/sample.txt'),
    )
    print(f'Sample Result: {sample_result}')
    assert sample_result == 14

    input_result = main(
        input_path=Path('data/input.txt'),
    )
    print(f'Input Result: {input_result}')
