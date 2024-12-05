import sys
from pathlib import Path
import math

# Change the working directory to the root of the project
project_root = Path(__file__).resolve().parent.parent  # Two levels up to the root
sys.path.append(str(project_root))

from config import BASE_DAY_URL, HEADERS
from src.utils import get_daily_title, run_part
from src.read_data import read_txt_to_str


def is_valid_order(upd_, rules_set):
    for idx in range(len(upd_)-1):
        for val_ in upd_[idx+1:]:
            if f"{upd_[idx]}|{val_}" not in rules_set:
               return False, (upd_[idx], val_)
    return True, None


def main_code(file_name, part=1):

    rules_, updates_ = read_txt_to_str(file_name, with_split="\n\n")
    rules_ = rules_.split("\n")
    updates_ = updates_.split("\n")

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


def main():
    day = 5
    expected_results = {1: 143, 2: 123}
    title = get_daily_title(day, BASE_DAY_URL, HEADERS)
    print(f"🧩 Starting puzzle for: {title}")
    run_part(day, 1, expected_results, main_code)
    run_part(day, 2, expected_results, main_code)

if __name__ == "__main__":
    main()