import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

plt.rcParams['font.family'] = 'DejaVu Sans'

baseline_color = '#4C72B0'
cd_color       = '#DD8452'
orch_color     = '#8172B3'

# 3 shared + 3 unique per agent
ROWS = [
    # Shared by all — AI flagged, human missed across all agents
    ('data', 'Global search inherits cooled schedule, not truly global (optimization flaw)', True,  True,  True,  '#eeeeee'),
    ('data', 'No ESS or particle filter diagnostics reported (verification gap)',            True,  True,  True,  '#eeeeee'),
    ('data', 'Cross-family log-likelihood comparison invalid (scale mismatch)',        True,  True,  True,  '#eeeeee'),
    # Baseline: code-level bugs caught without any skill file
    ('data', 'Modifying one variable silently changes another (implementation bug)', True,  False, False, '#dce8f8'),
    ('data', 'Code does not implement the model as written (implementation bug)',    True,  False, False, '#dce8f8'),
    ('data', 'Computation produces wrong values without error (implementation bug)', True,  False, False, '#dce8f8'),
    # 531_Ref / Meta-Skill: statistical methodology failures
    ('data', 'Confidence interval procedure is wrong (methodology flaw)',     False, True,  False, '#f8e8d8'),
    ('data', 'No simpler baseline model for comparison (model evaluation)',   False, True,  False, '#f8e8d8'),
    ('data', 'Too few starting values explored in fitting (optimization flaw)',False, True,  False, '#f8e8d8'),
    # Orchestrator: profile quality + domain knowledge issues
    ('data', 'Profile too flat/noisy to extract CIs (identifiability issue)', False, False, True,  '#e8e0f4'),
    ('data', 'Incorrect biological formula in model (domain error)',           False, False, True,  '#e8e0f4'),
    ('data', 'Results lack parameter estimates or captions (omission)',False, False, True,  '#e8e0f4'),
]

N_ROWS  = len(ROWS)
DATA_H  = 0.46
HDR_H   = 0.60
FOOT_H  = 0.52

FIG_W   = 12.5
FIG_H   = N_ROWS * DATA_H + HDR_H + FOOT_H + 0.5

COL_B   = 9.0
COL_C   = 10.1
COL_E   = 11.5
CAT_X   = 0.3
GRID_L  = 0.15
GRID_R  = 12.2
SEP_X   = 8.5

fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
ax.set_xlim(0, FIG_W)
ax.set_ylim(0, FIG_H)
ax.axis('off')

# ── Single header row: title on left, agent names on right ───────────────────
hdr_top = FIG_H
hdr_bot = FIG_H - HDR_H
hdr_mid = (hdr_top + hdr_bot) / 2

# Title left-aligned in the category column area
ax.text(CAT_X, hdr_mid, 'Domain Specific Breakdown of Agent-Unique Review Overlap',
        ha='left', va='center', fontsize=16, fontweight='bold', color='#1a1a1a', zorder=2)

# Agent names centered in their columns
ax.text(COL_B, hdr_mid, 'Baseline',
        ha='center', va='center', fontsize=13, fontweight='bold', color=baseline_color, zorder=2)
ax.text(COL_C, hdr_mid, '531_Ref /\nMeta-Skill',
        ha='center', va='center', fontsize=12, fontweight='bold', color=cd_color, zorder=2)
ax.text(COL_E, hdr_mid, 'Orchestrator',
        ha='center', va='center', fontsize=13, fontweight='bold', color=orch_color, zorder=2)

# ── Top row: AI-unique finding counts ─────────────────────────────────────────
foot_bg = '#f5f5f5'
ax.add_patch(mpatches.Rectangle(
    (GRID_L, hdr_bot - FOOT_H), GRID_R - GRID_L, FOOT_H,
    facecolor=foot_bg, edgecolor='#cccccc', linewidth=0.4, zorder=1
))
foot_mid = hdr_bot - FOOT_H / 2

ax.text(CAT_X, foot_mid, 'AI-unique findings (A+C) — total across W21–W25',
        ha='left', va='center', fontsize=11, fontweight='bold', color='#1a1a1a', zorder=2)

for col_x, label, color in [
    (COL_B, '929\n(12.9/proj)', baseline_color),
    (COL_C, '958\n(13.3/proj)', cd_color),
    (COL_E, '641\n(8.9/proj)',  orch_color),
]:
    ax.text(col_x, foot_mid, label, ha='center', va='center',
            fontsize=11, fontweight='bold', color=color, zorder=2)

# ── Data rows ─────────────────────────────────────────────────────────────────
y = hdr_bot - FOOT_H
for _, label, b, c, e, bg in ROWS:
    ax.add_patch(mpatches.Rectangle(
        (GRID_L, y - DATA_H), GRID_R - GRID_L, DATA_H,
        facecolor=bg, edgecolor='#cccccc', linewidth=0.4, zorder=1
    ))
    mid_y = y - DATA_H / 2
    ax.text(CAT_X, mid_y, label,
            ha='left', va='center', fontsize=12.5,
            fontweight='bold', color='#1a1a1a', zorder=2)
    for col_x, present, color in [(COL_B, b, baseline_color),
                                   (COL_C, c, cd_color),
                                   (COL_E, e, orch_color)]:
        if present:
            ax.text(col_x, mid_y, '✓', ha='center', va='center',
                    fontsize=18, color=color, fontweight='bold', zorder=2)
    y -= DATA_H

end_y = y

# Bottom border
ax.plot([GRID_L, GRID_R], [end_y, end_y], color='#888888', linewidth=1.0)

# Vertical dividers
for vx in [SEP_X, (COL_B + COL_C) / 2, (COL_C + COL_E) / 2]:
    ax.plot([vx, vx], [end_y, hdr_bot], color='#cccccc', linewidth=0.8, zorder=0)

plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
plt.savefig('matrix_comparison.png', dpi=150, bbox_inches='tight')
print("Saved: matrix_comparison.png")
