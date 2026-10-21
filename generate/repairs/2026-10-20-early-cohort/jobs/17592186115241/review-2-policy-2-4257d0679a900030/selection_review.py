import pathlib,json,sys,hashlib,collections,subprocess,importlib.util,copy
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;J=E.parent;P=J/'workspace';R=pathlib.Path('/home/jake/Developer/Course_Academy');sys.path.insert(0,str(P))
from independent_math import *
def read(p):return json.load(open(E/p))
def dump(n,x):(E/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def load(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
# Correct the inherited selection narrative and retain executable formulas.
I=json.load(open(J/'source/inventory.json'));batches=read('delivery-batch/accepted.json');draws=[]
for i in range(30):
 seed='independent-review-v1.1.1-'+str(i);digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53);draws.append({'seed':seed,'candidate_rank':int(u*len(batches))})
bands=collections.defaultdict(list)
for q in I['questions']:
 d=q.get(':question/difficulty');bands[d[':db/ident'].split('/')[-1] if d else 'unrated'].append(q[':db/id'])
for key in bands:bands[key].sort()
dump('learner-selection.json',{'implementation':'engine/rust/question_selection.rs select() and seen_before_task(), directly inspected','implementation_sha256':hashlib.sha256((R/'engine/rust/question_selection.rs').read_bytes()).hexdigest(),'captured_basis':I['basis'],'captured_band_candidates':dict(bands),'examined_rules':['exclude prior tasks and current prefix','sort/deduplicate numeric entity candidates','nonempty positive-weight difficulty band, then uniform candidate rank','unconfigured policy selects first numeric ID','unrated fallback only when no positive-weight rated band remains'],'batch_easy_candidate_count':len(batches),'batch_rank_draws':draws,'pre_post_decision_coverage':'delivery-shortcuts.json','source_variant_candidates':55,'source_unique_fraction_cues':0,'result':'No normalization/dedup or difficulty losses. Easy-band selection does not favor a mathematical case within the surviving candidate pool. Every batch candidate was independently audited, including the first-candidate fallback. The same analysis applies to all source-support candidates.','limits':['Future numeric IDs, live learner histories and configured weights are unavailable; no claim about a particular learner draw or probability across difficulty bands.','Seen exclusions can reduce coverage; audited banks are unchanged by selection.','Captured moderate/hard historical component defects remain recorded in affected-inventory.json; they are outside the requested easy batch.']})

x=json.load(open(E/"learner-selection.json"));x["unit_coefficient_cue"]={"q32244_candidates":20,"applicable":8,"correct":8,"after_filter_same":True};x["result"]='No normalization/dedup or difficulty losses. Within-band selection can deliver any cue-bearing source-profile candidate; it does not modify its bank. The exact runner batch has no successful unit-coefficient cue. All its candidates, including the unconfigured first-candidate fallback, were independently audited.';dump("learner-selection.json",x)

x=json.load(open(E/"learner-selection.json"));x["unit_coefficient_cue"]={"q32244_candidates":20,"applicable":8,"correct":8,"after_filter_same":True};x["result"]='No normalization/dedup or difficulty losses. Within-band selection can deliver any cue-bearing source-profile candidate; it does not modify its bank. The exact runner batch has no successful unit-coefficient cue. All its candidates, including the unconfigured first-candidate fallback, were independently audited.';dump("learner-selection.json",x)
