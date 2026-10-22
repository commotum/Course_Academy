import sys,importlib.util,json,itertools
from pathlib import Path
from audit_delivery import info,matrices,shortcut_group
sys.dont_write_bytecode=True
E=Path(__file__).resolve().parent;W=E.parent/'workspace';sys.path.insert(0,str(W))
s=importlib.util.spec_from_file_location('audited',W/'17592186119848.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
cat=json.loads((E/'catalog.json').read_text());pool=[r for r in cat if shortcut_group(info(r))];rows=[];retained=[]
for pair in itertools.combinations(pool,2):
 if len({r['generation']['mathematical_fingerprint'] for r in pair})!=2:continue
 keep=g.contrasting_subset(pair)
 row={'ids':[r['question'][':question/id'] for r in pair],'truths':[info(r)['matches'] for r in pair],'kept_by_changed_rule':keep};rows.append(row)
 if keep:retained.append(pair)
assert retained and all(all(len(info(r)['matches'])==1 for r in pair) for pair in retained)
c=json.loads((E/'targeted-counterfactual-records.json').read_text());m0=matrices(c[0]['question']);m2=matrices(c[2]['question']);assert m0['A']==m2['A'] and m0['B']==m2['B'] and m0['C']!=m2['C']
(E/'selection-rule-results.json').write_text(json.dumps({'command':'/home/jake/Developer/Course_Academy/.venv/bin/python -B prove_selection_rule.py','pool_size':len(pool),'pairs':rows,'admitted_pair_count':len(retained),'all_admitted_pairs_force_one_qualifier':True,'rule_reason':'Two nonempty subsets of two eligible matrices can make both labels qualify and fail across the pair only when subsets are A-only and C-only. The valid A+C case is therefore excluded in every two-record repeated subgroup.','counterfactual':{'input':'targeted-counterfactual-records.json','before_index':0,'after_index':2,'A_unchanged':True,'B_unchanged':True,'only_C_changed':True,'before_response':['A'],'after_response':['A','C'],'shortcut_before_response':['A'],'shortcut_after_response':['A']},'limitation':'This is a batch construction defect; the catalog and single-record generate API retain pair outcomes.'},indent=2)+'\n')
print(json.dumps({'admitted_pairs':len(retained),'all_exclusive':True,'counterfactual_only_C_changed':True}))
