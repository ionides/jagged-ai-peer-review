import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'DejaVu Sans'

themes = [
    'Statistical\ninterpretation',
    'Argumentation /\nnarrative',
    'Presentation /\nvisualization',
    'Model improvement\ndirection',
    'Domain /\ndata context',
]
counts = [52, 34, 31, 26, 9]
colors = ['#4C72B0', '#DD8452', '#55A868', '#C44E52', '#8172B3']

fig, ax = plt.subplots(figsize=(13, 9))

wedges, _, autotexts = ax.pie(
    counts,
    labels=None,
    colors=colors,
    autopct='%1.0f%%',
    startangle=140,
    pctdistance=0.65,
    wedgeprops=dict(edgecolor='white', linewidth=1.5),
)

for at in autotexts:
    at.set_fontsize(15)
    at.set_fontweight('bold')
    at.set_color('white')

legend_labels = [f'{t}  ({c})' for t, c in zip(
    ['Statistical interpretation', 'Argumentation / narrative',
     'Presentation / visualization', 'Model improvement direction',
     'Domain / data context'],
    counts
)]
legend = ax.legend(wedges, legend_labels,
                   loc='center left',
                   bbox_to_anchor=(0.75, 0.9),
                   fontsize=14,
                   frameon=False,
                   title='Category Breakdown of Human-Only Points\n(W21–W25)\n',
                   title_fontsize=16)
legend.get_title().set_fontweight('bold')
legend.get_title().set_multialignment('center')

plt.tight_layout()
plt.savefig('theme_piechart.png', dpi=150, bbox_inches='tight')
print("Saved: theme_piechart.png")
