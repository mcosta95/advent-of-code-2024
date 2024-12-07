import sys
from pathlib import Path

# Change the working directory to the root of the project
project_root = Path(__file__).resolve().parent.parent  # Two levels up to the root
sys.path.append(str(project_root))

from config import BASE_DAY_URL, HEADERS
from src.utils import get_daily_title, run_part
from src.read_data import read_txt_to_str
from itertools import product

def add_values(a, b):
    return a + b

def multiply_values(a, b):
    return a*b


def evaluate_expression(numbers, operators):
    """Evaluate the expression with given numbers and operators, left-to-right."""
    result = numbers[0]
    for i, op in enumerate(operators):
        if op == '+':
            result += numbers[i + 1]
        elif op == '*':
            result *= numbers[i + 1]
        elif op == 'x':
            result = int(str(result) + str(numbers[i + 1]))
    return result

def main_code(file_name, part=1):
    data = read_txt_to_str(file_name, with_split="\n")

    final_score = 0

    for equation_ in data:
        test_value, numbers_ = equation_.split(": ")
        test_value = int(test_value)

        print(f"--EQUATION---: {equation_}")
        print(f"Target value: {test_value}")
        list_numbers = list(map(int, numbers_.split()))
        nb_operators = len(list_numbers)-1

        if part==1:
            operators_ = "+*"
        elif part==2:
            operators_ = "+*x"

        for operators in product(operators_, repeat=nb_operators):

            if evaluate_expression(list_numbers, operators) == test_value:
                final_score += test_value
                print(f"Let's add this {test_value} result: {final_score}")
                break
            
    return final_score

def main():
    day = 7
    expected_results = {1: 3749, 2: 11387} # fill this
    title = get_daily_title(day, BASE_DAY_URL, HEADERS)
    print(f"🧩 Starting puzzle for: {title}")
    run_part(day, 1, expected_results, main_code)
    run_part(day, 2, expected_results, main_code)

if __name__ == "__main__":
    main()
