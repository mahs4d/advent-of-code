from pathlib import Path

from tqdm import tqdm


def get_stones(line: str) -> list[int]:
    return [int(x) for x in line.split()]


def blink(stones: list[int]) -> list[int]:
    result = []
    for stone in stones:
        if stone == 0:
            result.append(1)
            continue

        stone_str = str(stone)
        if len(stone_str) % 2 == 0:
            result.append(int(stone_str[:len(stone_str) // 2]))
            result.append(int(stone_str[len(stone_str) // 2:]))
            continue

        result.append(stone * 2024)

    return result

def main(input_path: Path) -> int:
    line = input_path.read_text()
    stones = get_stones(line=line)
    for _ in tqdm(range(25)):
        stones = blink(stones=stones)
    return len(stones)

if __name__ == '__main__':
    sample_result = main(
        input_path=Path('data/sample.txt'),
    )
    print(f'Sample Result: {sample_result}')
    assert sample_result == 55312

    input_result = main(
        input_path=Path('data/input.txt'),
    )
    print(f'Input Result: {input_result}')
