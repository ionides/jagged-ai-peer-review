"""
Parses comparator comparison markdown files and regenerates comparator_results.csv.

Each comparator file contains per-reviewer A-F count tables and coverage
records. This script reads those directly from the assembled markdown files
and aggregates them into a single CSV, deterministically, from the current
state of results/comparator/.

Usage:
    python parse_comparator.py

Output:
    comparator_results.csv
"""

import re
import csv
import os
from pathlib import Path

NED_CLEAN_DIR = Path(__file__).parent.parent / "results" / "comparator"
OUTPUT_FILE = Path(__file__).parent / "comparator_results.csv"

REVIEWERS = ["Alex", "Charlie", "Doug", "Evan"]

def parse_filename(filename):
    match = re.match(r"comparator-([Ww]\d{2})_PROJECT(\d{2})\.md", filename)
    if not match:
        return None, None
    semester = match.group(1).upper()
    project = match.group(2)
    return semester, project

def parse_reviewer_counts(text, reviewer):
    section_pattern = rf"^## {reviewer}\s*$"
    section_match = re.search(section_pattern, text, re.MULTILINE)
    if not section_match:
        return None

    section_text = text[section_match.end():]

    next_section = re.search(r"^## ", section_text, re.MULTILINE)
    if next_section:
        section_text = section_text[:next_section.start()]

    counts = {}
    for letter in "ABCDEF":
        pattern = rf"\|\s*{letter}\s*\([^|]+\)\s*\|\s*(\d+)\s*\|"
        match = re.search(pattern, section_text)
        if match:
            counts[letter] = int(match.group(1))
        else:
            counts[letter] = None  # missing

    return counts

def parse_reviewer_coverage(text, reviewer):

    section_match = re.search(rf"^## {reviewer}\s*$", text, re.MULTILINE)
    if not section_match:
        return {}
    section_text = text[section_match.end():]
    next_section = re.search(r"^## ", section_text, re.MULTILINE)
    if next_section:
        section_text = section_text[:next_section.start()]

    coverage = {}
    in_coverage = False
    for line in section_text.split("\n"):
        if "**Coverage record:**" in line:
            in_coverage = True
            continue
        if in_coverage:
            if line.startswith("**"):
                break
            m = re.match(
                r"^- Human Issue #(\d+)\s*(?:\([^)]*\))?\s*:\s*(missed|covered|contradiction)",
                line,
                re.IGNORECASE,
            )
            if m:
                coverage[int(m.group(1))] = m.group(2).lower()
    return coverage


def compute_metrics(counts, coverage):
    a, b, c, d, e, f = (counts[k] for k in "ABCDEF")
    total_ai = a + b + c + d
    n_cov = sum(1 for v in coverage.values() if v == "covered")
    n_mis = sum(1 for v in coverage.values() if v == "missed")
    total_human = n_cov + n_mis

   
    # Human Overlap = 1 - E / (total human issues)
    human_overlap = 1 - (n_mis / total_human) if total_human > 0 else 0.0
    # AI-Unique Rate = (A+C) / (A+B+C+D)
    ai_unique_rate = (a + c) / total_ai if total_ai > 0 else 0.0

    return total_ai, human_overlap, ai_unique_rate

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
            coverage = parse_reviewer_coverage(text, reviewer)
            if not coverage:
                errors.append(f"  MISSING coverage record: {filepath.name} / {reviewer}")
            total_ai, human_overlap, ai_unique_rate = compute_metrics(counts, coverage)

            rows.append({
                "Semester": semester,
                "Project": project,
                "Reviewer": reviewer,
                "A": a, "B": b, "C": c, "D": d, "E": e, "F": f,
                "Total_AI_Findings": total_ai,
                "Human_Overlap": round(human_overlap, 4),
                "AI_Unique_Rate": round(ai_unique_rate, 4),
                "Human_Overlap_Pct": f"{human_overlap * 100:.1f}%",
                "AI_Unique_Rate_Pct": f"{ai_unique_rate * 100:.1f}%",
            })

    fieldnames = ["Semester", "Project", "Reviewer", "A", "B", "C", "D", "E", "F",
                  "Total_AI_Findings", "Human_Overlap", "AI_Unique_Rate",
                  "Human_Overlap_Pct", "AI_Unique_Rate_Pct"]

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
