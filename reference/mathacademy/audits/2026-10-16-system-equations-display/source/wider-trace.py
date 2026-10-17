from pathlib import Path
import json,hashlib,importlib.util,sys,collections
from bs4 import BeautifulSoup
ROOT=Path('/home/jake/Developer/Course_Academy')
OUT=ROOT/'reference/mathacademy/audits/2026-10-16-system-equations-display/source'
WIDE=OUT.parent/'wide-mth341'
findings=json.loads((WIDE/'findings.json').read_text())
fields=json.loads((WIDE/'fields.json').read_text())
kps=[17592186073752,17592186073753,17592186192654,17592186192655,17592186192656,17592186192657]
lookup=collections.defaultdict(list)
for kp in kps:
 for p in (ROOT/f'generate/scratch/{kp}/reference').rglob('generated.json'):
  d=json.loads(p.read_text())
  def walk(x):
   if isinstance(x,dict):
    if ':question/problem' in x:
     for attr in [':question/problem',':question/worked-solution']:
      if attr in x: lookup[(kp,attr,x[attr])].append({'generated_file':str(p.relative_to(ROOT)),'question_uuid':x.get(':question/id')})
    for v in x.values():walk(v)
   elif isinstance(x,list):
    for v in x:walk(v)
  walk(d)
topics=[]
for topic in [17592186048826,17592186050190]:
 rows=[r for r in findings if r['topic']==topic]
 matched=[]
 for r in rows:
  matches=[m for kp in r['knowledge_points'] for m in lookup[(kp,r['attribute'],r['value'])]]
  matched.append({'entity':r['entity'],'attribute':r['attribute'],'ma_id':r['ma_id'],'knowledge_points':r['knowledge_points'],'exact_generated_value_matches':matches})
 all_questions={r['entity']:r['ma_id'] for r in fields if r['topic']==topic and r['attribute']==':question/problem'}
 topics.append({'topic':topic,'title':rows[0]['topic_title'],'affected_fields':len(rows),'affected_questions':len({r['entity'] for r in rows}),
                'affected_questions_with_math_academy_id':len({r['entity'] for r in rows if r['ma_id'] is not None}),
                'affected_questions_without_math_academy_id':len({r['entity'] for r in rows if r['ma_id'] is None}),
                'fields_matching_retained_generated_payload':sum(bool(r['exact_generated_value_matches']) for r in matched),
                'affected_kps':sorted({k for r in rows for k in r['knowledge_points']}),
                'whole_topic_question_and_example_count':len(all_questions),'whole_topic_with_ma_id':sum(v is not None for v in all_questions.values()),
                'whole_topic_without_ma_id':sum(v is None for v in all_questions.values()),'field_evidence':matched})
# Original labelled equations from substitution canonical example.
p=Path('/home/jake/Developer/MA/DATA/Lessons/487/Source/487.html')
soup=BeautifulSoup(p.read_text(),'html.parser');n=soup.select_one('[contentid="13010"]')
math=n.select('mjx-assistive-mml math')[1]
(OUT/'wider-substitution-labelled-system.mathml').write_text(str(math)+'\n')
codepath='/home/jake/Developer/MA/PIPELINE/Math-Academy/3-Capture/1-Source/3-JSON/lesson-json.py'
spec=importlib.util.spec_from_file_location('wider_trace_lj',codepath);mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
flattened=mod.mathml_to_text(math)
# A representative elimination canonical source retains stacked equations.
epath=Path('/home/jake/Developer/MA/DATA/Lessons/4026/Source/4026.html')
esoup=BeautifulSoup(epath.read_text(),'html.parser');en=esoup.select_one('[contentid="13995"]')
emath=en.select('mjx-assistive-mml math')[0]
(OUT/'wider-elimination-source-system.mathml').write_text(str(emath)+'\n')
representatives=[]
for entity in [17592186505001,17592186509133]:
 rs=[r for r in findings if r['entity']==entity]
 (OUT/f'wider-question-{entity}.json').write_text(json.dumps(rs,indent=2)+'\n')
 representatives.append({'entity':entity,'field_evidence':str((OUT/f'wider-question-{entity}.json').relative_to(ROOT))})
report={'scope':'Only two additional topics identified by wider MTH341 scan. Counts include question/example entities when stated; affected records are questions.',
        'topics':topics,'representatives':representatives,
        'conclusion':'All 78 affected question entities lack a Math Academy ID; exact retained generator payload matches independently establish generator origin for the matching fields. All six affected KP generators emit escaped literal braces with semicolon-separated rows in affected branches.',
        'generator_code_locations':{
          '17592186073752':['generate/scratch/17592186073752.py:109','generate/scratch/17592186073752.py:127'],
          '17592186073753':['generate/scratch/17592186073753.py:85','generate/scratch/17592186073753.py:206'],
          '17592186192654':['generate/scratch/17592186192654.py:67','generate/scratch/17592186192654.py:82'],
          '17592186192655':['generate/scratch/17592186192655.py:172','generate/scratch/17592186192655.py:196'],
          '17592186192656':['generate/scratch/17592186192656.py:109','generate/scratch/17592186192656.py:166'],
          '17592186192657':['generate/scratch/17592186192657.py:115','generate/scratch/17592186192657.py:122']},
        'substitution_equation_labels':{'source_html':str(p),'canonical_ma_id':'e-13010','dom_id':n.get('id'),'math_index':1,
          'source_format':'Two stacked equation rows; each row contains its (1)/(2) label after a 2em mspace. Labels and corresponding equations are red/blue.',
          'mathml':str((OUT/'wider-substitution-labelled-system.mathml').relative_to(ROOT)),
          'reproduced_old_extractor_output':flattened,
          'fault':'mtable semicolon joining loses rows; ignored mspace merges each equation RHS and its label, producing =0(1) / =0(2). These parenthesized digits are equation labels, not multiplicative factors.',
          'repair_requirement':'Restore separate aligned rows and separately spaced equation labels, preserving references (1)/(2) in prose. A generic row-split repair alone does not restore the lost label spacing.'},
        'elimination_original':{'source_html':str(epath),'canonical_ma_id':'e-13995','dom_id':en.get('id'),'mathml':str((OUT/'wider-elimination-source-system.mathml').relative_to(ROOT)),
          'reproduced_old_extractor_output':mod.mathml_to_text(emath),'source_rows':len(emath.select('mtable > mtr'))},
        'mutations':'Evidence artifacts only; no production/database changes.'}
(OUT/'wider-findings.json').write_text(json.dumps(report,indent=2)+'\n')
for t in topics:print({k:v for k,v in t.items() if k!='field_evidence'})
print('labels',flattened)
