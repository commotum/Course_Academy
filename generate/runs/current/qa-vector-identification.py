"""Root actual signatures/components, full categorical banks and stated real domains."""
import json,re,sys,hashlib,importlib.util,itertools
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186172085;D=ROOT/f'generate/scratch/{K}'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);sys.modules[name]=m;z.loader.exec_module(m);return m
base=load(R/'qa-parametric-scalar-line.py','identification_base');p=load(R/'vector-math-parser.py','identification_parent');labels={'I only':{0},'II only':{1},'III only':{2},'I and II only':{0,1},'I and III only':{0,2},'II and III only':{1,2},'I, II, and III':{0,1,2}}
C={k:0 for k in ('records','signatures','components','categorical_choices','whole_banks','solution_verdicts','stated_domain_points','declared_coordinate_mismatches')}
def condition(raw):
 raw=raw.replace(r'\,','').strip();match=re.search(r'\\ne|\\ge|\\le|[><]',raw);assert match,(raw,'relation');l,h=p.scalar(raw[:match.start()]),p.scalar(raw[match.end():]);op=match[0];return {r'\ne':s.Ne,r'\ge':s.Ge,r'\le':s.Le,'>':s.Gt,'<':s.Lt}[op](l,h)
def check(rec):
 q=rec['question'];text=q[':question/problem'];sol=q[':question/worked-solution'];forms=re.findall(r'^- \$(.*?)\$$',text,re.M);assert len(forms)==3;valid=set();data=[]
 for idx,raw in enumerate(forms):
  m=re.match(r'([A-Z])\(([^)]+)\)=(.*)',raw);assert m;name,coords,expr=m.groups();coords=coords.split(',');C['signatures']+=1
  if expr.startswith('⟨'):components=[p.scalar(z) for z in expr[1:-1].replace(r'\,','').split(',')]
  else:
   whole=s.expand(p.scalar(expr));components=[whole.coeff(z) for z in (p.i,p.j,p.k)];assert s.expand(whole-sum(c*z for c,z in zip(components,(p.i,p.j,p.k))))==0
   if components[2]==0:components=components[:2]
  if len(coords)==len(components)==2:valid.add(idx)
  data.append((name,coords,components));C['components']+=len(components)
  declared={p.locals_[z] for z in coords};assert set.union(set(),*(e.free_symbols for e in components))<=declared
  if len(coords)!=len(set.union(set(),*(e.free_symbols for e in components))):C['declared_coordinate_mismatches']+=1
 f=q[':question/answer-fields'][0];vs=[a[':answer/value'] for a in f[':answer-field/choices']];assert len(vs)==5 and len(set(vs))==5 and all(v in labels for v in vs);correct=[a[':answer/id'] for a in f[':answer-field/choices'] if labels[a[':answer/value']]==valid];assert correct==[f[':answer-field/correct'][1]];C['categorical_choices']+=5;C['whole_banks']+=1
 conclusion=re.search(r'Therefore, the correct answer is "(.*?)\."',sol)[1];assert labels[conclusion]==valid
 bullets=sol.split('\n\n- ')[1:];assert len(bullets)==3
 for idx,((name,coords,components),bullet) in enumerate(zip(data,bullets)):
  sig=name+'('+','.join(coords)+')';assert '$'+sig+'$' in bullet,(sig,bullet);assert ('*not* a vector field' in bullet)==(idx not in valid);C['solution_verdicts']+=1
  if idx not in valid:continue
  domains=re.findall(r'S=\\\{.*?\\,\|\\,?\s*(.*?)\\\}',bullet,re.S)
  if not domains:domains=re.findall(r'S=\\\{.*?\|\\,?\s*(.*?)\\\}',bullet,re.S)
  conditions=[] if not domains else [condition(v) for v in domains[0].split(',') if v.strip() and v.strip()!=chr(92)]
  # Every elementary domain restriction comes from the actual printed components.
  restrictions=[]
  for expr in components:
   denominator=s.denom(expr)
   if denominator!=1:restrictions.append(s.Ne(denominator,0))
   for log in expr.atoms(s.log):restrictions.append(s.Gt(log.args[0],0))
   for power in expr.atoms(s.Pow):
    if power.exp.is_Rational and power.exp.q%2==0:restrictions.append(s.Ge(power.base,0))
  assert bool(conditions)==bool(restrictions),(sig,domains,restrictions)
  for xx,yy in itertools.product(range(-5,6),repeat=2):
   sub={p.x:xx,p.y:yy};actual=all(bool(v.subs(sub)) for v in restrictions);stated=all(bool(v.subs(sub)) for v in conditions);assert actual==stated,(sig,xx,yy,restrictions,conditions);C['stated_domain_points']+=1
 C['records']+=1
if __name__=='__main__':
 g=load(D.with_suffix('.py'),'root_identification_gen');source=base.raw(g,K,D);records=json.loads((R/f'qa/{K}-sampled.json').read_text())
 for fam,lev in g.TEMPLATES.items():records.append(g.generate(lev,template=fam,seed=622))
 for rec in records:check(rec)
 out=dict(status='passed',source=source,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
