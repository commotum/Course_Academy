import importlib.util,json,os,re,sys
from pathlib import Path
from fractions import Fraction as F
b=Path('/home/jake/Developer/Course_Academy/reference/edb-math/repairs/2026-11-11-vector-independent-practice/package');out=Path('/tmp/question-audit-20261111/independent-review/vector-assets');out.mkdir(exist_ok=True)
os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']=str(out);sys.path.insert(0,str(b))
spec=importlib.util.spec_from_file_location('vector_candidate',b/'generator.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def val(t):return F(re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'\1/\2',t))
report={'cases':0,'bands':{},'failures':[]};examples=[]
for band in ['easy','moderate','hard']:
 details={'fields':{},'directions':set(),'component_signs':set(),'ratios':set()}
 for seed in [17,83,291]:
  records=g.batch(band,6,seed)
  for r in records:
   p=r['generation']['parameters'];a=list(map(F,p['a']));b0=list(map(F,p['b']));k=F(p['k']);ratio=F(p['r']);field=r['question'][':question/answer-fields'][0]
   # Independent read of rendered-asset coordinate payload; solve a lambda+b k=c.
   asset=json.loads((out/r['generation']['plot_assets']['prompt']).with_suffix('.json').read_text());c=list(map(F,asset['C']));det=a[0]*b0[1]-a[1]*b0[0];assert det!=0
   observed=(c[0]*b0[1]-c[1]*b0[0])/det;observed_k=(a[0]*c[1]-a[1]*c[0])/det
   assert observed==-ratio and observed_k==k
   answers=field[':answer-field/choices'];correct_id=field[':answer-field/correct'][1];correct=next(v for v in answers if v[':answer/id']==correct_id)
   assert val(correct[':answer/value'])==observed
   assert len(set(val(v[':answer/value']) for v in answers))==len(answers)
   assert asset['path'] is False
   assert not any(s in r['question'][':question/problem'] for s in ['\\overrightarrow{OP}','path','PC','opposite','length ratio'])
   solution_asset=json.loads((out/r['generation']['plot_assets']['solution']).with_suffix('.json').read_text());assert solution_asset['path'] is True
   f=field[':answer-field/type'];details['fields'][f]=details['fields'].get(f,0)+1;details['directions'].add('axis' if 0 in a else 'diagonal');details['component_signs'].add('negative' if k<0 else 'positive');details['ratios'].add(str(ratio));report['cases']+=1
   if len(examples)<2 or band!='easy' and not any(q['question'][':question/difficulty']==r['question'][':question/difficulty'] for q in examples):examples.append(r)
 report['bands'][band]={k:sorted(v) if isinstance(v,set) else v for k,v in details.items()}
report['status']='passed';Path('/tmp/question-audit-20261111/independent-review/vector-math.json').write_text(json.dumps(report,indent=2)+'\n');Path('/tmp/question-audit-20261111/independent-review/vector-examples.json').write_text(json.dumps(examples,indent=2)+'\n');print(json.dumps(report,indent=2))
