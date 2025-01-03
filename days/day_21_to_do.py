import sys
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
    day = 21
    expected_results = {1: None, 2: None} # fill this
    title = get_daily_title(day, BASE_DAY_URL, HEADERS)
    print(f"🧩 Starting puzzle for: {title}")
    run_part(day, 1, expected_results, main_code)
    file_exists_and_rename(f"days/day_21_to_do.py", f"days/day_21_part_2.py")
    #run_part(day, 2, expected_results, main_code)
    #file_exists_and_rename(f"days/day_21_part_2.py", f"days/day_21.py")

if __name__ == "__main__":
    main()
