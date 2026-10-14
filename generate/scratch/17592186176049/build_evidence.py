from pathlib import Path
import importlib.util,json,re
ROOT=Path(__file__).parent
s=importlib.util.spec_from_file_location('g',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
cases=[]
for name,(qid,_) in g.OBSERVED.items():
 q=g.QUESTIONS[qid];cases.append({'source_id':q[':question/id'],'math_academy_id':qid,'template':name,'level':'hard','parameters':g.ANCHORS[name],'bank_profile':'observed:'+name,'authored_level_assignment':qid=='q-27660'})
(ROOT/'source-cases.json').write_text(json.dumps(cases,indent=2,ensure_ascii=False)+'\n')
records=[];review=['# Tangent properties review\n\nAll generated records are local draft review data. Original basis: 1356.\n']
for c in cases:
 q=g.QUESTIONS[c['math_academy_id']];review+=['## Original '+c['math_academy_id'],q[':question/problem'],'\nBank: '+', '.join(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']), '\nCorrect: '+q[':question/answer-fields'][0].get(':answer-field/correct',{}).get(':answer/value','[missing; inferred I only only in completed output]'),re.sub(r'!\[\]\((images/[^)]+)\)',lambda m:'![](/media/jake/SSD/EDB/math/'+m[1]+')',q.get(':question/worked-solution','[Source worked solution absent.]'))]
 for seed in [20,21]:
  r=g.generate('hard',seed,template=c['template']);records.append(r);review+=['### Generated variant '+str(seed)+' (completed source family)',g.markdown(r)]
for level in ['easy','moderate','hard']:
 for seed in [20,21]:
  r=g.generate(level,seed,template='two_identity_properties' if level=='hard' else None);records.append(r);review+=['## Authored '+level+' variant '+str(seed),g.markdown(r)]
(ROOT/'review.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n');(ROOT/'review.md').write_text('\n\n'.join(review)+'\n')
rows=[]
for c in cases:
 q=g.QUESTIONS[c['math_academy_id']];rows.append({'source_id':c['math_academy_id'],'template':c['template'],'prompt':q[':question/problem'],'solution':q.get(':question/worked-solution'),'slots':c['parameters'],'bank':[{'value':a[':answer/value'],'recipe':'Select the listed subset of statements I, II, III; omission/inclusion of truth claims','correct_observed':a[':answer/id']==q[':question/answer-fields'][0].get(':answer-field/correct',{}).get(':answer/id')} for a in q[':question/answer-fields'][0][':answer-field/choices']]})
(ROOT/'template-specs.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
