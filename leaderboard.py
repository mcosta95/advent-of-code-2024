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


def analyze_leaderboard(df_leader, all_data):

    # Spotlight: User with the highest local score
    spotlight = df_leader.iloc[0]
    spotlight = f"🌟 {spotlight['user']} is shining bright with the highest score of {spotlight['score']}! Keep up the awesome work! 🌟"

    # Most improved: Find the user with the largest score increment between days
    improvements = []
    for _, values in all_data.items():
        days = values.get('completion_day_level', {})
        day_scores = [
            (day, sum(star.get('star_index', 0) for star in stars.values()))
            for day, stars in days.items()
        ]
        day_scores.sort()
        score_diffs = [day_scores[i][1] - day_scores[i - 1][1] for i in range(1, len(day_scores))]
        if score_diffs:
            improvements.append((values["name"], max(score_diffs)))

    most_improved = max(improvements, key=lambda x: x[1])

    # Milestone: Day when the group reaches 50%, 75%, and 100% of star goals
    total_days = len(data['members'].values()) * 2 * current_day()
    milestones = {}
    total_stars = 0
    for day in range(1, current_day() + 1):
        day_stars = sum(
            len(data['members'][member_id]['completion_day_level'].get(str(day), {}))
            for member_id in data['members']
        )
        total_stars += day_stars
        if not milestones.get('50%') and total_stars >= 0.5 * total_days:
            milestones['50%'] = day
        if not milestones.get('75%') and total_stars >= 0.75 * total_days:
            milestones['75%'] = day
        if not milestones.get('100%') and total_stars >= total_days:
            milestones['100%'] = day
            break

    # Top stars collector
    top_stars_collector = df.iloc[df['stars'].idxmax()]

    # The Fastest: User with the shortest average completion time per star
    fastest_user = None
    fastest_avg_time = float('inf')
    for member_id, values in data['members'].items():
        completion_times = []
        for day_stars in values['completion_day_level'].values():
            for star in day_stars.values():
                completion_times.append(star['get_star_ts'])
        if completion_times:
            avg_time = sum(completion_times) / len(completion_times)
            if avg_time < fastest_avg_time:
                fastest_avg_time = avg_time
                fastest_user = values.get('name', 'Anonymous')

    # Day people started to give up: Day with the largest drop in participation
    participants = [
        sum(1 for member_id in data['members'] if str(day) in data['members'][member_id]['completion_day_level'])
        for day in range(1, current_day() + 1)
    ]
    drops = [participants[i - 1] - participants[i] for i in range(1, len(participants))]
    give_up_day = drops.index(max(drops)) + 2 if drops else None

    return {
        'Spotlight': spotlight.to_dict(),
        'Most Improved': most_improved,
        'Milestones': milestones,
        'Top Stars Collector': top_stars_collector.to_dict(),
        'The Fastest': fastest_user,
        'Day People Gave Up': give_up_day
    }



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




