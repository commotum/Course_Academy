"""Compare exact old/new answer values and exercise generator templates."""
import importlib.util,json,subprocess,sys
from pathlib import Path
from .prepare import HERE,ROOT,Exact,PHANTOM
PYTHON=ROOT/'.venv/bin/python'
def run(script,count=100,replay=False):
 args=[str(PYTHON),str(script),'--count',str(count),'--seed','181028']
 if replay:args.append('--replay-source')
 r=subprocess.run(args,capture_output=True,text=True,timeout=45)
 assert r.returncode==0,r.stderr
 return json.loads(r.stdout)
def exact_question(record):
 q=record['question'];banks=[];keys=[]
 for f in q[':question/answer-fields']:
  bank=[Exact(PHANTOM.sub('',a[':answer/value'])).value() for a in f[':answer-field/choices']]
  banks.append(bank)
  key=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]);keys.append(key)
 return q[':question/problem'],q[':question/worked-solution'],banks,keys
if __name__=='__main__':
 info=json.loads((HERE/'generator-update.json').read_text());original=Path('/media/jake/SSD/EDB/math')/info['old_reference'];fixed=HERE/'generator/generator.py'
 old=run(original,300);new=run(fixed,300)
 assert [exact_question(x) for x in old]==[exact_question(x) for x in new]
 for rec in new:
  for f in rec['question'][':question/answer-fields']:
   for a in f[':answer-field/choices']:assert '\\phantom' not in a[':answer/value']
 replay=run(fixed,replay=True);assert [exact_question(x) for x in run(original,replay=True)]==[exact_question(x) for x in replay]
 checks=[]
 for w in info['workspaces']:
  records=run(ROOT/w['script'],50)
  for x in records:
   exact_question(x)
   assert '\\phantom' not in json.dumps(x)
  checks.append({'script':w['script'],'records_checked':len(records)})
 sys.path.insert(0,str(HERE/'generator'));spec=importlib.util.spec_from_file_location('fixed_product_generator',fixed);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
 combinations=0
 for kind,profile in (('integer','standard'),('integer','repeated'),('fraction','fraction')):
  for a in range(2,10):
   for b in range(2,10):
    for c in range(2,10):
     for n in (2,4,8):
      for reverse in (False,True):
       p=dict(kind=kind,profile=profile,a=a,b=b,c=c,n=n,reverse=reverse,layout='what')
       expr,texts,values,recipes=g.components(p)
       if len({values[r] for r in recipes})!=5:continue
       rec=g.build(p)
       f=rec['question'][':question/answer-fields'][0]
       for role,answer in zip(rec['generation']['recipes'],f[':answer-field/choices']):
        assert Exact(answer[':answer/value']).value()==values[role]
        assert '\\phantom' not in answer[':answer/value']
       assert Exact(expr).value()==values['correct']
       combinations+=1
 # Both sibling registrations use ordinary TeX and add no invisible padding.
 siblings=[]
 for kp in json.loads((HERE/'topic.json').read_text())[0][0][':topic/knowledge-points']:
  ref=kp[':knowledge-point/question-generator'][':question-generator/script']
  source=Path('/media/jake/SSD/EDB/math')/ref
  if kp[':db/id']!=17592186129111:assert '\\phantom' not in source.read_text()
  siblings.append({'kp':kp[':db/id'],'script':ref,'affected':kp[':db/id']==17592186129111})
 result={'passed':True,'old_new_records_with_identical_math_and_correct_positions':300,'unchanged_source_replays':len(replay),'generator_combinations_checked':combinations,'drafts':checks,'registrations_audited':siblings}
 (HERE/'generator-checks.json').write_text(json.dumps(result,indent=2)+'\n')
 (HERE/'generator-render-input.json').write_text(json.dumps(new[:4],indent=2)+'\n')
 print(json.dumps({'passed':True,'combinations':combinations,'drafts':len(checks)}))
