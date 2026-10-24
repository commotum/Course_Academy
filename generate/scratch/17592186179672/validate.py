"""Independent directed-edge and complete-bank checks; actual learner grader."""
import sys
sys.dont_write_bytecode=True
import hashlib,importlib.util,itertools,json,re,subprocess
from pathlib import Path
from PIL import Image,ImageDraw
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('triangle_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
# Independently read from each source diagram (not from its answer key).
EDGES={
 'q-76473':('OABO',['OA','BA','BO']), 'q-76476':('ABCA',['BA','BC','AC']),
 'q-77125':('ODEO',['OD','ED','OE']), 'q-77131':('KMLK',['KM','LM','KL']),
 'q-77138':('TUVT',['UT','UV','VT']), 'q-77143':('OGHO',['GO','HG','HO']),
 'q-77146':('LMNL',['LM','NM','NL']), 'q-77148':('DEFD',['DE','EF','DF']),
 'q-77134':('PQRP',['QP','QR','RP']), 'q-77145':('UVWU',['UV','WV','UW'])}
def write(path,x):path.write_text(json.dumps(x,indent=2,default=str)+'\n')
def engine_item(label,r):
 f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
 return {'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'complete radio bank'} for a in f[':answer-field/choices']]}
def normal_source(q):
 q={k:v for k,v in q.items() if k in (':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields')};q[':question/difficulty']=q[':question/difficulty'][':db/ident']
 fs=[]
 for old in q[':question/answer-fields']:
  f={':answer-field/id':old[':answer-field/id'],':answer-field/key':old[':answer-field/key'],':answer-field/type':old[':answer-field/type'][':db/ident'],':answer-field/correct':[':answer/id',old[':answer-field/correct'][':answer/id']],':answer-field/choices':[{':answer/id':a[':answer/id'],':answer/type':a[':answer/type'][':db/ident'],':answer/value':a[':answer/value']} for a in old[':answer-field/choices']]};fs.append(f)
 q[':question/answer-fields']=fs;return q

def math_check(r):
 m=r['generation'];s=tuple(m['parameters']['signs']);q=r['question'];asset=m['asset'];points=asset['points']
 # Positive signed triangle area establishes ABCA as counterclockwise.
 area=sp.det(sp.Matrix([[points[1][0]-points[0][0],points[1][1]-points[0][1]],[points[2][0]-points[0][0],points[2][1]-points[0][1]]]))
 assert area>0
 got=[]
 for i,edge in enumerate(asset['reference_edges']):
  forward=[i,(i+1)%3];got.append(1 if edge==forward else -1);assert sorted(edge)==sorted(forward)
 assert tuple(got)==s
 f=q[':question/answer-fields'][0];key=f[':answer-field/correct'][1];values=[g.signs(a[':answer/value']) for a in f[':answer-field/choices']]
 expected=sum(sign*var for sign,var in zip(got,g.I));eq=[sp.expand(sum(t*var for t,var in zip(v,g.I))-expected)==0 for v in values]
 assert sum(eq)==1 and f[':answer-field/choices'][eq.index(True)][':answer/id']==key
 assert len(set(values))==5
 # Read rendered solution key independently of metadata.
 final=q[':question/worked-solution'].split('&= ')[-1].split(r'.\end{aligned}')[0];assert g.signs(final)==tuple(got)
 for i,sign in enumerate(got):
  term=g.integral(i+1,sign<0);assert term in q[':question/worked-solution']
 assert '{{selection}}' not in q[':question/problem'] and '$ABCA$' in q[':question/problem'] and 'counterclockwise' in q[':question/problem']
 assert Path(asset['prompt']).is_file() and hashlib.sha256(Path(asset['prompt']).read_bytes()).hexdigest()==asset['sha256']
 return True

def main():
 replay=[];native=[]
 for mid,q in g.SOURCES.items():
  path,edges=EDGES[mid];traversal=[path[i:i+2] for i in range(3)];expected=tuple(1 if e==t else -1 for e,t in zip(edges,traversal));assert all(e in (t,t[::-1]) for e,t in zip(edges,traversal))
  f=q[':question/answer-fields'][0];assert g.signs(f[':answer-field/correct'][':answer/value'])==expected
  r=g.replay_source(mid);assert r['source_bank']==r['generated_bank'];assert r['correct']==f[':answer-field/correct'][':answer/value']
  replay.append({'source_id':mid,'path':path,'diagram_edges':edges,'correct_signs':expected,'complete_bank_matched':True,'matched_choices':5,'matched_distractors':4,'original':q,'generated_bank':r['generated_bank']})
  native.append(engine_item('source '+mid,{'knowledge_point':{'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE},'question':normal_source(q),'generation':{'template':'source '+mid}}))
 records=[];coverage={mid:[] for mid in g.SOURCES}
 for mid in g.SOURCES:
  for vector in g.DOMAIN:
   r=g.generate('easy',17,{'signs':vector},mid);math_check(r);coverage[mid].append(list(vector));records.append(r);native.append(engine_item(mid+' '+str(vector),r))
 # Deterministic replay, seed is not mathematical identity, no option permutation as novelty.
 a=g.generate('easy',7,{'signs':[-1,1,-1]},'q-76473');b=g.generate('easy',7,{'signs':[-1,1,-1]},'q-76473');c=g.generate('easy',999,{'signs':[-1,1,-1]},'q-76473');assert a==b and a['question']==c['question']
 # Same data and profile, single changed edge: rendered solution, diagram, key all change together.
 d=g.generate('easy',7,{'signs':[1,1,-1]},'q-76473');assert math_check(d) and math_check(a);assert a['generation']['asset']['points']==d['generation']['asset']['points'];assert a['generation']['asset']['reference_edges'][0]==list(reversed(d['generation']['asset']['reference_edges'][0]));assert a['question'][':question/worked-solution']!=d['question'][':question/worked-solution']
 for level in ['moderate','hard','unclassified']:
  try:g.generate(level)
  except ValueError:pass
  else:raise AssertionError('unsupported band accepted')
 for bad in [[True,1,1],[0,1,1],[1,1],[1,1,2]]:
  try:g.generate(parameters={'signs':bad})
  except ValueError:pass
  else:raise AssertionError('bad signs accepted')
 for count in [0,9]:
  try:g.batch('easy',count)
  except ValueError:pass
  else:raise AssertionError('finite bound not enforced')
 assert len({r['generation']['mathematical_fingerprint'] for r in g.batch('easy',8,93)})==8
 write(HERE/'source-replay.json',replay);write(HERE/'reference/engine-input.json',native)
 subprocess.run([str(HERE/'reference/check-engine'),str(HERE/'reference/engine-input.json'),str(HERE/'reference/engine-report.json')],check=True)
 review=[next(r for r in records if r['generation']['parameters']['signs']==list(s)) for s in g.DOMAIN];write(HERE/'review.json',review);(HERE/'review.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in review)+'\n')
 sheets=Image.new('RGB',(1200,720),'white')
 for i,r in enumerate(review):
  im=Image.open(r['generation']['asset']['prompt']).convert('RGB');im.thumbnail((300,325));card=Image.new('RGB',(300,360),'white');card.paste(im,((300-im.width)//2,30));ImageDraw.Draw(card).text((8,8),str(r['generation']['parameters']['signs']),fill='black');sheets.paste(card,((i%4)*300,(i//4)*360))
 sheets.save(HERE/'reference/generated-contact-sheet.png')
 report={'status':'passed','source_basis':g.SOURCE['basis'],'source_questions':10,'complete_source_banks_matched':10,'source_choices_matched':50,'source_distractors_matched':40,'source_correct_keys_matched':10,'raw_source_prose_preserved_as_evidence':True,'prose_fidelity':'same prompt and three solution stages; generated wording regularized, not literal prose replay','profiles':10,'template_count':1,'exhaustive_profile_by_sign_cases':len(records),'finite_mathematical_tasks':8,'coverage':coverage,'independent_diagram_edge_checks':10,'changed_edge_fixed_geometry_check':True,'deterministic_replay':True,'grader_report':'reference/engine-report.json','unsupported_bands':['moderate','hard'],'source_math_errors':[],'database_writes':0,'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest()};write(HERE/'validation.json',report);print(json.dumps({k:v for k,v in report.items() if k!='coverage'},indent=2))
if __name__=='__main__':main()
