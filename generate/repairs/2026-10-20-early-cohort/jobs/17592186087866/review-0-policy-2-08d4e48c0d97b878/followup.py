import audit as a
from collections import Counter
E=a.E;g=a.g
pairs=[];records=[]
for t,p1,p2 in [('q-16400',{'a':2,'b':3,'c':1,'h':4},{'a':2,'b':3,'c':2,'h':4}),('q-8359',{'k':1},{'k':2}),('q-103349',{'n':1},{'n':2})]:
 before=g.generate('easy',9401,t,parameters=p1);after=g.generate('easy',9401,t,parameters=p2);irr=g.generate('easy',9402,t,parameters=p1)
 records.extend([before,after,irr]);pairs.append({'template':t,'record_indices':[len(records)-3,len(records)-2,len(records)-1],'parameters_before':p1,'parameters_after':p2})
a.save('counterfactual-records.json',records);a.save('counterfactual-pairs.json',pairs)
allr=a.json.loads((E/'independent-records.json').read_text());render=[]
for t in g.FAMILIES['easy']+g.FAMILIES['moderate']+g.FAMILIES['hard']:render.append(next(r for r in allr if r['generation']['template']==t))
render.extend(records)
# Include one raw profile with captured underbrace glyph representation.
render.append(a.json.loads((E/'source-replays.json').read_text())[1]);a.save('render-records.json',render)
cases=[]
for i,r in enumerate(render+a.json.loads((a.JOB/'samples.json').read_text())):
 f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
 cases.append({'label':str(i)+':'+r['generation']['template'],'record':r,'checks':[{'field_index':0,'submitted_answer_id':v[':answer/id'],'expected':'accepted' if v[':answer/id']==correct else 'rejected','purpose':'radio correctness independently checked from displayed mathematics'} for v in f[':answer-field/choices']]})
a.save('grader-input.json',cases)
# Correct presentation-sensitive replay comparison, preserving original diff results.
source=a.json.loads((a.JOB/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions'];replays=a.json.loads((E/'source-replays.json').read_text());out=[]
def presentation(t):
 t=t.replace(r'\left','').replace(r'\right','')
 while r'\underbrace' in t:
  i=t.index(r'\underbrace');v,j=a.group(t,i+len(r'\underbrace'));t=t[:i]+'{{'+v+'}_{⏟}}'+t[j:]
 return t
for q,r in zip(source,replays):
 z=r['question'];prompt=presentation(q[':question/problem'])==z[':question/problem'];solution=presentation(q[':question/worked-solution'])==z[':question/worked-solution'];fields=[]
 for sf,gf in zip(q[':question/answer-fields'],z[':question/answer-fields']):
  bank=Counter(presentation(v[':answer/value']) for v in sf[':answer-field/choices'])==Counter(v[':answer/value'] for v in gf[':answer-field/choices'])
  sk=sf.get(':answer-field/correct');gk=gf.get(':answer-field/correct');key=(sk is None and gk is None) or (sk is not None and gk is not None and presentation(sk[':answer/value'])==next(v[':answer/value'] for v in gf[':answer-field/choices'] if v[':answer/id']==gk[1]))
  fields.append({'bank_equal':bank,'key_equal':bool(key),'type_equal':sf[':answer-field/type'][':db/ident']==gf[':answer-field/type'],'size':len(gf[':answer-field/choices'])})
 out.append({'source_id':q[':question/id'],'template':q[':question/math-academy-id'],'prompt_equal_after_presentation_normalization':prompt,'solution_equal_after_presentation_normalization':solution,'fields':fields,'passed':bool(prompt and solution and len(q[':question/answer-fields'])==len(z[':question/answer-fields']) and all(all(v[k] for k in ['bank_equal','key_equal','type_equal']) for v in fields))})
a.save('source-replay-normalized-results.json',{'normalizations':['Ignore automatic left/right sizing','Recognize captured {{content}_{⏟}}_{label} as underbrace annotation; render checked separately','UUIDs and choice ordering may change'],'results':out})
print('replays',sum(v['passed'] for v in out),'/',len(out),'render count',len(render),'grader cases',len(cases))
