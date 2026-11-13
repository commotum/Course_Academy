#!/usr/bin/env python3
"""Rebuild the disjoint review-2 matrix-table review and immutable field proposals.

No EDB access or writes. Geometry is recovered from stored rows by documented
family partitions. Actual MA source snapshots are evidence, never replacement
values for historical questions. All supplied entries come from assigned.json.
"""
from pathlib import Path
import collections, html, json, re, subprocess, sys
from bs4 import BeautifulSoup
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
sys.path.insert(0,str(ROOT))
from scripts.question_capture.math_format import matrix_answer,matrix_input_grid,matrix_equation,matrix_operands,matrix_tex
BASE=HERE.parent
A=json.loads((HERE/'assigned.json').read_text())
FIELDS=json.loads((BASE/'snapshot-fields.json').read_text())
ENTS={x[':db/id']:x for x in json.loads((BASE/'capture/entities.json').read_text())}
TOPICS={x[':db/id']:x[':topic/math-academy-id'] for x in json.loads((BASE/'capture/topics.json').read_text())}
SOURCE=Path('/home/jake/Developer/MA/DATA/Lessons')
CONFIRMED_TOPICS={5379,3231,3635,3190,147,2088,5916,1358}

def dump(name,data): (HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def bare(x):
 x=html.unescape(x.strip())
 return x[1:-1] if x.startswith('$') and x.endswith('$') else x

def source_evidence():
 """Actual source JSON items and raw-HTML matrix border/control geometry."""
 ids={str(ENTS[x['entity']].get(':tutorial/math-academy-id')) for x in A if not x['topics']}
 pattern='"content_id": "(?:'+'|'.join(sorted(ids))+')"'
 found=subprocess.run(['rg','-l',pattern,str(SOURCE),'-g','*.json'],text=True,capture_output=True,check=True).stdout.splitlines()
 files={SOURCE/str(TOPICS[t])/'Source'/f'{TOPICS[t]}.json' for x in A for t in x['topics']}
 files.update(Path(x) for x in found)
 out={}; tutorial_map={}
 for path in sorted(files):
  d=json.loads(path.read_text());tid=int(d['topic_id']);items=d['lesson']['items']
  entry={'source_json':str(path),'source_html':str(path.with_suffix('.html')),'topic_title':d['topic_title'],'questions':{},'tutorials':{}}
  for item in items:
   if item['item_type']=='question':
    qid=str(item['question_id']);entry['questions'][qid]={'selector':'#question-'+qid,'readable_text':item.get('readable_text','')[:5000],'format':item.get('question_format')}
   elif item.get('step_type')=='tutorial' and str(item.get('content_id')) in ids:
    cid=str(item['content_id']);entry['tutorials'][cid]={'selector':item.get('selector'),'title':item.get('title'),'readable_text':item.get('readable_text','')[:20000]};tutorial_map.setdefault(cid,[]).append(tid)
  soup=BeautifulSoup(path.with_suffix('.html').read_text(),'html.parser')
  for qid,q in entry['questions'].items():
   node=soup.select_one(q['selector']);tables=[]
   if node:
    for tb in node.find_all('table'):
     if tb.find_parent('table') is not None or 'questionWidget-choicesTable' in tb.get('class',[]):continue
     if not tb.select('.matheditor-wrapper-answer,.selectList,[id^=freeResponseTextbox]'):continue
     rr=[]
     for row in tb.find_all('tr'):
      if row.find_parent('table') is not tb:continue
      cc=[]
      for cell in row.find_all(['td','th'],recursive=False):
       m=cell.find('math')
       controls=[z['id'] for z in cell.select('[id]') if z.get('id','').startswith(('freeResponseTextbox','selectList-'))]
       cc.append({'rowspan':cell.get('rowspan'),'colspan':cell.get('colspan'),'style':cell.get('style'),'math_text':m.get_text(' ',strip=True) if m else None,'control_ids':controls})
      rr.append(cc)
     tables.append({'table_style':tb.get('style'),'rows':rr})
   q['raw_control_tables']=tables
  out[str(tid)]=entry
 dump('source-evidence.json',out)
 return out,tutorial_map

EVID,TUTORIAL_MAP=source_evidence()

def evidence(x):
 tids=[TOPICS[t] for t in x['topics']]
 if not tids:tids=TUTORIAL_MAP.get(str(ENTS[x['entity']].get(':tutorial/math-academy-id')),[])
 docs=[]
 for tid in tids:
  doc=EVID[str(tid)];exact=[]
  for iid in x['imported_ids']:
   qid=iid.removeprefix('q-')
   if qid in doc['questions']:exact.append(qid)
  source_questions=exact or [qid for qid,q in doc['questions'].items() if q['raw_control_tables']][:2] or list(doc['questions'])[:2]
  if tid==147 and len(x['rows'])==3:source_questions=['11571','19850']
  cid=ENTS[x['entity']].get(':tutorial/math-academy-id')
  match_kind='exact_tutorial_content_id' if cid is not None else 'exact_question_id' if exact else 'source_family_only'
  docs.append({'topic_id':tid,'source_json':doc['source_json'],'source_html':doc['source_html'],'source_question_ids':source_questions if cid is None else [],'match_kind':match_kind,'tutorial_content_id':cid,'evidence_file':'source-evidence.json'})
 return docs

def disconfirm_reason(x):
 text=' '.join(x['titles'])+' '+x['context_before']+' '+x['context_after'];r=x['rows']
 if 'Adjacency' in text or any(t==17592186050493 for t in x['topics']):
  return 'Legitimate labeled adjacency table: the first row and column identify relation elements, while the interior cells are edge indicators. Source retains blue header cells and full cell rules; converting headers to matrix entries would change meaning.'
 if "Prim" in text or 'spanning tree' in text or 'A Concrete Example' in text:
  return 'Legitimate labeled distance/Prim algorithm table. Vertex headers v_i and intermediate algorithm markings identify rows and columns; source uses data headers and cell rules, not bracket decoration.'
 if x['candidate_index']==521:return 'Long-division working layout, with quotient, divisor, subtraction and remainder positions; not a matrix or vector. No matrix repair is proposed.'
 if 'Affine Boolean' in text:return 'Boolean truth/minterm data table: x_1, x_2 and f headers index input/output cases; the final column annotates minterms. Empty annotation cells are intentional.'
 if any(w in text for w in ['Consequent','Implication','Premise','truth table']):return 'Truth table with premises/conclusion headers and logical valuations; empty separator columns and grouped headings are intentional.'
 if 'Cantor' in text:return 'Bijection/enumeration diagram for Cantor diagonal argument. Natural-number rows, arrows and decimal expansions are distinct semantic columns, not matrix entries.'
 if x['candidate_index'] in {563,564}:return 'Comparison table for vector-space axioms. R^2 and M_2(R) are column headings, A1–A8 are axiom labels, and prose states each property; not matrix layout.'
 if x['candidate_index'] in {581,582}:return 'Function-value table showing approach to a vertical asymptote. x and f(x) rows and directional annotations are data/limit semantics, not matrix brackets.'
 if x['candidate_index'] in {576,577}:return 'Slope-field value table: headers x=-1,0,1 and y=1,0,-1 name evaluation coordinates for dy/dx=x-y; empty or filled interior cells are scalar slope values at coordinate pairs, not matrix entries.'
 if x['candidate_index'] in {584,585,586}:return 'Side-by-side comparison of source-free stream functions and conservative potential functions, with labeled property rows and prose/formula cells. The outer nesting is comparison layout; neither nested table is a matrix.'
 if any(w in text for w in ['standard normal','cumulative distribution','Φ(z)']):return 'Nested standard-normal lookup tables with z headers and probabilities. The outer table arranges reference data side by side; values are not operands or answer matrices.'
 return 'Labeled representation/conversion table. Stored row/column labels and surrounding explanatory prose establish data-table intent; no bracketed matrix operand or answer is represented.'

def replacement(x):
 """All values below are taken verbatim from nonempty stored source cells."""
 rr=[[bare(c) for c in row if c.strip()] for row in x['rows']]
 tid=TOPICS[x['topics'][0]] if x['topics'] else None
 grids=[];parts=[];description=''
 if tid==5379:
  if rr[0][0]=='[':
   a,b=rr;assert len(a)==6 and len(b)==3
   grids=[a[1:3],b[:2]],[[a[4]],[b[2]]]
   label=a[3];assert label.startswith(']') and label.endswith('[')
   parts=[grids[0],label[1:-1],grids[1]]
   tail=a[5][1:]
   if tail:parts.append(tail)
   description='2x2 Jacobian times (x1-x0) equals a 2x1 residual; top row bracket/label cells span both rows in the actual Newton source.'
  else:
   a,b=rr;assert len(a)==3 and len(b)==1 and a[0].endswith('[') and a[2].startswith(']')
   grids=[[[a[1]],[b[0]]]];parts=[a[0][:-1],grids[0]]
   if a[2][1:]:parts.append(a[2][1:])
   description='2x1 iterate vector: first/third top cells are spanning label/closing bracket, second row contains the second component.'
 elif tid==3635:
  n=len(rr);assert n in [2,3] and len(rr[0])==n+3 and all(len(row)==n+1 for row in rr[1:])
  grids=[[rr[0][1:n+1]]+[row[:n] for row in rr[1:]],[[rr[0][-1]]]+[[row[-1]] for row in rr[1:]]]
  parts=[rr[0][0],grids[0],rr[0][-2],grids[1]]
  description=f'{n}x{n} coefficient matrix A followed by {n}x1 forcing vector f(t); source spanning labels and narrow border cells delimit both independent operands.'
 elif tid in [3231,147]:
  if tid==147 and len(rr)==3:
   assert all(len(row)==9+(i==1) for i,row in enumerate(rr))
   a,b,c=rr;assert b[6]=='=';b=b[:6]+b[7:]
   grids=[[row[:3] for row in [a,b,c]],[row[3:6] for row in [a,b,c]],[row[6:] for row in [a,b,c]]]
   parts=[grids[0],grids[1],'=',grids[2]]
   description='Three distinct 3x3 operands: first two given factors and mixed supplied/answer result. Stored blank columns delimit bracket boundaries; middle-row equals separates the result.'
  else:
   a,b=rr;assert len(a)==4 and len(b)==2
   grids=[[a[1:3],b]];parts=[a[0],grids[0],a[3]]
   description='2x2 answer matrix after the spanning Jacobian/product label; two populated entries per row, followed by punctuation. Empty cells were bracket borders.'
 elif tid==3190:
  a,b=rr;assert len(a)==2 and len(b)==1
  grids=[[[a[1]],[b[0]]]];parts=[a[0],grids[0]]
  description='2x1 solution vector after x(t)=; actual source has narrow border cells around two vertically aligned answer controls.'
 elif tid==2088:
  a,b=rr;assert len(a)==5 and len(b)==2
  grids=[[[a[1]],[b[0]]],[[a[3]],[b[1]]]];parts=[a[0],grids[0],a[2],grids[1],a[4]]
  description='Two separate 2x1 coefficient vectors, each followed by its original exponential scalar; source has spanning labels/scalars between bracket-cell groups.'
 elif tid==5916:
  a,b=rr
  if '⊙' in a[2:3]:
   assert len(a)==4 and len(b)==2
   grids=[[[a[1]],[b[0]]],[[a[3]],[b[1]]]];parts=[a[0],grids[0],a[2],grids[1]]
   description='Two 2x1 vector operands joined by the supplied Hadamard operator; source control-table geometry has a spanning ⊙ between vector bracket groups.'
  else:
   assert len(a)==4 and len(b)==3
   grids=[[a[1:3],b[:2]],[[a[3]],[b[2]]]];parts=[a[0],grids[0],grids[1]]
   description='2x2 matrix followed by 2x1 vector (matrix-product form); original source border-cell groups distinguish these operands, including supplied zeros and second-row values.'
 elif tid==1358:
  a,label,b=rr;assert len(a)==2 and len(label)==1 and len(b)==2
  grids=[[a,b]];parts=[label[0],grids[0]]
  description='2x2 standard matrix T: its two populated entry rows surround an otherwise empty vertical-centering label row. Source family asks for the 2x2 standard matrix; no third entry row is present.'
 else:raise ValueError(tid)
 return matrix_equation(parts),grids,parts,description

reviews=[];changes=collections.defaultdict(list);changed_current=[]
for x in A:
 key=f"{x['entity']}/{x['attribute']}";before=FIELDS[key]
 current=ENTS[x['entity']].get(':'+x['attribute'])
 assert current==before,('Captured current field differs',key)
 start,end=x['span'];assert before[start:end]==x['table'],(x['candidate_index'],'bad census span')
 tid=TOPICS[x['topics'][0]] if x['topics'] else None
 review={'candidate_index':x['candidate_index'],'entity':x['entity'],'attribute':x['attribute'],'status':'confirmed' if tid in CONFIRMED_TOPICS else 'disconfirmed','source_evidence':evidence(x),'stored_rows':x['rows'],'basis':14371}
 if review['status']=='confirmed':
  after,grids,parts,why=replacement(x)
  assert collections.Counter(re.findall(r'\{\{[^{}]+\}\}',x['table']))==collections.Counter(re.findall(r'\{\{[^{}]+\}\}',after))
  # Replacement representation explicitly records operand-wise row-major positions.
  review.update(reason=why,operand_rows=grids,equation_parts=parts,replacement=after)
  changes[key].append((start,end,after,x['candidate_index'],why))
 else:review['reason']=disconfirm_reason(x)
 reviews.append(review)

proposals=[]
for key,edits in sorted(changes.items()):
 before=FIELDS[key];after=before;end_of_prior=-1;patches=[]
 for start,end,repl,idx,reason in sorted(edits):assert start>=end_of_prior;end_of_prior=end
 for start,end,repl,idx,reason in sorted(edits,reverse=True):
  # Remove obsolete source-table-scroll wrapper if it surrounds exactly this table.
  wrapper='<div class="source-table-scroll">'
  if before[:start].endswith(wrapper) and before[end:].startswith('</div>'):
   start-=len(wrapper);end+=len('</div>')
  patches.append({'start':start,'end':end,'before':before[start:end],'after':repl,'candidate_indices':[idx]})
  after=after[:start]+repl+after[end:]
 assert collections.Counter(re.findall(r'\{\{[^{}]+\}\}',before))==collections.Counter(re.findall(r'\{\{[^{}]+\}\}',after))
 entity,attribute=key.split('/',1)
 proposals.append({'entity':int(entity),'attribute':attribute,'before':before,'after':after,'candidate_indices':[e[3] for e in sorted(edits)],'rationale':' '.join(dict.fromkeys(e[4] for e in sorted(edits))),'replacements':sorted(patches,key=lambda p:p['start'])})
dump('reviews.json',sorted(reviews,key=lambda x:x['candidate_index']));dump('proposals.json',proposals)
summary={'assigned':len(A),'statuses':dict(collections.Counter(x['status'] for x in reviews)),'proposal_fields':len(proposals),'basis':14371,'changed_since_census':changed_current}
dump('summary.json',summary);print(json.dumps(summary,indent=2))
