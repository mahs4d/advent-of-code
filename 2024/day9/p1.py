from pathlib import Path


def get_expanded_form(line: str) -> list[int]:
    result = []
    is_free_space = False

    id_index = 0
    for v in line:
        for i in range(int(v)):
            result.append(id_index if not is_free_space else '.')

        if not is_free_space:
            id_index += 1
        is_free_space = not is_free_space

    return result


def get_ordered_form(expanded_form: list[int]) -> list[int]:
    i = 0
    j = len(expanded_form) - 1

    result = list(['*'] * len(expanded_form))
    while i <= j:
        if expanded_form[i] != '.':
            result[i] = expanded_form[i]
            i += 1
            continue

        if expanded_form[j] == '.':
            result[j] = expanded_form[j]
            j -= 1
            continue

        result[i] = expanded_form[j]
        result[j] = '.'
        i += 1
        j -= 1

    return result


def get_checksum(ordered_form: list[int]) -> int:
    result = 0
    for i, v in enumerate(ordered_form):
        if v == '.':
            continue

        result += i * v

    return result


def main(input_path: Path) -> int:
    line = input_path.read_text()
    expanded_form = get_expanded_form(line=line)
    ordered_form = get_ordered_form(expanded_form=expanded_form)
    checksum = get_checksum(ordered_form=ordered_form)
    return checksum


if __name__ == '__main__':
    sample_result = main(
        input_path=Path('data/sample.txt'),
    )
    print(f'Sample Result: {sample_result}')
    assert sample_result == 1928

    input_result = main(
        input_path=Path('data/input.txt'),
    )
    print(f'Input Result: {input_result}')
