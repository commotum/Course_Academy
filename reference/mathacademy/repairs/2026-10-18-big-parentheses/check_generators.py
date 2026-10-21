"""Exercise updated published/draft generators and check formatting semantics."""
import importlib.util, json, subprocess, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
PYTHON=ROOT/'.venv/bin/python'
spec=importlib.util.spec_from_file_location('repair_formatter',ROOT/'scripts/question_capture/math_format.py');fmt=importlib.util.module_from_spec(spec);spec.loader.exec_module(fmt)
def strip(s):return s.replace(r'\left(', '(').replace(r'\right)', ')')
def verify(records):
 for record in records:
  q=record['question']
  for attr in (':question/problem',':question/worked-solution'):
   text=q[attr];assert fmt.scalable_fraction_parentheses(text)==text,(attr,text)
   fmt.validate_prose(text)
  for field in q[':question/answer-fields']:
   for answer in field[':answer-field/choices']:fmt.validate_tex(answer[':answer/value'])
 return len(records)
def run(script,difficulty,count=80,*extra):
 result=subprocess.run([str(PYTHON),str(script),'--difficulty',difficulty,'--count',str(count),'--seed','181026',*extra],capture_output=True,text=True,check=True,timeout=90)
 return json.loads(result.stdout)
def summary(q):
 return {'problem':strip(q[':question/problem']),'solution':strip(q[':question/worked-solution']),
  'difficulty':q[':question/difficulty'],'banks':[[a[':answer/value'] for a in f[':answer-field/choices']] for f in q[':question/answer-fields']],
  'correct':[next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]) for f in q[':question/answer-fields']]}
if __name__=='__main__':
 info=json.loads((HERE/'generator-update.json').read_text())
 old=run(Path('/media/jake/SSD/EDB/math')/info['old_reference'],'easy');new=run(HERE/'generator/generator.py','easy')
 assert [summary(x['question']) for x in old]==[summary(x['question']) for x in new]
 result=[{'script':'repaired registered package','difficulty':'easy','checked':verify(new),'same_mathematics_as_original':True}]
 render=new[:3]
 for w in info['workspaces']:
  script=ROOT/w['script'];kp=w['kp']
  for difficulty in (('easy','moderate') if kp.endswith('743') else ('moderate',) if kp.endswith('744') else ('easy',)):
   records=run(script,difficulty,64);result.append({'script':w['script'],'difficulty':difficulty,'checked':verify(records)})
   render.append(records[0])
   if kp.endswith('744'):
    replay=run(script,difficulty,5,'--replay-source','all');verify(replay)
    result.append({'script':w['script'],'replay_checked':len(replay)})
 # Exhaust the registered generator's fraction syntax domain, including each form.
 sys.path.insert(0,str(HERE/'generator'))
 spec=importlib.util.spec_from_file_location('fixed_generator',HERE/'generator/generator.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
 combinations=0
 for a in range(2,16):
  for b in range(2,16):
   if a==b:continue
   for n in range(2,10):
    for form in g.FORMS:
     for text in (g.prose(g.statement(a,b,n,form)),g.solution(a,b,n,form)):
      assert fmt.scalable_fraction_parentheses(text)==text;fmt.validate_prose(text)
     combinations+=1
 (HERE/'generator-checks.json').write_text(json.dumps({'passed':True,'sample_checks':result,'registered_template_combinations':combinations},indent=2)+'\n')
 (HERE/'generator-render-input.json').write_text(json.dumps(render,indent=2)+'\n')
 print(json.dumps({'passed':True,'sample_records':sum(x.get('checked',0)+x.get('replay_checked',0) for x in result),'template_combinations':combinations}))
