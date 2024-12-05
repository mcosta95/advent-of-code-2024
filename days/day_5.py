import sys
from pathlib import Path
import math
import time

# Change the working directory to the root of the project
project_root = Path(__file__).resolve().parent.parent  # Two levels up to the root
sys.path.append(str(project_root))

from config import BASE_DAY_URL, HEADERS
from src.utils import get_daily_title, submit_answer


def is_valid_order(upd_, rules_set):

    for idx in range(len(upd_)-1):
        for val_ in upd_[idx+1:]:
            if f"{upd_[idx]}|{val_}" not in rules_set:
               return False, (upd_[idx], val_)
    return True, None


def main_code(rules_, updates_, part=1):
    score = 0
    rules_ = set(rules_)
    for upd_ in updates_:
        upd_ = upd_.split(",")

        validation, pair = is_valid_order(upd_, rules_)

        if part == 1 and validation:
            score += int(upd_[math.ceil(len(upd_)/2)-1])

        if part == 2 and not validation:

            while not validation:
                first, second = pair

                if f"{second}|{first}" in rules_:
                    upd_ = [second if x == first else first if x == second else x for x in upd_]
                    validation, pair = is_valid_order(upd_, rules_)
                else:
                    break

            if validation:
                score += int(upd_[math.ceil(len(upd_)/2) - 1])

    return score


def process_data(file_name, part):
    with open(file_name, "r") as file:
        rules_, updates_ = file.read().split("\n\n")

    rules_ = rules_.split("\n")
    updates_ = updates_.split("\n")
    return main_code(rules_, updates_, part)


def run_part(day, part, expected_results):

    start_time = time.time()
    test_result = process_data(f"data/test/day_{day}_part_{part}.txt", part)
    elapsed_time = time.time() - start_time
    print(f"Time taken for test part {part}: {elapsed_time:.2f} seconds")
    
    if test_result == expected_results[part]:

        start_time = time.time()
        print(f"Part {part} test passed!")
        final_result = process_data(f"data/input/day_{day}_part_{part}.txt", part)
        print(f"Submitting result for part {part}: {final_result}")
        submit_answer(day, part, final_result)
        print(f"Time taken for final part {part}: {elapsed_time:.2f} seconds")
    else:
        print(f"Part {part} test failed. Expected {expected_results[part]}, got {test_result}.")


def main():
    day = 5
    expected_results = {1: 143, 2: 123}
    title = get_daily_title(day, BASE_DAY_URL, HEADERS)
    print(f"Starting puzzle for day {day}: {title}")
    run_part(day, 1, expected_results)
    run_part(day, 2, expected_results)

if __name__ == "__main__":
    main()
