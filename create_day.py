import os
from pathlib import Path
from src.utils import get_input
from config import BASE_DAY_URL, HEADERS

DAY_TEMPLATE = """import sys
from pathlib import Path

# Change the working directory to the root of the project
project_root = Path(__file__).resolve().parent.parent  # Two levels up to the root
sys.path.append(str(project_root))

from config import BASE_DAY_URL, HEADERS
from src.utils import get_daily_title, submit_answer
import time

def main_code(data, part=1):
    pass

def process_data(file_name, part):
    with open(file_name, "r") as file:
        data = file.read()
    return main_code(data, part)

def run_part(day, part, expected_results):
    start_time = time.time()
    test_result = process_data(f"data/test/day_{{day}}_part_{{part}}.txt", part)
    elapsed_time = time.time() - start_time
    
    rint(f"Time taken for test part {{part}}: {{elapsed_time:.2f}} seconds")
    if test_result == expected_results[part]:
        start_time = time.time()
        print(f"Part {{part}} test passed!")

        final_result = process_data(f"data/input/day_{{day}}_part_{{part}}.txt", part)
        print(f"Submitting result for part {{part}}: {{final_result}}")
        submit_answer(day, part, final_result)
        elapsed_time = time.time() - start_time
        rint(f"Time taken for final part {{part}}: {{elapsed_time:.2f}} seconds")
    else:
        print(f"Part {{part}} test failed. Expected {{expected_results[part]}}, got {{test_result}}.")

def main():
    day = {day}
    expected_results = {{1: None, 2: None}} # fill this
    title = get_daily_title(day, BASE_DAY_URL, HEADERS)
    print(f"Starting puzzle for day {{day}}: {{title}}")
    run_part(day, 1, expected_results)
    run_part(day, 2, expected_results)

if __name__ == "__main__":
    main()
"""
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


def create_day(day, part):
    DAYS_DIR = "days"
    day_file = Path(DAYS_DIR) / f"day_{day}.py"
    get_input(int(day), BASE_DAY_URL, "test", HEADERS, part=int(part))
    get_input(int(day), BASE_DAY_URL, "input", HEADERS, part=int(part))

    # Create folders if they don't exist
    os.makedirs(DAYS_DIR, exist_ok=True)

    # Create day script if it doesn't exist
    if not day_file.exists():
        with open(day_file, "w") as file:
            file.write(DAY_TEMPLATE.format(day=day))
        print(f"Created {day_file}")

if __name__ == "__main__":

    day = input("Enter the day number: ")
    part = input("What part are you in: ")

    create_day(day, part)