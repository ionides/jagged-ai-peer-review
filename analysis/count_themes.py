"""
Tallies categorized_misses.txt's per-finding theme labels into theme_counts.csv.


Usage:
    python count_themes.py
"""

import csv
import re
from pathlib import Path
from collections import Counter

INPUT_FILE = Path(__file__).parent / "categorized_misses.txt"
OUTPUT_FILE = Path(__file__).parent / "theme_counts.csv"

text = INPUT_FILE.read_text()

theme_order = re.findall(r"^\d+\.\s+([^—\n]+?)\s+—", text, re.MULTILINE)

labels = re.findall(r"^(?:->|→)\s*\d+\.\s*(.+)$", text, re.MULTILINE)

counts = Counter(label.strip() for label in labels)

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Theme", "Count"])
    for theme in theme_order:
        writer.writerow([theme.strip(), counts.get(theme.strip(), 0)])

total = sum(counts.get(t.strip(), 0) for t in theme_order)
print(f"Wrote {len(theme_order)} themes, {total} findings total, to {OUTPUT_FILE.name}")
if total != len(labels):
    print(f"WARNING: {len(labels)} labels found in file but only {total} matched a known theme")
