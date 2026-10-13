"""Extract full observed masks, preserving all prose, fields, banks and omissions."""
import importlib.util,json,re
from pathlib import Path
P=Path(__file__).parent
spec=importlib.util.spec_from_file_location('g',P.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
# Point substitution expressions retain the captured operation layout. Only complete
# coordinate factors are slots: symbolic x/y in derivative rows are never replaced.
EVAL={
'q-65204':r'(-\operatorname{cos}⁡({x0})\operatorname{sin}⁡({y0})-({x0})\operatorname{cos}⁡(({x0})\cdot ({y0})))i-(-\operatorname{sin}⁡({x0})\operatorname{cos}⁡({y0})-({y0})\operatorname{cos}⁡(({x0})\cdot ({y0})))j',
'q-130198':r'(-({x0})\operatorname{sin}⁡({y0})+\operatorname{sin}⁡({x0}))i-(\operatorname{cos}⁡({y0})+({y0})\operatorname{cos}⁡({x0}))j',
'q-130200':r'(2({x0})({y0}){e}^{{({y0})^2+1}}+1)i-{e}^{{({y0})^2+1}}\,j',
'q-37516':r'(\frac{{2({x0})}}{{({y0})}}-8({x0}))i-(2\operatorname{ln}⁡({y0})-8({y0}))\,j',
'q-72400':r'(2({y0})-2({x0}))\,i-(2({x0})-2({y0}))\,j',
'q-72463':r'(4({y0})({x0})^{{3}}-4({x0}))i-(6({x0})^{{2}}({y0})^{{2}}-4({y0})+3)j',
'q-130201':r'(({x0})+3({y0})^{{2}})i-(({y0})+2({x0}))j',
'q-72388':r'({x0})^{{2}}\,i-(2({x0})({y0})-1)j',
'q-130192':r'(({x0})^{{2}}-2({y0}))\,i-2({x0})({y0})\,j',
'q-130194':r'\frac{{({x0})}}{{({y0})}}\,i-(\operatorname{ln}⁡({y0})-2({x0}))\,j',
}
# For exact original typography we retain an evaluated row spelling mask. Its
# coordinate factors become tokens. This is notation, not an answer lookup.
# Formats below explicitly name each complete original evaluation row component.
TOKEN_REPLACEMENTS={
'q-65204':[(r'\frac{\pi }{2}','{y0}'),('(0)','({x0})'),('0\\cdot','{x0}\\cdot'),('-0\\operatorname','-{x0}\\operatorname')],
'q-130198':[(r'\frac{\pi }{2}','{x0}'),('⁡0','⁡{y0}'),('+0\\operatorname','+{y0}\\operatorname')],
'q-130200':[('0+1','@@square@@+1'),('(1)','({x0})'),('(0)','({y0})')],
'q-37516':[(r'\frac{2(1)}{e}',r'\frac{2({x0})}{{y0}}'),('(1)','({x0})'),('⁡e','⁡{y0}'),('(e)','({y0})')],
'q-72400':[('(2)','({y0})'),('(-1)','({x0})')],
'q-72463':[],
'q-130201':[],
'q-72388':[('(1)','({x0})'),('(2)','({y0})')],
'q-130192':[('{2}^{2}','{{x0}}^{2}'),('(2)','({x0})'),('(1)','({y0})')],
'q-130194':[(r'\frac{(-1)}{1}',r'\frac{({x0})}{{y0}}'),('⁡1','⁡{y0}'),('(-1)','({x0})')],
}
def escape_format(t):return t
templates={};cases=[]
for qid,q in g.QUESTIONS.items():
 F=g.expr(qid);a,b=map(g.sym,g.SOURCE_SPEC[qid][1:]);params={'x0':str(a),'y0':str(b)}
 point=re.findall(r'\$\((.*?)\)\.?\$',q[':question/problem'])[-1]
 # Capture exact tuple punctuation in source, including space after comma.
 pt='('+point+')';point_template=pt.replace(g.tex(a),'@@x0@@',1)
 # Explicit original spellings differ only by pi spacing (source component names).
 if qid in ('q-65204','q-130198'):point_template='({x0},{y0})'
 else:point_template='({x0}, {y0})' if ', ' in pt else '({x0},{y0})'
 prompt=q[':question/problem'].replace(pt,'@@point@@')
 sol=q.get(':question/worked-solution','').replace(pt,'@@point@@')
 # Every full evaluation row and final vector is masked separately, preserving
 # source row count, sentence sequence and omission of redundant reduction rows.
 vectors={};ev=''
 if sol:
  block=list(re.finditer(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S))[-1]
  body=block[1];rows=body.split(r'\\');evaluation=next(r.split('& =',1)[1] for r in rows if 't@@point@@' in r)
  final=rows[-1].split('& =',1)[1].strip()
  vectors['final']=final
  conclusion=re.search(r'Therefore, our tangent vector is \$(.*?)\.\$',q[':question/worked-solution'])
  assert conclusion,qid
  vectors['conclusion']=conclusion[1]
  sol=sol.replace(evaluation,'@@evaluation@@',1)
  sol=sol.replace(final,'@@final@@')
  # Aligned final rows and prose conclusions can differ in spacing/\, notation.
  # Mask the entire conclusion independently, rather than relying on substring
  # replacement of the aligned-row spelling.
  sol=re.sub(r'(Therefore, our tangent vector is \$).*?(\.\$)',lambda m:m[1]+'@@conclusion@@'+m[2],sol)
  # Exact original evaluation mask plus generalized expressions is recorded.
  ev=escape_format(evaluation)
  # Replace unambiguous complete factors after protecting original TeX braces.
  for before,after in TOKEN_REPLACEMENTS[qid]:ev=ev.replace(escape_format(before),after)
  if qid=='q-72463':
   ev=escape_format(evaluation)
   parts=['4(1)(1)^{3}','4(1)','6(1)^{2}(1)^{2}','4(1)']
   replacements=['4({y0})({x0})^{3}','4({x0})','6({x0})^{2}({y0})^{2}','4({y0})']
   for old,new in zip(parts,replacements):ev=ev.replace(escape_format(old),new,1)
  if qid=='q-130201':ev=escape_format(evaluation).replace('-1+3(-1)^{2}','{x0}+3({y0})^{2}').replace('-1+2(-1)','{y0}+2({x0})')
 banks=[]
 for fi,f in enumerate(q[':question/answer-fields']):
  bank=[]
  for ai,ans in enumerate(f[':answer-field/choices']):
   value=ans[':answer/value'];A,B=g.pair(value);fx,fy=[g.s.simplify(z.subs({g.x:a,g.y:b})) for z in (g.s.diff(F,g.x),g.s.diff(F,g.y))]
   if g.dot((fx,fy),(A,B))==0:
    token='answer_'+str(fi)+'_'+str(ai);vectors[token]=value;bank.append('@@'+token+'@@')
   else:bank.append(value)
  banks.append(bank)

 # Curve constants are slots in the prompt, first rearrangement and level prose.
 # The known q130201 mismatch is preserved by +2 in raw evidence.
 constants={
 'q-36391': [('4',F)],
 'q-65204': [],
 'q-130198': [(r'\frac{\pi }{2}',F)],
 'q-130200': [('e',F)],
 'q-37516': [('2-8e',F)],
 'q-72400': [('9',F)],
 'q-72463': [('1',F)],
 'q-130201': [('3',F+2)],
 'q-72388': [('1',F)],
 'q-130192': [('3',F)],
 'q-130194': [('-1',F)]}
 # Explicit complete constant sites avoid derivative exponents and point literals.
 consts={}
 for ci,(old,ex) in enumerate(constants[qid]):
  key='constant_'+str(ci);consts[key]={'original':old,'expression':str(ex)}
  # Prompt equation only; constants in assessed point coordinates are excluded.
  curve=re.findall(r'\$(.*?)\$',prompt)[0]
  left,right=curve.split('=',1)
  token='@@'+key+'@@'
  if qid=='q-72388':left=left.replace(old,token)
  else:right=right.replace(old,token,1)
  newcurve=left+'='+right
  prompt=prompt.replace(curve,newcurve,1)
  # Only the first rearrangement block and level-curve sentences, never operators.
  if sol:
   first=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)
   if first and 't(x,y)' not in first[1]:
    content=first[1]
    if qid=='q-72388':content=content.replace('x+1 &','x+@@'+key+'@@ &').replace('-x-1 &','-x-@@'+key+'@@ &')
    # Replace constants on equation right sides, preserving coefficients/indices.
    rows=content.split(r'\\')
    for ri,row in enumerate(rows):
     lhs,rhs=row.split('& =',1);rhs=rhs.replace(old,'@@'+key+'@@',1);rows[ri]=lhs+'& ='+rhs
    content=r'\\'.join(rows)
    sol=sol[:first.start(1)]+content+sol[first.end(1):]
   sol=sol.replace('f(x,y)='+old+'.$','f(x,y)=@@'+key+'@@.$')
 # q72400/q72388 put the level constant inside F, including operator inputs.
 if qid=='q-72400':sol=sol.replace('-9','-@@constant_0@@')
 if qid=='q-72388':sol=sol.replace('{x}^{2}y-x-1','{x}^{2}y-x-@@constant_0@@')
 # Trig product has zero source constant; genuine point variations add the new
 # level to its RHS. Its baseline zero spelling stays empty.
 if qid=='q-65204':
  key='rhs';original=r'\operatorname{sin}⁡(xy)'
  # This component contains symbolic variables; renderer uses F(point) as level.
  consts['triglevel']={'original':'0','expression':str(F)}
  prompt=prompt.replace(original+'.',original+'@@trigoffset@@.')
 templates[qid]={'coordinate_spellings':[v.strip() for v in point.split(',')],'constant_components':consts,'parameters':params,'point_template':point_template,'prompt':prompt,'solution':sol,'evaluation_template':ev,'spelling':{},'vector_spellings':vectors,'banks':banks,'raw_attribute_keys':list(q),'bank_interpretation':'Correct components from evaluated derivatives. All other full observed components remain opaque fixed expressions, evidence only.'}
 cases.append({'source_id':qid,'template':qid,'parameters':params,'bank_profile':'raw:'+qid,'level':('moderate' if ':question/difficulty' in q else 'unrated')})
(P/'source-templates.json').write_text(json.dumps(templates,indent=2,ensure_ascii=False)+'\n');(P/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
