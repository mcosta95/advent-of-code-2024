import sys
from pathlib import Path

# Change the working directory to the root of the project
project_root = Path(__file__).resolve().parent.parent  # Two levels up to the root
sys.path.append(str(project_root))

from config import BASE_DAY_URL, HEADERS
from src.utils import get_daily_title, run_part, file_exists_and_rename
from src.read_data import read_txt_to_str
import networkx as nx

def main_code(file_name, part=1):
    data = read_txt_to_str(file_name, with_split="\n")

    if "test" in file_name:
        nb_bytes = 12
        min_ = 0
        max_ = 7
    else:
        nb_bytes = 1024
        min_ = 0
        max_ = 71

    G = nx.Graph()
    coordinates = [tuple(map(int, coord_.split(","))) for coord_ in data]
    coordinates =  coordinates[:nb_bytes]

    for x in range(min_, max_):
        for y in range(min_, max_):
            if (x, y) not in coordinates:
                G.add_node((x, y))

                neighbors = [
                    (x-1, y), (x+1, y), 
                    (x, y-1), (x, y+1)
                ]
                for neighbor in neighbors:
                    if (neighbor not in coordinates and 
                        min_ <= neighbor[0] < max_ and 
                        min_ <= neighbor[1] < max_):
                        G.add_edge((x, y), neighbor)

    start_node = (0, 0)
    end_node = (max_-1, max_-1)

    if nx.has_path(G, start_node, end_node):
        shortest_path = nx.shortest_path(G, source=start_node, target=end_node)

    return len(shortest_path)-1 


def main():
    day = 18
    expected_results = {1: 22, 2: None} # fill this
    #title = get_daily_title(day, BASE_DAY_URL, HEADERS)
    #print(f"🧩 Starting puzzle for: {title}")
    run_part(day, 1, expected_results, main_code)
    file_exists_and_rename(f"days/day_18_to_do.py", f"days/day_18_part_2.py")
    #run_part(day, 2, expected_results, main_code)
    #file_exists_and_rename(f"days/day_18_part_2.py", f"days/day_18.py")

if __name__ == "__main__":
    main()
