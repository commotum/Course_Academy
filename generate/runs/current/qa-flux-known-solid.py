"""Root independent divergence, volume factors, source masks and banks."""
import importlib.util,json,re,hashlib,itertools,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186133930;D=R.parents[2]/f'generate/scratch/{K}'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'divergence-readback.py','parent_known_flux');x,y,z=p.variables
def math(t):return p.scalar(t.strip().rstrip('.,'))
def equal(a,b):return s.simplify(a-b)==0
def parts(t):
 depth=0;start=0;out=[]
 for i,c in enumerate(t):
  depth+=(c in '({')-(c in ')}')
  if c=='+' and depth==0:out.append(t[start:i]);start=i+1
 return out+[t[start:]]
def volume(g):
 if g[0]=='sphere':return s.Rational(4,3)*s.pi*g[1]**3
 if g[0]=='cylinder':return s.pi*g[1]**2*g[2]
 return s.prod(g[1:])
C={k:0 for k in ('records','actual_components','formal_held_operands','individual_derivative_contributions','collected_divergences','sphere_equations','closed_plot_geometries','volume_factors','flux_rows','choices','complete_method_banks','shared_source_masks','translation_identity_checks')}
def check(rec,old):
 q=rec['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];family=rec['generation']['template'];raw=rec['generation']['evidence_only']
 form=re.search(r'\$F=(.*?)\$',prompt,re.S)[1].rstrip('.')
 if form.startswith('⟨'):cs=[math(t) for t in form[1:-1].split(r',\,')]
 else:cs=p.vector(form)
 assert len(cs)==3;ds=[s.diff(c,v) for c,v in zip(cs,(x,y,z))];div=s.expand(sum(ds));assert not div.free_symbols;C['actual_components']+=3
 equation=re.search(r'given by \$(.*?)\$',prompt)
 if equation:
  lhs,rhs=equation[1].split('=');f=math(lhs);center=[-s.diff(f,v).subs({x:0,y:0,z:0})/2 for v in (x,y,z)];radius=s.sqrt(math(rhs)-f.subs(dict(zip((x,y,z),center))));geom=('sphere',radius,tuple(center));assert radius>0 and s.expand(f-sum((v-c)**2 for v,c in zip((x,y,z),center)))==0;C['sphere_equations']+=1
 else:
  assert not raw
  asset=Path(re.search(r'!\[\]\((.*?)\)',prompt)[1]);side=json.loads(asset.with_suffix('.json').read_text());geom=tuple(side['geometry']);assert side['renderer']=='Matplotlib' and side['closed_boundary'] and asset.stat().st_size>1000
  if geom[0]=='cylinder':
   assert side['cap_count']==2 and side['face_count']==0 and geom[3] in 'xyz';dims=[geom[1]]*3;dims['xyz'.index(geom[3])]=geom[2]
   assert math(re.search(r'height \$(.*?)\$',prompt)[1])==geom[2] and math(re.search(r'radius \$(.*?)\$',prompt)[1])==geom[1]
  else:assert side['face_count']==6 and side['cap_count']==0;dims=list(geom[1:])
  assert side['dimensions']==dims and side['axis_vectors']==[[-.72,-.58],[1,-.1],[0,1.0]];C['closed_plot_geometries']+=1
 vol=volume(geom);answer=div*vol;blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);assert len(blocks)==3
 assert blocks[0]==r'{∬}_{S}F\cdot dS={∭}_{R}\text{div}\,F\,\text{d}V.'
 _,operands=p.derivative_inputs(blocks[1]);assert len(operands)==3
 for c,var,(axis,text,*_) in zip(cs,(x,y,z),operands):assert axis==str(var) and equal(math(text),c);C['formal_held_operands']+=1
 der=blocks[1].split(' & =')[1:];assert len(der)==3;middle=der[1].split(chr(92)*2)[0].strip()
 if family=='sphere_two_cancellations':
  m=re.fullmatch(r'(.*?)\+\((.*?)\)\+(.*)',middle);assert m;contributions=m.groups();assert all(ds) and equal(ds[0]+ds[1]+ds[2],div) and ds[0].has(x,y) and ds[1].has(y) and ds[2].has(x)
 else:contributions=parts(middle)
 assert len(contributions)==3
 for t,v in zip(contributions,ds):assert equal(math(t),v);C['individual_derivative_contributions']+=1
 assert equal(math(der[-1].split(r'\end{aligned}')[0]),div);C['collected_divergences']+=1
 rows=blocks[-1].split(' & =')[1:];rows=[t.split(chr(92)*2)[0].split(r'\end{aligned}')[0].strip().rstrip('.') for t in rows];assert len(rows)==5
 assert equal(math(rows[0].split(r'{∭}_{R}')[1].split(r'\,\text{d}V')[0]),div)
 fact=rows[1].split(r'{∭}_{R}')[0];assert equal(math('-1' if fact=='-' else fact),div) and rows[1].endswith(r'{∭}_{R}\,\text{d}V')
 vf=rows[2].split(r'\text{Volume}(R)');assert len(vf)==2 and not vf[1];factor=vf[0].removesuffix(r'\cdot ');assert equal(math('-1' if factor=='-' else factor),div)
 assert equal(math(rows[3]),answer) and equal(math(rows[4]),answer)
 if geom[0]=='sphere':assert r'\frac{4}{3}\pi \cdot {'+str(geom[1])+r'}^{3}' in rows[3]
 elif geom[0]=='cylinder':assert r'\pi \cdot {'+str(geom[1])+r'}^{2}\cdot '+str(geom[2]) in rows[3]
 else:assert r'\cdot '.join(map(str,geom[1:])) in rows[3]
 C['volume_factors']+=3;C['flux_rows']+=5
 for f in q[':question/answer-fields']:
  choices=f[':answer-field/choices'];vals=[math(a[':answer/value']) for a in choices];assert len(vals)==5 and all(not equal(a,b) for a,b in itertools.combinations(vals,2));assert [a[':answer/id'] for a,v in zip(choices,vals) if equal(v,answer)]==[f[':answer-field/correct'][1]]
  if geom[0]=='sphere':r=geom[1];wanted=[answer,-answer,vol,div*s.Rational(4,3)*s.pi*r*r,div*4*s.pi*r**3]
  elif geom[0]=='cylinder':r,h=geom[1:3];wanted=[answer,-answer,vol,div*s.pi*r*h,div*s.pi*r*r]
  else:a,b,c=geom[1:];wanted=[answer,-answer,vol,div*a*b,div*a*c]
  assert all(sum(equal(v,w) for w in wanted)==1 for v in vals);C['choices']+=5;C['complete_method_banks']+=1
 prose=lambda t:re.sub(r'\s+',' ',re.sub(r'!\[\]\(.*?\)|\$\$.*?\$\$|\$.*?\$','',t,flags=re.S)).strip()
 assert prose(sol)==prose(old[':question/worked-solution']);assert len(re.findall(r'\$\$',sol))==len(re.findall(r'\$\$',old[':question/worked-solution']));C['shared_source_masks']+=1;C['records']+=1
if __name__=='__main__':
 g=load(D.with_suffix('.py'),'parent_known_solid');frozen=json.load(open(R/f'sources/{K}.json'));assert json.load(open(D/'source.json'))==frozen;originals={str(q[':db/id']):q for q in frozen['record'][':knowledge-point/questions']};S=dict(prompts=0,solutions=0,fields=0,values=0,refs=0,missing_refs=0)
 for case in json.load(open(D/'source-cases.json')):
  o=originals[str(case['source_id'])];q=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])['question'];assert set(q)==set(o) and q[':question/problem']==o[':question/problem'] and q[':question/worked-solution']==o[':question/worked-solution'];S['prompts']+=1;S['solutions']+=1
  for f,of in zip(q[':question/answer-fields'],o[':question/answer-fields']):
   assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);S['fields']+=1;S['values']+=len(of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
   if ':answer-field/correct' in of:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];S['refs']+=1
   else:S['missing_refs']+=1
 records=json.load(open(R/f'qa/{K}-sampled.json'))
 for name,level in g.TEMPLATES.items():records.extend(g.generate(level,seed=seed,template=name) for seed in (917,631))
 for rec in records:
  old=g.SPECS[rec['generation']['template']]['source'] if rec['generation']['template'] in g.SPECS else g.SPECS['q-162580']['source'];check(rec,old)
  if rec['generation']['geometry'][0]=='sphere':
   params=dict(rec['generation']['parameters']);geom=list(params['geometry']);geom[2]=[-v if v else 0 for v in geom[2]];params['geometry']=geom;other=g.generate(rec['question'][':question/difficulty'].rsplit('/',1)[1],template=rec['generation']['template'],parameters=params);assert other['generation']['mathematical_fingerprint']==rec['generation']['mathematical_fingerprint'];C['translation_identity_checks']+=1
 out=dict(status='passed',source=S,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
