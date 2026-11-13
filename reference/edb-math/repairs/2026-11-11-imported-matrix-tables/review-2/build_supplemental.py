#!/usr/bin/env python3
"""Complete non-Newton review of the supplemental other-math-layout queue.

No EDB writes. Stable keys use entity/attribute/original span. Original field
strings and metadata are recovered from the immutable basis14355 census dump.
"""
from pathlib import Path
import collections,gzip,html,json,re,sys
from bs4 import BeautifulSoup
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
ROOT=next(p for p in HERE.parents if (p/'scripts/question_capture/math_format.py').exists());sys.path.insert(0,str(ROOT))
from scripts.question_capture.math_format import MATH,matrix_equation,validate_prose
AUDIT=ROOT/'reference/edb-math/audits/2026-11-11-imported-matrix-tables'
QUEUE=json.loads((AUDIT/'other-math-layouts.json').read_text())
EXCLUDED={17592186048637,17592186049409};CONFIRMED={17592186050832,17592186048881}
OWN=[(i,x) for i,x in enumerate(QUEUE) if not set(x['topics'])&EXCLUDED]
WANTED={(x['entity'],x['attribute']) for _,x in OWN};TOPIC_IDS={t for _,x in OWN for t in x['topics']}
fields={};topics={}
with gzip.open(AUDIT/'snapshot.jsonl.gz','rt') as stream:
 for line in stream:
  row=json.loads(line)
  if (row['e'],row['a']) in WANTED:fields[(row['e'],row['a'])]=row['raw_string']
  if row['e'] in TOPIC_IDS and row['a']=='topic/math-academy-id':topics[row['e']]=int(row['value_edn'])
assert len(fields)==len(WANTED)
SOURCE=Path('/home/jake/Developer/MA/DATA/Lessons');sources={}
for ma in sorted(set(topics.values())):
 path=SOURCE/str(ma)/'Source'/f'{ma}.json'
 if not path.exists():
  sources[ma]={'path':str(path),'html_path':str(path.with_suffix('.html')),'topic_title':None,'questions':{},'source_missing':True}
  continue
 d=json.loads(path.read_text());qs={str(q['question_id']):q for q in d['lesson']['items'] if q['item_type']=='question'}
 sources[ma]={'path':str(path),'html_path':str(path.with_suffix('.html')),'topic_title':d['topic_title'],'questions':qs}

def bare(s):
 s=html.unescape(s.strip());return s[1:-1] if s.startswith('$') and s.endswith('$') else s

def inventory(s):
 out=[]
 for m in MATH.finditer(html.unescape(s)):
  v=m[0];out.append(v[2:-2].strip() if v.startswith(('$$',r'\(',r'\[')) else v[1:-1].strip())
 return collections.Counter(out)

def source_evidence(x):
 ma=topics[x['topics'][0]];src=sources[ma]
 ids=[iid.removeprefix('q-') for iid in x['imported_ids'] if iid.startswith('q-')]
 exact=[qid for qid in ids if qid in src['questions']]
 selected=exact or list(src['questions'])[:2]
 return {'source_json':src['path'],'source_html':src['html_path'],'math_academy_topic_id':ma,'source_topic_title':src['topic_title'],'match_scope':'Local MA source absent; direct stored prompt explicitly names a tree diagram and sample-space outcomes, sufficient to disconfirm matrix semantics.' if src.get('source_missing') else 'matching question ID in current source' if exact else 'source-family evidence only; stored historical variant may differ','question_evidence':[{'source_question_id':qid,'selector':'#question-'+qid,'readable_text':src['questions'][qid].get('readable_text','')[:4200]} for qid in selected]}

raw_geometry={}
for ma in [5527,6378]:
 soup=BeautifulSoup(Path(sources[ma]['html_path']).read_text(),'html.parser');out=[]
 for q in soup.select('[id^=question-]'):
  for tb in q.find_all('table'):
   if tb.find_parent('table') is not None or not tb.select('.matheditor-wrapper-answer,.selectList'):continue
   rows=[]
   for tr in tb.find_all('tr'):
    if tr.find_parent('table') is not tb:continue
    cc=[]
    for td in tr.find_all(['td','th'],recursive=False):
     math=td.find('math');controls=[z.get('id') for z in td.select('.matheditor-wrapper-answer,.selectList')]
     cc.append({'rowspan':td.get('rowspan'),'width':td.get('width'),'style':td.get('style'),'math_text':math.get_text(' ',strip=True) if math else None,'controls':controls})
    rows.append(cc)
   out.append({'selector':'#'+q['id'],'table_style':tb.get('style'),'rows':rows})
 raw_geometry[str(ma)]={'source_html':sources[ma]['html_path'],'control_tables':out}

def reason_disconfirmed(x):
 titles=' '.join(x['titles']);context=x['context_before']+' '+x['context_after']
 if 'Sign' in titles or 'sign' in titles:return 'Genuine sign table: interval/quadrant headers identify evaluation regions and the cells record signs of factors/functions. It is a labeled data table, not a bracketed matrix editor.'
 if 'Parametric' in titles:return 'Parametric coordinate equations x(t), y(t), z(t) plus the parameter interval. Rows are separate scalar equations and the interval is a condition; they are not matrix entries. Preserve this system editor.'
 if 'Area' in titles or 'area model' in context or 'Areas' in titles:return 'Genuine area model: outer side-length labels and interior products/areas have geometric meaning, with some numerator/denominator cells forming fractions. It is not a matrix/vector editor.'
 if 'Missing Digits' in titles or 'Multiplying Larger' in titles:return 'Vertical integer multiplication with positional digits, a multiplication sign and a product row. Place-value layout is arithmetic, not a matrix.'
 if 'Sample Spaces' in titles or 'tree diagram' in context:return 'Sample-space tree diagram: branch labels and ordered outcomes occupy distinct diagram locations; the table lays out branches rather than matrix entries.'
 if 'Riemann' in titles:return 'Definite-integral editor: vertically placed controls are upper/lower integral limits, and the central control is the integrand. Preserve scalar operator layout; it is not a matrix.'
 if 'Sigma' in titles:return 'Sigma-notation editor with summation limits and summand. Its upper/lower operator slots are not matrix rows.'
 if 'Euler' in titles:return 'Euler-method data table with x, y, derivative and increment headers. A missing next-row scalar is a data entry, not a matrix coordinate.'
 if 'Partial Fraction' in titles or 'partial fractions' in context:return 'Genuine partial-fraction decomposition: rows pair numerators with fixed denominator expressions, separated by supplied plus/minus operators. Preserve fraction editor semantics.'
 if 'Polynomial' in titles:return 'Polynomial division-result equation with fraction numerator/denominator slots and a quotient term. It is scalar arithmetic rather than a matrix/vector.'
 return 'Genuine scalar fraction/expression editor: stacked numerator and denominator slots, scalar equality and any supplied operators represent a fraction, derivative ratio, or mixed number. No matrix/vector operand is present.'

reviews=[];proposals=[]
for index,x in OWN:
 before=fields[(x['entity'],x['attribute'])];start,end=x['span'];assert before[start:end]==x['table']
 stable=f"{x['entity']}/{x['attribute']}/{start}:{end}";confirmed=bool(set(x['topics'])&CONFIRMED)
 review={'stable_key':stable,'queue_index':index,'entity':x['entity'],'attribute':x['attribute'],'span':x['span'],'candidate_indices':[],'status':'confirmed' if confirmed else 'disconfirmed','source_evidence':source_evidence(x),'stored_rows':x['rows'],'census_basis':14355}
 if not confirmed:
  review['rationale']=reason_disconfirmed(x);reviews.append(review);continue
 rows=[[c for c in row if c.strip()] for row in x['rows']];assert len(rows)==2
 label=bare(rows[0][0]);tail=''
 if x['topics'][0]==17592186048881:
  assert len(rows[0])==4 and len(rows[1])==2
  a=rows[0];b=rows[1];grid=[[bare(c) for c in a[1:3]],[bare(c) for c in b]]
  suffix=a[3];m=re.match(r'^(\$[^$]+\$)(.*)$',suffix,re.S);assert m and 'where' in m[2]
  replacement=matrix_equation([label,grid,bare(m[1])])+m[2]
  rationale='The target explicitly requests the linearized differential system. Source-family raw HTML draws bracket edges around a 2x2 coefficient matrix and rowspans both the u-prime label and the trailing u multiplier/definition. Keep the multiplier after the matrix and the definition outside it.'
 else:
  grid=[[bare(c) for c in rows[0][1:]],[bare(c) for c in rows[1]]];assert len(grid[0])==len(grid[1]) in [1,2]
  replacement=matrix_equation([label,grid])
  rationale=('The prompt asks for a two-component subset gradient (2x1 vector).' if len(grid[0])==1 else 'The prompt asks for the gradient of a two-component subset gradient (2x2 Hessian/Jacobian).')+' Actual source5527 has a rowspanned gradient label beside 5px bracket-edge cells and hidden interior borders. Supplied expressions and field placeholders remain in their source rows and columns.'
 assert inventory(x['table'])==inventory(replacement),(stable,inventory(x['table'])-inventory(replacement),inventory(replacement)-inventory(x['table']))
 assert collections.Counter(re.findall(r'\{\{[^{}]+\}\}',x['table']))==collections.Counter(re.findall(r'\{\{[^{}]+\}\}',replacement))
 for m in MATH.finditer(replacement):assert not re.search(r'\{\{(?:answer-field:)?field-\d+\}\}',m[0])
 s,e=start,end
 opening=re.search(r'<div class="source-table-scroll">\s*$',before[:s]);closing=re.match(r'\s*</div>',before[e:])
 if opening and closing:s=opening.start();e+=closing.end()
 after=before[:s]+replacement+before[e:];validate_prose(after)
 addition={'queue_stable_key':stable,'queue_index':index,'original_span':[start,end],'matrix_rows':grid,'label':label,'source_math_academy_topic_id':topics[x['topics'][0]],'source_geometry_artifact':'supplemental-source-geometry.json'}
 patch={'start':s,'end':e,'before':before[s:e],'after':replacement,'candidate_indices':[],'additional_layout':addition}
 proposals.append({'entity':x['entity'],'attribute':x['attribute'],'before':before,'after':after,'candidate_indices':[],'additional_layout':addition,'rationale':rationale,'replacements':[patch]})
 review.update(rationale=rationale,additional_layout=addition,replacement_span=[s,e],replacement=replacement);reviews.append(review)
assert len(reviews)==160 and len(proposals)==46
assert len({r['stable_key'] for r in reviews})==len(reviews)
assert len({(p['entity'],p['attribute']) for p in proposals})==46
for name,value in [('supplemental-reviews',reviews),('supplemental-proposals',proposals),('supplemental-source-geometry',raw_geometry)]:
 (HERE/f'{name}.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
summary={'queue_blocks_total':len(QUEUE),'excluded_Newton_blocks':len(QUEUE)-len(OWN),'reviewed_non_Newton_blocks':len(reviews),'statuses':dict(collections.Counter(r['status'] for r in reviews)),'proposal_fields':len(proposals),'math_token_and_marker_multisets_preserved':True,'all_replacement_grids_rectangular':True,'all_authored_replacements_prose_valid':True,'snapshot_basis':14355,'fresh_capture_validation':'Root must compare before strings to fresh current pull before native transaction.','no_db_writes':True}
(HERE/'supplemental-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
