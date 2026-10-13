"""Independent printed-prompt, full-bank, intermediate solution, and actual grader checks."""
import hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('inverse_tangent_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
x=g.x

def save(name,data):(HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def prompt(q):
 m=re.search(r'\\frac\{(\d+)\}\{(?:1\+(\d+)\{x\}\^\{2\}|(\d+)\+\{x\}\^\{2\})\}',q[':question/problem']);assert m
 n=sp.Integer(m[1]);b=sp.Integer(m[2] or m[3]);return n/(1+b*x*x) if m[2] else n/(b+x*x)
def fingerprint(q):
 if r'\dfrac{3}{2 + 50x^2}' in q[':question/problem']:return g.digest(str(sp.cancel(3/(2+50*x*x))))
 return g.digest(str(sp.cancel(prompt(q))))
def question_check(q):
 target=prompt(q);f=q[':question/answer-fields'][0]
 assert len(q[':question/answer-fields'])==1 and f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
 bank=f[':answer-field/choices'];assert len(bank)==5
 derivatives=[sp.diff(g.parse_value(a[':answer/value']),x) for a in bank]
 assert all(sp.simplify(a-b)!=0 for i,a in enumerate(derivatives) for b in derivatives[:i])
 right=[a[':answer/id'] for a,d in zip(bank,derivatives) if sp.simplify(d-target)==0]
 assert right==[f[':answer-field/correct'][1]]
 row=q[':question/worked-solution'].split('$$')[-2].split(r' \\ ')[-1]
 final=row.split('& =')[1].split(r'\end{aligned}')[0].strip()
 assert sp.simplify(sp.diff(g.parse_value(final),x)-target)==0

def scalar_before(row,marker):
 t=row.split('& =',1)[-1].split(marker,1)[0].strip()
 assert marker in row
 return sp.Integer(1) if not t else g.parse_value(t)
def check(rec):
 meta=rec['generation'];q=rec['question'];level=q[':question/difficulty'].split('/')[-1]
 assert rec['knowledge_point']['db_id']==g.KP_ID
 assert rec==g.generate(level,meta['seed'],meta['profile'],meta['parameters'])
 target=prompt(q);assert sp.denom(sp.cancel(target)).subs(x,0)>0
 n,b=map(sp.Integer,meta['parameters']);s=sp.sqrt(b);c=n/s
 assert target==(n/(1+b*x*x) if level=='easy' else n/(b+x*x))
 f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1 and f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
 bank=f[':answer-field/choices'];assert len(bank)==5 and len({a[':answer/id'] for a in bank})==5
 vals=[g.parse_value(a[':answer/value']) for a in bank];ds=[sp.diff(z,x) for z in vals]
 assert all(sp.simplify(a-b)!=0 for i,a in enumerate(ds) for b in ds[:i])
 correct=[a[':answer/id'] for a,d in zip(bank,ds) if sp.simplify(d-target)==0];assert correct==[f[':answer-field/correct'][1]]
 sol=q[':question/worked-solution'];assert '@@' not in sol and '![' not in sol
 blocks=sol.split('$$');final=blocks[-2];rows=final.split(r' \\ ');assert len(rows)==5
 if level=='easy':
  assert [scalar_before(z,r'\int') for z in rows[:3]]==[n,n,c]
  assert scalar_before(rows[3],r'\operatorname')==c
  assert r'\frac{1}{'+g.tex(s)+'}' in blocks[-4] if s.is_Integer else r'\frac{1}{\sqrt{'+str(b)+'}}' in blocks[-4]
 else:
  rewrite=blocks[1].split(r' \\ ');assert len(rewrite)==3
  assert [scalar_before(z,r'\int') for z in rewrite[1:]]==[n/b,n/b]
  assert [scalar_before(z,r'\int') for z in rows[:3]]==[n/b,n/b,c]
  assert scalar_before(rows[3],r'\operatorname')==c
 finalvalue=rows[-1].split('& =')[1].split(r'\end{aligned}')[0].strip()
 assert sp.simplify(sp.diff(g.parse_value(finalvalue),x)-target)==0
 assert fingerprint(q)==meta['mathematical_fingerprint']
 return rec

def native(label,rec):
 f=rec['question'][':question/answer-fields'][0]
 return {'label':label,'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'actual application radio selection grading'} for a in f[':answer-field/choices']]}
def main():
 source=json.loads((HERE/'source.json').read_text());qs={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']};inputs=[];replay=[];fps={'easy':set(),'moderate':set()};review=[]
 for sid,t in g.PROFILES.items():
  rec=check(g.generate(t['difficulty'],0,sid,t['parameters']));q=rec['question'];old=qs[sid];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
  values=[a[':answer/value'] for a in f[':answer-field/choices']];original=[a[':answer/value'] for a in of[':answer-field/choices']]
  assert values==original,(sid,list(zip(values,original)))
  assert q[':question/problem']==old[':question/problem'] and q[':question/worked-solution']==old[':question/worked-solution'],sid
  assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value']
  # Every original option has exactly one algebraically equivalent generated value.
  assert all(sum(sp.simplify(g.parse_value(a)-g.parse_value(b))==0 for b in values)==1 for a in original)
  replay.append({'source':sid,'profile':sid,'matched_choices':5,'matched_distractors':4,'complete_bank_match':True,'prompt_exact':True,'solution_exact':True})
  cs=g.candidates(sid);variant=check(g.generate(t['difficulty'],42,sid,cs[-1]));review.append('## '+sid+'\n\nOriginal\n\n'+old[':question/problem']+'\n\n'+old[':question/worked-solution']+'\n\nReplay\n\n'+g.markdown(rec)+'\n\nVariant\n\n'+g.markdown(variant))
  for p in cs:
   r=check(g.generate(t['difficulty'],0,sid,p));assert g.generate(t['difficulty'],97,sid,p)['question']==r['question'];inputs.append(native(sid+' '+str(p),r));fps[t['difficulty']].add(fingerprint(r['question']))
 save('source-replay.json',{'passed':True,'complete_banks_matched':16,'complete_banks_total':16,'distractors_matched':64,'distractors_total':64,'profiles':replay,'excluded_source_banks':[]})
 save('native-input.json',inputs);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 (HERE/'review.md').write_text('\n\n'.join(review)+'\n')
 previews=g.batch('easy',5,1986)+g.batch('moderate',5,1986);save('previews.json',previews)
 caps={'knowledgePoint':g.KP_ID,'supported_levels':['easy','moderate'],'exceptions':[{'difficulty':'hard','kind':'unsupported','bounded':True,'evidence':'All 16 complete source questions at basis '+str(source['basis'])+' are easy or moderate. No verified hard template or bank; the canonical example is ungraded and not a hard practice source. New source evidence reopens classification.','filled':False}], 'finite_variant_limits':{level:len(z) for level,z in fps.items()},'sampling_policy':'Observed denominator scale remains fixed. Seven nonunit-numerator profiles admit 2<=n<=30, preserving source integer/radical/quotient forms and rejecting correct/equivalent distractor collisions. Unit-numerator and n=s cancellation profiles replay only their observed parameters. This narrow policy makes no claim about wider mathematical possibility; exhaustion leaves shortages explicit.'}
 save('capabilities.json',caps)
 save('validation.json',{'passed':True,'source_basis':source['basis'],'exhaustive_instances':len(inputs),'distinct_bounded_integrands':{k:len(z) for k,z in fps.items()},'source_fidelity':'16/16 complete banks, 64/64 distractors, exact prompts, full solutions and option notation','correctness':'Independent printed integrand, option derivatives, distinct derivatives modulo constants and applicable real branches, substitution and intermediate solution coefficients, final derivative','grading':'actual course_academy_engine::learning::grade_field; all five choices of every bounded instance','hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'contract.json',HERE/'validate.py')}})
 print('Validated',len(inputs),'instances; distinct integrands',caps['finite_variant_limits'])
if __name__=='__main__':main()
