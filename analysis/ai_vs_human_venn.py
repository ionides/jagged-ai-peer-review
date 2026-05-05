"""
ai_vs_human_venn.py
Generate per-reviewer AI vs Human Venn diagrams (4 individual + 1 summary).
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

plt.rcParams['font.family'] = 'DejaVu Sans'

# ── Color palette ─────────────────────────────────────────────────────────────
AI_COLOR    = '#4C72B0'   # blue  — AI reviewer
HUM_COLOR   = '#C44E52'   # red   — Human reviewer
SHARE_COLOR = '#55A868'   # green — shared

REV_COLORS = {
    'Alex':    '#4C72B0',
    'Charlie': '#DD8452',
    'Doug':    '#55A868',
    'Evan':    '#8172B3',
}

# ── Helper ────────────────────────────────────────────────────────────────────

def draw_two_circle_venn(ax, cx_ai, cx_hu, cy, r,
                         ai_items, shared_items, human_items,
                         ai_label, hu_label='Human',
                         ai_color=AI_COLOR, hu_color=HUM_COLOR):
    """Draw a two-circle Venn on a given Axes."""
    # Circles
    for cx, color in [(cx_ai, ai_color), (cx_hu, hu_color)]:
        ax.add_patch(mpatches.Circle((cx, cy), r, color=color, alpha=0.10, zorder=1))
        ax.add_patch(mpatches.Circle((cx, cy), r, fill=False,
                                     edgecolor=color, linewidth=2.2, zorder=2))

    # Labels
    ax.text(cx_ai, cy + r - 0.42, ai_label, ha='center', va='center',
            fontsize=11, fontweight='bold', color=ai_color)
    ax.text(cx_hu, cy + r - 0.42, hu_label, ha='center', va='center',
            fontsize=11, fontweight='bold', color=hu_color)

    # AI-unique items (left side)
    y = cy + 0.85
    for item in ai_items:
        ax.text(cx_ai - 0.5, y, item, ha='center', va='center',
                fontsize=7.5, color='#111111')
        y -= 0.40

    # Shared items (center overlap)
    y = cy + 0.65
    for item in shared_items:
        ax.text((cx_ai + cx_hu) / 2, y, item, ha='center', va='center',
                fontsize=7.2, color='#111111', fontweight='semibold')
        y -= 0.36

    # Human-unique items (right side)
    y = cy + 0.85
    for item in human_items:
        ax.text(cx_hu + 0.5, y, item, ha='center', va='center',
                fontsize=7.5, color='#111111')
        y -= 0.40


# ═══════════════════════════════════════════════════════════════════════════════
# Figure 1–4: Individual reviewer Venn diagrams
# ═══════════════════════════════════════════════════════════════════════════════

REVIEWER_DATA = {
    'Alex': {
        'ai_items': [
            'Code bugs: wrong time step,',
            'wrong object, wrong axis',
            'Data reversed / truncated',
            '  silently',
            'Text ≠ code parameter values',
            'Particle filter on simulated data',
            'Ad hoc search box / circular box',
            'Attribution / verbatim copying',
            'Suppressed eval=FALSE output',
        ],
        'shared_items': [
            'Invalid LL comparisons',
            'Measurement model errors',
            'Convergence not shown',
        ],
        'human_items': [
            'Wrong model class for',
            '  phenomenon',
            'Research framing / motivation',
            'Flat profile = non-identifiability',
            '  (not convergence failure)',
            'Domain knowledge / data context',
            'EDA quality & interpretation',
            'Weak ID may be acceptable',
        ],
        'color': REV_COLORS['Alex'],
    },
    'Charlie': {
        'ai_items': [
            'No benchmark comparison',
            '  (absent in ~13/16 projects)',
            'rw.sd excludes key parameters',
            'MLE at box boundary',
            'Global search warm-started',
            '  from local mif2 result',
            'AIC from median, not max LL',
            'Benchmark failure = revision signal',
            'Np too small; cooling misconfigured',
        ],
        'shared_items': [
            'No profile CI',
            'Convergence not demonstrated',
            'Measurement model errors',
        ],
        'human_items': [
            'Wrong model class for',
            '  phenomenon',
            'Model motivation / domain fit',
            'Sample size vs model complexity',
            'Flat profile = data feature,',
            '  not solver failure',
            'Practical modeling alternatives',
            'Presentation & exposition gaps',
        ],
        'color': REV_COLORS['Charlie'],
    },
    'Doug': {
        'ai_items': [
            'ESS / conditional LL absent',
            'Smoothed data → count model',
            'Global search warm-started',
            'Conservation violations (S<0,',
            '  double-counting flows)',
            'AIC from median LL',
            'MC variance ignored in comparison',
            'Accumvars not reset (H=5 persists)',
        ],
        'shared_items': [
            'No profile CI',
            'Convergence not demonstrated',
            'Accumulator semantic errors',
        ],
        'human_items': [
            'Wrong model class for',
            '  phenomenon',
            'Model motivation / domain fit',
            'What structural change would fix it',
            'Flat profile = identifiability fact',
            'Domain-specific validity',
            '  (data source, epidemiology)',
            'Presentation & table formatting',
        ],
        'color': REV_COLORS['Doug'],
    },
    'Evan': {
        'ai_items': [
            'LL ~ −10¹⁴: overflow =',
            '  misspecification signal',
            'Profile present but unresolvable',
            '  (sparse, flat, max ambiguous)',
            'rho → 1 at boundary:',
            '  degenerate measurement model',
            'sigma < 0 / v₀ < 0: physically',
            '  impossible estimates',
        ],
        'shared_items': [
            'Invalid LL comparisons',
            'No profile CI',
            'Missing diagnostics',
            'Fixed params w/o justification',
        ],
        'human_items': [
            'Wrong model class for',
            '  phenomenon',
            'Model motivation / domain fit',
            'Project scope: routine vs novel',
            'Practical alternatives (log scale,',
            '  simpler model first)',
            'Writing quality / AI-artifact',
            'Data frequency for model class',
        ],
        'color': REV_COLORS['Evan'],
    },
}

for rev, data in REVIEWER_DATA.items():
    fig, ax = plt.subplots(figsize=(13, 8))
    fig.patch.set_facecolor('#F9F9F9')
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8)
    ax.set_aspect('equal')
    ax.axis('off')

    r  = 3.0
    cy = 4.0
    cx_ai = 3.8
    cx_hu = 9.2

    draw_two_circle_venn(
        ax, cx_ai, cx_hu, cy, r,
        data['ai_items'],
        data['shared_items'],
        data['human_items'],
        ai_label=rev,
        ai_color=data['color'],
        hu_color=HUM_COLOR,
    )

    # Footer
    ax.text(6.5, 0.35,
            'Bold center = findings both make  |  '
            'Left = AI-only (A-findings)  |  '
            'Right = Human-only (E-findings)',
            ha='center', va='center', fontsize=8.5, color='#555555')

    fig.suptitle(f'{rev} vs Human Reviewer: Finding Territory Map (W21–W25)',
                 fontsize=13, fontweight='bold', y=0.97)

    fname = f'venn_{rev.lower()}_vs_human.png'
    plt.tight_layout(pad=0.5)
    plt.savefig(fname, dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    plt.close()
    print(f'Saved: {fname}')


# ═══════════════════════════════════════════════════════════════════════════════
# Figure 5: Summary — all AI reviewers vs Human (4-circle + 1 human)
# ═══════════════════════════════════════════════════════════════════════════════

fig, ax = plt.subplots(figsize=(16, 12))
fig.patch.set_facecolor('#F9F9F9')
ax.set_xlim(0, 16)
ax.set_ylim(0, 12)
ax.set_aspect('equal')
ax.axis('off')

# Four AI reviewer circles (corners) + one human circle (center)
r_ai  = 2.8
r_hum = 2.6

positions = {
    'Alex':    (3.2,  9.0),
    'Charlie': (12.8, 9.0),
    'Doug':    (3.2,  3.2),
    'Evan':    (12.8, 3.2),
}
cx_hum, cy_hum = 8.0, 6.1

# Human circle
ax.add_patch(mpatches.Circle((cx_hum, cy_hum), r_hum,
                              color=HUM_COLOR, alpha=0.12, zorder=1))
ax.add_patch(mpatches.Circle((cx_hum, cy_hum), r_hum, fill=False,
                              edgecolor=HUM_COLOR, linewidth=2.5, zorder=2))
ax.text(cx_hum, cy_hum + r_hum - 0.4, 'Human', ha='center', va='center',
        fontsize=13, fontweight='bold', color=HUM_COLOR)

# Human-unique content
human_center_items = [
    'Wrong model class for phenomenon',
    'Research framing / motivation',
    'Domain knowledge & data context',
    'Statistical interpretation nuance',
    'Project scope & novelty assessment',
    'Practical modeling alternatives',
]
y = cy_hum + 0.5
for item in human_center_items:
    ax.text(cx_hum, y, item, ha='center', va='center',
            fontsize=7.8, color='#111111')
    y -= 0.38

# AI reviewer circles
for rev, (cx, cy) in positions.items():
    color = REV_COLORS[rev]
    ax.add_patch(mpatches.Circle((cx, cy), r_ai,
                                 color=color, alpha=0.10, zorder=1))
    ax.add_patch(mpatches.Circle((cx, cy), r_ai, fill=False,
                                 edgecolor=color, linewidth=2.2, zorder=2))
    ax.text(cx, cy + r_ai - 0.4, rev, ha='center', va='center',
            fontsize=12, fontweight='bold', color=color)

# Unique content per AI reviewer
unique_items = {
    'Alex': [
        'Code bugs: wrong time step,',
        '  wrong object, wrong axis',
        'Data reversed / silently truncated',
        'Text ≠ code parameter values',
        'Pfilter on simulated data',
        'Attribution / reproducibility',
    ],
    'Charlie': [
        'No benchmark comparison',
        '  (systematic, all projects)',
        'rw.sd excludes key parameters',
        'MLE at box boundary',
        'Benchmark failure = revision signal',
        'AIC from median LL',
    ],
    'Doug': [
        'ESS / conditional LL absent',
        'Smoothed data → count model',
        'Conservation violations',
        '  (S<0, double-count flows)',
        'MC variance in LL ignored',
        'accumvars not reset',
    ],
    'Evan': [
        'LL ~ −10¹⁴ = misspecification',
        'Profile unresolvable (sparse,',
        '  flat, max ambiguous)',
        'rho → 1: degenerate model',
        'Physically impossible estimates',
        '  (sigma<0, v₀<0)',
    ],
}

offset_map = {
    'Alex':    (-0.5, 0.8),
    'Charlie': (0.5,  0.8),
    'Doug':    (-0.5, 0.8),
    'Evan':    (0.5,  0.8),
}
for rev, (cx, cy) in positions.items():
    ox, oy_start = offset_map[rev]
    y = cy + oy_start
    for item in unique_items[rev]:
        ax.text(cx + ox*0.3, y, item, ha='center', va='center',
                fontsize=7.2, color='#111111')
        y -= 0.37

# Shared zone label (center, between all circles and human)
ax.text(cx_hum, 0.55,
        'All four AI reviewers share: No profile CI  ·  Invalid LL comparisons  ·  '
        'Missing diagnostics  ·  Fixed params w/o justification  ·  Global search warm-start',
        ha='center', va='center', fontsize=8.5, color='#333333',
        fontweight='semibold',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#EEEEEE',
                  edgecolor='#999999', linewidth=1))

fig.suptitle(
    'AI Reviewers vs Human: Finding Territory Map — All Reviewers (W21–W25)',
    fontsize=13, fontweight='bold', y=0.99,
)

ax.text(8.0, 11.55,
        'Each AI circle = what that reviewer finds that humans miss  |  '
        'Human circle = what expert finds that all AI miss  |  '
        'Bottom bar = universal AI findings (all four, not in human review)',
        ha='center', va='center', fontsize=8.5, color='#555555')

plt.tight_layout(pad=0.3)
plt.savefig('venn_all_vs_human.png', dpi=150, bbox_inches='tight',
            facecolor=fig.get_facecolor())
plt.close()
print('Saved: venn_all_vs_human.png')

print('\nAll Venn diagrams generated.')
