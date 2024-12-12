import sys
from pathlib import Path

# Change the working directory to the root of the project
project_root = Path(__file__).resolve().parent.parent  # Two levels up to the root
sys.path.append(str(project_root))

from config import BASE_DAY_URL, HEADERS
from src.utils import get_daily_title, run_part
from src.read_data import read_txt_vector_matrix_str
import networkx as nx


def main_code(file_name, part=1):
    data = read_txt_vector_matrix_str(file_name)

    len_rows, len_cols = (len(data), len(data[0]))

    G = nx.DiGraph()
    for r in range(len_rows):
        for c in range(len_cols):
            current = (r, c)
            current_height = int(data[r][c])
            neighbors = [
                        (r-1, c),
                        (r+1, c),
                        (r, c-1),
                        (r, c+1)
                    ]

            for nr, nc in neighbors:
                if 0 <= nr < len_rows and 0 <= nc < len_cols:
                    neighbor_height = int(data[nr][nc])
                    if neighbor_height == current_height + 1:
                        G.add_edge(current, (nr, nc))

    start_nodes = [(r, c) for r in range(len_rows) for c in range(len_cols) if int(data[r][c]) == 0]
    end_nodes = [(r, c) for r in range(len_rows) for c in range(len_cols) if int(data[r][c]) == 9]

    if part==1:
            
        trailhead_scores = {}
        for trailhead in start_nodes:
            reachable_from_trailhead = nx.descendants(G, trailhead)
            score = len([end for end in end_nodes if end in reachable_from_trailhead])
            trailhead_scores[trailhead] = score
    else:
        trailhead_scores = {}
        for trailhead in start_nodes:
            all_trails = []
            for end in end_nodes:
                paths = list(nx.all_simple_paths(G, source=trailhead, target=end))
                all_trails.extend(paths)
            trailhead_scores[trailhead] = len(all_trails)

    return sum(trailhead_scores.values())


def main():
    day = 10
    expected_results = {1: 36, 2: 81} # fill this
    title = get_daily_title(day, BASE_DAY_URL, HEADERS)
    print(f"🧩 Starting puzzle for: {title}")
    run_part(day, 1, expected_results, main_code)
    run_part(day, 2, expected_results, main_code)

if __name__ == "__main__":
    main()
