import sys
from pathlib import Path

# Change the working directory to the root of the project
project_root = Path(__file__).resolve().parent.parent  # Two levels up to the root
sys.path.append(str(project_root))

from config import BASE_DAY_URL, HEADERS
from src.utils import get_daily_title, run_part
from src.tools import DIRECTIONS
from src.read_data import read_txt_vector_matrix_str
from collections import Counter


def is_valid_position(x, y, rows, cols):
    return 0 <= x < rows and 0 <= y < cols


def build_matrix(data, word_build, start_letter, directions):
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


def main_code(file_name, part=1):

    data = read_txt_vector_matrix_str(file_name)

    if part==1:
        _, score_ = build_matrix(data, word_build="XMAS", start_letter="X", directions=DIRECTIONS.all_directions())

    else:
        matrix_, _ = build_matrix(data, word_build="MAS", start_letter="M", directions=DIRECTIONS.diagonal_directions())
        score_ = find_mas_x(matrix_, DIRECTIONS.diagonal_directions())

    return score_


def main():
    day = 4
    expected_results = {1: 18, 2: 9}
    title = get_daily_title(day, BASE_DAY_URL, HEADERS)
    print(f"🧩 Starting puzzle for: {title}")
    run_part(day, 1, expected_results, main_code)
    run_part(day, 2, expected_results, main_code)

if __name__ == "__main__":
    main()
