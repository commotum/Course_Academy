"""Root independent actual field, complete region/bank and solution readback."""
import importlib.util,json,re,hashlib,itertools,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186133929;D=R.parents[2]/f'generate/scratch/{K}'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'divergence-readback.py','parent_flux_components');x,y,z=p.variables
def math(t):return p.scalar(t.strip().rstrip('.,'))
def equal(a,b):return s.expand(a-b)==0
def group(t,pos):
 assert t[pos]=='{';start=pos+1;depth=1;pos+=1
 while depth:depth+=(t[pos]=='{')-(t[pos]=='}');pos+=1
 return t[start:pos-1],pos
def integral(t):
 t=t.strip().rstrip('.,');pos=0;bounds=[]
 for _ in range(3):
  assert t[pos:].startswith(r'{\int }_');pos+=len(r'{\int }_');a,pos=group(t,pos);assert t[pos]=='^';b,pos=group(t,pos+1);bounds.append((math(a),math(b)))
 assert t[pos:].startswith(r'\,');pos+=2;end=t.index(r'\,\text{d}',pos);f=math(t[pos:end]);axes=re.findall(r'\\text\{d\}([xyz])',t[end:]);assert len(axes)==3 and len(set(axes))==3
 return f,tuple((dict(zip('xyz',(x,y,z)))[v],a,b) for v,(a,b) in zip(reversed(axes),bounds))
def value(obj):
 f,bounds=obj
 for v,a,b in reversed(bounds):f=s.integrate(f,(v,a,b))
 return s.expand(f)
def same(a,b):return equal(a[0],b[0]) and len(a[1])==len(b[1]) and all(v==w and equal(l,m) and equal(u,n) for (v,l,u),(w,m,n) in zip(a[1],b[1]))
def terms(t):
 depth=0;start=0;out=[]
 for i,c in enumerate(t):
  depth+=(c in '({')-(c in ')}')
  if c=='+' and depth==0:out.append(t[start:i]);start=i+1
 return out+[t[start:]]
C={k:0 for k in ('records','actual_components','held_partial_operands','individual_derivative_terms','collected_divergences','plane_surface_bounds','worked_region_bounds','worked_complete_integrals','displayed_choices','complete_method_banks','shared_source_prose','scope_checks')}
def check(rec,original):
 q=rec['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];level=q[':question/difficulty'].rsplit('/',1)[1];f=q[':question/answer-fields'][0];cs=p.field(prompt);assert cs is not None;ds=[s.diff(a,v) for a,v in zip(cs,p.variables)];d=s.expand(sum(ds));C['actual_components']+=3
 eqs=re.findall(r'\$([xyz])=(.*?)\$',prompt.split('Given that')[0]);assert len(eqs)==6
 bounds=[]
 for i in range(0,6,2):
  a,b=eqs[i:i+2];assert a[0]==b[0];bounds.append((dict(zip('xyz',(x,y,z)))[a[0]],math(a[1]),math(b[1])))
 assert len(set(a[0] for a in bounds))==3;expected=(d,tuple(bounds));C['plane_surface_bounds']+=6
 blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);assert len(blocks)==(3 if level=='easy' else 5)
 assert blocks[0]==r'{∬}_{S}F\cdot dS={∭}_{R}\text{div}\,F\,\text{d}V.'
 der=blocks[1];_,ops=p.derivative_inputs(der);assert len(ops)==3
 for var,c,(axis,t,*_) in zip(p.variables,cs,ops):assert axis==str(var) and equal(math(t),c);C['held_partial_operands']+=1
 rows=der.split(' & =')[1:];assert len(rows)==3
 raw=rows[1].split(chr(92)*2)[0].strip();summands=terms(raw);assert len(summands)==3
 for t,v in zip(summands,ds):assert equal(math(t),v);C['individual_derivative_terms']+=1
 assert equal(math(rows[2].split(r'\end{aligned}')[0]),d);C['collected_divergences']+=1
 for triple in re.findall(r'\{∭\}_\{R\}(.*?)\\,\\text\{d\}V',sol):
  if triple!=r'\text{div}\,F':assert equal(math(triple),d)
 if level!='easy':
  assert '\\{' in blocks[3] and '\\}' in blocks[3]
  inequalities=blocks[3].split(r'\,:\,')[1].removesuffix(r'\}.').split(r',\,');assert len(inequalities)==3
  for raw,(axis,a,b) in zip(inequalities,bounds):
   left,v,right=raw.split(r'\le ');assert v==str(axis) and equal(math(left),a) and equal(math(right),b);C['worked_region_bounds']+=2
  assert 'type '+{x:'II',y:'III',z:'I'}[bounds[-1][0]]+' solid' in sol
 last=re.search(r'(\{\\int \}_.*?)\.\\end\{aligned\}',blocks[-1])[1];assert same(integral(last),expected);C['worked_complete_integrals']+=1
 choices=f[':answer-field/choices'];assert len(choices)==5
 if level=='easy':
  vals=[math(a[':answer/value']) for a in choices];valid=[a[':answer/id'] for a,t in zip(choices,vals) if equal(t,d)]
  nz=[i for i,t in enumerate(ds) if t!=0];i,j=nz[:2];want=[d,d-ds[i],d-ds[j],d-ds[i]+cs[i],sum(cs)]
  assert all(sum(equal(v,w) for w in want)==1 for v in vals)
 else:
  objs=[integral(a[':answer/value']) for a in choices];vals=[value(a) for a in objs];valid=[a[':answer/id'] for a,t in zip(choices,objs) if same(t,expected)]
  axis,lo,hi=bounds[-1];nonzero=[t for t in ds if t!=0];wrong=d-nonzero[0] if len(nonzero)>1 else sum(s.diff(t,axis) for t in cs)
  if equal(wrong,d):wrong=sum(cs)
  zeros={w:0 for w,_,_ in bounds[:-1]};flat=(lo,hi.subs(zeros)) if hi.free_symbols else (lo.subs(zeros),hi)
  specs=[(d,lo,hi),(wrong,lo,hi),(d,hi,lo),(d,*flat),(wrong,hi,lo)]
  wanted=[(expr,tuple(bounds[:-1])+((axis,l,h),)) for expr,l,h in specs]
  assert all(sum(same(obj,w) for w in wanted)==1 for obj in objs)
 assert valid==[f[':answer-field/correct'][1]] and all(not equal(a,b) for a,b in itertools.combinations(vals,2));C['displayed_choices']+=5;C['complete_method_banks']+=1
 if original and ':question/worked-solution' in original:
  prose=lambda t:re.sub(r'\s+',' ',re.sub(r'\$\$.*?\$\$|\$.*?\$','',t,flags=re.S)).strip()
  assert prose(sol)==prose(original[':question/worked-solution']);C['shared_source_prose']+=1
 assert 'Volume' not in sol and '=' not in blocks[-1].split(r'\end{aligned}')[0].split(r'\text{d}')[-1];C['scope_checks']+=1;C['records']+=1
if __name__=='__main__':
 g=load(D.with_suffix('.py'),'parent_flux_setup');frozen=json.load(open(R/f'sources/{K}.json'));assert json.load(open(D/'source.json'))==frozen;originals={q[':question/math-academy-id']:q for q in frozen['record'][':knowledge-point/questions']};S=dict(prompts=0,solutions=0,fields=0,values=0,refs=0,missing_refs=0)
 for case in json.load(open(D/'source-cases.json')):
  o=originals[case['source_id']];q=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])['question'];assert {k for k in q if k.startswith(':question/')}=={k for k in o if k.startswith(':question/')};assert q[':question/problem']==o[':question/problem'];S['prompts']+=1
  if ':question/worked-solution' in o:assert q[':question/worked-solution']==o[':question/worked-solution'];S['solutions']+=1
  for f,of in zip(q[':question/answer-fields'],o[':question/answer-fields']):
   assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);S['fields']+=1;S['values']+=len(of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
   if ':answer-field/correct' in of:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];S['refs']+=1
   else:S['missing_refs']+=1
 records=json.load(open(R/f'qa/{K}-sampled.json'))
 for t,c in g.CONFIG.items():records.extend(g.generate(c['level'],seed=seed,template=t) for seed in (719,941))
 for rec in records:
  ids=rec['generation']['source_ids'];check(rec,originals.get(ids[0]) if ids else None)
 result=dict(status='passed',source=S,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
