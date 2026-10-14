#!/usr/bin/env python3
"""Graphical three-statement neighborhood behavior. Basis 1356, step 7 only.
Observed profiles preserve all source omissions. Raster-traced curves are explicit
shape data, not recovered algebra. Easy preserves observed masks and banks;
moderate/hard are curriculum-anchored authored scale/target-reading extensions.
Normal banks are complete semantic subset banks selected before parameters.
"""
from __future__ import annotations
import argparse, hashlib, json, random, uuid, sys, os, tempfile
from pathlib import Path
import numpy as np
import sympy as sp
os.environ.setdefault('MPLCONFIGDIR','/tmp/matplotlib-68697')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
KP_ID=17592186068697; KP_UUID='3f92e521-e7ab-56ba-8eac-0484b140b1a2'
TITLE='Determining the Behavior of a Function in the Neighborhood of a Point'
VERSION='neighborhood-graphs-2'; ROOT=Path(__file__).with_suffix(''); SPECS=json.loads((ROOT/'specs.json').read_text())
SUBSETS=['I only','II only','III only','I and II only','I and III only','II and III only','I, II and III','None']
NS=uuid.UUID('28974b77-e87e-42cb-951b-9eeb8b63db1d')
def uid(s):return str(uuid.uuid5(NS,s))
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def tex(x):return sp.latex(sp.Rational(str(x)))
def answer_name(bits):return SUBSETS[{(1,0,0):0,(0,1,0):1,(0,0,1):2,(1,1,0):3,(1,0,1):4,(0,1,1):5,(1,1,1):6,(0,0,0):7}[tuple(int(v) for v in bits)]]
SOURCE_CRITERIA={
 'q-48042':['left_finite','right_finite','discontinuous'],
 'q-48064':['defined','limit_exists','continuous'],
 'q-48063':['defined','left_exists','continuous'],
 'q-104049':['defined','limit_unequal_value','discontinuous'],
 'q-104051':['defined','limit_exists','discontinuous'],
 'q-104052':['not_defined','limit_exists','continuous'],
 'q-104124':['not_defined','limit_equals_value','continuous'],
 'q-48040':['defined','limit_exists','continuous'],
 'q-48062':['defined','limit_exists','continuous'],
 'q-48065':['defined','limit_equals_value','continuous'],
 'q-48067':['defined','limit_equals_value','continuous'],
 'q-48068':['left_finite','right_not_finite','secondary_continuous']}
def source_truth(sid):
 z=SPECS[sid];left_finite=not isinstance(z['left'],str);right_finite=not isinstance(z['right'],str);exists=left_finite and right_finite and z['left']==z['right'];defined=z['value'] is not None;equal=exists and defined and z['left']==z['value'];continuous=equal
 predicates={'left_finite':left_finite,'right_finite':right_finite,'right_not_finite':not right_finite,'left_exists':left_finite,'limit_exists':exists,'defined':defined,'not_defined':not defined,'limit_equals_value':equal,'limit_unequal_value':exists and defined and z['left']!=z['value'],'continuous':continuous,'discontinuous':not continuous,'secondary_continuous':z['b']!=z['a'] and any(m[0]==z['b'] and m[2] for m in z['markers']) and not any(m[0]==z['b'] and not m[2] for m in z['markers'])}
 return [predicates[c] for c in SOURCE_CRITERIA[sid]]
def render_source(sid,shift):
 s=SPECS[sid];ox,oy,sx,sy=s['axes']; im=np.array(Image.open(s['image']).convert('RGBA').convert('RGB')); yy,xx=np.where((im[:,:,0]>180)&(im[:,:,1]<140)&(im[:,:,2]<140))
 x=(xx-ox)/sx+shift;y=(oy-yy)/sy
 # Remove marker footprints; marker topology is independently transcribed.
 keep=np.ones(len(x),dtype=bool)
 for mx,my,filled in s['markers']:keep &= ~((abs(x-(mx+shift))<3.5/sx)&(abs(y-my)<3.5/sy))
 return {'cloud':[x[keep].tolist(),y[keep].tolist()],'markers':[[mx+shift,my,f] for mx,my,f in s['markers']], 'asymptotes':[a+shift for a,_ in s['asymptotes']], 'bounds':[min(-.7,(0-ox)/sx+shift),max(.7,(339-ox)/sx+shift),min(-.7,(oy-303)/sy),max(.7,oy/sy)],'grid':1,'targets':[s['a']+shift,s['b']+shift],'raster_trace':True}
def graph(level,p):
 a=float(sp.Rational(str(p['a'])));l=float(p['left']) if p['left'] not in ['+inf','-inf'] else p['left'];r=float(p['right']) if p['right'] not in ['+inf','-inf'] else p['right'];v=p['value'];b=float(sp.Rational(str(p.get('b',p['a']))));
 xmin=min(-1,a-2,b-1);xmax=max(1,a+2,b+1); curves=[]
 for side,val in [(-1,l),(1,r)]:
  x=np.linspace(a+side*.015,a+side*2,160)
  if isinstance(val,str):y=(1 if val=='+inf' else -1)/abs(x-a)
  else:y=val+.35*(x-a)**2
  curves.append([x.tolist(),np.clip(y,-10,10).tolist()])
 markers=[]
 for val in [l,r]:
  if not isinstance(val,str):markers.append([a,val,False])
 if v is not None:markers.append([a,float(v),True])
 if level=='hard' and not p['b_continuous']:
  # Hole on the existing side branch at the distinct second assessed target.
  val=l if b<a else r
  if isinstance(val,str):by=(1 if val=='+inf' else -1)/abs(b-a)
  else:by=val+.35*(b-a)**2
  markers.append([b,by,False])
 return {'curves':curves,'markers':markers,'asymptotes':[a] if isinstance(l,str) or isinstance(r,str) else [],'bounds':[xmin,xmax,min(-3,min([z for z in [l,r,float(v or 0)] if not isinstance(z,str)])-1),max(2,5 if any(isinstance(z,str) for z in [l,r]) else max(l,r,float(v or 0))+1)],'grid':.5 if level=='moderate' else .25,'targets':[a,b],'raster_trace':False}
def render_plots(data):
 key=digest({'version':VERSION,'data':data}); directory=ROOT/'plots';directory.mkdir(exist_ok=True);png=directory/(key+'.png');sidecar=directory/(key+'.json')
 if png.exists() and sidecar.exists():return str(png.resolve())
 fig,ax=plt.subplots(figsize=(7.2,6.08),dpi=100);fig.subplots_adjust(left=.1,bottom=.08,right=.95,top=.95)
 xmin,xmax,ymin,ymax=data['bounds'];ax.set(xlim=(xmin,xmax),ylim=(ymin,ymax));ax.set_aspect('equal',adjustable='box')
 for spine in ['top','right']:ax.spines[spine].set_visible(False)
 ax.spines['left'].set_position(('data',0));ax.spines['bottom'].set_position(('data',0))
 step=data['grid']; xt=np.arange(np.ceil(xmin/step),np.floor(xmax/step)+1)*step; yt=np.arange(np.ceil(ymin/step),np.floor(ymax/step)+1)*step
 # Label target coordinates exactly; reduce unrelated clutter while retaining scale grid.
 ax.set_xticks(xt);ax.set_yticks(yt);ax.tick_params(labelsize=8);ax.grid(alpha=.12)
 ax.set_xticklabels(['$'+tex(z)+'$' if z and (step!=.25 or z==int(z) or z in data['targets']) else '' for z in xt]);ax.set_yticklabels(['$'+tex(z)+'$' if z and (step!=.25 or z==int(z)) else '' for z in yt]);ax.text(.06,.06,'0',transform=ax.transData,fontsize=8)
 for a in data['asymptotes']:ax.axvline(a,color='gray',ls='--',lw=1.3)
 if 'cloud' in data:ax.scatter(*data['cloud'],s=3,c='red',linewidths=0,zorder=2)
 for x,y in data.get('curves',[]):ax.plot(x,y,c='red',lw=1.5)
 for x,y,filled in data['markers']:
  ax.plot(x,y,'o',mec='red',mfc='red' if filled else 'white',ms=8,mew=1.3,zorder=4)
 ax.annotate('',xy=(xmax,0),xytext=(xmax-.15,0),arrowprops={'arrowstyle':'->','color':'black'});ax.annotate('',xy=(0,ymax),xytext=(0,ymax-.15),arrowprops={'arrowstyle':'->','color':'black'});ax.text(xmax,0,' x');ax.text(0,ymax,' y')
 fig.canvas.draw();transform=ax.transData.get_matrix().tolist();meta={'geometry':data,'transform':transform,'size':[720,608],'renderer':'Matplotlib','versions':{'python':sys.version.split()[0],'matplotlib':matplotlib.__version__},'origin':ax.transData.transform((0,0)).tolist()}
 fd,tmp=tempfile.mkstemp(suffix='.png',dir=directory);os.close(fd)
 try:fig.savefig(tmp);os.replace(tmp,png)
 finally:plt.close(fig);Path(tmp).unlink(missing_ok=True)
 fd,tmp=tempfile.mkstemp(suffix='.json',dir=directory);os.close(fd);Path(tmp).write_text(json.dumps(meta));os.replace(tmp,sidecar)
 return str(png.resolve())
def task_fingerprint(level,template,p):
 # Task identity excludes banks, raster pixels, variable aliases, and incidental
 # numeric translations/ordinates when the requested predicates ignore them.
 if template in SPECS:
  z=SPECS[template];criteria=SOURCE_CRITERIA[template]
  props={'criteria':criteria,'left_finite':not isinstance(z['left'],str),'right_finite':not isinstance(z['right'],str),'equal_limits':z['left']==z['right'],'defined':z['value'] is not None,'value_on_left':z['value'] is not None and z['value']==z['left'],'value_on_right':z['value'] is not None and z['value']==z['right'],'grid':1}
 else:
  props={'criteria':['defined','limit_equals_value','continuous'] if level=='moderate' else ['left_finite','right_not_finite','secondary_continuous'],'left_finite':not isinstance(p['left'],str),'right_finite':not isinstance(p['right'],str),'equal_limits':p['left']==p['right'] if level=='moderate' else 'unassessed','defined':p['value'] is not None if level=='moderate' else 'unassessed','value_matches':p['value']==p['left'] if level=='moderate' and p['left']==p['right'] else 'unassessed','second_continuous':p.get('b_continuous','unassessed'),'second_orientation':int(sp.sign(sp.Rational(str(p['b']))-sp.Rational(str(p['a'])))) if level=='hard' else 'same','grid':.5 if level=='moderate' else .25}
 return digest({'level':level,'assessed_relations':props})
def make_record(level,seed,template,profile,p,problem,solution,bank,correct,raw,spec=None,geometry=None):
 ident=digest({'version':VERSION,'difficulty':None if raw and ':question/difficulty' not in spec['presence'] else level,'problem':problem,'solution':solution,'bank':sorted(bank)})
 q={':question/id':uid(ident),':question/problem':problem}
 if not raw or ':question/difficulty' in spec['presence']:q[':question/difficulty']=':question.difficulty/'+level
 if solution is not None:q[':question/worked-solution']=solution
 if not raw or ':question/answer-fields' in spec['presence']:
  fid=uid(ident+'field');choices=[{':answer/id':uid(fid+v),':answer/type':':answer.type/text',':answer/value':v} for v in bank];random.Random(seed).shuffle(choices)
  f={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
  if correct is not None:f[':answer-field/correct']=[':answer/id',uid(fid+correct)]
  q[':question/answer-fields']=[f]
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':p,'source':{'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'},'evidence_only':raw,'eligible_for_learning':not raw,'mathematical_fingerprint':task_fingerprint(level,template,p), 'plot_geometry':geometry,'dependencies':{'python':sys.version.split()[0],'matplotlib':matplotlib.__version__,'sympy':sp.__version__}}}
def observed(level,seed,sid,parameters,profile):
 s=SPECS[sid];p={'shift':random.Random(seed).choice([-4,-3,-2,-1,0,1,2,3,4])} if parameters is None else dict(parameters)
 if set(p)!={'shift'} or not isinstance(p['shift'],int) or abs(p['shift'])>4:raise ValueError('easy shift must be integer in [-4,4]')
 shift=p['shift'];raw=profile=='observed';a=s['a']+shift;b=s['b']+shift
 vals={'a':str(a),'b':str(b),'a_power':('-' if a<0 else '')+'{'+str(abs(a))+'}','b_power':('-' if b<0 else '')+'{'+str(abs(b))+'}'}
 data=render_source(sid,shift);plot=s['image'] if shift==0 else render_plots(data)
 vals['plot']=plot
 def fill(text):
  for k,v in vals.items():text=text.replace('{{'+k+'}}',v)
  return text
 problem=fill(s['texts'][':question/problem']);solution=fill(s['texts'][':question/worked-solution']) if ':question/worked-solution' in s['texts'] else None
 bank=s['bank'];correct=s['correct']
 if not raw:
  correct=answer_name(source_truth(sid))
  if not bank:bank=['I only','II only','III only','I and II only','I and III only']
  if solution is None:solution='By inspecting the graph, we can conclude the following:\n\n- Statement I is true. Indeed, $f('+str(a)+')=1.$\n\n- Statement II is false. The left and right-sided limits are $1$ and $-2$, so the limit does not exist.\n\n- Statement III is false. The graph has a jump at $x='+str(a)+'$.'
  # Original numeric/bullet list labels are linked to Roman answer subsets in normal output.
  lines=problem.splitlines();idx=0
  for i,line in enumerate(lines):
   if line.startswith('- ') or re_numeric(line):idx+=1;lines[i]=['I. ','II. ','III. '][idx-1]+line.lstrip('- ').removeprefix(str(idx)+'. ')
  problem='\n'.join(lines)
  if sid=='q-48064':problem=problem.replace('$lim_(x → '+str(a)+')f(x)$',r'${lim}_{x\to '+str(a)+r'}f(x)$')
 return make_record(level,seed,sid,profile,p,problem,solution,bank,correct,raw,s,data)
def re_numeric(s):return len(s)>2 and s[0] in '123' and s[1:3]=='. '
# Easy: observed integer-coordinate graph-reading masks and complete banks.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# Moderate: authored fractional grid at one marked point, three interdependent claims.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# Hard: authored quarter grid, two separately assessed neighborhoods including infinity.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)
def authored(level,seed,p,profile):
 if p is not None:
  required={'a','left','right','value'}|({'b','b_continuous'} if level=='hard' else set())
  if set(p)!=required:raise ValueError('exact parameter keys required')
 rng=random.Random(seed);kind=rng.choice(['hole','displaced','jump']) if level=='moderate' else rng.choice(['left_infinite','right_infinite','both_infinite'])
 # Complete eligible bank is selected by semantic topology before numerical parameters.
 if p is None:
  planned_b_continuous=rng.choice([False,True]) if level=='hard' else False
  planned_bits=([kind!='hole',False,False] if level=='moderate' else [kind=='right_infinite',kind!='left_infinite',planned_b_continuous])
 else:
  planned_bits=([p['value'] is not None,p['left']==p['right'] and p['value'] is not None and p['left']==p['value'],False] if level=='moderate' else [not isinstance(p['left'],str),isinstance(p['right'],str),p['b_continuous']])
 planned_correct=answer_name(planned_bits);planned_bank=[planned_correct]+[v for v in SUBSETS if v!=planned_correct][:4]
 if p is None:
  a=rng.choice([-3,-1,1,3])/2 if level=='moderate' else rng.choice([-7,-5,-3,-1,1,3,5,7])/4
  l=rng.choice([-2,-1,0,1,2]);r=l if kind in ['hole','displaced'] else l+2;v=None if kind=='hole' else l+1
  if level=='hard':l='-inf' if kind!='right_infinite' else l;r='+inf' if kind!='left_infinite' else r
  p={'a':a,'left':l,'right':r,'value':v}
  if level=='hard':p.update(b=a+rng.choice([-1,1]),b_continuous=planned_b_continuous)
 else:p=dict(p)
 required={'a','left','right','value'}|({'b','b_continuous'} if level=='hard' else set())
 if set(p)!=required:raise ValueError('exact parameter keys required')
 a=sp.Rational(str(p['a']));
 if abs(a)>2 or a.q!=(2 if level=='moderate' else 4):raise ValueError('authored target uses signed half/quarter grid, |a|<=2')
 for k in ['left','right']:
  z=p[k]
  if isinstance(z,str):
   if level!='hard' or z not in ['+inf','-inf']:raise ValueError('only hard uses infinite limits')
  elif not isinstance(z,int) or isinstance(z,bool) or abs(z)>4:raise ValueError('ordinate outside authored bound')
 if p['value'] is not None and (not isinstance(p['value'],int) or isinstance(p['value'],bool) or abs(p['value'])>4):raise ValueError('value bound')
 if level=='moderate':
  if p['value'] is None and p['left']!=p['right']:raise ValueError('moderate hole topology uses agreeing limits')
  if p['value'] is not None and p['left']==p['right']==p['value']:raise ValueError('moderate requires distinguishing limit from point value')
  bits=[p['value'] is not None,p['left']==p['right'] and p['value'] is not None and p['left']==p['value'],False]
 else:
  b=sp.Rational(str(p['b']));
  if not any(isinstance(p[z],str) for z in ['left','right']) or b.q!=4 or abs(b-a)!=1 or not isinstance(p['b_continuous'],bool):raise ValueError('hard requires infinity and distinct quarter-grid second target')
  bits=[not isinstance(p['left'],str),isinstance(p['right'],str),p['b_continuous']]
 correct=answer_name(bits);bank=planned_bank
 if correct!=planned_correct:raise ValueError('whole selected bank topology mismatch')
 if len(set(bank))!=5:raise ValueError('whole bank criterion collision')
 data=graph(level,p);plot=render_plots(data);at=tex(a);l=p['left'];r=p['right'];v=p['value'];finite=lambda z: not isinstance(z,str);lt=lambda z: (r'\infty' if z=='+inf' else r'-\infty' if z=='-inf' else tex(z))
 if level=='moderate':statements=[rf'$f(x)$ is defined at $x={at}$',rf'${{lim}}_{{x\to {at}}}f(x)=f({at})$',rf'$f(x)$ is continuous at $x={at}$']
 else:statements=[rf'${{lim}}_{{x\to {{{at}}}^-}}f(x)$ is finite',rf'${{lim}}_{{x\to {{{at}}}^+}}f(x)$ is **not** finite',rf'$f(x)$ is continuous at $x={tex(p["b"])}$']
 problem=f'![]({plot})\n\nThe graph of $y=f(x)$ is shown above. Which of the following statements are true?\n\n'+'\n\n'.join(f'{n}. {s}' for n,s in zip(['I','II','III'],statements))
 opening='By inspecting the graph, we can conclude the following:\n\n'
 if level=='moderate':
  sol=[f'- Statement I is {"true" if bits[0] else "false"}. '+(rf'Indeed, $f({at})={tex(v)}.$' if v is not None else rf'No value has been assigned to $f(x)$ at $x={at}.$'),f'- Statement II is {"true" if bits[1] else "false"}. Indeed, from the graph we see that\n\n'+rf'$$\begin{{aligned}}{{lim}}_{{x\to {{{at}}}^-}}f(x)&={lt(l)},\\{{lim}}_{{x\to {{{at}}}^+}}f(x)&={lt(r)}.\end{{aligned}}$$'+'\n\n'+('The two one-sided limits are different, so the limit does not exist.' if l!=r else 'The limit exists, but '+('the function is not defined at the point.' if v is None else 'it is different from the value of the function.')),rf'- Statement III is false. The graph of $f(x)$ breaks at $x={at}$; it is impossible to draw the graph in that neighborhood without taking our pencil off of the paper.']
 else:
  sol=[f'- Statement I is {"true" if bits[0] else "false"}. We get '+rf'${{lim}}_{{x\to {{{at}}}^-}}f(x)={lt(l)}.$',f'- Statement II is {"true" if bits[1] else "false"}. We get '+rf'${{lim}}_{{x\to {{{at}}}^+}}f(x)={lt(r)}.$',f'- Statement III is {"true" if bits[2] else "false"}. '+('The graph has no break' if bits[2] else 'The graph has a hole')+rf' at $x={tex(p["b"])}$.']
 return make_record(level,seed,'fractional_value' if level=='moderate' else 'two_neighborhoods',profile,p,problem,opening+'\n\n'.join(sol),bank,correct,False,geometry=data)
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ['easy','moderate','hard']:raise ValueError('difficulty')
 if field_type not in [None,'radio',':answer-field.type/radio']:raise ValueError('radio only')
 if level=='easy':
  if profile not in [None,'observed','normal']:raise ValueError('profile')
  sid=template or random.Random(seed).choice(list(SPECS))
  if sid not in SPECS:raise ValueError('template')
  return observed(level,seed,sid,parameters,profile or 'normal')
 if template not in [None,'fractional_value' if level=='moderate' else 'two_neighborhoods'] or profile not in [None,'authored']:raise ValueError('level/template/profile scope')
 return authored(level,seed,parameters,profile or 'authored')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args();out=[generate(l,args.seed+i,args.template,profile=args.profile) for l in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 if args.format=='json':print(json.dumps(out,indent=2))
 else:
  for rec in out:
   q=rec['question'];print(q[':question/problem']);print('\nChoices:',[a[':answer/value'] for f in q.get(':question/answer-fields',[]) for a in f[':answer-field/choices']]);print('\nSolution:',q.get(':question/worked-solution','[source omitted]'))
if __name__=='__main__':main()
