import sys
from pathlib import Path

# Change the working directory to the root of the project
project_root = Path(__file__).resolve().parent.parent  # Two levels up to the root
sys.path.append(str(project_root))

from config import BASE_DAY_URL, HEADERS
from src.utils import get_daily_title, run_part, file_exists_and_rename
from src.read_data import read_txt_to_str
from collections import Counter
from math import ceil

def process_input_data(data):
    positions_ = [i.split(" ")[0] for i in data]
    positions_ = [tuple(i.replace("p=", "").split(",")) for i in positions_]
    positions_ = [(int(x), int(y)) for x, y in positions_]

    velocities_ = [i.split(" ")[1] for i in data]
    velocities_ = [tuple(i.replace("v=", "").split(",")) for i in velocities_]
    velocities_ = [(int(x), int(y)) for x, y in velocities_]
    
    return positions_, velocities_

def main_code(file_name, part=1):
    data = read_txt_to_str(file_name, with_split="\n")
    positions_, velocities_ = process_input_data(data)

    tall_len = max(positions_, key=lambda x: x[1])[1]+1
    wide_len = max(positions_, key=lambda x: x[0])[0]+1

    final_positions = []
    for pos_, vel_ in zip(positions_, velocities_):

        vx, vy = vel_
        px, py = pos_

        total_sec = 100
        for curr_sec in range(1, total_sec + 1):

            print(f"Current second {curr_sec}")
            px += vx
            if px < 0:
                px += wide_len
            elif px >= wide_len:
                px -= wide_len

            py += vy
            if py < 0:
                py += tall_len
            elif py >= tall_len:
                py -= tall_len

        print(f"Current position {(px, py)}")
        final_positions.append((px, py))
        

    counter_positions = Counter(final_positions)
    x_x = ceil(wide_len/2)-1
    y_y = ceil(tall_len/2)-1

    # limites dos quadrantes
    q1_score = sum(value for (x, y), value in counter_positions.items() if x < x_x and y < y_y)
    q2_score = sum(value for (x, y), value in counter_positions.items() if x > x_x and y < y_y)
    q3_score = sum(value for (x, y), value in counter_positions.items() if x < x_x and y > y_y)
    q4_score = sum(value for (x, y), value in counter_positions.items() if x > x_x and y > y_y)

    return q1_score*q2_score*q3_score*q4_score


def main():
    day = 14
    expected_results = {1: 12, 2: None} # fill this
    title = get_daily_title(day, BASE_DAY_URL, HEADERS)
    print(f"🧩 Starting puzzle for: {title}")
    run_part(day, 1, expected_results, main_code)
    file_exists_and_rename(f"days/day_14_to_do.py", f"days/day_14_part_2.py")
    #run_part(day, 2, expected_results, main_code)
    #file_exists_and_rename(f"days/day_14_part_2.py", f"days/day_14.py")

if __name__ == "__main__":
    main()
