import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import re
import glob
from collections import defaultdict

plt.rcParams['font.family'] = 'DejaVu Sans'

DATA_DIR = '/Users/jin/Desktop/ai/week12/ned-clean'

def get_semester(fname):
    fname = fname.lower()
    for sem in ['w21', 'w22', 'w24', 'w25']:
        if f'ned-clean-{sem}_' in fname:
            return sem.upper()
    return None

def parse_file(path):
    with open(path) as f:
        text = f.read()
    results = {}
    sections = re.split(r'\n## ', text)
    for sec in sections[1:]:
        lines = sec.strip().split('\n')
        reviewer = lines[0].strip()
        if reviewer not in ('Alex', 'Charlie', 'Doug', 'Evan'):
            continue
        counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0}
        for line in lines:
            m = re.match(r'\|\s*([A-F])\s*\(.*?\)\s*\|\s*(\d+)\s*\|', line)
            if m:
                counts[m.group(1)] = int(m.group(2))
        results[reviewer] = counts
    return results

reviewer_map = {
    'Alex':    'Baseline',
    'Charlie': '531_Ref',
    'Doug':    'Meta-Skill',
    'Evan':    'Orchestrator',
}

project_coverage = defaultdict(list)

files = glob.glob(f'{DATA_DIR}/ned-clean-*.md')
for fpath in sorted(files):
    sem = get_semester(fpath)
    if not sem:
        continue
    data = parse_file(fpath)
    for reviewer, counts in data.items():
        b, d, e = counts['B'], counts['D'], counts['E']
        denom = b + d + e
        if denom == 0:
            continue
        coverage = (b + d) / denom * 100
        project_coverage[reviewer_map[reviewer]].append(coverage)

reviewers = ['Baseline', '531_Ref', 'Meta-Skill', 'Orchestrator']
colors = {
    'Baseline':     '#4C72B0',
    '531_Ref':      '#DD8452',
    'Meta-Skill':   '#C45B1A',
    'Orchestrator': '#8172B3',
}

data_to_plot = [project_coverage[r] for r in reviewers]

fig, ax = plt.subplots(figsize=(10, 6))

parts = ax.violinplot(data_to_plot, positions=range(len(reviewers)),
                      showmedians=True, showextrema=False)

for pc, r in zip(parts['bodies'], reviewers):
    pc.set_facecolor(colors[r])
    pc.set_alpha(0.5)
parts['cmedians'].set_color('#333333')
parts['cmedians'].set_linewidth(2)

rng = np.random.default_rng(42)
for i, (r, data) in enumerate(zip(reviewers, data_to_plot)):
    x = rng.normal(i, 0.06, size=len(data))
    ax.scatter(x, data, alpha=0.5, s=25, color=colors[r], zorder=3)

# Print stats
print(f"{'Reviewer':<14} {'n':>4} {'median':>8} {'mean':>8} {'min':>6} {'max':>6}")
for r, data in zip(reviewers, data_to_plot):
    arr = np.array(data)
    print(f"{r:<14} {len(arr):>4} {np.median(arr):>7.1f}% {np.mean(arr):>7.1f}% {arr.min():>5.1f}% {arr.max():>5.1f}%")

ax.set_xticks(range(len(reviewers)))
ax.set_xticklabels(reviewers, fontsize=11)
ax.set_ylabel('Broad coverage per project (%)', fontsize=11)
ax.set_title('Per-Project Coverage Distribution (72 projects, W21–W25)',
             fontsize=12, fontweight='bold')
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{v:.0f}%'))
ax.set_ylim(0, 100)
ax.grid(axis='y', linestyle='--', alpha=0.4)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('per_project_coverage.png', dpi=150, bbox_inches='tight')
print("Saved: per_project_coverage.png")
