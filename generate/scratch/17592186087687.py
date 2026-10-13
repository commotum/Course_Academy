#!/usr/bin/env python3
"""Standard-form parallel-line recognition, frozen math basis 1356.

All source practice is unrated, without keys/solutions. Public q-* profiles are
raw evidence replays, preserving these omissions. completed:q-* profiles infer
keys and canonical-example solutions but remain evidence-only: historical banks
are opaque expression patterns. Normal practice uses complete method-error banks.
Easy, moderate and hard vary bounded coefficient arithmetic in the same three
isolation stages; no unknown parameters, perpendicularity, or equation writing.
"""
from __future__ import annotations
import argparse, hashlib, json, math, random, sys, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186087687
KP_UUID='d5bf8c8b-64f1-5552-a59e-78eef021c122'
TITLE='Identifying Parallel Lines Given in Standard Form'
VERSION='standard-parallel-3.0'
HERE=Path(__file__).resolve().with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
SUPPORTED_LEVELS=('easy','moderate','hard')
TEMPLATES=('standard-radio',)
# Complete observed banks. These homothetic expression-pattern recipes reproduce
# all source equations; error intent is unresolved, so never normal defaults.
BANK_PROFILES={
 'q-110094':(('-1','2/3'),('-3/2','2/15'),('4','5/9'),('4/9','-1/3'),('1','1/9')),
 'q-13400':(('1','-3/2'),('-1/8','-1'),('1/4','1/2'),('-1/4','2'),('2','0')),
 'q-22574':(('7/2','1/14'),('-1','2/7'),('1','0'),('3/2','-1/14'),('-2','2/21'))}
AUTHORED_PROFILES=('method-sign-reciprocal','method-sign-division')
SOURCE_CASES={'q-110094':{'A':6,'B':-4,'C':9},'q-13400':{'A':8,'B':-1,'C':2},'q-22574':{'A':4,'B':2,'C':7}}
SOURCE_LEVELS={'q-110094':'moderate','q-13400':'easy','q-22574':'moderate'}
DOMAIN={
'easy':'2<=abs(A)<=12; abs(B)=1; 1<=C<=12. Unit y coefficient; integer slope.',
'moderate':'2<=abs(A)<=12; 2<=abs(B)<=6; gcd(abs(A),abs(B))>1; reduced abs numerator<=6 and denominator<=3; 1<=C<=12. Divide and reduce familiar coefficients.',
'hard':'5<=abs(A)<=12; 3<=abs(B)<=6; gcd(abs(A),abs(B))=1; 1<=C<=12. Primitive noninteger slope with larger numerator/denominator; same isolation method.'}
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),v))
def tex(v):
 r=sp.Rational(v)
 return str(r) if r.q==1 else ('-' if r<0 else '')+r'\frac{'+str(abs(r.p))+'}{'+str(r.q)+'}'
def term(k,var):return ('' if k==1 else '-' if k==-1 else tex(k))+var
def standard(p):return term(p['A'],'x')+(' - ' if p['B']<0 else ' + ')+term(abs(p['B']),'y')+' = '+str(p['C'])
def line(m,b,observed=False):
 prefix='y ='+('' if m<0 else ' ') if observed else 'y = '
 return prefix+term(m,'x')+((' - ' if b<0 else ' + ')+tex(abs(b)) if b else '')
def parameters(level,p,evidence=False):
 if set(p)!={'A','B','C'} or any(type(v)!=int for v in p.values()):raise ValueError('Integer A,B,C required')
 A,B,C=p['A'],p['B'],p['C'];a,b=abs(A),abs(B)
 if not 2<=a<=12 or not 1<=b<=6 or not 1<=C<=12:raise ValueError('Outside overall source-grounded bounds')
 m=sp.Rational(a,b)
 eligible=(b==1) if level=='easy' else ((2<=a<=12 and 2<=b<=6 and math.gcd(a,b)>1 and m.p<=6 and m.q<=3) if level=='moderate' else (5<=a<=12 and 3<=b<=6 and math.gcd(a,b)==1))
 if not evidence and not eligible:raise ValueError('Outside '+level+' arithmetic workload: '+DOMAIN[level])
 return dict(p)
def task_key(p):
 # Recognition assesses the reduced slope; RHS and coefficient scaling do not
 # create new assessed recognition tasks. Content identity retains all of them.
 return digest({'slope':str(sp.Rational(-p['A'],p['B']))})
def line_key(p):
 return [str(sp.Rational(p[k],p['B'])) for k in ('A','B','C')]
def bank(p,profile):
 A,B,C=p['A'],p['B'],p['C'];m=sp.Rational(-A,B);b=sp.Rational(C,B)
 if profile in BANK_PROFILES:
  vals=[(m*sp.Rational(r),C*sp.Rational(s)) for r,s in BANK_PROFILES[profile]]
  labels=['opaque_observed_pattern_'+str(i) for i in range(5)]
 else:
  # Fixed complete banks, selected before sampling. All errors are actual slope
  # operations. Equal/ambiguous slopes reject the whole bank, with no replacements.
  fourth=sp.Integer(A) if profile=='method-sign-reciprocal' else sp.Integer(-A)
  vals=[(m,b+1),(-m,b-1),(1/m,b+2),(-1/m,b-2),(fourth,b+3)]
  labels=['correct_slope_distinct_intercept','fail_to_negate_x_coefficient','invert_slope_ratio','negative_reciprocal','ignore_y_divisor' if profile=='method-sign-division' else 'copy_x_coefficient']
 if len(set(vals))!=5 or sum(v[0]==m for v in vals)!=1:raise ValueError('Whole bank rejected: slope ambiguity')
 if any(v[0]==m and v[1]==b for v in vals):raise ValueError('Whole bank rejected: coincident line')
 return vals,labels

def solution(p,answer):
 A,B,C=p['A'],p['B'],p['C'];m=sp.Rational(-A,B);b=sp.Rational(C,B)
 return ('For two lines to be parallel, they must have the same slope.\n\n'
 f'To find the slope of the line ${standard(p)}$, we convert to slope-intercept form:\n\n'
 '$$\n\\begin{aligned}\n'+standard(p).replace(' = ',' &= ')+' \\\\\n'+term(B,'y')+' &= '+term(-A,'x')+' + '+str(C)+' \\\\\n'+line(m,b).replace(' = ',' &= ')+'\n\\end{aligned}\n$$\n\n'
 f'In slope-intercept form, the slope is the $x$-coefficient. So, the slope is ${tex(m)}$.\n\n'
 'From the given options, the only line that has a slope of $'+tex(m)+'$ is\n\n$$\n'+answer+'\n$$')
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in SUPPORTED_LEVELS:raise ValueError('Unknown difficulty')
 if template not in (None,'standard-radio') or field_type not in (None,'radio'):raise ValueError('Only standard-radio/radio supported')
 raw=profile in BANK_PROFILES;completed=bool(profile and profile.startswith('completed:'))
 bp=profile.removeprefix('completed:') if completed else profile
 evidence=raw or completed
 if bp is not None and bp not in (*BANK_PROFILES,*AUTHORED_PROFILES):raise ValueError('Unknown complete profile')
 if completed and bp not in BANK_PROFILES:raise ValueError('Completion applies only to source profiles')
 rng=random.Random(seed)
 # For fixed parameters, choose an eligible complete profile independently of seed.
 if bp is None:
  chooser=random.Random(json.dumps(parameters,sort_keys=True)) if parameters is not None else rng
  eligible=AUTHORED_PROFILES
  if parameters is not None:
   eligible=tuple(x for x in eligible if eligible_bank(parameters,x))
   if not eligible:raise ValueError('Whole bank rejected: no eligible complete profile')
  bp=chooser.choice(eligible)
 for attempt in range(256):
  p=globals()['parameters'](level,parameters,evidence) if parameters is not None else sample(level,rng)
  try:vals,labels=bank(p,bp)
  except ValueError:
   if parameters is not None:raise
   continue
  break
 else:raise ValueError('No eligible complete instance sampled')
 texts=[line(m,b,evidence) for m,b in vals];m=sp.Rational(-p['A'],p['B']);correct=texts[next(i for i,v in enumerate(vals) if v[0]==m)]
 prompt=f'Which of the following lines is parallel to ${standard(p)}$?'
 sol=None if raw else solution(p,correct)
 content=digest({'version':VERSION,'level':None if raw else level,'problem':prompt,'solution':sol,'bank':sorted(texts),'correct':None if raw else correct})
 qid=uid('question:'+content);fid=uid(qid+':field:selection')
 answers=[{':answer/id':uid(fid+':answer:'+v),':answer/type':':answer.type/math',':answer/value':v} for v in texts]
 aid=next(a[':answer/id'] for a in answers if a[':answer/value']==correct);rng.shuffle(answers)
 f={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
 q={':question/id':qid,':question/problem':prompt,':question/answer-fields':[f]}
 if not raw:q.update({':question/difficulty':':question.difficulty/'+level,':question/worked-solution':sol});f[':answer-field/correct']=[':answer/id',aid]
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'python_version':sys.version.split()[0],'sympy_version':sp.__version__,'seed':seed,'template':'standard-radio','parameters':p,'bank_profile':profile or bp,'recipes':labels,'parameter_fingerprint':task_key(p),'standard_line_fingerprint':digest(line_key(p)),'content_fingerprint':content,'domain':DOMAIN[level],'source_analysis':{'database':SOURCE['database'],'basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'source_ids':[bp] if evidence else [],'canonical_example':'e-14367'},'difficulty_origin':'absent in raw source' if raw else 'authored workload classification','key_origin':'absent in raw source' if raw else 'independently inferred from displayed slope','solution_origin':'absent in raw source' if raw else 'authored parameterization of canonical e-14367 prose and three stages','bank_origin':'opaque observed expression-pattern replay' if evidence else 'authored method-error bank','evidence_only':evidence,'eligible_for_learning':not evidence,'plot_rating':'none'}}
def eligible_bank(p,bp):
 try:bank(p,bp);return True
 except (ValueError,ZeroDivisionError):return False
def sample(level,rng):
 A,B=rng.choice(COEFFICIENTS[level]);return {'A':A,'B':B,'C':rng.randint(1,12)}
def coefficient_domain(level):
 out=[]
 for A in range(-12,13):
  for B in range(-6,7):
   try:parameters(level,{'A':A,'B':B,'C':1})
   except ValueError:continue
   if any(eligible_bank({'A':A,'B':B,'C':1},bp) for bp in AUTHORED_PROFILES):out.append((A,B))
 return tuple(out)
COEFFICIENTS={l:coefficient_domain(l) for l in SUPPORTED_LEVELS}
SLOPES={l:tuple(sorted({sp.Rational(-A,B) for A,B in COEFFICIENTS[l]})) for l in SUPPORTED_LEVELS}
# EASY: one unit-y-coefficient isolation; integer slopes, no denominator reduction.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: same isolation, nonunit familiar reducible coefficients; source-grounded.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: same isolation, primitive 5..12 numerator and 3..6 denominator; authored.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)
def batch(level,count,seed=0,template=None,field_type=None,profile=None):
 if not 1<=count<=len(SLOPES[level]):raise ValueError('Distinct slope task limit '+str(len(SLOPES[level])))
 rng=random.Random(seed);slopes=list(SLOPES[level]);rng.shuffle(slopes);out=[]
 for i,m in enumerate(slopes[:count]):
  A,B=rng.choice([(A,B) for A,B in COEFFICIENTS[level] if sp.Rational(-A,B)==m]);out.append(generate(level,seed+i,template,field_type,{'A':A,'B':B,'C':rng.randint(1,12)},profile))
 return out
def markdown(rec):
 q=rec['question'];f=q[':question/answer-fields'][0];cid=f.get(':answer-field/correct',[None,None])[1]
 return q[':question/problem']+'\n\n'+'\n'.join(('- [x] ' if a[':answer/id']==cid else '- [ ] ')+'$'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','Raw source replay: difficulty, key and worked solution are absent.')
def main():
 cli=argparse.ArgumentParser(description=__doc__);cli.add_argument('--difficulty',choices=(*SUPPORTED_LEVELS,'all'),default='all');cli.add_argument('--seed',type=int,default=0);cli.add_argument('--count',type=int,default=1);cli.add_argument('--format',choices=('json','markdown'),default='markdown');cli.add_argument('--template',choices=TEMPLATES);cli.add_argument('--profile',choices=(*BANK_PROFILES,*('completed:'+x for x in BANK_PROFILES),*AUTHORED_PROFILES));cli.add_argument('--field-type',choices=('radio',));args=cli.parse_args()
 try:out=[r for l in (SUPPORTED_LEVELS if args.difficulty=='all' else (args.difficulty,)) for r in batch(l,args.count,args.seed,args.template,args.field_type,args.profile)]
 except ValueError as exc:cli.error(str(exc))
 print(json.dumps(out,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,out)))
if __name__=='__main__':main()
