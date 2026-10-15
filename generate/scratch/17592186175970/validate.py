"""Independent printed-expression validation, full bank replay, actual grading."""
import hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
from functools import lru_cache
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('elliptic',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
t=sp.Symbol('t',real=True);x,y,z=sp.symbols('x y z',real=True)
def save(name,obj):(HERE/name).write_text(json.dumps(obj,indent=2)+'\n')
@lru_cache(maxsize=20000)
def read(value):
 value=value.replace('\\\\','\\').replace('\u2061','')
 value=re.sub(r'\\(?:operatorname|mathrm)\{(cosh|sinh|cos|sin|tan)\}',r'\1',value)
 value=re.sub(r'\\(cosh|sinh|cos|sin|tan)\b',r'\1',value)
 value=value.replace(r'\left','').replace(r'\right','').replace(r'\,','')
 def group(start):
  assert value[start]=='{'
  depth=1;end=start+1
  while depth:
   depth+=(value[end]=='{')-(value[end]=='}');end+=1
  return value[start+1:end-1],end
 while r'\frac' in value or r'\dfrac' in value:
  cmd=r'\dfrac' if r'\dfrac' in value else r'\frac'
  start=value.index(cmd);numer,end=group(start+len(cmd));denom,end=group(end)
  value=value[:start]+'(('+numer+')/('+denom+'))'+value[end:]
 value=value.replace('{','(').replace('}',')').replace('^','**')
 value=re.sub(r'(cosh|sinh|cos|sin|tan)\s*t\b',r'\1(t)',value)
 return parse_expr(value,local_dict={'t':t,'x':x,'y':y,'z':z,'cos':sp.cos,'sin':sp.sin,'cosh':sp.cosh,'sinh':sp.sinh,'tan':sp.tan},transformations=standard_transformations+(implicit_multiplication_application,))
@lru_cache(maxsize=2000)
def equation(s):
 # Expand nested powers before simple fraction conversion.
 s=s.replace('^{2}','^2').replace('{x}','x').replace('{y}','y').replace('{z}','z')
 left,right=s.split('=');return sp.expand(read(left)-read(right))
def check_math(r):
 q=r['question'];p=r['generation']['parameters'];a,b=p['a'],p['b'];plane=p['plane'];target=p['target'];u=next(c for c in 'xyz' if c not in plane)
 prompt=q[':question/problem'];line=re.search(r'f\(t,([xyz])\)=⟨(.*?)⟩',prompt)[2].split(r',\,');assert len(line)==3
 index=next(i for i,c in enumerate(line) if '_____' in c);wanted='xyz'.index(plane[0] if target=='cos' else plane[1]);assert index==wanted
 ordinal=['first','second','third'][index];assert f'What is the {ordinal} component' in prompt
 supplied={c:read(line[i]) for i,c in enumerate('xyz') if i!=index}
 assert supplied[u]==sp.Symbol(u,real=True)
 other=plane[1] if target=='cos' else plane[0]
 assert supplied[other]==(b*sp.sin(t) if target=='cos' else a*sp.cos(t))
 eq=equation(prompt.split('coordinates as $')[1].split('$')[0].rstrip('.'))
 v,w=[sp.Symbol(c,real=True) for c in plane]
 expected=v*v/(a*a)+w*w/(b*b)-1
 ratio=sp.cancel(eq/expected);assert ratio.is_number and ratio>0
 f=q[':question/answer-fields'][0];bank=f[':answer-field/choices'];assert len(bank)==5 and f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
 values=[read(c[':answer/value']) for c in bank];assert len(set(values))==5
 correct=a*sp.cos(t) if target=='cos' else b*sp.sin(t)
 assert sum(val==correct for val in values)==1
 idx=values.index(correct);assert f[':answer-field/correct'][1]==bank[idx][':answer/id']
 # Verify the entire parametrization against the printed Cartesian equation.
 assignments={v:a*sp.cos(t),w:b*sp.sin(t)}
 assert sp.trigsimp(eq.subs(assignments))==0
 for val in values:
  altered=assignments.copy();altered[sp.Symbol('xyz'[index],real=True)]=val
  residual=eq.subs(altered)
  if val==correct:assert sp.trigsimp(residual)==0
  else:
   assert any(residual.subs({t:angle,sp.Symbol(u,real=True):free}).equals(0) is False for angle,free in [(0,0),(0,1),(sp.pi/4,0),(sp.pi/4,1)]),(val,residual)
 solution=q[':question/worked-solution']
 assert f'in the ${plane}$-plane' in solution
 assert f'Therefore, the {ordinal} component of $f$ is $' in solution
 printed_answer=solution.rsplit('is $',1)[1].split('$')[0];assert read(printed_answer)==correct
 full=re.search(r'f\(t,'+u+r'\)=⟨x,y,z⟩=⟨(.*?)⟩',solution)[1].split(r',\,')
 assert [read(c) for c in full]==[assignments.get(c,c) for c in (x,y,z)]
 assert rf'\frac{{({g.tex(a*sp.cos(t))})^2}}{{{a*a}}}' in solution
 assert rf'\frac{{({g.tex(b*sp.sin(t))})^2}}{{{b*b}}}' in solution
 assert r'\cos^2 t+\sin^2 t' in solution and r'\in[0,2\pi)' in solution
 assert g.digest(g.task(p))==r['generation']['mathematical_fingerprint']
 return r
def check(r):
 m=r['generation'];level=r['question'][':question/difficulty'].split('/')[-1]
 assert r['knowledge_point']['db_id']==g.KP_ID
 expected=g.generate(level,m['seed'],parameters=m['parameters'],profile=m['bank_profile'],replay=m['evidence_only'])
 assert r==expected,'Stable identity/content/replay mismatch'
 return check_math(r)
def native(label,r):
 f=r['question'][':question/answer-fields'][0]
 return {'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'all options through actual learner grader'} for a in f[':answer-field/choices']]}
def fingerprint(q):
 sid=q.get(':question/math-academy-id')
 if sid in g.PROFILES:
  c=g.PROFILES[sid];return g.digest(g.task(c))
 if sid=='q-167887':return g.digest([3,3,'xy','cos'])
 if sid and sid.startswith('e-'):return g.digest([2,4,'xy','cos'])
 prompt=q[':question/problem'];m=re.search(r'f\(t,([xyz])\)=⟨(.*?)⟩',prompt);assert m
 parts=m[2].split(r',\,');index=next(i for i,v in enumerate(parts) if '_____' in v);eq=equation(prompt.split('coordinates as $')[1].split('$')[0].rstrip('.'))
 variables=[v for v in (x,y,z) if eq.has(v)];assert len(variables)==2
 c0=eq.subs({x:0,y:0,z:0});aa=sp.sqrt(-c0/eq.coeff(variables[0],2));bb=sp.sqrt(-c0/eq.coeff(variables[1],2))
 return g.digest([int(aa),int(bb),''.join(map(str,variables)),'cos' if str(variables[0])=='xyz'[index] else 'sin'])
def main():
 originals={q[':question/math-academy-id']:q for q in g.SNAPSHOT['record'][':knowledge-point/questions']};inputs=[];replays=[];review=[];extraction=[]
 for profile,c in g.PROFILES.items():
  p={k:c[k] for k in ('a','b','plane','target')};r=check(g.generate(c['level'],parameters=p,profile=profile,replay=True));old=originals[profile];f=old[':question/answer-fields'][0]
  observed=[read(a[':answer/value']) for a in f[':answer-field/choices']];made=[read(a[':answer/value']) for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
  assert len(set(observed))==len(observed)==5 and set(observed)==set(made)
  if ':answer-field/correct' in f:assert read(f[':answer-field/correct'][':answer/value'])==read(next(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'] if a[':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1]))
  replays.append({'source':profile,'matched_values':5,'matched_distractors':4,'complete_bank':True,'missing_or_extra':[],'key_origin':'source' if ':answer-field/correct' in f else 'derived; absent in source','original_difficulty':old.get(':question/difficulty'),'notation_normalization':'Captured legacy double backslashes normalized; operatorname and unicode application normalized for comparison','solution_correction':'first substituted denominator 5 -> 25' if profile=='q-164524' else None})
  extraction.append({'source':profile,'parameters':p,'field':f[':answer-field/key'],'source_prompt':old[':question/problem'],'source_solution':old.get(':question/worked-solution'),'choices':[{'original':ans[':answer/value'],'recipe':c['recipes'][made.index(read(ans[':answer/value']))],'exact_original_value':str(read(ans[':answer/value'])),'reproduced':True} for ans in f[':answer-field/choices']]})
  inputs.append(native('source-'+profile,r));review.append('## '+profile+'\n\nOriginal\n\n'+old[':question/problem']+'\n\nTemplate replay\n\n'+g.markdown(r))
 counts={};coverage={};valid=0;rejected=0
 for profile,c in g.PROFILES.items():
  if c.get('legacy'):continue
  coverage[profile]={'a':set(),'b':set(),'plane':set(),'target':set()};counts[profile]=0
  # Domain boundaries and signed errors irrelevant: all semiaxes positive integers.
  for a,b,plane in __import__('itertools').product(range(1,13),range(1,13),('xy','xz')):
   p=dict(a=a,b=b,plane=plane,target=c['target'])
   try:r=g.generate(c['level'],seed=0,parameters=p,profile=profile)
   except ValueError:rejected+=1;continue
   check_math(r);assert g.generate(c['level'],seed=999,parameters=p,profile=profile)['question']==r['question']
   for key in coverage[profile]:coverage[profile][key].add(p[key])
   counts[profile]+=1;valid+=1
   inputs.append(native(profile+str(p),r))
 previews=g.batch('easy',8,2690)+g.batch('moderate',8,2690)
 for r in previews:check(r);review.append('## Variant\n\n'+g.markdown(r))
 # Change the requested component with identical semiaxes and plane; keys and
 # supplied components change together, without treating a shuffled bank as new.
 r1=check(g.generate('moderate',profile='q-164526',parameters=dict(a=5,b=3,plane='xy',target='cos')))
 r2=check(g.generate('moderate',profile='q-164522',parameters=dict(a=5,b=3,plane='xy',target='sin')))
 assert r1['question'][':question/problem']!=r2['question'][':question/problem'] and fingerprint(r1['question'])!=fingerprint(r2['question'])
 save('changed-target.json',[r1,r2]);save('previews.json',previews);save('source-replay.json',{'passed':True,'basis':g.SNAPSHOT['basis'],'banks_matched':7,'banks_total':7,'values_matched':35,'values_total':35,'distractors_matched':28,'distractors_total':28,'results':replays});save('template-components.json',extraction)
 save('native-input.json',inputs);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 (HERE/'review.md').write_text('\n\n'.join(review))
 hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE.with_suffix('.py'),HERE/'validate.py',HERE/'source.json']}
 save('validation.json',{'passed':True,'bounded_valid_instances':valid,'rejected_colliding_banks':rejected,'counts_by_profile':counts,'slot_coverage':{p:{k:sorted(vals) for k,vals in slots.items()} for p,slots in coverage.items()},'source_bank_fidelity':'7/7 complete banks; 35/35 values; 28/28 distractors','rendered_math':'printed Cartesian equation, supplied components, every option, requested component, full solution vector and substitution denominators checked independently','notation_fidelity':'positive cos/sin convention and source stages preserved; normalized LaTeX and spacing; source denominator typo explicitly corrected','changed_target_check':True,'hard_unsupported':True,'hashes':hashes})
 save('freeze.json',{'version':g.VERSION,'sha256':hashes,'source_basis':g.SNAPSHOT['basis'],'lineage':g.SNAPSHOT['lineage']});print(json.dumps({'validated':valid,'bank_replays':7,'counts':counts}))
if __name__=='__main__':main()
