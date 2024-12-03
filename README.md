# Advent of code 2024

## With some code automation

This repository contains an automated setup for solving Advent of Code puzzles. It streamlines the process of fetching input data, organizing daily solutions, and submitting results directly to the Advent of Code platform. Additionally, it includes functionality for parsing leaderboard data and exporting it to an Excel file for use in Power Automate apps to share with colleagues on Teams as a "Card Div".


### Main Features

1. Automatic Day Setup:
    The __create_day.py__ script sets up the folder structure and Python files for each day's puzzle.
    Automatically fetches input data for the day and creates a template solution file.

2. Submission:
    Processes the puzzle data and submits the final answer directly to the Advent of Code browser.

3. Leaderboard Parsing:
    The leaderboard.py script fetches the leaderboard information, parses it, and saves it to an Excel file for integration with Power Automate apps.

### How to use it

1. Install Python env and dependencies:
    *  python3 -m venv venv
    *  source venv/bin/activate
    *  pip install -r requirements.txt

2. Create your own config file

3. Run the create_day.py script to set up a new day's folder and boilerplate solution file. You need to specify the day

4. Open the generated day_X.py file in the days/ folder.

5. Implement the logic in the main_code() or process_data(file_name, part) change the function for parts 1 and 2.

6. Run the script to test and submit answers.



