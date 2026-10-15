"""Independent printed-content oracle; source evidence, identities, mutation, native tests."""
import sys
sys.dont_write_bytecode=True
import copy,hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
spec=importlib.util.spec_from_file_location('private_perp_generator',H.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y=g.parser.SYMS['x'],g.parser.SYMS['y'];parse=g.parser.parse

def save(n,v):(H/n).write_text(json.dumps(v,indent=2,default=str)+'\n')
def poly(t):
 l,r=t.replace('&','').split('=');return sp.Poly(sp.expand(parse(l)-parse(r)),x,y)
def norm(t):
 e=poly(t);a=e.coeff_monomial(x);b=e.coeff_monomial(y);c=e.coeff_monomial(1);assert e.total_degree()==1 and (a or b);k=a or b;return tuple(sp.cancel(z/k) for z in (a,b,c))
def read_prompt(q):
 text=q[':question/problem'];assert 'perpendicular' in text
 pts=[tuple(map(int,z)) for z in re.findall(r'\((-?\d+),\s*(-?\d+)\)',text)];u,v=pts[0]
 if 'line passing through the points' in text:
  (u1,v1),(u2,v2)=pts[1:];a=v2-v1;b=u1-u2;c=-(a*u1+b*v1)
 else:
  math=text.split('perpendicular to ',1)[1].split('$')[1].rstrip('.?');e=poly(math);a=e.coeff_monomial(x);b=e.coeff_monomial(y);c=e.coeff_monomial(1)
 assert a and b
 return u,v,sp.Rational(-a,b),-c/b

def check(r):
 q=r['question'];s=r['generation']['template'];u,v,m1,refb=read_prompt(q);m=-1/m1;b=v-m*u;f=q[':question/answer-fields'][0];bank=f[':answer-field/choices'];blank=f[':answer-field/type'].endswith('/blank');target=norm('y='+g.tex(m*x+b));correct=f[':answer-field/correct'][1]
 assert len(bank)==(1 if blank else 5);keys=[]
 for a in bank:
  val=a[':answer/value'];e=poly('y='+val if blank else val);ok=e.as_expr().subs({x:u,y:v})==0 and e.coeff_monomial(x)+m*e.coeff_monomial(y)==0
  assert ok==(a[':answer/id']==correct),('wrong key',val,u,v,m)
  keys.append(norm('y='+val if blank else val))
 assert len(set(keys))==len(keys)
 sol=q[':question/worked-solution'];blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(blocks)==(3 if 'line passing through the points' in q[':question/problem'] else 2)
 replay=r['generation']['origin']=='normalized source replay'
 if replay:assert sol==g.fmt.normalize_prose(g.SOURCES[s][':question/worked-solution'])
 else:
  # Independent row-count expectations encode the source-specific operative stages.
  counts=[len(z.split('\\\\')) for z in blocks]
  first=4 if 'line passing through the points' in q[':question/problem'] else (2 if s=='q-237230' and r['generation']['parameters']['B']==1 else 3)
  targetrows=6 if s=='q-252524' else 7 if s=='q-23631' else 5 if s in ('q-237230','q-103449') else 4
  assert counts==([first,targetrows,4] if len(blocks)==3 else [first,targetrows]),('erased/reordered stage',counts,s)
 for bi,block in enumerate(blocks):
  prior=None
  for row in block.split('\\\\'):
   row=row.replace('&','').strip()
   if '=' not in row:continue
   lhs,rhs=row.split('=',1)
   if re.search(r'(?:_[{]?[12]|\{[xy]\}_|\bm\b)',lhs+rhs):continue
   if not lhs.strip():
    # The numeric slope chain carries forward m1 from its labeled first row.
    assert sp.simplify(parse(rhs)-m1)==0,('bad slope stage',row)
    continue
   if 'y' not in lhs+rhs:continue
   e=poly(row);expected=m1*x+refb if bi==0 and 'line passing through the points' not in q[':question/problem'] else m*x+b
   assert sp.expand(e.as_expr().subs(y,expected))==0,('bad worked equation',row,expected)
 # Independently read all stated concrete slope values.
 for val in re.findall(r'(?:given line has a slope of|perpendicular line must have a slope of) \$([^$]+)\$',sol):
  value=parse(val.rstrip(',.'));assert value in (m1,m)
 for val in re.findall(r'm\\cdot\s*\((.*?)\)=-1.*?m=(.*?)\.',sol):
  assert parse(val[0])==m1 and parse(val[1])==m
 for segment in re.findall(r'(?:pass through the point|passes through the point) \$([^$]+)\$',sol):
  pairs=re.findall(r'\((-?\d+),\s*(-?\d+)\)',segment)
  if pairs:assert tuple(map(int,pairs[-1]))==(u,v)
 # Verify each role individually for the prose form used by standard-reference sources.
 for val in re.findall(r'perpendicular line must have a slope of \$([^$]+)\$',sol):assert parse(val.rstrip(',.'))==m
 for val in re.findall(r'given line has a slope of \$([^$]+)\$',sol):assert parse(val.rstrip(',.'))==m1
 g.fmt.validate_generated_record(r)
 return True

def native(r,label):
 f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1];u,v,m1,_=read_prompt(r['question']);m=-1/m1;b=v-m*u
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'owned choice ID: actual equation truth independently checked'} for a in f[':answer-field/choices']]
  checks += [{'submitted':v,'expected':'unresolved','purpose':'malformed/foreign submission separate from owned ID grading'} for v in ['garbage','999999','00000000-0000-0000-0000-000000000000']]
 else:
  rhs=g.tex(m*x+b);checks=[{'submitted':v,'expected':e,'purpose':p} for v,e,p in [(rhs,'accepted','canonical RHS'),(str(m*x+b),'accepted','expanded equivalent RHS'),(f'({m.p}*x+({b*m.q}))/{m.q}','accepted','single fraction equivalent RHS'),(f'({m})*(x-({u}))+({v})','accepted','point-slope equivalent RHS'),('y='+rhs,'unresolved','full equation: unsupported response shape for explicit RHS-only blank'),(g.eq(-m,1,b),'unresolved','standard equation: unsupported response shape for explicit RHS-only blank'),(str(m*x+b+1),'rejected','wrong intercept'),(str(-m*x+b),'rejected','wrong perpendicular direction'),(f'({m*x+b})+0/(x-1)','unresolved','domain restriction, not a genuine global equivalent')]]
 return {'label':label,'record':r,'checks':checks}

def main():
 assert hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest()=='71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea'
 raws=[g.raw_replay(s) for s in g.SOURCES];save('raw-source-replay.json',{'questions':raws});cases=[];inputs=[];summary=[];review=[]
 for s,q in g.SOURCES.items():
  level=g.source_level(s);p=g.original(s);r=g.generate(level,0,s,p);check(r);of=q[':question/answer-fields'][0];f=r['question'][':question/answer-fields'][0];kind=f[':answer-field/type'];oldvals=of.get(':answer-field/choices',[])
  equivalent=(lambda a:norm(a[':answer/value'])) if kind.endswith('/radio') else (lambda a:parse(a[':answer/value']))
  assert sorted(map(str,map(equivalent,oldvals)))==sorted(map(str,map(equivalent,f[':answer-field/choices']))) if oldvals else s=='q-214033'
  if ':answer-field/correct' in of:
   answer=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert equivalent(answer)==equivalent(of[':answer-field/correct'])
  assert raws[list(g.SOURCES).index(s)]['question']==q
  summary.append({'source_id':s,'raw_attributes_exact':True,'raw_eligible':False,'complete_bank_matched':bool(oldvals),'matched_values':len(oldvals),'matched_distractors':max(0,len(oldvals)-1),'missing':raws[list(g.SOURCES).index(s)]['generation']['missing'],'served_origin':r['generation']['origin']})
  for i in range(3):
   out=r if i==0 else g.generate(level,2000+i,s);check(out);cases.append({'source_id':s,'difficulty':level,'template':s,'parameters':out['generation']['parameters'],'bank_profile':out['generation']['bank_profile'],'record':out,'case_role':'original parameters with explicit completion if missing' if i==0 else 'authored variant'});inputs.append(native(out,s+'-'+str(i)));review.append('## '+s+' / '+str(i)+'\n\n'+g.markdown(out))
 # Hard uses the same moderate families and workload; every family gets 3 documented instances.
 for s in [z for z in g.SOURCES if g.source_level(z)=='moderate']:
  for i in range(3):
   out=g.generate('hard',9000+i,s);check(out);cases.append({'source_id':s,'difficulty':'hard','template':s,'parameters':out['generation']['parameters'],'bank_profile':out['generation']['bank_profile'],'record':out,'case_role':'authored hard; no observed hard evidence'});inputs.append(native(out,'hard-'+s+'-'+str(i)));review.append('## Authored hard / '+s+' / '+str(i)+'\n\n'+g.markdown(out))
 counts={};coverage={};mut=[]
 for level in g.LEVELS:
  records=g.batch(level,150,8275);counts[level]=len(records);coverage[level]={'A':set(),'B':set(),'point_x':set(),'point_y':set(),'perpendicular_slope':set()}
  for r in records:
   check(r);p=r['generation']['parameters']
   for k,z in [('A','A'),('B','B'),('point_x','px'),('point_y','py')]:coverage[level][k].add(p[z])
   coverage[level]['perpendicular_slope'].add(str(sp.Rational(p['B'],p['A'])))
  inputs.extend(native(r,level+'-sample-'+str(i)) for i,r in enumerate(records[:8]))
  assert len({r['generation']['mathematical_fingerprint'] for r in records})==len(records)
 # Isolated mutations change displayed actual values, not metadata.
 base=g.generate('easy',42,'q-237232',{'A':4,'B':-3,'C':7,'px':0,'py':1})
 for name,change in [('wrong-point',lambda q:q.__setitem__(':question/problem',q[':question/problem'].replace('(0,1)','(0,2)'))),('stale-coefficient',lambda q:q.__setitem__(':question/problem',q[':question/problem'].replace('4 x','5 x'))),('perpendicular-direction',lambda q:q[':question/answer-fields'][0][':answer-field/choices'][0].__setitem__(':answer/value',r'\frac{3}{4}x+1')),('erased-equal-stage',lambda q:q.__setitem__(':question/worked-solution',q[':question/worked-solution'].replace(r' \\ y-(1) &= - \frac{3 x}{4}', '')))]:
  bad=copy.deepcopy(base);change(bad['question']);assert bad!=base,name
  try:check(bad)
  except (AssertionError,ValueError):mut.append({'mutation':name,'caught':True})
  else:raise AssertionError('uncaught mutation '+name)
 # Canonical equation comparator covers vertical/horizontal lines even outside sampled source branch.
 assert norm('x=2')==norm('2x=4') and norm('y=1')==norm('-3y=-3') and norm('x=2')!=norm('y=2')
 # Identities distinguish rendered content while collapsing scaling and irrelevant source intercept.
 p={'A':4,'B':-3,'C':7,'px':0,'py':1};a=g.generate('easy',1,'q-237232',p);z=g.generate('easy',999,'q-237232',p)
 assert a['question']==z['question']
 for changed in [dict(p,A=8,B=-6,C=14),dict(p,C=8)]:
  z=g.generate('easy',1,'q-237232',changed);assert a['generation']['mathematical_fingerprint']==z['generation']['mathematical_fingerprint'];assert a['question'][':question/id']!=z['question'][':question/id']
 # Exact 0/1 intercepts remain eligible.
 for py in (0,1):check(g.generate('easy',0,'q-237232',{'A':4,'B':-3,'C':7,'px':0,'py':py}))
 save('sourcecases.json',{'source_basis':2275,'cases':cases});save('source-replay.json',{'source_basis':2275,'sources':summary,'raw_exact':len(raws),'complete_banks':sum(bool(v['complete_bank_matched']) for v in summary),'observed_values':sum(v['matched_values'] for v in summary),'observed_distractors':sum(v['matched_distractors'] for v in summary),'ineligible_missing_evidence':sorted(g.INCOMPLETE)})
 save('native-input.json',inputs)
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(H/'native-input.json'),str(H/'native-grading.json')],check=True)
 baseline=json.loads((H/'registered-baseline.json').read_text());currentpaths=sorted([str(ROOT/'generate/scratch/17592186175924.py').replace(str(ROOT)+'/','')]+[str(p.relative_to(ROOT)) for p in (ROOT/'generate/scratch/17592186175924').rglob('*')]);assert currentpaths==baseline['paths']
 assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==v for p,v in baseline['files'].items())
 (H/'review.md').write_text('\n\n'.join(review)+'\n')
 save('validation.json',{'mathematics_passed':True,'random_distinct_records_checked':counts,'sourcecase_count':len(cases),'mutations':mut,'coverage':{l:{k:sorted(v,key=str) for k,v in z.items()} for l,z in coverage.items()},'registered_pair_immutable':True,'native_limitations':['Full equations are unsupported response shapes for RHS-only blanks; valid equivalent RHS expressions accepted.','Malformed/foreign radio entries tested separately; all owned bank IDs tested.','Rational expression with erased pole not accepted as globally equivalent; native returns unresolved.'],'no_valid_output_pruned':True})
 print('Verified',counts,'source cases',len(cases))
if __name__=='__main__':main()
