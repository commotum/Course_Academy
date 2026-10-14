#!/usr/bin/env python3
"""Independent printed-math, all-source, native-engine and PNG validation."""
import concurrent.futures,copy,hashlib,importlib.util,itertools,json,os,re,subprocess,sys,tempfile
from pathlib import Path
from collections import Counter
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
from PIL import Image
HERE=Path(__file__).resolve().parent
SCRIPT=HERE.with_suffix('.py')
spec=importlib.util.spec_from_file_location('perpendicular',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X,Y=sp.symbols('x y')
TRANS=standard_transformations+(implicit_multiplication_application,)
def parse(s):
 s=s.strip().rstrip('.,').replace(r'\left','').replace(r'\right','').replace('&','').replace(' ','')
 s=re.sub(r'\\(?:d?frac)\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',s)
 s=s.replace('{','').replace('}','')
 return parse_expr(s,local_dict={'x':X,'y':Y},transformations=TRANS)
def equation(s):
 if '=' not in s:return parse(s)
 l,r=s.split('=');return sp.expand(parse(l)-parse(r))
def canonical(expr):
 p=sp.Poly(sp.expand(expr),X,Y);return sp.expand(expr/p.LC()) if expr!=0 else expr

def display_readback(record,format_check=True):
 assert set(record['knowledge_point'])=={'db_id','id','title'}
 q=record['question'];meta=record['generation'];prompt=q[':question/problem']
 # First actual printed supplied equation, not generation values.
 math=re.findall(r'\$([^$]+)\$',prompt)
 supplied=next(s for s in math if s.startswith(('y=','y =')) and 'mx+b' not in s and len(s.replace(' ',''))>2)
 given=equation(supplied);a=-given.coeff(X)/given.coeff(Y);c=-given.subs({X:0,Y:0})/given.coeff(Y)
 if meta['template'].startswith('graph'):
  if 'sidecar' in meta['plots']:
   plotted=json.loads(Path(meta['plots']['sidecar']).read_text());u,v=sp.Rational(plotted['u']),sp.Rational(plotted['v'])
   assert sp.Rational(plotted['a'])==a and sp.Rational(plotted['c'])==c
   assert sp.Rational(plotted['m'])==-1/a and sp.Rational(plotted['b'])==v+u/a
   check_png(Path(meta['plots']['prompt']),plotted)
  else:u,v=map(sp.Rational,ORIGINAL_GEOMETRY[meta['source_id']]['point'])
 else:
  point=re.search(r'\(([-0-9]+),([-0-9]+)\)',prompt);assert point;u,v=map(sp.Rational,point.groups())
 m=-1/a;b=v-m*u;expected=Y-m*X-b
 fields=q[':question/answer-fields'];assert len(fields)==1
 f=fields[0];kind=f[':answer-field/type'].split('/')[-1]
 if kind=='blank':assert '{{'+f[':answer-field/key']+'}}' in prompt
 choices=f.get(':answer-field/choices',[])
 objects=[canonical(equation(z[':answer/value'])) if kind=='radio' and not meta['template'].startswith('intercept') else equation(z[':answer/value']) for z in choices]
 assert len(set(map(str,objects)))==len(objects),'equivalent bank members'
 if ':answer-field/correct' in f:
  correct=next(z for z in choices if z[':answer/id']==f[':answer-field/correct'][1]);obj=equation(correct[':answer/value'])
  assert sp.simplify(obj-b if meta['template'].startswith('intercept') else obj-(m*X+b) if kind=='blank' else canonical(obj)-canonical(expected))==0
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution']
  # Read claimed slope/point/intercept from the actual prose too.
  slope=re.search(r'must have a slope of \$([^$]+)\.\$',sol);assert slope and parse(slope.group(1))==m
  assert '$m='+g.tex(m)+'$' in sol
  if meta['template'].startswith('graph_intercept'):
   assert '$'+g.tex(b)+'.$' in sol
  else:
   assert '({x}_{1},{y}_{1})=('+g.tex(u)+','+g.tex(v)+').' in sol
  block=sol.split('$$')[1]
  if r'\begin{aligned}' in block:
   raw_rows=block.strip().removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}').split(r'\\')
   # Every ordered row independently equals the required entire equation.
   for row in raw_rows:
    row=row.replace('{y}_{1}',g.tex(v)).replace('{x}_{1}',g.tex(u))
    row=row.replace('m(',g.tex(m)+'(')
    assert canonical(equation(row))==canonical(expected),(row,expected)
   assert len(raw_rows)==(5 if u<0 else 4)
   # The actual operation sequence must remain formal/substitute/[signed rewrite]/distribute/collect.
   assert r'y-{y}_{1} & =m(x-{x}_{1})' in block
   assert g.lhs(v,True)+' & ='+g.tex(m)+'('+g.sub(u)+')' in block
   assert g.lhs(v)+' & ='+g.rhs(m,-m*u) in block
   assert 'y & ='+g.rhs(m,b) in block
  else:assert canonical(equation(block.strip()))==canonical(expected)
  if meta['template'].startswith('intercept'):assert 'Therefore, $b='+g.tex(b)+'.$' in sol
 if format_check:
  texts=[prompt,q.get(':question/worked-solution','')]+[z[':answer/value'] for z in choices]
  for text in texts:
   assert not any(ord(ch)<32 and ch not in '\n\t' for ch in text),'control characters'
   assert text.count('$')%2==0,'unbalanced dollar'
   depth=0
   for ch in text:
    if ch=='{':depth+=1
    if ch=='}':depth-=1
    assert depth>=0
   assert depth==0
 return {'a':str(a),'u':str(u),'v':str(v),'m':str(m),'b':str(b)}

def check_png(path,p):
 im=Image.open(path).convert('RGB');assert im.size==tuple(p['size'])
 origin=p['origin_pixel'];scale=p['unit_pixels'];assert scale>=7,'insufficient reading resolution'
 def near(x,y,color):
  px,py=origin[0]+float(sp.Rational(x))*scale,im.height-origin[1]-float(sp.Rational(y))*scale
  if not(4<px<im.width-4 and 4<py<im.height-4):return False
  for i in range(int(px)-3,int(px)+4):
   for j in range(int(py)-3,int(py)+4):
    r,b,c=im.getpixel((i,j))
    if color=='red' and r>150 and b<140 and c<140:return True
    if color=='blue' and c>150 and r<140 and b<140:return True
  return False
 assert near(p['u'],p['v'],'red'),'marked point absent from actual PNG'
 lo,hi=p['bounds']
 for slope,intercept,color in [(p['a'],p['c'],'blue'),(p['m'],p['b'],'red')]:
  a,c=float(sp.Rational(slope)),float(sp.Rational(intercept))
  points=[(lo+(hi-lo)*i/20,a*(lo+(hi-lo)*i/20)+c) for i in range(2,19)]
  visible=[(x,y) for x,y in points if lo+.8<y<hi-.8]
  assert len(visible)>=2
  assert sum(near(x,y,color) for x,y in visible)>=2,'actual colored line does not align with equation'
 for box in p['text_boxes']:
  x,y,w,h=box['bbox']
  if box['text'] in ('$l_1$','$l_2$'):
   assert (x+w<=origin[0]-4 or x>=origin[0]+4) and (y+h<=origin[1]-4 or y>=origin[1]+4),'line-name glyph overlaps a zero axis'
  assert x>=0 and y>=0 and x+w<=im.width and y+h<=im.height,'clipped reading label'
  crop=im.crop((int(x),int(im.height-y-h),int(x+w)+1,int(im.height-y)+1))
  assert any(min(pixel)<180 for pixel in crop.getdata()),'empty native label box'
 assert abs(float(sp.Rational(p['a']))*float(sp.Rational(p['m']))+1)<1e-12

ORIGINAL_GEOMETRY={
 'q-213914':{'point':['0','2'],'source_origin_px':[169,256],'source_marker_px':[170,219],'cue':'l2 y-intercept labelled 2, blue l1/red l2 meet on y axis; unit ticks without coordinate labels; no right-angle marker'},
 'q-44604':{'point':['-4','10'],'source_origin_px':[169,256],'source_marker_px':[95,69],'cue':'dashed guides to -4 and 10; unlabelled l2 intercept not independently read; blue l1 through origin, red l2; crossing near x>0; no right-angle marker'},
 'q-237193':{'point':['4','2'],'source_origin_px':[169,163],'source_marker_px':[294,100],'cue':'dashed guides to 4 and 2, red l2 rising/blue l1 falling; crossing left of y axis; no right-angle marker'},
 'q-44337':{'point':['0','6'],'source_origin_px':[169,256],'source_marker_px':[170,144],'cue':'l2 y-intercept labelled 6, unit tick marks, blue l1 rising/red l2 falling; crossing right of y axis; no right-angle marker'},
}

def native_fixture(label,r):
 f=r['question'][':question/answer-fields'][0]
 if ':answer-field/choices' not in f or ':answer-field/correct' not in f:return None
 correct=f[':answer-field/correct'][1];checks=[]
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':z[':answer/id'],'expected':'accepted' if z[':answer/id']==correct else 'rejected','purpose':'select every option in complete bank'} for z in f[':answer-field/choices']]
 else:
  z=next(z for z in f[':answer-field/choices'] if z[':answer/id']==correct);answer=z[':answer/value'];obj=parse(answer)
  # Unreduced common denominator and reversed term order remain genuinely distinct entries.
  if obj.has(X):
   slope=sp.expand(obj).coeff(X);b=obj.subs(X,0);den=int(sp.ilcm(slope.q,b.q));alt=r'\frac{'+str(b*den)+('+' if slope>0 else '')+str(slope*den)+'x}{'+str(den)+'}'
   reordered=g.tex(b)+('+' if slope>0 else '')+g.tex(slope)+'x'
  else:alt=r'\frac{'+str(obj*2)+'}{2}';reordered=alt
  checks=[{'submitted':answer,'expected':'accepted','purpose':'canonical fragment'}, {'submitted':alt,'expected':'accepted','purpose':'unreduced/common denominator fragment'}, {'submitted':reordered,'expected':'accepted','purpose':'reordered equivalent fragment'}, {'submitted':g.tex(obj+1) if not obj.has(X) else answer+'+1','expected':'rejected','purpose':'incorrect fragment'}]
 return {'label':label,'record':r,'checks':checks}

def main():
 source=json.loads((HERE/'source.json').read_text());assert source==json.loads(Path('generate/runs/current/refresh-2026-10-14/sources/17592186175922.json').read_text())
 cases=[];reviews=[];fixtures=[];fidelity=[];default_families=Counter();unique={k:set() for k in ('easy','moderate','hard')}
 for sid,q in g.SOURCES.items():
  template=next(k for k,v in g.TEMPLATES.items() if v[2]==sid);level=g.TEMPLATES[template][0];p=g.ANCHORS[sid]
  case={'source_id':sid,'template':template,'level':level,'parameters':p,'bank_profile':'raw:'+sid,'level_basis':'authored inference from graph cue' if ':question/difficulty' not in q else 'observed'};cases.append(case)
  r=g.generate(level,17,template,parameters=p,profile='raw:'+sid);rawq=r['question'];display_readback(r)
  for key in (':question/problem',':question/worked-solution',':question/difficulty'):
   assert (key in q)==(key in rawq),(sid,key,'presence')
   if key in q and key!=':question/difficulty':assert q[key]==rawq[key],(sid,key,'fidelity')
   if key==':question/difficulty' and key in q:assert q[key][':db/ident']==rawq[key]
  old=q[':question/answer-fields'][0];new=rawq[':question/answer-fields'][0]
  for key in (':answer-field/choices',':answer-field/correct'):assert (key in old)==(key in new),(sid,key,'presence')
  assert new[':answer-field/key']==old[':answer-field/key'] and new[':answer-field/type']==old[':answer-field/type'][':db/ident']
  if ':answer-field/choices' in old:
   oldvalues=[canonical(equation(a[':answer/value'])) if new[':answer-field/type'].endswith('/radio') and not template.startswith('intercept') else equation(a[':answer/value']) for a in old[':answer-field/choices']]
   newvalues=[canonical(equation(a[':answer/value'])) if new[':answer-field/type'].endswith('/radio') and not template.startswith('intercept') else equation(a[':answer/value']) for a in new[':answer-field/choices']]
   assert sorted(map(str,oldvalues))==sorted(map(str,newvalues)),(sid,'bank')
   assert sorted(a[':answer/value'] for a in old[':answer-field/choices'])==sorted(a[':answer/value'] for a in new[':answer-field/choices']),(sid,'exact bank formatting')
  if ':answer-field/correct' in old:
   correct=next(z for z in new[':answer-field/choices'] if z[':answer/id']==new[':answer-field/correct'][1]);assert equation(correct[':answer/value'])==equation(old[':answer-field/correct'][':answer/value'])
  fidelity.append({'source_id':sid,'prompt_exact':True,'solution_exact':True if ':question/worked-solution' in q else None,'difficulty_presence_exact':True,'attribute_presence_exact':True,'choices_matched':len(old.get(':answer-field/choices',[])),'choice_strings_exact':True if ':answer-field/choices' in old else None,'correct_designation_matched':':answer-field/correct' in old})
  reviews.append({'label':'Original parameter replay '+sid,'record':r});fixture=native_fixture(sid,r)
  if fixture:fixtures.append(fixture)
  completed=g.generate(level,18,template,parameters=p,profile='source:'+sid);display_readback(completed)
  reviews.append({'label':'Completed historical bank; evidence-only '+sid,'record':completed});fixtures.append(native_fixture('completed '+sid,completed))
  for i in range(2):
   normal=g.generate(level,301+i,template);display_readback(normal);reviews.append({'label':'Normal method-derived '+template+' '+str(i),'record':normal});fixtures.append(native_fixture(template+' '+str(i),normal))
  # Each public evidence profile supports changed coefficients through same math/masks.
  changed=dict(p);changed['c']=str(-sp.Rational(p['c'])) if p['c']!='0' else '1'
  replay=g.generate(level,42,template,parameters=changed,profile='raw:'+sid);display_readback(replay)
  changed=dict(p,u=str(-sp.Rational(p['u'])),v=str(-sp.Rational(p['v'])))
  target_replay=g.generate(level,43,template,parameters=changed,profile='source:'+sid);display_readback(target_replay)
  assert target_replay['generation']['mathematical_fingerprint']!=r['generation']['mathematical_fingerprint']
  fixtures.append(native_fixture('changed marked/supplied point '+sid,target_replay))
 for level in unique:
  for seed in range(120):
   r=g.generate(level,seed);display_readback(r);default_families[r['generation']['template']]+=1;unique[level].add(r['generation']['mathematical_fingerprint'])
   if seed<10:fixtures.append(native_fixture('default '+level+' '+str(seed),r))
 assert set(default_families)==set(g.TEMPLATES)
 invalid_checks=0
 for level,t,p in [('easy','graph_intercept_blank',dict(a='1/2',c='0',u='0',v='2')),('moderate','graph_point_blank',dict(a='4',c='0',u='1',v='2')),('moderate','graph_point_radio',dict(a='2/3',c='0',u='2',v='4')),('hard','intercept_blank',dict(a='4',c='0',u='4',v='2')),('hard','text_equation_blank',dict(a='4',c='0',u='0',v='2')),('hard','text_equation_blank',dict(a='6',c='0',u='6',v='2'))]:
  try:g.generate(level,template=t,parameters=p)
  except ValueError:invalid_checks+=1
  else:raise AssertionError('invalid explicit scope accepted')
 assert invalid_checks==6
 # Same parameters, option-order and seed independent IDs; unused c excluded from task identity.
 for t,(level,_,_) in g.TEMPLATES.items():
  r=g.generate(level,18,t);p=r['generation']['parameters'];s=g.generate(level,999,t,parameters=p);assert r['question'][':question/id']==s['question'][':question/id']
  changed=dict(p,c=str(sp.Rational(p['c'])+1))
  if abs(sp.Rational(changed['c']))<=12:
   try:s=g.generate(level,1,t,parameters=changed)
   except ValueError:continue
   assert r['generation']['mathematical_fingerprint']==s['generation']['mathematical_fingerprint']
   assert r['question'][':question/id']!=s['question'][':question/id']
 # Fresh concurrent identical/different renders: isolated output dir, no cached files.
 with tempfile.TemporaryDirectory(dir=HERE,prefix='concurrent-') as td:
  ps=[dict(a='-4',c='-3',u='4',v='2'),dict(a='-4',c='-3',u='4',v='2'),dict(a='3',c='2',u='-6',v='4'),dict(a='-2',c='3',u='6',v='-4')]
  with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:assets=list(pool.map(lambda p:g.render_plots(p,'graph_point_blank',td),ps))
  assert assets[0]==assets[1]
  for asset,p in zip(assets,ps):
   side=json.loads(Path(asset['sidecar']).read_text());assert all(side[k]==str(sp.Rational(p[k])) for k in p);check_png(Path(asset['prompt']),side)
  assert not list(Path(td).glob('.render-*'))
 # Targeted native seed1 regression: both line-name bboxes must clear each zero axis.
 label_target=g.generate_easy(1)
 label_data=json.loads(Path(label_target['generation']['plots']['sidecar']).read_text())
 label_regressions=[]
 check_png(Path(label_target['generation']['plots']['prompt']),label_data)
 for label,axis in itertools.product(('$l_1$','$l_2$'),(0,1)):
  mutated=copy.deepcopy(label_data)
  box=next(z for z in mutated['text_boxes'] if z['text']==label)
  box['bbox'][axis]=mutated['origin_pixel'][axis]-2
  try:check_png(Path(label_target['generation']['plots']['prompt']),mutated)
  except AssertionError as error:
   assert 'line-name glyph overlaps' in str(error)
   label_regressions.append(label+' axis'+str(axis))
  else:raise AssertionError('line-name axis overlap mutation missed')
 (HERE/'label-clearance-regression.json').write_text(json.dumps({'target':label_target,'native_sidecar':label_data,'axis_overlap_mutations_rejected':label_regressions},indent=2)+'\n')
 # Mutations must fail printed-stage and formatting validators, independent of metadata.
 baseline=g.generate_hard(304,template='text_equation_blank')
 mutations=[]
 for name,mutator in [('control',lambda s:s+'\f'),('distribution',lambda s:s.replace(' & ='+g.rhs(*((lambda a,c,u,v,m,b:(m,-m*u))(*g.values(baseline['generation']['parameters'])))),' & =99x+1')),('conclusion',lambda s:s.replace('y & =','y & =1+'))]:
  r=copy.deepcopy(baseline);r['question'][':question/worked-solution']=mutator(r['question'][':question/worked-solution'])
  try:display_readback(r)
  except (AssertionError,ValueError):mutations.append(name)
  else:raise AssertionError('mutation missed '+name)
 (HERE/'native-fixtures.json').write_text(json.dumps([f for f in fixtures if f],indent=2)+'\n')
 subprocess.run(['generate/runs/current/check-engine',str(HERE/'native-fixtures.json'),str(HERE/'native-report.json')],check=True)
 report={'status':'passed','script_sha256':hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),'source_count':7,'source_fidelity':fidelity,'matched_source_options':sum(x['choices_matched'] for x in fidelity),'matched_source_correct_refs':sum(x['correct_designation_matched'] for x in fidelity),'raw_missing_native_ungradeable':['q-213914: no choices/correct','q-44604: no correct ref'],'source_distractors_matched':8,'source_distractors_total':8,'inferred_source_distractors_matched':4,'inferred_source_distractors_total':4,'normal_samples':360,'distinct_assessed_tasks_sampled':{k:len(v) for k,v in unique.items()},'default_family_counts':dict(default_families),'invalid_explicit_scope_rejections':invalid_checks,'explicit_changed_point_checks':7,'concurrent_fresh_render_checks':4,'line_label_axis_overlap_regressions':label_regressions,'mutation_regressions':mutations,'native':json.loads((HERE/'native-report.json').read_text()),'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':g.matplotlib.__version__},'unresolved':['Historical q44337/q44606 distractor intent is opaque; complete structural evidence profiles are ineligible for learning.','Unrated missing fields/solution/refs cannot establish original native grading or observed difficulty.'],'writes':'private evidence only; no DB operations'}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n');(HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(HERE/'review.json').write_text(json.dumps(reviews,indent=2)+'\n')
 md=[]
 for item in reviews:
  r=item['record'];plots=r['generation']['plots'];text=g.markdown(r)
  if plots.get('original'):text=text.replace(plots['original'],plots['prompt'])
  md.extend(['## '+item['label'],'',text,''])
 (HERE/'review.md').write_text('\n'.join(md))
 (HERE/'source-geometry.json').write_text(json.dumps(ORIGINAL_GEOMETRY,indent=2)+'\n')
 (HERE/'extracted-masks.json').write_text(json.dumps(g.MASKS,indent=2)+'\n')
 print(json.dumps({k:report[k] for k in ('status','source_count','matched_source_options','source_distractors_matched','distinct_assessed_tasks_sampled','script_sha256')},indent=2))
if __name__=='__main__':main()
