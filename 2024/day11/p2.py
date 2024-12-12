from pathlib import Path

from tqdm import tqdm


def get_stones(line: str) -> list[int]:
    return [int(x) for x in line.split()]


def get_final_count(cache: dict[tuple[int, int], int], stone: int, blinks: int) -> int:
    if blinks == 0:
        return 1

    if (stone, blinks) in cache:
        return cache[(stone, blinks)]

    if stone == 0:
        cache[(stone, blinks)] = get_final_count(cache=cache, stone=1, blinks=blinks - 1)
        return cache[(stone, blinks)]

    stone_str = str(stone)
    if len(stone_str) % 2 == 0:
        mid_point = len(stone_str) // 2
        first_part = get_final_count(cache=cache, stone=int(stone_str[:mid_point]), blinks=blinks - 1)
        second_part = get_final_count(cache=cache, stone=int(stone_str[mid_point:]), blinks=blinks - 1)
        cache[(stone, blinks)] = first_part + second_part
        return cache[(stone, blinks)]

    cache[(stone, blinks)] = get_final_count(cache=cache, stone=stone * 2024, blinks=blinks - 1)
    return cache[(stone, blinks)]


def main(input_path: Path) -> int:
    line = input_path.read_text()
    stones = get_stones(line=line)
    cache = {}
    result = 0
    for stone in stones:
        result += get_final_count(cache=cache, stone=stone, blinks=75)
    return result


if __name__ == '__main__':
    sample_result = main(
        input_path=Path('data/sample.txt'),
    )
    print(f'Sample Result: {sample_result}')
    assert sample_result == 65601038650482

    input_result = main(
        input_path=Path('data/input.txt'),
    )
    print(f'Input Result: {input_result}')
