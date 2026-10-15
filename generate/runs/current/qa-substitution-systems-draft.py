"""Root readback of displayed substitution systems, complete banks and operative stages."""
import importlib.util,json,hashlib,re,sys,copy
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;ROOT=R.parents[2];D=ROOT/'generate/scratch/17592186073752-draft'
def mod(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
g=mod('root_substitution_generator',D.with_suffix('.py'));p=mod('root_substitution_parser',R/'ode-scalar-parser.py');x,y=p.x,p.y
SHA=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest();n={'records':0,'choices':0,'operative_equations':0,'substitution_transitions':0,'printed_systems':0,'source_values':0,'source_keys':0,'source_solutions':0};tasks={z:set() for z in ['easy','moderate','hard']}
def stripped(t):return re.sub(r'\\[a-zA-Z]+(?:\{(?:aligned|cases)\})?','',t)
def expr(t,names):
 mp=dict(zip(names,('x','y')));chunks=re.split(r'(\\[a-zA-Z]+)',t.replace('&','').strip().rstrip('.,:'))
 return p.scalar(''.join(z if z.startswith('\\') else re.sub('[a-z]',lambda m:mp.get(m[0],m[0]),z) for z in chunks))
def group_rows(text):
 return [re.split(r'\\\\',m) for m in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',text,re.S)]
def eq(row,names):
 parts=row.replace('&','').strip().rstrip('.,:').split('=');assert len(parts)==2,row;return s.expand(expr(parts[0],names)-expr(parts[1],names))
def check(r):
 q=r['question'];pr=q[':question/problem'];sol=q[':question/worked-solution'];systems=re.findall(r'\\left\\\{\\begin\{aligned\}(.*?)\\end\{aligned\}\\right\.',pr+'\n'+sol,re.S)
 if systems:rows=re.split(r'\\\\',systems[0])
 else:rows=[v.rstrip('.,') for v in re.findall(r'\$([^$]*=[^$]*)\$',pr)[:2]]
 assert len(rows)==2,rows
 letters=set(re.findall('[a-z]',stripped(' '.join(rows))));assert len(letters)==2,letters;names=tuple(sorted(letters));eqs=[eq(z,names) for z in rows]
 M,v=s.linear_eq_to_matrix(eqs,(x,y));assert M.det()!=0;answer=M.inv()*v;subs={x:answer[0],y:answer[1]};n['printed_systems']+=1
 diff=re.search(r'value of \$([a-z])\s*-\s*([a-z])\$',pr)
 fs=sorted(q[':question/answer-fields'],key=lambda f:f[':answer-field/key'])
 if diff:wants=[subs[(x,y)[names.index(diff[1])]]-subs[(x,y)[names.index(diff[2])]]]
 elif 'cakes' in pr:wants=[subs[(x,y)[names.index(z)]] for z in ('n','y')]
 elif 'Mary and Sam' in pr:wants=[subs[(x,y)[names.index(z)]] for z in ('t','d')]
 else:
  tup=re.search(r'\$\(([a-z]),\s*([a-z])\)',pr);order=tup.groups() if tup else names
  wants=[subs[(x,y)[names.index(z)]] for z in order]
 assert len(fs)==len(wants)
 for f,want in zip(fs,wants):
  values=[expr(a[':answer/value'],names) for a in f[':answer-field/choices']];assert len(values)==len(set(values));truth=[s.simplify(z-want)==0 for z in values];assert sum(truth)==1,(r['generation'],pr,values,want)
  assert next(a[':answer/id'] for a,t in zip(f[':answer-field/choices'],truth) if t)==f[':answer-field/correct'][1]
  if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in pr
  n['choices']+=len(values)
 groups=group_rows(sol);residualgroups=[]
 for rows in groups:
  lhs=None;residuals=[]
  for row in rows:
   parts=[z.replace('&','').strip().rstrip('.,:') for z in row.split('=')];assert len(parts)>=2,row
   if not parts[0]:parts[0]=lhs
   lhs=parts[0];vals=[expr(z,names) for z in parts];rr=[]
   for a,b in zip(vals,vals[1:]):
    residual=s.expand(a-b);assert s.simplify(residual.subs(subs))==0,(row,subs);n['operative_equations']+=1;rr.append(residual)
    if len(residual.free_symbols)==1:var=next(iter(residual.free_symbols));assert s.solve(residual,var)==[subs[var]]
   residuals.append(rr[0])
  residualgroups.append(residuals)
  for previous,current in zip(residuals,residuals[1:]):
   removed=previous.free_symbols-current.free_symbols
   if len(previous.free_symbols)==2 and len(current.free_symbols)==1 and len(removed)==1:
    var=next(iter(removed));isolated=[z for e in eqs for z in s.solve(e,var)]+[subs[var]];assert any(s.expand(previous.subs(var,z)-current)==0 for z in isolated),(r['generation']['template'],previous,current,isolated);n['substitution_transitions']+=1
 # All standalone equations and final coordinate conclusions are read separately.
 for display,inline in re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',sol,re.S):
  block=display or inline
  if '=' not in block or '\\begin' in block:continue
  for part in re.split(r',\\,',block):
   if '=' not in part:continue
   vals=[expr(z,names) for z in part.strip().rstrip('.,:').split('=')];assert all(s.simplify((vals[0]-z).subs(subs))==0 for z in vals[1:]),block
 name=r['generation']['template'];sizes=[len(z) for z in groups]
 expected={'coefficient_b_first':[2,6,2],'coefficient_a_first':[2,6,2],'tuple_xy':[6,2],'direct_pq':[2,4],'difference_ab':[2,6,2],'unit_pair':[2,6,2],'preisolated_uv':[5,3],'isolate_xy':[5,4],'cake_context':[9,1],'meeting_context':[2,7,3]}
 assert sizes==expected[name],(name,sizes)
 # Preserve algebraic expansion and collection, including both coefficients, before solving.
 ix=1 if name.startswith('coefficient') or name in ('difference_ab','unit_pair','direct_pq','meeting_context') else 0
 rs=residualgroups[ix]
 if name not in ('direct_pq','cake_context','meeting_context'):
  assert s.expand(rs[1]-rs[2])==0
  if name not in ('preisolated_uv','isolate_xy'):assert s.expand(rs[2]-rs[3])==0
 grade=q.get(':question/difficulty','authored/unrated');level=(grade.get(':db/ident') if isinstance(grade,dict) else grade).rsplit('/',1)[1];tasks.setdefault(level,set()).add(tuple(map(str,answer)));n['records']+=1
for row in json.loads((D/'native-input.json').read_text()):check(row['record'])
for template,(level,kind) in g.TEMPLATES.items():
 for seed in range(8):check(g.generate(level,seed=seed+300,template=template))
# Frozen MA full source banks and shared solution wording, normalized presentation separately.
from scripts.question_capture.math_format import normalize_prose
sources=json.loads((D/'source-cases.json').read_text());replay=json.loads((D/'source-replay.json').read_text())
for row,r in zip(sources,replay):
 o=row['record'];q=r['question'];assert len(o[':question/answer-fields'])==len(q[':question/answer-fields'])
 for of,f in zip(sorted(o[':question/answer-fields'],key=lambda z:z[':answer-field/key']),sorted(q[':question/answer-fields'],key=lambda z:z[':answer-field/key'])):
  ov=[expr(z[':answer/value'],()) for z in of.get(':answer-field/choices',[])];gv=[expr(z[':answer/value'],()) for z in f[':answer-field/choices']]
  if ov:assert sorted(ov,key=str)==sorted(gv,key=str);n['source_values']+=len(ov)
  if ':answer-field/correct' in of:assert expr(of[':answer-field/correct'][':answer/value'],())==expr(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]),());n['source_keys']+=1
 if o.get(':question/worked-solution'):
  a=normalize_prose(o[':question/worked-solution']);b=normalize_prose(q[':question/worked-solution']);canon=lambda z:re.sub(r'\s|&|\\left|\\right','',z)
  # One documented source delimiter repair is separate from exact source wording.
  if row['source_id']=='q-166843':
   assert a.count('is $$')==1;a=a.replace('is $$','is $');n['source_solution_presentation_repairs']=1
  assert canon(a)==canon(b),(row['source_id'],'source solution wording');n['source_solutions']+=1
saved_counts=dict(n)
mut=copy.deepcopy(g.generate('moderate',seed=13));mut['question'][':question/worked-solution']=mut['question'][':question/worked-solution'].replace(' & =',' & =1+',1)
try:check(mut)
except AssertionError:pass
else:raise AssertionError('unchanged-key bad worked row escaped root reader')
n=saved_counts
assert hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest()==SHA
out={'status':'passed','script_sha256':SHA,'independent_readback':n,'distinct_sampled_coordinate_pairs_by_level':{k:len(v) for k,v in tasks.items()},'negative_controls':1,'limits':'Coordinate counts describe root sample only, not global capacity; empirical source distractor intent unresolved and raw omitted context remains evidence-only.'}
(R/'qa/17592186073752-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
