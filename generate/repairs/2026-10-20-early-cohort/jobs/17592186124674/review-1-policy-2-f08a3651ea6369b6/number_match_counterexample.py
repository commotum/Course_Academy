import sys,pathlib,importlib.util,json,re,copy,uuid
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;W=E.parent/'workspace'
def save(n,x):(E/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
s=importlib.util.spec_from_file_location('g',W/'17592186124674.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
r=g.generate_easy(seed=3,parameters={'context':'deer','capacity':60});q=r['question'];f=q[':question/answer-fields'][0];a=copy.deepcopy(r);af=a['question'][':question/answer-fields'][0]
# Keep correct model, prompt, solution and workload unchanged. Only let a wrong
# source-supported structural equation share the equilibrium number.
wrong=next(c for c in af[':answer-field/choices'] if c[':answer/value'].split('=')[1].startswith('-k'))
old=wrong[':answer/value'];rhs=old.split('=')[1];wrong[':answer/value']=old.replace(re.search(r'\d+',rhs)[0],'60');assert wrong[':answer/value']!=old
wrong[':answer/id']=str(uuid.uuid5(uuid.NAMESPACE_URL,'review-number-match-wrong:'+wrong[':answer/value']));a['question'][':question/id']=str(uuid.uuid5(uuid.NAMESPACE_URL,'review-number-match-counterfactual'))
a['generation']={'reviewer_authored_counterfactual':True,'not_generator_output':True,'based_on_seed':3,'based_on_parameters':{'context':'deer','capacity':60},'changed':{'before':old,'after':wrong[':answer/value']},'held_fixed':'prompt, solution, correct equation, all other four options','source_basis':'54bac72f-651e-55b5-8b4b-fbc4e753ebc5 uses capacity150 in both correct and wrong structural models'}
save('number-match-counterfactual-records.json',[r,a])
params={'context':'deer','capacity':60,'candidates':[30,45,60,60,95],'target_rank':2,'linear_indices':[0,2,4]}
try:g.generate_easy(seed=3,parameters=params);outcome='accepted'
except ValueError as ex:outcome=str(ex)
save('number-match-role-restriction.json',{'seed':3,'parameters':params,'actual':outcome,'source_supported_reference':'number-match-counterfactual-records.json index1','essential_constraint':'five distinct equations, not five distinct constants; two different sign/factor equations can share capacity, as in source structural banks','change_before':old,'change_after':wrong[':answer/value']})
checks=json.loads((E/'native-grader-input.json').read_text())
for i,rec in enumerate([r,a]):
 ff=rec['question'][':question/answer-fields'][0];checks.append({'label':'new numeral-cue counterexample '+str(i),'record':rec,'checks':[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/id']==ff[':answer-field/correct'][1] else 'rejected','purpose':'Same prompt/equilibrium; wrong structural option can share capacity without becoming correct'} for c in ff[':answer-field/choices']]})
save('native-grader-input.json',checks)
print(json.dumps({'restriction':outcome,'before':old,'after':wrong[':answer/value'],'fixture_count':2}))
