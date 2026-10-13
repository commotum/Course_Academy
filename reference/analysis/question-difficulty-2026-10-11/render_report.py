from pathlib import Path
import json,html,os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
OUT=Path(__file__).resolve().parent
s=json.loads((OUT/'summary.json').read_text());avail=json.loads((OUT/'availability-illustration.json').read_text())
B=['easy','moderate','hard']; colors=['#398b82','#4268b2','#ae5279']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False})
fig,(ax1,ax2)=plt.subplots(1,2,figsize=(14,7),gridspec_kw={'width_ratios':[1,1.22]})
types=['lesson','review','assessment','multistep','diagnostic'];ys=np.arange(len(types));left=np.zeros(len(types))
for b,c in zip(B,colors):
 vals=np.array([s['unique_by_source_type'][t]['percent'][b] for t in types]);ax1.barh(ys,vals,left=left,color=c,label=b.title())
 for y,v,l in zip(ys,vals,left):
  if v>=8:ax1.text(l+v/2,y,f'{v:.1f}%',ha='center',va='center',color='white',fontsize=10)
 left+=vals
ax1.set_yticks(ys,[f"{t.title()}\n{s['unique_by_source_type'][t]['n']:,} unique" for t in types]);ax1.invert_yaxis();ax1.set_xlim(0,100);ax1.set_xlabel('Percent of unique questions seen in each activity type');ax1.set_title('Rated questions by captured source',loc='left',fontweight='bold',pad=18)
labels=[];valrows=[]
for typ,phase in [('lesson','initial'),('lesson','remedial'),('review','initial'),('review','remedial')]:
 observed=s['phase_distributions']['all/'+typ+'/'+('additional' if phase=='remedial' else phase)]
 labels.extend([f'{typ.title()} {phase}\nEngine weights',f'Observed, n={observed["n"]:,}'])
 valrows.append([s['engine_weights'][typ+'/'+phase][b] for b in B]);valrows.append([observed['percent'][b] for b in B])
y=np.array([0,0.72,2,2.72,4,4.72,6,6.72]);left=np.zeros(len(y))
for bi,(b,c) in enumerate(zip(B,colors)):
 vals=np.array([r[bi] for r in valrows]);ax2.barh(y,vals,left=left,color=c,height=.55)
 for yy,v,l in zip(y,vals,left):
  if v>=7:ax2.text(l+v/2,yy,f'{v:.1f}%',ha='center',va='center',color='white',fontsize=9)
 left+=vals
ax2.set_yticks(y,labels,fontsize=10);ax2.invert_yaxis();ax2.set_xlim(0,100);ax2.set_xlabel('Percent');ax2.set_title('Nominal weights and observed appearances',loc='left',fontweight='bold',pad=18)
fig.legend(handles=ax1.get_legend_handles_labels()[0],labels=['Easy','Moderate','Hard'],loc='lower center',ncol=3,frameon=False,bbox_to_anchor=(.5,.03))
fig.suptitle('Captured Math Academy question difficulties',fontweight='bold',fontsize=18,x=.055,ha='left',y=.99)
fig.text(.055,.94,'Math EDB snapshot at basis 1149 • 28,631 rated questions • sources recovered for every rated question',fontsize=11,color='#465164')
fig.text(.055,.003,'Source categories overlap. Observed “remedial” means questions after the first 2 per lesson KP or first 3 per review.\nNominal weights are normalized over available bands; appearances are not recovered selection probabilities.',fontsize=9,color='#465164')
fig.tight_layout(rect=(0,.085,1,.91),w_pad=3)
fig.savefig(OUT/'difficulty-comparison.png',dpi=170);fig.savefig(OUT/'difficulty-comparison.svg');plt.close(fig)
def table(headers,rows):
 return '<table><thead><tr>'+''.join('<th>'+html.escape(str(x))+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(x)+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table>'
def mix(d):return [f"{d['percent'][b]:.1f}%" for b in B]
def fmt(n):return f'{n:,}'
source_table=table(['Captured source','Unique rated questions','Easy','Moderate','Hard'],[[t.title(),fmt(s['unique_by_source_type'][t]['n']),*mix(s['unique_by_source_type'][t])] for t in types]+[['All unique questions',fmt(s['rated_question_count']),*mix(s['all_rated_distribution'])]])
rows=[]
for typ,phase in [('lesson','initial'),('lesson','remedial'),('review','initial'),('review','remedial')]:
 d=s['phase_distributions']['all/'+typ+'/'+('additional' if phase=='remedial' else phase)]
 w=s['engine_weights'][typ+'/'+phase]
 rows.append([typ.title()+' '+phase,fmt(d['n']),' / '.join(f'{w[b]:.0f}' for b in B),' / '.join(f'{d["percent"][b]:.1f}' for b in B),' / '.join(f'{d["percent"][b]-w[b]:+.1f}' for b in B)])
phase_table=table(['Sequence position','Rated appearances','Engine E / M / H','Observed E / M / H','Difference in percentage points'],rows)
rows=[]
for stream,label in [('older-automated','Older automated captures'),('recent-automated','Recent automated captures'),('human-history','Human task history')]:
 for typ in ['lesson','review']:
  for phase in ['initial','additional']:
   d=s['phase_distributions'][stream+'/'+typ+'/'+phase]
   rows.append([label,typ.title()+' '+phase,fmt(d['n']),*mix(d)])
stream_table=table(['Source stream','Position','Rated appearances','Easy','Moderate','Hard'],rows)
rows=[]
for key,v in avail.items():rows.append([key.replace('/',' ').capitalize(),fmt(v['slots']),*mix(v),fmt(v['no_positive_rated_band'])])
avail_table=table(['Engine phase','Slots with eligible rated bands','Easy','Moderate','Hard','Slots without a positive rated band'],rows)
rows=[]
for k,v in sorted(s['exclusive_source_combinations'].items(),key=lambda x:-x[1]['n']):rows.append([k.replace(';',' + ').title(),fmt(v['n']),*mix(v)])
exclusive_table=table(['Exact set of observed activity types','Unique questions','Easy','Moderate','Hard'],rows)
report='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Engine weights and captured question difficulties</title><style>
body{font:16px/1.6 system-ui,sans-serif;color:#233044;background:#f5f7fa;margin:0}main{max-width:1100px;margin:36px auto;padding:40px;background:white;border-radius:12px}h1{font-size:32px;line-height:1.2;margin:0 0 24px}p{margin:20px 0}strong{color:#18253a}table{width:100%;border-collapse:collapse;font-size:14px;margin:22px 0 28px}th,td{padding:10px 12px;border-bottom:1px solid #dae1e9;text-align:right}th:first-child,td:first-child{text-align:left}th{background:#eef3f8;font-weight:600}img{width:100%;height:auto;margin:18px 0}a{color:#2d58a1}aside{background:#eff4fa;padding:14px 20px;border-radius:6px}small{color:#566378}.scroll{overflow-x:auto}.downloads{display:flex;flex-wrap:wrap;gap:18px}details{margin:24px 0}summary{cursor:pointer;font-weight:600}@media(max-width:700px){main{padding:22px;margin:0}h1{font-size:26px}table{font-size:12px}th,td{padding:8px}}
</style><main><h1>Engine weights and captured question difficulties</h1>
<p>The current engine’s zero Hard weight for remedial lessons and reviews does not match the captured behavior. Hard questions appear after the initial cutoff in both activity types, including in human task history. The largest numerical difference is review remedial selection: the engine specifies 90% Easy, 10% Moderate, and 0% Hard, while the captured additional questions are 32.7%, 44.1%, and 23.2% respectively.</p>
<p>The analysis covers every question with a difficulty rating in the <code>math</code> database at transaction basis <strong>1149</strong>, captured on October 11, 2026. The database has <strong>55,015</strong> questions, of which <strong>28,631</strong> have a rating and <strong>26,384</strong> do not. Every rated question was matched to a source activity; every available source rating agreed with the current database rating.</p>
<aside>These are observed distributions of captured questions. They describe the available evidence, but do not recover Math Academy’s private sampling probabilities. Automated captures, question-bank availability, and activity stopping rules affect the observed mix.</aside>
<img src="difficulty-comparison.png" alt="Stacked bars comparing captured source difficulty proportions and engine weights with observed initial and additional question appearances">
<p><strong>The full rated question inventory</strong> contains 12,680 Easy, 11,635 Moderate, and 4,316 Hard questions. The source files distinguish lessons, reviews, assessments, multisteps, and diagnostics, even where EDB stores only shared question and knowledge-point membership.</p>
SOURCE_TABLE
<p>A question can appear in several activity types. There are <strong>1,344</strong> such questions, so the activity rows above overlap and should not be added together. Each row deduplicates question identities within its activity type; the final row deduplicates across the whole database.</p>
<p><strong>The comparison with engine weights</strong> uses question appearances rather than unique bank entries: one appearance per question identity per task, with repeated use across different tasks retained. The rated questions have <strong>32,449</strong> source appearances across <strong>3,248</strong> completed tasks. Lessons contribute 23,516 appearances in 1,616 tasks; reviews contribute 7,322 in 1,508 tasks. Assessments contribute 556 in 65 tasks, multisteps 314 in 41 tasks, and diagnostics 741 in 18 tasks.</p>
<p>The engine switches from initial to remedial weights after the first <strong>two practice questions per lesson knowledge point</strong> or the first <strong>three questions per review</strong>. The same cutoffs were applied to source order. “Additional” in the source tables means questions beyond those cutoffs; the captures do not explicitly label Math Academy’s internal sampling phase. Assessments, multisteps, and diagnostics have fixed captured sequences and are outside these four engine distributions.</p>
PHASE_TABLE
<p>Lesson initial selection produces a less Easy-heavy observed mix than the nominal 60 / 30 / 10 configuration. Review initial selection is comparatively close to 40 / 40 / 20. Both remedial configurations exclude a difficulty band that occurs in the sources. Across additional questions, the lesson sample contains <strong>1,884 Hard appearances</strong>, and the review sample contains <strong>653</strong>.</p>
<p><strong>Capture policy matters most for the remedial comparison.</strong> Older automated captures dominate the additional-question sample. Their saved policies frequently specify <code>CWCWC</code> or <code>WCWCC</code>, deliberately alternating correct and wrong answers to capture more questions. These are task presentations elicited by a collection policy, rather than a representative learner error distribution. Recent automated captures and human history therefore appear separately below.</p>
STREAM_TABLE
<p>The human additional samples are small: 89 rated lesson appearances and 18 review appearances. Their Hard shares are 7.9% and 5.6%. This still contradicts a strict zero Hard weight, while the small review sample cannot establish a reliable replacement distribution. The recent automated review sample also differs sharply from the current remedial weights: 30.4 / 44.7 / 24.9 over 237 additional appearances.</p>
<p>Two saved human tasks illustrate why the zero needs scrutiny. In <a href="../../mathacademy/progress-history-2026-10-04/11611286.json">lesson 11611286</a>, one KP has the ordered sequence Hard Correct, Hard Incorrect, <strong>Hard Correct</strong>, Moderate Correct. The third question is <code>q-329274</code>. In <a href="../../mathacademy/progress-history-2026-10-04/4866772.json">review 4866772</a>, the ordered sequence is Moderate Correct, Hard Correct, Hard Incorrect, <strong>Hard Correct</strong>, Easy Correct. The fourth question is <code>q-236651</code>. These are genuine additional questions following an incorrect answer, not an inference from bank membership.</p>
<p><strong>Available bands change the realized percentages.</strong> The selector first chooses a difficulty band, normalizing the weights over available fresh, usable questions, then chooses a question in that band. A large band does not receive extra probability merely because it contains more questions. Among 3,712 knowledge points with at least one rated question, only 439 (11.8%) contain all three rated bands. There are 862 Easy-only KPs, 404 Moderate-only KPs, and 144 Hard-only KPs. A nominal 60% Easy weight therefore need not produce 60% Easy across tasks.</p>
<p>An illustrative calculation applies the current engine weights to the current captured rated banks at each source position, excluding earlier questions in that source sequence. Lesson candidates come from the question’s KP; review candidates come from the captured topic. It assumes all those rated questions are usable and otherwise fresh, and omits earlier learner history, answer-key completeness, unrated fallback, and Math Academy’s uncaptured bank. These assumptions prevent treating it as a production prediction.</p>
AVAIL_TABLE
<p>Availability brings review initial selection fairly close to its observed mix. It does not explain the remedial Hard questions: a zero weight still excludes Hard whenever the engine selects from rated bands. The lesson calculation also reaches 485 source positions with no positively weighted rated band remaining; actual usability and unrated fallback would determine whether the running engine can continue there.</p>
<p><strong>The data supports revisiting the remedial exclusions first.</strong> If the objective is to reproduce observed capture behavior, both lesson and review remedial selection should permit Hard questions, and review remedial selection should allow substantially more Moderate questions. The full observed percentages are useful empirical baselines, but automatic replacement with those percentages would overfit a collection policy and a captured subset of the bank. Initial weights warrant calibration against available bands and topic mix before changing them.</p>
<p><strong>Coverage and validation</strong> were checked by joining the database’s current question IDs, ratings, KP membership, and policy records at one fixed basis. Activity types and source order came from normalized captures, their saved state, and original completed-task HTML. Human lesson sequences use the source DOM’s KP groups; reviews use whole-task order. Archived source streams include <code>question-capture</code>, <code>question-capture-workers</code>, <code>capture</code>, <code>progress-history-2026-10-04</code>, and manual assessment/multistep folders.</p>
<p>Source sequences retain questions absent from the rated database, so an unimported question never moves a later question into an initial slot. There are 99 lesson/review sequences with at least one question outside the rated database. Restricting the comparison to fully represented sequences changes the four E / M / H results only slightly: lesson initial 46.3 / 39.9 / 13.9; lesson additional 45.7 / 40.1 / 14.3; review initial 39.7 / 44.1 / 16.2; review additional 32.6 / 44.2 / 23.2.</p>
<p>The database itself has no rated question-to-imported-Math-Academy-task links through learner-task records. Direct activity structure resolves only 1,115 rated questions, and shared KP membership does not establish whether a question was captured in a lesson or review. Source-document recovery supplies that distinction. None of the rated questions are canonical worked examples. All rated questions have KP membership.</p>
<details><summary>Exact source combinations without overlapping counts</summary>EXCLUSIVE_TABLE</details>
<p><strong>Analysis files</strong> preserve the question-level audit trail, all phase counts, KP bank coverage, and the fixed EDB query results. The database and engine configuration were read without changes.</p>
<div class="downloads"><a href="rated-questions.csv">Every rated question and its sources</a><a href="rated-appearances.csv">Every rated task appearance</a><a href="phase-distributions.csv">Phase distributions</a><a href="knowledge-point-banks.csv">KP difficulty banks</a><a href="sequence-coverage.csv">Sequence coverage</a><a href="summary.json">Summary data</a><a href="difficulty-comparison.svg">Export chart</a></div>
<p><small>Reproduction: <code>capture_db.py</code> reads EDB at basis 1149; <code>index_sources.py</code> indexes source appearances; <code>analyze.py</code> computes and validates counts; <code>render_report.py</code> renders this report. Use the project’s existing EDB peer configuration and Python environments. Raw evidence may include captures made after the snapshot; only identities present with a rating at basis 1149 enter the analysis.</small></p>
</main></html>'''
for key,value in [('SOURCE_TABLE',source_table),('PHASE_TABLE',phase_table),('STREAM_TABLE',stream_table),('AVAIL_TABLE',avail_table),('EXCLUSIVE_TABLE',exclusive_table)]:report=report.replace(key,'<div class="scroll">'+value+'</div>')
(OUT/'analysis.html').write_text(report)
print(OUT/'analysis.html')
