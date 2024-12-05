import sys
from pathlib import Path

# Change the working directory to the root of the project
project_root = Path(__file__).resolve().parent.parent  # Two levels up to the root
sys.path.append(str(project_root))

from config import BASE_DAY_URL, HEADERS
from src.utils import get_daily_title, run_part
from src.read_data import read_txt_to_str
import re

def apply_multiplication(str_):
    a, b  = map(int, re.findall(r'\d+', str_))
    return a * b

def main_code(file_name, part=1):

    data = read_txt_to_str(file_name)
    
    if part == 1:
        pattern = r"mul\((\d+),(\d+)\)"
        matches = re.findall(pattern, data)
        multiply_ = [int(match[0]) * int(match[1]) for match in matches]
    else:
        pattern = r"mul\(\d+,\d+\)|do\(\)|don't\(\)"
        matches = re.findall(pattern, data)

        multiply_ = []
        inside_do_block = True
        for item in matches:
            if "don't()" in item:
                inside_do_block = False
            elif "do()" in item:
                inside_do_block = True
            elif inside_do_block and "mul" in item:
                multiply_.append(apply_multiplication(item))

    return sum(multiply_)


def main():
    day = 3
    expected_results = {1: 161, 2:48}
    title = get_daily_title(day, BASE_DAY_URL, HEADERS)
    print(f"🧩 Starting puzzle for: {title}")
    run_part(day, 1, expected_results, main_code)
    run_part(day, 2, expected_results, main_code)

if __name__ == "__main__":
    main()
