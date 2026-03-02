"""
Module: master_urls
Description: This script reads all .txt files in a specified directory,
    extracts valid URLs, removes duplicates, and saves them alphabetically
    to a master file named urls_Master_YYMMDD.txt in the same directory.

Usage:
    python3 master_urls.py <directory>

Arguments:
    directory : Path to the directory containing URL text files.

Example:
    python3 master_urls.py data2
"""

import sys
import re
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse


def extract_urls_from_file(file_path, url_pattern):
    """
    Extract valid URLs from a text file.
    
    Args:
        file_path: Path to the text file
        url_pattern: Compiled regex pattern for matching URLs
    
    Returns:
        Set of valid URLs found in the file
    """
    urls = set()
    
    try:
        with file_path.open("r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                for url in url_pattern.findall(line):
                    # Validate URL has both scheme and netloc
                    parsed = urlparse(url)
                    if parsed.scheme and parsed.netloc:
                        # Clean up URL by removing trailing punctuation
                        url = url.rstrip('.,;:)')
                        urls.add(url)
    except Exception as e:
        print(f"Warning: Could not read {file_path.name}: {e}")
    
    return urls


def main():
    """Main function to process URLs from directory."""
    
    # Check if directory argument is provided
    if len(sys.argv) < 2:
        print("Error: Please provide a directory path.")
        print("Usage: python3 master_urls.py <directory>")
        sys.exit(1)
    
    # Get and validate directory
    directory = Path(sys.argv[1]).expanduser().resolve()
    
    if not directory.exists():
        print(f"Error: Directory '{directory}' does not exist.")
        sys.exit(1)
    
    if not directory.is_dir():
        print(f"Error: '{directory}' is not a directory.")
        sys.exit(1)
    
    # URL regex pattern
    url_pattern = re.compile(r'https?://[^\s)>\]]+')
    
    # Collect all URLs from all .txt files
    all_urls = set()
    txt_files = list(directory.glob("*.txt"))
    
    if not txt_files:
        print(f"Warning: No .txt files found in '{directory}'")
        sys.exit(0)
    
    print(f"Processing {len(txt_files)} text files in '{directory.name}'...")
    
    for txt_file in txt_files:
        urls = extract_urls_from_file(txt_file, url_pattern)
        all_urls.update(urls)
        if urls:
            print(f"  {txt_file.name}: {len(urls)} URLs")
    
    # Sort URLs alphabetically
    sorted_urls = sorted(all_urls)
    
    # Create output filename with current date
    timestamp = datetime.now().strftime("%y%m%d")
    output_file = directory / f"urls_Master_{timestamp}.txt"
    
    # Write to master file
    try:
        with output_file.open("w", encoding="utf-8") as f:
            for url in sorted_urls:
                f.write(url + "\n")
        
        print(f"\nSuccess!")
        print(f"  Total unique URLs: {len(sorted_urls)}")
        print(f"  Output file: {output_file.name}")
    except Exception as e:
        print(f"Error: Could not write to {output_file}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
