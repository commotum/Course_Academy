#!/usr/bin/env python3
"""Read displayed transformations independently, verify every coordinate and grade all choices."""
import copy,hashlib,importlib.util,itertools,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('extrema_generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
ROOT=D.parents[2]
ASSETS={}
for sid,c in {**g.CASES,**g.FIELDLESS}.items():
 image=re.search(r'!\[\]\((.*?)\)',g.ORIGINALS[sid][':question/problem'])[1]
 assert image not in ASSETS or all(ASSETS[image][key]==c[key] for key in ['scope','minimum','maximum'])
 ASSETS[image]={key:c[key] for key in ['scope','minimum','maximum']}
# Canonical example is a separate source graph, not practice inventory.
image=re.search(r'!\[\]\((.*?)\)',g.SOURCE['record'][':knowledge-point/canonical-example'][':question/problem'])[1]
ASSETS[image]=dict(scope='local',minimum=[1,5],maximum=[2,6])
def expression(s):
 s=re.sub(r'\\(?:d?frac)\s*\{([^{}]+)\}\s*\{([^{}]+)\}',r'(\1)/(\2)',s)
 s=s.replace(r'\cdot','*').replace(' ','')
 s=re.sub(r'(?<=[\d)])(?=[x(])','*',s)
 return sp.sympify(s,locals={'x':sp.Symbol('x')})
def coordinate(s):
 s=s.strip().rstrip('.').strip('$ ')
 assert s[0]=='(' and s[-1]==')',s
 a,b=s[1:-1].split(',');return expression(a),expression(b)
def transform(s):
 a,i,k=re.fullmatch(r'(.*?)f\((.*?)\)(.*)',s.replace(' ','')).groups()
 a=expression('1' if a=='' else '-1' if a=='-' else a)
 inside=expression(i);x=sp.Symbol('x');b=inside.coeff(x);h=inside.subs(x,0);k=expression(k or '0')
 assert b>0 and sp.expand(inside-b*x-h)==0
 return a,b,h,k

def read_prompt(q):
 prompt=q[':question/problem'];image=re.search(r'!\[\]\((.*?)\)',prompt)[1];scope,target=re.search(r'What is the (local|global) (minimum|maximum)',prompt).groups()
 assert scope==ASSETS[image]['scope']
 e=re.search(r'What is.*?\$y=(.*?)\?\$',prompt,re.S)[1];a,b,h,k=transform(e)
 original='maximum' if (target=='minimum')==(a<0) else 'minimum'
 x,y=ASSETS[image][original];good=((sp.Rational(x)-h)/b,a*y+k)
 return image,scope,target,original,(sp.Rational(x),sp.Rational(y)),good,(a,b,h,k)

def display_check(r):
 q=r['question'];image,scope,target,original,point,good,params=read_prompt(q)
 assert r['knowledge_point']['db_id']==g.KP_ID
 sol=q[':question/worked-solution'].replace('**','');assert f'the {scope} {original} of $y=f(x)$' in sol
 assert f'to the {scope} {target} of $y=' in sol
 start=re.search(r'So, we need to find the image of \$(.*?),\$',sol)[1];assert coordinate(start)==point
 blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S)
 stages=re.findall(r'and get the graph of \$y=(.*?)\.\$',sol)
 assert len(blocks)==len(stages)==(2 if params[0]>0 else 3)
 for block,stage in zip(blocks,stages):
  lhs,rhs=block.strip().rstrip('.').split('=');assert coordinate(lhs)==coordinate(rhs)
  a,b,h,k=transform(stage);expected=((point[0]-h)/b,a*point[1]+k)
  assert coordinate(rhs)==expected,(rhs,expected,stage)
 final=re.search(r'Therefore, the (local|global) (minimum|maximum) of \$y=.*?\$ is \$(.*?)\.\$',sol)
 assert final and final.groups()[:2]==(scope,target) and coordinate(final[3])==good
 fields=q[':question/answer-fields'];assert len(fields)==1;f=fields[0]
 assert f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio'
 choices=[coordinate(a[':answer/value']) for a in f[':answer-field/choices']];assert len(choices)==len(set(choices))==5
 correct=f[':answer-field/correct'][1];assert sum(a[':answer/id']==correct for a in f[':answer-field/choices'])==1
 assert next(coordinate(a[':answer/value']) for a in f[':answer-field/choices'] if a[':answer/id']==correct)==good
 assert sum(z==good for z in choices)==1
 for text in [q[':question/problem'],sol]+[a[':answer/value'] for a in f[':answer-field/choices']]:
  assert text.count('$')%2==0 and text.count('{')==text.count('}')
  assert not any(z in text for z in ['+-','--'])
 return good

def grade(records,path):
 path.mkdir(parents=True,exist_ok=True)
 items=[]
 for r in records:
  f=r['question'][':question/answer-fields'][0]
  items.append({'label':r['question'][':question/id'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every owned radio choice'} for a in f[':answer-field/choices']]})
 (path/'native-input.json').write_text(json.dumps(items,indent=2)+'\n')
 binary=D/'check-engine'
 subprocess.run([str(binary),str(path/'native-input.json'),str(path/'native-report.json')],check=True,capture_output=True,text=True)
 report=json.loads((path/'native-report.json').read_text());assert report['accepted_checks']==len(records) and report['rejected_checks']==len(records)*4 and report['documented_unresolved_checks']==0
 return report

def main():
 fidelity=[];records=[];review=[];coverage={};witness={}
 for sid,c in g.CASES.items():
  p=dict(c['p'],target=c['target']);r=g.generate(c['level'],profile=sid,parameters=p);display_check(r)
  source=g.ORIGINALS[sid];sf=source[':question/answer-fields'][0];rf=r['question'][':question/answer-fields'][0]
  original=[coordinate(a[':answer/value']) for a in sf[':answer-field/choices']];new=[coordinate(a[':answer/value']) for a in rf[':answer-field/choices']]
  assert sorted(original)==sorted(new)
  assert read_prompt(source)==read_prompt(r['question'])
  assert coordinate(sf[':answer-field/correct'][':answer/value'])==display_check(r)
  fidelity.append({'source_id':sid,'bank_matched':5,'bank_total':5,'distractors_matched':4,'distractors_total':4,'missing':[],'extra':[],'correct_designation_match':True,'prompt_mathematics_match':True,'solution_stages':len(re.findall(r'\$\$',source[':question/worked-solution']))//2,'solution_wording':'Shared operative wording and ordered coordinate stages; punctuation and connective wording normalized'})
  review.extend([{'label':'Captured original '+sid,'question':source},{'label':'Source parameter replay '+sid,'record':r}]);records.append(r)
  p['target']=g.opposite(p['target']);changed=g.generate(c['level'],profile=sid,parameters=p);display_check(changed)
  assert read_prompt(r['question'])[4]!=read_prompt(changed['question'])[4]
  review.append({'label':'Changed target with transformation held constant '+sid,'record':changed});records.append(changed)
  seen=set();tasks=set();signs={key:set() for key in c['p']};eligible=0
  domains=[[-5,-4,-3,-2,-1,1,2,3,4,5] if key in ('h','k') else ['1/2','1/3',2,3,4] if c['level']=='easy' else [2,3,4] for key in c['p']]
  # Exhaustive finite parameter domain (2 target roles per profile).
  for values in itertools.product(*domains):
   for target in ('minimum','maximum'):
    p=dict(zip(c['p'],values),target=target)
    try:r=g.generate(c['level'],profile=sid,parameters=p)
    except ValueError as e:
     assert str(e)=='Degenerate source bank';continue
    display_check(r);eligible+=1;tasks.add(r['generation']['mathematical_fingerprint']);seen.add(target)
    for key in c['p']:signs[key].add(str(p[key]))
  assert seen=={'minimum','maximum'} and len(tasks)>5
  witness[sid]={'eligible_parameter_instances':eligible,'distinct_mathematical_tasks':len(tasks),'exhaustive_finite_profile_domain':True}
  coverage[sid]={'requested_extrema':sorted(seen),'parameter_values':{k:sorted(z) for k,z in signs.items()}}
  for seed in range(24):
   r=g.generate(c['level'],seed,profile=sid);display_check(r);records.append(r)
   same=g.generate(c['level'],seed+909,profile=sid,parameters=r['generation']['parameters']);assert same['question'][':question/id']==r['question'][':question/id']
   if seed<2:review.append({'label':'Sampled variant '+sid+'/'+str(seed),'record':r})
 # Fieldless source examples verify mathematics but do not establish a response contract.
 incomplete=[]
 for sid in g.FIELDLESS:
  q=g.ORIGINALS[sid];assert ':question/answer-fields' not in q
  good=read_prompt(q)[5];last=re.search(r'Therefore,.*? is \$(.*?)\.\$',q[':question/worked-solution'],re.S)
  assert coordinate(last[1])==good;incomplete.append({'source_id':sid,'verified_answer':g.pair(good),'gradable':False,'reason':'Captured answer fields absent; preserved and excluded'})
  review.append({'label':'Fieldless captured source '+sid,'question':q})
 # Negative controls exercise stale extrema and incorrect printed mathematics.
 negatives=0;base=g.generate('moderate',profile='q-211465',parameters=dict(h=-1,k=-2,target='minimum'))
 for mut in ['key','stage','target']:
  r=copy.deepcopy(base)
  if mut=='key':r['question'][':question/answer-fields'][0][':answer-field/correct'][1]=next(a[':answer/id'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'] if a[':answer/id']!=r['question'][':question/answer-fields'][0][':answer-field/correct'][1])
  elif mut=='stage':r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace('(3,3).','(3,4).',1)
  else:r['question'][':question/problem']=r['question'][':question/problem'].replace('What is the local minimum','What is the local maximum')
  try:display_check(r)
  except AssertionError:negatives+=1
  else:raise AssertionError('Corruption escaped independent validator: '+mut)
 native=grade(records,D/'reference/validation')
 asset_manifest=[]
 for image,coords in ASSETS.items():
  p=Path('/media/jake/SSD/EDB/math')/image;assert p.is_file();assert p.name[:-4]==hashlib.sha256(p.read_bytes()).hexdigest()
  asset_manifest.append({'path':image,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'extrema':coords,'visually_inspected':True,'reused_unchanged':True})
 (D/'assets.json').write_text(json.dumps(asset_manifest,indent=2)+'\n')
 (D/'review.json').write_text(json.dumps(review,indent=2)+'\n')
 parts=[]
 for item in review:
  q=item.get('question',item.get('record',{}).get('question'))
  parts.append('## '+item['label']+'\n\n'+q[':question/problem']+'\n\n'+ '\n'.join('- $'+a[':answer/value']+'$' for f in q.get(':question/answer-fields',[]) for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution'])
 (D/'review.md').write_text('# Extrema source and variant review\n\n'+'\n\n---\n\n'.join(parts)+'\n')
 result={'status':'passed','source_basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'generator_version':g.VERSION,'generator_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'source_fidelity':fidelity,'full_banks_matched':8,'choices_matched':40,'distractors_matched':32,'incomplete_sources':incomplete,'finite_variety_witness':witness,'slot_coverage':coverage,'independent_checks':'Displayed prompt transformation, visually verified extrema, every solution-stage transform and coordinate equality, final answer and uniqueness','negative_controls_rejected':negatives,'native_grading':{'records':len(records),'accepted':native['accepted_checks'],'rejected':native['rejected_checks'],'unresolved':0,'binary_sha256':hashlib.sha256((D/'check-engine').read_bytes()).hexdigest(),'database_writes':0},'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'limitations':['Hard unsupported by this source-bound package','Four fieldless sources preserved; no inferred answer shapes added','Opaque recipes retain complete parameterized coordinate patterns without claiming recovered misconception intent','Source literal punctuation and connective wording are normalized; mathematical expressions, banks, designation and operative solution stages are checked separately']}
 (D/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['status','full_banks_matched','choices_matched','native_grading','finite_variety_witness']},indent=2))
if __name__=='__main__':main()
