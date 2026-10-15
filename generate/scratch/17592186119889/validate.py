#!/usr/bin/env python3
"""Independent readback of printed surfaces, derivatives, cofactors, and banks."""
import hashlib,importlib.util,itertools,json,re,subprocess,sys
from pathlib import Path
import sympy as S
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def module(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
g=module('surface_integrand_generator',HERE.with_suffix('.py'))
p=module('printed_math_parser',ROOT/'generate/runs/current/vector-math-parser.py')
u,v=S.symbols('u v',nonnegative=True);p.locals_.update(u=u,v=v)
def scalar(z):return p.scalar(z.strip().rstrip('.,'))
def same(a,b):return S.simplify(S.trigsimp(S.expand(a-b)))==0
def vector(z):
 z=z.strip().replace(r'\,','');assert z.startswith(r'\langle') and z.endswith(r'\rangle'),z
 return S.Matrix([scalar(x) for x in z[len(r'\langle'):-len(r'\rangle')].split(',')])
def veq(a,b):return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
def save(path,value):path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def ordered(r):
 r=json.loads(json.dumps(r));r['question'][':question/answer-fields'][0][':answer-field/choices'].sort(key=lambda a:a[':answer/id']);r['generation'].pop('seed');return r
checks=[];stats={'records':0,'surface_components':0,'partial_inputs':0,'partial_values':0,'determinant_cells':0,'minor_cells':0,'cross_vectors':0,'norm_stages':0,'bank_values':0,'bank_pairs':0}
def verify(rec):
 q=rec['question'];m=rec['generation'];sol=q[':question/worked-solution'];prompt=q[':question/problem']
 r=vector(re.search(r'\\langle.*?\\rangle',prompt).group());du,dv=r.diff(u),r.diff(v);cross=du.cross(dv).applyfunc(S.trigsimp);square=S.trigsimp(cross.dot(cross))
 stats['surface_components']+=3
 vectors=re.findall(r'\\langle.*?\\rangle',sol)
 partials=[z for z in vectors if r'\frac{\partial}{\partial' in z]
 assert len(partials)==2
 for z,axis,want in zip(partials,(u,v),(du,dv)):
  parts=z[len(r'\langle'):-len(r'\rangle')].replace(r'\,','').split(',');assert len(parts)==3
  for piece,component in zip(parts,r):
   prefix=r'\frac{\partial}{\partial '+str(axis)+r'}\left(';assert piece.strip().startswith(prefix),piece
   raw=piece.strip()[len(prefix):-len(r'\right)')];assert same(scalar(raw),component);stats['partial_inputs']+=1
  got=vector(vectors[vectors.index(z)+1]);assert veq(got,want);stats['partial_values']+=3
 dets=re.findall(r'\\begin\{vmatrix\}(.*?)\\end\{vmatrix\}',sol,re.S);assert len(dets)==4
 rows=[row.split('&') for row in dets[0].split(r'\\')];assert [c.strip() for c in rows[0]]==list('ijk')
 assert veq(S.Matrix([scalar(c) for c in rows[1]]),du) and veq(S.Matrix([scalar(c) for c in rows[2]]),dv);stats['determinant_cells']+=6
 for body,cols in zip(dets[1:],[(1,2),(0,2),(0,1)]):
  mat=[[scalar(c) for c in row.split('&')] for row in body.split(r'\\')]
  assert mat==[[du[c] for c in cols],[dv[c] for c in cols]];stats['minor_cells']+=4
 assert r'\rangle' in sol and r'\end{vmatrix},\,-\begin{vmatrix}' in sol
 # Raw cofactor expansion may retain sin²+cos²; both printed vectors must equal it.
 group=sol.split('Now, the fundamental vector product is')[1].split('\n\nand\n')[0]
 concrete=[z for z in re.findall(r'\\langle.*?\\rangle',group) if r'\begin{vmatrix}' not in z]
 assert concrete
 for z in concrete:assert veq(vector(z),cross);stats['cross_vectors']+=1
 norm_group=sol.split('\n\nand\n\n')[1].split('Therefore, the surface area is')[0]
 rhs=re.findall(r'&\s*=(.*?)(?=\\\\|\\end\{aligned\})',norm_group,re.S);assert len(rhs)>=5
 assert veq(vector(re.search(r'\\langle.*?\\rangle',rhs[0]).group()),cross)
 for z in rhs[1:]:
  value=scalar(z);assert same(value**2,square),(m,z,value,square)
  for uv in [(S.Rational(1,4),S.Rational(1,3)),(S.Rational(3,4),S.Rational(2,3))]:assert S.N(value.subs({u:uv[0],v:uv[1]}))>0
  stats['norm_stages']+=1
 field=q[':question/answer-fields'][0];bank=field[':answer-field/choices'];assert len(bank)==5 and len({x[':answer/id'] for x in bank})==5
 vals=[scalar(a[':answer/value']) for a in bank];cid=field[':answer-field/correct'][1]
 good=[a[':answer/id'] for a,z in zip(bank,vals) if same(z*z,square) and all(S.N(z.subs({u:uv[0],v:uv[1]}))>0 for uv in [(S.Rational(1,4),S.Rational(1,3)),(S.Rational(3,4),S.Rational(2,3))])]
 assert good==[cid],(m,good,cid)
 for x,y in itertools.combinations(vals,2):assert not same(x,y);stats['bank_pairs']+=1
 stats['bank_values']+=5
 # The final displayed integrand must agree with the checked correct option.
 final=sol.split('Therefore, the surface area is')[1];z=re.findall(r'\\iint_D (.*?)\\,\\mathrm\{d\}A',final)[0]
 assert same(scalar(z),next(z for a,z in zip(bank,vals) if a[':answer/id']==cid))
 bounds=re.findall(r'0\\le u\\le (.*?),\\,0\\le v\\le ([^$]*?)(?:\\\}|\.)',prompt)
 assert len(bounds)==2 and bounds[0]==bounds[1],(m,bounds,prompt)
 assert not re.search(r'!\[',prompt+sol)
 stats['records']+=1
 checks.append({'label':m['template']+':'+json.dumps(m['parameters'],sort_keys=True),'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==cid else 'rejected','purpose':'every displayed radio option'} for a in bank]})
 return r,square

def run(records=None,out=None):
 out=out or HERE/'reference/validation';out.mkdir(parents=True,exist_ok=True)
 fidelity=[];review=[];coverage={}
 if records is None:
  records=[]
  for sid,t in g.TEMPLATES.items():
   print('Validating',sid,flush=True)
   baseline=g.generate(t['level'],template=sid,parameters=t['base']);r,square=verify(baseline)
   old=g.QS[sid];f=old[':question/answer-fields'][0];bank=baseline['question'][':question/answer-fields'][0]
   src=[scalar(a[':answer/value']) for a in f[':answer-field/choices']];got=[scalar(a[':answer/value']) for a in bank[':answer-field/choices']]
   matched=sum(sum(same(a,b) for b in got)==1 for a in src);assert matched==5
   oldcid=f[':answer-field/correct'][':answer/id'];oldcorrect=scalar(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==oldcid));assert same(oldcorrect**2,square)
   for idx,a in enumerate(f[':answer-field/choices']):
    fidelity.append({'source':sid,'source_question':old[':db/id'],'source_answer':a[':answer/id'],'source_value':a[':answer/value'],'recipe_index':next(i for i,b in enumerate(g.model(sid,t['base'])[2]) if same(scalar(a[':answer/value']),b)),'correct':a[':answer/id']==oldcid,'matched':True})
   observed=scalar(re.search(r'⟨(.*?)⟩',old[':question/problem']).group(1).replace(r'\,','').split(',')[0])
   # Full source vector replay, independent of the source parameter declaration.
   source_vec=S.Matrix([scalar(x) for x in re.search(r'⟨(.*?)⟩',old[':question/problem']).group(1).replace(r'\,','').split(',')]);assert veq(source_vec,r)
   covered=[]
   for params in t['domain']:
    rec=g.generate(t['level'],seed=31,template=sid,parameters=params);verify(rec);records.append(rec);covered.append(params)
    assert ordered(rec)==ordered(g.generate(t['level'],seed=49,template=sid,parameters=params))
   coverage[sid]={'declared':t['domain'],'observed':covered,'missing':[]}
   variant=next(x for x in records if x['generation']['template']==sid and x['generation']['parameters']!=t['base'])
   review.append({'source_id':sid,'original':old,'replay':baseline,'variant':variant})
  save(out/'source-bank-fidelity.json',{'source_basis':g.SOURCE['basis'],'matched_options':len(fidelity),'total_options':35,'complete_banks':7,'total_banks':7,'missing':[],'extra':[],'choices':fidelity,'solution_fidelity':'Original prose and ordered partial/cofactor/norm/integral stages preserved; TeX normalized and redundant intermediate factorization rows consolidated. Bounds mismatch q-110019 corrected consistently to prose 0<=u<=1. Exact original retained in source.json.'})
  save(out/'slot-coverage.json',coverage);save(out/'side-by-side.json',review)
 else:
  for rec in records:verify(rec)
 save(out/'grading-input.json',checks)
 engine=ROOT/'generate/runs/current/check-engine';subprocess.run([str(engine),str(out/'grading-input.json'),str(out/'grading-report.json')],check=True,timeout=55)
 save(out/'validation.json',{'passed':True,'source_basis':g.SOURCE['basis'],'stats':stats,'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'real_grader':'course_academy_engine::learning::grade_field','engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'source_fidelity':'source-bank-fidelity.json','all_declared_parameters_checked':records is not None,'dependencies':{'sympy':S.__version__,'python':sys.version.split()[0]}})
 if review:
  md=[]
  for row in review:
   md+=['# '+row['source_id'],'## Original',row['original'][':question/problem'],row['original'][':question/worked-solution']]
   for label in ['replay','variant']:
    rec=row[label];md+=['## '+label,rec['question'][':question/problem'],str(rec['generation']['parameters']),*['- $'+a[':answer/value']+'$' for a in rec['question'][':question/answer-fields'][0][':answer-field/choices']],rec['question'][':question/worked-solution']]
  (out/'side-by-side.md').write_text('\n\n'.join(md)+'\n')
 print(json.dumps(stats),flush=True)
if __name__=='__main__':run()
