import os
from pathlib import Path
from src.utils import get_input
from config import BASE_DAY_URL, HEADERS, DAYS_DIR

DAY_TEMPLATE = """import sys
from pathlib import Path

# Change the working directory to the root of the project
project_root = Path(__file__).resolve().parent.parent  # Two levels up to the root
sys.path.append(str(project_root))

from config import BASE_DAY_URL, HEADERS
from src.utils import get_daily_title, run_part, file_exists_and_rename
from src.read_data import read_txt_to_str, read_txt_vector_matrix_str

def main_code(file_name, part=1):
    data = read_txt_to_str(file_name, with_split=None)
    pass


def main():
    day = {day}
    expected_results = {{1: None, 2: None}} # fill this
    title = get_daily_title(day, BASE_DAY_URL, HEADERS)
    print(f"🧩 Starting puzzle for: {{title}}")
    run_part(day, 1, expected_results, main_code)
    file_exists_and_rename(f"days/day_{day}_to_do.py", f"days/day_{day}_part_2.py")
    run_part(day, 2, expected_results, main_code)
    file_exists_and_rename(f"days/day_{day}_part_2.py", f"days/day_{day}.py")

if __name__ == "__main__":
    main()
"""

def create_day(day, part):
    day_file = Path(DAYS_DIR) / f"day_{day}_to_do.py"
    day_part = Path(DAYS_DIR) / f"day_{day}_part_2.py"
    get_input(int(day), BASE_DAY_URL, "test", HEADERS, part=int(part))
    get_input(int(day), BASE_DAY_URL, "input", HEADERS, part=int(part))

    # Create folders if they don't exist
    os.makedirs(DAYS_DIR, exist_ok=True)

    # Create day script if it doesn't exist
    if not day_file.exists() and not day_part.exists():
        with open(day_file, "w") as file:
            file.write(DAY_TEMPLATE.format(day=day))
        print(f"Created {day_file}")

if __name__ == "__main__":

    day = input("Enter the day number: ")
    part = input("What part are you in: ")

    create_day(day, part)