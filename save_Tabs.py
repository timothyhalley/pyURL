import subprocess

OUTPUT_FILE = "open_tabs.txt"

applescript = '''
tell application "Brave Browser"
    set url_list to {}
    repeat with w in windows
        repeat with t in tabs of w
            set end of url_list to URL of t
        end repeat
    end repeat
    return url_list
end tell
'''

# Run the AppleScript
result = subprocess.run(
    ["osascript", "-e", applescript],
    capture_output=True,
    text=True
)

# Parse output (AppleScript returns URLs separated by commas)
urls = [u.strip() for u in result.stdout.split(",") if u.strip()]

# Write to file
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for url in urls:
        f.write(url + "\n")

print(f"Saved {len(urls)} URLs to {OUTPUT_FILE}")