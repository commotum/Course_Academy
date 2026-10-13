"""One-time extraction of complete-component source masks, retaining raw record."""
import json,re
from pathlib import Path
H=Path(__file__).parent
src=json.loads((H/'source.json').read_text())
keys=['power_easy','exp_true','sin_none','cos_i','log_all','inverse_none','exp_none','log_scaled','power_moderate']
recipes=[
 {'F':r'{x}^{4}','D':r'4{x}^{3}','C':r'5{x}^{5}','R':r'\frac{4y}{x}','S':r'\frac{4({x}^{4})}{x}'},
 {'F':r'{e}^{2x}','D':r'2{e}^{2x}','R':r'2y'},
 {'F':r'\frac{1}{2}\operatorname{sin}⁡2x','D':r'\operatorname{cos}⁡2x','C':r'2\operatorname{cos}⁡2x','R':r'2y','S':r'2(\frac{1}{2}\operatorname{sin}⁡2x)','E':r'\operatorname{sin}⁡2x','P':r'\frac{1}{2}\cdot 2\operatorname{cos}⁡2x'},
 {'F':r'\operatorname{cos}⁡2x','D':r'-2\operatorname{sin}⁡2x','R':r'y\operatorname{cos}⁡2x','S':r'\operatorname{cos}⁡2x\cdot \operatorname{cos}⁡2x','E':r'{cos}^{2}⁡2x'},
 {'F':r'\operatorname{ln}⁡x','D':r'\frac{1}{x}','R':r'\frac{1}{{e}^{y}}','S':r'\frac{1}{{e}^{\operatorname{ln}⁡x}}'},
 {'F':r'-\frac{1}{{x}^{2}}','D':r'\frac{2}{{x}^{3}}','C':r'-\frac{2}{{x}^{3}}','R':r'\frac{y}{{x}^{2}}','S':r'\frac{(-\frac{1}{{x}^{2}})}{{x}^{2}}','E':r'-\frac{1}{{x}^{4}}'},
 {'F':r'3{e}^{-x}','D':r'-3{e}^{-x}','R':r'-3y','S':r'-3(3{e}^{-x})','E':r'-9{e}^{-x}'},
 {'F':r'4\operatorname{ln}⁡x','D':r'\frac{4}{x}','C':r'\frac{1}{4x}','R':r'\frac{4x}{{e}^{y/2}}','S':r'\frac{4x}{{e}^{(4\operatorname{ln}⁡x)/2}}','H':r'\frac{4x}{{e}^{2\operatorname{ln}⁡x}}','J':r'\frac{4x}{{e}^{\operatorname{ln}⁡{x}^{2}}}','K':r'\frac{4x}{{x}^{2}}'},
 {'F':r'-3{x}^{2}','D':r'-6x','C':r'-5x','R':r'\frac{2y}{x}','S':r'\frac{2(-3{x}^{2})}{x}','P':r'-3\cdot 2x'}
]
masks={}; cases=[]
params=[{'n':4},{'k':2},{'k':2},{'k':2},{'h':0},{'n':2},{'a':3,'k':1,'b':3},{'m':2},{'a':-3,'n':2}]
for t,q,r,p in zip(keys,src['record'][':knowledge-point/questions'],recipes,params):
 inverse={v:k for k,v in r.items()}; pat=re.compile('|'.join(re.escape(v) for v in sorted(inverse,key=len,reverse=True)))
 def mask(v):return pat.sub(lambda m:'@@'+inverse[m.group()]+'@@',v)
 field=q[':question/answer-fields'][0];profile=q[':question/math-academy-id']+'_bank'
 masks[t]={'prompt':mask(q[':question/problem']),'solution':mask(q[':question/worked-solution']),'bank':[a[':answer/value'] for a in field[':answer-field/choices']],'source_id':q[':question/math-academy-id'],'profile':profile,'components_at_source':r}
 cases.append({'source_id':q[':question/math-academy-id'],'template':t,'parameters':p,'bank_profile':'raw_'+profile,'raw_evidence_profile':True,'evidence_only':True,'eligible_for_learning':False,'level':q[':question/difficulty'][':db/ident'].split('/')[-1]})
(H/'masks.json').write_text(json.dumps(masks,ensure_ascii=False,indent=2)+'\n')
(H/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
