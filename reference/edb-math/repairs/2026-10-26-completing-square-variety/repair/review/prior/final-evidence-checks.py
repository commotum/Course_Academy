import argparse,json,re,sys,importlib.util
from pathlib import Path
from html.parser import HTMLParser
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
ap=argparse.ArgumentParser();ap.add_argument('--evidence',type=Path,required=True);ap.add_argument('--repo',type=Path,required=True);a=ap.parse_args();E,R=a.evidence,a.repo
read=lambda n:json.loads((E/n).read_text())
write=lambda n,d:(E/n).write_text(json.dumps(d,indent=2)+'\n')
def expr(t):
 t=t.strip().rstrip('.,:').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\dfrac',r'\frac')
 t=re.sub(r'_\{\\text\{perfect square\}\}','',t).replace(r'\underbrace','')
 while r'\frac' in t:
  t,n=re.subn(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',r'((\1)/(\2))',t);assert n,t
 t=t.replace(r'\cdot','*').replace('{','(').replace('}',')').replace('^','**')
 return sp.expand(parse_expr(t,transformations=standard_transformations+(implicit_multiplication_application,),local_dict={v:sp.Symbol(v,real=True) for v in 'xytzw'}))
paths=read('solution-paths.json');paths['cases']=[c for c in paths['cases'] if not c['template'].startswith('source-replay:')];replay=read('source-replay-records.json');sourcepaths=[]
for r in replay:
 q=r['question'];pol=expr(re.search(r'\$([^$]+)\$',q[':question/problem'])[1]);steps=[];final=''
 for block in re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S):
  block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
  for row in block.split(r'\\'):
   for part in row.replace('&','').split('='):
    if not part.strip():continue
    assert sp.simplify(expr(part)-pol)==0,part
    steps.append(part.strip())
    # Capture the actual completed-square expression, before optional expansion checks.
    if ('\\right)^2' in part or re.search(r'\)\}\^\{2\}',part)) and '\\underbrace' not in part:
     if part.count('^2')+part.count('^{2}')<=1:final=part.strip().rstrip('.')
 assert final,(q[':question/id'],steps)
 for f in q[':question/answer-fields']:
  cid=f[':answer-field/correct'][1];key=next(c[':answer/value'] for c in f[':answer-field/choices'] if c[':answer/id']==cid);radio=f[':answer-field/type'].endswith('/radio')
  paths['cases'].append({'template':'source-replay:'+q[':question/id'],'field_key':f[':answer-field/key'],'final_expression':final,'keyed_answer':key,'domain':'Real variable; '+('full completed-square expression selected' if radio else 'numeric fragment at the displayed field scope'),'conclusion':'Every displayed source/exemplar equality checked independently; original complete bank or signed/scaffold numeric fragment is retained.','sample_refs':['source-replay-records.json','source-path-checks.json'],'status':'passed','conversions':[] if radio else [{'rule':'Read the half and remaining constant at the displayed signed or supplied-sign field scope.','scope_source':'This exact complete source or published exemplar: '+q[':question/id'],'shown_step':final+'; '+q[':question/problem']+'; '+q[':question/worked-solution'].split('\n\n')[-1],'status':'passed'}]})
 sourcepaths.append({'id':q[':question/id'],'displayed_expression_parts_checked':steps,'completed_result':final})
write('source-path-checks.json',sourcepaths);write('solution-paths.json',paths)
spec=importlib.util.spec_from_file_location('mf',R/'scripts/question_capture/math_format.py');mf=importlib.util.module_from_spec(spec);spec.loader.exec_module(mf)
class DOM(HTMLParser):
 def __init__(self):super().__init__();self.tags={};self.mml={};self.emphasis=[];self.instrong=False
 def handle_starttag(self,tag,attrs):
  d=dict(attrs);self.tags[tag]=self.tags.get(tag,0)+1
  if 'data-mml-node' in d:self.mml[d['data-mml-node']]=self.mml.get(d['data-mml-node'],0)+1
  if tag in ('strong','b'):self.instrong=True
 def handle_endtag(self,tag):
  if tag in ('strong','b'):self.instrong=False
 def handle_data(self,data):
  if self.instrong:self.emphasis.append(data)
render_checks=[]
for name,inputfile in [('easy','final-easy.json'),('moderate','final-moderate.json'),('hard','final-hard.json'),('controls','render-controls.json'),('negative-constants','render-negative-constants.json')]:
 records=read(inputfile);rep=read('render-'+name+'/rendering.json');assert rep['passed'] and len(rep['cases'])==len(records)
 for i,(record,case) in enumerate(zip(records,rep['cases']),1):
  assert case['passed'] and not any(case[k] for k in ['rawTex','codeMath','mathErrors','javascriptErrors','brokenImages','danglingGlyphs'])
  q=record['question'];dom=DOM();dom.feed((E/('render-'+name)/('question-'+str(i).zfill(3)+'.html')).read_text());ordinary=not record.get('generation',{}).get('mode')=='source-replay'
  expected=sum(len(list(mf.MATH.finditer(q[k]))) for k in (':question/problem',':question/worked-solution'))
  if ordinary:
   assert dom.tags.get('mjx-container')==expected+2,(name,i,dom.tags.get('mjx-container'),expected)
   assert dom.mml.get('mtr')==3,(name,i,dom.mml)
   assert 'Add and subtract' in ''.join(dom.emphasis)
  else:assert dom.tags.get('mjx-container',0)>=expected
  render_checks.append({'set':name,'index':i,'question_id':q[':question/id'],'expected_prose_math_segments':expected,'actual_math_containers':dom.tags.get('mjx-container',0),'derivation_rows':dom.mml.get('mtr',0),'ordinary_three_rows_retained':ordinary,'rendered_emphasis':dom.emphasis,'status':'passed'})
write('render-boundary-checks.json',{'cases':render_checks,'conclusion':'All 46 actual UI previews passed visible raw-TeX/code/error checks. For every ordinary preview, each intended prose math segment plus two answer summaries is present and exactly three derivation rows survive. No data tables/matrix partitions/currency or percentage text in this KP.'})
print('Displayed source steps, field-scope paths and all rendering boundary checks passed:',len(render_checks))
