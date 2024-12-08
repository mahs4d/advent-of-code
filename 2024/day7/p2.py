from pathlib import Path

from tqdm import tqdm


def get_equations(equation_lines: list[str]) -> list[tuple[int, list[int]]]:
    equations = []
    for line in equation_lines:
        target, numbers = line.split(": ")
        target = int(target)
        numbers = numbers.split()
        equations.append((target, [int(x) for x in numbers]))

    return equations

def is_equation_solvable(
        target: int,
        numbers: list[int],
        current_value: int = 0,
        is_first_number: bool = True,
) -> bool:
    if not numbers:
        return current_value == target

    plus_number = current_value + numbers[0]
    multi_number = current_value * numbers[0] if not is_first_number else numbers[0]
    concat_number = int(f'{current_value}{numbers[0]}')

    with_plus = is_equation_solvable(target, numbers[1:], plus_number, False)
    with_multi = is_equation_solvable(target, numbers[1:], multi_number, False)
    with_concat = is_equation_solvable(target, numbers[1:], concat_number, False)

    return with_plus or with_multi or with_concat


def main(input_path: Path) -> int:
    equation_lines = input_path.read_text().splitlines()
    equations = get_equations(equation_lines=equation_lines)

    result = 0
    for target, numbers in tqdm(equations):
        if is_equation_solvable(
                target=target,
                numbers=numbers,
        ):
            result += target

    return result


if __name__ == '__main__':
    sample_result = main(
        input_path=Path('data/sample.txt'),
    )
    print(f'Sample Result: {sample_result}')
    assert sample_result == 11387

    input_result = main(
        input_path=Path('data/input.txt'),
    )
    print(f'Input Result: {input_result}')
