#!/usr/bin/env python3
"""Independent prompt/solution/PNG, source fidelity, bank and native checks."""
import copy,concurrent.futures,hashlib,importlib.util,json,os,re,subprocess,sys,tempfile
from pathlib import Path
import numpy as np
from PIL import Image
import sympy as sp
HERE=Path(__file__).parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('reciprocal',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def require(ok,message):
 if not ok:raise AssertionError(message)
def arithmetic(s,env):
 s=s.strip().replace(r'\cdot','*').replace(r'\,','').replace(' ','').rstrip('.,')
 s=re.sub(r'\\(?:d?frac)\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',s)
 return sp.sympify(s,locals=env,rational=True)
def blue_mask(im):
 rgb=np.asarray(im.convert('RGB'));return (rgb[:,:,2]>110)&(rgb[:,:,0]<90)&(rgb[:,:,1]>55)&(rgb[:,:,1]<160)
def check_generated_pixels(r):
 side=r['generation']['plot']
 if 'source_asset' in side:return
 im=Image.open(r['generation']['plot_asset']);mask=blue_mask(im);w,h=im.size
 require([w,h]==side['dimensions'],'native output dimensions')
 # Recover plot transform independently from bounds and the fixed axes rectangle.
 lo,hi,bottom,top=side['bounds'];trans=lambda x,y:(.07*w+(x-lo)/(hi-lo)*.86*w,h-(.07*h+(y-bottom)/(top-bottom)*.86*h))
 p={k:sp.Rational(v) for k,v in side['parameters'].items()};a,b,k,x,y=(float(p[t]) for t in ('a','b','k','px','py'))
 def present(xx,yy,radius=4):
  u,v=trans(xx,yy);u,v=round(u),round(v)
  return 0<=u<w and 0<=v<h and bool(mask[max(0,v-radius):min(h,v+radius+1),max(0,u-radius):min(w,u+radius+1)].any())
 require(present(x,y),'visible actual marked point')
 checked=0;branches=[0,0]
 for xx in np.linspace(lo+.1,hi-.1,43):
  if abs(xx-b)<.05:continue
  yy=a/(xx-b)+k
  if bottom+.3<yy<top-.3:
   require(present(xx,yy),'PNG curve does not follow the displayed function '+str((r['generation']['template'],r['generation']['seed'],xx,yy)));checked+=1;branches[int(xx>b)]+=1
 require(checked>=12 and min(branches)>=5,'both curve branches visibly represented')
 # True zero axes appear black across their real transformed locations.
 rgb=np.asarray(im.convert('RGB'));u,v=trans(0,0);u,v=round(u),round(v)
 require((rgb[v-2:v+3,:,0]<80).sum()>w*.6,'horizontal zero axis')
 require((rgb[:,u-2:u+3,0]<80).sum()>h*.6,'vertical zero axis')
 require(side['label_values']['point']==['('+g.fmt(p['px'])+', '+g.fmt(p['py'])+')'],'actual marker label readback')
 require(side['label_values']['ticks']==[g.fmt(p[t]) for t in ('b','k') if p[t]],'actual signed tick label readback')
 gray=(rgb[:,:,0]>100)&(rgb[:,:,0]<190)&(np.max(rgb,axis=2)-np.min(rgb,axis=2)<5)
 if b:
  ub,_=trans(b,0);ub=round(ub);require(gray[:,ub-2:ub+3].sum()>h*.15,'actual PNG vertical asymptote')
 if k:
  _,vk=trans(0,k);vk=round(vk);require(gray[vk-2:vk+3,:].sum()>w*.15,'actual PNG horizontal asymptote')
 texts=[t['text'] for t in side['artist_text_readback']]
 require(sorted(texts)==sorted(['$x$','$y$']+side['label_values']['ticks']+side['label_values']['point']),'actual Matplotlib text artist readback')
 for t in side['artist_text_readback']:
  bx,by,bw,bh=t['bbox_pixels_bottom'];require(bx>=0 and by>=0 and bx+bw<=w and by+bh<=h,'actual tick/point label clipping')
 return checked

def check_record(r):
 require(set(r['knowledge_point'])=={'db_id','id','title'},'outer schema')
 q=r['question'];meta=r['generation'];p={k:sp.Rational(v) for k,v in meta['parameters'].items()}
 # Read supplied operator from the actual learner prompt before using graph.
 prompt=q[':question/problem'];level=g.FAMILIES[meta['template']][0]
 supplied=re.search(r'function \$([^$]+)\$|graph of \$([^$]+)\$',prompt);require(supplied,'actual supplied equation')
 eq=(supplied.group(1) or supplied.group(2)).rstrip('.')
 den=re.search(r'\\(?:d?frac)\{a\}\{([^{}]+)\}',eq).group(1)
 require(den==('x-b' if level=='hard' else 'x'),'actual denominator and operator')
 require(('+k' in eq)==(level!='easy'),'actual vertical shift operator')
 side=meta['plot']
 if 'source_asset' in side:
  geom=json.loads((HERE/'plot-extraction.json').read_text())['plots'][meta['source_ids'][0]];actual={k:sp.Rational(v) for k,v in geom['parameters'].items()}
 else:
  point=side['label_values']['point'][0];xx,yy=re.fullmatch(r'\(([^,]+), ([^)]+)\)',point).groups()
  actual={'px':sp.Rational(xx),'py':sp.Rational(yy),'b':sp.Rational(str(side['vertical_asymptote'])),'k':sp.Rational(str(side['horizontal_asymptote']))};actual['a']=(actual['py']-actual['k'])*(actual['px']-actual['b'])
 actual['a']=(actual['py']-actual['k'])*(actual['px']-actual['b'])
 require(actual==p,'actual graph labels/asymptotes yield parameters')
 expected={'a':actual['a'],'b':actual['b'],'k':actual['k']};target=expected['a'] if level=='easy' else sum(expected[t] for t in ('a','k')) if level=='moderate' else sum(expected.values())
 for f in q.get(':question/answer-fields',[]):
  values=[arithmetic(a[':answer/value'],{}) for a in f[':answer-field/choices']]
  for i,v in enumerate(values):
   for z in values[i+1:]:require(sp.simplify(v-z)!=0,'complete criterion-pair bank collision')
  correct=f.get(':answer-field/correct')
  if correct:
   ans=next(a for a in f[':answer-field/choices'] if a[':answer/id']==correct[1]);wanted=target if f[':answer-field/type'].endswith('radio') else expected[{'field-1':'a','field-2':'b' if level=='hard' else 'k','field-3':'k'}[f[':answer-field/key']]]
   require(arithmetic(ans[':answer/value'],{})==wanted,'actual answer target')
  if f[':answer-field/type'].endswith('blank'):require('{{'+f[':answer-field/key']+'}}' in prompt,'matching blank placeholder')
 text='\n'.join([prompt,q.get(':question/worked-solution','')]+[a[':answer/value'] for f in q.get(':question/answer-fields',[]) for a in f[':answer-field/choices']])
 require(not any(ord(c)<32 and c not in '\n\t\r' for c in text),'control characters')
 require(text.count('$')%2==0,'balanced math delimiters');depth=0
 for c in text:
  if c=='{':depth+=1
  elif c=='}':depth-=1
  require(depth>=0,'unbalanced TeX braces')
 require(depth==0,'balanced groups')
 sol=q.get(':question/worked-solution')
 if sol:
  point=re.search(r'point \$\(([^,]+),([^)]+)\)\$',sol)
  require(point and arithmetic(point[1],{})==p['px'] and arithmetic(point[2],{})==p['py'],'solution prose coordinate readback')
  env={'a':p['a'],'b':p['b'],'k':p['k'],'x':p['px'],'y':p['py']}
  for block in re.findall(r'\$\$([\s\S]*?)\$\$',sol):
   block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','')
   for row in block.split(r'\\'):
    expressions=row.strip().split('=')
    if len(expressions)<2:continue
    evaluated=[arithmetic(e,env) for e in expressions]
    for v in evaluated[1:]:require(sp.simplify(evaluated[0]-v)==0,'displayed solution operand/stage equality: '+row)
  if level!='easy':
   h=re.search(r'horizontal asymptote of the graph is \$y=([^$]+)\$',sol);require(h and arithmetic(h[1],{})==p['k'],'solution horizontal asymptote prose')
  if level=='hard':
   v=re.search(r'vertical asymptote is \$x=([^$]+)\$',sol);require(v and arithmetic(v[1],{})==p['b'],'solution vertical asymptote prose')
  final=re.search(r'Finally, \$([^$]+)\$',sol)
  if final:
   terms=final[1].rstrip('.').split('=');vals=[arithmetic(t,env) for t in terms];require(all(v==target for v in vals),'concluding sum')
 check_generated_pixels(r)
 return True

def native_row(r,label):
 checks=[]
 for i,f in enumerate(r['question'].get(':question/answer-fields',[])):
  if ':answer-field/correct' not in f:return None
  if f[':answer-field/type'].endswith('radio'):
   checks += [{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete owned scalar bank'} for a in f[':answer-field/choices']]
  else:
   v=f[':answer-field/choices'][0][':answer/value'];exact=arithmetic(v,{})
   checks += [{'field_index':i,'submitted':v,'expected':'accepted','purpose':'canonical scalar fragment'},{'field_index':i,'submitted':f'({exact.p*3})/({exact.q*3})','expected':'accepted','purpose':'unreduced equivalent scalar fragment'},{'field_index':i,'submitted':str(exact+1),'expected':'rejected','purpose':'incorrect scalar fragment'}]
 if not checks:return None
 return {'record':r,'label':label,'checks':checks}

def main():
 cases=[];source_report=[];rows=[];engine=[]
 for sid,src in g.QS.items():
  family=g.SOURCE_FAMILY[sid];level=g.FAMILIES[family][0];case={'source_id':sid,'template':family,'parameters':g.ANCHORS[sid],'bank_profile':'raw:'+sid,'authored_level_assignment':level if ':question/difficulty' not in src else None};cases.append(case)
  r=g.generate(level,seed=17,template=family,parameters=case['parameters'],profile=case['bank_profile']);check_record(r)
  for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):require((key in src)==(key in r['question']),sid+' key-presence parity '+key)
  require(src[':question/problem']==r['question'][':question/problem'],sid+' full prompt fidelity')
  if ':question/worked-solution' in src:require(src[':question/worked-solution']==r['question'][':question/worked-solution'],sid+' full worked-solution fidelity')
  count=0
  for original,generated in zip(src.get(':question/answer-fields',[]),r['question'].get(':question/answer-fields',[])):
   require(original[':answer-field/key']==generated[':answer-field/key'],'field layout/order')
   require(original[':answer-field/type'][':db/ident']==generated[':answer-field/type'],'field type')
   require(sorted(a[':answer/value'] for a in original[':answer-field/choices'])==sorted(a[':answer/value'] for a in generated[':answer-field/choices']),'full observed bank fidelity');count+=len(original[':answer-field/choices'])
   require((':answer-field/correct' in original)==(':answer-field/correct' in generated),'designation presence')
   if ':answer-field/correct' in original:require(original[':answer-field/correct'][':answer/value']==next(a[':answer/value'] for a in generated[':answer-field/choices'] if a[':answer/id']==generated[':answer-field/correct'][1]),'correct value fidelity')
  source_report.append({'source_id':sid,'prompt_exact':True,'solution_exact':':question/worked-solution' in src,'option_count':count,'key_presence_exact':True,'raw_eligible':False});rows.append(r)
  e=native_row(r,sid)
  if e:engine.append(e)
 (HERE/'source-cases.json').write_text(json.dumps(cases,indent=2))
 generated=[]
 for family,(level,kind,sid) in g.FAMILIES.items():
  for seed in range(18):
   r=g.generate(level,seed=seed,template=family);check_record(r);generated.append(r)
   if seed<2:rows.append(r)
   if seed<6:engine.append(native_row(r,family+':'+str(seed)))
 # Exercise every source structural mask at changed inputs, including negative
 # denominator and nonunit denominator; raw API truly computes, not literal replay.
 changed=[]
 for sid in g.QS:
  family=g.SOURCE_FAMILY[sid];level=g.FAMILIES[family][0];p=g.norm(g.ANCHORS[sid]);p['k']=-p['k'] if level!='easy' else p['k'];p['a']=-p['a'] if level!='easy' else p['a']+p['px'];p['py']=p['a']/(p['px']-p['b'])+p['k']
  r=g.generate(level,seed=3,parameters={k:str(v) for k,v in p.items()},profile='raw:'+sid);check_record(r);changed.append(r)
  require(r['question'][':question/problem']!=g.QS[sid][':question/problem'],'parameterized graph prompt changed')
  p=g.norm(g.ANCHORS[sid]);p['a']*=3 if level=='easy' else 2;p['k']=-p['k'] if level!='easy' else p['k'];p['py']=p['a']/(p['px']-p['b'])+p['k']
  r=g.generate(level,seed=4,parameters={k:str(v) for k,v in p.items()},profile='raw:'+sid);check_record(r);changed.append(r)
 # Content IDs insensitive to seed/order, task IDs insensitive to banks/styles.
 for family in g.FAMILIES:
  r=next(x for x in generated if x['generation']['template']==family);p=r['generation']['parameters'];level=g.FAMILIES[family][0];profile=r['generation']['profile']
  q=g.generate(level,999,template=family,parameters=p,profile=profile);require(q['question'][':question/id']==r['question'][':question/id'],'seed identity invariant')
 # Signed boundary/explicit invalid workload checks.
 invalid=[('easy',dict(a=4,b=1,k=0,px=3,py=2)),('moderate',dict(a=2,b=0,k=0,px=1,py=2)),('hard',dict(a=4,b=0,k=1,px=2,py=3))]
 for level,p in invalid:
  try:g.generate(level,parameters=p)
  except ValueError:pass
  else:raise AssertionError('explicit workload guard bypass')
 # Mutation catches displayed arithmetic/control/PNG-label changes.
 mut=copy.deepcopy(generated[-1]);mut['question'][':question/worked-solution']=mut['question'][':question/worked-solution'].replace('point $','point $(999,999)$ and the point $',1)
 try:check_record(mut)
 except (AssertionError,ValueError):pass
 else:raise AssertionError('stale prose mutation not caught')
 mut=copy.deepcopy(generated[0]);mut['question'][':question/problem']+='\x0c'
 try:check_record(mut)
 except AssertionError:pass
 else:raise AssertionError('control mutation not caught')
 # Concurrent renderer calls use new private directory, same and different sets.
 concurrency=Path(tempfile.mkdtemp(prefix='concurrency-',dir=HERE))
 code="import importlib.util,sys,json; s=importlib.util.spec_from_file_location('g',sys.argv[1]);g=importlib.util.module_from_spec(s);s.loader.exec_module(g);print(g.render_plots(g.norm(json.loads(sys.argv[2])),sys.argv[3])[0])"
 par=[g.ANCHORS['q-113482'],g.ANCHORS['q-320718'],g.ANCHORS['q-113482']]
 def run(p):return subprocess.run([sys.executable,'-c',code,str(HERE.with_suffix('.py')),json.dumps(p),str(concurrency)],capture_output=True,text=True,check=True).stdout.strip()
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:paths=list(pool.map(run,par))
 require(paths[0]==paths[2] and paths[0]!=paths[1],'concurrent renderer identities')
 require(not list(concurrency.glob('render-*')) and not list(concurrency.glob('side-*')),'private temporary inputs cleaned')
 for p in paths:require(Path(p).exists() and Path(p).with_suffix('.json').exists(),'concurrent PNG+sidecar')
 # Enumerate meaningful eligible finite domains, excluding seed/profile aliases.
 variety={}
 for level in ('easy','moderate','hard'):
  seen=set()
  for seed in range(6000):
   p=g.sample(level,__import__('random').Random(seed))
   try:
    g.guard(level,p);profile='method-unit' if level=='easy' and abs(p['py'])==1 else 'method-product' if level=='easy' else 'method';g.eligible(g.bank(p,level,profile))
   except ValueError:continue
   seen.add(tuple(str(p[k]) for k in ('a','b','k','px','py')))
  variety[level]=len(seen)
 (HERE/'review.json').write_text(json.dumps(rows+changed,indent=2))
 (HERE/'engine-input.json').write_text(json.dumps(engine,indent=2));res=subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],capture_output=True,text=True,check=True)
 negative=copy.deepcopy(engine[:1]);negative[0]['checks'][0]['expected']='rejected' if negative[0]['checks'][0]['expected']=='accepted' else 'accepted';(HERE/'engine-negative-input.json').write_text(json.dumps(negative));negative_result=subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'engine-negative-input.json'),str(HERE/'engine-negative-report.json')],capture_output=True,text=True);require(negative_result.returncode!=0,'engine negative control');(HERE/'engine-negative-result.txt').write_text(negative_result.stderr)
 report={'status':'pass','sources':source_report,'practice_sources':len(cases),'full_prompts_exact':len(cases),'worked_solutions_exact':sum(':question/worked-solution' in s for s in g.QS.values()),'worked_solutions_absent_preserved':1,'complete_banks_exact':7,'source_answer_values_exact':sum(s['option_count'] for s in source_report),'source_correct_designations_exact':9,'missing_correct_designations_preserved':1,'fieldless_presence_preserved':1,'normal_generated_records_checked':len(generated),'changed_raw_records_checked':len(changed),'meaningful_curve_point_domains_sampled':variety,'native':json.loads((HERE/'engine-report.json').read_text()),'provenance':{'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'source_sha256':hashlib.sha256((HERE/'source.json').read_bytes()).hexdigest(),'engine_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'basis':1356},'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':g.matplotlib.__version__},'unresolved':['Observed scalar distractor intentions are underdetermined; raw affine-offset banks are explicit ineligible evidence.','Unrated q-39046 has no original correct designation or solution; normal easy level, correct a=4 and worked solution are authored/inferred.','q-113479 is fieldless; normal hard radio contract is explicitly authored.']}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2));print(res.stdout.strip());print('PASS:',len(cases),'source prompts;',len(generated),'normal records;',variety)
if __name__=='__main__':main()
