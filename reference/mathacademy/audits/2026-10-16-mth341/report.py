"""Combine snapshot, static checks, image review, and actual-renderer findings."""
import collections,html,json,re,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from math_format import validate_tex,validate_prose
from edn import loads
E=lambda x:html.escape(str(x))
def read(n):return json.loads((HERE/n).read_text())
def save(n,v):(HERE/n).write_text(json.dumps(v,indent=2)+'\n')
entities=read('entities.json');fields=read('fields.json');inv=read('inventory.json');images=read('images.json');assignments=read('assignments.json');render=read('rendering.json')['fields']
assert len(render)==len(fields)==9005
rr={(r['entity'],r['attribute']):r for r in render};formula={x['path'] for x in images if x['classification']=='formula'}
qkp=collections.defaultdict(list)
for e in entities.values():
 if ':knowledge-point/id' in e:
  for q in [e[':knowledge-point/canonical-example']]+e.get(':knowledge-point/questions',[]):qkp[q[':db/id']].append(e[':db/id'])
component_kps=collections.defaultdict(set)
for q in entities.values():
 if ':question/id' not in q:continue
 for a in q.get(':question/answer-fields',[]):
  component_kps[a[':db/id']].update(qkp.get(q[':db/id'],[]))
  for c in a.get(':answer-field/choices',[]):component_kps[c[':db/id']].update(qkp.get(q[':db/id'],[]))
for f in fields:
 f['flags']=[z for z in f['flags'] if z['kind'] not in ['formula-image','raw-tex','render-warning','markdown-code']]
 refs=[v for z in f['flags'] if z['kind']=='images' for v in z['detail']]
 if any(v in formula for v in refs):f['flags'].append({'kind':'formula-image','detail':[v for v in refs if v in formula]})
 r=rr[f['entity'],f['attribute']]
 for key,kind in [('residualText','raw-tex'),('undefinedMacros','render-warning'),('codeBlocks','markdown-code')]:
  if r.get(key):f['flags'].append({'kind':kind,'detail':r[key]})
 if f.get('normalized'):
  try:(validate_tex if f['kind']=='math' else validate_prose)(f['normalized']);f['normalization_validates']=True
  except Exception:f['normalization_validates']=False
 f['knowledge_points']=qkp.get(f['entity'],[])
 # Choice and answer-field ownership is also retained for actionable findings.
 if not f['knowledge_points']:f['knowledge_points']=sorted(component_kps[f['entity']])
for t in inv:
 fs=[f for f in fields if t['id'] in f['topics']]
 t['flags']=dict(collections.Counter(z['kind'] for f in fs for z in f['flags']))
 t['missing_solutions']=[q for q in t['questions'] if not entities[str(q)].get(':question/worked-solution')]
 t['missing_correct_questions']=[q for q in t['questions'] if any(not a.get(':answer-field/correct') for a in entities[str(q)].get(':question/answer-fields',[]))]
 t['assignments']=[]
 for a in assignments:
  if any(v[':db/id']==t['id'] for s in a.get(':activity/steps',[]) for v in s.get(':step/content',{}).get(':assigned-problem/topic-coverage',[])):t['assignments'].append(a[':db/id'])
summary=read('summary.json');summary.update({'basis':3078,'assignments':len(assignments),'flags':dict(collections.Counter(z['kind'] for f in fields for z in f['flags'])),'unique_images':len(images),'formula_images':len(formula),'diagram_images':len(images)-len(formula),'missing_images':sum(not x['exists'] for x in images),'missing_solutions':sum(not e.get(':question/worked-solution') for e in entities.values() if ':question/id' in e),'answer_fields_missing_correct':sum(not e.get(':answer-field/correct') for e in entities.values() if ':answer-field/id' in e),'questions_missing_correct':len({q for t in inv for q in t['missing_correct_questions']}),'rendered_fields':len(render),'database_mutated':False})
save('summary.json',summary);save('fields.json',fields);save('findings.json',[f for f in fields if f['flags']]);save('inventory.json',inv)
style='''body{font:16px/1.5 system-ui,sans-serif;color:#172534;background:#f7f8fa;max-width:1280px;margin:auto;padding:32px}h1,h2,h3{line-height:1.2}table{border-collapse:collapse;width:100%;background:white;margin:20px 0}td,th{padding:9px;border:1px solid #d3dae2;text-align:left;vertical-align:top}th{background:#e7edf5}code,pre{font:13px/1.5 ui-monospace,monospace}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#edf1f6;padding:14px}a{color:#07579b}details{background:white;padding:12px;margin:12px 0;border:1px solid #d3dae2}summary{cursor:pointer;font-weight:600}img{max-width:100%;border:1px solid #ddd}small{color:#45556b}.notice{border-left:5px solid #a34220;padding:12px;background:#fff0e8}.counts{display:flex;gap:12px;flex-wrap:wrap}.counts span{background:white;padding:12px;border:1px solid #d3dae2}section{scroll-margin-top:20px}.tag{font-size:12px;color:#963815}'''
out=['<!doctype html><html lang="en"><meta charset="utf-8"><title>MTH 341 content audit</title><style>'+style+'</style><h1>MTH 341 Markdown and LaTeX audit</h1>', '<p>16 October 2026 · math database basis 3078 · read-only investigation</p>','<div class="counts">'+''.join(f'<span><b>{summary[k]:,}</b> {label}</span>' for k,label in [('assignments','assignments'),('topics','target topics'),('kps','KPs'),('questions','questions and examples'),('tutorials','tutorials'),('fields','content fields rendered')])+'</div>', '<p class="notice">The reported matrix defect is confirmed. This report records findings and repair candidates; no database content or application code was changed.</p>']
out+=['<h2>Confirmed findings</h2><ul><li><b>89 fields</b> use literal brackets around layout environments. For ordinary matrices, replace bracketed aligned layouts with bmatrix; retain explicit column rules for augmented matrices.</li><li><b>49 fields</b> fail the shared TeX validator. Rendering exposes raw TeX in <b>46 fields</b>, including 19 invertible-matrix theorem fragments and malformed systems of equations.</li><li><b>13 question prompts</b> have matrix-answer labels ending in <code>=\\=</code>, visibly emitting an unsupported command. These are in addition to other renderer warnings.</li><li><b>1 question</b>, 17592186235392, renders answer labels/placeholder HTML in Markdown code blocks because of indentation.</li><li><b>105 formula assets</b> occur in 79 fields: 85 MathJax SVGs retain MathML, and 20 PNGs contain matrices. Preserve annotations when converting. The remaining 148 images are graphs or diagrams; all 253 referenced image files exist.</li><li><b>148 fields</b> differ structurally from the shared normalizer. This includes the bracket failures and benign equivalent notation; it is not a count of 148 independent rendering failures.</li></ul>', '<p>Additional completeness findings: <b>74 practice questions</b> lack worked solutions; <b>82 answer fields across 75 questions</b> lack correct-answer links. Two practice questions (17592186233433 and 17592186233218) have no answer fields. The 92 canonical examples also have no answer fields, which is expected for their role.</p>']
out+=['<h2>Your examples</h2><table><tr><th>Entity</th><th>Finding</th></tr>']
examples=[(17592186125757,'Introduction contains two SVG matrix formulas. Their embedded MathML preserves every entry and the highlighted pivots; TeX conversion need not rely on guessing from pixels.'),(17592186566216,'Problem and solution both use B=[\\begin{aligned}…\\end{aligned}]. Reproduces the supplied screenshot. The correct key is columns 1, 3, 4.'),(17592186566219,'Same defect in problem and solution. The correct key is columns 1, 3, 5.'),(17592186124903,'Uses bmatrix correctly in problem and solution.'),(17592186414495,'Uses bmatrix correctly in problem and solution.'),(17592186403661,'Uses bmatrix correctly in problem and solution.')]
for eid,msg in examples:out.append(f'<tr><td><a href="#e{eid}">{eid}</a></td><td>{E(msg)}</td></tr>')
out+=['</table><p>The pivot topic has four affected questions (17592186566216, 17592186566219, 17592186566245, 17592186124885), totaling eight bracket-layout fields, plus seven fields containing formula images.</p>', '<h2>Why good and bad formats coexist</h2><p>The three good example fields have source <code>:application/ca-engine</code>. The two bad examples have source <code>:org/Math-Academy</code> and transaction 13194139536104 (basis 2792). The retained capture request was prepared at basis 2791 and already contained the bad bracketed-aligned text.</p><p>Current <code>core.py</code> and <code>math_content.py</code> call <code>normalize_capture_question</code>. That function would correct these matrices. The captured transaction nevertheless retained the old form. This establishes an ingestion/repair coverage gap; it does not establish whether a stale process, an older prepared batch, or an alternate writer produced it. Normalize and validate at the final preparation boundary before generating a new immutable request. Preserve request identity during retries.</p>', '<p>Evidence: <a href="provenance.edn">field provenance</a>; <a href="../../capture/linear/14248325/database/requests/capture-dd94755c-4799-40c8-82d7-37a47b191ec1/request.json">retained capture request</a>.</p>', '<h2>All 30 assignment target topics</h2><p>Counts are fields, except KPs/Qs. Categories overlap. “Standard” means a structural normalization difference; “TeX” means validator failures; “Formula” means fields using formula images; “Render” combines raw TeX, red command warnings and code blocks.</p><table><tr><th>Topic</th><th>ID</th><th>KPs / Qs</th><th>Brackets</th><th>Standard</th><th>TeX</th><th>Formula</th><th>Render</th><th>Missing solutions</th></tr>']
for t in inv:
 c=t['flags'];out.append(f'<tr><td><a href="#t{t["id"]}">{E(t["title"])}</a></td><td><code>{t["id"]}</code></td><td>{len(t["kps"])} / {len(t["questions"])}</td>'+''.join(f'<td>{c.get(k,0)}</td>' for k in ['fixed-brackets','noncanonical','validation','formula-image'])+f'<td>{sum(c.get(k,0) for k in ["raw-tex","render-warning","markdown-code"])}</td><td>{len(t["missing_solutions"])}</td></tr>')
out+=['</table><h2>Assignment coverage</h2>']
for a in assignments:
 tids=[t for t in inv if a[':db/id'] in t['assignments']];out.append(f'<details><summary>{E(a[":activity/title"])} · {len(tids)} targets · {a[":db/id"]}</summary><ul>'+''.join(f'<li><a href="#t{t["id"]}">{E(t["title"])}</a> · {t["id"]}</li>' for t in tids)+'</ul></details>')
out+=['<h2>Topic, KP, and question inventory</h2><p>Every direct assignment target is included. Prerequisite-only topics are not recursively added. All stored practice questions and canonical examples in the topic snapshots are included; generator scripts were inventoried, not executed.</p>']
for t in inv:
 out.append(f'<section id="t{t["id"]}"><h3>{E(t["title"])} · {t["id"]}</h3>')
 for kid in t['kps']:
  k=entities[str(kid)];qids=[k[':knowledge-point/canonical-example'][':db/id']]+[q[':db/id'] for q in k.get(':knowledge-point/questions',[])];out.append(f'<details><summary>KP {kid} · {E(k[":knowledge-point/title"])} · {len(qids)-1} practice + example</summary><p>Canonical example: {qids[0]}. Generator: {E(k.get(":knowledge-point/question-generator",{}).get(":db/id","none"))}.</p><ul>')
  for qid in qids:
   q=entities[str(qid)];flags=sorted({z['kind'] for f in fields if f['entity']==qid for z in f['flags'] if z['kind']!='indented-lines'});status=', '.join(flags) or 'no formatting flags'
   if not q.get(':question/worked-solution'):status+='; missing solution'
   if any(not a.get(':answer-field/correct') for a in q.get(':question/answer-fields',[])):status+='; missing correct answer'
   out.append(f'<li><a href="#e{qid}">{qid}</a> · {E(q.get(":question/math-academy-id","generated/local"))} · {E(status)}</li>')
  out.append('</ul></details>')
 out.append('</section>')
out+=['<h2>Entity evidence</h2><p>Source text below is escaped for inspection. Suggested normalization is a candidate only; it does not recover images, fix every broken formula, or establish mathematical correctness.</p>']
byentity=collections.defaultdict(list)
for f in fields:byentity[f['entity']].append(f)
for eid,fs in byentity.items():
 # Keep every question addressable and show all flagged content fields.
 relevant=[f for f in fs if f['flags']]
 if not relevant and eid not in qkp:continue
 out.append(f'<details id="e{eid}"><summary>{eid} · {E(entities[str(eid)].get(":question/math-academy-id",entities[str(eid)].get(":tutorial/title","content")))} · {len(relevant)} flagged fields</summary>')
 if (HERE/f'entity-{eid}.png').exists():out.append(f'<p><a href="entity-{eid}.png">Rendered screenshot</a></p>')
 for f in relevant or fs[:1]:
  out.append(f'<h4>{E(f["attribute"])}</h4><p class="tag">{E(", ".join(z["kind"] for z in f["flags"]))}</p><pre>{E(f["value"])}</pre>')
  if f.get('normalized') and any(z['kind']=='noncanonical' for z in f['flags']):out.append('<details><summary>Normalizer candidate · '+('passes' if f.get('normalization_validates') else 'still fails')+' structural validation</summary><pre>'+E(f['normalized'])+'</pre></details>')
 out.append('</details>')
out+=['<h2>Recommended repair order</h2><ol><li>Repair the 89 bracket-layout fields, malformed theorem/system fragments, 13 escaped-equals labels, and the indented answer block. Preserve matrix entries, augmented dividers, field identities, and keys.</li><li>Recover the 85 SVG formulas from their retained MathML; transcribe and verify the 20 PNG matrix assets. Keep pivot shading, row-operation annotations, and other instructional emphasis.</li><li>Normalize remaining equivalent notation to the shared convention, then render again with the actual Markdown, inline-field, and MathJax code.</li><li>Repair incomplete practice separately, with mathematical verification of solutions and answer keys.</li><li>Check final prepared capture content so new imports cannot reintroduce the old form.</li></ol>', '<h2>Method and limits</h2><p>Assignment scope follows the app’s assignment_targets relation: course MTH 341 → assignments → assigned-problem/topic-coverage. All 11 assignments have direct, non-multistep contents. One database basis is used throughout. Snapshots include topic KPs, all questions, canonical examples, and scoped activity steps. Content fields, answer values, and answer-field labels were inspected; labels contain no math delimiters. All 9,005 content fields were rendered with the repository’s Markdown renderer, inlinePrompt, MathJax configuration and vendored MathJax, with answer-field types supplied. Selected failure screenshots and all PNG contact sheets were visually inspected. All image files exist. This is a content-format audit, not a proof-check of all 1,384 mathematical solutions or a full interaction test of answer controls.</p><p>No MathJax merror nodes were emitted, despite visible failures. Raw-text and red-command detection therefore form part of the evidence. “No formatting flags” is not a guarantee of mathematical correctness.</p><p>Machine-readable evidence: <a href="summary.json">summary</a>, <a href="inventory.json">all topics</a>, <a href="findings.json">field findings</a>, <a href="images.json">image classification</a>, <a href="rendering.json">rendering results</a>, <a href="completeness.json">completeness observations</a>. Reproduction scripts: snapshot.py (read-only database access), audit.py, render.py, report.py. Image classifications were manually verified from png-contact-0.jpg through png-contact-3.jpg and SVG MathML.</p></html>']
(HERE/'report.html').write_text('\n'.join(out));print(json.dumps(summary,indent=2))
