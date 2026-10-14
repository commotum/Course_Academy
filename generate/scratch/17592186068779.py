#!/usr/bin/env python3
"""Graph recognition of transformed reciprocal functions. Basis 1356.

Raw observed profiles are parameterized evidence recipes, never default learning
banks. They preserve missing attributes and documented malformed source text.
Default banks derive complete transformation mistakes from the assessed method.
No EDB writes. See private classification/extraction/validation evidence.
"""
from __future__ import annotations
import argparse,hashlib,json,os,random,re,sys,tempfile,uuid
from pathlib import Path
from fractions import Fraction
os.environ.setdefault('MPLCONFIGDIR','/tmp/reciprocal-17592186068779-mpl')
import matplotlib
matplotlib.use('Agg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np
import sympy as sp
KP_ID=17592186068779
KP_UUID='4640f978-9caa-5960-bec4-f153a1b4cc5d'
TITLE='Graphing a Transformed Reciprocal Function'
VERSION='reciprocal-transform-v1'
ROOT=Path(__file__).with_suffix('')
SOURCE=json.loads((ROOT/'source.json').read_text())
QUESTIONS=SOURCE['record'][':knowledge-point/questions']
CASES=json.loads((ROOT/'source-cases.json').read_text())
SPECS=json.loads((ROOT/'plot-extraction.json').read_text())
BY_PROFILE={c['bank_profile']:(c,q) for c,q in zip(CASES,QUESTIONS)}
NAMESPACE=uuid.UUID(KP_UUID)
R=sp.Rational

def canonical(v):return str(R(str(v)))
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(NAMESPACE,str(v)))
def triple(a,h,k):return [canonical(a),canonical(h),canonical(k)]
def tex(v):
 v=R(str(v));return str(v) if v.q==1 else ('-' if v<0 else '')+r'\frac{'+str(abs(v.p))+'}{'+str(v.q)+'}'
def expr(a,h,k,style='plain'):
 a,h,k=map(lambda t:R(str(t)),[a,h,k]);den='x'
 if h:den+='-'+tex(h) if h>0 else '+'+tex(-h)
 if a.q!=1:den=str(a.q)+(f'({den})' if h else den)
 out=('-' if a<0 else '')+r'\frac{'+str(abs(a.p))+'}{'+den+'}'
 if k:out+=('+' if k>0 else '-')+tex(abs(k))
 if style=='q-16508':out=out.replace('x+','x + ').replace('x-','x - ')
 if style=='q-98003':out=out.replace('+',' + ').replace('-',' - ') if k else out
 # The source second prompt has a leading negative fraction but spaced vertical addition.
 if style=='q-98003':out=out.strip().replace('- '+chr(92),'-'+chr(92))
 return out

def raw_text(q,p,solution=False):
 """Full original prose skeleton; replace complete equation/scalar nodes in order.
 Intro anomalies remain parameterized offsets in ineligible raw evidence only.
 """
 c=next(c for c in CASES if c['source_id']==q[':db/id']);anchor=c['parameters'];a,h,k=[R(str(p[t])) for t in ['a','h','k']]
 text=q[':question/worked-solution' if solution else ':question/problem'];style=c['source_math_academy_id']
 if not solution:
  match=re.search(r'\$(.*?)\$',text,re.S);old=match[1];oldexpr=old.split('=',1)[1];leading=oldexpr[:len(oldexpr)-len(oldexpr.lstrip())]
  newexpr=expr(a,h,k,style);newexpr=(' ' if leading else '')+newexpr+('?' if oldexpr.endswith('?') else '')
  return text[:match.start(1)]+old.split('=',1)[0]+'='+newexpr+text[match.end(1):]
 sign=1 if a>0 else -1
 stages=[(a,h,k),(sign,0,0)]
 if anchor['h']:stages.extend([(sign,h,0),(a,h,0)])
 else:stages.extend([(a,0,0),(a,0,k)])
 # Raw source stale intro is a complete, explicit offset slot.
 if style=='q-113372':stages[0]=(a,h,k-2)
 if style=='q-113369':stages[0]=(a,h,k-1)
 yi=0;si=0;scalars=[abs(h),abs(a)] if anchor['h'] else [abs(a),abs(k)]
 def replace(m):
  nonlocal yi,si
  tok=m[1]
  if tok=='y':return m[0]
  if tok.startswith('y='):
   aa,hh,kk=stages[yi];yi+=1
   suffix=tok[-1] if tok[-1] in ',.' else ''
   return '$y='+expr(aa,hh,kk)+suffix+'$'
  # Scalars occur in the source at operative stretch and translation stages.
  v=scalars[si];si+=1;return '$'+tex(v)+'$'
 text=re.sub(r'\$(.*?)\$',replace,text,flags=re.S)
 assert yi==len(stages)
 if anchor['h']:
  text=text.replace('to the right','to the '+('right' if h>0 else 'left')).replace('to the left','to the '+('right' if h>0 else 'left'))
 else:
  direction='up' if k>0 else 'down'
  text=re.sub(r' units? (?:up|down)',lambda m:m[0].rsplit(' ',1)[0]+' '+direction,text)
 # Every source image represents one stage; changing parameters renders its geometric recipe.
 paths=re.findall(r'!\[\]\((.*?)\)',text)
 for path in paths:
  spec=SPECS[path];anchor_a=R(str(anchor['a']));source_t=[R(spec[t]) for t in ['a','h','k']]
  # Base sign curves are independent of coefficient magnitude.
  if source_t[0]==(1 if anchor_a>0 else -1) and source_t[1]==0 and source_t[2]==0:new_t=[sign,0,0]
  elif source_t[0]==(1 if anchor_a>0 else -1) and source_t[1]!=0:new_t=[sign,h,0]
  elif source_t[2]==0:new_t=[a,h,0]
  else:new_t=[a,h,k]
  actual=path if triple(*new_t)==triple(*source_t) else render_plot(new_t)
  text=text.replace('![]('+path+')','![]('+actual+')')
 return text

def render_plot(t,dist=1,marker_labels=None,force=False):
 """Unique Figure per call; atomic immutable content addressed PNG + sidecar.
 True zero axes; separately clipped branches; source-shaped points at h±d.
 """
 vals=triple(*t);a,h,k=map(lambda v:float(R(v)),vals);d=float(dist)
 data={'version':VERSION,'triple':vals,'distance':canonical(dist),'marker_labels':marker_labels,'renderer':matplotlib.__version__}
 stem=digest(data);folder=ROOT/'plots';folder.mkdir(exist_ok=True);png=folder/(stem+'.png');side=png.with_suffix('.json')
 if not force and png.exists() and side.exists():return str(png)
 xlo=min(-2,h-4);xhi=max(2,h+4);yl=max(3,abs(a)/d+1);ylo=min(-2,k-yl);yhi=max(2,k+yl)
 fig=Figure(figsize=(4.8,4),dpi=100);FigureCanvasAgg(fig);ax=fig.add_axes([.14,.13,.80,.81]);ax.set_xlim(xlo,xhi);ax.set_ylim(ylo,yhi)
 ax.spines['left'].set_position('zero');ax.spines['bottom'].set_position('zero');ax.spines['top'].set_visible(False);ax.spines['right'].set_visible(False)
 ax.tick_params(labelsize=10,pad=4);ax.set_xticks(sorted(set([int(xlo)+1,int(xhi)-1,int(h)])));ax.set_yticks(sorted(set([int(ylo)+1,int(yhi)-1,int(k)])))
 ax.set_xticklabels([str(int(t)) if t else '' for t in ax.get_xticks()]);ax.set_yticklabels([str(int(t)) if t else '' for t in ax.get_yticks()]);ax.text(xhi-.2,.2,'x',fontsize=12);ax.text(.15,yhi-.35,'y',fontsize=12)
 ax.annotate('',xy=(xhi,0),xytext=(xhi-.35,0),arrowprops={'arrowstyle':'->','color':'black'});ax.annotate('',xy=(0,yhi),xytext=(0,yhi-.35),arrowprops={'arrowstyle':'->','color':'black'})
 if h:ax.axvline(h,color='#b0b0b0',lw=1,ls=(0,(4,3)))
 if k:ax.axhline(k,color='#b0b0b0',lw=1,ls=(0,(4,3)))
 for low,high in [(xlo,h-1e-4),(h+1e-4,xhi)]:
  xx=np.linspace(low,high,1800);yy=a/(xx-h)+k;valid=(yy>=ylo)&(yy<=yhi);yy[~valid]=np.nan;ax.plot(xx,yy,color='#2276c6',lw=1.8)
 points=[[h-d,k-a/d],[h+d,k+a/d]]
 for j,(x,y) in enumerate(points):
  ax.plot(x,y,'o',color='#2276c6',ms=4)
  label=marker_labels[j] if marker_labels else '('+tex(R(vals[1])-R(str(dist)) if j==0 else R(vals[1])+R(str(dist)))+', '+tex(R(vals[2])-R(vals[0])/R(str(dist)) if j==0 else R(vals[2])+R(vals[0])/R(str(dist)))+')'
  ax.annotate('$'+label+'$',(x,y),xytext=(-7 if j==0 else 7,10 if y>=k else -17),textcoords='offset points',ha='right' if j==0 else 'left',fontsize=10)
 data.update({'bounds':[xlo,xhi,ylo,yhi],'points':points,'axes_origin':[0,0],'branch_segments':2,'dpi':100,'pixels':[480,400],'python':sys.version.split()[0]})
 fd,tmp=tempfile.mkstemp(prefix=stem+'-',suffix='.png',dir=folder);os.close(fd)
 try:fig.savefig(tmp,facecolor='white');os.replace(tmp,png)
 finally:
  if os.path.exists(tmp):os.unlink(tmp)
 fd,tmp=tempfile.mkstemp(prefix=stem+'-',suffix='.json',dir=folder);os.close(fd)
 try:Path(tmp).write_text(json.dumps(data,indent=2));os.replace(tmp,side)
 finally:
  if os.path.exists(tmp):os.unlink(tmp)
 return str(png)

def observed_bank(profile,p):
 """Geometric recipes, not claimed recovered author intentions.
 Relative coefficient ratios and selected shift components faithfully account
 for each complete bank. Opaque composite graph 503f... remains evidence-only.
 """
 c,q=BY_PROFILE[profile];aa,hh,kk=[R(str(c['parameters'][t])) for t in ['a','h','k']];a,h,k=[R(str(p[t])) for t in ['a','h','k']]
 result=[]
 for ans in q[':question/answer-fields'][0][':answer-field/choices']:
  s=SPECS[ans[':answer/value']];sa,sh,sk=[R(s[t]) for t in ['a','h','k']]
  na=(sa/aa)*a
  nh=(sh/hh)*h if hh else ((sh/kk)*k if kk else sh)
  nk=(sk/kk)*k if kk else 0
  # Omitted-scale graphs are signed unit reciprocals, irrespective of |a|.
  if abs(sa)==1 and abs(aa)!=1:na=(1 if sa>0 else -1)*(1 if a*aa>0 else -1)
  t=triple(na,nh,nk)
  path=ans[':answer/value'] if t==triple(sa,sh,sk) else render_plot(t,dist=(R(s['marked_points'][1][0])-R(s['marked_points'][0][0]))/2)
  result.append((t,path))
 return result

def authored_bank(a,h,k,level):
 sign=1 if a>0 else -1
 if level=='easy':
  if h:return [triple(a,h,0),triple(-a,h,0),triple(a,-h,0),triple(a,0,0),triple(-a,-h,0)]
  return [triple(a,0,k),triple(-a,0,k),triple(a,0,-k),triple(a,0,0),triple(-a,0,-k)]
 if level=='moderate':return [triple(a,0,k),triple(-a,0,k),triple(a,0,0),triple(a,0,-k),triple(a,-k,0)]
 return [triple(a,h,0),triple(-a,h,0),triple(a,-h,0),triple(sign,h,0),triple(a,0,0)]

def normal_solution(a,h,k,template,final_only=False):
 sign=1 if a>0 else -1;target=expr(a,h,k)
 out='To plot $y='+target+',$ we apply the following steps:\n\n- Take the curve $y='+expr(sign,0,0)+'.$'
 if not final_only:out+='\n\n![]('+render_plot([sign,0,0])+')'
 if template=='horizontal_then_scale':
  out+='\n\n- Translate it by $'+tex(abs(h))+'$ '+('unit' if abs(h)==1 else 'units')+' to the '+('right' if h>0 else 'left')+' to get the graph of $y='+expr(sign,h,0)+'.$'
  if not final_only:out+='\n\n![]('+render_plot([sign,h,0])+')'
  if abs(a)!=1:out+='\n\n- Then, stretch the result by a scale factor of $'+tex(abs(a))+'$ parallel to the $y$-axis to get the graph of $y='+expr(a,h,0)+'.$'
 else:
  if abs(a)!=1:
   out+='\n\n- Then, stretch the result by a scale factor of $'+tex(abs(a))+'$ parallel to the $y$-axis to get the graph of $y='+expr(a,0,0)+'.$'
   if not final_only:out+='\n\n![]('+render_plot([a,0,0])+')'
  out+='\n\n- Translate it by $'+tex(abs(k))+'$ '+('unit' if abs(k)==1 else 'units')+' '+('up' if k>0 else 'down')+' to get the graph of $y='+target+'.$'
 return out+'\n\n![]('+render_plot([a,h,k])+')'

# EASY: authored missing level; unit signed reciprocal with exactly one nonzero
# integer translation. One transformation, no scale arithmetic, 32 actual tasks across two orientations.
# MODERATE: observed vertical translation after signed rational/integer scaling;
# HARD: observed horizontal translation before signed rational/integer scaling.
# Both observed levels retain two operative transformations, differentiated by
# reading denominator translation versus supplied vertical addition.
SCALES=sorted({R(n,q) for n in range(1,6) for q in range(1,6) if n!=q})
def domain(level,template):
 if level=='easy':
  return [{'a':str(a),'h':h,'k':0} for a in [-1,1] for h in [-4,-3,-2,-1,1,2,3,4]] if template=='horizontal_then_scale' else [{'a':str(a),'h':0,'k':k} for a in [-1,1] for k in [-4,-3,-2,-1,1,2,3,4]]
 return [{'a':str(sign*s),'h':v if level=='hard' else 0,'k':v if level=='moderate' else 0} for s in SCALES for sign in [-1,1] for v in [-4,-3,-2,-1,1,2,3,4]]

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ['easy','moderate','hard']:raise ValueError('unknown difficulty')
 if field_type not in [None,'radio',':answer-field.type/radio']:raise ValueError('radio only')
 rng=random.Random(seed);raw=profile in BY_PROFILE
 eligible=['normal:'+c['source_math_academy_id'] for c in CASES if c['level']==level and c['source_math_academy_id']!='q-113372']
 if not profile and level!='easy':profile=rng.choice(eligible+['authored:method'])
 normal_observed=profile is not None and profile.startswith('normal:')
 if normal_observed and profile not in eligible:raise ValueError('normal profile outside level or opaque bank')
 if profile and not raw and not normal_observed and profile!='authored:method':raise ValueError('unknown profile')
 if raw:
  c,q=BY_PROFILE[profile];template=template or c['template']
  if template!=c['template'] or level!=c['level']:raise ValueError('source profile level/template mismatch')
  parameters=parameters or c['parameters']
 else:
  if normal_observed:
   c,q=BY_PROFILE['raw:'+profile.split(':',1)[1]]
   template=template or c['template']
  template=template or (rng.choice(['horizontal_then_scale','scale_then_vertical']) if level=='easy' else 'scale_then_vertical' if level=='moderate' else 'horizontal_then_scale')
  if template not in ['horizontal_then_scale','scale_then_vertical']:raise ValueError('unknown template')
  if level=='moderate' and template!='scale_then_vertical' or level=='hard' and template!='horizontal_then_scale':raise ValueError('template outside authored level bounds')
  parameters=parameters or rng.choice(domain(level,template));profile=profile or 'authored:method'
 if set(parameters)!=set(['a','h','k']):raise ValueError('exact a,h,k parameter keys required')
 a,h,k=[R(str(parameters[t])) for t in ['a','h','k']]
 if abs(a.p)>5 or a.q>5:raise ValueError('reduced coefficient magnitude and denominator≤5')
 if not a or h.q!=1 or k.q!=1 or abs(h)>4 or abs(k)>4 or (h and k):raise ValueError('single nonzero integer shift, magnitude≤4')
 if template=='horizontal_then_scale' and (not h or k) or template=='scale_then_vertical' and (not k or h):raise ValueError('template requires its sole translation')
 if not raw:
  if level=='easy' and abs(a)!=1:raise ValueError('easy has no nonunit scale')
  if level!='easy' and (abs(a)==1 or abs(a) not in SCALES):raise ValueError('source-grounded reduced scales numerator/denominator≤5, nonunit')
 p={'a':str(a),'h':int(h),'k':int(k)}
 if raw:
  bank=observed_bank(profile,p);prompt=raw_text(q,p);solution=raw_text(q,p,True) if ':question/worked-solution' in q else None
  has_correct=':answer-field/correct' in q[':question/answer-fields'][0]
 elif normal_observed:
  bank=observed_bank('raw:'+profile.split(':',1)[1],p);prompt=raw_text(q,p);has_correct=True
  solution=raw_text(q,p,True) if ':question/worked-solution' in q else normal_solution(a,h,k,template)
  if profile=='normal:q-113369':
   solution=re.sub(r'(?<=To plot )\$.*?\$',lambda m:'$y='+expr(a,h,k)+',$',solution,count=1)
  if profile=='normal:q-98017':solution=solution.replace('$1$ units','$1$ unit')
 else:
  ts=authored_bank(a,h,k,level);bank=[(t,render_plot(t)) for t in ts];prompt='Which of the following is the graph of $y='+expr(a,h,k)+'?$';solution=normal_solution(a,h,k,template);has_correct=True
 target=triple(a,h,k)
 if len(set(tuple(t) for t,path in bank))!=5:raise ValueError('whole bank collision')
 correct=[i for i,(t,path) in enumerate(bank) if t==target]
 if len(correct)!=1:raise ValueError('no unique correct graph')
 math_id=digest({'criterion':'complete graph','a':str(a),'h':str(h),'k':str(k),'assessed_information':'equation'})
 content=digest({'version':VERSION,'difficulty':None if raw and ':question/difficulty' not in q else level,'prompt':prompt,'solution':solution,'bank':sorted(path for t,path in bank),'field':'radio','correct':bank[correct[0]][1] if has_correct else None})
 qid=uid(content);fid=uid(qid+':selection')
 choices=[{':answer/id':uid(fid+':'+path),':answer/type':':answer.type/image',':answer/value':path} for t,path in bank]
 correct_id=choices[correct[0]][':answer/id'];rng.shuffle(choices)
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
 if has_correct:field[':answer-field/correct']=[':answer/id',correct_id]
 question={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
 if not raw or ':question/difficulty' in q:question[':question/difficulty']=':question.difficulty/'+level
 if solution is not None:question[':question/worked-solution']=solution
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'seed':seed,'difficulty':level,'template':template,'profile':profile,'parameters':p,'mathematical_fingerprint':math_id,'content_fingerprint':content,'source':{k:SOURCE[k] for k in ['database','basis','lineage']},'source_id':q[':db/id'] if raw or normal_observed else None,'evidence_only':raw,'eligible_for_learning':not raw,'bank_geometry':{path:t for t,path in bank},'raw_correct_inferred_index':correct[0] if raw and not has_correct else None,'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':matplotlib.__version__}}}
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(record):
 q=record['question'];out=q[':question/problem']+'\n\n'
 for j,a in enumerate(q.get(':question/answer-fields',[{}])[0].get(':answer-field/choices',[])):out+=f'{j+1}. ![]({a[":answer/value"]})\n\n'
 if ':question/worked-solution' in q:out+='Worked solution:\n\n'+q[':question/worked-solution']+'\n'
 return out
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
