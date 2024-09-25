import os
import random
import re
import subprocess
import tkinter as tk
from tkinter import filedialog

# Specify the path to the Brave binary (adjust as needed)
BRAVE_PATH = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"

# Create a file dialog to select a text file
root = tk.Tk()
root.withdraw()  # Hide the main window

# Set the initial directory to the current working directory
initial_dir = os.getcwd()
file_path = filedialog.askopenfilename(
    filetypes=[("Text files", "*.txt")], initialdir=initial_dir
)

if not file_path:
    print("No file selected. Exiting.")
    exit(1)

# Read URLs from the selected file
try:
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.readlines()
except FileNotFoundError:
    print(f"Error: {os.path.basename(file_path)} not found. Make sure the file exists.")
    exit(1)


def sort_and_return_random(arr, number):
    """
    Function: return random values or sorted array
    """
    if number >= len(arr):
        return sorted(arr)

    sorted_arr = sorted(arr)
    return random.sample(sorted_arr, number)


# Use regex to find URLs (http/https) in each line
url_pattern = re.compile(r"https?://\S+")
valid_urls = []
for line in content:
    extracted_urls = url_pattern.findall(line)
    valid_urls.extend(extracted_urls)

# Print valid URLs
# print(f"Valid URLs - \n{valid_urls}")

# Get list of sorted_urls and limit number to parameter
final_urls = []
num_elements = 25
final_urls = sort_and_return_random(valid_urls, num_elements)


# Open each valid URL in a new incognito mode tab
for url in final_urls:
    try:
        cleaned_url = url.replace("http://", "")
        process = subprocess.Popen([BRAVE_PATH, "--incognito", cleaned_url])
        # process = subprocess.Popen([BRAVE_PATH, cleaned_url])
        print(f"Opened {cleaned_url}")

        # Terminate the subprocess gracefully
        # process.terminate()
        # process.wait()  # Wait for the process to finish

        # Wait for the process to finish
        # process.communicate()
    except FileNotFoundError:
        print(f"Error: Brave browser executable not found at {BRAVE_PATH}")
        exit(1)
