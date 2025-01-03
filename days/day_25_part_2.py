import sys
from pathlib import Path

# Change the working directory to the root of the project
project_root = Path(__file__).resolve().parent.parent  # Two levels up to the root
sys.path.append(str(project_root))

from config import BASE_DAY_URL, HEADERS
from src.utils import get_daily_title, run_part, file_exists_and_rename
from src.read_data import read_txt_to_str, read_txt_vector_matrix_str


def count_hashtags_per_column(matrix):
    # Transpose the matrix to iterate over columns
    transposed_matrix = list(zip(*matrix))
    
    # Count the number of hashtags in each column
    hashtag_counts = [sum(row.count('#') for row in column) for column in transposed_matrix]
    
    return hashtag_counts


def main_code(file_name, part=1):
    data = read_txt_to_str(file_name, with_split="\n\n")
    n_cols = len(data[0].split()[0])
    n_rows = len(data[0].split())

    locker_lst = []
    key_lst = []
    for schematic_ in data:
        lst_ = schematic_.split()
        if lst_[0] == "#"*n_cols and lst_[-1] == "."*n_cols:
            locker_lst.append(count_hashtags_per_column(lst_))
        elif lst_[0] == "."*n_cols and lst_[-1] == "#"*n_cols:
            key_lst.append(count_hashtags_per_column(lst_))

    count_fit = 0
    for key_ in key_lst:
        for locker in locker_lst:
            total = [k + l for k, l in zip(key_, locker)]
            if all(t <= n_rows for t in total):
                count_fit += 1

    return count_fit


def main():
    day = 25
    expected_results = {1: 3, 2: None} # fill this
    title = get_daily_title(day, BASE_DAY_URL, HEADERS)
    print(f"🧩 Starting puzzle for: {title}")
    run_part(day, 1, expected_results, main_code)
    file_exists_and_rename(f"days/day_25_to_do.py", f"days/day_25_part_2.py")
    #run_part(day, 2, expected_results, main_code)
    #file_exists_and_rename(f"days/day_25_part_2.py", f"days/day_25.py")

if __name__ == "__main__":
    main()
