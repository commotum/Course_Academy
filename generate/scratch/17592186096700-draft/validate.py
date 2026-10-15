"""Independent prompt, worked-stage, pixel readback and native grader validation.
Never imports the registered generator and never writes registered paths.
"""
import copy, hashlib, importlib.util, itertools, json, re, subprocess, sys, uuid
from fractions import Fraction
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('kp96700_draft',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
ROOT=HERE.parents[2]

def check(condition,message):
 if not condition:raise AssertionError(message)
def write(name,value):(HERE/name).write_text(json.dumps(value,indent=2)+'\n')
def latex_rat(s):
 s=re.sub(r'\\frac\{(\d+)\}\{(\d+)\}',r'\1/\2',s)
 return sp.Rational(s or '1')
def parse_equation(text):
 match=re.fullmatch(r'([a-e])=([+-]?(?:\d+(?:/\d+)?)?)([a-e])',re.sub(r'\\frac\{(\d+)\}\{(\d+)\}',r'\1/\2',text.replace(' ','')))
 check(match is not None,'Unparseable displayed relation '+text)
 a,k,b=match.groups();return a,sp.Rational('-1' if k=='-' else '1' if k in ('','+') else k),b

def math_check(r,raster):
 q=r['question'];gen=r['generation'];fields=q[':question/answer-fields']
 st=[parse_equation(x) for x in re.findall(r'^- \*\*[IV]+\.\*\* \$(.*?)\$',q[':question/problem'],re.M)]
 check(len(st)==3,'Exactly three displayed statements')
 # Displacements are measured from the actual rendered PNG, snapped to its equal grid.
 vectors={label:[sp.Integer(a['recovered_tip_grid'][j]-a['recovered_tail_grid'][j]) for j in (0,1)] for label,a in raster['arrows'].items()}
 true=frozenset(i for i,(a,k,b) in enumerate(st) if all(vectors[a][j]==k*vectors[b][j] for j in (0,1)))
 check(g.parse_subset(gen['correct_inference'])==true,'Inference versus displayed geometry')
 check(raster['equal_physical_scale'],'Equal physical grid scale')
 if gen['plot'].get('labels'):
  check(set(raster['labels'])==set('abcde'),'Five actual PNG labels checked')
  check(all(v['blue_pixels_within_bbox_and_3px_margin']==0 and v['black_text_pixels']>=5 and v['association_distance_grid']<=.9 for v in raster['labels'].values()),'Actual PNG text clearance and close association')
 check(len(fields)==3 and [f[':answer-field/key'] for f in fields]==list(g.ROMAN),'Three source statement keys')
 for i,f in enumerate(fields):
  check(f[':answer-field/type']==':answer-field.type/checkbox','Current checkbox type')
  bank={a[':answer/id']:a for a in f[':answer-field/choices']}
  check(sorted((a[':answer/type'],a[':answer/value']) for a in bank.values())==[(':answer.type/text','false'),(':answer.type/text','true')],'Complete boolean bank')
  ref=f[':answer-field/correct'];check(ref[0]==':answer/id' and ref[1] in bank,'Field-owned correct answer')
  check(bank[ref[1]][':answer/value']==('true' if i in true else 'false'),'Correct selection versus actual PNG')
 if gen['evidence_only']:
  check(not gen['eligible_for_learning'] and ':question/difficulty' not in q,'Source replay stays unrated')
  values=re.findall(r'([a-e])=\((-?\d+),(-?\d+)\)',q[':question/worked-solution']);check(len(values)==4,'Four source computed vectors')
  for label,x,y in values:check(vectors[label]==[int(x),int(y)],'Source solution versus actual PNG')
 else:
  check(gen['eligible_for_learning'],'Completed instances eligible')
  sol=q[':question/worked-solution']
  bullets=re.findall(r'^- Statement (I|II|III) is (true|false)\.',sol,re.M)
  check(bullets==[(g.ROMAN[i],'true' if i in true else 'false') for i in range(3)],'Worked statements/conclusion reflect rendered prompt')
  for a,value,b in re.findall(r'The magnitude of \$([a-e])\$ is \$(.*?)\$ times the magnitude of \$([a-e])\$',sol,flags=re.I):
   actual=sp.sqrt(sum(x*x for x in vectors[a]))/sp.sqrt(sum(x*x for x in vectors[b]));check(sp.simplify(actual-latex_rat(value))==0,'Displayed magnitude ratio')
  for a,b,wording in re.findall(r'[Vv]ectors \$([a-e])\$ and \$([a-e])\$ (?:are parallel and )?have (the same direction|opposite directions)',sol):
   cross=vectors[a][0]*vectors[b][1]-vectors[a][1]*vectors[b][0];check(cross==0,'Stated parallelism')
   dot=sum(vectors[a][j]*vectors[b][j] for j in (0,1));check((dot>0)==(wording=='the same direction'),'Displayed direction prose')
  for i,bullet in enumerate(sol.split('\n\n')[0].split('\n')):
   final=re.findall(r'\$([^$]*(?:=|\\neq)[^$]*)\$',bullet)[-1]
   expr=final.replace(r'\neq','=');check(parse_equation(expr)==st[i],'Solution conclusion uses actual statement slots')
  if len(true)==1:expected=f'Therefore, only statement {g.ROMAN[next(iter(true))]} is true.'
  elif len(true)==2:expected='Therefore, only statements '+' and '.join(g.ROMAN[i] for i in sorted(true))+' are true.'
  elif len(true)==3:expected='Therefore, all three statements are true.'
  else:expected='Therefore, none of the statements are true.'
  check(sol.endswith(expected),'Final true-subset prose')
 text=q[':question/problem']+q.get(':question/worked-solution','')
 check(text.count('$')%2==0 and text.count('{')==text.count('}'),'Math delimiter/group balance')
 ids=[q[':question/id']]
 for f in fields:
  check(f[':answer-field/id']==g.owned(q[':question/id'],f[':answer-field/key']),'Field UUID ownership')
  check(all(a[':answer/id']==g.owned(f[':answer-field/id'],a[':answer/value']) for a in f[':answer-field/choices']),'Answer UUID ownership')
  ids+=[f[':answer-field/id']]+[a[':answer/id'] for a in f[':answer-field/choices']]
 for x in ids:uuid.UUID(x)
 check(len(set(ids))==len(ids),'Unique owned IDs')
 return {'true_subset':g.subset_text(true),'vectors_read_from_png':{k:[str(x) for x in v] for k,v in vectors.items()}}

def ordered(x):
 if isinstance(x,dict):return {str(k):ordered(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return sorted([ordered(v) for v in x],key=lambda z:json.dumps(z,sort_keys=True))
 return str(x) if not isinstance(x,(str,int,float,bool)) and x is not None else x

def engine_item(r):
 checks=[]
 for i,f in enumerate(r['question'][':question/answer-fields']):
  correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
  for a in f[':answer-field/choices']:
   checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==correct else 'rejected','purpose':'Current checkbox field-owned true/false ID'})
  # The actual current contract is choice IDs, including explicit false.
  # Leading-zero decimal encoding resolves to the same field-owned entity ID.
  for ai,a in enumerate(f[':answer-field/choices']):
   checks.append({'field_index':i,'submitted':str(100+2*i+ai).zfill(6),'expected':'accepted' if a[':answer/value']==correct else 'rejected','purpose':'Equivalent decimal-ID encoding; canonical text boolean is not a submission'})
 return {'label':r['question'][':question/id'],'record':r,'checks':checks}

def raster_records(records):
 original=json.loads((HERE/'original-geometry.json').read_text());request=[]
 for r in records:
  gen=r['generation'];q=r['question'];level=q.get(':question/difficulty',':question.difficulty/moderate').split('/')[-1]
  replay=g.generate(level,gen['seed'],template=gen['template'],parameters=gen['parameters'],profile=gen['bank_profile'])
  check(ordered(q)==ordered(replay['question']),'Deterministic public replay')
  p=g.normalize_parameters(level,gen['template'],gen['parameters'],gen['evidence_only'])
  check(gen['mathematical_fingerprint']==g.task_key(gen['template'],p),'Recomputed mathematical signature')
  plot=gen['plot'];asset=plot.get('source_asset') or q[':question/problem'].split('![](')[1].split(')')[0]
  transform=original[g.match_original(gen['template'],p)['source_id']]['transform'] if plot.get('source_asset') else plot['transform']
  check(g.file_hash(asset)==plot['png_sha256'],'Plot hash')
  request.append({'id':q[':question/id'],'path':asset,'geometry':gen['geometry'],'transform':transform,'labels':plot.get('labels')})
 write('raster-input.json',{'audit_existing':True,'records':request,'output':str(HERE/'raster-report.json')})
 subprocess.run([g.RUNTIME,str(HERE/'render_plot.py'),str(HERE/'raster-input.json')],check=True,capture_output=True)
 return json.loads((HERE/'raster-report.json').read_text())

def normalized_record(q):
 def enum(v):return v[':db/ident'] if isinstance(v,dict) else v
 out={k:v for k,v in q.items() if k.startswith(':question/') and k!=':question/math-academy-id'}
 if ':question/difficulty' in out:out[':question/difficulty']=enum(out[':question/difficulty'])
 fields=[]
 for f in sorted(q[':question/answer-fields'],key=lambda f:g.ROMAN.index(f[':answer-field/key'])):
  ff={k:v for k,v in f.items() if k.startswith(':answer-field/')};ff[':answer-field/type']=enum(ff[':answer-field/type'])
  ff[':answer-field/choices']=[{k:enum(v) if k==':answer/type' else v for k,v in a.items() if k.startswith(':answer/')} for a in f[':answer-field/choices']]
  ff[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']];fields.append(ff)
 out[':question/answer-fields']=fields
 return out

def main():
 cases=json.loads((HERE/'source-cases.json').read_text());byid={x['source_id']:x['record'] for x in cases};records=[];fidelity=[]
 for case in g.SOURCE_CASES:
  r=g.generate('moderate',0,case['template'],parameters=case['parameters'],profile='source-a' if case['template']==g.TEMPLATES[0] else 'source-b')
  q=byid[case['source_id']];new=r['question'];check(':question/difficulty' not in q and ':question/difficulty' not in new,'Current original remains unrated')
  for key in (':question/problem',':question/worked-solution'):check(new[key]==q[key],'Exact current source text '+key)
  oldfields={f[':answer-field/key']:f for f in q[':question/answer-fields']}
  check(set(oldfields)==set(g.ROMAN),'Current original field layout')
  for f in new[':question/answer-fields']:
   old=oldfields[f[':answer-field/key']]
   check(f[':answer-field/type']==old[':answer-field/type'][':db/ident'],'Current source field type')
   check(sorted((a[':answer/type'],a[':answer/value']) for a in f[':answer-field/choices'])==sorted((a[':answer/type'][':db/ident'],a[':answer/value']) for a in old[':answer-field/choices']),'Whole source bank')
   correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);check(correct==old[':answer-field/correct'][':answer/value'],'Source designation')
  records.append(r);fidelity.append({'source_id':case['source_id'],'exact_prompt':True,'exact_solution':True,'complete_banks_matched':3,'values_matched':6,'correct_designations_matched':3,'unrated_status_preserved':True})
 legacy=json.loads((HERE/'reference/registered-drafts.json').read_text());legacy_byid={r['question'][':question/id']:r for r in legacy};preserved=[];repairs=[]
 for inv in json.loads((HERE/'independent-inventory.json').read_text())['questions']:
  raw=inv['record'];qid=raw[':question/id'];old=legacy_byid[qid];gen=old['generation'];level=raw[':question/difficulty'][':db/ident'].split('/')[-1]
  r=g.generate(level,gen['seed'],gen['template'],parameters=gen['parameters'],profile=gen['bank_profile'])
  # Absolute local assets became content addressed EDB image references at registration.
  expected=normalized_record(raw);expected[':question/problem']=r['question'][':question/problem']
  bad_tex=re.findall(r'\\neq[a-e]',expected[':question/worked-solution'])
  if bad_tex:
   repaired=re.sub(r'\\neq(?=[a-e])',lambda m:m.group(0)+' ',expected[':question/worked-solution'])
   check(r['question'][':question/worked-solution']==repaired,'Only minimal invalid TeX separator repaired')
   for newfield,oldfield in zip(r['question'][':question/answer-fields'],expected[':question/answer-fields']):
    check(newfield[':answer-field/key']==oldfield[':answer-field/key'],'Repair field role unchanged')
    check(sorted(a[':answer/value'] for a in newfield[':answer-field/choices'])==sorted(a[':answer/value'] for a in oldfield[':answer-field/choices']),'Repair complete bank unchanged')
    newanswer=next(a[':answer/value'] for a in newfield[':answer-field/choices'] if a[':answer/id']==newfield[':answer-field/correct'][1]);oldanswer=next(a[':answer/value'] for a in oldfield[':answer-field/choices'] if a[':answer/id']==oldfield[':answer-field/correct'][1]);check(newanswer==oldanswer,'Repair key unchanged')
   repairs.append({'original_question_id':qid,'draft_question_id':r['question'][':question/id'],'invalid_tex_commands':bad_tex,'repair':'Insert a TeX command separator after \\neq before its vector label; mathematics, prose, bank and key retained.'})
  else:check(ordered(r['question'])==ordered(expected),'All valid registered authored content identities/fields/prose preserved '+qid)
  check(raw[':question/problem'].split(')\n',1)[1]==r['question'][':question/problem'].split(')\n',1)[1],'Registered prompt mathematical text unchanged')
  records.append(r)
  if not bad_tex:preserved.append(qid)
 # Cover each target slot with the other data held constant and all truth masks.
 slot_cases=[]
 for level in ('easy','moderate','hard'):
  templates=g.TEMPLATES[:1] if level=='easy' else g.TEMPLATES
  for template in templates:
   primary=(('b','e'),('a','e')) if template==g.TEMPLATES[0] else (('a','c'),('c','a'))
   secondary=(('c','d'),('d','c')) if template==g.TEMPLATES[0] else (('b','d'),('d','b'))
   for pair,cross,signs in itertools.product(primary,secondary,itertools.product((-1,1),repeat=2)):
    p=dict(u=[2,2] if level=='easy' else [2,4] if level=='hard' else [2,1],v=[0,2] if level=='easy' else [3,-2],k='1' if level=='easy' else '3/2' if level=='hard' else '2',s=signs[0],t=signs[1],targets={'primary':list(pair),'secondary':list(cross)})
    r=g.generate(level,7,template,parameters=p);records.append(r);slot_cases.append({'level':level,'template':template,'targets':p['targets'],'s':p['s'],'t':p['t'],'truth':r['generation']['correct_inference']})
 for level in ('easy','moderate','hard'):
  for seed in range(6):records.append(g.generate(level,seed))
 for r in records:
  gen=r['generation'];level=r['question'].get(':question/difficulty',':question.difficulty/moderate').split('/')[-1]
  other=g.generate(level,999,gen['template'],parameters=gen['parameters'],profile=gen['bank_profile']);check(ordered(other['question'])==ordered(r['question']),'Seed-independent content')
 invalid=[]
 for value in (True,False,None,1.0,'1'):
  try:g.generate('easy',value)
  except ValueError:invalid.append(repr(value))
  else:raise AssertionError('Invalid built-in seed accepted')
 raster=raster_records(records);math=[math_check(r,raster[r['question'][':question/id']]) for r in records]
 write('math-report.json',math);write('review.json',records);write('slot-coverage.json',slot_cases);write('source-replay.json',fidelity);write('preserved-inventory.json',preserved);write('inventory-repairs.json',repairs)
 write('native-input.json',[engine_item(r) for r in records])
 subprocess.run([str(HERE/'check-engine33510bf3'),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
 # Genuine unsupported typed math/text is preserved separately in native probes,
 # no invented expected mathematical equivalence for a checkbox field.
 probes=engine_item(records[-1]);probes['checks']=[]
 for i in range(3):
  for submission in ('','true','false','I only','-2e','{"checked":true}','{"value":"true"}'):
   probes['checks'].append({'field_index':i,'submitted':submission,'expected':'unresolved','purpose':'Unsupported typed checkbox entry explicitly documented'})
 write('unsupported-native-input.json',[probes])
 subprocess.run([str(HERE/'check-engine33510bf3'),str(HERE/'unsupported-native-input.json'),str(HERE/'unsupported-native-report.json')],check=True)
 # Final keys unchanged in every mutation. Independent readback must catch each.
 base=next(r for r in records if not r['generation']['evidence_only'] and r['generation']['parameters'].get('targets',{}).get('primary')==['b','e'] and r['generation']['parameters']['s']==-1)
 negative=[]
 def reject_mutation(kind,mutated,rr):
  check(mutated['question'][':question/answer-fields']==base['question'][':question/answer-fields'],'Negative control final keys unchanged')
  try:math_check(mutated,rr)
  except AssertionError as e:negative.append({'kind':kind,'caught':True,'reason':str(e)})
  else:raise AssertionError('Negative control escaped: '+kind)
 rr=raster[base['question'][':question/id']]
 bad=copy.deepcopy(base);bad['question'][':question/problem']=bad['question'][':question/problem'].replace('$b =-', '$a =-',1);reject_mutation('wrong statement target',bad,rr)
 bad=copy.deepcopy(base);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('opposite directions','the same direction',1);reject_mutation('wrong direction prose',bad,rr)
 bad=copy.deepcopy(base);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('is $1$ times','is $2$ times',1);reject_mutation('wrong magnitude stage',bad,rr)
 # Render an actual different vector with the original metadata/key kept intact.
 geom=copy.deepcopy(base['generation']['geometry']);a=geom['b'];a['tip']=[str(2*int(a['tail'][j])-int(a['tip'][j])) for j in (0,1)]
 asset,meta=g.render_plots(geom);bad=copy.deepcopy(base);bad['question'][':question/problem']=re.sub(r'!\[\]\([^)]*\)','![]('+asset+')',bad['question'][':question/problem'],count=1)
 reject_mutation('wrong plotted vector actual PNG',bad,meta['raster'])
 write('negative-controls.json',negative)
 write('validation.json',{'status':'passed','basis':g.SOURCE['basis'],'source_originals':2,'independent_inventory_preserved':len(preserved),'independent_inventory_tex_repairs':len(repairs),'complete_source_banks':'6/6','source_values':'12/12','source_designations':'6/6','source_prompt_and_solution':'2/2','pixel_and_math_records':len(records),'target_cases':len(slot_cases),'seed_invalid_rejections':invalid,'negative_controls':negative})
 print('passed',len(records),'records',len(slot_cases),'target cases')
if __name__=='__main__':main()
