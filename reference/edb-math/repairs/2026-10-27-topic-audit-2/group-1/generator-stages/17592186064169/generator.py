#!/usr/bin/env python3
"""Seeded reciprocal-power antiderivatives, repaired against math basis 4609.

Easy/moderate source prompts and solutions with explicitly authored choice grids.
Observed full banks and missing-field parity remain available for source replay.
No runtime repository imports, database operations, or asset writes.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, math, random, uuid
from integral_display import display_integral
from math_format import checked_math_content, normalize_prose, normalize_tex
from pathlib import Path
import sympy as sp

KP_ID=17592186064169
KP_UUID='3174cae9-484e-5ca3-8e5c-3c9cddc86145'
TITLE='Finding the Antiderivative of a Reciprocal Function'
VERSION='reciprocal-power-v2-format-audit-9122-v1'
X=sp.Symbol('x', positive=True)
C=sp.Symbol('C', real=True)
PROVENANCE={'database':'math','basis':4609,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
TEMPLATES={
 'negative_named_radio': {'level':'easy','source':'q-29987','form':'negative','layout':'old'},
 'reciprocal_named_radio': {'level':'easy','source':'q-29989','form':'reciprocal','layout':'old'},
 'negative_named': {'level':'easy','source':'q-71100','form':'negative','layout':'named'},
 'reciprocal_named': {'level':'moderate','source':'q-113705','form':'reciprocal','layout':'named'},
 'reciprocal_integer': {'level':'moderate','source':'q-29633','form':'reciprocal','layout':'integer'},
 'reciprocal_sqrt': {'level':'moderate','source':'q-29662','form':'sqrt','layout':'sqrt'},
 'reciprocal_sqrt_named': {'level':'moderate','source':'q-29993','form':'sqrt','layout':'named'},
 'reciprocal_integer_equals': {'level':'easy','source':'q-29643','form':'reciprocal','layout':'integer'},
}
ORIGINAL_PARAMETERS={'q-29987':{'p':2,'q':3},'q-29989':{'p':3,'q':5},
 'q-71100':{'p':1,'q':7},'q-113705':{'p':4,'q':3},
 'q-29633':{'p':4,'q':1},'q-29662':{'p':5,'q':2},
 'q-29993':{'p':3,'q':2},'q-113703':{'p':3,'q':2},'q-29643':{'p':5,'q':1},'e-368':{'p':3,'q':1}}
RAW_PROFILES={f'raw_{v["source"]}':t for t,v in TEMPLATES.items() if v['source']}
OPENING="Remember that integration is the opposite of differentiation. So, if ${F}^{'}(x)=f(x),$ then integrating both sides of this equation gives\n\n$$\n\\begin{aligned}{F}^{'}(x) & =f(x) \\\\ \\int {F}^{'}(x)\\,\\text{d}x & =\\int f(x)\\,\\text{d}x \\\\ F(x) & =\\int f(x)\\,\\text{d}x.\\end{aligned}\n$$\n\n"

def slug(value):
 return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def ident(text): return str(uuid.uuid5(uuid.UUID(KP_UUID),text))
def rat(v):
 v=sp.Rational(v)
 return str(v) if v.q==1 else ('-' if v<0 else '')+r'\frac{'+str(abs(v.p))+'}{'+str(v.q)+'}'
def slash(v): return str(sp.Rational(v))
def power(e,braced=False): return ('{x}' if braced else 'x')+('' if sp.Rational(e)==1 else '^{'+slash(e)+'}')
def term(a,e,braced=False,space=False):
 a=sp.Rational(a)
 coefficient='' if a==1 else '-' if a==-1 else rat(a)
 return coefficient+power(e,braced)+(' + C' if space else '+C')
def reciprocal(a,e,braced=False):
 # e is negative; the absolute coefficient is folded into numerator/denominator.
 a=sp.Rational(a)
 denominator=(str(a.q) if a.q!=1 else '')+power(-e,braced)
 return ('-' if a<0 else '')+r'\frac{'+str(abs(a.p))+'}{'+denominator+'}+C'
def integrand(t,p):
 r=sp.Rational(p['p'],p['q']); conf=TEMPLATES[t]
 if conf['form']=='negative': return power(-r,conf['layout']=='named')
 if conf['form']=='sqrt': return r'\frac{1}{\sqrt{{x}^{'+str(p['p'])+'}}}'
 if conf['form']=='root': return r'\frac{1}{\sqrt['+str(p['q'])+']{{x}^{'+str(p['p'])+'}}}'
 return r'\frac{1}{'+power(r,conf['layout']!='old')+'}'
def prompt(t,p):
 i=integrand(t,p); layout=TEMPLATES[t]['layout']
 if t=='reciprocal_integer_equals': return r'$\int '+i+r'\,\text{d}x=$'
 if layout=='old': return 'Given that $f(x) = '+i+'$ and that $F^{′}(x) = f(x)$, calculate $F(x)$.'
 if layout=='named': return "Given that $f(x)="+i+"$ and that ${F}^{'}(x)=f(x)$, calculate $F(x).$"
 if layout=='integer': return 'What is the antiderivative of $'+i+'?$'
 return 'Calculate the integral of $'+i+'$'

def solution(t,p,raw=False):
 r=sp.Rational(p['p'],p['q']); n=-r; m=n+1; a=1/m
 i=integrand(t,p); layout=TEMPLATES[t]['layout']; b=layout!='old'
 if layout=='old':
  # No source solution exists. This is an explicitly authored completion.
  note=('We can use the power rule with $n='+rat(n)+'$ and get' if TEMPLATES[t]['form']=='negative' else 'Note that $'+i+'='+power(n)+'.$ So, we can use the power rule with $n='+rat(n)+'$ and get')
  return OPENING+note+'\n\n$$\n\\begin{aligned}F(x) & =\\int f(x)\\,\\text{d}x \\\\ & =\\int '+power(n)+r'\,\text{d}x \\ & =\frac{'+('x^{'+slash(n)+'+1}')+'}{('+rat(n)+'+1)}+C \\\\ & ='+term(a,m)+'.\\end{aligned}\n$$'
 note='We can use the power rule with $n='+rat(n)+'$ and get' if TEMPLATES[t]['form']=='negative' else 'Note that $'+i+'='+(r'\frac{1}{'+power(r,True)+'}=' if TEMPLATES[t]['form'] in ('sqrt','root') and t!='reciprocal_sqrt_named' else '')+power(n,True)+'.$ So, we can use the power rule with $n='+rat(n)+'$ and get'
 if layout=='named':
  rows=[r'F(x) & =\int '+(i if t=='reciprocal_sqrt_named' else 'f(x)')+r'\,\text{d}x',r' & =\int '+power(n,True)+r'\,\text{d}x',r' & =\frac{{x}^{'+slash(n)+'+1}}{('+rat(n)+'+1)}+C',r' & =\frac{'+power(m,True)+'}{('+rat(m)+')}+C',r' & ='+term(a,m,True)]
  if m<0 and t!='reciprocal_sqrt_named': rows.append(r' & ='+reciprocal(a,m,True)+'.')
  else: rows[-1]+='.'
  return OPENING+note+'\n\n$$\n\\begin{aligned}'+r' \\ '.join(rows)+'\\end{aligned}\n$$'
 first=r'\int '+i+(r'\,\text{d}x' if layout!='sqrt' or not raw else '')+r' & =\int '+power(n,True)+r'\,\text{d}x'
 rows=[first,r' & =\frac{{x}^{'+slash(n)+'+1}}{'+rat(n)+'+1}+C']
 if t=='reciprocal_integer_equals':
  rows.append(r' & =\frac{'+power(m,True)+'}{'+rat(m)+'}+C')
 elif layout=='integer':
  rows.append(r' & =-\frac{'+power(m,True)+'}{'+str(abs(1/a))+'}+C')
 else: rows.append(r' & ='+term(a,m,True))
 rows.append(r' & ='+reciprocal(a,m,True)+'.')
 return note+'\n\n$$\n\\begin{aligned}'+r' \\ '.join(rows)+'\\end{aligned}\n$$'


NORMAL_TEMPLATES = {
 'easy': ['negative_named', 'reciprocal_integer_equals'],
 'moderate': ['reciprocal_named', 'reciprocal_integer', 'reciprocal_sqrt', 'reciprocal_sqrt_named'],
}

def domain(level, template):
 if level not in NORMAL_TEMPLATES or template not in NORMAL_TEMPLATES[level]:
  raise ValueError('unsupported difficulty/template')
 if 'integer' in template:
  return [{'p':p,'q':1} for p in range(2,10)]
 if 'sqrt' in template:
  return [{'p':p,'q':2} for p in range(3,10,2)]
 if level=='easy':
  return [{'p':p,'q':q} for q in range(2,10) for p in range(1,q) if math.gcd(p,q)==1]
 return [{'p':p,'q':q} for q in range(2,6) for p in range(q+1,10) if math.gcd(p,q)==1]

def observed_pairs(source_id, p):
 """Complete source-bank formulas; opaque recipes remain replay-only."""
 pp,qq=p['p'],p['q']; n=-sp.Rational(pp,qq); m=n+1; a=1/m
 banks={
 'q-29987':[(1,-n),(pp+qq,-m),(-m,1-n),(a,m),(m,-m)],
 'q-29989':[(n,sp.Rational(pp,qq-pp)),(-1,m),(m,1/m),(m,m),(a,m)],
 'q-71100':[(sp.Rational(qq-2,qq-pp),-m),(a,m),(sp.Rational(1,qq-pp),-n),(-a,m-sp.Rational(1,qq)),(-sp.Rational(1,qq-pp),m)],
 'q-29993':[(-pp,-n),(1,-sp.Rational(1,pp)),(a,m),(-a,-m),(1,n)],
 'q-113703':[(a,m),(a,1-n),(1,m),(1,-m),(n-1,n-1)],
 'q-29643':[(a,m),(-a,m),(a,n),(a,-m),(-1/a,m)],
 }
 return [(sp.Rational(b),sp.Rational(e)) for b,e in banks.get(source_id,[])]

def authored_pairs(n, rng, eligible_parameters):
 """A five-cell grid with two unit-power antiderivatives.

 Assign the correct role to a row/column before filling numerical values. Both
 reciprocal coefficient/exponent pairs survive the missing-cell selection, so
 noticing b*e=1 cannot select the answer without reading the integrand.
 """
 row=rng.randrange(2); col=rng.randrange(3)
 other_col=rng.choice([j for j in range(3) if j!=col])
 decisive={(row,col),(1-row,other_col)}
 missing=rng.choice([(i,j) for i in range(2) for j in range(3) if (i,j) not in decisive])
 m=n+1; a=1/m
 decoy=rng.choice([p for p in eligible_parameters if -sp.Rational(p['p'],p['q'])!=n])
 other_n=-sp.Rational(decoy['p'],decoy['q']); other_m=other_n+1; b=1/other_m
 scale=b/a
 third_col=next(j for j in range(3) if j not in (col,other_col))
 candidates=set()
 for nn in (n,other_n):
  mm=nn+1;candidates.update({nn,nn-1,-mm,1-nn,-nn,mm*3,mm/3})
 candidates=sorted(candidates-{m,other_m,sp.S.Zero})
 candidates=[v for v in candidates if sp.sign(v)==sp.sign(m)]
 exps={col:m,other_col:1/b,third_col:rng.choice(candidates)}
 coeffs={row:a,1-row:b}
 # Filter only the selected missing cell; keep correct first for key derivation.
 pairs=[(a,m)]+[(coeffs[i],exps[j]) for i in range(2) for j in range(3)
                if (i,j)!=(row,col) and (i,j)!=missing]
 assert sum(c*e==1 for c,e in pairs)==2
 return pairs, {'correct_row':row,'correct_column':col,'other_diagonal_column':other_col,'missing_cell':list(missing),'coefficient_scale':str(scale),'third_exponent':str(exps[third_col]),'decoy_parameters':decoy}

@checked_math_content
def generate(level='moderate',seed=0,template=None,parameters=None,profile=None):
 if level not in NORMAL_TEMPLATES: raise ValueError('supported difficulties: easy, moderate; hard has no source evidence')
 if profile not in (None,'authored_two_diagonal_grid'): raise ValueError('use source_replay for observed evidence')
 rng=random.Random(seed)
 template=template or rng.choice(NORMAL_TEMPLATES[level])
 values=domain(level,template)
 params=dict(parameters) if parameters is not None else dict(rng.choice(values))
 if set(params)!={'p','q'} or any(type(v)!=int for v in params.values()) or params not in values:
  raise ValueError('parameters outside supported template domain')
 n=-sp.Rational(params['p'],params['q']);m=n+1;a=1/m
 pairs,layout=authored_pairs(n,rng,values)
 if len(set(pairs))!=5: raise AssertionError('bank collision')
 if sum(b==a and e==m for b,e in pairs)!=1: raise AssertionError('ambiguous bank')
 base=prompt(template,params)
 if template=='reciprocal_integer_equals':
  text=normalize_prose('Assume $x>0$.\n\n'+base)
 else:
  if not base.endswith(('.', '.$', '?$')):base+='.'
  text=normalize_prose(base+' Assume $x>0$.')
 worked=normalize_prose(solution(template,params))
 # All choices in a layout use identical notation; no key-only formatting cue.
 use_reciprocal=TEMPLATES[template]['form']=='reciprocal'
 def render(b,e):
  return normalize_tex(reciprocal(b,e,True) if use_reciprocal and e<0 else term(b,e,True))
 rendered=[render(b,e) for b,e in pairs]
 text=display_integral(text)
 identity=slug({'version':VERSION,'prompt':text,'solution':worked,'bank':sorted(rendered),'difficulty':level})
 fid=ident(identity+'/selection')
 answers=[{':answer/id':ident(fid+'/'+v),':answer/type':':answer.type/math',':answer/value':v} for v in rendered]
 correct=answers[0][':answer/id'];rng.shuffle(answers)
 q={':question/id':ident(identity),':question/problem':text,':question/difficulty':':question.difficulty/'+level,
    ':question/worked-solution':worked,':question/answer-fields':[
    {':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',
     ':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,
 'generation':{'version':VERSION,'source':PROVENANCE,'template':template,'profile':'authored_two_diagonal_grid',
 'level':level,'seed':seed,'parameters':params,'domain':'x>0; n != -1',
 'source_references':[TEMPLATES[template]['source']],
 'origin':'source prompt/solution with authored mixed bank',
 'bank_layout':layout,'bank_pairs':{render(b,e):[str(b),str(e)] for b,e in pairs},
 'mathematical_fingerprint':slug({'n':str(n),'domain':'x>0'}),
 'dependency_versions':{'sympy':sp.__version__}}}

def source_replay(source_id):
 """Immutable captured evidence, retaining missing fields and source labels.

 Formula replay of every bank is checked independently in validate.py. Source
 captures are not default learner records and are not sent to delivery.
 """
 cases=json.loads(Path(__file__).with_name('source_cases.json').read_text())
 q=copy.deepcopy(next(q for q in cases if q[':question/math-academy-id']==source_id))
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,
         'generation':{'source':PROVENANCE,'source_id':source_id,'parameters':ORIGINAL_PARAMETERS[source_id],
                       'evidence_only':True}}

def main():
 parser=argparse.ArgumentParser(description='Source-grounded reciprocal antiderivatives')
 parser.add_argument('--difficulty',choices=['easy','moderate','hard'],default='moderate')
 parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1)
 parser.add_argument('--format',choices=['json'],default='json');parser.add_argument('--template')
 parser.add_argument('--source-replay',choices=list(ORIGINAL_PARAMETERS))
 args=parser.parse_args()
 if args.count<1:parser.error('count must be positive')
 if args.difficulty=='hard':parser.error('hard unsupported: no source evidence')
 records=[source_replay(args.source_replay)] if args.source_replay else [generate(args.difficulty,args.seed+i,template=args.template) for i in range(args.count)]
 print(json.dumps(records,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
