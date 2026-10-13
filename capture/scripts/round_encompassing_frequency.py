"""Round the original per-account crossing frequencies to the selected fractions.

Run: PYTHONPATH=capture python3 -m scripts.round_encompassing_frequency REPORT_FOLDER
Writes a separate frequency-fractions directory; original evidence is read-only.
"""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
import argparse
import hashlib
import json
from pathlib import Path


ACCOUNTS = ('foundations', 'linear', 'multivariable', 'differential')
ALLOWED_WEIGHTS = tuple(Fraction(value) for value in
                        ('1/5', '1/4', '1/3', '2/5', '1/2', '3/5', '2/3', '3/4', '4/5', '1'))
METHOD = ('Weight = rising eligible activities / all eligible activities, rounded '
          'to the nearest selected fraction; exact-distance ties choose the larger fraction. '
          'Each rising activity counts once, regardless of jump magnitude. '
          'The original account-local candidate set, denominators, and activity sequences are retained.')


def nearest_fraction(rises, activities):
    """Use rational arithmetic so thirds and exact midpoint ties are unambiguous."""
    if (type(rises) is not int or type(activities) is not int
            or not 0 < rises <= activities):
        raise ValueError('Positive original frequency counts must satisfy 0 < K <= N.')
    raw = Fraction(rises, activities)
    return min(ALLOWED_WEIGHTS, key=lambda candidate: (abs(candidate - raw), -candidate))


def fraction_counts(proposals):
    counts = Counter(item['weight_fraction'] for item in proposals)
    return {str(weight): counts[str(weight)] for weight in ALLOWED_WEIGHTS}


def convert_account(source_path, account):
    """Return a derivative without modifying its frozen input or account evidence."""
    source_path = Path(source_path).resolve()
    content = source_path.read_bytes()
    report = json.loads(content)
    if report['account'] != account:
        raise ValueError('Source account does not match requested account.')
    original_report = Path(report['source_report'])
    if hashlib.sha256(original_report.read_bytes()).hexdigest() != report['source_report_sha256']:
        raise ValueError('Original source-report hash does not match frozen evidence.')
    seen = set()
    for item in report['proposals']:
        if item['account'] != account or any(event['account'] != account for event in item['sequence']):
            raise ValueError('Cross-account observation in original estimate.')
        pair = (item['source'], item['target'])
        if pair in seen:
            raise ValueError('Duplicate source-target pair within an account.')
        seen.add(pair)
        rises, activities = item['rising_activities'], item['eligible_activities']
        weight = nearest_fraction(rises, activities)
        if (len(item['sequence']) != activities
                or sum(event['after'] > event['before'] for event in item['sequence']) != rises
                or item['frequency_weight_estimate'] != rises / activities):
            raise ValueError('Original frequency counts disagree with preserved sequence.')
        item['original_proposed_starting_coverage_weight'] = item['proposed_starting_coverage_weight']
        item['proposed_starting_coverage_weight'] = float(weight)
        item['weight_fraction'] = str(weight)
        item['frequency_fraction'] = str(Fraction(rises, activities))
        item['weight_status'] = 'Selected initial weight: original crossing frequency rounded to the chosen fraction set.'
    report['original_created_at'] = report['created_at']
    report['created_at'] = datetime.now(timezone.utc).isoformat()
    report['original_method'] = report['method']
    report['method'] = METHOD
    report['original_frequency_estimates'] = str(source_path)
    report['original_frequency_estimates_sha256'] = hashlib.sha256(content).hexdigest()
    report['allowed_weight_fractions'] = [str(weight) for weight in ALLOWED_WEIGHTS]
    report['rounding_tie_rule'] = 'Choose the larger fraction.'
    report['assumptions'] = [
        'Use observed crossing frequency as the selected practical encompassing-weight estimate.',
        'Count every eligible rising activity once; retain larger jump magnitudes as supporting evidence only.',
        'Retain all original candidates, including single-activity relationships.',
        'Do not adjust for spacing, magnitude, content, or later diagnostic/relearning analyses.',
        'Keep each account independent; never pool its observations with another account.',
    ]
    return report


def generate(folder, output_folder=None):
    folder = Path(folder).resolve()
    output_folder = Path(output_folder).resolve() if output_folder else folder / 'frequency-fractions'
    if output_folder == folder:
        raise ValueError('Output must be separate from the original frozen estimates.')
    # Validate every account before writing any output.
    reports = [convert_account(folder / (account + '-frequency-estimates.json'), account)
               for account in ACCOUNTS]
    proposals = [item for report in reports for item in report['proposals']]
    summary = {
        'method': METHOD,
        'allowed_weight_fractions': [str(weight) for weight in ALLOWED_WEIGHTS],
        'account_specific_relationships': len(proposals),
        'unique_source_target_pairs': len({(item['source'], item['target']) for item in proposals}),
        'unique_source_topics': len({item['source'] for item in proposals}),
        'single_activity_relationships': sum(item['eligible_activities'] == 1 for item in proposals),
        'fraction_counts': fraction_counts(proposals),
        'accounts': {},
        'database_changes': False,
    }
    output_folder.mkdir(parents=True, exist_ok=True)
    for report in reports:
        account, items = report['account'], report['proposals']
        summary['accounts'][account] = {
            'relationships': len(items),
            'source_topics': len({item['source'] for item in items}),
            'single_activity_relationships': sum(item['eligible_activities'] == 1 for item in items),
            'fraction_counts': fraction_counts(items),
            'original_frequency_estimates': report['original_frequency_estimates'],
            'original_frequency_estimates_sha256': report['original_frequency_estimates_sha256'],
        }
        (output_folder / (account + '-frequency-estimates.json')).write_text(json.dumps(report, indent=2) + '\n')
    (output_folder / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    lines = [
        '# Initial frequency weights at the selected fractions', '',
        'These are the selected initial encompassing estimates. They use the original frequency method and the requested human-friendly fractions.', '',
        '`w = nearest_fraction(K / N)`', '',
        '- `K`: original eligible activities with an upward target-band change.',
        '- `N`: all original eligible activities for the same source, target, and account; flats and falls remain in the denominator.',
        '- Allowed weights: **1/5, 1/4, 1/3, 2/5, 1/2, 3/5, 2/3, 3/4, 4/5, 1**.',
        '- Distances are calculated as exact rational numbers; midpoint ties round upward.',
        '- A 1→6 rise contributes one rising activity, as does 3→4. The original jump sizes and full sequences remain available.',
        '- No additional eligibility filters, sample-count threshold, or spacing, magnitude, content, or diagnostic corrections are applied.',
        '- Accounts remain separate. This directory does not select between accounts for a shared database relationship.', '',
        f"There are **{summary['account_specific_relationships']:,} account-specific relationships**, covering **{summary['unique_source_target_pairs']:,} unique source-target pairs** and **{summary['unique_source_topics']} source topics**. **{summary['single_activity_relationships']:,}** relationships have one eligible observation and are retained.", '',
        '| Account | Relationships | Single-observation relationships |',
        '|---|---:|---:|',
    ]
    for account, values in summary['accounts'].items():
        lines.append(f"| {account} | {values['relationships']} | {values['single_activity_relationships']} |")
    lines += ['', '| Weight | Account-specific relationships |', '|---|---:|']
    lines += [f'| {fraction} | {count} |' for fraction, count in summary['fraction_counts'].items()]
    lines += ['', 'The original frequency files are preserved unchanged. Each derivative records its original file SHA-256 and retains the underlying source-report path and SHA-256. The numerical `proposed_starting_coverage_weight` is accompanied by exact `weight_fraction` and `frequency_fraction` strings. Values below 1/5 round to 1/5; no zero edge is introduced.', '',
              'Reproduce from the repository root:', '', '```bash',
              'PYTHONPATH=capture python3 -m scripts.round_encompassing_frequency reference/mathacademy/encompassing-analysis-2026-10-11', '```', '',
              'No database writes are performed by this generator.']
    (output_folder / 'README.md').write_text('\n'.join(lines) + '\n')
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', type=Path)
    parser.add_argument('--output-folder', type=Path)
    args = parser.parse_args()
    print(json.dumps(generate(args.folder, args.output_folder), indent=2))


if __name__ == '__main__':
    main()
