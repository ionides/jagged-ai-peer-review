import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
from pathlib import Path

plt.rcParams['font.family'] = 'DejaVu Sans'

baseline_color = '#4C72B0'
cd_color       = '#DD8452'
orch_color     = '#8172B3'



REVIEWER_MAP = {'Alex': 'Baseline', 'Charlie': 'CourseGuided', 'Doug': 'MetaSkill', 'Evan': 'Orchestrator'}

df = pd.read_csv(Path(__file__).parent / "comparator_results.csv")
df['Agent'] = df['Reviewer'].map(REVIEWER_MAP)
n_proj = df[['Semester', 'Project']].drop_duplicates().shape[0]
ac_per_proj = (df.groupby('Agent')[['A', 'C']].sum().sum(axis=1) / n_proj).round(1)


def agent_entry(name, color):
    return (name, f'{ac_per_proj[name]:.1f}', color)

BLOCKS = [
    (
        [
            ('Global search inherits cooled schedule, not truly global (optimization flaw)', '1'),
            ('Cross-family log-likelihood comparison invalid (scale mismatch)', '2'),
            ('No ESS or particle filter diagnostics reported (verification gap)', '3'),
        ],
        [],
        '#eeeeee',
        'Found by\nall four\nagents',
    ),
    (
        [
            ('Modifying one variable silently changes another (implementation bug)', '4'),
            ('Code does not implement the model as written (implementation bug)', '5'),
            ('Computation produces wrong values without error (implementation bug)', '6'),
        ],
        [
            agent_entry('Baseline', baseline_color),
        ],
        '#dce8f8',
        None,
    ),
    (
        [
            ('Confidence interval procedure is wrong (methodology flaw)', '7'),
            ('No simpler baseline model for comparison (model evaluation)', '8'),
            ('Too few starting values explored in fitting (optimization flaw)', '9'),
        ],
        [
            agent_entry('CourseGuided', cd_color),
            agent_entry('MetaSkill', cd_color),
        ],
        '#f8e8d8',
        None,
    ),
    (
        [
            ('Incorrect biological formula in model (domain error)', '10'),
            ('Profile too flat/noisy to extract CIs (identifiability issue)', '11'),
            ('Results lack parameter estimates or captions (omission)', '12'),
        ],
        [
            agent_entry('Orchestrator', orch_color),
        ],
        '#e8e0f4',
        None,
    ),
]

DATA_H  = 0.52
HDR_H   = 0.62
FOOT_H  = 0.0
LABEL_W = 2.6
FIG_W   = 14.2

N_ROWS = sum(len(rows) for rows, _, _, _ in BLOCKS)
FIG_H  = N_ROWS * DATA_H + HDR_H + FOOT_H + 0.4

GRID_L = 0.15
GRID_R = FIG_W - 0.3
CAT_X  = LABEL_W + 0.25

fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
ax.set_xlim(0, FIG_W)
ax.set_ylim(0, FIG_H)
ax.axis('off')

hdr_top = FIG_H
hdr_bot = FIG_H - HDR_H
hdr_mid = (hdr_top + hdr_bot) / 2
ax.text(GRID_L, hdr_mid, 'Domain-Specific Breakdown of Agent-Unique Review Overlap',
        ha='left', va='center', fontsize=16, fontweight='bold', color='#1a1a1a', zorder=2)

y = hdr_bot
for rows, agents, bg, label_override in BLOCKS:
    block_h = len(rows) * DATA_H
    block_top, block_bot = y, y - block_h


    ax.add_patch(mpatches.Rectangle(
        (GRID_L, block_bot), LABEL_W, block_h,
        facecolor=bg, edgecolor='none', zorder=1
    ))


    for i, (label, sup) in enumerate(rows):
        ax.add_patch(mpatches.Rectangle(
            (GRID_L + LABEL_W, block_top - (i + 1) * DATA_H), GRID_R - GRID_L - LABEL_W, DATA_H,
            facecolor=bg, edgecolor='#cccccc', linewidth=0.4, zorder=1
        ))
        mid_y = block_top - (i + 0.5) * DATA_H
        text = label if sup is None else f'{label}$^{{{sup}}}$'
        ax.text(CAT_X, mid_y, text, ha='left', va='center', fontsize=12,
                fontweight='bold', color='#1a1a1a', zorder=2)


    label_x = GRID_L + LABEL_W / 2
    block_mid = block_top - block_h / 2

    if label_override is not None:
        ax.text(label_x, block_mid, label_override, ha='center', va='center',
                fontsize=13, fontweight='bold', color='#555555',
                linespacing=1.4, zorder=2)
    else:
        n_agents = len(agents)
        fontsize = 14 if n_agents == 1 else 12
        offset_step = 0.55
        for j, (name, count, color) in enumerate(agents):
            txt = f'{name}\n({count}/proj)'
            offset = ((n_agents - 1) / 2 - j) * offset_step
            ax.text(label_x, block_mid + offset, txt, ha='center', va='center',
                    fontsize=fontsize, fontweight='bold', color=color,
                    linespacing=1.4, zorder=2)

    y = block_bot

end_y = y
ax.plot([GRID_L, GRID_R], [end_y, end_y], color='#888888', linewidth=1.0)
ax.plot([GRID_L, GRID_R], [hdr_bot, hdr_bot], color='#888888', linewidth=1.0)


ax.plot([GRID_L + LABEL_W, GRID_L + LABEL_W], [end_y, hdr_bot],
        color='#888888', linewidth=1.0, zorder=3)

ax.set_ylim(end_y - 0.15, FIG_H)

plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
plt.savefig('matrix_comparison.png', dpi=150, bbox_inches='tight')
print("Saved: matrix_comparison.png")
