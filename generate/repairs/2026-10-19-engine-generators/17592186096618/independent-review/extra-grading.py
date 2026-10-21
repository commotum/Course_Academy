from audit import *
cases=json.loads((E/'grader-observed-input.json').read_text())
for i,r in enumerate(json.loads((E/'replays.json').read_text())):
 f=r['question'][':question/answer-fields'][0]
 if f[':answer-field/type'].endswith('radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete source bank selection'} for a in f[':answer-field/choices']]
 else:
  checks=[{'submitted':a[':answer/value'],'expected':'accepted','purpose':'valid captured source alias'} for a in f[':answer-field/choices']]
  checks.append({'submitted':r'\frac{2\left('+key(r)+r'\right)}{2}','expected':'accepted','purpose':'unsimplified canceling-scalar equivalent'})
  product=re.search(r'\$f\(x\)\s*=\s*(.*?)\$',r['question'][':question/problem'])[1].rstrip(' ,');checks.append({'submitted':s.latex(s.diff(parse(product),X),ln_notation=True),'expected':'rejected','purpose':'full derivative in missing-fragment blank'})
 cases.append({'label':'source replay '+str(i),'record':r,'checks':checks})
save('grader-complete-input.json',cases)
