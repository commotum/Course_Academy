import sys
sys.dont_write_bytecode=True
import json,re,hashlib,copy,importlib.util
from pathlib import Path
R=Path(__file__).resolve().parent;K=17592186100870;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=load('parent_dimension_polynomials',R/'variable-matrix-scalar.py');s=p.s
counts=dict(records=0,supplied_dimensions=0,answer_values=0,annotated_factor_dimensions=0,normal_complete_banks=0,source_values=0,source_fields=0,source_keys=0,source_missing_keys=0,source_solutions=0,raw_known_factor_label_errors=0)
def same(a,b):return s.expand(a-b)==0
def balanced(text,start):
 assert text[start]=='{';depth=1;i=start+1
 while depth:
  assert i<len(text)
  if text[i]=='{':depth+=1
  elif text[i]=='}':depth-=1
  i+=1
 return text[start+1:i-1],i

def dimension(text):
 parts=re.split(r'\\(?:times|cdot)\s*',text);assert len(parts)==2,text
 return tuple(p.scalar(z.replace(r'\left','').replace(r'\right','')) for z in parts)
def equal(a,b):return a==b if isinstance(a,str) or isinstance(b,str) else len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
def answer(z):return 'undefined' if 'undefined' in z.lower() else dimension(z)
def prompt(text):
 supplied={name:dimension(shape) for name,shape in re.findall(r'\$([A-Z])\$ is a\s*\$(.*?)\$ matrix',text)};assert len(supplied)==2,text
 islands=re.findall(r'(?<!\$)\$(?!\$)(.*?)\$',text,re.S);target=next(t.strip('?. ') for t in islands if re.fullmatch(r'[A-Z]{2}[?.]?',t));assert all(c in supplied for c in target)
 return supplied,target

def annotations(solution):
 found=[]
 for mt in re.finditer(r'\{([A-Z]{1,2})\}_\{',solution):
  body,end=balanced(solution,mt.end()-1)
  # Remove only semantic box/text wrappers; preserve whole affine components.
  while (m:=re.search(r'\\(?:boxed|text)\{',body)):
   inside,close=balanced(body,m.end()-1);body=body[:m.start()]+inside+body[close:]
  found.append((mt[1],dimension(body)))
 assert len(found)==3,(solution,found);return found

def check(record,raw_case=None):
 q=record['question'];supplied,target=prompt(q[':question/problem']);A,B=(supplied[z] for z in target);assert same(A[1],B[0]);expected=(A[0],B[1]);counts['supplied_dimensions']+=4
 for f in q[':question/answer-fields']:
  vals=[answer(z[':answer/value']) if f[':answer-field/type'].endswith('/radio') else p.scalar(z[':answer/value']) for z in f[':answer-field/choices']]
  wanted=expected if f[':answer-field/type'].endswith('/radio') else expected[int(f[':answer-field/key'][-1])-1]
  good=[equal(v,wanted) if isinstance(v,(str,tuple)) else same(v,wanted) for v in vals];assert sum(good)==1
  if ':answer-field/correct' in f:assert good[next(i for i,z in enumerate(f[':answer-field/choices']) if z[':answer/id']==f[':answer-field/correct'][1])]
  if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
  else:
   for i,a in enumerate(vals):assert all(not equal(a,b) for b in vals[:i])
   if record['generation']['bank_profile']=='method-derived':
    m,n,k=A[0],A[1],B[1];bank=[(m,k),(k,m),(m,n),(n,k),'undefined'];assert all(sum(equal(a,b) for b in bank)==1 for a in vals);counts['normal_complete_banks']+=1
  counts['answer_values']+=len(vals)
 if ':question/worked-solution' in q:
  text=q[':question/worked-solution'];ann=annotations(text)
  if raw_case=='q-70702':
   assert ann[0][0]==target[1] and ann[1][0]==target[0] and ann[2][0]==target;counts['raw_known_factor_label_errors']+=1
  else:assert [z[0] for z in ann]==[*target,target]
  for (_,actual),want in zip(ann,[A,B,expected]):assert equal(actual,want)
  counts['annotated_factor_dimensions']+=6
  # The prose comparison must name the actual ordered factors and inner dimension.
  cmp=re.search(r'\$([^$]+)\$ columns? in \$([A-Z])\$ and \$([^$]+)\$ rows? in \$([A-Z])\.?\$',text);assert cmp,(text,A,target)
  assert same(p.scalar(cmp[1]),A[1]) and same(p.scalar(cmp[3]),B[0]) and cmp[2]+cmp[4]==target
  assert '$'+target+'$ is a $' in text
 counts['records']+=1

def prose(text):return re.sub(r'\$\$.*?\$\$|(?<!\$)\$(?!\$).*?(?<!\$)\$(?!\$)','[MATH]',text,flags=re.S)
if __name__=='__main__':
 g=load('parent_given_dimensions',D.with_suffix('.py'));source=json.loads((R/'refresh-2026-10-14/sources'/f'{K}.json').read_text());assert source==json.loads((D/'source.json').read_text());originals={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
 for case in json.loads((D/'source-cases.json').read_text()):
  r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['profile']);q=r['question'];old=originals[case['source_id']];check(r,case['source_id'])
  assert prompt(old[':question/problem'])==prompt(q[':question/problem']) and prose(old[':question/problem'])==prose(q[':question/problem'])
  for key in (':question/worked-solution',':question/difficulty'):assert (key in old)==(key in q)
  if ':question/worked-solution' in old:assert prose(old[':question/worked-solution'])==prose(q[':question/worked-solution']);counts['source_solutions']+=1
  assert {z[':answer-field/key'] for z in old[':question/answer-fields']}=={z[':answer-field/key'] for z in q[':question/answer-fields']}
  for of in old[':question/answer-fields']:
   nf=next(z for z in q[':question/answer-fields'] if z[':answer-field/key']==of[':answer-field/key'])
   assert of[':answer-field/key']==nf[':answer-field/key'] and of[':answer-field/type'][':db/ident']==nf[':answer-field/type'];convert=answer if nf[':answer-field/type'].endswith('/radio') else p.scalar;remaining=[convert(z[':answer/value']) for z in nf[':answer-field/choices']]
   for z in of[':answer-field/choices']:
    wanted=convert(z[':answer/value']);found=[i for i,a in enumerate(remaining) if equal(a,wanted) if isinstance(a,(str,tuple))] if isinstance(wanted,(str,tuple)) else [i for i,a in enumerate(remaining) if same(a,wanted)];assert len(found)==1;remaining.pop(found[0]);counts['source_values']+=1
   assert not remaining;counts['source_fields']+=1
   if ':answer-field/correct' in of:
    actual=convert(next(z[':answer/value'] for z in nf[':answer-field/choices'] if z[':answer/id']==nf[':answer-field/correct'][1]));wanted=convert(of[':answer-field/correct'][':answer/value']);assert equal(actual,wanted) if isinstance(actual,(str,tuple)) else same(actual,wanted);counts['source_keys']+=1
   else:assert ':answer-field/correct' not in nf;counts['source_missing_keys']+=1
 supplement=json.loads((D/'supplement-reconciliation.json').read_text())
 for item in supplement['later_independent_additions']['questions']:check(item['record'])
 counts['independent_supplement_records']=len(supplement['later_independent_additions']['questions'])
 samples=json.loads((R/'qa'/f'{K}-sampled.json').read_text())
 for r in samples:check(r)
 mutant=copy.deepcopy(next(r for r in samples if ':question/worked-solution' in r['question']));text=mutant['question'][':question/worked-solution'];ann=annotations(text);label=ann[0][0];mutant['question'][':question/worked-solution']=text.replace('{'+label+'}_','{Z}_',1);assert text!=mutant['question'][':question/worked-solution'];saved=copy.deepcopy(counts)
 try:check(mutant)
 except AssertionError:pass
 else:raise AssertionError('Incorrect ordered factor label survived unchanged key')
 counts=saved;counts.update(status='passed',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),unchanged_key_wrong_factor_label_rejected=True,database_writes=0)
 (R/'qa'/f'{K}-root-readback.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
