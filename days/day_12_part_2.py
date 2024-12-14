import sys
from pathlib import Path

# Change the working directory to the root of the project
project_root = Path(__file__).resolve().parent.parent  # Two levels up to the root
sys.path.append(str(project_root))

from config import BASE_DAY_URL, HEADERS
from src.utils import get_daily_title, run_part
from src.read_data import read_txt_vector_matrix_str



def calculate_perimeter(positions):
    """Calculate the actual perimeter of a region, considering internal edges."""
    positions_set = set(positions)
    perimeter = 0

    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for row, col in positions:
        for dr, dc in directions:
            neighbor = (row + dr, col + dc)
            # If the neighbor is not in the region, it contributes to the perimeter
            if neighbor not in positions_set:
                perimeter += 1

    return perimeter

    
def calculate_number_of_sides(positions, grid, letter):
    """Calculate the number of sides (external edges) of a region."""
    positions_set = set(positions)
    sides = 0

    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dr, dc in directions:
        for row, col in positions:
            neighbor = (row + dr, col + dc)
            # If the neighbor is not in the region, it contributes to the perimeter
            if neighbor not in positions_set:
                sides += 1
            else:
                no = 0

    return sides



def find_connected_regions(positions):
    """Returns list of connected regions as lists of positions."""
    visited = set()
    regions = []

    def dfs(position, region):
        stack = [position]
        while stack:
            pos = stack.pop()
            if pos not in visited:
                visited.add(pos)
                region.append(pos)
                # Add neighboring positions (up, down, left, right)
                row, col = pos
                neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
                for neighbor in neighbors:
                    if neighbor in positions and neighbor not in visited:
                        stack.append(neighbor)

    for pos in positions:
        if pos not in visited:
            region = []
            dfs(pos, region)
            regions.append(region)

    return regions


def main_code(file_name, part=1):
    data = read_txt_vector_matrix_str(file_name)

    positions_dict = {}
    # Loop through the matrix to find each letter's position
    for row_index, row in enumerate(data):
        for col_index, value in enumerate(row):
            if value not in positions_dict:
                positions_dict[value] = []
            positions_dict[value].append((row_index, col_index))

    price_score = 0
    for letter, positions in positions_dict.items():

        regions = find_connected_regions(positions)
        for reg_pos in regions:
            if part == 1:
                perimeter = calculate_perimeter(reg_pos)

            elif part == 2:
               perimeter = calculate_number_of_sides(positions, data, letter)
            
            area = len(reg_pos)
            print(f"For letter '{letter}': perimeter {perimeter} and area {area}")
            price_score += perimeter*area

    return price_score


def main():
    day = 12
    expected_results = {1: 1930, 2: None} # fill this
    #title = get_daily_title(day, BASE_DAY_URL, HEADERS)
    #print(f"🧩 Starting puzzle for: {title}")
    #run_part(day, 1, expected_results, main_code)
    run_part(day, 2, expected_results, main_code)

if __name__ == "__main__":
    main()
