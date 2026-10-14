"""Source replay, independent graph facts, all checkbox grading, finite identity."""
import copy,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('g',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
FACTS={'q-48042':(2,2,'-inf',3,3),'q-48064':(2,2,1,-2,1),'q-48063':(2,2,3,3,1),'q-104049':(2,2,2,2,2),'q-104051':(5,5,2,4,2),'q-104052':(0,0,3,3,None),'q-104124':(-2,-2,5,5,5),'q-48040':(-1,-1,2,1,1),'q-48062':(1,1,1,1,None),'q-48065':(2,2,1,1,1),'q-48067':(1,1,1,1,1),'q-48068':(1,-1,1,1,None)}
EXPECTED={'q-48042':[False,True,True],'q-48064':[True,False,False],'q-48063':[True,True,False],'q-104049':[True,False,False],'q-104051':[True,False,True],'q-104052':[True,True,False],'q-104124':[False,True,True],'q-48040':[True,False,False],'q-48062':[False,True,False],'q-48065':[True,True,True],'q-48067':[True,True,True],'q-48068':[True,False,True]}
def check(rec):
 q=rec['question'];t=rec['generation']['template'];assert t in FACTS
 assert rec['knowledge_point']['db_id']==g.KP_ID
 z=g.SPECS[t];assert tuple(z[k] for k in ('a','b','left','right','value'))==FACTS[t]
 assert g.truth(t)==EXPECTED[t]
 assert q[':question/problem']==g.QUESTIONS[t][':question/problem']
 assert q[':question/worked-solution']==g.QUESTIONS[t][':question/worked-solution']
 assert [f[':answer-field/key'] for f in q[':question/answer-fields']]==['I','II','III']
 assert len(re.findall(r'\*\*(?:I|II|III)\.\*\*',q[':question/problem']))==3
 for f,expected in zip(q[':question/answer-fields'],EXPECTED[t]):
  assert f[':answer-field/type']==':answer-field.type/checkbox'
  choices=f[':answer-field/choices'];assert len(choices)==2
  assert {a[':answer/value'] for a in choices}=={'true','false'}
  assert all(a[':answer/type']==':answer.type/text' for a in choices)
  assert next(a[':answer/value'] for a in choices if a[':answer/id']==f[':answer-field/correct'][1])==str(expected).lower()
  assert len({a[':answer/id'] for a in choices})==2
 assert rec['generation']['mathematical_fingerprint']==g.fingerprint(t)
 asset=Path('/media/jake/SSD/EDB/math')/re.search(r'!\[\]\((.*?)\)',q[':question/problem'])[1]
 assert asset.exists();assert hashlib.sha256(asset.read_bytes()).hexdigest()==asset.stem
 for text in (q[':question/problem'],q[':question/worked-solution']):assert all(ord(c)>=32 or c in '\n\t' for c in text)

def engine_item(rec):
 checks=[]
 for i,f in enumerate(rec['question'][':question/answer-fields']):
  for a in f[':answer-field/choices']:
   checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Actual checkbox grader, true and false choice IDs'})
 return {'label':rec['generation']['template'],'record':rec,'checks':checks}

def grade(records,path):
 path.mkdir(parents=True,exist_ok=True);(path/'native-input.json').write_text(json.dumps([engine_item(r) for r in records],indent=2))
 subprocess.run([str(ROOT/'check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
 report=json.loads((path/'native-report.json').read_text());assert report['accepted_checks']==3*len(records) and report['rejected_checks']==3*len(records) and report['documented_unresolved_checks']==0
 return report

def main():
 records=[];source_options=0;source_banks=0;images=[]
 for t in g.QUESTIONS:
  r=g.replay_source(t);check(r);records.append(r);assert r['question']==g.normalize(g.QUESTIONS[t]);source_options+=6;source_banks+=3
  images.append(re.search(r'!\[\]\((.*?)\)',r['question'][':question/problem'])[1])
 for t in g.TEMPLATES:
  r=g.generate('easy',template=t);check(r);records.append(r)
  a=copy.deepcopy(r['question']);b=copy.deepcopy(g.replay_source(t)['question'])
  def values(q):return (q[':question/problem'],q[':question/worked-solution'],[(f[':answer-field/key'],f[':answer-field/type'],sorted(a[':answer/value'] for a in f[':answer-field/choices']),next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])) for f in q[':question/answer-fields']])
  assert values(a)==values(b)
  assert g.generate('easy',1,t)['question']==g.generate('easy',987,t)['question']
 for level,params in [('moderate',None),('hard',None),('easy',{'shift':2})]:
  try:g.generate(level,parameters=params)
  except ValueError:pass
  else:raise AssertionError('unsupported extension or duplicate shift accepted')
 catalog=g.batch('easy',1000,20261014);assert len(catalog)==len({r['generation']['mathematical_fingerprint'] for r in catalog})==10
 bad=copy.deepcopy(records[0]);f=bad['question'][':question/answer-fields'][0];f[':answer-field/correct'][1]=next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1])
 try:check(bad)
 except AssertionError:pass
 else:raise AssertionError('incorrect key not detected')
 native=grade(records,ROOT/'reference/validation')
 report={'status':'passed','version':g.VERSION,'script_sha256':hashlib.sha256(ROOT.with_suffix('.py').read_bytes()).hexdigest(),'source_basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'source_replay':{'questions':12,'complete_banks_matched':source_banks,'complete_banks_total':36,'options_matched':source_options,'options_total':72,'correct_designations_matched':36,'prompt_solution_exact':True},'mathematics':{'independent_graph_facts':12,'independent_checkbox_truths':36,'wrong_key_mutation_rejected':True},'grading':{'accepted':native['accepted_checks'],'rejected':native['rejected_checks'],'unresolved':0,'build':json.loads((ROOT/'check-engine-build.json').read_text())},'supported_levels':['easy'],'unsupported_levels':['moderate','hard'],'finite_catalog_tasks':10,'variable_slots':[],'rejected_duplicate_coordinate_shifts':True,'deterministic_identity':True,'q48064_unrated_preserved':True,'plots':{'new_required':False,'existing_assets_verified':images},'db_writes':0}
 (ROOT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');(ROOT/'review.md').write_text('\n\n---\n\n'.join('## '+r['generation']['template']+(' — source replay' if r['generation']['evidence_only'] else ' — generated replay (existing task; excluded from replenishment)')+'\n\n'+r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution'] for r in records)+'\n')
 print(json.dumps({k:report[k] for k in ('status','source_replay','finite_catalog_tasks','supported_levels','unsupported_levels')}))
if __name__=='__main__':main()
