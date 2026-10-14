"""Root readback of actual signed circulation equations and complete banks."""
import importlib.util,json,re,hashlib,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186133899;D=R.parents[2]/f'generate/scratch/{K}'
z=importlib.util.spec_from_file_location('root_circulation',D.with_suffix('.py'));g=importlib.util.module_from_spec(z);z.loader.exec_module(g)
def val(t):
 t=t.strip().rstrip('.').replace('π','pi').replace(r'\pi','pi').replace(' ','')
 t=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',t);t=re.sub(r'(\d)pi',r'\1*pi',t)
 assert re.fullmatch(r'[0-9().+*/pi-]+',t),t
 return s.sympify(t)
C=dict(records=0,prompt_operands=0,orientation_decisions=0,symbolic_components=0,substituted_components=0,common_denominator_components=0,conclusions=0,choices=0,method_banks=0,shared_prose=0,asset_hashes=0)
S=dict(prompts=0,solutions=0,values=0,refs=0,absent_refs=0)
originals={q[':question/math-academy-id']:q for q in json.load(open(R/f'sources/{K}.json'))['record'][':knowledge-point/questions']}
assert json.load(open(D/'source.json'))==json.load(open(R/f'sources/{K}.json'))
for c in json.load(open(D/'source-cases.json')):
 q=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile'])['question'];o=originals[c['source_id']]
 for k in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):assert (k in q)==(k in o)
 assert q[':question/problem']==o[':question/problem'];S['prompts']+=1
 if ':question/worked-solution' in o:assert q[':question/worked-solution']==o[':question/worked-solution'];S['solutions']+=1
 a,b=q[':question/answer-fields'][0],o[':question/answer-fields'][0];assert sorted(x[':answer/value'] for x in a[':answer-field/choices'])==sorted(x[':answer/value'] for x in b[':answer-field/choices']);S['values']+=5
 assert (':answer-field/correct' in a)==(':answer-field/correct' in b)
 if ':answer-field/correct' in b:assert next(x[':answer/value'] for x in a[':answer-field/choices'] if x[':answer/id']==a[':answer-field/correct'][1])==b[':answer-field/correct'][':answer/value'];S['refs']+=1
 else:S['absent_refs']+=1
records=json.load(open(R/f'qa/{K}-sampled.json'))
for level in ('easy','moderate','hard'):
 for family,data in g.FAMILIES.items():
  if data['level']==('moderate' if level=='hard' else level):records.extend(g.generate(level,template=family,seed=n) for n in (631,917))
for rec in records:
 q=rec['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];assert '∮_(' not in prompt
 numbers=[val(t.replace(r'\,','')) for t in re.findall(r'\\text\{d\}r\s*=\s*([^,\n$]+)',prompt)];assert len(numbers)==3;C['prompt_operands']+=3
 prose=prompt.split('where ',1)[1].split(', calculate',1)[0];directions={}
 for chunk in re.finditer(r'(.*?)(?:is|are) oriented (counterclockwise|clockwise)',prose):
  for idx in re.findall(r'C[^\d]*([123])',chunk[1]):directions[int(idx)]=chunk[2]
 assert set(directions)=={1,2,3};signs=[1 if directions[i]==('counterclockwise' if i==1 else 'clockwise') else -1 for i in (1,2,3)];C['orientation_decisions']+=3
 chain=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)[1];rows=[t.split('& =',1)[1].strip() for t in chain.split(chr(92)*2)];hard=q[':question/difficulty'].endswith('/hard');assert len(rows)==(4 if hard else 3)
 tokens=re.findall(r'([+-]?)\{∮\}_\{\{C\}_\{([123])\}\}F\\cdot \\text\{d\}r',rows[0]);assert [int(i) for _,i in tokens]==[1,2,3] and [-1 if t=='-' else 1 for t,i in tokens]==signs;C['symbolic_components']+=3
 pattern=re.compile(r'([+-]?)(\(-?(?:\\frac\{\d+\}\{\d+\}|\d+)\)|-?(?:\\frac\{\d+\}\{\d+\}|\d+))')
 def components(text):
  text=text.replace(" ","");pos=0;out=[]
  while pos<len(text):
   m=pattern.match(text,pos);assert m,(text,pos);out.append((-1 if m[1]=='-' else 1,val(m[2])));pos=m.end()
  return out
 assert components(rows[1])==list(zip(signs,numbers));C['substituted_components']+=3
 total=sum(v*sgn for v,sgn in zip(numbers,signs));assert val(rows[-1])==total;C['conclusions']+=1
 if hard:
  m=re.fullmatch(r'\\frac\{([^{}]+)\}\{(\d+)\}',rows[2]);assert m;den=int(m[2]);assert den==s.ilcm(*[n.q for n in numbers]);assert components(m[1])==[(sgn,n*den) for sgn,n in zip(signs,numbers)];C['common_denominator_components']+=3
 f=q[':question/answer-fields'][0];answers=f[':answer-field/choices'];bank=[val(a[':answer/value']) for a in answers];assert len(set(bank))==5
 assert [a[':answer/id'] for a,v in zip(answers,bank) if v==total]==[f[':answer-field/correct'][1]]
 if rec['generation']['bank_profile']=='method_signs':want=[total]+[total-2*n*sgn for n,sgn in zip(numbers,signs)]+[-total]
 else:want=[total]+[total-n*sgn for n,sgn in zip(numbers,signs)]+[-total]
 assert set(bank)==set(want);C['choices']+=5;C['method_banks']+=1
 sid=rec['generation']['source_id'];source_sol=originals[sid].get(':question/worked-solution',originals['q-126862'][':question/worked-solution']);clean=lambda t:re.sub(r'!\[\]\([^)]+\)','PLOT',t)
 assert clean(sol.split(r'\begin{aligned}')[0])==clean(source_sol.split(r'\begin{aligned}')[0]);assert sol.split(r'\end{aligned}')[1]==source_sol.split(r'\end{aligned}')[1];C['shared_prose']+=1;C['records']+=1
for asset in json.load(open(D/'plot-spec.json'))['assets']:assert hashlib.sha256(Path(asset['asset']).read_bytes()).hexdigest()==asset['sha256'];C['asset_hashes']+=1
out=dict(status='passed',source=S,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
