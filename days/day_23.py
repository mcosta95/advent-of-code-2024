import sys
from pathlib import Path

# Change the working directory to the root of the project
project_root = Path(__file__).resolve().parent.parent  # Two levels up to the root
sys.path.append(str(project_root))

from config import BASE_DAY_URL, HEADERS
from src.utils import get_daily_title, run_part, file_exists_and_rename
from src.read_data import read_txt_to_str, read_txt_vector_matrix_str
import networkx as nx



def main_code(file_name, part=1):
    list_connections = read_txt_to_str(file_name, with_split="\n")

    G = nx.Graph()

    # Assuming data contains edges in the format "node1 node2"
    for line in list_connections:
        comp1, comp2 = line.split("-")
        G.add_edge(comp1, comp2)

    if part==1:
        triangles = [clique for clique in nx.enumerate_all_cliques(G) if len(clique) == 3 and any(item.startswith('t') for item in clique)]
        final_result = len(triangles)
    else:
        cliques = list(nx.find_cliques(G))
        largest_clique = max(cliques, key=len)
        final_result = ",".join(sorted(largest_clique))
    return final_result


def main():
    day = 23
    expected_results = {1: 7, 2: "co,de,ka,ta"} # fill this
    title = get_daily_title(day, BASE_DAY_URL, HEADERS)
    print(f"🧩 Starting puzzle for: {title}")
    run_part(day, 1, expected_results, main_code)
    file_exists_and_rename(f"days/day_23_to_do.py", f"days/day_23_part_2.py")
    run_part(day, 2, expected_results, main_code)
    file_exists_and_rename(f"days/day_23_part_2.py", f"days/day_23.py")

if __name__ == "__main__":
    main()
