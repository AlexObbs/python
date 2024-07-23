import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Initialize WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get("https://stake.com/casino/games/limbo")  # Replace with the actual URL of the game

# Function to extract results
def extract_results():
    result_elements = driver.find_elements(By.CLASS_NAME, 'past-bets')
    new_results = [element.text for element in result_elements]
    return new_results

# Function to get stored results from a JSON file
def get_stored_results(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Function to store results in a JSON file
def store_results(results, file_path):
    with open(file_path, 'w') as file:
        json.dump(results, file)

# Path to store the results
results_file = "results.json"

# Main loop to check for new results every 4 seconds
try:
    while True:
        new_results = extract_results()
        stored_results = get_stored_results(results_file)
        for result in new_results:
            if result not in stored_results:
                stored_results.append(result)
                print(f"New result added: {result}")
        store_results(stored_results, results_file)
        time.sleep(4)  # Wait for 4 seconds before checking again
except KeyboardInterrupt:
    print("Bot stopped.")

# Convert stored results to a CSV file
stored_results = get_stored_results(results_file)
df = pd.DataFrame(stored_results, columns=["Result"])
df.to_csv("limbo_results.csv", index=False, encoding='utf-8-sig')

print("Results saved to limbo_results.csv")
