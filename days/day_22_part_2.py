import sys
from pathlib import Path

# Change the working directory to the root of the project
project_root = Path(__file__).resolve().parent.parent  # Two levels up to the root
sys.path.append(str(project_root))

from config import BASE_DAY_URL, HEADERS
from src.utils import get_daily_title, run_part, file_exists_and_rename
from src.read_data import read_txt_to_str
import math
from collections import defaultdict

def mix_value(secret_nb, result):
    return secret_nb ^ result

def prune_value(secret_nb):
    return secret_nb % 16777216

def mix_and_prune(secret_nb, result):
    mix_ =  mix_value(secret_nb, result)
    return prune_value(mix_)


def main_code(file_name, part=1):
    init_secret_nb_lis = read_txt_to_str(file_name, with_split="\n")

    final_score_part_1 = 0
    for secret_nb in init_secret_nb_lis:
        secret_nb = int(secret_nb)
        print(f"Initialize Secret Number {secret_nb}")
        print(f"------------------------------------")

        lst_secret_nbs = [secret_nb]
        nb_times = 2000
        for _ in range(nb_times):
            secret_nb = mix_and_prune(secret_nb, result=secret_nb*64)
            secret_nb = mix_and_prune(secret_nb, result=math.floor(secret_nb/32))
            secret_nb = mix_and_prune(secret_nb, result=secret_nb*2048)
            
            lst_secret_nbs.append(secret_nb)

        final_score_part_1+=secret_nb


        if part == 2:
            lst_secret_nbs    
            changes = [""] + [lst_secret_nbs[i]%10 - lst_secret_nbs[i-1]%10 for i in range(1, len(lst_secret_nbs))]
            last_value = [lst_secret_nbs[i]%10 for i in range(0, len(lst_secret_nbs))]
            zip_values = tuple(zip(last_value, changes))
            
            sequence_counts = defaultdict(int)
            for i in range(0, len(changes) - 4, 4):
                seq = tuple(changes[i-1: i+3])
                sequence_counts[seq] = last_value[i + 3]

            a = 1

    if part==1:
        final_score = final_score_part_1
    
    return final_score


def main():
    day = 22
    expected_results = {1: 37327623, 2: None} # fill this
    title = get_daily_title(day, BASE_DAY_URL, HEADERS)
    print(f"🧩 Starting puzzle for: {title}")
    #run_part(day, 1, expected_results, main_code)
    #file_exists_and_rename(f"days/day_22_to_do.py", f"days/day_22_part_2.py")
    run_part(day, 2, expected_results, main_code)
    file_exists_and_rename(f"days/day_22_part_2.py", f"days/day_22.py")

if __name__ == "__main__":
    main()
