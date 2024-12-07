import sys
from pathlib import Path

# Change the working directory to the root of the project
project_root = Path(__file__).resolve().parent.parent  # Two levels up to the root
sys.path.append(str(project_root))

from config import BASE_DAY_URL, HEADERS
from src.utils import get_daily_title, run_part
from src.read_data import read_txt_to_str
from src.tools import DIRECTIONS


def found_positions_based_on_value(matrix, value_position, value_start_lst):

    positions = []
    start_position = None
    for row_idx, row in enumerate(matrix):
        for col_idx, cell in enumerate(row):
            if cell == value_position:
                positions.append((row_idx, col_idx))
            elif cell in value_start_lst:
                start_position = cell, row_idx, col_idx

    return positions, start_position


def get_next_direction(values, current_value):
    index = values.index(current_value)  # Find the current index
    next_index = (index + 1) % len(values)  # Circular next index
    return values[next_index]  # Get the next value


def find_distance_path(start, target, direction):

    """Efficiently calculate all positions from start to target."""
    start_x, start_y = start
    target_x, target_y = target
    dx, dy = direction

    # Calculate number of steps needed in each direction
    steps = max(abs(target_x - start_x) // abs(dx) if dx != 0 else 0,
                abs(target_y - start_y) // abs(dy) if dy != 0 else 0)

    # Generate all positions using list comprehension
    path = [(start_x + i * dx, start_y + i * dy) for i in range(steps + 1)]
    return path
  
def find_valid_positions(dx, dy, start_x, start_y, positions, len_matrix):

    valid_positions = []
    for px, py in positions:
        if dy == 0: # moving vertical
            if py == start_y and ((px - start_x) * dx > 0):
                valid_positions.append((px, py))

        elif dx == 0: # moving horizontal
            if px == start_x and ((py - start_y) * dy > 0):
                valid_positions.append((px, py))
        #elif dx != 0 and dy != 0:  # Moving diagonally
        #    if (px - start_x) * dx > 0 and (py - start_y) * dy > 0:  # Correct diagonal direction
        #        valid_targets.append((px, py))

    if not valid_positions:

        if dx == 0:
            new_x = start_x
            new_y = len_matrix*dy if len_matrix*dy > 0 else 0

        elif dy == 0:
            new_x = len_matrix*dx if len_matrix*dx > 0 else 0
            new_y = start_y

        return False, (new_x, new_y)
    
    if len(valid_positions) > 1:
        
        if dx == 0:
            if dy < 0:
                new_x, new_y = max(valid_positions)
            else:
                new_x, new_y = min(valid_positions)  

        elif dy == 0:
            if dx < 0:
                new_x, new_y = max(valid_positions)
            else:
                new_x, new_y = min(valid_positions)
    else:
        new_x, new_y = valid_positions[0]
    a=1
    
    return True, (new_x, new_y)


def main_code(data, part=1):

    create_directions = DIRECTIONS.arrow_directions()
    len_matrix = len(data)-1
    positions, start_position_values = found_positions_based_on_value(data, 
                                                               value_position="#", 
                                                               value_start_lst=create_directions.keys())
    

    arrow_, start_x, start_y  = start_position_values
    dx, dy = create_directions[arrow_]
    distance = []
    valid_positions = True
    iter_ = 0
    while valid_positions:
        valid_positions, (new_x, new_y) = find_valid_positions(dx, dy, start_x, start_y, positions, len_matrix)
        path_ = find_distance_path((start_x, start_y ), (new_x, new_y), (dx, dy))[:-1]
        distance.extend(path_)

        print(f"iter: {iter_}")
        print(f"start_position: {(start_x, start_y)}")
        print(f"target_position: {(new_x, new_y)}")
        print(f"direction: {(dx, dy)}")
        print(f"")
    
        start_x, start_y = abs(new_x - dx), abs(new_y - dy)
        dx, dy = get_next_direction(list(create_directions.values()), (dx, dy))
        iter_ += 1

    return len(set(distance))+1  #add the last one

def process_data(file_name, part):
    data = read_txt_to_str(file_name, with_split='\n')
    return main_code(data, part)

def main():
    day = 6
    expected_results = {1: 41, 2: None} # fill this
    title = get_daily_title(day, BASE_DAY_URL, HEADERS)
    print(f"🧩 Starting puzzle for: {title}")
    run_part(day, 1, expected_results, process_data)
    # run_part(day, 2, expected_results, process_data)

if __name__ == "__main__":
    main()
