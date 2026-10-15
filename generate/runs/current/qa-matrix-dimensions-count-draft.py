import sys
sys.dont_write_bytecode=True
import json,re,copy,hashlib,importlib.util
from pathlib import Path
R=Path(__file__).resolve().parent;K=17592186100871;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
reader=load('parent_dimension_components',R/'qa-matrix-dimensions-given-draft.py');p=reader.p;s=reader.s;dimension=reader.dimension;answer=reader.answer;equal=reader.equal;same=reader.same;prose=reader.prose
counts=dict(records=0,matrices_counted=0,displayed_entries_counted=0,answer_values=0,source_fields=0,source_values=0,source_keys=0,source_missing_keys=0,source_solutions=0,annotated_dimensions=0,known_raw_wrong_dimension=0,authored_easy_scaffold_checks=0)
def prompt(text):
 items=[]
 for m in re.finditer(r'([A-Z])\s*=\s*\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S):
  rows=[[z.strip() for z in row.split('&')] for row in m[2].split(chr(92)*2)];width=len(rows[0]);assert width and all(len(row)==width and all(z for z in row) for row in rows)
  items.append((m[1],(len(rows),width)));counts['displayed_entries_counted']+=len(rows)*width
 assert len(items)==2
 target=re.search(r'dimensions of \$([A-Z]{2})',text)[1];return items,target

def check(record):
 q=record['question'];items,target=prompt(q[':question/problem']);shapes=dict(items);a,b=target;A,B=shapes[a],shapes[b];assert A[1]==B[0];result=(A[0],B[1]);level=q.get(':question/difficulty','').split('/')[-1];raw=record['generation'].get('evidence_only');sid=record['generation'].get('source_question')
 if not raw:
  assert all(1<=v<=4 for _,shape in items for v in shape)
  if level=='easy':assert target==''.join(n for n,_ in items) and 'For conformable factors, use the number of rows of the first factor and the number of columns of the second.' in q[':question/problem'];counts['authored_easy_scaffold_checks']+=1
  elif level=='moderate':assert target==''.join(n for n,_ in items) and max(*A,*B)>=3
  elif level=='hard':assert target==''.join(n for n,_ in items)[::-1] and max(*A,*B)>=3
  else:raise AssertionError(level)
 for f in q[':question/answer-fields']:
  radio=f[':answer-field/type'].endswith('/radio');convert=answer if radio else p.scalar;values=[convert(z[':answer/value']) for z in f[':answer-field/choices']];wanted=result if radio else result[int(f[':answer-field/key'][-1])-1];match=lambda a,b:equal(a,b) if isinstance(a,(str,tuple)) else same(a,b)
  for i,z in enumerate(values):assert all(not match(z,w) for w in values[:i])
  good=[match(z,wanted) for z in values];assert sum(good)==1
  if ':answer-field/correct' in f:assert good[next(i for i,z in enumerate(f[':answer-field/choices']) if z[':answer/id']==f[':answer-field/correct'][1])]
  if not radio:assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
  counts['answer_values']+=len(values)
 if ':question/worked-solution' in q:
  text=q[':question/worked-solution'];opening=re.search(r'We notice that \$([A-Z])\$ is a \$(.*?)\$ matrix and \$([A-Z])\$ is a \$(.*?)\$ matrix',text);assert opening
  assert [opening[1],opening[3]]==[n for n,_ in items]
  for j,(name,shape) in enumerate(items):
   stated=dimension(opening[2+2*j])
   if raw and sid=='q-22067' and j==0:assert stated==(3,shape[1]);counts['known_raw_wrong_dimension']+=1
   else:assert stated==shape
  cmp=re.search(r'\$(\d+)\$ columns? in \$([A-Z])\$ and \$(\d+)\$ rows? in \$([A-Z])\.?\$',text);assert cmp;assert (int(cmp[1]),cmp[2],int(cmp[3]),cmp[4])==(A[1],a,B[0],b)
  ann=reader.annotations(text);assert [z[0] for z in ann]==[a,b,target]
  for (_,shown),wanted in zip(ann,[A,B,result]):assert equal(shown,wanted)
  conclusion=re.search(r'The product \$([A-Z]{2})\$ has dimensions \$(.*?):\$',text);assert conclusion and conclusion[1]==target and dimension(conclusion[2])==result
  counts['annotated_dimensions']+=6
 counts['records']+=1;counts['matrices_counted']+=2

if __name__=='__main__':
 g=load('parent_actual_matrix_dimensions',D.with_suffix('.py'));fmt=load('parent_dimensions_count_format',R.parents[2]/'scripts/question_capture/math_format.py');src=json.loads((R/'refresh-2026-10-14/sources'/f'{K}.json').read_text());assert src==json.loads((D/'source.json').read_text());originals={q[':question/math-academy-id']:q for q in src['record'][':knowledge-point/questions']}
 for c in json.loads((D/'source-cases.json').read_text()):
  r=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['profile']);q=r['question'];old=originals[c['source_id']];check(r)
  assert q[':question/problem']==fmt.normalize_prose(old[':question/problem'])
  for key in (':question/difficulty',':question/worked-solution'):assert (key in old)==(key in q)
  if ':question/worked-solution' in old:assert prose(old[':question/worked-solution'])==prose(q[':question/worked-solution']);counts['source_solutions']+=1
  assert {f[':answer-field/key'] for f in old[':question/answer-fields']}=={f[':answer-field/key'] for f in q[':question/answer-fields']}
  for of in old[':question/answer-fields']:
   nf=next(f for f in q[':question/answer-fields'] if f[':answer-field/key']==of[':answer-field/key']);assert of[':answer-field/type'][':db/ident']==nf[':answer-field/type'];radio=nf[':answer-field/type'].endswith('/radio');convert=answer if radio else p.scalar;match=equal if radio else same;remaining=[convert(z[':answer/value']) for z in nf[':answer-field/choices']]
   for z in of[':answer-field/choices']:
    found=[i for i,a in enumerate(remaining) if match(a,convert(z[':answer/value']))];assert len(found)==1;remaining.pop(found[0]);counts['source_values']+=1
   assert not remaining;counts['source_fields']+=1
   if ':answer-field/correct' in of:
    designated=next(z[':answer/value'] for z in nf[':answer-field/choices'] if z[':answer/id']==nf[':answer-field/correct'][1]);assert match(convert(designated),convert(of[':answer-field/correct'][':answer/value']));counts['source_keys']+=1
   else:assert ':answer-field/correct' not in nf;counts['source_missing_keys']+=1
 independent=json.loads((D/'supplemental-independent-inventory.json').read_text())['questions']
 for item in independent:
  q=copy.deepcopy(item['record']);q[':question/difficulty']=q[':question/difficulty'][':db/ident']
  for f in q[':question/answer-fields']:
   f[':answer-field/type']=f[':answer-field/type'][':db/ident']
   if ':answer-field/correct' in f:f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
  check({'question':q,'generation':{'source_question':None,'evidence_only':False}})
 counts['independent_supplement_records']=len(independent)
 samples=json.loads((R/'qa'/f'{K}-sampled.json').read_text())
 for z in samples:check(z)
 # Read every declared authored-E dimension triple with scaffold present.
 for a in range(1,5):
  for b in range(1,5):
   for c in range(1,5):check(g.generate('easy',parameters=dict(r=a,k=b,c=c)))
 mutant=copy.deepcopy(samples[0]);old=mutant['question'][':question/problem'];replacement=old.replace(r'\begin{bmatrix}',r'\begin{bmatrix}0 & ',1);mutant['question'][':question/problem']=replacement;assert old!=replacement;saved=copy.deepcopy(counts)
 try:check(mutant)
 except AssertionError:pass
 else:raise AssertionError('Incorrect printed matrix row width survived unchanged answer')
 counts=saved;counts.update(status='passed',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),unchanged_key_wrong_printed_matrix_shape_rejected=True,database_writes=0)
 (R/'qa'/f'{K}-root-readback.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
