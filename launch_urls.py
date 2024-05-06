"""
launch_urls.py: A script to open URLs from a file in the Brave browser.
"""

import webbrowser

# Specify the path to the Brave binary (adjust as needed)
BRAVE_PATH = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"

# Register Brave as a browser type
try:
    webbrowser.register("brave", None, webbrowser.BackgroundBrowser(BRAVE_PATH))
except webbrowser.Error as e:
    print(f"Error registering Brave browser: {e}")
    exit(1)

# Read URLs from a file (urls.txt)
try:
    with open("urls.txt", "r", encoding="utf-8") as file:
        urls = file.read().splitlines()
except FileNotFoundError:
    print("Error: urls.txt not found. Make sure the file exists.")
    exit(1)

# Print URLs
print(f"urls - \n{urls}")

# Open each URL in a new incognito mode tab
for url in urls:
    try:
        cleaned_url = url.replace("http://", "")
        webbrowser.get("brave").open_new(cleaned_url)
        print(f"Opened {cleaned_url}")
    except webbrowser.Error as e:
        print(f"Error opening {cleaned_url}: {e}")
