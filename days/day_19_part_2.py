import sys
from pathlib import Path

# Change the working directory to the root of the project
project_root = Path(__file__).resolve().parent.parent  # Two levels up to the root
sys.path.append(str(project_root))

from config import BASE_DAY_URL, HEADERS
from src.utils import get_daily_title, run_part, file_exists_and_rename
from src.read_data import read_txt_to_str


def can_make_design(design, patterns):
    if not design:
        return True
    for pattern in patterns:
        if design.startswith(pattern):
            if can_make_design(design[len(pattern):], patterns):
                return True
    return False


def main_code(file_name, part=1):
    towel_patterns_available, design_ = read_txt_to_str(file_name, with_split="\n\n")
    designs = design_.split("\n")
    patterns = towel_patterns_available.split(", ")

    possible_score = 0
    for design in designs:
        if can_make_design(design, patterns):
            possible_score += 1
            print(f"{design} can be made")
        else:
            print(f"{design} is impossible")

    return possible_score


def main():
    day = 19
    expected_results = {1: 6, 2: None} # fill this
    title = get_daily_title(day, BASE_DAY_URL, HEADERS)
    print(f"🧩 Starting puzzle for: {title}")
    run_part(day, 1, expected_results, main_code)
    file_exists_and_rename(f"days/day_19_to_do.py", f"days/day_19_part_2.py")
    #run_part(day, 2, expected_results, main_code)
    #file_exists_and_rename(f"days/day_19_part_2.py", f"days/day_19.py")

if __name__ == "__main__":
    main()
