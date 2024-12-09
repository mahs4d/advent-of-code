from pathlib import Path


def get_compact_form(line: str) -> list[tuple[int | str, int]]:
    result = []
    is_free_space = False

    id_index = 0
    for v in line:
        if is_free_space:
            result.append(('.', int(v)))
        else:
            result.append((id_index, int(v)))
            id_index += 1

        is_free_space = not is_free_space

    return result


def get_ordered_form(compact_form: list[tuple[int | str, int]]) -> list[tuple[int | str, int]]:
    result = []
    i = 0
    while i < len(compact_form):
        id_index, size = compact_form[i]
        if id_index != '.':
            result.append((id_index, size))
            i += 1
            continue

        j = len(compact_form) - 1
        while j > i:
            second_id_index, second_size = compact_form[j]
            if second_id_index == '.':
                j -= 1
                continue

            if second_size > size:
                j -= 1
                continue

            break

        selected_id, selected_size = compact_form[j]
        result.append((selected_id, selected_size))
        compact_form[j] = ('.', selected_size)
        if selected_size < size:
            compact_form.insert(i + 1, ('.', size - selected_size))

        i += 1

    return result


def get_expanded_form(compact_form: list[tuple[int | str, int]]) -> list[int]:
    result = []
    for value, repeat in compact_form:
        for i in range(repeat):
            result.append(value)

    return result


def get_checksum(expanded_form: list[int]) -> int:
    result = 0
    for i, v in enumerate(expanded_form):
        if v == '.':
            continue

        result += i * v

    return result


def main(input_path: Path) -> int:
    line = input_path.read_text()
    compact_form = get_compact_form(line=line)
    ordered_form = get_ordered_form(compact_form=compact_form)
    expanded_form = get_expanded_form(compact_form=ordered_form)
    checksum = get_checksum(expanded_form=expanded_form)
    return checksum


if __name__ == '__main__':
    sample_result = main(
        input_path=Path('data/sample.txt'),
    )
    print(f'Sample Result: {sample_result}')
    assert sample_result == 2858

    input_result = main(
        input_path=Path('data/input.txt'),
    )
    print(f'Input Result: {input_result}')
