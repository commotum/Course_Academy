#!/usr/bin/env python3
"""Finding the equation of a perpendicular line — steps 3–7 local draft.

Public API: generate(level, seed=0, template=None, field_type=None,
parameters=None, profile=None); generate_easy/moderate/hard with same keywords.
CLI --difficulty easy|moderate|hard|all --seed N --count N --format markdown|json.

Source basis2275 is immutable. raw:q-ID profiles preserve attribute omissions as evidence; source:q-ID profiles complete missing fields
and normalize presentation but retain historical whole banks. These profiles are
explicit evidence-only, especially opaque banks44337/44606. They use the same
parameterized masks, mathematics and renderer as normal instances. Defaults use
complete, method-derived banks selected before parameters. No source-return path,
DB connections, registration, transactions or engine modifications.

All slopes are nonzero. Easy reads an annotated y-intercept; moderate reads a
non-axis annotated point and substitutes into point-slope form; hard uses the
supplied textual point, with RHS or intercept response. No unknown given slope,
standard-form conversion, horizontal/vertical, parallel or angle/distance branch.
See adjacent extraction for bounded domains and full historical recipe limits.
"""
from __future__ import annotations
import argparse, hashlib, json, os, random, re, sys, tempfile, uuid
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR','/tmp/perpendicular-mpl')
import sympy as sp
import matplotlib
matplotlib.use('Agg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

KP_ID=17592186175922
VERSION='perpendicular-1.0'
ROOT=Path(__file__).with_suffix('')
SOURCE=json.loads((ROOT/'source.json').read_text())
KP=SOURCE['record']
X,Y=sp.symbols('x y')
TEMPLATES={
 'graph_intercept_radio':('easy','radio','q-44337'),
 'graph_intercept_blank':('easy','blank','q-213914'),
 'graph_point_blank':('moderate','blank','q-237193'),
 'graph_point_radio':('moderate','radio','q-44604'),
 'text_equation_blank':('hard','blank','q-237031'),
 'intercept_blank':('hard','blank','q-237197'),
 'intercept_radio':('hard','radio','q-44606'),
}
ANCHORS={
 'q-213914':dict(a='3',c='2',u='0',v='2'),
 'q-44604':dict(a='1/2',c='0',u='-4',v='10'),
 'q-237031':dict(a='4',c='-6',u='8',v='-3'),
 'q-237193':dict(a='-4',c='-3',u='4',v='2'),
 'q-237197':dict(a='2/5',c='-2',u='6',v='-1'),
 'q-44337':dict(a='2',c='-1',u='0',v='6'),
 'q-44606':dict(a='1/2',c='-3',u='-1',v='5'),
}
SOURCES={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}

def tex(z):
 z=sp.Rational(z)
 if z.q==1:return str(z.p)
 return ('-' if z<0 else '')+r'\frac{'+str(abs(z.p))+'}{'+str(z.q)+'}'
def add(z, spaced=False):
 z=sp.Rational(z)
 if z==0:return ''
 return (' + ' if spaced and z>0 else ' - ' if spaced else '+' if z>0 else '-')+tex(abs(z))
def line(a,b,spaced=False):
 return ('y = ' if spaced else 'y=')+tex(a)+('x' if not spaced else 'x')+add(b,spaced)
def historical_equation(sid,a,b):
 # q44604's original complete bank has a space before positive slopes only.
 if sid=='q-44604':return 'y ='+(' ' if a>0 else '')+tex(a)+'x'+add(b,True)
 return line(a,b)
def rhs(a,b):return tex(a)+'x'+add(b)
def par(z):return '('+tex(z)+')' if z<0 else tex(z)
def sub(z):return 'x-'+par(z)
def simple_sub(z):return 'x'+add(-z)
def lhs(z,initial=False):return 'y-'+par(z) if initial else 'y'+add(-z)
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,s))
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def values(p):
 a,c,u,v=[sp.Rational(p[k]) for k in ('a','c','u','v')]
 return a,c,u,v,-1/a,v+u/a

# Extract complete mathematical component masks once; never substitute short numerals.
def component_mask(text,replacements):
 for old,new in sorted(replacements.items(),key=lambda kv:-len(kv[0])):
  if old not in text:raise ValueError('missing complete component '+old)
  text=text.replace(old,new)
 return text

def make_masks():
 out={}
 for sid,q in SOURCES.items():
  a,c,u,v,m,b=values(ANCHORS[sid]); spaced=sid in ('q-213914','q-44604')
  problem=q[':question/problem']
  old=line(a,c,spaced)
  problem=component_mask(problem,{old:'@@given@@'})
  if not sid.startswith('q-213914') and sid not in ('q-44604','q-237193','q-44337'):
   problem=component_mask(problem,{'('+tex(u)+','+tex(v)+')':'@@point@@'})
  sol=q.get(':question/worked-solution')
  if sol:
   repl={}
   if '$'+line(a,c)+',$' in sol:repl['$'+line(a,c)+',$']='$@@given@@,$'
   repl['$'+tex(a)+',$']='$@@a@@,$'
   repl['$'+tex(m)+'.$']='$@@m@@.$'
   repl['$m='+tex(m)+'$']='$m=@@m@@$'
   if '$({x}_{1},{y}_{1})=('+tex(u)+','+tex(v)+').$' in sol:
    repl['$({x}_{1},{y}_{1})=('+tex(u)+','+tex(v)+').$']='$({x}_{1},{y}_{1})=@@point@@.$'
   if sid=='q-44337':repl['$'+tex(b)+'.$']='$@@b@@.$'
   if '$b='+tex(b)+'.$' in sol:repl['$b='+tex(b)+'.$']='$b=@@b@@.$'
   # Replace entire display block separately; preserve source stage count/whitespace.
   display=sol.split('$$')[1]
   sol=sol.replace('$$'+display+'$$','$$@@display@@$$')
   sol=component_mask(sol,repl)
  out[sid]={'problem':problem,'solution':sol,'spaced':spaced}
 return out
MASKS=make_masks()

def rows(p):
 a,c,u,v,m,b=values(p)
 r=[r'y-{y}_{1} & =m(x-{x}_{1})',lhs(v,True)+' & ='+tex(m)+'('+sub(u)+')']
 if u<0:r.append(lhs(v,True)+' & ='+tex(m)+'('+simple_sub(u)+')')
 r.append(lhs(v)+' & ='+rhs(m,-m*u))
 r.append('y & ='+rhs(m,b))
 return r

def solution(sid,p):
 a,c,u,v,m,b=values(p)
 mask=MASKS[sid]['solution']
 if mask is None:
  # Inferred completions use observed shared prose and the corresponding method.
  donor='q-44337' if u==0 else 'q-237193'
  mask=MASKS[donor]['solution']
 if sid=='q-44337' or (sid=='q-213914'):
  display='\n'+line(m,b)+'.\n'
 else:
  display='\n'+r'\begin{aligned}'+' \\\\ '.join(rows(p))+r'\end{aligned}'+'\n'
 parts={'given':line(a,c),'a':tex(a),'m':tex(m),'b':tex(b),'point':'('+tex(u)+','+tex(v)+')','display':display}
 return render_mask(mask,parts)

def render_mask(mask,parts):
 for key,val in parts.items():mask=mask.replace('@@'+key+'@@',str(val))
 if '@@' in mask:raise ValueError('unfilled slot')
 return mask

def historical(sid,p):
 """Whole evidence banks; opaque recipes are literal structural hypotheses."""
 a,c,u,v,m,b=values(p)
 if sid=='q-44337':return [(a,b),(m,b),(1/a,0),(-b,-a),(-a,b)]
 if sid=='q-44604':return [(m,b),(-a,v+a*u),(m,u),(a,v-a*u),(1/a,v-a*u)]
 if sid=='q-44606':return [m,-u,b,u,v-a*u]
 return [b if sid=='q-237197' else m*X+b]

def method_bank(template,p):
 a,c,u,v,m,b=values(p)
 if template=='graph_intercept_blank':return [m*X+b]
 if template=='graph_intercept_radio':
  return [(m,b),(a,b),(1/a,b),(-a,b),(m,c)]
 if template=='graph_point_radio':
  return [(m,b),(a,v-a*u),(1/a,v-u/a),(-a,v+a*u),(m,v+m*u)]
 if template=='intercept_radio':
  return [b,v-a*u,v-u/a,v+a*u,-m*u]
 return [b if template=='intercept_blank' else m*X+b]

def bank_recipes(template,sid,evidence):
 if evidence:
  return {'q-44337':['given-slope/marked-intercept','negative-reciprocal/marked-intercept','positive-reciprocal/zero-intercept','opaque-negative-intercept-as-slope/negative-given-slope-as-intercept','negative-given-slope/marked-intercept'],
          'q-44604':['negative-reciprocal/point-derived-intercept','negative-given-slope/point-derived-intercept','negative-reciprocal/x-coordinate-as-intercept','given-slope/point-derived-intercept','positive-reciprocal/intercept-from-given-slope'],
          'q-44606':['perpendicular-slope-as-intercept','opaque-negative-x-coordinate','point-derived-correct-intercept','opaque-x-coordinate','given-slope-substitution']}.get(sid,['correct-fragment'])
 if template=='graph_intercept_radio':return ['correct','given-slope','reciprocal-sign-error','negative-given-slope','given-line-intercept']
 if template=='graph_point_radio':return ['correct','given-slope-substitution','reciprocal-sign-error-substitution','negative-given-slope-substitution','point-slope-distribution-sign-error']
 if template=='intercept_radio':return ['correct','given-slope-substitution','reciprocal-sign-error-substitution','negative-given-slope-substitution','omit-point-y-coordinate']
 return ['correct-fragment']

def bank_math(bank):
 return [Y-s*X-t if isinstance(z,tuple) else z for z in bank for s,t in ([z] if isinstance(z,tuple) else [(0,0)])]
def unique_bank(bank):
 objs=bank_math(bank)
 return len(set(map(str,map(sp.expand,objs))))==len(objs)

def guard(level,template,p,evidence=False):
 if set(p)!=set('acuv'):raise ValueError('parameters must be exactly a,c,u,v')
 a,c,u,v,m,b=values(p)
 if not a or any(z.q!=1 for z in (c,u,v)):raise ValueError('nonzero rational slope and integer coordinates/intercept required')
 if abs(a.p)>5 or a.q>5 or any(abs(z)>12 for z in (c,u,v)) or abs(b)>24:raise ValueError('bounded arithmetic domain violated')
 if template.startswith('graph_intercept') and u!=0:raise ValueError('intercept must be on y-axis')
 if template.startswith('graph_point') and (not u or not v):raise ValueError('moderate point must be off both axes')
 if template=='graph_point_blank' and a.q!=1:raise ValueError('integer known slope required by moderate blank source')
 if template=='text_equation_blank' and a.q!=1:raise ValueError('integer known slope required by text equation source')
 if template.startswith('intercept') and a.q==1 and not evidence:raise ValueError('hard intercept sources have fractional known slopes')
 if not evidence and (not v or not b or abs(a)==1):raise ValueError('nondegenerate instructional workload required')
 if not evidence and u and (u/a).q!=1:raise ValueError('source workload requires integral distributed offset')
 if not evidence and template.startswith('graph_intercept') and a.q!=1:raise ValueError('easy known slope must be integer')
 if not evidence and template=='graph_point_radio' and (abs(a.p)!=1 or a.q==1):raise ValueError('moderate radio known slope must be a signed unit fraction')
 if template in ('text_equation_blank','intercept_blank','intercept_radio') and not u:raise ValueError('non-axis supplied point required')

def sample(level,template,rng):
 integers=[i for i in range(-5,6) if abs(i)>1]
 if template in ('graph_point_blank','text_equation_blank'):a=rng.choice(integers)
 elif template=='graph_point_radio':a=rng.choice([sp.Rational(n,d) for n in (-1,1) for d in range(2,6)])
 elif template.startswith('intercept'):
  a=rng.choice(sorted({sp.Rational(n,d) for n in range(-5,6) if n for d in range(2,6) if sp.Rational(n,d).q>1}))
 else:a=rng.choice(integers)
 c=rng.randint(-8,8)
 if template.startswith('graph_intercept'):u=0;v=rng.choice([i for i in range(-8,9) if i])
 else:
  u=rng.choice([i for i in range(-12,13) if i and (sp.Rational(i)/a).q==1])
  v=rng.choice([i for i in range(-10,11) if i])
 return dict(a=str(a),c=str(c),u=str(u),v=str(v))

# Matplotlib renderer, instance-derived native geometry, unique atomic writes.
def render_plots(p,template,output_dir=None):
 a,c,u,v,m,b=values(p)
 data={'a':str(a),'c':str(c),'u':str(u),'v':str(v),'m':str(m),'b':str(b),'template':template,'renderer':matplotlib.__version__,'geometry_revision':5}
 target=Path(output_dir or ROOT/'plots');target.mkdir(parents=True,exist_ok=True)
 name=digest(data);png=target/(name+'.png');side=target/(name+'.json')
 if png.exists() and side.exists():return {'prompt':str(png),'sidecar':str(side)}
 cross_x=float((b-c)/(a-m));cross_y=float(a*sp.Rational(str(cross_x))+c)
 # Include the marked reading cue, both intercepts, origin and crossing.
 xs=[0,float(u),cross_x];ys=[0,float(v),float(c),float(b),cross_y]
 margin=2.5;lo=min(xs+ys)-margin;hi=max(xs+ys)+margin
 # Equal unit scaling gives actual perpendicular geometry, avoiding source unscaled ambiguity.
 fig=Figure(figsize=(4.8,4.2),dpi=120);FigureCanvasAgg(fig)
 ax=fig.add_axes([.08,.08,.86,.86]);ax.set_xlim(lo,hi);ax.set_ylim(lo,hi);ax.set_aspect('equal')
 ax.axis('off')
 ax.annotate('',(hi,0),(lo,0),arrowprops=dict(arrowstyle='->',color='black',lw=1))
 ax.annotate('',(0,hi),(0,lo),arrowprops=dict(arrowstyle='->',color='black',lw=1))
 ax.text(hi-.4,-.7,'$x$',fontsize=12);ax.text(.3,hi-.6,'$y$',fontsize=12)
 xx=[lo,hi]
 ax.plot(xx,[float(a)*t+float(c) for t in xx],color='blue',lw=1.6)
 ax.plot(xx,[float(m)*t+float(b) for t in xx],color='red',lw=1.6)
 if u!=0:
  ax.plot([float(u),float(u)],[0,float(v)],'--',color='gray',lw=.8)
  ax.plot([0,float(u)],[float(v),float(v)],'--',color='gray',lw=.8)
  ax.annotate('$'+tex(u)+'$',(float(u),0),xytext=(0,-15 if v>0 else 7),textcoords='offset points',ha='center',fontsize=11)
 ax.plot([float(u)],[float(v)],'o',color='red',ms=5)
 ax.annotate('$'+tex(v)+'$',(0,float(v)),xytext=(-17,3),textcoords='offset points',ha='right',fontsize=11)
 # Move each complete line-name glyph away from both actual zero axes.
 # Calibrate its native text bbox before accepting a candidate; geometry is unchanged.
 fig.canvas.draw()
 origin=ax.transData.transform((0,0))
 for slope,intercept,label in [(a,c,'$l_1$'),(m,b,'$l_2$')]:
  candidates=[(lo+(hi-lo)*f,float(slope)*(lo+(hi-lo)*f)+float(intercept)) for f in [i/40 for i in range(1,40)]]
  visible=sorted([z for z in candidates if lo+1<z[1]<hi-1],key=lambda z:(z[0]-cross_x)**2+(z[1]-cross_y)**2,reverse=True)
  for pt in visible:
   offset=(-18 if pt[0]<0 else 8,-17 if pt[1]<0 else 9)
   name=ax.annotate(label,pt,xytext=offset,textcoords='offset points',fontsize=12)
   fig.canvas.draw()
   bx,by,bw,bh=name.get_window_extent(fig.canvas.get_renderer()).bounds
   axis_clear=(bx+bw<=origin[0]-4 or bx>=origin[0]+4) and (by+bh<=origin[1]-4 or by>=origin[1]+4)
   if axis_clear and bx>=4 and by>=4 and bx+bw<=572 and by+bh<=500:break
   name.remove()
  else:raise ValueError('no readable line-label placement')
 fig.canvas.draw()
 data.update(bounds=[lo,hi],size=[576,504],point_pixel=list(map(float,ax.transData.transform((float(u),float(v))))),crossing=[cross_x,cross_y],labels=['x','y','l_1','l_2',tex(v)]+([tex(u)] if u else []),unit_pixels=float(ax.transData.transform((1,0))[0]-ax.transData.transform((0,0))[0]),origin_pixel=list(map(float,ax.transData.transform((0,0)))),text_boxes=[{'text':t.get_text(),'bbox':list(map(float,t.get_window_extent(fig.canvas.get_renderer()).bounds))} for t in ax.texts])
 fd,tmp=tempfile.mkstemp(prefix='.render-',suffix='.png',dir=target);os.close(fd)
 try:fig.savefig(tmp,dpi=120,facecolor='white');os.replace(tmp,png)
 finally:
  if os.path.exists(tmp):os.unlink(tmp)
 fd,tmp=tempfile.mkstemp(prefix='.render-',suffix='.json',dir=target)
 try:
  with os.fdopen(fd,'w') as f:json.dump(data,f,indent=2)
  os.replace(tmp,side)
 finally:
  if os.path.exists(tmp):os.unlink(tmp)
 return {'prompt':str(png),'sidecar':str(side)}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('unknown difficulty')
 rng=random.Random(seed)
 raw=bool(profile and profile.startswith('raw:'));evidence=bool(profile and profile.startswith(('raw:','source:')))
 sid=profile.split(':',1)[1] if evidence else None
 eligible=[k for k,v in TEMPLATES.items() if v[0]==level and (field_type is None or v[1]==field_type) and (sid is None or v[2]==sid)]
 if template is None:
  if not eligible:raise ValueError('no compatible template')
  template=rng.choice(eligible)
 if template not in eligible:raise ValueError('template/level/type/profile mismatch')
 _,kind,donor=TEMPLATES[template];sid=sid or donor
 if profile is None:profile='method-derived'
 if not evidence and profile!='method-derived':raise ValueError('unknown profile')
 if parameters is not None:p={k:str(v) for k,v in parameters.items()}
 else:p=ANCHORS[sid].copy() if evidence else None
 if p is not None:p={k:str(sp.Rational(v)) for k,v in p.items()}
 for attempt in range(1000):
  if p is None:p=sample(level,template,rng)
  try:
   guard(level,template,p,evidence)
   bank=historical(sid,p) if evidence else method_bank(template,p)
   if not unique_bank(bank):raise ValueError('whole bank collision')
   break
  except ValueError:
   if parameters is not None or evidence:raise
   p=None
 else:raise RuntimeError('no valid instance')
 a,c,u,v,m,b=values(p)
 source=SOURCES[sid];mask=MASKS[sid]
 prompt=render_mask(mask['problem'],{'given':line(a,c,mask['spaced']),'point':'('+tex(u)+','+tex(v)+')'})
 plots={}
 if '![](' in prompt:
  orig=re.search(r'!\[\]\(([^)]+)\)',prompt).group(1)
  if evidence and p==ANCHORS[sid]:plots={'prompt':str(ROOT/'original-plots'/Path(orig).name),'original':orig}
  else:
   plots=render_plots(p,template);prompt=prompt.replace(orig,plots['prompt'])
 if not raw:
  # q213914 joins question and supplied y=; preserve math shape, add normal line separation.
  prompt=prompt.replace('?$y =$', '?\n\n$y =$')
 sol=solution(sid,p)
 answer_text=[]
 for z in bank:
  if isinstance(z,tuple):value=historical_equation(sid,*z) if evidence else line(*z)
  else:value=tex(z) if not sp.sympify(z).has(X) else rhs(sp.expand(z).coeff(X),sp.expand(z).subs(X,0))
  answer_text.append(value)
 if evidence and sid=='q-44606':answer_text[-1]=str(float(bank[-1])) if sp.Rational(bank[-1]).q==2 else tex(bank[-1])
 # Mathematical identity excludes irrelevant given-line intercept and response/bank aliases.
 task={'given_slope':str(a),'required_point':[str(u),str(v)],'information':'graph-intercept' if template.startswith('graph_intercept') else 'graph-point' if template.startswith('graph_point') else 'text-point'}
 has_choices=not(raw and ':answer-field/choices' not in source[':question/answer-fields'][0])
 has_correct=not(raw and ':answer-field/correct' not in source[':question/answer-fields'][0])
 has_solution=not(raw and ':question/worked-solution' not in source)
 has_difficulty=not(raw and ':question/difficulty' not in source)
 ident=digest({'version':VERSION,'difficulty':level if has_difficulty else None,'prompt':prompt,'solution':sol if has_solution else None,'bank':sorted(answer_text) if has_choices else None,'kind':kind,'correct_present':has_correct})
 field_key='field-1' if kind=='blank' else 'selection'
 field={':answer-field/id':uid(ident+'/field'),':answer-field/key':field_key,':answer-field/type':':answer-field.type/'+kind}
 answers=[{':answer/id':uid(ident+'/answer/'+text),':answer/type':':answer.type/math',':answer/value':text} for text in answer_text]
 correct_value=tex(b) if template.startswith('intercept') else (historical_equation(sid,m,b) if evidence else line(m,b)) if kind=='radio' else rhs(m,b)
 correct=next((z for z in answers if z[':answer/value']==correct_value),None)
 if correct is None:raise ValueError('correct value not in bank')
 if has_choices:
  rng.shuffle(answers);field[':answer-field/choices']=answers
 if has_correct:field[':answer-field/correct']=[':answer/id',correct[':answer/id']]
 question={':question/id':uid(ident),':question/problem':prompt,':question/answer-fields':[field]}
 if has_solution:question[':question/worked-solution']=sol
 if has_difficulty:question[':question/difficulty']=':question.difficulty/'+level
 return {'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':question,'generation':{'version':VERSION,'template':template,'profile':profile,'bank_recipes':bank_recipes(template,sid,evidence),'seed':seed,'parameters':p,'source_id':sid,'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'mathematical_fingerprint':digest(task),'content_fingerprint':ident,'evidence_only':evidence,'eligible_for_learning':not evidence,'inferred_completion':sid in ('q-213914','q-44604') and not raw,'plots':plots,'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':matplotlib.__version__}}}

# Easy: one negative reciprocal plus an explicitly marked y-intercept.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('easy',seed,template,field_type,parameters,profile)
# Moderate: read a non-axis graph point; same ordered point-slope substitution/distribution.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('moderate',seed,template,field_type,parameters,profile)
# Hard: text point plus point-slope arithmetic; fractional given slopes for intercept fields.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
 q=record['question'];out=[q[':question/problem']]
 for f in q.get(':question/answer-fields',[]):
  out.extend('- $'+z[':answer/value']+'$' for z in f.get(':answer-field/choices',[]))
 if ':question/worked-solution' in q:out.extend(['',q[':question/worked-solution']])
 return '\n'.join(out)
def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile')
 ar=ap.parse_args();levels=['easy','moderate','hard'] if ar.difficulty=='all' else [ar.difficulty]
 records=[generate(level,ar.seed+i,ar.template,profile=ar.profile) for level in levels for i in range(ar.count)]
 print(json.dumps(records,indent=2) if ar.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
