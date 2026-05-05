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

fig, ax = plt.subplots(figsize=(10, 5))

bars = ax.bar(themes, counts, color=colors, width=0.55, edgecolor='white', linewidth=0.8)

for bar, count in zip(bars, counts):
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.8,
            str(count),
            ha='center', va='bottom', fontsize=12, fontweight='bold', color='#1a1a1a')

total = sum(counts)
for bar, count in zip(bars, counts):
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() / 2,
            f'{count/total*100:.0f}%',
            ha='center', va='center', fontsize=11, color='white', fontweight='bold')

ax.set_ylabel('Counts', fontsize=11)
ax.set_title('Category E (W21–W25)',
             fontsize=13, fontweight='bold', pad=12)
ax.set_ylim(0, 62)
ax.grid(axis='y', linestyle='--', alpha=0.4)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(axis='x', labelsize=10)

plt.tight_layout()
plt.savefig('theme_breakdown.png', dpi=150, bbox_inches='tight')
print("Saved: theme_breakdown.png")
