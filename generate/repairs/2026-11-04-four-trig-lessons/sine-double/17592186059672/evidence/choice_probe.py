from pathlib import Path
import collections,importlib.util,json,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from numeric_audit import Numeric,nodes,field_key
out={}
for path in sorted(HERE.glob('*-[0-9]*.json')):
 data=json.loads(path.read_text());groups=collections.defaultdict(list)
 for r in data:
  f=r['question'][':question/answer-fields'][0]
  if not f[':answer-field/type'].endswith('/radio'):continue
  choices=f[':answer-field/choices'];key=field_key(f)
  vals=[Numeric(nodes(a[':answer/value']),{}).evaluate() for a in choices]
  i=next(i for i,a in enumerate(choices) if a[':answer/value']==key)
  gen=r['generation'];family=gen.get('family') or gen['template']
  if gen.get('symbolic_terminal'):family+=':symbolic'
  for group in ('overall',family):
   groups[group].append({'position':i,'numeric_rank':sorted(vals).index(vals[i]),'key_length_rank':sorted(map(lambda a:len(a[':answer/value']),choices)).index(len(key)), 'negative':int(vals[i]<0)})
 stats={}
 for group,rows in groups.items():
  stats[group]={'n':len(rows),'fixed_position':dict(collections.Counter(r['position'] for r in rows)), 'fixed_numeric_rank':dict(collections.Counter(r['numeric_rank'] for r in rows)), 'text_length_rank':dict(collections.Counter(r['key_length_rank'] for r in rows)), 'negative_keys':sum(r['negative'] for r in rows)}
 out[path.name]=stats
(HERE/'choice-probes.json').write_text(json.dumps({'allowed_information':{'position':'option order only','numeric_rank':'numeric values of all options, without prompt; assumes prerequisite evaluation','text_length_rank':'bare-TeX string length only'},'results':out,'limitations':['Small subgroups can agree by chance; these counts alone do not establish a recurring shortcut. Numeric rank is not a pure surface rule for symbolic banks.']},indent=2)+'\n')
for name,stats in out.items():
 print(name,{g:v for g,v in stats.items() if g=='overall'})
