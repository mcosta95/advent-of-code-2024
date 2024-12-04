import sys
from pathlib import Path

# Change the working directory to the root of the project
project_root = Path(__file__).resolve().parent.parent  # Two levels up to the root
sys.path.append(str(project_root))

from config import BASE_DAY_URL, HEADERS
from src.utils import get_daily_title, submit_answer
from src.tools import ALL_DIRECTIONS, DIAGONAL_DIRECTIONS
from collections import Counter

def is_valid_position(x, y, rows, cols):
    return 0 <= x < rows and 0 <= y < cols


def build_matrix(data, word_build, start_letter, directions, part):
    count_ = 0
    rows, cols = len(data), len(data[0])
    final_matrix = [['.' for _ in range(cols)] for _ in range(rows)]

    for row_ in range(rows):
        for col_ in range(cols):
            if data[row_][col_] == start_letter:

                # transform this part on a function
                for direction in directions:
                    dx, dy = direction
                    curr_word = start_letter
                    for i in range(1, len(word_build)):
                        idx_x, idx_y = row_ + dx*i, col_ + dy*i
                        if not is_valid_position(idx_x, idx_y, rows, cols) or data[idx_x][idx_y] != word_build[i]:
                            break
                        else:
                            curr_word +=  word_build[i]

                    if curr_word == word_build:
                        for i in range(len(word_build)):
                            idx_x, idx_y = row_ + dx * i, col_ + dy * i
                            final_matrix[idx_x][idx_y] = word_build[i]
                        
                        count_ += 1 
                        print(f"We already have: {count_}")
                    

    return final_matrix, count_


def find_mas_x(data, directions_):
    count = 0
    rows, cols = len(data), len(data[0])

    for row in range(1, rows - 1):
        for col in range(1, cols - 1):
            if data[row][col] == "A":
                vect_bool = [data[row + dir_[0]][col + dir_[1]] in ['M', 'S'] for dir_ in directions_]

                if all(vect_bool):
                    vect_letter = [data[row + dir_[0]][col + dir_[1]] for dir_ in directions_]
                    vect_letter_count = Counter(vect_letter)
                    if vect_letter_count['M'] == 2 and vect_letter_count['S'] == 2:
                        count+=1

    return count


def main_code(data, part=1):


    
    if part==1:
        _, score_ = build_matrix(data, word_build="XMAS", start_letter="X", directions=ALL_DIRECTIONS, part=part)

    else:
        matrix_, _ = build_matrix(data, word_build="MAS", start_letter="M", directions=DIAGONAL_DIRECTIONS, part=part)
        score_ = find_mas_x(matrix_, DIAGONAL_DIRECTIONS)

    return score_


def process_data(file_name, part):
    with open(file_name, "r") as file:
        data = [list(line.strip()) for line in file]
    return main_code(data, part)

def run_part(day, part, expected_results):

    test_result = process_data(f"data/test/day_{day}_part_{part}.txt", part)
    
    if test_result == expected_results[part]:
        print(f"Part {part} test passed!")

        final_result = process_data(f"data/input/day_{day}_part_{part}.txt", part)
        print(f"Submitting result for part {part}: {final_result}")
        submit_answer(day, part, final_result)
    else:
        print(f"Part {part} test failed. Expected {expected_results[part]}, got {test_result}.")

def main():
    day = 4
    expected_results = {1: 18, 2: 9} # fill this
    title = get_daily_title(day, BASE_DAY_URL, HEADERS)
    print(f"Starting puzzle for day {day}: {title}")
    run_part(day, 1, expected_results)
    run_part(day, 2, expected_results)

if __name__ == "__main__":
    main()
