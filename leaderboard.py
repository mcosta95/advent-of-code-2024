import requests
from config import HEADERS, LEADERBOARD_URL, BASE_DAY_URL, SHAREPOINT_PATH
from src.utils import get_daily_title

import pandas as pd
from datetime import datetime

from openpyxl import load_workbook
from openpyxl.worksheet.table import Table, TableStyleInfo


def current_day():
    today = datetime.now()
    if today.month != 12:
        raise ValueError("This script only works during December.")
    current_day = today.day
    return current_day

def get_rank_positions(df):

    df['rank'] = df['score'].rank(method='dense', ascending=False).astype(int)
    emoji_map = {1: "🥇", 2: "🥈", 3: "🥉"}
    df['position'] = df['rank'].map(emoji_map).fillna("😭") + " " + df['rank'].astype(str)

    df.sort_values(by="rank", inplace=True)
    df.drop(columns=["rank"], inplace=True)

    return df

def fetch_leaderboard_data():
    response = requests.get(LEADERBOARD_URL, headers=HEADERS)

    if response.status_code != 200:
        print("Failed to fetch leaderboard!")

    data_ = eval(response.text)['members']

    leaderboard_list = []
    for _, values in data_.items():
        row = {'user': values['name'], 
               'score': values['local_score'],
               'stars': values['stars'],
               'last_star_date': datetime.utcfromtimestamp(values['last_star_ts']).strftime("%Y-%m-%d %H:%M:%S")}
        leaderboard_list.append(row)

    # Accumulate rows in a list
    df = pd.DataFrame(leaderboard_list)

    # positions attribution
    df = get_rank_positions(df)
    df['score'] = df['score'].apply(lambda x: f"{x} points")

    curr_day = current_day()
    df['day'] = curr_day - 1
    df['title'] = get_daily_title(curr_day, BASE_DAY_URL, HEADERS)

    df['total_stars'] = sum(df['stars'])
    df['goal_stars'] = 2*curr_day*df.shape[0]
    df['goal_stars_perc'] = (df['total_stars']/df['goal_stars'])*100

    return df, data_


def save_data_on_sharepoint(df, file_path, sheet_name, table_name):

    # Write the DataFrame to Excel
    df.to_excel(file_path, index=False, sheet_name=sheet_name)

    # Open the workbook and select the sheet
    wb = load_workbook(file_path)
    ws = wb[sheet_name]

    # Define the table range (adjust for your DataFrame size)
    table_ref = f"A1:{chr(65 + len(df.columns) - 1)}{len(df) + 1}"

    # Create a table
    table = Table(displayName=table_name, ref=table_ref)

    # Add style to the table
    style = TableStyleInfo(
        name="TableStyleMedium9",
        showFirstColumn=False,
        showLastColumn=False,
        showRowStripes=True,
        showColumnStripes=True,
    )
    table.tableStyleInfo = style

    # Add the table to the worksheet
    ws.add_table(table)

    # Save the workbook
    wb.save(file_path)


def main():

    file_path = f"{SHAREPOINT_PATH}/leaderboard_data.xlsx"

    df, data_all = fetch_leaderboard_data()

    #df_analyze = analyze_leaderboard(df, data_all)

    try:
        existing_df = pd.read_excel(file_path)
        # If the CSV file exists, append new data to it, avoiding duplication
        combined_df = pd.concat([existing_df, df], ignore_index=True)
        combined_df.drop_duplicates(inplace=True)

        print(f"Update existing data!")

    except FileNotFoundError:
        # If the CSV doesn't exist yet, just create it
        combined_df = df

    save_data_on_sharepoint(df, file_path, "board_data", "LeaderboardTable")
    print(f"Leaderboard saved to {file_path}")


if __name__ == "__main__":
    main()




