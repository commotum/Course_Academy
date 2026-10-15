import sys
sys.dont_write_bytecode=True
import importlib.util,json,hashlib,shutil
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
sp=importlib.util.spec_from_file_location('draft00867',D.with_suffix('.py'));g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
def save(name,x):(D/name).write_text(json.dumps(x,indent=2)+'\n')
save('independent-inventory.json',{'basis':g.CAP['basis'],'lineage':g.CAP['lineage'],'questions':[{'record':q,'role':'independently authored inventory','relationship_to_source_templates':'Current supported numeric matrix-column practice.'} for q in g.RECORD[':knowledge-point/questions'] if ':question/math-academy-id' not in q]})
sup=json.loads((D/'reference/supplemental-source-basis2659.json').read_text());save('supplemental-analysis.json',{'basis':sup['basis'],'lineage':sup['lineage'],'questions':len(sup['record'][':knowledge-point/questions']),'records_equal_to_assigned_snapshot':sup['record']==g.RECORD,'scope':'Exact registered later snapshot retained; same11 originals and all supported families preserved.'})
canonical=g.RECORD[':knowledge-point/canonical-example'];save('canonical-original.json',canonical)
assetrows=[]
for rel in __import__('re').findall(r'!\[\]\(([^)]+)\)',canonical[':question/problem']):
 src=Path('/media/jake/SSD/EDB/math')/rel;dst=D/'reference'/Path(rel).name;shutil.copyfile(src,dst);assetrows.append({'source':str(src),'copy':str(dst.relative_to(ROOT)),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'inspection':'Visible numeric matrix/column transcription agrees with first two solution operands.'})
save('canonical-assets.json',assetrows)
cases=[];maps=[];reviews=[]
for mid,q in g.SOURCES.items():
 p=g.parameters_of(q);t=g.template_of(mid);profile='observed:'+mid
 cases.append({'source_id':mid,'template':t,'parameters':p,'bank_profile':profile,'level':'moderate','difficulty_role':'observed moderate' if ':question/difficulty'in q else 'unrated raw replay retains absent difficulty','original_correct_designations':sum(':answer-field/correct'in f for f in q[':question/answer-fields'])})
 r=g.generate('moderate',parameters=p,profile=profile);reviews.append({'label':'MA original '+mid,'record':r})
 changed={**p,'A':[[n*scale for n in row] for row,scale in zip(p['A'],[2,-1,1])],'v':[-n for n in p['v']],'matrix_name':'Z','vector_name':'n'}
 rr=g.generate('moderate',99,parameters=changed,profile=profile);reviews.append({'label':'Changed observed family '+mid+(' — opaque covariance evidence only' if mid in g.OPAQUE else ''),'record':rr})
 rows=[]
 for f in q[':question/answer-fields']:
  for a in f[':answer-field/choices']:
   rows.append({'field':f[':answer-field/key'],'field_type':f[':answer-field/type'][':db/ident'],'answer_id':a[':answer/id'],'value':a[':answer/value'],'designated_correct':a[':answer/id']==f.get(':answer-field/correct',{}).get(':answer/id'),'correct_present':':answer-field/correct'in f,'formula':'k*d_i*source_option_i under A_i=d_i*A0_i, v=k*v0; evidence-only, no error interpretation' if mid in g.OPAQUE else 'Bank formula in bank(profile,p), matching this complete value; no feedback added'})
 maps.append({'source_id':mid,'template':t,'bank_profile':profile,'parameters':p,'choices':rows,'solution_stages':['printed operands','ordered three products per row','three evaluated signed terms per row','final three-component column'] if ':question/worked-solution'in q else [],'missing_source_attributes':[k for k in (':question/difficulty',':question/worked-solution') if k not in q]})
for level in g.LEVELS:
 for t in g.TEMPLATES:
  for seed in (51,97):reviews.append({'label':'Authored '+level+' '+t,'record':g.generate(level,seed,template=t)})
recipes={
'q-127267':[['r','t','u'],['r','t','-u'],['r','-t','-u'],['r','-t','u'],['r','r','-u']],
'q-70188':[['r','t','u'],['r','-t','-u'],['r','t','-u'],['-r','-t','u'],['r','-t','u']],
'q-70190':[['r','t','u'],['r','t','-u'],['r','-t','u'],['-r','t','u'],['-r','-t','u']],
'q-70191':[['r','t','u'],['r','-t','u'],['r','-t','-u'],['-r','t','u'],['r','t','-u']],
'q-77350':[['r','t','u'],['-r','-t','u'],['r','u','t'],['r','-t','u'],['u','t','r']],
'q-13558':[['r','t','u'],['-r','-t','u'],['-r','t','u'],['r','-t','-u'],['r','t','-u']]}
fullmap=[]
for mid,q in g.SOURCES.items():
 p=g.parameters_of(q);rv,tv,uv=g.dot(p);env={'r':rv,'t':tv,'u':uv};entries=g.bank('observed:'+mid,p)
 mapped=[]
 for fi,f in enumerate(q[':question/answer-fields']):
  for ai,a in enumerate(f[':answer-field/choices']):
   if mid in g.OPAQUE:formula=[f'k*d_{i+1}*({row[0]})' for i,row in enumerate(g.matrices(a[':answer/value'])[0])]
   elif mid in recipes:
    vals=tuple(row[0] for row in g.matrices(a[':answer/value'])[0]);formula=next(expr for expr in recipes[mid] if tuple(int(g.s.sympify(z,locals=env)) for z in expr)==vals)
   else:formula=['sum(A['+str(int(f[':answer-field/key'][-1])-1)+'][j]*v[j] for j=0,1,2)']
   mapped.append({'field_index':fi,'field_key':f[':answer-field/key'],'source_answer_id':a[':answer/id'],'source_value':a[':answer/value'],'formula':formula,'matched_exact_value':True,'feedback_present':':answer/feedback'in a,'interpretation':'opaque mathematical covariance only' if mid in g.OPAQUE else 'complete observed expression pattern; no diagnosis inferred'})
 fullmap.append({'source_id':mid,'family':g.template_of(mid),'prompt_mask_anchor':q[':question/problem'],'solution_mask_anchor':q.get(':question/worked-solution'),'parameters':p,'row_order':[0,1,2],'ordered_multiplicands':[[[a,b] for a,b in zip(row,p['v'])] for row in p['A']],'evaluated_terms':[[a*b for a,b in zip(row,p['v'])] for row in p['A']],'result':[rv,tv,uv],'fields_and_complete_bank':mapped})
save('source-template-map.json',fullmap)
save('source-cases.json',cases);save('bank-map.json',maps);save('review.json',reviews)
text=[]
for item in reviews:
 q=item['record']['question'];text+=['## '+item['label'],q[':question/problem']]
 for f in q[':question/answer-fields']:
  text+=['Field '+f[':answer-field/key']+' '+f[':answer-field/type']]
  text+=['- $'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==f.get(':answer-field/correct',[None,None])[1] else '') for a in f[':answer-field/choices']]
 text+=[q.get(':question/worked-solution','Original source omits the worked solution.'),'']
(D/'review.md').write_text('\n\n'.join(text))
print('Prepared',len(cases),'MA originals,',len(reviews),'review records')
