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

# Theme keyword sets
themes = {
    'Implementation bug': [
        'aliased', 'shared state', 'shared-state', 'silently', 'wrong value',
        'wrong population', 'wrong n=', 'hard-coded', 'hardcoded',
        'code does not', 'diverges from', 'mismatch', 'inconsistenc',
        'rinit', 'rprocess error', 'conservation', 'double-deduct',
        'phantom', 'never used', 'reproducib', 'missing data file',
        'missing seed', 'broken', 'dmeas', 'rmeas', 'wrong formula',
        'incorrect formula', 'typo', 'run_level', 'compartment',
        'population size', 'overflow', 'numerically absurd',
    ],
    'Methodology / inference': [
        'profile likelihood', 'confidence interval', 'ci not', 'no ci',
        'benchmark', 'simpler model', 'baseline model', 'arima benchmark',
        'global search', 'starting value', 'cooling', 'rw.sd',
        'mif2', 'if2', 'optimizer', 'optimization', 'convergence',
        'ess', 'r-hat', 'mcmc', 'diagnostic', 'log-likelihood',
        'likelihood ratio', 'aic', 'identifiab', 'profile',
        'local search', 'filter', 'particle', 'pfilter',
    ],
    'Statistical reporting': [
        'not reported', 'not shown', 'absent', 'missing parameter',
        'no parameter estimate', 'no standard error', 'no uncertainty',
        'parameter not justified', 'fixed parameter', 'assumed without',
        'no justification', 'no rationale', 'unjustified',
        'caption', 'figure caption', 'no caption', 'unlabeled',
        'significant figure', 'decimal place', 'hard-code number',
        'inline r', 'hard-coded number',
    ],
    'Domain / biological': [
        'biological', 'epidemiolog', 'disease', 'compartment model',
        'sir ', 'seir', 'seiqr', 'secsdr', 'measurement model',
        'reporting rate', 'rho', 'transmission', 'recovery',
        'beta', 'gamma', 'domain', 'formula wrong', 'wrong formula',
        'leverage', 'volatility', 'financial', 'stock price',
        'overdispers', 'process noise', 'stochastic',
    ],
    'Reproducibility / code quality': [
        'reproducib', 'caching', 'bake', 'stew', 'seed',
        'hard-coded', 'hardcoded', 'inline r', 'run_level=1',
        'not provided', 'missing file', 'source code',
        'reference', 'citation', 'cited',
    ],
}

def classify(text):
    scores = defaultdict(int)
    for theme, keywords in themes.items():
        for kw in keywords:
            if kw in text:
                scores[theme] += 1
    if not scores:
        return 'Other'
    return max(scores, key=scores.get)

# Collect and classify
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
theme_order = ['Implementation bug', 'Methodology / inference', 'Statistical reporting',
               'Domain / biological', 'Reproducibility / code quality', 'Other']

print(f"\n{'Theme':<35} {'Baseline':>10} {'531_Ref':>10} {'Meta-Skill':>10} {'Orchestrator':>12}")
print('-' * 80)

theme_counts = {rev: defaultdict(int) for rev in ['Alex', 'Charlie', 'Doug', 'Evan']}
for rev in ['Alex', 'Charlie', 'Doug', 'Evan']:
    for code, text in all_findings[rev]:
        theme = classify(text)
        theme_counts[rev][theme] += 1

for theme in theme_order:
    row = f"{theme:<35}"
    for rev in ['Alex', 'Charlie', 'Doug', 'Evan']:
        total = len(all_findings[rev])
        n = theme_counts[rev][theme]
        row += f"  {n:4d} ({n/total*100:4.1f}%)"
    print(row)

print()
for rev in ['Alex', 'Charlie', 'Doug', 'Evan']:
    total = len(all_findings[rev])
    print(f"{reviewer_map[rev]}: {total} total findings")
