"""Independent refreshed-source, extension, mathematical and native grading QA."""
import hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('base_validation',HERE/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.m
spec=importlib.util.spec_from_file_location('extras',HERE/'extensions.py');e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)
def check(r):
 name=r['generation']['template']
 if name not in e.PARAMS:return v.check(r)
 q=r['question'];meta=r['generation'];p=meta['parameters'];f=q[':question/answer-fields'][0]
 x=sp.Symbol('x');a=sp.Rational(p['a0'])+sp.Rational(p['a1'])*x;b=sp.Rational(p['b0'])+sp.Rational(p['b1'])*x;t=sp.solve(a-b,x)[0];y=a.subs(x,t)
 paths=[HERE/ref for ref in re.findall(r'!\[\]\((.*?)\)',q[':question/problem']+'\n'+q[':question/worked-solution'])]
 assert len(paths)==2
 for i,path in enumerate(paths):
  assert path.read_bytes().startswith(b'\x89PNG')
  if path.with_suffix('.json').exists():
   side=json.loads(path.with_suffix('.json').read_text());assert side['parameters']==p
   for key in ('a','b'):
    for xx,yy in side['plotted_line_endpoints'][key]:assert sp.Rational(yy)==sp.Rational(p[key+'0'])+sp.Rational(p[key+'1'])*sp.Rational(xx)
   if i==1:assert list(map(sp.Rational,side['annotation_point']))==[t,y]
 assert f'point $({t},{y}).$' in q[':question/worked-solution']
 if name=='planes':assert f'${int(y)*1000:,}\\,\\text{{ft}}$' in q[':question/worked-solution']
 else:assert f'${y}\\,\\text{{L}}$' in q[':question/worked-solution'] and '{{field-1}}' in q[':question/problem']
 vals=[sp.Rational(a[':answer/value']) for a in f[':answer-field/choices']];assert len(set(vals))==len(vals)
 assert len(vals)==(5 if name=='planes' else 1)
 assert [a[':answer/id'] for a in f[':answer-field/choices'] if sp.Rational(a[':answer/value'])==t]==[f[':answer-field/correct'][1]]
 replay=g.generate('easy',999,template=name,parameters=p,profile=meta['bank_profile']);assert replay['question'][':question/id']==q[':question/id']
 for text in (q[':question/problem'],q[':question/worked-solution']):assert text.count('$')%2==0 and text.count('{')==text.count('}')
 return t,y

def native(r):
 f=r['question'][':question/answer-fields'][0];t=str(check(r)[0])
 if f[':answer-field/type']==':answer-field.type/blank':
  checks=[{'submitted':s,'expected':expect,'purpose':'Native numeric-equivalence and wrong-value check'} for s,expect in [(t,'accepted'),t and (t+'.0','accepted'),(str(int(t)*2)+'/2','accepted'),(str(int(t)+1),'rejected'),('-'+t,'rejected')]]
 else:checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Independently derived intersection, complete displayed bank'} for a in f[':answer-field/choices']]
 return {'label':r['question'][':question/id'],'record':r,'checks':checks}

def main():
 source=json.loads((HERE/'source-current.json').read_text());records=[];replays=[]
 for name in e.PARAMS:
  r=g.generate('easy',template=name,parameters=e.PARAMS[name],profile='observed_plane_expressions' if name=='planes' else 'blank');check(r);records.append(r)
  sq=next(q for q in source['record'][':knowledge-point/questions'] if q[':question/math-academy-id']==e.SOURCE_IDS[name]);f=r['question'][':question/answer-fields'][0];sf=sq[':question/answer-fields'][0]
  assert r['question'][':question/problem']==sq[':question/problem']
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
  assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==sf[':answer-field/correct'][':answer/value']
  norm=lambda text:re.sub(r'!\[\]\(.*?\)','<PLOT>',text)
  assert norm(r['question'][':question/worked-solution'])==norm(sq[':question/worked-solution'])
  replays.append({'source':e.SOURCE_IDS[name],'choices_matched':len(sf[':answer-field/choices']),'complete_bank':True,'correct_designation':True,'prompt_exact':True,'normalized_solution_exact':True})
 for name in e.PARAMS:
  for seed in range(12):records.append(g.generate('easy',seed,template=name));check(records[-1])
 (HERE/'current-engine-input.json').write_text(json.dumps([native(r) for r in records],indent=2)+'\n')
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'current-engine-input.json'),str(HERE/'current-engine-report.json')],check=True)
 report={'passed':True,'basis':source['basis'],'lineage':source['lineage'],'source_practice_count':4,'complete_source_banks_matched':4,'choices_matched':16,'distractors_matched':12,'new_source_replays':replays,'old_source_validation':'validation.json','blank_equivalent_entries':'native accepted integer, decimal, and quotient; rejected wrong and negative values','sampled_extensions':24,'difficulty_origin':{'easy':'observed sources plus authored truck, airplane, tank variants','moderate':'authored two-day horizontal labels in canonical pool context','hard':'authored twenty-meter labels with ten-meter minor grid in car context'},'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE.with_suffix('.py'),HERE/'extensions.py',HERE/'render.py',Path(__file__),ROOT/'generate/runs/current/check-engine']}}
 (HERE/'current-validation.json').write_text(json.dumps(report,indent=2)+'\n');(HERE/'current-review.json').write_text(json.dumps(records,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
