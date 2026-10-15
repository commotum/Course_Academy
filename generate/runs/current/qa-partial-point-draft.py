import sys
sys.dont_write_bytecode=True
import re,json,hashlib,copy,importlib.util
from pathlib import Path
R=Path(__file__).resolve().parent;K=17592186124644;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=load('parent_scalar_partial_point',R/'ode-scalar-parser.py');s=p.s
counts={'records':0,'source_banks':0,'source_values':0,'source_keys':0,'source_missing_keys':0,'source_solutions':0,'derivative_stages':0,'point_stages':0,'choices':0,'normal_complete_banks':0,'individually_split_derivatives':0}
def same(a,b):return s.simplify(s.trigsimp((a-b).doit()))==0
def balanced(text,start):
 assert text[start] in '({'
 closing=')' if text[start]=='(' else '}';depth=1;i=start+1
 while depth:
  assert i<len(text),text
  if text[i]==text[start]:depth+=1
  elif text[i]==closing:depth-=1
  i+=1
 return text[start+1:i-1],i

def math(raw):
 text=raw.strip().replace(r'\left','').replace(r'\right','').replace(r'\dfrac',r'\frac').replace(r'\partial','∂')
 replacements={}
 op=re.compile(r'\\frac\{∂\}\{∂([xy])\}')
 while (match:=op.search(text)):
  start=match.end()
  while text[start].isspace():start+=1
  operand,end=balanced(text,start);var=getattr(p,match[1]);symbol=(p.t,p.u,p.v,p.z)[len(replacements)]
  replacements[symbol]=s.Derivative(math(operand),var,evaluate=False)
  text=text[:match.start()]+'('+str(symbol)+')'+text[end:]
 return p.scalar(text).xreplace(replacements)
def point(text):
 parts=[];depth=0;begin=0
 for i,ch in enumerate(text):
  if ch in '({':depth+=1
  elif ch in ')}':depth-=1
  elif ch==',' and depth==0:parts.append(text[begin:i]);begin=i+1
 parts.append(text[begin:]);assert len(parts)==2
 return dict(zip((p.x,p.y),map(math,parts)))
def prompt(q):
 islands=re.findall(r'(?<!\$)\$(?!\$)(.*?)\$',q[':question/problem'],re.S)
 F=math(islands[0].split('=',1)[1]);ask=islands[1]
 target=re.search(r'(?:∂|\\partial)\s*([xy])',ask) or re.search(r'_\{?([xy])\}?',ask);assert target
 tupletext=islands[2].strip().rstrip('.,') if len(islands)==3 else ask[ask.index('('):].strip().rstrip('.,')
 assert tupletext[0]=='(' and tupletext[-1]==')'
 return F,getattr(p,target[1]),point(tupletext[1:-1])
def prose(text):return re.sub(r'\$\$.*?\$\$|(?<!\$)\$(?!\$).*?(?<!\$)\$(?!\$)','[MATH]',text,flags=re.S)
def stages(text):
 groups=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',text,re.S);assert len(groups)==2
 result=[]
 for group in groups:
  rows=group.split(chr(92)*2);values=[]
  for row in rows:
   lhs,rhs=row.split('&',1);assert rhs.strip().startswith('=');values.append((lhs.strip(),rhs.strip()[1:].strip()))
  result.append(values)
 return result

def additive_pieces(text):
 depth=0;start=0;parts=[]
 for i,ch in enumerate(text):
  if ch in '({[':depth+=1
  elif ch in ')}]':depth-=1
  elif ch in '+-' and depth==0 and i>start:
   parts.append(text[start:i]);start=i
 assert depth==0
 parts.append(text[start:]);return parts

def individual_stages(F,var,rendered_rows):
 expected=[s.diff(t,var) for t in s.Add.make_args(F)]
 for _,text in rendered_rows:
  terms=additive_pieces(text);assert len(terms)==len(expected),(text,F)
  remaining=list(expected)
  for term in terms:
   value=math(term);matches=[i for i,want in enumerate(remaining) if same(value,want)];assert len(matches)==1,(term,F,remaining)
   remaining.pop(matches[0])
  assert not remaining
 return len(expected)*len(rendered_rows)

def check(record,source=False):
 q=record['question'];F,var,pt=prompt(q);derivative=s.diff(F,var);C=s.simplify(derivative.subs(pt));fields=q[':question/answer-fields'];assert len(fields)==1
 f=fields[0];assert f[':answer-field/type']==':answer-field.type/radio';values=[math(a[':answer/value']) for a in f[':answer-field/choices']];assert len(values)==5
 for i,a in enumerate(values):assert all(not same(a,b) for b in values[:i])
 good=[same(v,C) for v in values];assert sum(good)==1
 if ':answer-field/correct' in f:assert good[next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])]
 if not source:
  terms=s.Add.make_args(F);assert len(terms)==2
  contributions=[s.diff(z,var).subs(pt) for z in terms];A,B=contributions;expected=[A+B,A-B,-A+B,A,B]
  assert all(sum(same(a,b) for b in expected)==1 for a in values)
  counts['normal_complete_banks']+=1
 if ':question/worked-solution' in q:
  text=q[':question/worked-solution'];drows,erows=stages(text)
  assert len(drows) in (5,6) and len(erows) in (2,3)
  for lhs,rhs in drows:assert same(math(rhs),derivative),(rhs,F,derivative)
  for lhs,rhs in erows:assert same(math(rhs),C),(rhs,F,pt,C)
  for lhs,_ in [drows[0],erows[0]]:
   m=re.search(r'∂([xy])|_\{?([xy])\}?',lhs);assert m and next(v for v in m.groups() if v)==str(var),(lhs,var)
  assert 'with respect to $'+str(var)+',$' in text
  dsplit=next(rhs for _,rhs in drows if len(list(math(rhs).atoms(s.Derivative)))==2)
  individual=list(math(dsplit).atoms(s.Derivative));assert len(individual)==2
  assert all(z.variables==(var,) for z in individual)
  assert all(sum(same(z.expr,t) for t in s.Add.make_args(F))+sum(same(-z.expr,t) for t in s.Add.make_args(F))>=1 for z in individual)
  counts['individually_split_derivatives']+=2
  count=individual_stages(F,var,drows[-4:-1]);counts['individual_operative_contributions']=counts.get('individual_operative_contributions',0)+count
  # The evaluated LHS and prose must carry the same physical coordinate pair.
  lhs=erows[0][0];coords=balanced(lhs,lhs.index('('))[0];got=point(coords);assert all(same(got[v],pt[v]) for v in pt)
  counts['derivative_stages']+=len(drows);counts['point_stages']+=len(erows)
 counts['records']+=1;counts['choices']+=len(values)
 return q

if __name__=='__main__':
 g=load('parent_review_partial_point',D.with_suffix('.py'))
 source=json.loads((R/'refresh-2026-10-14/sources'/f'{K}.json').read_text());assert json.loads((D/'source.json').read_text())==source
 originals={z[':question/math-academy-id']:z for z in source['record'][':knowledge-point/questions']}
 for case in json.loads((D/'source-cases.json').read_text()):
  old=originals[case['source_id']];new=check(g.generate(case['difficulty'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']),True)
  assert prose(old[':question/problem'])==prose(new[':question/problem'])
  oldF,oldt,oldpt=prompt(old);newF,newt,newpt=prompt(new);assert same(oldF,newF) and oldt==newt and all(same(oldpt[v],newpt[v]) for v in oldpt)
  oldf=old[':question/answer-fields'][0];newf=new[':question/answer-fields'][0];remaining=[math(z[':answer/value']) for z in newf[':answer-field/choices']]
  for z in oldf[':answer-field/choices']:
   matches=[i for i,v in enumerate(remaining) if same(math(z[':answer/value']),v)];assert len(matches)==1;remaining.pop(matches[0]);counts['source_values']+=1
  assert not remaining;counts['source_banks']+=1
  for key in (':question/difficulty',':question/worked-solution'):assert (key in old)==(key in new)
  if ':answer-field/correct' in oldf:
   designated=next(z[':answer/value'] for z in newf[':answer-field/choices'] if z[':answer/id']==newf[':answer-field/correct'][1]);assert same(math(designated),math(oldf[':answer-field/correct'][':answer/value']));counts['source_keys']+=1
  else:assert ':answer-field/correct' not in newf;counts['source_missing_keys']+=1
  if ':question/worked-solution' in old:
   assert prose(old[':question/worked-solution'])==prose(new[':question/worked-solution'])
   oldst,newst=stages(old[':question/worked-solution']),stages(new[':question/worked-solution'])
   for a,b in zip(oldst,newst):
    assert len(a)==len(b)
    for (_,av),(_,bv) in zip(a,b):assert same(math(av),math(bv))
   counts['source_solutions']+=1
 samples=json.loads((R/'qa'/f'{K}-sampled.json').read_text())
 for record in samples:check(record)
 for record in json.loads((D/'samples.json').read_text()):check(record)
 mutant=copy.deepcopy(samples[0]);original=mutant['question'][':question/worked-solution'];groups=stages(original);bad=groups[0][-2][1];mutant['question'][':question/worked-solution']=original.replace(bad,'('+bad+')+1',1);assert original!=mutant['question'][':question/worked-solution']
 saved=copy.deepcopy(counts)
 try:check(mutant)
 except AssertionError:pass
 else:raise AssertionError('Wrong intermediate derivative survived unchanged correct answer')
 counts=saved;counts.update(status='passed',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),unchanged_key_wrong_intermediate_rejected=True,database_writes=0)
 (R/'qa'/f'{K}-root-readback.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
