import sys
from pathlib import Path

# Change the working directory to the root of the project
project_root = Path(__file__).resolve().parent.parent  # Two levels up to the root
sys.path.append(str(project_root))

from config import BASE_DAY_URL, HEADERS
from src.utils import get_daily_title, run_part
from src.read_data import read_txt_to_str
import string
from itertools import combinations
from tqdm import tqdm


def extract_frequencies(data):
    lower_freq = []
    upper_freq = []
    digit_freq = []

    for i, row in enumerate(data):
        for j, element in enumerate(row):
            if element in string.ascii_lowercase:  # Check for lowercase
                lower_freq.append((i, j, element))
            elif element in string.ascii_uppercase:  # Check for uppercase
                upper_freq.append((i, j, element))
            elif element.isdigit():  # Check for digit
                digit_freq.append((i, j, element))
    
    return lower_freq, upper_freq, digit_freq


def between_bounds(node, max_x, max_y):
    return 0 <= node[0] < max_x and 0 <= node[1] < max_y


def add_antinode_positions(node_x, node_y, dist_x, dist_y, len_rows, len_cols, antinode_positions):
    while True:
        antinode = (node_x + dist_x, node_y + dist_y)
        if between_bounds(antinode, len_rows, len_cols):
            antinode_positions.add(antinode)
            node_x, node_y = antinode
        else:
            break
    
    return antinode_positions


def main_code(file_name, part=1):
    data = read_txt_to_str(file_name, with_split="\n")
    len_rows, len_cols = (len(data), len(data[0]))

    # Extract frequencies
    lower_freq, upper_freq, digit_freq = extract_frequencies(data)
    all_frequencies = {'lower': lower_freq, 'upper': upper_freq, 'digit': digit_freq}

    antinode_positions = set()
    for freq_type, antennas in all_frequencies.items():
        print(f"Current frequency: {freq_type}")
        if not antennas:
            continue
        
        for pair in tqdm(combinations(antennas, 2)):
            print(f"Current pair: {pair}")
            frequency = pair[0][2]

            (x1, y1, freq1), (x2, y2, freq2) = pair
            if freq1 == frequency and freq2 == frequency:

                dist_x, dist_y = (abs(x1-x2), abs(y1-y2))
                nodea_x, nodea_y = min((x1, y1),  (x2, y2))
                nodeb_x, nodeb_y = max((x1, y1),  (x2, y2))


                if part==1:

                    if x1<x2 and y1>y2:
                        antinode_a = (nodea_x-dist_x, nodea_y+dist_y)
                        antinode_b = (nodeb_x+dist_x, nodeb_y-dist_y)

                    elif x1<=x2 and y1<=y2:
                        antinode_a = (nodea_x-dist_x, nodea_y-dist_y)
                        antinode_b = (nodeb_x+dist_x, nodeb_y+dist_y)

                    if between_bounds(antinode_a, len_rows, len_cols):
                        antinode_positions.add(antinode_a)

                    if between_bounds(antinode_b, len_rows, len_cols):
                        antinode_positions.add(antinode_b)

                else:
                    if x1<x2 and y1>y2:
                        antinode_positions.add((nodea_x, nodea_y))
                        add_antinode_positions(nodea_x, nodea_y, -dist_x, dist_y, len_rows, len_cols, antinode_positions)

                        antinode_positions.add((nodeb_x, nodeb_y))
                        add_antinode_positions(nodeb_x, nodeb_y, dist_x, -dist_y, len_rows, len_cols, antinode_positions)

                    elif x1<=x2 and y1<=y2:
                        antinode_positions.add((nodea_x, nodea_y))
                        add_antinode_positions(nodea_x, nodea_y, -dist_x, -dist_y, len_rows, len_cols, antinode_positions)
                        antinode_positions.add((nodeb_x, nodeb_y))
                        add_antinode_positions(nodeb_x, nodeb_y, dist_x, dist_y, len_rows, len_cols, antinode_positions)

    return len(antinode_positions)


def main():
    day = 8
    expected_results = {1: 14, 2: 34} # fill this
    title = get_daily_title(day, BASE_DAY_URL, HEADERS)
    print(f"🧩 Starting puzzle for: {title}")
    run_part(day, 1, expected_results, main_code)
    run_part(day, 2, expected_results, main_code)

if __name__ == "__main__":
    main()
