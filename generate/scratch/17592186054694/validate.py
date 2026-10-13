"""Independent symbolic checks, complete source-bank replay, real radio grading."""
import copy,hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('line_table',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
x=sp.Symbol('x')
# Inspected source rasters: intercept and a second marked point establish each line.
OBSERVED={'q-54397':[[-1,0],[1,-2],[-1,1],[1,2],[1,0]],'q-59676':[[-1,2],[1,-2],[1,-1],[-2,4],[-1,1]],'q-71695':[[2,-2],[-2,2],[-1,2],[2,2],[1,2]]}
def save(name,v):(HERE/name).write_text(json.dumps(v,indent=2)+'\n')
def fingerprint(q):return g.fingerprint(q)
def check(r):
 q=r['question'];meta=r['generation'];p=meta['parameters'];m,b=p['m'],p['b'];assert p in g.candidates(meta['template'])
 assert r['knowledge_point']['db_id']==g.KP_ID and meta['version']==g.VERSION
 expected=g.generate('easy',meta['seed'],meta['template'],p,replay=meta['replay'])['question']
 # Content-addressed assets may replace local paths during preparation.
 actual=copy.deepcopy(q)
 if meta.get('asset_rewrites'):
  for local,published in meta['asset_rewrites'].items():
   actual[':question/worked-solution']=actual[':question/worked-solution'].replace(published,local)
   for a in actual[':question/answer-fields'][0][':answer-field/choices']:
    if a[':answer/value']==published:a[':answer/value']=local
 assert actual==expected,'Content/identity mismatch'
 assert fingerprint(q)==g.digest([str(m),str(b)])==meta['mathematical_fingerprint']
 f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1 and f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
 lines=[tuple(map(sp.Rational,v)) for v in meta['lines']];assert len(lines)==len(set(lines))==len(f[':answer-field/choices'])==5
 expected_poly=m*x+b
 keys=[a[':answer/id'] for a,line in zip(f[':answer-field/choices'],lines) if sp.expand(line[0]*x+line[1]-expected_poly)==0]
 assert keys==[f[':answer-field/correct'][1]]
 # Parse every substitution and the filled table independently of parameter helpers.
 calcs=re.findall(r'if \$x=(-?\d+)\$ then \$y=([^$]+)\$',q[':question/worked-solution']);assert len(calcs)==4
 for index,calc in calcs:
  left,right=calc.rstrip(',.').split('=');left=re.sub(r'(\d|\))\(',r'\1*(',left)
  assert sp.sympify(left)==sp.sympify(right)==expected_poly.subs(x,int(index))
 table=re.search(r'\| \$y\$ \| (\$[^\n]+)',q[':question/worked-solution'])[1];values=re.findall(r'\$(-?\d+)\$',table);assert list(map(int,values))==[m*i+b for i in range(4)]
 for i,a in enumerate(f[':answer-field/choices']):
  asset=Path(a[':answer/value']);asset=asset if asset.is_absolute() else Path('/media/jake/SSD/EDB/math')/asset
  assert asset.is_file()
  local=next((k for k,v in meta.get('asset_rewrites',{}).items() if v==a[':answer/value']),str(asset))
  if not meta['replay']:
   data=json.loads(Path(local+'.json').read_text());assert tuple(map(sp.Rational,(data['m'],data['b'])))==lines[i]
   assert [sp.Rational(v) for v in data['y_table']]==[lines[i][0]*n+lines[i][1] for n in range(4)]
   assert hashlib.sha256(asset.read_bytes()).hexdigest()==data['sha256']
   assert data['limits'][2]<min(map(int,data['y_table']))<=max(map(int,data['y_table']))<data['limits'][3]
 assert q[':question/difficulty']==':question.difficulty/easy'
 return r
def native(label,r):
 f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
 return {'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'complete image radio bank via application grader'} for a in f[':answer-field/choices']]}
def main():
 replays=[];mapping=[];inputs=[];review=[]
 for t,info in g.TEMPLATES.items():
  r=check(g.generate('easy',0,t,{'m':info['m'],'b':info['b']},replay=True));q=g.SOURCES[info['source']];f=q[':question/answer-fields'][0]
  assert [list(map(sp.Rational,p)) for p in r['generation']['lines']]==OBSERVED[info['source']]
  assert q[':question/problem']==r['question'][':question/problem']
  assert [a[':answer/value'] for a in f[':answer-field/choices']]==[a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
  correct=OBSERVED[info['source']].index([info['m'],info['b']])
  if ':answer-field/correct' in f:assert f[':answer-field/correct'][':answer/id']==f[':answer-field/choices'][correct][':answer/id']
  if ':question/worked-solution' in q:assert q[':question/worked-solution']==r['question'][':question/worked-solution']
  for i,(a,line) in enumerate(zip(f[':answer-field/choices'],OBSERVED[info['source']])):
   mapping.append({'source':info['source'],'field':f[':answer-field/key'],'answer_id':a[':answer/id'],'asset':a[':answer/value'],'parameters':{'m':info['m'],'b':info['b']},'observed_line':line,'marked_points':[[0,line[1]],[1,sum(line)]],'recipe':r['generation']['lines'][i],'correct':i==correct,'exact_complete_value_reproduced':True,'profile':info['source']})
  replays.append({'source':info['source'],'template':t,'complete_bank_match':True,'matched_choices':5,'total_choices':5,'matched_distractors':4,'total_distractors':4,'prompt_exact':True,'source_solution_exact':True if ':question/worked-solution' in q else None,'source_key_present':':answer-field/correct' in f,'missing_evidence':'none' if ':question/worked-solution' in q else 'key, solution and rating absent; graph-derived key and canonical-style solution authored'})
  inputs.append(native('source-'+t,r));review.append('## Source '+info['source']+'\n\n'+g.markdown(r))
 previews=[];fps=set()
 for t in g.TEMPLATES:
  for p in g.candidates(t):
   r=check(g.generate('easy',2025,t,p));assert check(g.generate('easy',99,t,p))['question']==r['question'];fps.add(fingerprint(r['question']));inputs.append(native(t+str(p),r));previews.append(r)
 assert len(fps)==len(previews)==18
 for level in ('moderate','hard'):
  try:g.generate(level)
  except ValueError:pass
  else:raise AssertionError('Unsupported difficulty accepted')
 for r in previews[:3]:review.append('## Variant\n\n'+g.markdown(r))
 save('previews.json',previews);save('source-choice-mapping.json',mapping);save('source-replay.json',{'passed':True,'basis':g.S['basis'],'complete_observed_banks':3,'complete_observed_banks_matched':3,'matched_answer_values':15,'total_answer_values':15,'matched_source_distractors':12,'total_source_distractors':12,'missing_or_extra_options':[],'profiles':replays,'fidelity_limits':'Two solutions/keys preserved exactly. q-59676 missing key, solution and difficulty; additions derived and identified. Replay reuses source rasters; generated raster style differs.'})
 save('native-input.json',inputs);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 (HERE/'review.md').write_text('\n\n'.join(review)+'\n')
 save('validation.json',{'passed':True,'supported_levels':['easy'],'unsupported_levels':['moderate','hard'],'exhaustive_instances':18,'distinct_bounded_tasks':18,'math':'exact linear polynomials, unique complete banks, printed substitutions and filled table, plot sidecars and hashes independently checked','native_grading':'all five choices for all 18 tuples and three source replays through course_academy_engine::learning::grade_field','source_fidelity':'15/15 complete graph values; 12/12 distractors; three complete banks; two exact original solutions and keys; missing third key/solution explicitly authored','hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'validate.py',HERE/'source.json')}})
 print('Validated 18 distinct bounded easy tasks and 3 complete source banks')
if __name__=='__main__':main()
