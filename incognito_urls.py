"""
Module: launch_urls
Description: This script opens URLs from a specified text file in either Brave or Edge browser on a Mac.
             The browser and URL file are specified via command line arguments.

Usage:
    python launch_urls.py --browser edge --urlfile urls.txt
    python launch_urls.py --browser brave --urlfile urls.txt

Arguments:
    --browser : Specify the browser to use (brave or edge).
    --urlfile : Path to the text file containing URLs.

Example:
    python launch_urls.py --browser edge --urlfile urls.txt
"""

import os
import random
import re
import subprocess
import sys

# Specify the path to the Brave binary (adjust as needed)
BRAVE_PATH = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"

# Get the input file path from the command line
if len(sys.argv) < 2:
    print("Usage: python script.py <input_file>")
    exit(1)

file_path = sys.argv[1]

# Read URLs from the provided file
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

# Get list of sorted URLs and limit number to a specified parameter
num_elements = 25
final_urls = sort_and_return_random(valid_urls, num_elements)

# Open each valid URL in a new incognito mode tab
for url in final_urls:
    try:
        cleaned_url = url.replace("http://", "")
        process = subprocess.Popen([BRAVE_PATH, "--incognito", cleaned_url])
        print(f"Opened {cleaned_url}")
    except FileNotFoundError:
        print(f"Error: Brave browser executable not found at {BRAVE_PATH}")
        exit(1)
