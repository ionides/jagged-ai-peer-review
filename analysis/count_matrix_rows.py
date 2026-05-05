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
            m = re.search(r':\s*([AC])\s*[—–-]+\s*(.+)', line)
            if m:
                findings.append((m.group(1), m.group(2).strip().lower()))
        results[reviewer] = findings
    return results

# Keyword patterns for each matrix row
matrix_rows = {
    # Gray — shared
    'No CIs for parameters': ['no confidence interval', 'no ci', 'profile likelihood', 'confidence interval', 'no profile'],
    'Convergence not demonstrated': ['convergence', 'not demonstrated', 'no convergence', 'convergence not'],
    'Parameter values unjustified': ['parameter.*fixed', 'assumed', 'without justification', 'no justification', 'fixed.*param', 'unjustified'],
    # Blue — Baseline
    'Implementation bug (aliasing)': ['aliased', 'shared', 'silently', 'modif.*variable', 'copy'],
    'Code diverges from model': ['code.*implement', 'implement.*model', 'diverges', 'inconsistent.*model', 'model.*written'],
    'Wrong values no error': ['wrong value', 'incorrect value', 'wrong result', 'silent.*error', 'produces wrong'],
    # Orange — 531_Ref/Meta-Skill
    'CI procedure wrong': ['ci.*wrong', 'profile.*wrong', 'incorrect.*ci', 'wrong.*profile', 'procedure.*wrong', 'incorrectly.*profile'],
    'No simpler baseline': ['benchmark', 'simpler model', 'baseline model', 'arima.*benchmark', 'no.*benchmark'],
    'Too few starting values': ['starting value', 'global search', 'too few.*start', 'starting point', 'initial.*search'],
    # Purple — Orchestrator
    'Profile flat/noisy': ['flat.*profile', 'noisy.*profile', 'profile.*flat', 'profile.*noisy', 'unextractable'],
    'Wrong biological formula': ['biological.*formula', 'wrong.*formula', 'incorrect.*formula', 'formula.*wrong', 'wrong.*equation', 'biological.*wrong'],
    'Missing estimates/captions': ['missing.*caption', 'no caption', 'missing.*estimate', 'no.*estimate', 'caption.*missing', 'absent.*caption'],
}

# Collect findings
all_findings = defaultdict(list)
files = sorted(glob.glob(str(DATA_DIR / "ned-clean-*.md")))
for fpath in files:
    sem = get_semester(fpath)
    if not sem:
        continue
    data = parse_findings(fpath)
    for reviewer, findings in data.items():
        all_findings[reviewer].extend(findings)

reviewer_map = {'Alex': 'Baseline', 'Charlie': '531_Ref', 'Doug': 'Meta-Skill', 'Evan': 'Orchestrator'}

print(f"\n{'Row':<32} {'Baseline':>10} {'531_Ref':>10} {'Meta-Skill':>10} {'Orchestrator':>12}")
print('-' * 76)

for row_name, keywords in matrix_rows.items():
    counts = {}
    for rev in ['Alex', 'Charlie', 'Doug', 'Evan']:
        n = 0
        for code, text in all_findings[rev]:
            for kw in keywords:
                if re.search(kw, text):
                    n += 1
                    break
        counts[rev] = n
    row = f"{row_name:<32}"
    for rev in ['Alex', 'Charlie', 'Doug', 'Evan']:
        row += f"  {counts[rev]:>6}"
    print(row)
