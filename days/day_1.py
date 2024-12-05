import sys
from pathlib import Path

# Change the working directory to the root of the project
project_root = Path(__file__).resolve().parent.parent

sys.path.append(str(project_root))

from config import BASE_DAY_URL, HEADERS
from src.utils import get_daily_title, run_part
from src.read_data import read_txt_to_df


def main_code(file_name, part=1):

    data = read_txt_to_df(file_name, col_names=['vector1', 'vector2'])

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


def main():
    day = 1
    expected_results = {1: 11, 2: 31}
    title = get_daily_title(day, BASE_DAY_URL, HEADERS)
    print(f"Starting puzzle for day {day}: {title}")
    run_part(day, 1, expected_results, main_code)
    run_part(day, 2, expected_results, main_code)

if __name__ == "__main__":
    main()
