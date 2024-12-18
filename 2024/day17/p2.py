from __future__ import annotations

from pathlib import Path
from typing import Callable


def get_combo_operand_value(operand: int, registers: dict[str, int | None]) -> int:
    if 0 <= operand <= 3:
        return operand

    if 4 <= operand <= 6:
        return registers[{
            4: 'A',
            5: 'B',
            6: 'C',
        }[operand]]

    raise Exception(f'combo operand `{operand}` is not valid')


def run_adv_instruction(operand: int, registers: dict) -> int | None:
    operand = get_combo_operand_value(operand=operand, registers=registers)
    result = registers['A'] // (pow(2, operand))
    registers['A'] = result
    return None


def run_bxl_instruction(operand: int, registers: dict) -> int | None:
    result = registers['B'] ^ operand
    registers['B'] = result
    return None


def run_bst_instruction(operand: int, registers: dict) -> int | None:
    operand = get_combo_operand_value(operand=operand, registers=registers)
    result = operand % 8
    registers['B'] = result
    return None


def run_jnz_instruction(operand: int, registers: dict) -> int | None:
    if registers['A'] == 0:
        return None

    return operand


def run_bxc_instruction(operand: int, registers: dict) -> int | None:
    result = registers['B'] ^ registers['C']
    registers['B'] = result
    return None


def run_out_instruction(operand: int, registers: dict) -> int | None:
    operand = get_combo_operand_value(operand=operand, registers=registers)
    result = operand % 8
    registers['O'].append(result)
    return None


def run_bdv_instruction(operand: int, registers: dict) -> int | None:
    operand = get_combo_operand_value(operand=operand, registers=registers)
    result = registers['A'] // (pow(2, operand))
    registers['B'] = result
    return None


def run_cdv_instruction(operand: int, registers: dict) -> int | None:
    operand = get_combo_operand_value(operand=operand, registers=registers)
    result = registers['A'] // (pow(2, operand))
    registers['C'] = result
    return None


def get_instruction_fn_by_opcode(opcode: int) -> Callable:
    return {
        0: run_adv_instruction,
        1: run_bxl_instruction,
        2: run_bst_instruction,
        3: run_jnz_instruction,
        4: run_bxc_instruction,
        5: run_out_instruction,
        6: run_bdv_instruction,
        7: run_cdv_instruction,
    }[opcode]


def run(register_a: int, register_b: int, register_c: int, program: list[int]) -> list[int]:
    registers = {
        'A': register_a,
        'B': register_b,
        'C': register_c,
        'O': [],
    }
    i = 0
    while i < len(program):
        opcode = program[i]
        operand = program[i + 1]
        instruction_fn = get_instruction_fn_by_opcode(opcode=opcode)
        new_i = instruction_fn(operand=operand, registers=registers)
        if new_i is not None:
            i = new_i
            continue

        i += 2

    return registers['O']


def run_with_prefix(
    prefix: int,
    target_output: list[int],
    program: list[int],
) -> list[int]:
    registers = []
    for postfix in range(8):
        register_a = (prefix * 8) + postfix
        output = run(
            register_a=register_a,
            register_b=0,
            register_c=0,
            program=program,
        )

        if output == target_output:
            registers.append(register_a)

    return registers


def get_p2_result(input_lines: list[str]) -> list[int]:
    program = list(map(int, input_lines[4][9:].split(',')))

    target_i = 1
    register_a_prefixes = [0]
    while target_i <= len(program):
        next_prefixes = []
        for prefix in register_a_prefixes:
            new_register_a = run_with_prefix(
                prefix=prefix,
                target_output=program[-target_i:],
                program=program,
            )
            next_prefixes.extend(new_register_a)

        if not next_prefixes:
            raise Exception(f'{target_i} is not a valid prefix')

        register_a_prefixes = next_prefixes
        target_i += 1

    return register_a_prefixes


def main(input_path: Path) -> int:
    input_lines = input_path.read_text().splitlines()
    result = get_p2_result(input_lines=input_lines)
    return min(result)


if __name__ == '__main__':
    sample_result = main(
        input_path=Path('data/sample_2.txt'),
    )
    print(f'Sample Result: {sample_result}')
    assert sample_result == 117440

    input_result = main(
        input_path=Path('data/input_1.txt'),
    )
    print(f'Input Result: {input_result}')
