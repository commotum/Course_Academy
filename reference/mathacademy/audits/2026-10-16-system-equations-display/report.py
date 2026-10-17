"""Build a reviewable read-only source investigation report."""
import html
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
def read(path):return json.loads((HERE/path).read_text())
e=html.escape
scope=read('content/scope.json')
wide=read('wide-mth341/summary.json')
tutorials=read('source/tutorial-findings.json')
summary={
 'database':read('snapshot.json'),'database_writes':0,'production_code_changes':0,
 'primary_question':17592186529306,'origin':'locally_generated',
 'primary_question_insert_basis':2487,'primary_question_insert_utc':'2026-10-14T23:19:00.037Z',
 'original_source_layout_is_correct':True,
 'root_causes':['Old MathML extraction replaced equation-table rows with semicolons and cell boundaries with bars.',
                'Local generators retained the flattened layout and duplicated operation bars.',
                'The shared normalizer recognizes a literal opening brace but skips the escaped opening brace used by these generators.',
                'Prior checks validated TeX syntax without requiring multirow system structure.'],
 'full_content_audit':read('content/summary.json'),
 'targeted_broader_question_scan':wide,
 'additional_candidate_rendering':read('ui/wide/all-fields-summary.json'),
 'additional_source_verification':read('source/wider-findings.json'),
 'confirmed_affected_question_fields':wide['affected_fields'],
 'confirmed_affected_questions':wide['affected_questions'],
 'additional_tutorial_fields':len(tutorials),
 'total_confirmed_affected_fields':wide['affected_fields']+len(tutorials),
 'ui_changes_required_for_canonical_layout':False,
 'scope_limits':'Four named topics: all captured learner display fields rendered. Broader 42 targets: question prompts and existing worked solutions scanned for these signatures; not a full audit of every other tutorial.',
 'proposed_repairs':['Restore proper multirow systems in affected stored question fields, retaining equation-label and operation columns.',
                     'Remove only source-confirmed duplicate operation bars.',
                     'Correct the eight affected generator templates and their stale source snapshots.',
                     'Extend conservative normalization and semantic layout checks to escaped-brace systems.',
                     'Restore source display blocks and numbered/nested lists in the two tutorials.']}
(HERE/'verification.json').write_text(json.dumps(summary,indent=2)+'\n')
rows=[]
for t in scope:
 finding={17592186050240:'15 questions with flat prompts/solutions; 30 solutions with duplicated operation bars.',
          17592186048343:'No flat-system defect; one tutorial lost display-math blocks.',
          17592186048853:'No confirmed formatting defect found.',
          17592186049058:'No flat-system defect; one tutorial lost list numbering and nesting.'}[t['topic']]
 rows.append(f'<tr><td>{t["topic"]}<br>{e(t["title"])}</td><td>{t["kps"]}</td><td>{t["questions"]}</td><td>{t["tutorials"]}</td><td>{t["fields"]}</td><td>{finding}</td></tr>')
wide_rows=''.join(f'<tr><td>{t["topic"]}<br>{e(t["title"])}</td><td>{t["affected_questions"]}</td><td>{t["affected_fields"]}</td></tr>' for t in wide['affected_topics'])
tutorial_text=''.join(f'<li><code>{t["entity"]}</code>: {e(t["finding"])} <a href="source/tutorial-{t["entity"]}-original.png">Original screenshot</a><p>{e(t["boundary"])}</p></li>' for t in tutorials)
doc='''<!doctype html><meta charset="utf-8"><title>System equation display investigation</title>
<style>body{font:16px/1.5 system-ui,sans-serif;max-width:1180px;margin:32px auto;padding:0 24px;color:#17202a}h1{line-height:1.2}table{border-collapse:collapse;width:100%;margin:20px 0}td,th{border:1px solid #ccd3d9;padding:10px;text-align:left;vertical-align:top}th{background:#edf2f7}code,pre{background:#f4f6f8;padding:3px}pre{white-space:pre-wrap;padding:14px}a{color:#1363a8}.note{border-left:4px solid #567;padding:8px 16px;background:#f3f6f8}</style>
<h1>System equation display investigation</h1>
<p>The source Math Academy systems are correctly stacked. The malformed layout was introduced by an old extraction pipeline, copied into local generators, and missed by a normalization rule that handles <code>{</code> but not <code>\\{</code>. The current UI renders correctly when supplied structured LaTeX.</p>
<p class="note">Read-only investigation at database basis 3187. No database, generator, capture-worker, or UI code changes.</p>
<h2>The reported question</h2>
<p><code>17592186529306</code> is a locally generated question in KP <code>17592186073776</code>. Its malformed prompt was inserted unchanged at basis 2487, 2026-10-14 23:19:00.037 UTC, by <code>:application/ca-engine</code>.</p>
<pre>Stored: $\\{-3x - y = 8; 3x + y = -6$
Canonical: \\left\\{\\begin{aligned}-3x-y &amp;=8 \\\\ 3x+y &amp;=-6\\end{aligned}\\right.</pre>
<p><a href="ui/actual-ui/question-001.png">Actual UI: stored content</a> · <a href="ui/actual-ui/question-002.png">Same UI: canonical system preview</a> · <a href="source/source-practice-question.png">Original Math Academy system</a></p>
<h2>Confirmed source chain</h2><ol>
<li>Original HTML/MathML contains separate table rows, display blocks, and one operation bar.</li>
<li>The old <code>lesson-json.py</code> joins table rows with semicolons and cells with a bar; this destroys row structure and duplicates existing operation bars.</li>
<li>Local generators copy semicolon joins and escape the opening brace, treating that as a formatting repair.</li>
<li><code>legacy_choice()</code> only recognizes a literal opening brace; the escaped-brace variant passes through unchanged.</li>
<li>This remains syntactically valid math. Prior render checks found no parser error but did not require a system to contain multiple rows.</li></ol>
<p><a href="source/verification.json">Source evidence and exact code locations</a> · <a href="history.json">Reported question history</a> · <a href="ui/all-fields-rendering.json">Full renderer evidence</a></p>
<h2>Full audit of the four requested lessons</h2>
<p>10 KPs, 128 practice questions, 10 canonical examples, 12 tutorials, and 838 display fields. All fields were rendered through the application's Markdown renderer and MathJax. There were no parser errors, raw-TeX leftovers, undefined commands, or unintended code blocks.</p>
<table><tr><th>Lesson</th><th>KPs</th><th>Questions/examples</th><th>Tutorials</th><th>Fields</th><th>Findings</th></tr>'''+''.join(rows)+'''</table>
<h2>Broader target-topic check</h2>
<p>A targeted scan covered 42 current MTH 341 target topics, 126 KPs, 1,854 question/example entities, and 3,604 prompt/solution fields. It found 175 affected fields on 108 questions. This wider scan checks the identified system/bar signatures; it is not a complete render audit of all other lesson tutorials.</p>
<table><tr><th>Lesson</th><th>Affected questions</th><th>Affected prompt/solution fields</th></tr>'''+wide_rows+'''</table>
<p>All 130 additional candidate fields were also rendered: each contains a flat system with missing table rows despite passing MathJax syntax checks. All 130 exactly match retained generated payloads, confirming local generation. Substitution equation labels such as (1) and (2) also lost their original spacing and appear glued to equation values; they must be restored as labels, not multiplication.</p>
<p><a href="wide-mth341/findings.json">Exact affected question IDs and fields</a> · <a href="wide-mth341/summary.json">Broader scope and counts</a> · <a href="ui/wide/all-fields-summary.json">Additional candidate render verification</a> · <a href="source/wider-findings.json">Additional source verification</a></p>
<h2>Separate tutorial Markdown defects</h2><ul>'''+tutorial_text+'''</ul>
<p><a href="source/tutorial-findings.json">Tutorial source comparison</a></p>
<h2>Repair scope</h2><p>177 confirmed fields in total: 175 question fields and two tutorial fields. Restore equation rows and annotation/label columns; remove source-confirmed duplicate operation bars; restore display blocks and numbered/nested lists. Update the affected generators and normalizer so generated replacements retain the corrected structure. No UI change is needed to render the canonical format.</p>
<p><a href="verification.json">Machine-readable verification</a></p>'''
(HERE/'report.html').write_text(doc)
print(json.dumps({'report':'report.html','affected_questions':wide['affected_questions'],'affected_fields_including_tutorials':summary['total_confirmed_affected_fields']}))
