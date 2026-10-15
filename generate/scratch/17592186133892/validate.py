"""Printed-value parsing, independent calculus, complete source-bank replay and grading."""
import hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
from functools import lru_cache
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('line_y',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
t=g.t;x,y=g.x,g.y
def save(name,obj):(HERE/name).write_text(json.dumps(obj,indent=2,default=str)+'\n')
def group(value,start):
 assert value[start]=='{',(value,start)
 depth=1;end=start+1
 while depth:
  depth+=(value[end]=='{')-(value[end]=='}');end+=1
 return value[start+1:end-1],end
@lru_cache(maxsize=4000)
def read(value):
 value=value.replace('\u2061','').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\!','')
 value=re.sub(r'\\(?:operatorname|mathrm)\{(sin|cos)\}',r'\1',value)
 value=re.sub(r'\{(sin|cos)\}',r'\1',value);value=value.replace(r'\sin','sin').replace(r'\cos','cos').replace(r'\pi','pi')
 while r'\frac' in value:
  start=value.index(r'\frac');num,end=group(value,start+5);den,end=group(value,end);value=value[:start]+'(('+num+')/('+den+'))'+value[end:]
 value=re.sub(r'\^\{(\d+)\}',r'**\1',value).replace('^','**')
 value=re.sub(r'(sin|cos)\*\*(\d+)\s*t',r'(\1(t)**\2)',value)
 value=re.sub(r'(sin|cos)\s*t',r'\1(t)',value)
 value=value.replace('{','(').replace('}',')')
 return parse_expr(value,local_dict={'t':t,'x':x,'y':y,'sin':sp.sin,'cos':sp.cos,'pi':sp.pi},transformations=standard_transformations+(implicit_multiplication_application,))
@lru_cache(maxsize=4000)
def integral(value):
 value=value.replace(r'{\int }',r'\int').replace(r'\displaystyle','')
 pos=value.index(r'\int');coef=read(value[:pos]) if value[:pos].strip() else sp.Integer(1);tail=value[pos+4:];assert tail[0]=='_'
 lo,e=group(tail,1);assert tail[e]=='^';hi,e=group(tail,e+1)
 body=re.sub(r'\\(?:text|mathrm)\{d\}t\s*$','',tail[e:]).strip()
 return coef,read(body),read(lo),read(hi)
@lru_cache(maxsize=1000)
def evaluated(expr,lo,hi):return sp.simplify(sp.integrate(expr,(t,lo,hi)))
def bankmath(q):return [integral(a[':answer/value']) for a in q[':question/answer-fields'][0][':answer-field/choices']]
def check(r):
 m=r['generation'];profile=m['bank_profile'];k=m['parameters']['k'];assert profile in g.SUPPORTED and k in range(1,5) and not m['evidence_only']
 assert r==g.generate('easy',m['seed'],profile=profile,k=k,render=False)
 q=r['question'];prompt=q[':question/problem'];f=q[':question/answer-fields'][0];assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection' and len(f[':answer-field/choices'])==5
 # Independently read the actual displayed hint and integrand, then differentiate.
 hint=re.search(r'r\(t\)=\\langle (.*?),\\,(.*?)\\rangle',prompt);X,Y=read(hint[1]),read(hint[2])
 F=read(prompt.split(r'\int_C\left(')[1].split(r'\right)')[0]);lo,hi=g.PROFILES[profile]['lo'],g.PROFILES[profile]['hi']
 actual=sp.trigsimp(F.subs({x:X,y:Y},simultaneous=True)*sp.diff(Y,t));values=bankmath(q)
 assert all(a==lo and b==hi for _,_,a,b in values)
 wanted=evaluated(actual,lo,hi);totals=[evaluated(coef*expr,a,b) for coef,expr,a,b in values]
 assert len(set(totals))==5,(profile,k,totals)
 hits=[i for i,z in enumerate(totals) if sp.simplify(z-wanted)==0];assert len(hits)==1,(profile,k,totals,wanted)
 assert f[':answer-field/correct'][1]==f[':answer-field/choices'][hits[0]][':answer/id']
 assert sp.simplify(sp.trigsimp(values[hits[0]][0]*values[hits[0]][1]-actual))==0
 # Verify endpoint coordinates and concrete solution references from rendered text.
 expected=g.task(profile,k)
 assert all(sp.simplify(a-b)==0 for a,b in zip((X,Y,F),expected[:3]))
 for v in (lo,hi):assert rf'({g.tex(X.subs(t,v))},{g.tex(Y.subs(t,v))})' in prompt
 solution=q[':question/worked-solution'];assert hint[0].split('=',1)[1] in solution
 assert g.tex(sp.diff(Y,t))+'.\n$$' in solution
 assert f[':answer-field/choices'][hits[0]][':answer/value']+'.\\end{aligned}' in solution
 assert m['mathematical_fingerprint']==g.fingerprint(profile,k)
 return totals

def native(label,r):
 f=r['question'][':question/answer-fields'][0]
 return {'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'actual radio learner grader, every answer'} for a in f[':answer-field/choices']]}
def sourcefingerprint(q):
 mid=q.get(':question/math-academy-id')
 if mid in g.PROFILES:return g.fingerprint(mid,1)
 # Generated question identities/content are checked against the bounded domain.
 for profile in g.SUPPORTED:
  for k in range(1,5):
   r=g.generate(profile=profile,k=k,render=False)
   if q[':question/problem']==r['question'][':question/problem']:return g.fingerprint(profile,k)
 return hashlib.sha256(q[':question/problem'].encode()).hexdigest()

def main():
 originals={q[':question/math-academy-id']:q for q in g.SNAPSHOT['kp'][':knowledge-point/questions']};replay=[];components=[];review=[]
 for profile,p in g.PROFILES.items():
  old=originals[profile];r=g.generate(profile=profile,k=1,replay=True);obs=bankmath(old);made=bankmath(r['question']);matches=[]
  for a in obs:
   matching=[i for i,b in enumerate(made) if a[2:]==b[2:] and sp.trigsimp(a[0]*a[1]-b[0]*b[1])==0];assert len(matching)==1;matches.append(matching[0])
  assert sorted(matches)==list(range(5));f=old[':question/answer-fields'][0];ci=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][':answer/id']);assert matches[ci]==p['index']
  totals=[evaluated(a*b,lo,hi) for a,b,lo,hi in obs]
  replay.append({'source':profile,'complete_bank_reproduced':True,'matched_options':5,'matched_distractors':4,'missing_or_extra':[],'correct_designation_matched':True,'complete_definite_integral_values':list(map(str,totals)),'supported':profile in g.SUPPORTED,'exclusion':p.get('excluded')})
  components.append({'source':profile,'difficulty':'easy','template':profile,'field_type':'radio','field_key':'selection','prompt':old[':question/problem'],'solution':old[':question/worked-solution'],'original_parameters':{'X':str(p['X']),'Y':str(p['Y']),'F':str(p['F']),'lo':str(p['lo']),'hi':str(p['hi']),'k':1},'choices':[{'original':a[':answer/value'],'field':'selection','bank_profile':profile,'recipe':f'{coef} * k^{p["degree"]} * Integral({expr}, (t, {p["lo"]}, {p["hi"]}))','recipe_interpretation':'explicit observed expression pattern; inferred error interpretation unresolved','full_source_value_reproduced':True} for a,(coef,expr) in zip(f[':answer-field/choices'],p['bank'])]})
  review.append('## '+profile+'\n\nOriginal\n\n'+old[':question/problem']+'\n\nReplay\n\n'+g.markdown(r))
 records=[];coverage={};inputs=[]
 for profile in g.SUPPORTED:
  coverage[profile]=[]
  for k in range(1,5):
   r=g.generate(profile=profile,k=k);check(r);assert r['question']==g.generate(seed=999,profile=profile,k=k,render=False)['question'];records.append(r);coverage[profile].append(k);inputs.append(native(profile+'-k'+str(k),r))
  review.append('## Changed geometry '+profile+' (k=2)\n\n'+g.markdown(g.generate(profile=profile,k=2)))
 assert len({r['generation']['mathematical_fingerprint'] for r in records})==32
 assert g.batch('easy',32,123,False)==g.batch('easy',32,123,False)
 for level in ('moderate','hard'):
  try:g.batch(level,1)
  except ValueError:pass
  else:raise AssertionError('Unsupported level accepted')
 for k in (0,5,-1):
  try:g.generate(k=k)
  except ValueError:pass
  else:raise AssertionError('Out of domain scale accepted')
 save('source-replay.json',{'basis':g.SNAPSHOT['basis'],'banks':replay,'matched_complete_banks':10,'matched_distractors':40,'supported_complete_banks':8,'supported_distractors':32,'excluded_banks':2})
 save('template-components.json',components);save('previews.json',records);save('native-input.json',inputs)
 subprocess.run([str(HERE/'check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True,timeout=55)
 (HERE/'review.md').write_text('\n\n---\n\n'.join(review));save('validation.json',{'passed':True,'distinct_easy_tasks':32,'supported_profiles':8,'domain_coverage':coverage,'deterministic_replay':True,'every_generated_bank_has_five_distinct_definite_integral_values':True,'source_bank_fidelity':'50/50 options and 10/10 banks replayed; 2 mathematically defective source banks explicitly excluded','grading':'160 real learner radio checks','backbone':'hint, formula, parametrization, dy/dt, substitution and required trig identities, assembly; no evaluation requested','unsupported_levels':['moderate','hard'],'bounded_capacity':32,'normal_policy':'8 supported source profiles x integer scale k=1..4; no target/position slot is declared; same source interval and integrand operations','source_and_variant_visual_review':'pending'})
 print('Validated all 32 supported mathematical tasks; full source banks replayed, two excluded.')
if __name__=='__main__':main()
