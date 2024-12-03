import sys
from pathlib import Path

# Change the working directory to the root of the project
project_root = Path(__file__).resolve().parent.parent  # Two levels up to the root
sys.path.append(str(project_root))

from config import BASE_DAY_URL, HEADERS
from src.utils import get_daily_title, submit_answer
import pandas as pd


def main_code(data, part=1):

    if part==1:
        data["vector1"].values.sort()
        data["vector2"].values.sort()
        data["distance"] = abs(data["vector1"] - data["vector2"])
        final_score = data["distance"].sum()

    elif part==2:

        df_count = data.groupby("vector2").agg({"vector1": "count"}).reset_index()
        df_count = df_count.rename(columns={"vector1": "count", "vector2": "vector1"})
        df_count["similarity"] = df_count["vector1"] * df_count["count"]

        final_df = data.merge(df_count, on="vector1", how="left").fillna(0)
        final_score = int(final_df["similarity"].sum())

    return final_score

def process_data(file_name, part):
    data = pd.read_csv(file_name, sep='\s+', header=None, names=['vector1', 'vector2'])
    return main_code(data, part)

def run_part(day, part, expected_results):

    test_result = process_data(f"data/test/day_{day}_part_{part}.txt", part)
    
    if test_result == expected_results[part]:
        print(f"Part {part} test passed!")

        final_result = process_data(f"data/input/day_{day}_part_{part}.txt", part)
        print(f"Submitting result for part {part}: {final_result}")
        submit_answer(day, part, final_result)
    else:
        print(f"Part {part} test failed. Expected {expected_results[part]}, got {test_result}.")

def main():
    day = 1
    expected_results = {1: 11, 2: 31}
    title = get_daily_title(day, BASE_DAY_URL, HEADERS)
    print(f"Starting puzzle for day {day}: {title}")
    run_part(day, 1, expected_results)
    run_part(day, 2, expected_results)

if __name__ == "__main__":
    main()
