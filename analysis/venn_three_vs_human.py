"""
venn_three_vs_human.py — polished two-circle AI vs Human Venn diagram
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

plt.rcParams['font.family'] = 'DejaVu Sans'

C_AI     = '#2E6DB4'   # rich blue
C_HUMAN  = '#B5282E'   # deep red
C_SHARED = '#6A4E9C'   # purple — visual blend of AI+Human

fig, ax = plt.subplots(figsize=(15, 9))
fig.patch.set_facecolor('#F8F8F8')
ax.set_xlim(0, 15)
ax.set_ylim(0, 9)
ax.set_aspect('equal')
ax.axis('off')

# ── Geometry ──────────────────────────────────────────────────────────────────
r     = 3.4
cy    = 4.3
cx_ai = 5.5    # AI center
cx_hu = 9.5    # Human center  (d = 4.0, overlap = 2×3.4 − 4.0 = 2.8)
x_lens = (cx_ai + cx_hu) / 2   # = 7.5

# ── Circles ───────────────────────────────────────────────────────────────────
for cx, col in [(cx_ai, C_AI), (cx_hu, C_HUMAN)]:
    ax.add_patch(mpatches.Circle((cx, cy), r,
                                 color=col, alpha=0.09, zorder=1))
    ax.add_patch(mpatches.Circle((cx, cy), r,
                                 fill=False, edgecolor=col,
                                 linewidth=2.6, zorder=2))

# ── Circle labels ─────────────────────────────────────────────────────────────
ax.text(cx_ai, cy + r + 0.52, 'AI Reviewers',
        ha='center', va='center', fontsize=14, fontweight='bold', color=C_AI)
ax.text(cx_ai, cy + r + 0.14, 'Baseline, 531_Ref, Meta_skill',
        ha='center', va='center', fontsize=9.5, color=C_AI, alpha=0.72)
ax.text(cx_hu, cy + r + 0.52, 'Human Expert',
        ha='center', va='center', fontsize=14, fontweight='bold', color=C_HUMAN)

# ── Content helper ────────────────────────────────────────────────────────────
def place(items, x, y, gap=0.42, fs=8.0, color='#1A1A1A',
          fw='normal', style='normal'):
    for item in items:
        ax.text(x, y, item, ha='center', va='center',
                fontsize=fs, color=color, fontweight=fw, fontstyle=style)
        y -= gap

# ── AI-unique (centered vertically in AI-only zone) ──────────────────────────
ai_unique = [
    'Code bugs: wrong time step or wrong axis',
    'Data reversed or silently truncated',
    'Parameter values inconsistent with code',
    'Particle filter applied to simulated data',
    'No non-mechanistic benchmark comparison',
    'Key parameters excluded from rw.sd',
    'MLE lies at search-box boundary',
    'Global search initialized from prior local search',
    'ESS and conditional log-likelihood absent',
    'Smoothed data used with count-based model',
    'Population conservation violations',
]
# 11 items × gap 0.42 = height 4.20 → start at cy + 2.10 to center at cy
place(ai_unique, 4.1, cy + 2.10, gap=0.42, fs=7.8)

# ── Shared (lens center, purple italic) ───────────────────────────────────────
shared = [
    'Invalid log-likelihood comparisons',
    'No profile likelihood CI',
    'Convergence not demonstrated',
    'Measurement model misspecification',
    'Accumulator variable errors',
]
# 5 items × gap 0.44 = height 1.76 → start at cy + 0.88 to center at cy
place(shared, x_lens, cy + 0.88, gap=0.44, fs=8.0, color=C_SHARED,
      fw='bold', style='italic')

# ── Human-unique (centered vertically in Human-only zone) ────────────────────
human_unique = [
    'Wrong model class for the phenomenon',
    'Research framing and motivation',
    'Domain knowledge and data context',
    'Nuanced statistical interpretation',
    'Project scope and novelty',
    'Practical modeling alternatives',
]
# 6 items × gap 0.44 = height 2.20 → start at cy + 1.10 to center at cy
place(human_unique, 10.9, cy + 1.10, gap=0.44, fs=7.8)

# ── Title ─────────────────────────────────────────────────────────────────────
fig.suptitle(
    'AI Reviewers vs Human Expert',
    fontsize=14, fontweight='bold', y=0.995,
)

# ── Footer ────────────────────────────────────────────────────────────────────
ax.text(x_lens, 0.32,
        'Left = AI-unique   |   Center = both find    |   Right = human-unique',
        ha='center', va='center', fontsize=9.0, color='#666666')

plt.tight_layout(pad=0.4)
out = 'venn_three_vs_human.png'
plt.savefig(out, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print(f'Saved: {out}')
