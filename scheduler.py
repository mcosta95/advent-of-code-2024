import schedule
import time
import subprocess

# Function to run your Python script
def run_script():
    script_path = "leaderboard.py"
    print("Running the script...")
    subprocess.run(["python3", script_path])

# Schedule the script to run every day at 2 AM
schedule.every().day.at("08:00").do(run_script)

# Loop to keep the scheduler running
while True:
    schedule.run_pending()
    time.sleep(60*14)  # Wait for a minute before checking again