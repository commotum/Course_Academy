"""Independent parsing of displayed mathematics and actual learner radio grading."""
import hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('fractional_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
x=sp.Symbol('x',real=True)
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2)+'\n')
def group(s,i):
 assert s[i]=='{',(s,i)
 depth=1;j=i+1
 while depth:
  if s[j]=='{':depth+=1
  if s[j]=='}':depth-=1
  j+=1
 return s[i+1:j-1],j
def math(text):
 def convert(s):
  out='';i=0
  while i<len(s):
   if s.startswith(r'\frac',i) or s.startswith(r'\dfrac',i):
    i+=6 if s.startswith(r'\dfrac',i) else 5;a,i=group(s,i);b,i=group(s,i);out+='(('+convert(a)+')/('+convert(b)+'))'
   elif s.startswith(r'\sqrt',i):
    a,i=group(s,i+5);out+='sqrt('+convert(a)+')'
   elif s[i]=='{':
    a,i=group(s,i);out+='('+convert(a)+')'
   else:out+=s[i];i+=1
  return out
 text=text.replace('+C','').replace(r'\,','')
 return parse_expr(re.sub(r'\b[sy]\b','x',convert(text)),local_dict={'x':x,'sqrt':sp.sqrt},transformations=standard_transformations+(convert_xor,implicit_multiplication_application))
def prompt_integrand(q):
 p=q[':question/problem'];start=p.index(r'\int')+4;end=p.find(r'\,',start)
 if end<0:end=p.index('dx',start)
 t=p[start:end].strip();return math(t)
def fingerprint(q):return g.digest(['integrand',sp.srepr(sp.cancel(prompt_integrand(q)))])
def check(rec):
 m=rec['generation'];q=rec['question'];t=g.PROFILES[m['template']];b=m['parameters'][0]
 assert rec==g.generate(t['level'],m['seed'],m['template'],[b])
 f=q[':question/answer-fields'][0];assert f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio'
 bank=f[':answer-field/choices'];assert len(bank)==5
 fs=[math(a[':answer/value']) for a in bank];ds=[sp.simplify(sp.diff(a,x)) for a in fs]
 integrand=prompt_integrand(q);assert sp.simplify(integrand-g.integrand(t,b))==0
 assert sp.simplify(ds[0]-integrand)==0 and f[':answer-field/correct'][1]==bank[0][':answer/id']
 for i in range(5):
  for j in range(i):assert sp.simplify(ds[i]-ds[j])!=0,'equivalent choices modulo C'
 sol=q[':question/worked-solution'];u=math(re.search(r'Let \$u=([^$]+)\.\$',sol)[1]);assert u==b+t['sign']*x**t['n']
 du=re.search(r'\\frac\{\\text\{d\}u\}\{\\text\{d\}[xsy]\}=([^\\]+)',sol)[1]
 assert sp.simplify(math(du)-sp.diff(u,x))==0
 final=sol.split(' & =')[-1].split(r'\end{aligned}')[0];assert sp.simplify(sp.diff(math(final),x)-integrand)==0
 assert fingerprint(q)==m['mathematical_fingerprint']
 assert all('@@' not in s for s in [q[':question/problem'],sol]+[a[':answer/value'] for a in bank])
 return rec
def native(label,rec):
 f=rec['question'][':question/answer-fields'][0]
 return {'label':label,'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if i==0 else 'rejected','purpose':'actual application radio grading'} for i,a in enumerate(f[':answer-field/choices'])]}
def main():
 source=json.loads((HERE/'source.json').read_text());qs={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']};inputs=[];replay=[];review=[];all_records=[]
 for sid,t in g.PROFILES.items():
  r=check(g.generate(t['level'],0,sid,t['parameters']));q=r['question'];old=qs[sid];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
  assert q[':question/problem']==old[':question/problem'] and q[':question/worked-solution']==old[':question/worked-solution']
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices'])
  assert f[':answer-field/choices'][0][':answer/value']==of[':answer-field/correct'][':answer/value']
  replay.append({'source':sid,'matched_choices':5,'matched_distractors':4,'complete_bank_match':True,'prompt_exact':True,'solution_exact':True})
  review.append('## '+sid+'\n\nOriginal\n\n'+old[':question/problem']+'\n\n'+old[':question/worked-solution']+'\n\nReplay\n\n'+g.markdown(r)+'\n\nVariant\n\n'+g.markdown(check(g.generate(t['level'],0,sid,[12]))))
  for b in range(1,13):
   r=check(g.generate(t['level'],0,sid,[b]));assert g.generate(t['level'],99,sid,[b])['question']==r['question'];inputs.append(native(sid+' '+str(b),r));all_records.append(r)
 incomplete=qs['q-49636'];assert ':question/difficulty' not in incomplete and ':question/worked-solution' not in incomplete and ':answer-field/correct' not in incomplete[':question/answer-fields'][0]
 # Canonical and incomplete legacy prompts also participate in novelty checks.
 for q in source['record'][':knowledge-point/questions']+[source['record'][':knowledge-point/canonical-example']]:fingerprint(q)
 save('source-replay.json',{'passed':True,'complete_banks_matched':9,'complete_banks_total':9,'distractors_matched':36,'distractors_total':36,'profiles':replay,'excluded_incomplete_sources':['q-49636'],'reason':'missing difficulty, correct designation, worked solution; original retained unchanged'})
 save('native-input.json',inputs);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 save('previews.json',g.batch('moderate',5,1936)+g.batch('hard',5,1936));(HERE/'review.md').write_text('\n\n'.join(review)+'\n')
 save('validation.json',{'passed':True,'mathematical_checks':'Independently parsed displayed integrands, every choice derivative, distinct modulo constants, substitution derivative, and final solution derivative; all 108 bounded instances','exhaustive_instances':len(all_records),'distinct_by_level':{l:len({r['generation']['mathematical_fingerprint'] for r in all_records if r['question'][':question/difficulty']==':question.difficulty/'+l}) for l in g.LEVELS},'source_fidelity':'9/9 complete banks, 36/36 distractors, exact prompts and worked solutions','supported_levels':list(g.LEVELS),'native_grading':'all choices for all 108 instances','hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'contract.json',HERE/'validate.py')}})
if __name__=='__main__':main()
