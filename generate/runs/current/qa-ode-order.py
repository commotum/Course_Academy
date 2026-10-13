"""Root independent printed derivative-order and field-owned response readback."""
import sys,re,json,importlib.util
from pathlib import Path
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
words=['first','second','third','fourth','fifth','sixth','seventh','eighth'];ordinal=dict(zip(words,range(1,9)))
def orders(text):
 # Independent token patterns: exponent in the denominator identifies a
 # Leibniz derivative and must equal its numerator derivative exponent.
 result=[]
 for m in re.finditer(r'\\(?:d?frac)\{(.*?)\}\{\\text\{d\}(?:\{x\}|x)(?:\^\{(\d+)\})?\}',text):
  top=m[1];order=int(m[2] or 1);power=re.findall(r'\^\{(\d+)\}',top);assert (int(power[0]) if power else 1)==order,(m[0],order);result.append(order)
 for primes in re.findall(r'\{y\}\^\{([′″‴\']+)\}',text):result.append(sum({'′':1,'″':2,'‴':3,"'":1}[c] for c in primes))
 assert result,text;return result
n=dict(records=0,fields=0,choices=0,equations=0,derivative_occurrences=0,highest_prose=0,conclusions=0,source_prompts=0,source_solutions=0,source_values=0,source_refs=0)
def check(rec):
 q=rec['question'];g=rec['generation'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];fs=q[':question/answer-fields'];selected=[]
 if len(fs)==3:
  target=ordinal[re.search(r'are (\w+)-order',prompt)[1]];eqs=dict(re.findall(r'- \*\*(I|II|III)\.\*\* \$(.*?)\$',prompt));assert len(eqs)==3
  for f in fs:
   key=f[':answer-field/key'];ds=orders(eqs[key]);highest=max(ds);expected='true' if highest==target else 'false';choices=f[':answer-field/choices'];assert {a[':answer/value'] for a in choices}=={'false','true'}
   actual=next(a[':answer/value'] for a in choices if a[':answer/id']==f[':answer-field/correct'][1]);assert actual==expected
   if expected=='true':selected.append(key)
   sentence=re.search(r'- Equation '+key+r' (.*?)(?=\n\n|$)',sol,re.S)[1];shown=re.search(r'highest derivative in this equation is \$(.*?)\$',sentence)[1];assert max(orders(shown))==highest
   assert ('is not a' in sentence)==(highest!=target)
   if highest!=target:assert re.search(r'this is a (\w+)-order',sentence)[1]==words[highest-1]
   n['derivative_occurrences']+=len(ds);n['equations']+=1;n['highest_prose']+=1
  first=re.search(r'largest derivative term in the equation is \$(.*?)\$',sol);assert first and max(orders(first[1]))==target
  conclusion=re.search(r'correct answer is "(.*?)\."',sol)[1];expected='none' if not selected else 'all three' if len(selected)==3 else ' and '.join(selected)+' only';assert conclusion==expected;n['conclusions']+=1
 else:
  equation=prompt.split('$$')[1] if '$$' in prompt else re.findall(r'\$(.*?)\$',prompt)[0];ds=orders(equation);highest=max(ds);f=fs[0];vs=[a[':answer/value'] for a in f[':answer-field/choices']];assert len(vs)==len(set(vs))
  actual=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert int(actual)==highest
  shown=re.search(r'highest derivative in the given ODE is \$(.*?)\$',sol);assert shown and max(orders(shown[1]))==highest
  declared=re.search(r'which has order \$(\d+)\.',sol);final=re.search(r'order of the ODE is \$(\d+)\.',sol);assert declared and final and int(declared[1])==int(final[1])==highest
  if g['authored']:
   assert set(map(int,vs))=={highest,min(ds),g['parameters']['e'],highest-1,highest+1} and len(ds)==2
  n['equations']+=1;n['derivative_occurrences']+=len(ds);n['highest_prose']+=1;n['conclusions']+=1
 n['records']+=1;n['fields']+=len(fs);n['choices']+=sum(len(f[':answer-field/choices']) for f in fs)
if __name__=='__main__':
 kp=17592186166813;D=R.parents[2]/'generate/scratch'/str(kp);g=load(D.with_suffix('.py'),'generator');src=json.load(open(D/'source.json'));assert src==json.load(open(R/'sources'/f'{kp}.json'));olds={q[':question/math-academy-id']:q for q in src['record'][':knowledge-point/questions']}
 for c in json.load(open(D/'source-cases.json')):
  rec=g.generate(c['level'],parameters=c['parameters'],template=c['template'],profile=c['bank_profile']);check(rec);q=rec['question'];o=olds[c['source_id']]
  for attr in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):assert (attr in q)==(attr in o)
  assert q[':question/problem']==o[':question/problem'] and q[':question/worked-solution']==o[':question/worked-solution'] and q[':question/difficulty']==o[':question/difficulty'][':db/ident']
  for f,of in zip(q[':question/answer-fields'],o[':question/answer-fields']):
   assert f[':answer-field/key']==of[':answer-field/key'] and f[':answer-field/type']==of[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);assert ':answer-field/correct' in f and ':answer-field/correct' in of
   correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert correct==of[':answer-field/correct'][':answer/value'];n['source_values']+=len(f[':answer-field/choices']);n['source_refs']+=1
  n['source_prompts']+=1;n['source_solutions']+=1
 for item in json.load(open(D/'review.json')):check(item['record'])
 for level in ('easy','moderate','hard'):
  for seed in range(50):check(g.generate(level,seed=440000+seed))
 (R/'qa'/f'{kp}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
