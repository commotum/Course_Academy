"""Independent integer arithmetic on rendered prompts and actual learner grading."""
import copy,hashlib,importlib.util,json,re,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('matrix_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(n,x):(HERE/n).write_text(json.dumps(x,indent=2,default=str)+'\n')
def mul(a,b):return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def printed(text):
 out=[]
 for body in g.MATRIX.findall(text):
  rows=[]
  for row in re.split(r'\\\\',body):
   values=[]
   for cell in row.split('&'):
    t=cell.replace(r'\cdot','*').strip();assert re.fullmatch(r'[\d\s()+*\-]+',t),t
    # Restricted integer arithmetic, no names or executable code.
    values.append(int(g.sp.sympify(t)))
   rows.append(values)
  out.append(rows)
 return out

def check(r):
 q=r['question'];meta=r['generation'];t=meta['template'];src=g.TEMPLATES[t]
 assert r['knowledge_point']['db_id']==g.KP_ID
 assert q[':question/difficulty']==src[':question/difficulty'][':db/ident']
 A,B,C=printed(q[':question/problem']);p=dict(zip('ABC',(A,B,C)));g.domain(t,p)
 assert p==meta['parameters']
 AB=mul(A,B);BC=mul(B,C);R=mul(AB,C);assert R==mul(A,BC)
 left='product $AB$' in src[':question/worked-solution'];seq=printed(q[':question/worked-solution'])
 expected=[A,B,AB,AB,C,R] if left else [B,C,BC,A,BC,R]
 if t=='q-320021':expected[2:2]=[AB,AB]
 if t=='q-319943':expected[2:2]=[BC]
 assert seq==expected,(t,seq,expected)
 # Read answer positions directly from placeholders, requiring the original layout.
 assert re.findall(r'\{\{(field-\d+)\}\}',q[':question/problem'])==['field-'+str(i+1) for i in range(len(R)*len(R[0]))]
 flat=sum(R,[]);fs=sorted(q[':question/answer-fields'],key=lambda f:f[':answer-field/key'])
 assert len(fs)==len(flat) and len({f[':answer-field/id'] for f in fs})==len(fs)
 for i,f in enumerate(fs):
  assert f[':answer-field/key']=='field-'+str(i+1) and f[':answer-field/type']==':answer-field.type/blank'
  assert len(f[':answer-field/choices'])==1
  a=f[':answer-field/choices'][0];assert a[':answer/value']==str(flat[i]) and a[':answer/type']==':answer.type/math'
  assert f[':answer-field/correct']==[':answer/id',a[':answer/id']]
  assert a[':answer/id']==g.uid(f[':answer-field/id'],'answer:'+a[':answer/value'])
 assert meta['mathematical_fingerprint']==g.fingerprint(q)
 assert q[':question/id']==g.uid(g.KP_UUID,'matrix-triple:'+g.fingerprint(q))
 assert r==g.generate(q[':question/difficulty'].split('/')[-1],meta['seed'],t,p)
 return R

def native(label,r):
 checks=[]
 for i,f in enumerate(r['question'][':question/answer-fields']):
  a=f[':answer-field/choices'][0];n=a[':answer/value']
  for value,expect,purpose in [(n,'accepted','correct integer'),('('+n+')+0','accepted','equivalent arithmetic'),(str(int(n)+1),'rejected','off-by-one')]:
   checks.append({'field_index':i,'submitted':value,'expected':expect,'purpose':purpose})
 return {'label':label,'record':r,'checks':checks}

def main():
 replay=[];records=[];coverage={};boundaries=[]
 for t,src in g.TEMPLATES.items():
  level=src[':question/difficulty'][':db/ident'].split('/')[-1];p=g.parameters(src);r=g.generate(level,0,t,p);check(r)
  assert r['question'][':question/problem']==src[':question/problem']
  assert r['question'][':question/worked-solution']==src[':question/worked-solution'],t
  got={f[':answer-field/key']:f[':answer-field/choices'][0][':answer/value'] for f in r['question'][':question/answer-fields']}
  expected={f[':answer-field/key']:f[':answer-field/correct'][':answer/value'] for f in src[':question/answer-fields']}
  assert got==expected
  replay.append({'source':t,'complete_fields_matched':len(got),'total_fields':len(expected),'complete_banks_matched':len(got),'source_distractors':0,'prompt_and_solution_exact':True})
  records.append(native('source-'+t,r));sample=[]
  for seed in range(150):
   r=g.generate(level,seed,t);check(r);sample.append(r);records.append(native(t+'-'+str(seed),r))
  covered=[]
  fixed={(k,i,j) for k in 'BC' for i,row in enumerate(p[k]) for j,v in enumerate(row) if t=='q-320017' and j==2} # B col 3; C row 3 handled below
  if t=='q-320017':fixed={('B',0,2),('B',1,2),('C',2,0)}
  else:fixed=set()
  for k in 'ABC':
   for i,row in enumerate(p[k]):
    for j,value in enumerate(row):
     if (k,i,j) in fixed:continue
     vals=sorted({r['generation']['parameters'][k][i][j] for r in sample})
     assert all(v in vals for v in range(-6,7)),(t,k,i,j,vals)
     for v in (-7,0,7):
      changed=copy.deepcopy(p);changed[k][i][j]=v;r=g.generate(level,0,t,changed);check(r)
      boundaries.append({'template':t,'slot':[k,i,j],'value':v,'passed':True})
     covered.append({'slot':[k,i,j],'sampled_values':vals})
  coverage[t]={'variable_slots':covered,'fixed_slots':[list(x) for x in sorted(fixed)],'fixed_role':'All entries of ABC requested; dimensions fixed to preserve grouping and workload; no independently variable targets.'}
 # Validate all source matrix products and record defective fields, preserving them.
 source_audit=[]
 for t,q in g.SOURCES.items():
  A,B,C=printed(q[':question/problem']);R=mul(mul(A,B),C);issues=[]
  fs=q[':question/answer-fields'];keys=[f[':answer-field/key'] for f in fs]
  if len(set(keys))!=len(keys):issues.append('Duplicate field key; source excluded from inventory validation')
  if ':question/difficulty' not in q:issues.append('Unrated')
  if not q.get(':question/worked-solution'):issues.append('Missing worked solution')
  for f in fs:
   c=f.get(':answer-field/correct')
   if not c:issues.append('Missing correct-answer link');continue
   if f[':answer-field/type'][':db/ident'].endswith('/radio'):
    assert printed(c[':answer/value'])==[R],t
    vals=[printed(a[':answer/value']) if 'bmatrix' in a[':answer/value'] else int(a[':answer/value']) for a in f[':answer-field/choices']]
    assert sum(x==[R] for x in vals)==1
  source_audit.append({'source':t,'id':q[':db/id'],'result':R,'issues':issues,'radio_generation':'Excluded: literal source banks retained; error transformations unresolved' if any(f[':answer-field/type'][':db/ident'].endswith('/radio') for f in fs) else None})
 save('source-replay.json',replay);save('source-mathematics.json',source_audit);save('slot-coverage.json',coverage);save('boundaries.json',boundaries)
 save('native-input.json',records)
 subprocess.run([str(HERE/'check-engine'),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
 previews=[]
 for level in g.LEVELS:previews+=g.fresh(level,12,1930)
 for r in previews:check(r)
 save('previews.json',previews)
 # Side-by-side examples retain source solution stages and show changed coefficients.
 md=[]
 for t,src in g.TEMPLATES.items():
  level=src[':question/difficulty'][':db/ident'].split('/')[-1];r=g.generate(level,1930,t);check(r)
  md+=['## '+t,'### Source',src[':question/problem'],src[':question/worked-solution'],'### Variant',r['question'][':question/problem'],r['question'][':question/worked-solution']]
 (HERE/'review.md').write_text('\n\n'.join(md)+'\n')
 files=[HERE.with_suffix('.py'),HERE/'source.json',HERE/'validate.py',HERE/'previews.json',HERE/'native-report.json']
 save('validation.json',{'passed':True,'templates':len(g.TEMPLATES),'sampled_instances':900,'source_replay_complete':True,'fidelity':'Exact prompt, solution and all blank answer banks for six source questions','correctness':'Independent integer matrix multiplication on rendered prompts; associative products equal; every rendered intermediate and answer checked','grading':'Real course_academy_engine::learning::grade_field; correct and equivalent accepted, incorrect rejected','boundaries':len(boundaries),'coverage':coverage,'radio_generation_supported':False,'hard_supported':False,'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}})
 print('Validated six source blank templates, 900 sampled variants, boundaries, and actual learner grading.')
if __name__=='__main__':main()
