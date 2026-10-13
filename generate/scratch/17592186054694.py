#!/usr/bin/env python3
"""Plotting a Line Using a Table: bounded, source-bank-aware easy generator.
No database operations. CLI --difficulty easy --count N --seed N --format json|markdown.
Moderate/hard unsupported in this validated package. Source evidence basis 2025.
"""
from __future__ import annotations
import argparse,hashlib,json,os,random,re,sys,uuid
from pathlib import Path
try: import sympy as sp
except ImportError:
 runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python'
 if __name__=='__main__':os.execv(str(runtime),[str(runtime),__file__,*sys.argv[1:]])
 raise
KP_ID=17592186054694
KP_UUID='2491cf6c-260b-5992-a910-9fe6a80e30bc'
TITLE='Plotting a Line Using a Table'
VERSION='line-table-1'
HERE=Path(__file__).resolve().with_suffix('')
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
os.environ.setdefault('MPLCONFIGDIR',str(HERE/'matplotlib-cache'))
S=json.loads((HERE/'source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in S['record'][':knowledge-point/questions']}
TEMPLATES={'unit_positive':{'level':'easy','source':'q-54397','m':1,'b':-2},'unit_negative':{'level':'easy','source':'q-59676','m':-1,'b':1},'double_positive':{'level':'easy','source':'q-71695','m':2,'b':2}}
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def rhs(m,b):
 m=sp.Rational(m);b=sp.Rational(b)
 return ('x' if m==1 else '-x' if m==-1 else sp.latex(m)+'x')+('+'+sp.latex(b) if b>0 else '-'+sp.latex(-b) if b<0 else '')
def arithmetic(m,b,i):return ('' if m==1 else '-' if m==-1 else str(m))+f'({i})'+('+'+str(b) if b>0 else '-'+str(-b) if b<0 else '')+'='+str(m*i+b)
def fingerprint(q):
 text=q[':question/problem'];match=re.search(r'\$y\s*=\s*([^$]+)\$',text)
 if not match:raise ValueError('Unknown current task')
 value=match[1].replace(' ','').rstrip('.');value=re.sub(r'(\d)x',r'\1*x',value)
 x=sp.Symbol('x');p=sp.Poly(sp.sympify(value,locals={'x':x}),x)
 if p.degree()!=1:raise ValueError('Unexpected non-linear source')
 return digest([str(p.nth(1)),str(p.nth(0))])
def candidates(template):
 bs=(-6,-4,-2,2,4,6) if template!='unit_negative' else (-3,-2,-1,1,2,3)
 return [{'m':TEMPLATES[template]['m'],'b':b} for b in bs]
def bank(template,p):
 m,b=sp.Integer(p['m']),sp.Integer(p['b'])
 if template=='unit_positive':return [(-m,0),(m,b),(-m,-b/2),(m,-b),(m,0)]
 if template=='unit_negative':return [(m,2*b),(-m,-2*b),(-m,-b),(2*m,4*b),(m,b)]
 if template=='double_positive':return [(m,-b),(-m,b),(-m/2,b),(m,b),(m/2,b)]
 raise ValueError('Unknown template')
def render_plot(m,b,points_only,limits,output_dir):
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 import numpy as np
 data={'m':str(m),'b':str(b),'points_only':points_only,'limits':limits,'x_table':[0,1,2,3],'y_table':[str(m*i+b) for i in range(4)]}
 path=Path(output_dir)/('line-'+digest(data)+'.png');path.parent.mkdir(parents=True,exist_ok=True)
 if path.exists():return str(path)
 fig,ax=plt.subplots(figsize=(4,4));fig.subplots_adjust(left=.13,right=.95,bottom=.12,top=.95)
 xmin,xmax,ymin,ymax=limits
 ax.set(xlim=(xmin,xmax),ylim=(ymin,ymax),aspect='equal')
 step=2 if ymax<=12 else 4
 ax.set_xticks(range(0,xmax+1,step));ax.set_xticks(list(range(-step,xmin-1,-step))+list(range(0,xmax+1,step)));ax.set_yticks(list(range(-step,ymin-1,-step))+list(range(0,ymax+1,step)))
 ax.set_xticks(range(xmin,xmax+1),minor=True);ax.set_yticks(range(ymin,ymax+1),minor=True);ax.grid(which='both',color='#d2d2d2',lw=.65)
 for side in ('top','right'):ax.spines[side].set_visible(False)
 ax.spines['left'].set_position('zero');ax.spines['bottom'].set_position('zero');ax.tick_params(labelsize=7,length=2)
 ax.set_xlabel('$x$',loc='right');ax.set_ylabel('$y$',loc='top',rotation=0)
 if not points_only:
  xx=np.linspace(xmin,xmax,401);ax.plot(xx,float(m)*xx+float(b),color='red',lw=1.8)
 ax.plot(range(4),[float(m*i+b) for i in range(4)],'o',color='blue',ms=4)
 fig.savefig(path,dpi=120,metadata={'Software':'Course Academy '+VERSION});plt.close(fig)
 data['sha256']=hashlib.sha256(path.read_bytes()).hexdigest();Path(str(path)+'.json').write_text(json.dumps(data,indent=2));return str(path)
def generate(level,seed=0,template=None,parameters=None,replay=False):
 if level!='easy':raise ValueError('Unsupported difficulty; see capabilities.json')
 template=template or random.Random(seed).choice(list(TEMPLATES));info=TEMPLATES[template]
 p=dict(parameters or random.Random(seed).choice(candidates(template)))
 if p not in candidates(template):raise ValueError('Outside bounded parameter policy')
 m,b=p['m'],p['b'];src=SOURCES[info['source']]
 if replay and p!={'m':info['m'],'b':info['b']}:raise ValueError('Replay requires source parameters')
 lines=bank(template,p)
 if len(set(lines))!=5 or sum(line==(m,b) for line in lines)!=1:raise ValueError('Ambiguous bank')
 fp=digest([str(m),str(b)]);qid=str(uuid.uuid5(uuid.UUID(KP_UUID),VERSION+':'+fp));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
 ys=[int(s*i+c) for s,c in lines for i in range(4)];lim=max(6,max(abs(y) for y in ys)+1);limits=[-lim,lim,-lim,lim]
 # Source templates retain their exact Markdown, including legacy table alignment.
 old_eq=re.search(r'\$y\s*=\s*([^$]+)\$',src[':question/problem'])[0]
 prompt=src[':question/problem'] if replay else src[':question/problem'].replace(old_eq,'$y='+rhs(m,b)+'.$')
 assets=[a[':answer/value'] for a in src[':question/answer-fields'][0][':answer-field/choices']] if replay else [render_plot(s,c,False,limits,HERE/'images') for s,c in lines]
 correct_index=lines.index((m,b));solsrc=src if ':question/worked-solution' in src else SOURCES['q-54397'];sm,sb=(info['m'],info['b']) if ':question/worked-solution' in src else (1,-2)
 sol=solsrc[':question/worked-solution']
 # Tokenize before replacement: prevents equal source numbers from interfering.
 for i in range(4):sol=sol.replace(arithmetic(sm,sb,i),f'@@CALC{i}@@')
 oldrow='| $y$ | '+' | '.join('$'+str(sm*i+sb)+'$' for i in range(4))+' |'
 sol=sol.replace(oldrow,'@@ROW@@').replace('y='+rhs(sm,sb),'y=@@EQ@@')
 found=re.findall(r'!\[\]\(([^)]+)\)',sol);assert len(found)==2
 sol=sol.replace(found[0],'@@POINTS@@').replace(found[1],'@@LINE@@')
 points=found[0] if replay and ':question/worked-solution' in src else render_plot(m,b,True,limits,HERE/'images')
 sol=sol.replace('@@EQ@@',rhs(m,b)).replace('@@ROW@@','| $y$ | '+' | '.join('$'+str(m*i+b)+'$' for i in range(4))+' |').replace('@@POINTS@@',points).replace('@@LINE@@',assets[correct_index])
 for i in range(4):sol=sol.replace(f'@@CALC{i}@@',arithmetic(m,b,i))
 assert '@@' not in sol
 answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),'line:'+str(s)+','+str(c))),':answer/type':':answer.type/image',':answer/value':asset} for (s,c),asset in zip(lines,assets)]
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':sol,':question/difficulty':':question.difficulty/easy',':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[correct_index][':answer/id']]}]},'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':p,'bank_profile':info['source'],'source_question':info['source'],'source_basis':S['basis'],'source_lineage':S['lineage'],'mathematical_fingerprint':fp,'domain':'x,y real; integral nonzero slope and intercept in documented bounded policy','replay':replay,'lines':[[str(s),str(c)] for s,c in lines],'assets':assets+[points],'dependencies':{'sympy':sp.__version__,'matplotlib':__import__('matplotlib').__version__,'numpy':__import__('numpy').__version__},'difficulty_origin':'easy observed q-54397/q-71695; negative template authored equivalent workload','fidelity_limits':'q-59676 has no key/solution/difficulty; these are derived additions. Source raster pixels are reused only in source replay.'}}
def batch(level,count,seed):
 if level!='easy':raise ValueError('Unsupported difficulty')
 if count<1:raise ValueError('Positive count required')
 ps=[(t,p) for t in TEMPLATES for p in candidates(t)];random.Random(seed).shuffle(ps)
 if count>len(ps):raise ValueError('Finite limit: 18 tasks before source/current-pool exclusions')
 return [generate(level,seed,t,p) for t,p in ps[:count]]
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n\n'.join('![]('+a[':answer/value']+')' for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
def main():
 a=argparse.ArgumentParser();a.add_argument('--difficulty',required=True);a.add_argument('--count',type=int,default=1);a.add_argument('--seed',type=int,default=0);a.add_argument('--format',choices=['json','markdown'],default='json');o=a.parse_args();r=batch(o.difficulty,o.count,o.seed);print(json.dumps(r,indent=2) if o.format=='json' else '\n\n'.join(map(markdown,r)))
if __name__=='__main__':main()
