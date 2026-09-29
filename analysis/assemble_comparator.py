#!/usr/bin/env python3
"""
Assemble a Comparator output file from sub-reports and human-issues files.

Reads sub-report files verbatim from disk, parses counts and coverage records,
and computes the combined summary table, per-reviewer metrics, consensus misses,
and unique finds deterministically.

Usage:
  python analysis/assemble_comparator.py <semester> [<project>]

Examples:
  python analysis/assemble_comparator.py W25 PROJECT01
  python analysis/assemble_comparator.py W25          # all W25 projects
  python analysis/assemble_comparator.py W21          # regenerate all W21
"""

import sys
import re
from pathlib import Path

REVIEWERS = ['Alex', 'Charlie', 'Doug', 'Evan']

MAX_PROJECTS = {
    'W21': 16,
    'W22': 23,
    'W24': 16,
    'W25': 17,
}


class CoverageError(ValueError):
    """A sub-report's coverage record does not account for every human issue."""


def find_sub_report(sub_dir: Path, reviewer: str, sem: str, proj: str) -> Path | None:
    for prefix in [reviewer, reviewer.lower()]:
        p = sub_dir / f'{prefix}-{sem}_{proj}.md'
        if p.exists():
            return p
    return None


def parse_human_issues(text: str) -> dict[int, str]:
    issues = {}
    for line in text.split('\n'):
        m = re.match(r'^(\d+)\.\s+(.+)', line)
        if m:
            issues[int(m.group(1))] = m.group(2).strip()
    return issues


def strip_title_line(text: str) -> str:
    lines = [l for l in text.split('\n') if not re.match(r'^# ', l)]
    return '\n'.join(lines).strip()


def parse_coverage(text: str) -> dict[int, str]:
    coverage = {}
    in_coverage = False
    for line in text.split('\n'):
        if '**Coverage record:**' in line:
            in_coverage = True
            continue
        if in_coverage:
            if line.startswith('**'):
                break
            
            m = re.match(
                r'^- Human Issue #(\d+)\s*(?:\([^)]*\))?\s*:\s*(missed|covered|contradiction)',
                line,
                re.IGNORECASE,
            )
            if m:
                coverage[int(m.group(1))] = m.group(2).lower()
    return coverage


def parse_counts(text: str) -> dict[str, int]:
    counts = {cat: 0 for cat in 'ABCDEF'}
    for line in text.split('\n'):
        m = re.match(r'^\|\s*([A-F])\s*\([^)]+\)\s*\|\s*(\d+)\s*\|', line)
        if m:
            counts[m.group(1)] = int(m.group(2))
    return counts


def format_pct(num: int, den: int) -> str:
    if den == 0:
        return 'N/A'
    pct = round(num / den * 100)
    return f'{num}/{den} = {pct}%'


def assemble(sem: str, proj: str, base_dir: Path) -> str:
    results_dir = base_dir / 'results' / 'comparator'

    human_file = results_dir / 'human-issues' / f'human-issues-{sem}_{proj}.md'
    if not human_file.exists():
        raise FileNotFoundError(f'Missing: {human_file}')
    human_text = human_file.read_text()
    human_issues = parse_human_issues(human_text)
    n_human = len(human_issues)
    human_body = strip_title_line(human_text)

    sub_dir = results_dir / 'sub-reports'
    found_reviewers = []
    sub_texts = {}
    coverage_by = {}
    counts_by = {}

    for reviewer in REVIEWERS:
        path = find_sub_report(sub_dir, reviewer, sem, proj)
        if path is None:
            continue
        text = path.read_text()
        if 'file not found' in text.lower() and len(text.strip().split('\n')) <= 3:
            continue
        found_reviewers.append(reviewer)
        sub_texts[reviewer] = text.rstrip()
        coverage_by[reviewer] = parse_coverage(text)
        counts_by[reviewer] = parse_counts(text)

    # A human issue absent from a coverage record must not be scored silently.
    # Consensus misses and unique finds below would read the gap as 'missed',
    # while Human Overlap would drop it from the denominator entirely.
    for reviewer in found_reviewers:
        missing = sorted(set(human_issues) - set(coverage_by[reviewer]))
        extra = sorted(set(coverage_by[reviewer]) - set(human_issues))
        if missing or extra:
            parts = []
            if missing:
                parts.append(f'no coverage line for issue(s) {missing}')
            if extra:
                parts.append(f'coverage line for unknown issue(s) {extra}')
            raise CoverageError(
                f'{reviewer} {sem}_{proj}: {"; ".join(parts)} '
                f'({n_human} human issues in list)'
            )

    k = len(found_reviewers)
    proj_num = proj.replace('PROJECT', '')

    out = []

    out.append(f'# Comparator Analysis — {sem} Project {proj_num}')
    out.append('')
    out.append('---')
    out.append('')
    out.append('## Human Issues')
    out.append('')
    out.append(human_body)
    out.append('')
    out.append('---')
    out.append('')

    for reviewer in found_reviewers:
        out.append(sub_texts[reviewer])
        out.append('')
        out.append('---')
        out.append('')

    # Combined summary table
    out.append('## Combined Summary Table')
    out.append('')
    out.append('| Category | ' + ' | '.join(found_reviewers) + ' |')
    out.append('|----------|' + ''.join(['--------:|' for _ in found_reviewers]))
    for cat, label in [
        ('A', 'AI major, human missed'),
        ('B', 'AI major, human also found'),
        ('C', 'AI minor, human missed'),
        ('D', 'AI minor, human also found'),
        ('E', 'Human found, AI missed'),
        ('F', 'Human-AI contradiction'),
    ]:
        vals = ' | '.join(str(counts_by[r][cat]) for r in found_reviewers)
        out.append(f'| {cat} ({label}) | {vals} |')
    out.append('')
    out.append('---')
    out.append('')

    # Per-reviewer metrics
    out.append('## Per-Reviewer Metrics')
    out.append('')
    out.append('Human Overlap = covered / (covered + missed) = 1 - E/(total human issues), counted over human issues')
    out.append('AI-Unique Rate = (A + C) / (A + B + C + D), counted over AI findings')
    out.append('')
    out.append('| Reviewer | B | D | E | Human Overlap | A | C | AI-Unique Rate |')
    out.append('|----------|--:|--:|--:|--------------:|--:|--:|---------------:|')
    for r in found_reviewers:
        c = counts_by[r]
        cov = coverage_by[r]
        n_cov = sum(1 for v in cov.values() if v == 'covered')
        n_mis = sum(1 for v in cov.values() if v == 'missed')
        ho = format_pct(n_cov, n_cov + n_mis)
        au = format_pct(c['A'] + c['C'], c['A'] + c['B'] + c['C'] + c['D'])
        out.append(f'| {r} | {c["B"]} | {c["D"]} | {c["E"]} | {ho} | {c["A"]} | {c["C"]} | {au} |')
    out.append('')
    out.append('---')
    out.append('')

    # Cross-reviewer aggregation
    out.append('## Cross-Reviewer Aggregation')
    out.append('')
    out.append('### Consensus misses')
    out.append('')
    out.append('Human issues that every reviewer failed to cover:')
    out.append('')

    consensus_nums = []
    for num in sorted(human_issues):
        if all(coverage_by[r].get(num, 'missed') == 'missed' for r in found_reviewers):
            consensus_nums.append(num)
            out.append(
                f'- Human Issue #{num}: {human_issues[num]} '
                f'(Missed by all {k} reviewers — {k} out of {k})'
            )

    if not consensus_nums:
        out.append('(none)')

    out.append('')
    pct = round(len(consensus_nums) / n_human * 100) if n_human else 0
    out.append(f'Total consensus misses: {len(consensus_nums)} out of {n_human} human issues ({pct}%).')
    out.append('')

    out.append('### Unique finds per reviewer')
    out.append('')
    out.append('Human issues covered by exactly one reviewer and missed by all others:')
    out.append('')

    unique_counts = {r: 0 for r in found_reviewers}
    unique_lines = []
    for num in sorted(human_issues):
        coverers = [r for r in found_reviewers if coverage_by[r].get(num, 'missed') == 'covered']
        if len(coverers) == 1:
            unique_counts[coverers[0]] += 1
            unique_lines.append(
                f'- Human Issue #{num}: {human_issues[num]} (Covered only by {coverers[0]})'
            )

    if unique_lines:
        out.extend(unique_lines)
    else:
        out.append('(none)')
    out.append('')

    out.append('| Reviewer | Unique finds |')
    out.append('|----------|-------------:|')
    for r in found_reviewers:
        out.append(f'| {r} | {unique_counts[r]} |')

    return '\n'.join(out) + '\n'


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    sem = sys.argv[1].upper()
    base_dir = Path('.')
    out_dir = base_dir / 'results' / 'comparator'

    if len(sys.argv) >= 3:
        projects = [sys.argv[2].upper()]
    else:
        max_proj = MAX_PROJECTS.get(sem)
        if max_proj is None:
            print(f'Unknown semester: {sem}. Valid: {", ".join(MAX_PROJECTS)}')
            sys.exit(1)
        projects = [f'PROJECT{i:02d}' for i in range(1, max_proj + 1)]

    for proj in projects:
        try:
            content = assemble(sem, proj, base_dir)
            out_file = out_dir / f'comparator-{sem}_{proj}.md'
            out_file.write_text(content)
            print(f'OK  {sem}_{proj}')
        except FileNotFoundError as e:
            print(f'SKIP {sem}_{proj}: {e}')
        except CoverageError as e:
            print(f'ERR  {e}')
        except Exception as e:
            print(f'ERR  {sem}_{proj}: {e}')
            raise


if __name__ == '__main__':
    main()
