import sys
from pathlib import Path

# Change the working directory to the root of the project
project_root = Path(__file__).resolve().parent.parent  # Two levels up to the root
sys.path.append(str(project_root))

from config import BASE_DAY_URL, HEADERS
from src.utils import get_daily_title, run_part
from src.read_data import read_txt_vector_matrix


def all_increasing(vector):
    return all(vector[i] > vector[i + 1] for i in range(len(vector) - 1))

def all_decreasing(vector):
    return all(vector[i] < vector[i + 1] for i in range(len(vector) - 1))

def pairwise_distances(vector):
    return all([abs(vector[i + 1] - vector[i]) <= 3 and abs(vector[i + 1] - vector[i]) >= 1 for i in range(len(vector) - 1)])

def if_safe_report(vector):
    return (all_increasing(vector) or all_decreasing(vector)) and pairwise_distances(vector)
    

def pairwise_distances_exclude_one(vector):
    results = []
    for i in range(len(vector)):
        # Exclude the i-th element
        modified_vector = vector[:i] + vector[i+1:]
        if if_safe_report(modified_vector):
            results.append(True)

    return any(results)


def main_code(file_name, part=1):
    """
    Logic for part 2: 
        * The levels are either all increasing or all decreasing.
        * Any two adjacent levels differ by at least one and at most three.

    EXTRA: if removing a single level from an unsafe report would make it safe, 
    the report instead counts as safe.
    """

    data = read_txt_vector_matrix(file_name)

    safe_count = 0
    for vector in data:
        if if_safe_report(vector):
            safe_count += 1

        else:
            if part == 2 and pairwise_distances_exclude_one(vector):
                safe_count += 1

    return safe_count


def main():
    day = 2
    expected_results = {1: 2, 2:4}
    title = get_daily_title(day, BASE_DAY_URL, HEADERS)
    print(f"🧩 Starting puzzle for: {title}")
    run_part(day, 1, expected_results, main_code)
    run_part(day, 2, expected_results, main_code)

if __name__ == "__main__":
    main()
