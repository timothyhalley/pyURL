"""
Module: launch_urls
Description: This script opens URLs from a specified text file
    in either Brave or Edge browser on a Mac.
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

import argparse
import os
import random
import re
import subprocess
import sys
import time

# Specify the paths to the Brave and Edge binaries (adjust as needed)
BRAVE_PATH = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
EDGE_PATH = "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"


def sort_and_return_random(arr, number):
    """
    Function: return random values or sorted array
    """
    if number >= len(arr):
        return sorted(arr)
    return random.sample(sorted(arr), number)


def sort_urls(arr):
    """
    Function: return sorted array
    """
    return sorted(arr)


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Open URLs in a specified browser.")
    parser.add_argument(
        "--browser",
        choices=["brave", "edge"],
        required=True,
        help="Choose the browser: brave or edge",
    )
    parser.add_argument(
        "--urlfile", required=True, help="Path to the text file containing URLs"
    )
    parser.add_argument("--new-tab", action="store_true", help="Open URLs in new tabs")
    parser.add_argument(
        "--delay", type=int, default=3, help="Delay between opening tabs in seconds"
    )
    args = parser.parse_args()

    # Determine the browser path based on the argument
    if args.browser == "brave":
        BROWSER_PATH = BRAVE_PATH
    elif args.browser == "edge":
        BROWSER_PATH = EDGE_PATH
    else:
        print("Error: Unsupported browser specified.")
        sys.exit(1)

    # Read URLs from the specified file
    file_path = args.urlfile
    if not os.path.isfile(file_path):
        print(f"Error: {file_path} not found. Make sure the file exists.")
        sys.exit(1)

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.readlines()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        sys.exit(1)

    # Use regex to find URLs (http/https) in each line
    url_pattern = re.compile(r"https?://\S+")
    valid_urls = []
    for line in content:
        extracted_urls = url_pattern.findall(line)
        valid_urls.extend(extracted_urls)

    # Sort URLs from text file
    final_urls = valid_urls

    # Open each valid URL in a new tab with a delay
    for url in final_urls:
        try:
            cleaned_url = url.replace("http://", "https://")
            if args.new_tab:
                subprocess.Popen([BROWSER_PATH, "--new-tab", cleaned_url])
            else:
                subprocess.Popen([BROWSER_PATH, "--incognito", cleaned_url])
            print(f"Opened {cleaned_url}")
            time.sleep(args.delay)
        except FileNotFoundError:
            print(f"Error: Browser executable not found at {BROWSER_PATH}")
            sys.exit(1)
        except Exception as e:
            print(f"Error opening URL {cleaned_url}: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
