"""Root pointwise surface integrands, held partials, every minor and pullback."""
import json,re,sys,hashlib,importlib.util,itertools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186172130;D=R.parents[2]/f'generate/scratch/{K}'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','surface_setup_parent');x,y,z,u,v=p.x,p.y,p.z,p.u,p.v
def math(raw):return p.scalar(raw.strip().rstrip('.,'))
def vec(raw):
 raw=raw.strip().rstrip('.,');assert raw.startswith('⟨') and raw.endswith('⟩');return s.Matrix([math(t) for t in raw[1:-1].split(r',\,')])
def displays(text):return re.findall(r'\$\$\s*(.*?)\s*\$\$',text,re.S)
def rows(text):return [t.strip().removesuffix(r'\end{aligned}').strip().rstrip('.,') for t in text.split(' & =')[1:]]
def eq(a,b,domain):
 diff=s.expand(a-b)
 if diff==0:return True
 if domain:diff=diff.subs(domain,s.Symbol('restricted',nonnegative=True))
 return s.simplify(diff)==0
C={k:0 for k in ('records','actual_coordinates','actual_functions','hint_metrics','formal_partials','held_coordinate_operands','derivative_components','cross_input_matrices','cofactor_minors','norm_stages','pullback_stages','coordinate_restrictions','final_integrands','choices','whole_banks','source_structure_checks')}
def check(rec,originals):
 q=rec['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];family=rec['generation']['template'];level=q[':question/difficulty'].rsplit('/',1)[1]
 F=math(re.search(r'\$f\(x,y,z\)=(.*?)\$',prompt)[1]);coords=vec(displays(prompt)[1].split('=',1)[1]);ru,rv=coords.diff(u),coords.diff(v);cross=ru.cross(rv);square=s.expand(cross.dot(cross));norm=s.sqrt(square);pull=s.expand(F.subs(dict(zip((x,y,z),coords)),simultaneous=True));answer=pull*norm
 restrictions=re.findall(r'Assume \$([uv])\\geq0\.\$',prompt);assert len(restrictions)<=1;domain={'u':u,'v':v}.get(restrictions[0]) if restrictions else None
 C['actual_coordinates']+=3;C['actual_functions']+=1;blocks=displays(sol);old=originals['mixed' if family=='mixed_hard' else family];oldblocks=displays(old[':question/worked-solution']);assert len(blocks)==len(oldblocks)
 assert re.sub(r'\$\$.*?\$\$|\$.*?\$','[MATH]',sol,flags=re.S)==re.sub(r'\$\$.*?\$\$|\$.*?\$','[MATH]',old[':question/worked-solution'],flags=re.S)
 if level=='easy':
  hint=math(re.search(r'‖\{r\}_\{u\}\^\{′\}\\times \{r\}_\{v\}\^\{′\}‖=(.*?)\.\$\*',prompt)[1]);assert eq(hint,norm,domain);assert eq(math(blocks[1].split('=',1)[1]),norm,domain);C['hint_metrics']+=2
 else:
  der=rows(blocks[1]);assert len(der)==6
  for offset,var,wanted in ((0,u,ru),(3,v,rv)):
   formal=der[offset].removesuffix(r'\\').strip();assert formal=='⟨'+r',\,'.join(r'\frac{∂'+str(a)+'}{∂'+str(var)+'}' for a in (x,y,z))+'⟩';C['formal_partials']+=3
   operated=der[offset+1].removesuffix(r'\\').strip();operands=re.findall(r'\\frac\{∂\}\{∂([uv])\}\((.*?)\)(?=,\\,|⟩)',operated);assert len(operands)==3
   for (axis,raw),coordinate in zip(operands,coords):assert axis==str(var) and eq(math(raw),coordinate,domain);C['held_coordinate_operands']+=1
   actual=vec(der[offset+2].removesuffix(r'\\').strip());assert actual==wanted;C['derivative_components']+=3
  matrices=re.findall(r'\|\\begin\{aligned\}(.*?)\\end\{aligned\}\|',blocks[2],re.S);assert len(matrices)==4
  parsed=[[row.strip().split('&') for row in m.split(r'\\')] for m in matrices];assert [a.strip() for a in parsed[0][0]]==['i','j','k'];assert s.Matrix([[math(a) for a in row] for row in parsed[0][1:]])==s.Matrix([list(ru),list(rv)]);C['cross_input_matrices']+=1
  for raw,(i,j) in zip(parsed[1:],((1,2),(0,2),(0,1))):assert s.Matrix([[math(a) for a in row] for row in raw])==s.Matrix([[ru[i],ru[j]],[rv[i],rv[j]]]);C['cofactor_minors']+=1
  assert vec(rows(blocks[2])[-1])==cross
  normrows=rows(blocks[3]);assert len(normrows)==len(rows(oldblocks[3]));assert vec(normrows[0][1:-1].removesuffix(r'\\').strip())==cross
  for raw in normrows[1:]:assert eq(math(raw.removesuffix(r'\\').strip()),norm,domain);C['norm_stages']+=1
  if family in ('fold','plane','cylinder'):assert '+' in normrows[2] and normrows[2].startswith(r'\sqrt{')
 pb=next(b for b in blocks if b.startswith(r'\begin{aligned}f(r(u,v))'));stages=rows(pb);assert len(stages)==len(rows(next(b for b in oldblocks if b.startswith(r'\begin{aligned}f(r(u,v))'))))
 function,substitutions=stages[0].removesuffix(r'\\').strip().split(r'\,{|}_{');assert eq(math(function),F,domain)
 for raw,axis,coordinate in zip(substitutions.removesuffix('}').split(r'\,'),(x,y,z),coords):
  lhs,rhs=raw.split('=');assert lhs==str(axis) and eq(math(rhs),coordinate,domain);C['coordinate_restrictions']+=1
 for raw in stages[1:]:assert eq(math(raw.removesuffix(r'\\').strip()),pull,domain);C['pullback_stages']+=1
 if family=='cancel':assert '(u-v^{2})+v^{2}' in stages[1]
 if family=='product':assert '(u+v)' in stages[1] and stages[1].count(r'\cdot')>=2
 if family=='powers':assert stages[1].count(r'\cdot')>=3
 if family in ('mixed','mixed_hard'):assert r'^{2}\cdot (' in stages[1]
 if family=='cylinder':assert r'(v^{2}\cdot v^{2})' in stages[1]
 final=rows(blocks[-1]);assert len(final)==2 and 'f(r(u,v))' in final[0];raw=re.search(r'\{∬\}_\{D\}\\,(.*?)\\,\\,\\text\{d\}A',final[1])[1];assert eq(math(raw),answer,domain);C['final_integrands']+=1
 f=q[':question/answer-fields'][0];values=[math(a[':answer/value']) for a in f[':answer-field/choices']];assert len(values)==5 and all(not eq(a,b,domain) for a,b in itertools.combinations(values,2));assert [a[':answer/id'] for a,val in zip(f[':answer-field/choices'],values) if eq(val,answer,domain)]==[f[':answer-field/correct'][1]]
 parts=s.Add.make_args(pull)
 if family=='plane':
  fx,fy=F.coeff(x,2),F.coeff(y,2);wanted=[answer,pull,fx*coords[0]**2*norm,pull.subs(u,v)*norm,(fx*coords[0]**2+fy*v*v)*norm]
 elif len(parts)>1:wanted=[answer,pull,(pull-parts[0])*norm,(pull-2*parts[0])*norm,pull*square]
 else:wanted=[answer,pull,pull*norm/u,pull*norm/v,pull*square]
 assert all(sum(eq(val,t,domain) for t in wanted)==1 for val in values);C['choices']+=5;C['whole_banks']+=1;C['records']+=1;C['source_structure_checks']+=1
 if family=='mixed_hard':assert s.diff(coords[2],u)!=0 and s.degree(coords[2],v)==2 and len(s.Add.make_args(cross[1]))==2 and len(s.Add.make_args(pull))==3
if __name__=='__main__':
 g=load(D.with_suffix('.py'),'root_surface_setup');originals={name:q for name,q in g.BY_NAME.items()};source=dict(prompts=0,solutions=0,fields=0,values=0,refs=0,missing_refs=0)
 frozen=json.load(open(R/f'sources/{K}.json'));assert json.load(open(D/'source.json'))==frozen
 for case in json.load(open(D/'source-cases.json')):
  q=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])['question'];o=next(o for o in frozen['record'][':knowledge-point/questions'] if o[':db/id']==case['source_id'])
  assert q[':question/problem']==o[':question/problem'] and q[':question/worked-solution']==o[':question/worked-solution'];source['prompts']+=1;source['solutions']+=1
  for f,of in zip(q[':question/answer-fields'],o[':question/answer-fields']):
   assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);source['fields']+=1;source['values']+=len(of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
   if ':answer-field/correct' in of:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];source['refs']+=1
   else:source['missing_refs']+=1
 records=json.load(open(R/f'qa/{K}-sampled.json'))
 for family,level in g.LEVELS.items():records.append(g.generate(level,seed=753,template=family))
 for rec in records:check(rec,originals)
 out=dict(status='passed',source=source,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
