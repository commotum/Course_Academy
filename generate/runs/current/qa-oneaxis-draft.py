"""Root reads all 39 draft one-axis matrices, ordered complete banks and source omissions."""
import sys,re,json,hashlib,importlib.util
from pathlib import Path
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
def load(file,name):
 z=importlib.util.spec_from_file_location(name,file);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','scalar')
n=dict(records=0,choices=0,solution_rows=0,source_prompts=0,source_values=0,source_solutions=0,source_refs=0,whole_method_banks=0)
def arrays(text):
 pattern=r'([A-Z])\s*=\s*(?:\\begin\{bmatrix\}([\s\S]*?)\\end\{bmatrix\}|\[\\begin\{aligned\}([\s\S]*?)\\end\{aligned\}\]|\[([^\[\]]+)\])';found=[]
 for m in re.finditer(pattern,text):
  rows=[z.split('&') for z in (m[2] or m[3] or m[4]).split(r'\\')];assert len(set(map(len,rows)))==1
  for row in rows:
   for cell in row:assert p.scalar(cell).is_real
  found.append((m[1],len(rows),len(rows[0])))
 assert len(found)==1;return found[0]
def pair(text):
 m=re.fullmatch(r'(\d+)\s*\\(?:times|cdot)\s*(\d+)\.?',text.strip());assert m,text;return int(m[1]),int(m[2])
def check(rec):
 q=rec['question'];meta=rec['generation'];name,r,c=arrays(q[':question/problem']);forms=[]
 if meta['eligible_for_learning']:
  level=q[':question/difficulty'].split('/')[-1]
  lo,hi={'easy':(1,5),'moderate':(6,12),'hard':(13,20)}[level]
  assert min(r,c)==1 and lo<=max(r,c)<=hi
 for f in q[':question/answer-fields']:
  radio=f[':answer-field/type'].endswith('/radio');vs=[pair(a[':answer/value']) if radio else int(a[':answer/value']) for a in f[':answer-field/choices']];assert len(set(vs))==len(vs);expected=(r,c) if radio else r if f[':answer-field/key']=='field-1' else c;assert vs.count(expected)==1
  if ':answer-field/correct' in f:assert vs[next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])]==expected
  else:assert meta['evidence_only'] and not meta['eligible_for_learning']
  if not radio:assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
  if meta['eligible_for_learning'] and radio:
   size=max(r,c);wanted={(1,1),(0,1),(1,0),(0,0),(2,2)} if r==c else {(r,c),(c,r),(size,size),(r,c-1) if r==1 else (r-1,c),(r,c+1) if r==1 else (r+1,c)};assert set(vs)==wanted;n['whole_method_banks']+=1
  n['choices']+=len(vs)
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];m=re.search(r'The matrix \$([A-Z])\$ has \$(\d+)\$ rows?\s+and \$(\d+)\$ columns?',sol);assert m and (int(m[2]),int(m[3]))==(r,c)
  assert m[1]==name;assert pair(re.search(r'dimensions are\s+\$(.*?)\$',sol)[1])==(r,c);n['solution_rows']+=1
 n['records']+=1;return r,c
if __name__=='__main__':
 kp=17592186087694;D=R.parents[2]/'generate/scratch'/f'{kp}-draft';g=load(D.with_suffix('.py'),'generator');src=json.load(open(D/'source.json'));assert src==json.load(open(R/'sources'/f'{kp}.json'));old={q[':question/math-academy-id']:q for q in src['record'][':knowledge-point/questions']}
 for c in json.load(open(D/'source-cases.json')):
  rec=g.generate(c['level'],template=c['template'],profile=c.get('bank_profile',c.get('profile')),parameters=c['parameters']);check(rec);q=rec['question'];o=old[c['source_id']]
  for key in (':question/problem',':question/worked-solution',':question/difficulty'):
   assert (key in q)==(key in o)
   if key in o:assert q[key]==(o[key][':db/ident'] if key.endswith('difficulty') else o[key])
  fs={f[':answer-field/key']:f for f in q[':question/answer-fields']}
  for of in o[':question/answer-fields']:
   f=fs[of[':answer-field/key']];assert f[':answer-field/type']==of[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
   if ':answer-field/correct' in of:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];n['source_refs']+=1
   n['source_values']+=len(f[':answer-field/choices'])
  n['source_prompts']+=1;n['source_solutions']+=int(':question/worked-solution' in o)
 review=json.load(open(D/'review.json')); items=review['original_replays']+review['generated_variants'] if isinstance(review,dict) else review
 for item in items:check(item.get('record',item))
 levels={level:[(1,n) for n in range(lo,hi+1)]+[(n,1) for n in range(max(2,lo),hi+1)] for level,(lo,hi) in {'easy':(1,5),'moderate':(6,12),'hard':(13,20)}.items()}
 for level,pairs in levels.items():
  for r,c in pairs:
   params={'name':'W','entries':[[str((i+j)%9) for j in range(c)] for i in range(r)]}
   for template in ('aligned_radio','double_blank'):assert check(g.generate(level,template=template,parameters=params))==(r,c)
 n['exhaustive_meaningful_domains']={level:len(pairs) for level,pairs in levels.items()};n['union']=39
 (R/'qa'/f'{kp}-draft-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
