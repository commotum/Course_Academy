"""Independent circulation / rendered-data / proposition / real grader checks."""
import copy,hashlib,importlib.util,json,re,subprocess,sys,uuid
from pathlib import Path
import sympy as sp
import numpy as np
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
spec=importlib.util.spec_from_file_location('curl_generator',P.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
ENGINE=ROOT/'generate/runs/current/check-engine'
def save(path,x):Path(path).write_text(json.dumps(x,indent=2)+'\n')
def checks(rec):
 out=[]
 for i,f in enumerate(rec['question'][':question/answer-fields']):
  for a in f[':answer-field/choices']:
   out.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete source bank / field key'})
 return {'label':rec['question'][':question/id'],'record':rec,'checks':out}
def native(records,path):
 path=Path(path);path.mkdir(parents=True,exist_ok=True);save(path/'native-input.json',[checks(r) for r in records]);r=subprocess.run([str(ENGINE),str(path/'native-input.json'),str(path/'native-report.json')],check=True,capture_output=True,text=True,timeout=55);(path/'native.log').write_text(r.stdout+r.stderr)
 report=json.load(open(path/'native-report.json'));assert report['documented_unresolved_checks']==0;return report

def validate(rec,asset_root=None):
 q=rec['question'];m=rec['generation'];sid=m['template'];a,b,c,d,u,v=map(sp.Rational,m['parameters'])
 # Independently integrate circulation around counterclockwise unit square:
 # bottom + right + top + left, rather than importing generator's curl helper.
 t=sp.symbols('t');circ=sp.integrate(a*t+u,(t,0,1))+sp.integrate(c+d*t+v,(t,0,1))-sp.integrate(a*t+b+u,(t,0,1))-sp.integrate(d*t+v,(t,0,1))
 assert circ==c-b
 prompt=q[':question/problem'];lines=[line for line in prompt.splitlines() if re.match(r'(?:- \*\*)?(?:I|II|III|IV)\.',line)];assert len(lines)==4
 flags=[]
 for line in lines:
  if 'irrotational' in line:flag=(circ!=0) if 'not ' in line else (circ==0)
  elif 'positive' in line:flag=circ>0
  elif 'negative' in line:flag=circ<0
  elif r'\ne' in line:flag=circ!=0
  else:flag=circ==0
  flags.append(bool(flag))
 for f in q[':question/answer-fields']:
  bank=f[':answer-field/choices'];values=[a[':answer/value'] for a in bank];assert len(values)==len(set(values));correct=next(a[':answer/value'] for a in bank if a[':answer/id']==f[':answer-field/correct'][1])
  if f[':answer-field/type'].endswith('/radio'):
   selected=[k for k,v in zip(('I','II','III','IV'),flags) if v];expected=' and '.join(selected)+' only';assert len(bank)==5
  else:expected=str(flags[('I','II','III','IV').index(f[':answer-field/key'])]).lower();assert set(values)=={'true','false'}
  assert correct==expected
  assert '$' not in correct and all(a[':answer/type']==':answer.type/text' for a in bank)
 if not m['replay']:
  for k,vv in zip(('I','II','III','IV'),flags):assert f'Statement {k} is {str(vv).lower()}.' in q[':question/worked-solution']
  refs=re.findall(r'!\[.*?\]\((.*?)\)',prompt);assert len(refs)==1
  asset=Path(refs[0]);asset=asset if asset.is_absolute() else Path(asset_root or '/media/jake/SSD/EDB/math')/asset
  assert hashlib.sha256(asset.read_bytes()).hexdigest()==m['assets'][0]['sha256']
  data=json.load(open(m['assets'][0]['data']));grid=np.array(data['grid']);X,Y=np.meshgrid(grid,grid)
  assert np.allclose(np.array(data['U']),float(a)*X+float(b)*Y+float(u));assert np.allclose(np.array(data['V']),float(c)*X+float(d)*Y+float(v))
  assert data['scale']==3*max(1,float(np.max(np.hypot(np.array(data['U']),np.array(data['V'])))))
  for s in (prompt,q[':question/worked-solution']):assert s.count('$')%2==0 and '{{' not in s and s.count('{')==s.count('}')
 assert q[':question/difficulty']==g.SOURCES[sid][':question/difficulty'][':db/ident']
 assert rec['knowledge_point']['db_id']==g.KP_ID and ':question/math-academy-id' not in q
 ids=[q[':question/id']]+[f[':answer-field/id'] for f in q[':question/answer-fields']]+[a[':answer/id'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']];assert len(ids)==len(set(ids));[uuid.UUID(i) for i in ids]
 return g.canonical_key(m['parameters'])

def main():
 reports=[];records=[];banks=options=0
 for sid,source in g.SOURCES.items():
  level=source.get(':question/difficulty',{}).get(':db/ident','').split('/')[-1]
  if level not in g.SUPPORTED:
   # Classify and audit unrated source but never synthesize its difficulty.
   flags=g.truth(sid,g.REALIZATIONS[sid][2]-g.REALIZATIONS[sid][1]);fields=g.fields(sid,flags,'audit-unrated')
   rec={'knowledge_point':{'title':g.TITLE},'question':{':question/id':source[':question/id'],':question/problem':source[':question/problem'],':question/answer-fields':fields},'generation':{'template':sid}}
  else:
   rec=g.generate(level,template=sid,replay=True);validate(rec)
   assert rec['question'][':question/problem']==source[':question/problem'];assert rec['question'][':question/worked-solution']==source[':question/worked-solution']
  for old,new in zip(source[':question/answer-fields'],rec['question'][':question/answer-fields']):
   assert old[':answer-field/key']==new[':answer-field/key'] and old[':answer-field/type'][':db/ident']==new[':answer-field/type']
   oldvals=sorted(a[':answer/value'] for a in old[':answer-field/choices']);newvals=sorted(a[':answer/value'] for a in new[':answer-field/choices']);assert oldvals==newvals
   assert old[':answer-field/correct'][':answer/value']==next(a[':answer/value'] for a in new[':answer-field/choices'] if a[':answer/id']==new[':answer-field/correct'][1]);banks+=1;options+=len(oldvals)
  reports.append({'source_id':sid,'level':level or 'unrated','complete_banks_matched':len(source[':question/answer-fields']),'missing_options':[],'extra_options':[],'unscaled_source_plot_reused':True});records.append(rec)
 # Exhaust every declared coefficient-ratio boundary, for every rated profile.
 coverage={};variants=[]
 for sid,source in g.SOURCES.items():
  level=source.get(':question/difficulty',{}).get(':db/ident','').split('/')[-1]
  if level not in g.SUPPORTED:continue
  family=g.FAMILIES[sid];seen=set();slots=set()
  for seed in range(128):
   params=g.parameters(sid,__import__('random').Random(seed));slots.add(tuple(params));seen.add(g.canonical_key(params))
   # Render each ratio once. Validate numerical plot data at every ratio.
   if any(r['generation']['template']==sid and r['generation']['canonical_field']==g.canonical_key(params) for r in variants):continue
   rec=g.generate(level,seed,template=sid,params=params);validate(rec);assert rec==g.generate(level,seed,template=sid,params=params);variants.append(rec)
  coverage[sid]={'family':family,'sampled_parameter_tuples':sorted(map(list,slots)),'normalized_fields':len(seen),'positive_scale_collapses':len(slots)-len(seen)}
 # Explicit held-data proposition check: changing positive to negative direction
 # must change its key, while permuting source statements must retain field keys.
 probe=copy.deepcopy(next(r for r in variants if r['generation']['template']=='q-105669'));probe['question'][':question/problem']=probe['question'][':question/problem'].replace('positive $z$','negative $z$')
 try:validate(probe)
 except AssertionError:pass
 else:raise AssertionError('Stale direction key was not rejected')
 report=native(records+variants,P/'reference/validation')
 save(P/'source-fidelity.json',{'passed':True,'banks_matched':banks,'banks_total':banks,'options_matched':options,'options_total':options,'sources':reports,'source_math_vs_numeric_replay':'qualitative diagram replay only; exact original coefficients unavailable','solution_exception':'q-105664 contains contradictory clockwise sentence; source retained verbatim for fidelity replay, corrected variants use counterclockwise'})
 save(P/'coverage.json',coverage);save(P/'review-variants.json',variants)
 save(P/'review.md','' if False else {'source_contact':'source-contact.png','variants':len(variants),'source_layout_preserved':True})
 save(P/'validation.json',{'passed':True,'version':g.VERSION,'source_practice_records':len(g.SOURCES),'rated_profiles':13,'variant_records':len(variants),'circulation_and_rendered_arrays_checked':True,'stale_direction_key_rejected':True,'source_banks_matched':banks,'source_options_matched':options,'native_accepted':report['accepted_checks'],'native_rejected':report['rejected_checks'],'native_unresolved':0,'grader_executable_sha256':hashlib.sha256(ENGINE.read_bytes()).hexdigest()})
 print(json.dumps(json.load(open(P/'validation.json'))))
if __name__=='__main__':main()
