"""Independently solve the three named topics from their displayed operands."""
from pathlib import Path
import collections,importlib.util,json,re
import sympy as s
from scripts.question_capture.math_format import MATH,cells,environment,normalize_tex,matrix_tex
P=Path(__file__).resolve().parent
import types
parser=types.ModuleType('matrix_audit_parser')
exec((P.parents[3]/'generate/runs/current/vector-math-parser.py').read_text().replace('[tuvxyzijke]', '[A-Za-z]'),parser.__dict__)
parser.locals_.update({c:s.Symbol(c,real=True) for c in 'abcdfghlmnopqrwABCDEFGHIJKLMNOPQRSTUVWXYZ'})
proposals={(x['entity'],x['attribute']):x['new'] for x in json.loads((P/'source-proposals.json').read_text())}
def scalar(text):
 text=re.sub(r'\\text\{\s*\}','',text).replace('\xa0','').replace(r'\dfrac',r'\frac').replace(r'\tfrac',r'\frac')
 text=re.sub(r"(?<![\w.])([0-9]+)\.([0-9]+)",lambda m:r"\frac{"+str(int(m[1]+m[2]))+"}{"+str(10**len(m[2]))+"}",text)
 return parser.scalar(text)
def matrices(text):
 text=normalize_tex(text);out=[]
 for m in re.finditer(r'\\begin\{(bmatrix|pmatrix|matrix)\}',text):
  span=environment(text,m.start());assert span
  rr=cells(text[span[0]:span[1]]);assert rr and len({len(r) for r in rr})==1
  arr=s.Matrix([[scalar(c) for c in r] for r in rr]);pre=text[:m.start()];label=re.search(r'\{?([A-Z])\}?\s*=\s*$',pre)
  out.append(dict(name=label[1] if label else None,matrix=arr,rows=rr,start=m.start(),end=span[2]))
 return out

def tex(m):return matrix_tex([[s.latex(v) for v in m.row(i)] for i in range(m.rows)])
def same(a,b):
 if isinstance(a,s.MatrixBase) and isinstance(b,s.MatrixBase):return a.shape==b.shape and all(s.simplify(v)==0 for v in a-b)
 return a==b

def classify(m,kind):
 return {'zero':lambda:not any(m),'square':lambda:m.rows==m.cols,'diagonal':lambda:m.rows==m.cols and all(m[i,j]==0 for i in range(m.rows) for j in range(m.cols) if i!=j),'identity':lambda:m.rows==m.cols and m==s.eye(m.rows),'row':lambda:m.rows==1,'column':lambda:m.cols==1}[kind]()

def option_value(value,target):
 if isinstance(target,set):return set(re.findall(r'\$([A-Z])\$',value))
 if isinstance(target,tuple):
  m=re.fullmatch(r'\s*(\d+)\s*\\(?:times|cdot)\s*(\d+)\s*',value.strip('$'));assert m,value;return tuple(map(int,m.groups()))
 if isinstance(target,s.MatrixBase):
  ms=matrices(value);assert len(ms)==1,value;return ms[0]['matrix']
 if isinstance(target,str):return value
 return scalar(value.split('=',1)[-1])

report=[];key_proposals=[];solution_proposals=[];issues=[];layout_targets=[]
for topic in [862,146,232]:
 t=json.loads((P/(str(topic)+'-priority.json')).read_text())
 for kp in t[':topic/knowledge-points']:
  title=kp[':knowledge-point/title']
  for q in [kp[':knowledge-point/canonical-example']]+kp[':knowledge-point/questions']:
   e=q[':db/id'];example=q is kp[':knowledge-point/canonical-example'];prompt=proposals.get((e,'question/problem'),q[':question/problem']);
   if e==17592186059552:prompt='Find $C^T$, if\n\n$$C='+r'\begin{bmatrix}-1 & 1 \\ 0 & 2 \\ -2 & -3\end{bmatrix}'+'$$'
   ms=matrices(prompt);fs=q.get(':question/answer-fields',[]);checks=[]
   try:
    if topic==862:
     kind=next((k for k in ['zero','square','diagonal','identity','row','column'] if re.search(r'are '+k+r' (?:matrices|vectors)',prompt)),None)
     if kind:
      target={m['name'] for m in ms if classify(m['matrix'],kind)};assert None not in target
      solution='\n\n'.join('- $'+m['name']+'$ '+('is' if m['name'] in target else 'is not')+' a '+kind+(' vector' if kind in ['row','column'] else ' matrix')+'.' for m in ms)+'\n\nTherefore, '+(', '.join('$'+n+'$' for n in sorted(target))+' '+('satisfies' if len(target)==1 else 'satisfy')+' the definition.' if target else 'none of the matrices satisfy the definition.')
     else:
      assert len(ms)==1
      m=ms[0]['matrix'];target=next((label for label,kind in [('A zero matrix','zero'),('An identity matrix','identity'),('A row vector','row'),('A column vector','column'),('A diagonal matrix','diagonal')] if classify(m,kind)),'Other')
      bank=[a[':answer/value'] for f in fs for a in f.get(':answer-field/choices',[])]
      if target not in bank and not example:
       # Existing wording uses "An identity matrix" / "An ..." variants; retain exact bank wording.
       target=next((v for v in bank if v.lower().removeprefix('a ').removeprefix('an ')==target.lower().removeprefix('a ').removeprefix('an ')),target)
      solution=f'The matrix has ${m.rows}$ rows and ${m.cols}$ columns. '+('It is rectangular, with more than one row and column, so none of the named special types apply.' if target=='Other' else 'It is '+target.lower()+'.')
    elif topic==232:
     assert len(ms)==1
     m=ms[0]['matrix'];target=(m.cols,m.rows) if 'Dimensions' in title else m.T
     solution=f'To find the transpose, we interchange the rows and columns.\n\n$$\n{ms[0]["name"] or "A"}^T={tex(target)}\n$$' if isinstance(target,s.MatrixBase) else f'The original matrix has ${m.rows}$ rows and ${m.cols}$ columns. Transposing interchanges them, so its transpose has dimensions ${m.cols}\\times {m.rows}$.'
    elif 'Value of a Scalar' in title:
     if len(ms)==1:
      # Existing explanation supplies the omitted prior-part matrix; flag context before using it.
      original=matrices(q.get(':question/worked-solution',''))[0]['matrix'];given=ms[0]['matrix'];issues.append(dict(entity=e,kind='missing-prior-part-context',detail='P is referenced but its definition is absent from the prompt'))
     elif 'original payoff matrix' in prompt:
      assert len(ms)==2;original,given=[m['matrix'] for m in ms]
     else:assert len(ms)==2;given,original=[m['matrix'] for m in ms]
     ratios={s.simplify(a/b) for a,b in zip(given,original) if b!=0};assert len(ratios)==1;target=ratios.pop();assert given==target*original
     solution='Multiplying by $k$ scales every entry. Equating corresponding nonzero entries gives\n\n$$\nk='+s.latex(target)+'.\n$$'
    else:
     if 'Linear Combination' in title:
      assert len(ms)==2
      expr=re.search(r'Calculate\s*\$([^$]+)\$',prompt)[1];expr=normalize_tex(expr);byname={m['name']:m['matrix'] for m in ms};assert len(byname)==2
      target=s.zeros(*ms[0]['matrix'].shape)
      terms=re.findall(r'([+-]?\s*(?:\\frac\{[^{}]+\}\{[^{}]+\}|\d+(?:/\d+)?)?\s*)\{?([A-Z])\}?',expr)
      assert len(terms)==2,(e,expr,terms)
      for coeff,name in terms:
       coeff=coeff.strip();coeff=coeff+'1' if coeff in ['','+','-'] else coeff;target+=scalar(coeff)*byname[name]
      solution='Multiply each matrix by its scalar, then add corresponding entries:\n\n$$\n'+expr+'='+tex(target)+'\n$$'
     else:
      assert len(ms)==1
      mt=re.search(r'Calculate\s*\$([^$]+)\$',prompt)
      if mt:expr=normalize_tex(mt[1]);coef=re.sub(r'\{?[A-Z]\}?','',expr)
      else:
       first=next(MATH.finditer(prompt));body=normalize_tex(first[0]);coef=body[:body.index(r'\begin{bmatrix}')];expr=coef+'A'
      target=scalar(coef)*ms[0]['matrix'];solution='Multiply every entry by $'+coef+'$:\n\n$$\n'+tex(target)+'\n$$'
    if not example and not fs:issues.append(dict(entity=e,kind='no-fields',detail='Known computed answer; original controls must be recovered',expected=tex(target) if isinstance(target,s.MatrixBase) else str(target)))
    for f in fs:
     kind=f[':answer-field/type'][':db/ident'];key=f[':answer-field/key'];expected=target
     if kind.endswith('/checkbox'):expected=str(key in target).lower()
     elif kind.endswith('/blank'):
      if isinstance(target,s.MatrixBase):
       # Preserve exact authored table position, including fixed entries.
       table=[line for line in prompt.splitlines() if line.strip().startswith('|') and not re.match(r'^\s*\|[\s:|\-]+\|\s*$',line)]
       if table:
        table_cells=[]
        for line in table:
         vs=[z.strip().strip('$').strip() for z in line.strip().strip('|').split('|')];vs=[z for z in vs if z and '=' not in z];table_cells.extend(vs)
        assert len(table_cells)==target.rows*target.cols,(e,len(table_cells),target.shape)
        index=table_cells.index('{{'+key+'}}');expected=target[index]
       else:raise ValueError('Matrix blank has no explicit supported row mapping')
      elif isinstance(target,tuple):expected=s.Integer(target[int(key.split('-')[-1])-1])
     bank=f.get(':answer-field/choices',[]);matches=[]
     for a in bank:
      try:
       if same(option_value(a[':answer/value'],expected),expected):matches.append(a)
      except (AssertionError,ValueError):pass
     assert matches,(e,key,'no matching owned answer',str(expected))
     correct=f.get(':answer-field/correct');matching_correct=correct and any(a[':db/id']==correct[':db/id'] for a in matches)
     if correct and not matching_correct:issues.append(dict(entity=e,kind='wrong-correct-answer',field=f[':db/id'],expected=str(expected),stored=correct[':answer/value']))
     if not correct:
      assert len(matches)==1,(e,key,'ambiguous bank')
      key_proposals.append(dict(question=e,field=f[':db/id'],correct=matches[0][':db/id'],value=matches[0][':answer/value'],expected=str(expected),kp=kp[':db/id']))
     checks.append(dict(field=f[':db/id'],key=key,expected=str(expected),matchingOwnedChoices=len(matches),correct=bool(matching_correct)))
    # Spot coordinates are factual assertions even when the final selection is right.
    for label,row,col,value in re.findall(r'\$\{?([a-z])\}?_\{([1-9])([1-9])\}=([^$=]+?)\\n(?:eq|e)\s*0\$',q.get(':question/worked-solution','')):
     matrix=next((m['matrix'] for m in ms if m['name']==label.upper()),None)
     if matrix is not None and (int(row)>matrix.rows or int(col)>matrix.cols or scalar(value)!=matrix[int(row)-1,int(col)-1]):issues.append(dict(entity=e,kind='wrong-witness-coordinate',detail=f'{label}_{row}{col}={value}'))
    if not example and not q.get(':question/worked-solution'):solution_proposals.append(dict(entity=e,new=solution,kp=kp[':db/id']))
    report.append(dict(entity=e,kp=kp[':db/id'],topic=topic,role='example' if example else 'practice',expected=tex(target) if isinstance(target,s.MatrixBase) else sorted(target) if isinstance(target,set) else str(target),checks=checks))
   except (AssertionError,ValueError,KeyError,StopIteration,TypeError) as ex:issues.append(dict(entity=e,kind='math-review-required',detail=str(ex)))
(P/'priority-math-report.json').write_text(json.dumps(report,indent=2));(P/'priority-math-issues.json').write_text(json.dumps(issues,indent=2));(P/'key-proposals.json').write_text(json.dumps(key_proposals,indent=2));(P/'solution-proposals.json').write_text(json.dumps(solution_proposals,indent=2));print('Independently solved',len(report),'items,',sum(len(x['checks']) for x in report),'fields.');print('Missing-key repairs:',len(key_proposals),'missing solutions:',len(solution_proposals));print(json.dumps(issues,indent=2))
