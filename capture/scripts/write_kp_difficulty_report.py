"""Write the KP difficulty analysis report and standalone plots from saved evidence."""
import json
import math
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def absence_confidence_section():
    # Fixed-basis counts of distinct rated practice questions; shared questions
    # contribute once, rather than once per KP membership.
    counts = {'easy': 13601, 'moderate': 12347, 'hard': 4530}
    total = sum(counts.values())
    lines = [
        '### Absence confidence measure', '',
        '**Absence confidence (a heuristic score): how likely we would have been to observe at least one question at this difficulty, if it occurred at the expected rate.** When a KP has zero observations at a level, a high score means that absence is surprising under the assumed distribution.', '',
        'For a missing level, let n be the number of distinct rated practice questions in the KP and p be the expected share of that level:', '',
        '```text\nP_zero = (1 - p)^n\nAbsence confidence score = 100 × (1 - P_zero)\n```', '',
        'Equivalently, subtract the zero-observation likelihood expressed as a percentage from 100. The score ranges from 0 to 100. Unrated questions and repeat appearances do not increase n. KPs with no rated questions are excluded. An observed question at the level, whether in the database or captures, establishes that it exists and takes precedence over an absence score.', '',
        'The baseline uses **30,478 distinct rated practice questions**, deduplicated by question entity rather than KP membership:', '',
        '| Level | Distinct questions | Expected share p | First n with P_zero below 1% |',
        '|---|---:|---:|---:|',
    ]
    for level, count in counts.items():
        probability = count / total
        threshold = math.floor(math.log(.01) / math.log1p(-probability)) + 1
        lines.append(f'| {level.title()} | {count:,} | {100 * probability:.4f}% | {threshold} |')
    lines += ['', 'For moderate, p = 12347 / 30478 ≈ 0.405111884. Its zero-observation likelihood first falls below 1% at **9 rated questions**, giving an absence confidence score of **99.07**.', '',
        '| Rated questions n | Chance of zero moderate | Absence confidence score |',
        '|---|---:|---:|']
    probability = counts['moderate'] / total
    for n in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30):
        zero_percent = 100 * (1 - probability) ** n
        lines.append(f'| {n} | {zero_percent:.8g}% | {100 - zero_percent:.8g} |')
    lines += ['', '**Interpretation:** with 9 rated questions, a sample would detect at least one moderate question 99.07% of the time under the assumed distribution, yet this KP has none observed. That supplies evidence for absence; it is not a literal 99.07% probability that moderate questions do not exist for that KP.', '',
        'The calculation assumes independent draws and the same expected difficulty share for the KP as the reference distribution. Lesson position, mathematical content, adaptive selection, and deduplication of repeated draws can affect that assumption. The overall shares provide a consistent benchmark; position-specific shares can supply an alternative reference. A posterior probability of true unavailability would additionally require a model of how often KPs lack a level and how existing levels are sampled.', '',
        'For a KP missing multiple levels, report a separate score for each missing level rather than multiplying the confidence scores. This continuous measure supplements the sample-size classifications above.', '']
    return lines


def candidate_absence_section(root):
    folder = root / 'generate/reports/kp-absence-2026-10-12'
    scores = json.loads((folder / 'scores.json').read_text())
    identity = json.loads((root / 'reference/mathacademy/kp-difficulty-analysis-2026-10-12/database/identity.json').read_text())
    if scores['database'] != identity:
        raise ValueError('Candidate scores and report inventory must share database, lineage and basis')
    lines = [
        '### Scores for surfaced candidate KPs', '',
        f"The saved [find_candidates.py](generate/scripts/find_candidates.py) discovery at **{scores['discovery_at']}** surfaces **384 distinct KPs across 120 topics**, at the same database basis **1522** as this report. Of these, **358 have rated questions** and **26 have no rated evidence**. Each KP appears in exactly one missing-level group below.", '',
        'Every missing level receives the separate absence score defined above. A **hybrid score** also measures the entire missing-level pattern. Let M be the set of missing levels and p_M the sum of their expected shares:', '',
        '```text\np_M = sum(p_level for level in M)\nP_zero_pattern = (1 - p_M)^n\nHybrid absence score = 100 × (1 - P_zero_pattern)\n```', '',
        'For two missing levels A and B, this uses the probability of observing neither: (1 − p_A − p_B)ⁿ. For one missing level, the hybrid equals the separate score. With no missing levels or no rated evidence, no hybrid is assigned. The same global shares and independent-draw assumptions apply.', '',
        'A high hybrid means the combined gap is surprising under the reference distribution. It does not imply equally strong evidence for each missing level, or a posterior probability that both levels are unavailable. Keep the separate scores alongside it.', '',
        'The table shows **medians of individual KP scores within each group**, not pooled group confidences. Scores range from 0 to 100; — means no applicable absence score.', '',
        '| Missing levels | KPs | Median easy score | Median moderate score | Median hard score | Median hybrid score |',
        '|---|---:|---:|---:|---:|---:|',
    ]
    def fmt(value):
        if value is None:
            return '—'
        formatted = f'{value:.4f}'
        return '>99.9999' if formatted == '100.0000' else formatted
    for group in scores['groups']:
        cells = [fmt(group['median_level_scores'].get(level)) for level in ('easy', 'moderate', 'hard')]
        lines.append(f"| {group['label']} | {group['kps']} | " + ' | '.join(cells)
                     + ' | ' + fmt(group['median_hybrid_score']) + ' |')
    lines += ['',
        '**320 KPs** have at least one missing level, yielding **443 separate level scores and 320 hybrid scores**. The other **38 rated KPs** have all three levels observed. Values that would round to 100.0000 are shown as >99.9999; the saved JSON retains the zero-observation probabilities.', '',
        '[Every KP’s counts and separate/hybrid scores, organized by group](generate/reports/kp-absence-2026-10-12/report.md) · [Full-precision scores and group summaries](generate/reports/kp-absence-2026-10-12/scores.json) · [Saved discovery output](generate/reports/kp-absence-2026-10-12/candidates.json).', '',
        'Reproduce these scores from the saved discovery and fixed-basis inventory:', '',
        '```bash\npython3 generate/scripts/score_absence.py \\\n  --candidates generate/reports/kp-absence-2026-10-12/candidates.json \\\n  --output generate/reports/kp-absence-2026-10-12\n```', '',
    ]
    return lines


def missing_level_pilot_section():
    return [
        '### Content pilot: can we invent the missing level?', '',
        'Three surfaced KPs with individual missing-level scores between 80 and 95 were examined using [Classify](generate/docs/3-classify.md) and [Template Extraction](generate/docs/4-template-extraction.md), with one missing-easy, one missing-moderate, and one missing-hard case. All 26 practice records were read at basis 1522, with complete choice mappings and available worked solutions preserved.', '',
        '| KP | Missing level | Absence score | Design result |',
        '|---|---|---:|---|',
        '| Finding an Entry of a Matrix | Moderate | 92.5497 | Narrow scope: a fractional entry in a 5×4 matrix still requires one lookup. A convincing moderate family was not found without adding other skills. |',
        '| Computing a Reciprocal Ratio Using the Pythagorean Identity | Easy | 94.7935 | Natural easy family: Pythagorean-triple coordinates preserve identity recovery and inversion while removing rationalization. An unrated original and the canonical example already support simpler in-scope cases. |',
        '| Calculating the Determinant of a 2x2 Matrix With Non-Integer Entries | Hard | 85.4986 | Feasible authored hard family: compound radical fractions add conjugate-product and fraction algebra while retaining the same 2×2 determinant procedure. |', '',
        'Best judgment: retain easy lookup variants; propose an easy reciprocal family; allow a harder determinant family with its prerequisite-algebra burden documented. Absence scores prioritize investigation; content scope and meaningful difficulty separation decide whether to invent a missing level. Authored labels remain distinct from source-observed labels.', '',
        '[Full three-KP analysis, classifications, and template extractions](generate/reports/missing-level-pilot-2026-10-12/report.md) · [Concrete probes and worked solutions](generate/reports/missing-level-pilot-2026-10-12/probes.md) · [Exact verification](generate/reports/missing-level-pilot-2026-10-12/probe-verification.json). No database facts were changed.', '',
    ]


def main():
    root=Path(__file__).resolve().parents[2]
    f=root/'reference/mathacademy/kp-difficulty-analysis-2026-10-12'
    rows=json.loads((f/'kp-inventory.json').read_text());s=json.loads((f/'summary.json').read_text());p=json.loads((f/'position-comparisons.json').read_text())
    levels=('easy','moderate','hard');colors=('#3b9e78','#e2a641','#c75861')
    fig,axes=plt.subplots(1,2,figsize=(11.5,4.1),layout='constrained')
    positions=range(1,5);bottom=[0.]*4
    for l,c in zip(levels,colors):
     values=[s['all_positions'][str(i)]['question_percent'][l] for i in positions]
     axes[0].bar(list(positions),values,bottom=bottom,color=c,label=l.title(),width=.66)
     bottom=[a+b for a,b in zip(bottom,values)]
    axes[0].set(title='Rated question distribution',xlabel='KP position in lesson',ylabel='Share of distinct rated questions (%)',xticks=list(positions),ylim=(0,108))
    for i in positions:
     axes[0].text(i,102,f"{s['all_positions'][str(i)]['questions']:,} questions",ha='center',fontsize=8)
    fig.legend(*axes[0].get_legend_handles_labels(),loc='outside lower center',ncol=3,frameon=False)
    for l,c in zip(('easy','hard'),(colors[0],colors[2])):
     values=[]
     for i in positions:
      group=[r for r in rows if r['rated_questions']>=10 and r['latest_position'] and r['latest_position']['position']==i]
      values.append(100*sum(r['counts'][l]>0 for r in group)/len(group))
     axes[1].plot(list(positions),values,'o-',label=l.title(),color=c,linewidth=2)
    axes[1].set(title='Observed options (≥10 rated questions per KP)',xlabel='KP position in lesson',ylabel='KPs with at least one question at level (%)',xticks=list(positions),ylim=(0,108))
    for i in positions:
     n=sum(bool(r['rated_questions']>=10 and r['latest_position'] and r['latest_position']['position']==i) for r in rows)
     axes[1].text(i,102,f'{n} KPs',ha='center',fontsize=8)
    axes[1].legend(loc='lower right');axes[1].grid(axis='y',alpha=.2)
    fig.suptitle('Math Academy KP difficulty and lesson position — database basis 1522',fontsize=13)
    fig.savefig(f/'position-distribution.png',dpi=170)
    fig.savefig(f/'position-distribution.svg')
    plt.close(fig)
    lines=['# KP difficulty options and lesson position', '',
    '**Best estimate: many KPs have a restricted difficulty range, and that range is strongly associated with lesson position.** Early KPs favor easy questions; later KPs favor moderate and hard questions. Position supplies a useful prior, but does not determine the allowed levels: hard first-position questions and easy final-position questions both exist.', '',
    'At 20 or more distinct rated questions, **26 KPs likely lack hard questions, 13 likely lack easy questions, and 7 likely lack moderate questions**. These correspond to **35 distinct KPs with at least one likely unavailable level**. The four moderate-only KPs appear in both the no-easy and no-hard counts. The largest rated sample is **27**, so there are no 30-question cases in this snapshot.', '',
    '## Database inventory first', '',
    'This report analyzes practice questions linked to an identified KP. The analysis starts with the EDB `math` database at immutable basis **1522**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. All database reads use that basis. No database facts were changed.', '',
    '| Inventory | Count |','|---|---:|',
    f"| KPs | {s['database_kps']:,} |",f"| Distinct questions in practice pools | {s['unique_database_questions']:,} |",f"| KP–question memberships | {s['total_questions']:,} |",f"| Rated memberships | {s['rated_questions']:,} |",'| Unrated memberships | 16,296 |','| KPs with no rated questions | 5,716 |','| KPs with at least 10 rated questions | 1,168 |','| KPs with at least 20 rated questions | 51 |','',
    'One question is shared between two pools, so the membership count exceeds the distinct-question count by one. All 30,479 rated memberships have Math Academy source attribution. The strongest absence candidates therefore use source-observed ratings. Canonical worked examples are excluded: the inventory reads `:knowledge-point/questions`, not the canonical-example reference.', '',
    'Raw zero counts are **6,831 KPs without easy, 6,835 without moderate, and 8,474 without hard**. These are database absences, not evidence that Math Academy lacks those options. Most have inadequate rated coverage.', '',
    'Excluding the **5,716 KPs with no difficulty ratings across all three levels** leaves **3,923 KPs**. Each KP appears exactly once below, grouped by its missing levels. These are gaps in the collected ratings, before estimating whether those levels likely exist.', '',
    '| Missing levels | Count |', '|---|---:|',
    '| None | 452 |', '| Easy | 520 |', '| Moderate | 39 |', '| Hard | 1,391 |',
    '| Easy–moderate | 154 |', '| Moderate–hard | 926 |', '| Easy–hard | 441 |',
    '| **Total** | **3,923** |', '',
    '## Position and distribution', '',
    'Full captured lesson inventories assign positions to **2,538 KPs**. The evidence contains **955 lesson captures**, covering **789 distinct topics**. Positions count KPs, starting at 1; tutorials do not occupy KP positions. Modern captures use explicit lesson-definition order. Legacy captures use completed-lesson checkpoint order, checked against numbered history labels. Every legacy lesson used passed that order check. No matched KP changed numerical position across its captured lessons.', '',
    '![Distribution and observed difficulty options](reference/mathacademy/kp-difficulty-analysis-2026-10-12/position-distribution.png)', '',
    '| KP position | KPs with known position | Rated questions | Easy | Moderate | Hard |', '|---|---:|---:|---:|---:|---:|']
    for i in range(1,6):
     r=s['all_positions'][str(i)];lines.append(f"| {i} | {r['kps']} | {r['questions']:,} | {r['question_percent']['easy']:.1f}% | {r['question_percent']['moderate']:.1f}% | {r['question_percent']['hard']:.1f}% |")
    lines+=['', 'The fifth-position sample has only four KPs. The first four positions provide the useful pattern. Giving each KP equal weight produces the same progression, rather than allowing a few larger pools to drive it.', '',
    'Availability also changes with position. Restricting this comparison to KPs with at least 10 rated questions:', '',
    '| Position | KPs | Easy observed | Hard observed |','|---|---:|---:|---:|']
    for i in range(1,5):
     g=[r for r in rows if r['rated_questions']>=10 and r['latest_position'] and r['latest_position']['position']==i]
     lines.append(f"| {i} | {len(g)} | {100*sum(r['counts']['easy']>0 for r in g)/len(g):.1f}% | {100*sum(r['counts']['hard']>0 for r in g)/len(g):.1f}% |")
    lines+=['', '### Comparison within the same lesson', '',
    'For each topic, select its latest complete captured lesson, then compare its first and final KP. Give each topic equal weight. Among **197 topics** where both endpoints have at least 10 rated questions:', '',
    '| Final KP minus first KP | Difference | Topic-bootstrap 95% interval |','|---|---:|---:|']
    for l in levels:
     v=p['paired_latest_lesson_first_last']['10']['question_share_difference_last_minus_first'][l];lo,hi=v['bootstrap_95_percent_interval'];lines.append(f"| {l.title()} question share | {v['mean_percentage_points']:+.1f} percentage points | {lo:+.1f} to {hi:+.1f} |")
    lines+=['', 'The final KP is also **45.7 percentage points more likely to have at least one observed hard question**, and **52.3 points less likely to have an observed easy question**. The direction persists in two-, three-, and four-KP lessons and across sample-size cutoffs of 1, 5, 10 and 15 questions. At 20 questions, few matched endpoint pairs remain; that subgroup is not suitable for a precise position estimate. Intervals resample captured topics 4,000 times with seed 20261012; they measure stability within these observations, not a random sample of the entire Math Academy curriculum.', '',
    '### Position does not impose a fixed level', '',
    'Examples with actual database counts:', '',
    '| KP | Position | Easy / Moderate / Hard |','|---|---:|---:|',
    '| Classifying a Given Critical Point Using the Second Derivative Test (`e-3744`) | 1 of 2 | 7 / 2 / 11 |',
    '| Finding the Cartesian Equation of a Curve Defined Parametrically (`e-5087`) | 1 of 2 | 11 / 6 / 3 |',
    '| Evaluating Definite Integrals (`e-14422`) | 3 of 3 | 16 / 5 / 6 |',
    '| Finding a Derivative Using Properties of Inverse Functions (`e-14722`) | 4 of 4 | 4 / 9 / 12 |','',
    'The likely explanation is instructional sequencing: lessons begin with simpler procedures and progress to more demanding variants. The procedure demonstrated by a KP drives its question repertoire. Our captures do not move the same KP between positions, so they cannot isolate position itself from the mathematical content.', '',
    '## Distinguishing missing collection from likely unavailable options', '',
    'Count **distinct practice questions with source-observed ratings**, not repeated appearances, attempts, or canonical examples. Use only rated questions as the sampling denominator. Unrated questions stay visible in the inventory; they are not counted as easy, moderate or hard.', '',
    'For every KP and level, apply this practical decision rule:', '',
    '| Evidence | Classification |','|---|---|',
    '| At least one question at the level in EDB | Observed in database |',
    '| No question at the level in EDB, but one exists in captures | Exists; database pool incomplete |',
    '| Zero at the level and at least 20 distinct source-rated questions | Best guess: unavailable |',
    '| Zero at the level and 10–19 rated questions | Tentative absence |',
    '| Zero at the level and fewer than 10 rated questions | Insufficient sampling |','',
    'All KPs remain in the evidence files, including zero-question and four-question cases. The cutoffs classify strength; they do not exclude observations. Future 30-question cases with multiple captured tasks receive a stronger label. No current KP meets that threshold.', '',
    'For a missing level with n rated questions, a simple sampling diagnostic is:', '',
    '```text\nP(no observations | level selected with probability p) = (1 - p)^n\n```','',
    '| n | p = 5% | p = 10% | p = 15% |','|---|---:|---:|---:|']
    for n in (4,10,20,27,30):lines.append(f"| {n} | {100*.95**n:.1f}% | {100*.9**n:.1f}% | {100*.85**n:.1f}% |")
    lines+=['', 'This is an illustrative sampling calculation, not a posterior probability that an option exists. Distinct scraped questions are selected adaptively, and difficulty levels need not be equally common. A rare level can remain unseen even with a substantial sample. The best-guess classifications also gain support from the strong position pattern, recurring single-level or two-level pools, multiple captured tasks, and neighboring KPs that did receive the supposedly missing level.', '',
    *absence_confidence_section(),
    'All **13 likely no-easy KPs** have easy questions in other KPs of the same captured lesson. **12 of the 26 likely no-hard KPs** have hard questions elsewhere in the same captured lesson. This makes a general lack of easy or hard sampling an inadequate explanation for those cases. It does not rule out KP-specific adaptive selection.', '',
    'Of the 51 KPs with at least 20 rated questions: **7 are easy-only, 4 moderate-only, 15 easy/moderate, 9 moderate/hard, and 16 have all three levels**. Persistent restricted repertoires are therefore common in our best-sampled group.', '',
    '### Full list of best-guess restricted KPs', '',
    'Counts below are the fixed-basis EDB inventory. “Unrated” is retained explicitly. Capture links point to the latest lesson providing position evidence.', '',
    '| KP | Position | E | M | H | Unrated | Likely unavailable | Captured tasks |','|---|---:|---:|---:|---:|---:|---|---:|']
    candidates=[r for r in rows if r['rated_questions']>=20 and r['missing_levels']]
    for r in sorted(candidates,key=lambda r:(-r['rated_questions'],r['title'])):
     pos=r['latest_position'];position=f"{pos['position']}/{pos['lesson_kps']}" if pos else '?'
     title=f"[{r['title']}]({pos['source_file']})" if pos else r['title'];c=r['counts']
     lines.append(f"| {title} (`{r['example_id']}`) | {position} | {c['easy']} | {c['moderate']} | {c['hard']} | {r['unknown_questions']} | {', '.join(r['missing_levels'])} | {r['distinct_capture_tasks']} |")
    lines+=['', 'Every listed KP has position evidence and multiple captured tasks. The most decisive matched example is the two-KP lesson with **Solving a 2x2 System of Equations Using an Inverse Matrix** first (27 easy, no moderate or hard), followed by **…With Reorganization** (9 moderate, 13 hard, no easy). Hard and easy questions both occur within its captured lessons, in different KPs.', '',
    '### Capture evidence that overturns a database zero', '',
    'Captures demonstrate an easy option for **15** database-zero KPs, a moderate option for **16**, and a hard option for **6**. These counts can overlap. None belongs to the 20-question restricted-KP list. Across all KPs, **139 captured question–KP pairs are absent from the corresponding fixed-basis database pool**. These are collection/import or snapshot gaps, rather than evidence that a difficulty option cannot exist. No matched question had conflicting captured difficulty labels.', '',
    *candidate_absence_section(root),
    *missing_level_pilot_section(),
    '## Account and selection effects', '',
    'The question catalog is shared content, so its availability evidence can combine distinct question identities collected across accounts. Learner progress is not merged. Selection distributions below are calculated separately for each account, with the legacy archive kept explicitly unlabelled.', '',
    'The first two distinct lesson questions per KP reduce the influence of later remediation. They still represent selected practice, rather than a uniform sample of a question bank. A separate order audit checked 1,284 identified current-capture KP sample pointers, all matching captured question order.', '',
    '| Account | First-position questions | First-position hard | Third-position questions | Third-position hard |','|---|---:|---:|---:|---:|']
    cells={tuple(r['group']):r for r in p['first_two_lesson_questions_by_account_and_position']}
    for account in ('differential','foundations','linear','multivariable','legacy-unlabelled'):
     a,b=cells[(account,1)],cells[(account,3)];lines.append(f"| {account} | {a['question_occurrences']} | {a['percent']['hard']:.1f}% | {b['question_occurrences']} | {b['percent']['hard']:.1f}% |")
    lines+=['', 'The direction appears separately in every current account and the legacy archive. Linear has a weaker first-to-third change, which is a useful reminder that subject matter affects the repertoire. The detailed evidence also retains distributions separately for lessons, reviews, assessments and diagnostics; those activity types have different selection behavior.', '',
    '## Engine implications', '',
    'Use **per-KP available levels** when selecting questions. Position is a fallback prior for under-collected KPs; it should not declare a level impossible. Keep inferred unavailability distinct from the levels currently present in our database, so a newly scraped hard question can immediately overturn a no-hard estimate.', '',
    'The current selector already renormalizes policy weights over nonempty eligible rated bands in [question_selection.rs](engine/rust/question_selection.rs:173). With initial weights 45/40/15, an easy/moderate-only pool uses **52.94% easy and 47.06% moderate**; a moderate-only pool uses **100% moderate**. That behavior fits this evidence. Aggregate proportions by position cannot directly identify the underlying global policy weights.', '',
    'Topic workload calibration currently applies one global expected difficulty distribution to all KPs. These findings identify a possible refinement: calculate each KP’s expected workload from its effective available-band weights before fitting the topic multiplier. Existing topic multipliers already absorb some of those repertoire differences. Changing that expectation would require recalculating multipliers to preserve captured lesson denominators; this analysis does not change the current calibration or policy.', '',
    '## Evidence and reproduction', '',
    '- [Full KP inventory, counts, classifications and capture links](reference/mathacademy/kp-difficulty-analysis-2026-10-12/kp-inventory.json)',
    '- [Missing-level candidates with at least 10 rated questions](reference/mathacademy/kp-difficulty-analysis-2026-10-12/missing-level-candidates.json)',
    '- [Position comparisons, account distributions and bootstrap results](reference/mathacademy/kp-difficulty-analysis-2026-10-12/position-comparisons.json)',
    '- [Fixed-basis EDB pool inventory](reference/mathacademy/kp-difficulty-analysis-2026-10-12/database/pool-inventory.json)',
    '- [KP-linked captured question occurrences](reference/mathacademy/kp-difficulty-analysis-2026-10-12/capture-occurrences.json)',
    '- [Analysis script](capture/scripts/analyze_kp_difficulty.py), [position-comparison script](capture/scripts/analyze_kp_position.py), and [report/figure generator](capture/scripts/write_kp_difficulty_report.py)', '',
    'The EDB export uses explicit Pull patterns in bounded 40-KP batches, with `--as-of 1522` on every read. The saved query and input files preserve those requests. Difficulty provenance is checked independently against `:org/Math-Academy`. Capture KP identity uses the canonical example ID or the stable database KP UUID, never a title-only match.', '',
    'Rerun the analysis against the frozen database export and capture projections:', '',
    '```bash\npython3 capture/scripts/analyze_kp_difficulty.py analyze\n/home/jake/Developer/MA/.venv/bin/python capture/scripts/analyze_kp_position.py\n```','',
    'Running `collect` replaces capture projections with a fresh local snapshot. A new analysis of live data should also export a fresh EDB basis. Do not combine new capture counts with an old database snapshot without explicitly recording that difference.', '']
    (root/'kp-difficulty-report.md').write_text('\n'.join(lines))
    print('Wrote kp-difficulty-report.md and distribution figures; candidates:',len(candidates))


if __name__ == "__main__":
    main()
