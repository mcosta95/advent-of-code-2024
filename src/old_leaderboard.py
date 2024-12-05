import requests
from bs4 import BeautifulSoup
from config import HEADERS, LEADERBOARD_URL, BASE_DAY_URL, SHAREPOINT_PATH
from src.utils import get_daily_title

import pandas as pd

from openpyxl import load_workbook
from openpyxl.worksheet.table import Table, TableStyleInfo


def current_day(row_):
    # Find all anchor tags (with href)
    day_links = row_.find_all('a', href=True)

    # Extract the day numbers
    days = [int(link['href'].split('/day/')[1]) for link in day_links]

    # Get the last day with a link (the current day)
    current_day = max(days)
    return current_day


def fetch_leaderboard_data():
    response = requests.get(LEADERBOARD_URL, headers=HEADERS)

    if response.status_code != 200:
        print("Failed to fetch leaderboard!")

    data_ = response.text


    soup = BeautifulSoup(response.text, 'html.parser')

    leaderboard_rows = soup.find_all('div', class_='privboard-row')
    curr_day = current_day(leaderboard_rows[0])

    leaderboard_data = []
    prev_score = None  # Store the score from the previous row to handle ties
    actual_position = 0  #

    # Loop through each row and extract the position, stars, and user name
    for row in leaderboard_rows[1:]:  # Skip the first row with the day info

        if row.find('span', class_='privboard-position'):
            position = int(row.find('span', class_='privboard-position').text.replace(")", "").strip())
            score = int(row.contents[1].strip())
        else:
            score = int(row.contents[0].strip())

        user = row.find('span', class_='privboard-name').text.strip()

        # Handle tie logic: If current score is the same as previous, don't change the actual position
        if score != prev_score:
            # New position, so update the previous score and actual position
            prev_score = score
            actual_position += 1  # Move to the next actual position

        # Append emoji for the first 3 positions
        if actual_position == 1:
            position_text = f"🥇 {position}"
        elif actual_position == 2:
            position_text = f"🥈 {position}"
        elif actual_position == 3:
            position_text = f"🥉 {position}"
        else:
            position_text = f"😭 {position}"
        
        leaderboard_data.append({
            'position': position_text,
            'score': f"{score} points",
            'user': user
        })

    df = pd.DataFrame(leaderboard_data)
    df['day'] = curr_day - 1

    title = get_daily_title(curr_day, BASE_DAY_URL, HEADERS)
    df['title'] = title

    return df


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

    df = fetch_leaderboard_data()

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




