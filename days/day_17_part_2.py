import sys
from pathlib import Path

# Change the working directory to the root of the project
project_root = Path(__file__).resolve().parent.parent  # Two levels up to the root
sys.path.append(str(project_root))

from config import BASE_DAY_URL, HEADERS
from src.utils import get_daily_title, run_part, file_exists_and_rename
from src.read_data import read_txt_to_str, read_txt_vector_matrix_str
from collections import defaultdict

def transform_register(register_list):
    registers = defaultdict()
    register_list = register_list.split("\n")
    for register_ in register_list:
        register_, value = register_.split(": ")
        registers[register_.replace("Register ", "")] = int(value)

    registers["out"] = []

    return registers


def transform_program(program):
    program_lst = program.replace("Program: ", "").split(",")
    opcode_operand = [(int(program_lst[i]), int(program_lst[i+1])) for i in range(0, len(program_lst), 2)]
    return opcode_operand


def operand_result(operand_value, registers_dict):

    # this means combo value
    if registers_dict:
        operand_dict = {0: 0,
                        1: 1,
                        2: 2,
                        3: 3,
                        4: registers_dict["A"],
                        5: registers_dict["B"],
                        6: registers_dict["C"],
                        7: None}
        return operand_dict[operand_value]
    
    # this means literal value
    return operand_value
        

def division(registers_dict, operand_value):
    value_a =  registers_dict["A"]
    value_b = 2**operand_result(operand_value, registers_dict)
    return value_a // value_b


def bywise(registers_dict, operand_value, opcode=4):
    value_a = registers_dict["B"]

    if opcode==1:
        value_b = operand_result(operand_value, registers_dict=None)
    elif opcode==4:
        value_b = registers_dict["C"]
    else:
        value_b = 0

    return value_a ^ value_b

def module(operand_value, registers_dict):
    value = operand_result(operand_value, registers_dict)
    return value % 8


def does_nothing(operand_value, registers_dict):

    if registers_dict["A"] == 0:
        return None
    
    else:
        return operand_value


def opcode_operation(opcode, operand_value, registers_dict):

    inst_ = None
    opcodes_operations = {
        0: lambda: ("A", division(registers_dict, operand_value)),
        1: lambda: ("B", bywise(registers_dict, operand_value, opcode)),
        2: lambda: ("B", module(operand_value, registers_dict)),
        3: lambda: ("inst_", does_nothing(operand_value, registers_dict)),
        4: lambda: ("B", bywise(registers_dict, operand_value, opcode)),
        5: lambda: ("out", module(operand_value, registers_dict)),
        6: lambda: ("B", division(registers_dict, operand_value)),
        7: lambda: ("C", division(registers_dict, operand_value))
    }

    result_ = opcodes_operations[opcode]()
    
    if result_[0] == "out":
        registers_dict["out"].append(str(result_[1]))

    elif result_[0] == "inst_":
        if result_[1] is not None:
            inst_ = result_[1]
    else:
        registers_dict[result_[0]] = result_[1]

    return registers_dict, inst_

def main_code(file_name, part=1):
    register_list, program_list = read_txt_to_str(file_name, with_split="\n\n")

    programs = transform_program(program_list)
    registers_dict = transform_register(register_list)

    instruction_point = 0
    while instruction_point < len(programs):
        opcode, operand = programs[instruction_point]

        registers_dict, inst_ = opcode_operation(opcode, operand, registers_dict)

        if inst_ is not None:
            instruction_point = inst_
        else:
            instruction_point += 1

    return ",".join(registers_dict["out"])


def main():
    day = 17
    expected_results = {1: "4,6,3,5,6,3,5,2,1,0", 2: None} # fill this
    title = get_daily_title(day, BASE_DAY_URL, HEADERS)
    print(f"🧩 Starting puzzle for: {title}")
    run_part(day, 1, expected_results, main_code)
    file_exists_and_rename(f"days/day_17_to_do.py", f"days/day_17_part_2.py")
    run_part(day, 2, expected_results, main_code)
    file_exists_and_rename(f"days/day_17_part_2.py", f"days/day_17.py")

if __name__ == "__main__":
    main()
