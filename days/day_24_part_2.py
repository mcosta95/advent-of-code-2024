import sys
from pathlib import Path

# Change the working directory to the root of the project
project_root = Path(__file__).resolve().parent.parent  # Two levels up to the root
sys.path.append(str(project_root))

from config import BASE_DAY_URL, HEADERS
from src.utils import get_daily_title, run_part, file_exists_and_rename
from src.read_data import read_txt_to_str


def main_code(file_name, part=1):
    gates, wire = read_txt_to_str(file_name, with_split="\n\n")

    gates_dict = {item.split(": ")[0]: int(item.split(": ")[1]) for item in gates.split("\n")}
    wires_ = wire.lower().replace("xor", "^").replace("chr", "char").split("\n")

    remaining_wires = wires_.copy()
    while remaining_wires:
        i = 0
        while i < len(remaining_wires):
            wire = remaining_wires[i]
            parts = wire.split(" -> ")
            logic_expr = parts[0]
            result_var = parts[1]

            for key, value in gates_dict.items():
                logic_expr = logic_expr.replace(key, str(value))

            try:
                print(logic_expr)
                result_value = eval(logic_expr)
                # Update the gates_dict with the result
                gates_dict[result_var] = result_value
                remaining_wires.pop(i)
            except (NameError, TypeError):
                # If there is a NameError, it means some variables are not yet defined
                i+=1
        
    z_values = [str(gates_dict[key]) for key in sorted(gates_dict.keys(), reverse=True) if key.startswith('z')]
    final_value = int("".join(z_values), 2)
    return final_value


def main():
    day = 24
    expected_results = {1: 2024, 2: None} # fill this
    title = get_daily_title(day, BASE_DAY_URL, HEADERS)
    print(f"🧩 Starting puzzle for: {title}")
    run_part(day, 1, expected_results, main_code)
    file_exists_and_rename(f"days/day_24_to_do.py", f"days/day_24_part_2.py")
    #run_part(day, 2, expected_results, main_code)
    #file_exists_and_rename(f"days/day_24_part_2.py", f"days/day_24.py")

if __name__ == "__main__":
    main()
