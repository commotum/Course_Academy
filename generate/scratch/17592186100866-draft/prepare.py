import sys
sys.dont_write_bytecode=True
import json,importlib.util,shutil
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('draft',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def dump(name,obj): (D/name).write_text(json.dumps(obj,indent=2)+'\n')
cap=g.CAP
inventory=[{'record':q,'role':'independently authored inventory','relationship_to_source_templates':'Current independent integer multiplication practice; compare the five source-shaped matrix/column layouts.'} for q in cap['record'][':knowledge-point/questions'] if ':question/math-academy-id' not in q]
dump('independent-inventory.json',{'basis':cap['basis'],'lineage':cap['lineage'],'questions':inventory})
shutil.copyfile(ROOT/'generate/scratch/17592186100866/reference/source.json',D/'reference/supplemental-source-basis2655.json')
sup=json.loads((D/'reference/supplemental-source-basis2655.json').read_text());dump('supplemental-analysis.json',{'basis':sup['basis'],'lineage':sup['lineage'],'question_count':len(sup['record'][':knowledge-point/questions']),'families':[{'source_id':q.get(':question/math-academy-id',q[':question/id']),'template':g.template_of(q[':question/math-academy-id']) if q.get(':question/math-academy-id') in g.SOURCES else 'independent-current-integer','parameters':g.parameters_of(q),'relationship':'All current supported integer layouts are carried into the draft; supplemental source never replaces the assigned frozen2275 wrapper.'} for q in sup['record'][':knowledge-point/questions']]})
for n in ('principles.md','docs/3-classify.md','docs/4-template-extraction.md','docs/5-plot-extraction.md','docs/6-template-generator.md','docs/7-plot-generator.md','runs/current/worker-instructions.md'):
 shutil.copyfile(ROOT/'generate'/n,D/'reference'/Path(n).name)
for typ in ('topics','lessons'):
 p=ROOT/'generate/runs/current/refresh-2026-10-14'/typ/'17592186048954.json';shutil.copyfile(p,D/'reference'/('dot-product-'+typ+'.json'))
cases=[];bankmap=[]
def clean(v):
 # Compatibility guard for a doubled capture layer; assigned2275 banks have one actual command slash, so this is a no-op.
 return v.replace('\\\\','\\') if v.startswith('\\\\begin') else v
for mid,q in g.SOURCES.items():
 p=g.parameters_of(q)
 if mid=='q-126512':p['opaque_slots']=[['1','-2']]
 if mid=='q-13566':p['opaque_slots']=[['19','12']]
 case={'source_id':mid,'template':g.template_of(mid),'parameters':p,'bank_profile':'observed:'+mid,'level':'easy','observed_difficulty':q.get(':question/difficulty'),'field_attribute_presence':[{k:k in f for k in (':answer-field/correct',)} for f in q[':question/answer-fields']]};cases.append(case)
 values=g.bank(case['bank_profile'],p); recipes=g.RECIPES.get(mid,[])
 rows=[]
 for fi,f in enumerate(q[':question/answer-fields']):
  for a in f[':answer-field/choices']:
   v=clean(a[':answer/value']);mat=g.matrices(v)
   if mat:
    pair=tuple(g.s.Rational(row[0].strip()) for row in mat[0]);ix=values.index(pair);recipe=recipes[ix]
   else:recipe=('r' if f[':answer-field/key']=='field-1' else 't',)
   rows.append({'field_index':fi,'field_key':f[':answer-field/key'],'answer_id':a[':answer/id'],'raw_value':a[':answer/value'],'normalized_value':v,'recipe':recipe,'source_correct_present':':answer-field/correct' in f,'is_designated_correct':a[':answer/id']==f.get(':answer-field/correct',{}).get(':answer/id'),'interpretation':'Opaque observed vector slot; no pedagogical error inference' if any(str(x).startswith('z') for x in recipe) else 'Observed expression pattern only; no learner-facing diagnosis'})
 bankmap.append({'source_id':mid,'profile':case['bank_profile'],'mapping':rows})
dump('source-cases.json',cases);dump('bank-map.json',bankmap)
review=[]
for case in cases:
 record=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);review.append({'label':'Original replay '+case['source_id'],'record':record})
 # Changed values for every profile, preserving entire bank (including evidence-only opaque slot).
 p=case['parameters']|{'a':str(int(case['parameters']['a'])+1)}
 for shift in range(1,20):
  p=case['parameters']|{'a':str(g.s.Rational(case['parameters']['a'])-shift if g.s.Rational(case['parameters']['a'])>0 else g.s.Rational(case['parameters']['a'])+shift)}
  try:r=g.generate('easy',template=case['template'],parameters=p,profile=case['bank_profile']);break
  except ValueError:continue
 else:raise AssertionError('No changed bank '+case['source_id'])
 review.append({'label':'Changed-parameter observed recipe '+case['source_id']+' (ineligible evidence)','record':r})
for level in g.LEVELS:
 for i,t in enumerate(g.TEMPLATES):
  for seed in (50+i,90+i):review.append({'label':'Authored '+level+' '+t,'record':g.generate(level,seed,template=t)})
for level in g.LEVELS:
 for template,profiles in g.ELIGIBLE_PROFILES.items():
  for profile in profiles:
   if profile.startswith('source-method:'):
    for seed in (137,243):review.append({'label':'Normal '+level+' '+template+' '+profile,'record':g.generate(level,seed,template=template,profile=profile)})
dump('review.json',review)
text=[]
for item in review:
 q=item['record']['question'];text+=['## '+item['label'],q[':question/problem']]
 for f in q[':question/answer-fields']:
  text+=['Field '+f[':answer-field/key']+' '+f[':answer-field/type']]
  for a in f[':answer-field/choices']:text+=['- $'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==f.get(':answer-field/correct',[None,None])[1] else '')]
 text+=[q.get(':question/worked-solution','Source omits the worked solution.'),'']
(D/'review.md').write_text('\n\n'.join(text))
print('Prepared',len(cases),'original cases;',len(review),'review records')
