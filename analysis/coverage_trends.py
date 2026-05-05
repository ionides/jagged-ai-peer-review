import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'DejaVu Sans'

semesters = ['W21', 'W22', 'W24', 'W25']
x = range(len(semesters))

# Broad coverage: (B+D)/(B+D+E)
broad = {
    'Baseline':   [33.3, 31.5, 22.5, 21.1],
    '531_Ref':    [33.7, 37.1, 30.5, 23.6],
    'Meta-Skill': [30.1, 35.4, 31.1, 23.6],
    'Orchestrator': [28.9, 38.8, 28.0, 19.0],
}

# Strict coverage: B/(B+E)
strict = {
    'Baseline':   [22.2, 21.3, 18.2, 15.3],
    '531_Ref':    [26.7, 27.7, 26.1, 17.5],
    'Meta-Skill': [24.7, 25.3, 24.1, 18.1],
    'Orchestrator': [18.1, 24.3, 22.3, 11.2],
}

colors = {
    'Baseline':     '#4C72B0',
    '531_Ref':      '#DD8452',
    'Meta-Skill':   '#C45B1A',
    'Orchestrator': '#8172B3',
}
markers = {'Baseline': 'o', '531_Ref': 's', 'Meta-Skill': 'D', 'Orchestrator': '^'}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5), sharey=False)

for reviewer in ['Baseline', '531_Ref', 'Meta-Skill', 'Orchestrator']:
    c = colors[reviewer]
    m = markers[reviewer]
    ax1.plot(x, broad[reviewer],  color=c, marker=m, linewidth=2, markersize=7, label=reviewer)
    ax2.plot(x, strict[reviewer], color=c, marker=m, linewidth=2, markersize=7, label=reviewer)

for ax, title, data in [
    (ax1, 'Broad Coverage  (B+D) / (B+D+E)', broad),
    (ax2, 'Strict Coverage  B / (B+E)',       strict),
]:
    ax.set_xticks(list(x))
    ax.set_xticklabels(semesters, fontsize=11)
    ax.set_ylabel('Coverage rate (%)', fontsize=11)
    ax.set_title(title, fontsize=12, fontweight='bold', pad=10)
    ax.set_ylim(0, 50)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{v:.0f}%'))
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend(fontsize=10, framealpha=0.8)

fig.suptitle('Agent Coverage of Human Review',
             fontsize=14, fontweight='bold', y=1.01)

plt.tight_layout()
plt.savefig('coverage_trends.png', dpi=150, bbox_inches='tight')
print("Saved: coverage_trends.png")
