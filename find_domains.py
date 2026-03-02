import sys
import re
from pathlib import Path
from urllib.parse import urlparse

# Determine directory from CLI or default to current directory
if len(sys.argv) > 1:
    directory = Path(sys.argv[1]).expanduser().resolve()
else:
    directory = Path.cwd()

# Simple URL regex
url_pattern = re.compile(r'https?://[^\s)>\]]+')

domains = set()

for txt_file in directory.glob("*.txt"):
    with txt_file.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            for url in url_pattern.findall(line):
                parsed = urlparse(url)
                if parsed.scheme and parsed.netloc:
                    # Normalize to scheme + domain
                    domain = f"{parsed.scheme}://{parsed.netloc}"
                    domains.add(domain)

# Output unique domains
for d in sorted(domains):
    print(d)

print(f"\nTotal unique domains: {len(domains)}")