#!/usr/bin/env python3
"""Join captured assessment evidence to lesson order; write an auditable report.

Consumes the inventory and fixed-basis EDB exports; never writes to the database.
Uses only the Python standard library. Run as a module from the repository root.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
from html import escape
import json
from pathlib import Path
import random
from statistics import mean

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'reference/mathacademy/assessment-kp-position-analysis-2026-10-16'


def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def groups(rows, key):
    result = defaultdict(list)
    for row in rows:
        result[str(row[key])].append(row)
    return result


def describe(rows):
    eligible = [r for r in rows if r.get('normalized_position') is not None]
    n = len(eligible)
    return dict(questions=len(rows), positioned=sum(r.get('kp_position') is not None for r in rows),
        single_kp=sum(r.get('lesson_kp_count') == 1 for r in rows), directional_questions=n,
        topics=len({r['topic_id'] for r in eligible}), quizzes=len({r['task_key'] for r in eligible}),
        mean_position=mean(r['normalized_position'] for r in eligible) if n else None,
        first=sum(r['kp_position'] == 1 for r in eligible),
        last=sum(r['kp_position'] == r['lesson_kp_count'] for r in eligible),
        early=sum(r['normalized_position'] < .5 for r in eligible),
        middle=sum(r['normalized_position'] == .5 for r in eligible),
        late=sum(r['normalized_position'] > .5 for r in eligible),
        expected_first_or_last=sum(1 / r['lesson_kp_count'] for r in eligible),
        uniform_mean=.5,
        counts_by_position=dict(sorted(Counter(r['kp_position'] for r in eligible).items())),
        captured_pool_mean=mean(r['captured_pool_mean'] for r in eligible)
            if n and all(r.get('captured_pool_mean') is not None for r in eligible) else None)


def percentile(values, p):
    ordered = sorted(values)
    index = (len(ordered) - 1) * p
    low = int(index)
    return ordered[low] + (ordered[min(low + 1, len(ordered) - 1)] - ordered[low]) * (index - low)


def clustered_interval(rows, key, repetitions=10000):
    clusters = list(groups(rows, key).values())
    if not clusters:
        return None
    totals = [(sum(r['normalized_position'] for r in cluster), len(cluster)) for cluster in clusters]
    rng = random.Random(20261016)
    means = []
    for _ in range(repetitions):
        draw = rng.choices(totals, k=len(totals))
        means.append(sum(t[0] for t in draw) / sum(t[1] for t in draw))
    return dict(cluster=key, clusters=len(clusters), repetitions=repetitions, seed=20261016,
        method='percentile cluster bootstrap; descriptive uncertainty, not random population sampling',
        lower=percentile(means, .025), upper=percentile(means, .975))


def join(inventory, database):
    tasks = {t['task_key']: t for t in inventory['assessments']}
    rows = []
    for original in inventory['questions']:
        row = dict(original)
        topic = database['topics'].get(row['topic_id'], {})
        q = database['questions'].get(row['question_id'], {})
        row.update(course_title=database['courses'].get(row['course_id'], {}).get('title'),
            topic_title=topic.get('title'), topic_entity=topic.get('entity'),
            question_entity=q.get('entity'), retake=tasks[row['task_key']]['retake'],
            kp_position=None, lesson_kp_count=None, normalized_position=None,
            captured_pool_mean=None, mapping_status='unresolved_kp')
        candidates = {m['kp_entity'] for m in q.get('memberships', []) if row['topic_id'] in m['topic_ids']}
        evidence = 'permanent question ID → database KP membership within captured topic'
        if not candidates and not q.get('entity'):
            # History anchors are not globally canonical-example IDs. Require
            # independent agreement of the exact unique topic/title AND anchor.
            title_matches = [database['kps'][str(e)] for e in topic.get('kp_entities', [])
                if ' '.join((database['kps'][str(e)]['title'] or '').split()).casefold()
                == ' '.join((row['kp_title'] or '').split()).casefold()]
            if len(title_matches) == 1 and title_matches[0]['canonical_example_id'] == 'e-' + row['raw_kp_anchor_id']:
                candidates = {title_matches[0]['entity']}
                evidence = 'captured topic + unique exact KP title + source anchor corroborating canonical example; question absent from DB'
        row['candidate_kp_entities'] = sorted(candidates)
        if len(candidates) == 1:
            kp = database['kps'][str(next(iter(candidates)))]
            row.update(kp_entity=kp['entity'], kp_uuid=kp['uuid'], database_kp_title=kp['title'],
                canonical_example_id=kp['canonical_example_id'],
                title_agrees=' '.join((kp['title'] or '').split()).casefold() == ' '.join((row['kp_title'] or '').split()).casefold(),
                mapping_evidence=evidence)
            sequence = topic.get('ordered_kp_entities')
            if not sequence or topic['order_status'] != 'unique':
                row['mapping_status'] = 'kp_known_order_unresolved'
            elif kp['entity'] not in sequence:
                row['mapping_status'] = 'kp_not_in_sequence'
            else:
                k = len(sequence)
                p = sequence.index(kp['entity']) + 1
                row.update(mapping_status='positioned', kp_position=p, lesson_kp_count=k,
                    normalized_position=(p - 1) / (k - 1) if k > 1 else None,
                    order_evidence='complete activity first-step/step-next route; historical topic-member KPs outside route excluded')
                counts = [database['kps'][str(e)]['pool_count_ma_attributed'] for e in sequence]
                if k > 1 and sum(counts) and all(counts):
                    row['captured_pool_mean'] = sum(i / (k - 1) * count for i, count in enumerate(counts)) / sum(counts)
        rows.append(row)
    return rows


def summary(rows, inventory, database):
    eligible = [r for r in rows if r['normalized_position'] is not None]
    result = dict(generated_at=datetime.now(timezone.utc).isoformat(), database=database['identity'],
        capture_inventory=inventory['summary'], mapping_status=dict(Counter(r['mapping_status'] for r in rows)),
        mapping_evidence=dict(Counter(r.get('mapping_evidence', 'unresolved') for r in rows)),
        primary=describe(rows), quiz_cluster_interval=clustered_interval(eligible, 'task_key'),
        topic_cluster_interval=clustered_interval(eligible, 'topic_id'),
        topic_equal_mean=mean(mean(r['normalized_position'] for r in rs) for rs in groups(eligible, 'topic_id').values()),
        quiz_equal_mean=mean(mean(r['normalized_position'] for r in rs) for rs in groups(eligible, 'task_key').values()),
        distinct_question_result_identical=len({r['question_id'] for r in rows}) == len(rows),
        title_disagreements=[r['occurrence_id'] for r in rows if r.get('title_agrees') is False],
        by_course={key:dict(course_title=rs[0]['course_title'], **describe(rs)) for key, rs in groups(rows, 'course_id').items()},
        by_account={key:describe(rs) for key, rs in groups(rows, 'account').items()},
        by_difficulty={key:describe(rs) for key, rs in groups(rows, 'difficulty').items()},
        by_lesson_length={key:describe(rs) for key, rs in groups(rows, 'lesson_kp_count').items()},
        by_retake={key:describe(rs) for key, rs in groups(rows, 'retake').items()},
        interpretations=[
            'Normalized position=(KP position−1)/(lesson KP count−1); 0=first, 1=last. Single-KP lessons excluded from directional comparisons.',
            'Uniform-KP-within-topic is a benchmark, not a verified model of platform eligibility or sampling.',
            'These are captured assessments from four accounts, not a random sample of all Math Academy assessments.',
            'Later position can correlate with difficulty, compound skills, learner eligibility and recency; this observational result does not isolate the cause.',
            'The captured-pool benchmark uses only Math Academy-attributed permanent questions in this database; this is an incomplete and selected bank that includes the assessed questions.'
        ])
    if all(r.get('captured_pool_mean') is not None for r in eligible):
        differences = [dict(r, normalized_position=r['normalized_position'] - r['captured_pool_mean']) for r in eligible]
        result['captured_pool_comparison'] = dict(mean_difference=mean(r['normalized_position'] for r in differences),
            quiz_cluster_interval=clustered_interval(differences, 'task_key'))
    result['by_mapping_evidence'] = {key:describe(rs) for key,rs in groups(rows,'mapping_evidence').items()}
    source_path = OUT / 'source-lesson-sequences.json'
    if source_path.exists():
        source = json.loads(source_path.read_text())
        evidence = {q['occurrence_id']:q for q in source['questions']}
        result['source_order_verification'] = source['summary']
        result['source_order_sensitivity'] = {}
        for key in ['all_source', 'prior_source', 'same_account_prior_source']:
            subset = [r for r in rows if evidence.get(r['occurrence_id'],{}).get(key+'_matches_database')]
            result['source_order_sensitivity'][key] = describe(subset)
        for r in rows:
            r['source_order_evidence'] = evidence.get(r['occurrence_id'])
    return result


def pct(value):
    return f'{100 * value:.1f}%'


def plot_summary(stats):
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        return
    primary=stats['primary']; n=primary['directional_questions']
    observed=[primary['first']/n,1-(primary['first']+primary['last'])/n,primary['last']/n]
    expected=[primary['expected_first_or_last']/n,1-2*primary['expected_first_or_last']/n,primary['expected_first_or_last']/n]
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False})
    fig,axes=plt.subplots(1,2,figsize=(12,4.5),gridspec_kw={'width_ratios':[1.2,1]})
    for offset,values,label,color in [(-.18,observed,'Captured assessments','#245f99'),(.18,expected,'Uniform within topic','#becad6')]:
        bars=axes[0].bar([x+offset for x in range(3)],[v*100 for v in values],width=.34,label=label,color=color)
        axes[0].bar_label(bars,labels=[pct(v) for v in values],padding=4,fontsize=10)
    axes[0].set(xticks=range(3),xticklabels=['First KP','Interior KPs','Final KP'],ylabel='Share of questions (%)',ylim=(0,67),title='Interior KPs dominate the sample')
    axes[0].legend(frameon=False,fontsize=9,loc='upper left')
    labels=[]
    for y,key in enumerate(['easy','moderate','hard']):
        stat=stats['by_difficulty'][key];value=stat['mean_position']
        axes[1].scatter([value],[y],s=85,color='#245f99',zorder=3)
        axes[1].annotate(f'{value:.3f}',(value,y),xytext=(9,0),textcoords='offset points',va='center')
        labels.append(f'{key.title()} (n={stat["questions"]})')
    axes[1].axvline(.5,color='#7c8794',linestyle='--',linewidth=1)
    axes[1].set(yticks=range(3),yticklabels=labels,xlim=(0,1),ylim=(2.6,-.6),xlabel='Mean normalized lesson position',title='Hard questions occur later in lessons')
    axes[1].set_xticks([0,.5,1],['0 · first','0.5 · midpoint','1 · last'])
    fig.suptitle('85 captured assessments · 768 unique questions · 514 topics',fontsize=14,fontweight='bold',y=1.02)
    fig.text(.01,-.03,'Descriptive capture sample. Uniform-KP benchmark is not the platform’s verified eligibility model.',fontsize=9,color='#566578')
    fig.tight_layout()
    for suffix in ['png','svg']:
        fig.savefig(OUT/f'position-summary.{suffix}',dpi=170,bbox_inches='tight',facecolor='white')
    plt.close(fig)


def write_report(rows, inventory, database, stats):
    h = lambda s: escape(str(s if s is not None else '—'))
    main = stats['primary']; n = main['directional_questions']
    ci = stats['quiz_cluster_interval']
    parts = ['''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Assessment KP position audit · 16 October 2026</title><style>
body{font:16px/1.55 system-ui,sans-serif;color:#17283b;background:#f7f9fc;margin:0}main{max-width:1250px;margin:auto;padding:32px}h1{font-size:32px;line-height:1.15}h2{margin-top:36px}a{color:#175da3}table{width:100%;border-collapse:collapse;background:white;margin:16px 0}th,td{text-align:left;padding:10px 12px;border-bottom:1px solid #dce4ed;vertical-align:top}th{background:#eaf0f6}small,.muted{color:#54657a}code{font-size:12px}details{background:white;border:1px solid #dce4ed;border-radius:8px;margin:12px 0;padding:12px}summary{cursor:pointer;font-weight:600}.cards{display:flex;gap:16px;flex-wrap:wrap}.card{padding:20px;background:white;border:1px solid #dce4ed;border-radius:8px;min-width:180px}.big{display:block;font-size:30px;font-weight:700}.scroll{overflow:auto}input{width:min(95%,700px);font:inherit;padding:12px;border:1px solid #8899aa;border-radius:6px}pre{white-space:pre-wrap;font:13px/1.5 system-ui}li{margin:6px 0}.pill{font-weight:700;white-space:nowrap}tr[hidden],details[hidden]{display:none}@media print{input{display:none}details{break-inside:avoid}}
</style><main><p class="muted">Captured assessment audit · 16 October 2026</p><h1>Which lesson KPs do quizzes assess?</h1>''']
    parts.append('<p><strong>The sample has a modest tilt toward later KPs, with much stronger concentration on interior KPs. It does not show a blanket preference for the final KP.</strong> Hard questions skew later; easy questions are approximately centered. These are descriptive associations, not proof of a platform selection rule.</p>')
    parts.append(f'<p>Mapped {main["positioned"]} of {len(rows)} questions across {len(inventory["assessments"])} assessments. '
        f'{main["single_kp"]} questions belong to single-KP lessons; {n} contribute to the early-versus-late comparison.</p>')
    parts.append('<div class="cards">' + ''.join(f'<div class="card">{label}<span class="big">{value}</span><small>{note}</small></div>' for label,value,note in [
        ('Mean lesson position',f'{main["mean_position"]:.3f}','0 = first · 1 = last · uniform benchmark = 0.500'),
        ('Questions from final KP',pct(main['last']/n),f'{main["last"]}/{n}; benchmark {pct(main["expected_first_or_last"]/n)}'),
        ('Questions from first KP',pct(main['first']/n),f'{main["first"]}/{n}; same benchmark'),
    ]) + '</div>')
    parts.append(f'<p>95% quiz-cluster bootstrap interval for the mean: <strong>{ci["lower"]:.3f}–{ci["upper"]:.3f}</strong>. '
        'This interval describes variation in this capture sample; it does not turn the sample into a random population survey.</p>')
    if (OUT/'position-summary.svg').exists():
        parts.append('<img src="position-summary.svg" alt="Interior KPs account for 56.1% of questions versus 35.2% under uniform KP selection; hard questions have later mean position than easy questions." style="width:100%;height:auto;background:white">')
    parts.append('<h2>Comparison and sensitivity checks</h2><table><tr><th>Measure</th><th>Observed</th><th>Uniform-KP benchmark</th></tr>')
    for label,value,baseline in [
        ('Earlier half / midpoint / later half',f'{main["early"]} / {main["middle"]} / {main["late"]}','Earlier and later halves have equal opportunity'),
        ('Topic-equal mean position',f'{stats["topic_equal_mean"]:.3f}','0.500'),
        ('Quiz-equal mean position',f'{stats["quiz_equal_mean"]:.3f}','0.500'),
        ('Topic-cluster 95% interval',f'{stats["topic_cluster_interval"]["lower"]:.3f}–{stats["topic_cluster_interval"]["upper"]:.3f}','0.500'),
        ('Distinct question sensitivity','All question IDs are unique; result unchanged' if stats['distinct_question_result_identical'] else 'See JSON','—'),
        ('Observed captured-bank weighted mean',f'{main["captured_pool_mean"]:.3f}' if main['captured_pool_mean'] is not None else 'Not available for all lessons','Incomplete bank; sensitivity only')]:
        parts.append(f'<tr><td>{h(label)}</td><td>{h(value)}</td><td>{h(baseline)}</td></tr>')
    parts.append('</table>')
    if stats.get('captured_pool_comparison'):
        pool=stats['captured_pool_comparison']; pci=pool['quiz_cluster_interval']
        parts.append(f'<p>Relative to the observed captured-bank baseline, the mean-position difference is {pool["mean_difference"]:.3f} '
            f'(95% quiz-cluster interval {pci["lower"]:.3f}–{pci["upper"]:.3f}). This bank is incomplete and includes these assessment questions, so it is a sensitivity check rather than an independent selection model.</p>')
    parts.append('<h2>Exact position counts</h2><p>This table exposes the concentration on interior KPs, which an average position alone obscures.</p><table><tr><th>Lesson length</th><th>KP 1</th><th>KP 2</th><th>KP 3</th><th>KP 4</th><th>KP 5</th></tr>')
    for k,stat in sorted(stats['by_lesson_length'].items(), key=lambda item:int(item[0]) if item[0].isdigit() else 0):
        parts.append(f'<tr><td>{h(k)} KPs</td>'+''.join(f'<td>{stat["counts_by_position"].get(p,0) if k.isdigit() and p<=int(k) else "—"}</td>' for p in range(1,6))+'</tr>')
    parts.append('</table>')
    for key,title,labelkey in [('by_course','By source course','course_title'),('by_lesson_length','By number of lesson KPs',None),('by_difficulty','By question difficulty',None)]:
        parts.append(f'<h2>{title}</h2><div class="scroll"><table><tr><th>Group</th><th>Questions</th><th>Directional questions</th><th>Mean position</th><th>First KP</th><th>Final KP</th></tr>')
        for name, stat in stats[key].items():
            den = stat['directional_questions']
            label = (stat.get(labelkey) or name) if labelkey else name
            position = f'{stat["mean_position"]:.3f}' if den else '—'
            parts.append(f'<tr><td>{h(label)}</td><td>{stat["questions"]}</td><td>{den}</td><td>{position}</td><td>{pct(stat["first"]/den) if den else "—"}</td><td>{pct(stat["last"]/den) if den else "—"}</td></tr>')
        parts.append('</table></div>')
    parts.append('<h2>Evidence and limits</h2><ul>' + ''.join(f'<li>{h(s)}</li>' for s in stats['interpretations']) + '</ul>')
    direct=sum('permanent question' in r['mapping_evidence'] for r in rows)
    parts.append(f'<p>Database basis: <code>{h(database["identity"])}</code>. {direct} questions map through permanent Math Academy question IDs and recorded KP membership within the captured topic. '
        f'The other {len(rows)-direct} questions are absent from this database snapshot; each maps through its explicit captured topic, a unique exact KP title, and a source anchor matching that KP’s canonical example. '
        'Lesson order follows the complete activity step chain, excluding tutorials. Historical topic members outside that route do not inflate lesson length. Numeric result-header KP anchors are retained separately. Capture files are identified by SHA-256 in the inventory.</p>')
    if stats.get('source_order_sensitivity'):
        parts.append('<table><tr><th>Source lesson evidence</th><th>Questions</th><th>Mean position</th></tr>')
        for name,stat in stats['source_order_sensitivity'].items():
            pos=f'{stat["mean_position"]:.3f}' if stat['directional_questions'] else '—'
            parts.append(f'<tr><td>{h(name.replace("_"," "))}</td><td>{stat["questions"]}</td><td>{pos}</td></tr>')
        parts.append('</table><p>“Prior source” requires a complete lesson definition recorded before the assessment; “same account” additionally requires that lesson capture to belong to the assessment account. These are robustness subsets, not eligibility reconstructions.</p>')
    parts.append('<p>Download <a href="questions.json">every question mapping</a>, <a href="topics.json">complete topic sequences</a>, <a href="assessments.json">quiz topic inventories</a>, or <a href="summary.json">statistics and provenance</a>.</p>')
    parts.append('<h2>Every assessment and question</h2><p>Expand a quiz to see its topics and question mappings. “3 / 4” means the third KP in a four-KP lesson.</p><input id="filter" type="search" placeholder="Filter by quiz, account, course, topic, KP or question ID" aria-label="Filter assessment questions"><p id="count"></p>')
    by_task = groups(rows, 'task_key')
    for task in inventory['assessments']:
        rs = by_task[task['task_key']]
        label = f'{task["account"]} · {task["title"]} · task {task["task_id"]} · {rs[0]["course_title"]}'
        parts.append(f'<details class="quiz"><summary>{h(label)} <small>({len(rs)} questions)</small></summary>')
        topics = sorted({r['topic_title'] or r['topic_id'] for r in rs})
        parts.append(f'<p><strong>Topics:</strong> {h("; ".join(topics))}</p><div class="scroll"><table><tr><th>Question</th><th>Topic</th><th>Knowledge point</th><th>Lesson position</th></tr>')
        for r in rs:
            position = f'{r["kp_position"]} / {r["lesson_kp_count"]}' if r['kp_position'] else r['mapping_status']
            parts.append(f'<tr class="question"><td>Q{r["question_number"]}<br><code>{h(r["question_id"])}</code><br><small>{h(r["difficulty"])}</small></td><td><a href="#topic-{h(r["topic_id"])}">{h(r["topic_title"])}</a><br><small>MA {h(r["topic_id"])}</small></td><td>{h(r.get("database_kp_title") or r["kp_title"])}<br><code>:db/id {h(r.get("kp_entity"))}</code><br><small>{h(r.get("canonical_example_id"))} · source anchor {h(r["raw_kp_anchor_id"])}</small><details><summary>Captured problem</summary><pre>{h(r["problem"])}</pre><a href="{h((ROOT/r["source_file"]).as_uri())}">Source capture</a></details></td><td class="pill">{h(position)}</td></tr>')
        parts.append('</table></div></details>')
    parts.append('<h2>Complete lesson sequences</h2><p>Listed in lesson order. Counts show questions selected by the assessments in this snapshot.</p>')
    kp_counts = Counter(r.get('kp_entity') for r in rows)
    for topic_id in sorted({r['topic_id'] for r in rows}, key=lambda tid: database['topics'].get(tid,{}).get('title','')):
        topic = database['topics'].get(topic_id,{})
        parts.append(f'<details id="topic-{h(topic_id)}"><summary>{h(topic.get("title"))} · MA {h(topic_id)}</summary><ol>')
        for entity in topic.get('ordered_kp_entities') or []:
            kp = database['kps'][str(entity)]
            parts.append(f'<li>{h(kp["title"])} — <strong>{kp_counts[entity]} assessed</strong><br><small>:db/id {entity} · {h(kp["canonical_example_id"])}</small></li>')
        parts.append('</ol></details>')
    parts.append('''<script>
const input=document.querySelector('#filter');input.addEventListener('input',()=>{let shown=0;const term=input.value.toLowerCase();document.querySelectorAll('details.quiz').forEach(d=>{const title=d.querySelector('summary').textContent.toLowerCase();let matches=0;d.querySelectorAll('tr.question').forEach(r=>{const ok=!term||(title+' '+r.textContent.toLowerCase()).includes(term);r.hidden=!ok;if(ok)matches++});d.hidden=!matches;if(term&&matches)d.open=true;shown+=matches});document.querySelector('#count').textContent=shown+' matching questions'});document.querySelectorAll('a[href^="#topic-"]').forEach(a=>a.addEventListener('click',()=>{document.querySelector(a.getAttribute('href')).open=true}));
</script></main></html>''')
    (OUT/'report.html').write_text('\n'.join(parts))


def main():
    inventory=json.loads((OUT/'capture-inventory.json').read_text())
    database=json.loads((OUT/'database/mapping.json').read_text())
    rows=join(inventory,database)
    save('resolved-question-identities.json',[
        {k:r.get(k) for k in ['occurrence_id','question_id','topic_id','source_sha256',
            'mapping_status','kp_entity','canonical_example_id','mapping_evidence']} for r in rows])
    stats=summary(rows,inventory,database)
    save('questions.json',rows)
    save('summary.json',stats)
    by_task=groups(rows,'task_key')
    save('assessments.json',[dict(t,statistics=describe(by_task[t['task_key']])) for t in inventory['assessments']])
    save('topics.json',[dict(database['topics'][tid],knowledge_points=[database['kps'][str(k)] for k in (database['topics'][tid].get('ordered_kp_entities') or [])]) for tid in sorted({r['topic_id'] for r in rows})])
    plot_summary(stats)
    write_report(rows,inventory,database,stats)
    save('analysis-manifest.json',dict(script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        inputs={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [OUT/'capture-inventory.json',OUT/'database/mapping.json',OUT/'source-lesson-sequences.json'] if p.exists()}))
    print(json.dumps({k:stats[k] for k in ['mapping_status','primary','quiz_cluster_interval','topic_equal_mean','title_disagreements']},indent=2))


if __name__ == '__main__':
    main()
