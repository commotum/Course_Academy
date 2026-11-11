import json,copy
from pathlib import Path
H=Path(__file__).resolve().parent;P=H/'package'
code=(P/'generator.py').read_text().replace("VERSION = '3.0.1'","VERSION = '3.0.2'")
code=code.replace("    if level=='easy':\n        prompt+=\" The normal slope is the negative reciprocal of the tangent slope.\"\n",'')
code=code.replace("prompt+='\\n\\nComplete the equation, using signed exact values.\\n\\n$x+($ {{coefficient}} $)\\\\cdot y=$ {{constant}}'","prompt+='\\n\\nGive exact values of $a$ and $b$ in $x+ay=b$.\\n\\n$a=$ {{coefficient}}\\n\\n$b=$ {{constant}}'")
assert 'normal slope is the negative reciprocal' not in code
assert '$x+ay=b$' in code
(P/'generator.py').write_text(code)
qs=json.loads((H/'siblings.json').read_text());ledger=[];proposed=[]
for q in qs:
 old=q[':question/problem'];new=old;reason=[]
 if not q.get(':question/math-academy-id'):
  for phrase in [" You are given $f'(x)=2x$."," The normal slope is the negative reciprocal of the tangent slope."]:
   if phrase in new:new=new.replace(phrase,'');reason.append('Remove supplied prerequisite/target work: '+phrase.strip())
  if q[':db/id']==17592186710391:
   new=new.split('\n\nComplete the equation.')[0]+'\n\nGive exact values of $a$ and $b$ in $y=ax+b$.\n\n$a=$ {{slope}}\n\n$b=$ {{intercept}}';reason.append('Label slope/intercept blanks clearly')
  if '{{coefficient}}' in new:
   new=new.split('\n\nComplete the equation')[0]+'\n\nGive exact values of $a$ and $b$ in $x+ay=b$.\n\n$a=$ {{coefficient}}\n\n$b=$ {{constant}}';reason.append('Label existing coefficient and constant without changing endpoint')
 p=copy.deepcopy(q);p[':question/problem']=new;proposed.append(p)
 ledger.append(dict(entity=q[':db/id'],imported=bool(q.get(':question/math-academy-id')),changed=new!=old,reasons=reason,before=old,after=new))
(H/'case-ledger.json').write_text(json.dumps(ledger,indent=2)+'\n');(H/'proposed-siblings.json').write_text(json.dumps(proposed,indent=2)+'\n')
manifest=dict(entrypoint='generator.py',files=['generator.py','math_format.py','requirements.txt','source_replay.json','check_refill.py','refill-validation.json','refill-review-plan.json'],dependencies=dict(python='3.13.5',packages=dict(sympy='1.14.0')))
(P/'package.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Changed prompts:',[r['entity'] for r in ledger if r['changed']])
