import re
import glob
from collections import defaultdict
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "results" / "ned-clean"

def get_semester(fname):
    fname = fname.lower()
    for sem in ['w21', 'w22', 'w24', 'w25']:
        if f'ned-clean-{sem}_' in fname:
            return sem.upper()
    return None

def parse_findings(path):
    with open(path) as f:
        text = f.read()

    results = {}
    sections = re.split(r'\n## ', text)
    for sec in sections[1:]:
        lines = sec.strip().split('\n')
        reviewer = lines[0].strip()
        if reviewer not in ('Alex', 'Charlie', 'Doug', 'Evan'):
            continue
        findings = []
        for line in lines:
            # Match lines with classification A or C
            m = re.search(r':\s*([AC])\s*[—–-]+\s*(.+)', line)
            if m:
                code = m.group(1)
                text_finding = m.group(2).strip()
                findings.append((code, text_finding))
        results[reviewer] = findings
    return results

# Collect all A and C findings
all_findings = defaultdict(list)  # reviewer -> list of (code, text)

files = sorted(glob.glob(str(DATA_DIR / "ned-clean-*.md")))
for fpath in files:
    sem = get_semester(fpath)
    if not sem:
        continue
    data = parse_findings(fpath)
    for reviewer, findings in data.items():
        all_findings[reviewer].extend(findings)

# Print counts
reviewer_map = {'Alex': 'Baseline', 'Charlie': '531_Ref', 'Doug': 'Meta-Skill', 'Evan': 'Orchestrator'}
for rev in ['Alex', 'Charlie', 'Doug', 'Evan']:
    findings = all_findings[rev]
    a_count = sum(1 for c, _ in findings if c == 'A')
    c_count = sum(1 for c, _ in findings if c == 'C')
    print(f"{reviewer_map[rev]}: A={a_count}, C={c_count}, total={a_count+c_count}")

# Write all findings to file for review
out_path = Path(__file__).parent / "ac_findings.txt"
with open(out_path, 'w') as f:
    for rev in ['Alex', 'Charlie', 'Doug', 'Evan']:
        f.write(f"\n{'='*60}\n{reviewer_map[rev]} ({rev})\n{'='*60}\n\n")
        for code, text in all_findings[rev]:
            f.write(f"[{code}] {text}\n")

print(f"\nWritten to ac_findings.txt")
