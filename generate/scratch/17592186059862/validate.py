"""Exact independent differentiation, source-bank replay and native grading QA."""
import hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x=sp.Symbol('x',positive=True)
def save(n,v):(HERE/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def scalar(s):
 s=s.replace(r'\sqrt{x}','sqrt(x)').replace('{x}','x').replace(' ','')
 def parse(t):
  if t.startswith(r'\frac{'):
   def group(t,i):
    assert t[i]=='{';d=1;j=i+1
    while d:d+=(t[j]=='{')-(t[j]=='}');j+=1
    return t[i+1:j-1],j
   a,i=group(t,5);b,j=group(t,i);assert j==len(t);return parse(a)/parse(b)
  t=t.replace(r'\sqrt{x}','sqrt(x)');t=re.sub(r'x\^\{([^}]+)\}',r'x**(\1)',t);t=re.sub(r'x\^(-?\d+)',r'x**(\1)',t)
  t=re.sub(r'(\d)(x|sqrt)',r'\1*\2',t)
  return sp.sympify(t,locals={'x':x,'sqrt':sp.sqrt})
 return parse(s)
def fingerprint(q):
 t=q[':question/problem'].replace('{x}','x')
 m=re.search(r'=\s*(\d+)x\^(?:\{(\d+)\}|(\d+))',t)
 if m:return g.digest(['power',int(m[1]),int(m[2] or m[3])])
 t=q.get(':question/worked-solution','')
 m=re.search(r'\((\\frac\{\d+\}\{\d+\}|\d+)\\sqrt\{x\}',t)
 assert m,t
 return g.digest(['root',str(scalar(m[1]))])
def check(rec):
 m=rec['generation'];q=rec['question'];level=q[':question/difficulty'].split('/')[-1]
 assert rec==g.generate(level,m['seed'],m['template'],m['parameters'])
 assert fingerprint(q)==m['mathematical_fingerprint']
 f=q[':question/answer-fields'][0];a=f[':answer-field/choices'];values=[scalar(z[':answer/value']) for z in a]
 c=sp.Rational(m['parameters'][0]);n=m['parameters'][1]
 function=c*x**int(n) if level=='easy' else c*sp.sqrt(x)+int(n)
 derivative=sp.diff(function,x)
 good=[z[':answer/id'] for z,y in zip(a,values) if sp.simplify(y-derivative)==0]
 assert good==[f[':answer-field/correct'][1]]
 assert all(sp.simplify(y-z)!=0 for i,y in enumerate(values) for z in values[:i])
 final=q[':question/worked-solution'].split('&=')[-1].split('& =')[-1].split(r'\end{aligned}')[0].strip();assert sp.simplify(scalar(final)-derivative)==0
 assert len(a)==(5 if level=='easy' else 1)
 assert '{{field-1}}' in q[':question/problem'] if level=='moderate' else True
 assert 'sqrt' not in q[':question/problem'] or m['domain']=='x > 0'
 return rec
def native(label,rec):
 f=rec['question'][':question/answer-fields'][0]
 if f[':answer-field/type']==':answer-field.type/radio':
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'radio bank grading'} for a in f[':answer-field/choices']]
 else:
  c=sp.Rational(rec['generation']['parameters'][0]);correct=f[':answer-field/choices'][0][':answer/value']
  checks=[{'submitted':correct,'expected':'accepted','purpose':'canonical blank'},{'submitted':r'\frac{'+str(c.p)+r'}{'+str(2*c.q)+r'\sqrt{x}}','expected':'accepted','purpose':'equivalent fraction'},{'submitted':r'\frac{'+str(c.p+1)+r'}{'+str(2*c.q)+r'\sqrt{x}}','expected':'rejected','purpose':'wrong coefficient'},{'submitted':'0','expected':'rejected','purpose':'wrong derivative'}]
 return {'label':label,'record':rec,'checks':checks}
def main():
 old={q[':question/math-academy-id']:q for q in json.loads((HERE/'reference/source.json').read_text())[':knowledge-point/questions']};replays=[];inputs=[];review=[];count=0
 for sid,p in [('q-1214',[6,6]),('q-272',[4,3])]:
  r=check(g.generate('easy',0,sid,p));f=r['question'][':question/answer-fields'][0];bank=[scalar(a[':answer/value']) for a in f[':answer-field/choices']];source=old[sid][':question/answer-fields'][0][':answer-field/choices']
  matches=[sum(sp.simplify(scalar(a[':answer/value'])-b)==0 for b in bank) for a in source];assert matches==[1]*5
  assert r['question'][':question/problem']==old[sid][':question/problem']
  replays.append({'source':sid,'matched_distractors':4,'total_distractors':4,'matched_bank':5,'total_bank':5,'missing':[],'extra':[],'correct_designation':'source omits correct ref; independently inferred unique derivative','prompt_exact':True,'solution_fidelity':'source has no solution; canonical e-138 wording reused'})
 for sid,p in [('q-142993',['2/3',3]),('q-167561',['2',-1])]:
  r=check(g.generate('moderate',0,'root-blank',p));assert sp.simplify(scalar(r['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'])-scalar(old[sid][':question/answer-fields'][0][':answer-field/correct'][':answer/value']))==0
  replays.append({'source':sid,'blank_answer_replayed':True,'prompt_fidelity':'explicit function restored from solution; consistent g label; irrelevant whitespace normalized','solution_fidelity':'same six-step rule sequence; corrected derivative operator and function label'})
 for sid in ['q-1214','q-272','root-blank']:
  level='moderate' if sid=='root-blank' else 'easy'
  for i,p in enumerate(g.candidates(sid)):
   r=check(g.generate(level,i,sid,p));count+=1;inputs.append(native(sid+str(p),r))
   if i in (0,1,len(g.candidates(sid))-1):review.append(r)
 save('source-replay.json',replays);save('native-input.json',inputs);save('review.json',review)
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE.with_suffix('.py'),HERE/'validate.py',HERE/'capabilities.json']}
 save('validation.json',{'passed':True,'checked_instances':count,'all_complete_profiles_replayed':True,'exact_symbolic_derivatives':True,'actual_engine_grading':True,'deterministic_replay':True,'hashes':hashes,'difficulty_evidence':'easy integer powers match q-10289; moderate square-root blanks q-142993 q-167561','fidelity_exceptions':'Source gaps and supported corrections documented in extraction; originals unchanged'})
if __name__=='__main__':main()
