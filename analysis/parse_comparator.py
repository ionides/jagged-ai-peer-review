"""
Parses comparator comparison markdown files and regenerates comparator_results.csv.

Each comparator file contains per-reviewer A-F count tables. This script reads
those tables directly and aggregates them into a single CSV, providing an
independently verifiable alternative to the Claude-generated CSV.

Usage:
    python parse_comparator.py

Output:
    comparator_results_parsed.csv  (compare against comparator_results.csv to verify)
"""

import re
import csv
import os
from pathlib import Path

NED_CLEAN_DIR = Path(__file__).parent.parent / "results" / "comparator"
OUTPUT_FILE = Path(__file__).parent / "comparator_results_parsed.csv"

REVIEWERS = ["Alex", "Charlie", "Doug", "Evan"]

def parse_filename(filename):
    """Extract semester and project number from filename."""
    # handles both 'comparator-W21_PROJECT02.md' and 'comparator-w21_PROJECT06.md'
    match = re.match(r"comparator-([Ww]\d{2})_PROJECT(\d{2})\.md", filename)
    if not match:
        return None, None
    semester = match.group(1).upper()
    project = match.group(2)
    return semester, project

def parse_reviewer_counts(text, reviewer):
    """
    Extract A-F counts from a reviewer's count table within the file.
    Looks for the section '## {reviewer}' and finds the first Category|Count table after it.
    """
    # Find the reviewer section
    section_pattern = rf"^## {reviewer}\s*$"
    section_match = re.search(section_pattern, text, re.MULTILINE)
    if not section_match:
        return None

    section_text = text[section_match.end():]

    # Find the next ## heading to limit scope
    next_section = re.search(r"^## ", section_text, re.MULTILINE)
    if next_section:
        section_text = section_text[:next_section.start()]

    # Parse the Category | Count table
    counts = {}
    for letter in "ABCDEF":
        pattern = rf"\|\s*{letter}\s*\([^|]+\)\s*\|\s*(\d+)\s*\|"
        match = re.search(pattern, section_text)
        if match:
            counts[letter] = int(match.group(1))
        else:
            counts[letter] = None  # missing

    return counts

def compute_metrics(counts):
    a, b, c, d, e, f = (counts[k] for k in "ABCDEF")
    total_ai = a + b + c + d
    denominator = b + d + e
    human_recall = (b + d) / denominator if denominator > 0 else 0.0
    ai_unique_rate = (a + c) / total_ai if total_ai > 0 else 0.0
    return total_ai, human_recall, ai_unique_rate

def main():
    rows = []
    errors = []

    files = sorted(NED_CLEAN_DIR.glob("comparator-*_PROJECT*.md"))

    for filepath in files:
        semester, project = parse_filename(filepath.name)
        if not semester:
            continue

        text = filepath.read_text(encoding="utf-8")

        for reviewer in REVIEWERS:
            counts = parse_reviewer_counts(text, reviewer)
            if counts is None:
                errors.append(f"  MISSING section: {filepath.name} / {reviewer}")
                continue

            missing = [k for k, v in counts.items() if v is None]
            if missing:
                errors.append(f"  MISSING counts {missing}: {filepath.name} / {reviewer}")
                continue

            a, b, c, d, e, f = (counts[k] for k in "ABCDEF")
            total_ai, human_recall, ai_unique_rate = compute_metrics(counts)

            rows.append({
                "Semester": semester,
                "Project": project,
                "Reviewer": reviewer,
                "A": a, "B": b, "C": c, "D": d, "E": e, "F": f,
                "Total_AI_Findings": total_ai,
                "Human_Recall": round(human_recall, 4),
                "AI_Unique_Rate": round(ai_unique_rate, 4),
                "Human_Recall_Pct": f"{human_recall * 100:.1f}%",
                "AI_Unique_Rate_Pct": f"{ai_unique_rate * 100:.1f}%",
            })

    # Write CSV
    fieldnames = ["Semester", "Project", "Reviewer", "A", "B", "C", "D", "E", "F",
                  "Total_AI_Findings", "Human_Recall", "AI_Unique_Rate",
                  "Human_Recall_Pct", "AI_Unique_Rate_Pct"]

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {OUTPUT_FILE.name}")
    print(f"Files parsed: {len(files)}, Reviewers per file: {len(REVIEWERS)}, Expected rows: {len(files) * len(REVIEWERS)}")

    if errors:
        print(f"\nWarnings ({len(errors)}):")
        for e in errors:
            print(e)
    else:
        print("No warnings.")

if __name__ == "__main__":
    main()
