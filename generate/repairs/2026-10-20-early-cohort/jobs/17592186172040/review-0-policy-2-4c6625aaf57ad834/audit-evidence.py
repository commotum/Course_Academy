from review import *
import collections,re,math
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
from PIL import Image,ImageDraw
fresh=json.loads((E/'fresh-records.json').read_text());cf=json.loads((E/'counterfactual-records.json').read_text());batch=json.loads((E/'batch-records.json').read_text());src=json.loads((J/'source/source.json').read_text()); inventory=json.loads((J/'source/inventory.json').read_text())
# Prompt math independently read from served TeX, rather than treating generation.equation as truth.
x,y=sp.symbols('x y',real=True);prompt_checks=[]
for r in fresh+cf+batch:
 if not r['generation']['template'].startswith('possible'):continue
 tex=r['question'][':question/problem'].split('x}=')[1].split('?$')[0]
 text=re.sub(r'e\^\{([^{}]*)\}',r'exp(\1)',tex).replace('{','(').replace('}',')').replace('^','**')
 e=parse_expr(text,local_dict={'x':x,'y':y,'exp':sp.exp},transformations=standard_transformations+(implicit_multiplication_application,))
 m=sp.sympify(r['generation']['equation'],locals={'x':x,'y':y,'exp':sp.exp})
 prompt_checks.append({'id':r['question'][':question/id'],'tex':tex,'parsed':str(e),'matches_plotted_equation':sp.simplify(e-m)==0})
dump('prompt-math.json',prompt_checks)
# Verify exact bytes of all captured source image evidence and make a bounded visual bank sheet.
assets=[];sheet=Image.new('RGB',(5*170,8*175),'white');draw=ImageDraw.Draw(sheet)
for row,q in enumerate(src['material']['kp'][':knowledge-point/questions']):
 for col,a in enumerate(q[':question/answer-fields'][0][':answer-field/choices']):
  rel=a[':answer/value'];canonical=pathlib.Path('/media/jake/SSD/EDB/math')/rel;local=PK/KP/rel
  assets.append({'source_id':q[':question/id'],'asset':rel,'canonical_exists':canonical.exists(),'bytes_equal':canonical.read_bytes()==local.read_bytes() if canonical.exists() else None})
  im=Image.open(local).convert('RGB');im.thumbnail((165,145));sheet.paste(im,(col*170,row*175+25));draw.text((col*170+3,row*175+4),q[':question/math-academy-id']+' #'+str(col+1),fill='black')
sheet.save(E/'source-banks.png');dump('source-assets.json',assets)
# Complete inventory inspection: it contains eight source instances and no generated records.
source_ids={q[':question/id'] for q in src['material']['kp'][':knowledge-point/questions']}
dump('inventory-review.json',{'database':inventory['database'],'basis':inventory['basis'],'count':len(inventory['questions']),'records':[{'question_id':q[':question/id'],'entity_id':q[':db/id'],'original_source':q[':question/id'] in source_ids,'generation_attributes':[k for k in q if 'generat' in k]} for q in inventory['questions']],'conclusion':'Verified absence of generated instances in this captured inventory; packaging failure does not implicate original source records. No stored generated-record reproduction is possible or required.'})
dump('affected-inventory.json',{'affected_questions':[]})
# Counterfactual dependencies, including actual prompt, image response, solution, plus native grader and renderer evidence elsewhere.
def key(r):
 f=r['question'][':question/answer-fields'][0];return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def common(r,s):
 def vals(q):return {a[':answer/value'] for a in q['question'][':question/answer-fields'][0][':answer-field/choices']}
 return len(vals(r)&vals(s))
dump('counterfactual-results.json',{'parameters':cf[0]['generation']['parameters'],'relevant_sign':{'before':cf[0]['question'][':question/problem'],'after':cf[1]['question'][':question/problem'],'key_image_changed':key(cf[0])!=key(cf[1]),'common_options':common(cf[0],cf[1]),'new_key_in_solution':key(cf[1]) in cf[1]['question'][':question/worked-solution']},'irrelevant_unused_slot':{'change':'single linear to exp in moderate product, used only for hard outlier','question_preserved':cf[0]['question']==cf[2]['question'],'same_key_image':key(cf[0])==key(cf[2])},'relevant_target':{'change':'impossible_x to impossible_y, other parameters and seed held fixed','prompt_preserved':cf[3]['question'][':question/problem']==cf[4]['question'][':question/problem'],'common_options':common(cf[3],cf[4]),'key_image_changed':key(cf[3])!=key(cf[4]),'before_solution':cf[3]['question'][':question/worked-solution'],'after_solution':cf[4]['question'][':question/worked-solution']}})
# Faithful deterministic learner draw within a sole positively weighted moderate band; inspect source for fallbacks and history limitations.
def select_index(seed,count):
 d=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(d[8:16],'big')>>11)/2**53;return int(u*count)
selection=[]
for name in ['batch','moderate','hard','easy']:
 rs=json.loads((E/('delivery-'+name)/'accepted.json').read_text()); sorted_rs=sorted(enumerate(rs),key=lambda t:t[1]['question'][':question/id']); draws=collections.Counter()
 for n in range(128):
  if not rs:continue
  idx=select_index('independent-review-'+str(n),len(rs));r=sorted_rs[idx][1];draws[r['generation']['template']]+=1
 selection.append({'pool':name,'accepted_count':len(rs),'input_cases':dict(collections.Counter(r['generation']['template'] for r in rs)),'within_band_draws':dict(draws),'seed_prefix':'independent-review-','draws':128,'ordering':'question UUID order used as a stable entity-order stand-in; live entity IDs and learner history unavailable','basis':inventory['basis']})
dump('selection-results.json',{'implementation':'engine/rust/question_selection.rs select(): floor(uniform(second 8 bytes of SHA256(domain/seed))*pool.len), uniform within selected band; seen_before_task separately excludes history','cases':selection,'limits':'No live learner policy weights, future entity IDs or seen/reserved history supplied. Audited the applicable within-band mapping for captured moderate eligible pool; cannot certify a particular live learner sequence. Unconfigured policy picks first entity, so arbitrary UUID ordering is not claimed to reproduce that fallback.'})
# All image choices use identical authored styling, positions shuffled. Count superficial actions separately within each recognizable template.
probes=[]
def position(r):
 f=r['question'][':question/answer-fields'][0];return next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])
for pool,rs in [('fresh',fresh),('runner_batch',batch),('delivered_batch',json.loads((E/'delivery-batch/accepted.json').read_text()))]:
 groups={'overall':rs}
 for t in set(r['generation']['template'] for r in rs):groups[t]=[r for r in rs if r['generation']['template']==t]
 for t,gr in sorted(groups.items()):
  counts=collections.Counter(position(r) for r in gr)
  probes.append({'pool':pool,'template':t,'total':len(gr),'position_counts':dict(counts),'choose_first_correct':counts[0],'best_constant_position_correct':max(counts.values()),'best_position':max(counts,key=counts.get),'baseline':.2,'all_same_position':len(counts)==1})
dump('shortcut-results.json',probes)
print('prompt checks',len(prompt_checks),'failures',sum(not c['matches_plotted_equation'] for c in prompt_checks),'source assets',len(assets),'mismatches',sum(not a['bytes_equal'] for a in assets))
print('shortcut summaries',[(p['pool'],p['template'],p['total'],p['position_counts']) for p in probes])
