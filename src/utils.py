import requests
from bs4 import BeautifulSoup
from config import BASE_DAY_URL, HEADERS
import time

def get_daily_title(day, BASE_URL, HEADERS):
    response = requests.get(f"{BASE_URL}{day}", headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to fetch day {day} page!")
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("h2").text.strip()

    return title.replace("-", "").strip()


def get_input(day, base_url, mode, headers, part=1):
    """
    Fetches and saves input or test example for the specified day and mode (input or test).
    
    Args:
        day (int): The day of the challenge.
        base_url (str): The base URL for fetching inputs.
        mode (str): The mode ('input' or 'test').
        headers (dict): HTTP headers for the request.
        part (int, optional): The part of the challenge (1 or 2). Default is 1.
    """
    input_url = f"{base_url}{day}/input" if mode == 'input' else f"{base_url}{day}"
    
    # Default file naming for both modes and both parts
    file_name = f"data/{mode}/day_{day}"

    # Check if we need to handle part distinction
    if mode == 'input':  # If it's 'input' mode, we treat the data as for part 1.
        file_name += f"_part_{part}.txt"
    else:  # If it's 'test', we treat it as per the part requested
        file_name += f"_part_{part}.txt"

    response = requests.get(input_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch day {day} {mode} for part {part}!")
        return None
    
    input_text = response.text.strip()

    if mode == 'test':
        # Parse the HTML to extract test examples
        soup = BeautifulSoup(input_text, 'html.parser')
        pre_elements = soup.find_all('pre')  # Find all <pre> elements
        if len(pre_elements) >= part:
            input_text = pre_elements[part - 1].code.get_text(strip=True)
        else:
            print(f"Test example for part {part} not found! Falling back to part 1.")
            # Fall back to part 1 if part 2 test is missing
            input_text = pre_elements[0].code.get_text(strip=True)  # Use the first test example
            # Save as part 2 file, but with part 1's data
            file_name = f"data/{mode}/day_{day}_part_2.txt"  # Save it as part_2.txt (not part_1.txt)


    print(f"The data for day {day}, {mode}, part {part} was saved!")
    with open(file_name, "w") as file:
        file.write(input_text)
        

def submit_answer(day, part, answer):
    submit_url = f"{BASE_DAY_URL}{day}/answer"
    payload = {"level": part, "answer": answer}
    response = requests.post(submit_url, data=payload, headers=HEADERS)
    
    if response.status_code == 200:
        if "That's the right answer!" in response.text:
            print("🚀 Correct! You've completed this part.")
        elif "That's not the right answer" in response.text:
            print("❌ Incorrect answer. Try again.")
        elif "Did you already complete it" in response.text:
            print("🤔 You already submited this part!")
        elif "You gave an answer too recently" in response.text:
            print("⏳ Slow down! You're submitting too quickly.")
        else:
            print("🔥 Unexpected response:")
            print(response.text)
    else:
        print(f"⚠️ Failed to submit answer for day {day}, part {part}.")
        print(f"HTTP Status Code: {response.status_code}")
        print("Response Text:", response.text)


def run_part(day, part, expected_results, process_data):

    start_time = time.time()
    test_result = process_data(f"data/test/day_{day}_part_{part}.txt", part)
    elapsed_time_test = time.time() - start_time
    print(f"")
    if test_result == expected_results[part]:

        start_time = time.time()
        print(f"✅ [Part {part}] test passed!")
        final_result = process_data(f"data/input/day_{day}_part_{part}.txt", part)
        print(f"⭐️ Submitting result for part {part}: {final_result}")
        submit_answer(day, part, final_result)
        elapsed_time_final = time.time() - start_time
        print(f"⌛️ Time taken for [test]: {elapsed_time_test:.2f} seconds")
        print(f"⌛️ Time taken for [final]: {elapsed_time_final:.2f} seconds")
    else:
        print(f"Part {part} test failed. Expected {expected_results[part]}, got {test_result}.")
