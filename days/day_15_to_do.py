import sys
from pathlib import Path

# Change the working directory to the root of the project
project_root = Path(__file__).resolve().parent.parent  # Two levels up to the root
sys.path.append(str(project_root))

from config import BASE_DAY_URL, HEADERS
from src.utils import get_daily_title, run_part, file_exists_and_rename
from src.read_data import read_txt_to_str, read_txt_vector_matrix_str
from src.tools import DIRECTIONS

def fetch_positions(data_):

    positions = {
    '#': [],
    '@': [],
    'O': []}

    # Iterate over each row and column to get the positions
    for row_idx, row in enumerate(data_):
        for col_idx, char in enumerate(row):
            if char in positions:
                positions[char].append((row_idx, col_idx))


    return positions


def move_boxes(boxes, dx, dy, start_pos, set_walls):

    updated_boxes = boxes.copy()
    updated_boxes = sorted(updated_boxes)
    idx = updated_boxes.index(start_pos)

    moved_any = False  # Flag to check if any box has moved

    # Start moving the box from the specified position
    while idx < len(updated_boxes):
        # Find the current box position
        current_pos = updated_boxes[idx]
        # Try moving it 1 step to the right
        new_pos = (current_pos[0] + dx, current_pos[1] + dy)
        nex_pos = (new_pos[0] + dx, new_pos[1] + dy)
        
        # Check if the new position is valid and not occupied by another box
        if new_pos in set_walls:
            break

        if nex_pos in set_walls:
            break

        if new_pos in updated_boxes:
            updated_boxes[idx] = new_pos
            idx += 1
            continue
                    
        updated_boxes[idx] = new_pos
        moved_any = True

        break

    return updated_boxes, moved_any



def main_code(file_name, part=1):
    map_, moves_ = read_txt_to_str(file_name, with_split="\n\n")
    map_ = map_.split("\n")
    moves_ = moves_.replace("\n", "")

    moves_direct_ = dict(zip(["^", "v", ">", "<"], DIRECTIONS.vert_horiz_directions()))

    positions_ = fetch_positions(map_)
    rob_x, rob_y = positions_['@'][0]
    print(f"🤖 is in the 🎬 position {rob_x, rob_y}")
    for mov_ in moves_:
        print(f"Lets move to {mov_}")
        dx, dy = moves_direct_[mov_]

        new_pos = (rob_x+dx, rob_y+dy)
        if not new_pos in positions_['#']:

            # update boxes if there is any to update
            if new_pos in positions_['O']:

                positions_['O'], moved_any = move_boxes(positions_['O'], dx, dy, new_pos, set(positions_['#']))

                rob_x, rob_y = new_pos if moved_any else (rob_x, rob_y)

            else:
                rob_x, rob_y = new_pos
        else:
            print(f"🛑 there is a wall!!")

        print(f"🤖 is in the current position {rob_x, rob_y}")

    final_score = sum([100 * box_[0] + box_[1] for box_ in positions_['O']])

    return final_score


def main():
    day = 15
    expected_results = {1: 10092, 2: None} # fill this
    title = get_daily_title(day, BASE_DAY_URL, HEADERS)
    print(f"🧩 Starting puzzle for: {title}")
    run_part(day, 1, expected_results, main_code)
    #file_exists_and_rename(f"days/day_15_to_do.py", f"days/day_15_part_2.py")
    #run_part(day, 2, expected_results, main_code)
    #file_exists_and_rename(f"days/day_15_part_2.py", f"days/day_15.py")

if __name__ == "__main__":
    main()
