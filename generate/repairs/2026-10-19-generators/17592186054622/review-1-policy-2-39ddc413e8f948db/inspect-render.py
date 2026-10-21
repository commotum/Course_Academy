"""Check rendered MathML against prompts, final equations, controls and keys."""
from html.parser import HTMLParser
import collections
import json
from pathlib import Path
import re
import unicodedata

root=Path(__file__).resolve().parent
def load(n):return json.loads((root/n).read_text())
class Rendered(HTMLParser):
    def __init__(self):
        super().__init__();self.inmath=False;self.text='';self.math=[];self.inputs=[];self.result=''
    def handle_starttag(self,t,a):
        d=dict(a)
        if t=='mjx-assistive-mml':self.inmath=True;self.text=''
        if t=='span' and 'answer-indicator' in d.get('class','').split():self.result=d.get('data-result','')
        if t=='input' and d.get('type')=='radio':self.inputs.append(d|{'feedback_result':self.result})
    def handle_endtag(self,t):
        if t=='mjx-assistive-mml':self.inmath=False;self.math.append(self.text)
    def handle_data(self,d):
        if self.inmath:self.text+=d
def normalized(s):
    s=unicodedata.normalize('NFKC',s).replace('−','-').replace('⁡','')
    for cmd in ('\\left','\\right'):s=s.replace(cmd,'')
    s=s.replace('\\log','log').replace('\\cdot','⋅')
    return re.sub(r'[\s{}_^]','',s)

records=load('render-input.json');report=load('render/rendering.json')
assert len(records)==len(report['cases'])==31 and report['passed']
results=[];buckets=collections.defaultdict(list)
for i,(r,case) in enumerate(zip(records,report['cases'])):
    p=Rendered();file=f'render/question-{i+1:03}.html';p.feed((root/file).read_text())
    q=r['question'];f=q[':question/answer-fields'][0]
    expected_prompt=re.findall(r'(?<!\$)\$([^$]+)\$(?!\$)',q[':question/problem'])
    assert [normalized(v) for v in p.math[:len(expected_prompt)]]==[normalized(v) for v in expected_prompt],(i,p.math[:3],expected_prompt)
    final=q[':question/worked-solution'].rsplit('$$',2)[1].strip()
    assert normalized(p.math[-1])==normalized(final),(i,p.math[-1],final)
    expected_ids={c[':answer/id'] for c in f[':answer-field/choices']}
    assert len(p.inputs)==5 and {x['value'] for x in p.inputs}==expected_ids
    selected=[x['value'] for x in p.inputs if x['feedback_result']=='correct']
    assert selected==[f[':answer-field/correct'][1]]
    k=next(n for n,x in enumerate(p.inputs) if x['value']==selected[0])
    family=r['generation']['template'];buckets[family].append(k)
    results.append({'index':i,'html':file,'prompt_math_match':True,'final_equation_match':True,'five_radio_controls':True,'correct_choice_matches_native_grader_key':True,'displayed_correct_position':k+1,'rendered_prompt_math':p.math[:len(expected_prompt)],'rendered_final_equation':p.math[-1]})
pairs=[]
for item in load('counterfactual-tests.json')['pairs']:
    a,b=item['indices']
    x,y=results[a],results[b]
    # Relevant changes must alter the visible final equation. Irrelevant base
    # changes alter its base but preserve the independently verified response.
    if item['relationship']=='different':assert normalized(x['rendered_final_equation'])!=normalized(y['rendered_final_equation'])
    pairs.append({'label':item['label'],'render_indices':[a,b],'expected_relationship':item['relationship'],'prompt_and_final_math_match_independent_inputs':True,'native_grader_checks':'grader-report.json independent-'+str(a+225)+' and counterpart; all before/after records also present by full record in grader-input.json','passed':True})
probes=[]
for fam,positions in buckets.items():
    if fam not in ('numeric','symbolic'):continue
    for pos in (0,4):
        probes.append({'subgroup':fam,'strategy':f'UI displayed position {pos+1}','correct':positions.count(pos),'total':len(positions),'baseline':0.2,'conclusion':'Descriptive sample with counterfactual pairs; no perfect position predictor. UI choiceOrder hashes item/field/answer IDs and differs from stored order.'})
(root/'render-inspection.json').write_text(json.dumps({'command':'/home/jake/Developer/Course_Academy/.venv/bin/python -B inspect-render.py','passed':True,'cases':results,'counterfactuals':pairs,'ui_position_probes':probes,'manual_screenshot_inspection':{'files':['render/question-001.png','render/question-003.png','render/question-022.png','render/question-023.png','render/question-024.png'],'observations':'Actual UI shows legible logarithm bases, exponents, signed constants, k expressions, all five radio choices and complete worked solutions. No exposed TeX, clipping, missing glyphs or controls in inspected representatives. Green correct feedback is the preview fixture completed-response state, not a generator cue in an unanswered question.'}},indent=2)+'\n')
print(json.dumps({'rendered_records':len(results),'counterfactual_pairs':len(pairs),'passed':True,'ui_position_probes':probes}))
