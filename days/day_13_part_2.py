import sys
from pathlib import Path

# Change the working directory to the root of the project
project_root = Path(__file__).resolve().parent.parent  # Two levels up to the root
sys.path.append(str(project_root))

from config import BASE_DAY_URL, HEADERS, DAYS_DIR
from src.utils import get_daily_title, run_part, file_exists_and_rename
from src.read_data import read_txt_to_str
from pathlib import Path

def execute_problem_solving(a_, b_, target, letter, part):

    a_ = int(a_.replace(f"{letter}+", ""))
    b_ = int(b_.replace(f"{letter}+", ""))
    target = int(target.replace(f"{letter}=", ""))
    if part==2:
        target = 10000000000000 + target
        max_a = min(100, target // a_)
    else:
        max_a = 100

    solutions = []
    for a in range(max_a + 1): #target // a_coef + 1
        remainder = target - a_ * a
        if remainder % b_ == 0:  # Check if b is an integer
            b = remainder // b_
            if b >= 0:  # Ensure b is non-negative
                score = a*3 + b*1
                solutions.append((a, b, score))

    return set(solutions)


def main_code(file_name, part=1):
    list_machines = read_txt_to_str(file_name, with_split="\n\n")
    final_score = 0
    for claw_machine in list_machines:

        print(claw_machine)
        instructions_ =  [tuple(value_.split(":")[1].strip().split(",")) for value_ in claw_machine.split("\n")]

        x_a, y_a = instructions_[0]
        x_b, y_b = instructions_[1]
        x, y = instructions_[2]

        solutions_x = execute_problem_solving(x_a, x_b, x, letter="X", part=part)
        solutions_y = execute_problem_solving(y_a, y_b, y, letter="Y", part=part)

        inter_ = list(solutions_x&solutions_y)
        if inter_:
            final_score += min(inter_, key=lambda x: x[2])[2]

    return final_score


def main():
    day = 13
    expected_results = {1: 480, 2: None} # fill this
    title = get_daily_title(day, BASE_DAY_URL, HEADERS)
    
    print(f"🧩 Starting puzzle for: {title}")
    #run_part(day, 1, expected_results, main_code)
    #file_exists_and_rename(f"days/day_{day}_to_do.py", f"days/day_{day}_part_2.py")

    run_part(day, 2, expected_results, main_code)
    file_exists_and_rename(f"days/day_{day}_part_2.py", f"days/day_{day}.py")


if __name__ == "__main__":
    main()
