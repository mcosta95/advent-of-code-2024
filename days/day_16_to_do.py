import sys
from pathlib import Path

# Change the working directory to the root of the project
project_root = Path(__file__).resolve().parent.parent  # Two levels up to the root
sys.path.append(str(project_root))

from config import BASE_DAY_URL, HEADERS
from src.utils import get_daily_title, run_part, file_exists_and_rename
from src.read_data import read_txt_vector_matrix_str
import networkx as nx
from multiprocessing import Pool
import numpy as np

def found_positions_based_on_value(data, value_position, value_start, value_end):

    rows, cols = len(data), len(data[0])
    possible_positions = []
    start_position = None
    end_position = None
    for x in range(rows):
        for y in range(cols):
            curr_value = data[x][y]
            if curr_value == value_start:
                start_position = (x, y)
                possible_positions.append(start_position)
            elif curr_value == value_end:
                end_position = (x, y)
                possible_positions.append(end_position)
            elif curr_value == value_position:
                possible_positions.append((x, y))

    return possible_positions, start_position, end_position


def build_graph(data, possible_positions):

    rows, cols = len(data), len(data[0])
    G = nx.Graph()

    for x in range(rows):
        for y in range(cols):
            if (x, y) in possible_positions:
                neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
                G.add_node((x, y))
                for neighbor in neighbors:
                    if (neighbor in possible_positions and 
                        0 <= neighbor[0] < rows and 
                        0 <= neighbor[1] < cols):
                        G.add_edge((x, y), neighbor, weight=1)

                        
    return G


def find_turns(points):
    # Convert points to a NumPy array
    points = np.array(points)
    
    # Compute the directional vectors
    directions = points[1:] - points[:-1]
    
    # Check for changes in direction
    changes = (directions[1:] != directions[:-1]).any(axis=1)
    score_turns = np.sum(changes)
    
    # Calculate the total score
    return score_turns * 1000 + len(points) - 1 + 1000



def main_code(file_name, part=1):
    data = read_txt_vector_matrix_str(file_name)

    print("Find Positions")
    possible_positions, start_position, end_position = found_positions_based_on_value(data, value_position=".", value_start="S", value_end="E")
   
    graph_map = build_graph(data, possible_positions)
    print("Build Graph")

    print("All paths")
    best_score = float("inf")
    for path in nx.all_simple_paths(graph_map, source=start_position, target=end_position):
        score = find_turns(path)
        if score < best_score:
            best_score = score

    return best_score
    

    #best_score = float("inf")
    #for path in nx.all_simple_paths(graph_map, source=start_position, target=end_position):
    #    score = find_turns(path)
    #    if score < best_score:
    #        best_score = score
    
    #return best_score


def main():
    day = 16
    expected_results = {1: 11048, 2: None} # fill this
    title = get_daily_title(day, BASE_DAY_URL, HEADERS)
    print(f"🧩 Starting puzzle for: {title}")
    run_part(day, 1, expected_results, main_code)
    file_exists_and_rename(f"days/day_16_to_do.py", f"days/day_16_part_2.py")
    #run_part(day, 2, expected_results, main_code)
    #file_exists_and_rename(f"days/day_16_part_2.py", f"days/day_16.py")

if __name__ == "__main__":
    main()
