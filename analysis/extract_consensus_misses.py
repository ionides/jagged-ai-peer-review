import re
import glob
from collections import defaultdict
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "results" / "comparator"

def get_semester(fname):
    fname = fname.lower()
    for sem in ['w21', 'w22', 'w24', 'w25']:
        if f'comparator-{sem}_' in fname:
            return sem.upper()
    return None

def parse_consensus_misses(path):
    with open(path) as f:
        text = f.read()

    m = re.search(r'### Consensus misses\n(.*?)(?=\n###|\n##|\Z)', text, re.DOTALL)
    if not m:
        return []

    section = m.group(1)
    misses = []

    for line in section.split('\n'):
        line = line.strip()
        if not line.startswith('- Human Issue #'):
            continue
        issue_text = re.sub(r'\s*\(Missed by all \d+ reviewers.*?\)\s*$', '', line)
        issue_text = re.sub(r'^- Human Issue #\d+:\s*', '', issue_text).strip()
        if issue_text:
            misses.append(issue_text)

    return misses

all_misses = []  # list of (semester, project, text)
counts_by_sem = defaultdict(int)

files = sorted(glob.glob(str(DATA_DIR / "comparator-*.md")))
for fpath in files:
    sem = get_semester(fpath)
    if not sem:
        continue
    project = re.search(r'comparator-((?:W|w)\d+_PROJECT\d+)', fpath, re.IGNORECASE).group(1).upper()
    misses = parse_consensus_misses(fpath)
    for text in misses:
        all_misses.append((sem, project, text))
        counts_by_sem[sem] += 1


print(f"Total consensus misses: {len(all_misses)}\n")
for sem in ['W21', 'W22', 'W24', 'W25']:
    print(f"  {sem}: {counts_by_sem[sem]}")

out_path = Path(__file__).parent / "consensus_misses.txt"
with open(out_path, 'w') as f:
    f.write(f"Total consensus misses: {len(all_misses)}\n\n")
    current_sem = None
    for sem, project, text in all_misses:
        if sem != current_sem:
            f.write(f"\n{'='*60}\n{sem}\n{'='*60}\n\n")
            current_sem = sem
        f.write(f"[{project}]\n{text}\n\n")

print(f"\nFull list written to: consensus_misses.txt")
