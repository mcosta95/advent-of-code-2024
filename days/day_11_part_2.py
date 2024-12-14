import sys
from pathlib import Path

# Change the working directory to the root of the project
project_root = Path(__file__).resolve().parent.parent  # Two levels up to the root
sys.path.append(str(project_root))

from config import BASE_DAY_URL, HEADERS
from src.utils import get_daily_title, run_part
from src.read_data import read_txt_to_str
from collections import Counter


def non_otimized_rules(init_array):
    
    curr_array = []
    for s in init_array:
        # rule 1
        if s == "0":
            curr_array.append("1")

        # rule 2
        elif len(s) % 2 == 0:
            midpoint = len(s) // 2
            curr_array.extend([str(int(s[:midpoint])), str(int(s[midpoint:]))])

        # rule 3
        else:
            curr_array.append(str(int(s) * 2024))

    return curr_array


def optimized_rules(init_array):
    curr_array = []
    counter = Counter(init_array)  # Track how many times each element appears

    for s, count in counter.items():
        if s == "0":
            # Rule 1: If 's' is "0", add '1' count times
            curr_array.extend(["1"] * count)

        elif len(s) % 2 == 0:
            # Rule 2: If length of 's' is even, split and process the first and second half
            midpoint = len(s) // 2
            first_half = str(int(s[:midpoint]))
            second_half = str(int(s[midpoint:]))
            curr_array.extend([first_half] * count)
            curr_array.extend([second_half] * count)

        else:
            # Rule 3: If length of 's' is odd, multiply it by 2024
            curr_array.extend([str(int(s) * 2024)] * count)

    return curr_array


def main_code(file_name, part=1):

    nr_blinks = 25 if part == 1 else 75

    # Convert initial array to integers
    init_array = [x for x in read_txt_to_str(file_name, with_split=" ")]

    curr_blink = 1
        
    while curr_blink <= nr_blinks:

        #curr_array = non_otimized_rules(init_array)
        init_array = optimized_rules(init_array)

        curr_blink += 1

    return len(init_array)


def main():
    day = 11
    expected_results = {1: 55312, 2: None} # fill this
    title = get_daily_title(day, BASE_DAY_URL, HEADERS)
    print(f"🧩 Starting puzzle for: {title}")
    run_part(day, 1, expected_results, main_code)
    run_part(day, 2, expected_results, main_code)

if __name__ == "__main__":
    main()
