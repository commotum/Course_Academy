import json
from pathlib import Path
D=Path(__file__).resolve().parent;s=json.loads((D/'source.json').read_text());t=json.loads((D/'templates.json').read_text())
rows=[];profiles=[]
for q in s['record'][':knowledge-point/questions']:
 mid=q[':question/math-academy-id'];fields=q.get(':question/answer-fields',[]);level=q.get(':question/difficulty',{}).get(':db/ident','unrated').split('/')[-1]
 if mid in t: status='complete validated replay profile'
 elif mid=='q-113958':status='missing fields; rated mathematical basis for explicitly authored hard radio extension'
 elif mid in ('q-143522','q-167569'):status='undefined v(t) in prompt; exclude from available and generation despite complete blank field'
 elif mid=='q-71666':status='malformed csc in two distractors (missing argument); exclude entire profile; preserve source'
 else:status='incomplete field/correct/solution or unrated; exclude'
 rows.append({'source_id':mid,'db_id':q[':db/id'],'difficulty':level,'problem':q[':question/problem'],'solution':q.get(':question/worked-solution'),'field_keys':[f.get(':answer-field/key') for f in fields],'field_types':[f[':answer-field/type'][':db/ident'] for f in fields],'status':status,'plot_rating':'none'})
 for f in fields:
  vals=f.get(':answer-field/choices',[])
  for a in vals:
   recipe=None
   if mid in t:
    i=next(i for i,v in enumerate([v.replace('{a}',str(t[mid]['parameters'].get('a',''))).replace('{b}',str(t[mid]['parameters'].get('b',''))) for v in t[mid]['choices']]) if v==a[':answer/value'])
    recipe=t[mid]['choices'][i]
   profiles.append({'source':mid,'source_field':f.get(':answer-field/key'),'field_id':f[':answer-field/id'],'answer_id':a[':answer/id'],'value':a[':answer/value'],'recipe':recipe or a[':answer/value'],'recipe_scope':'parameterized complete bank' if mid in t else 'literal observed source only; excluded from generation','correct':a[':answer/id']==f.get(':answer-field/correct',{}).get(':answer/id'),'reproduces_complete_value':True})
(D/'classification.json').write_text(json.dumps({'basis':s['basis'],'lineage':s['lineage'],'questions':rows,'source_bank_profiles':profiles},indent=2)+'\n')
(D/'classification.md').write_text('''# Integrating Cosecant Squared

Captured math basis 1872, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. The complete scoped EDB read and native inventory are in reference/initial; source.json preserves all 13 practice sources and canonical e-385. No generator or supplied generated file existed at capture. Native inventory reported easy above threshold, moderate 2 available and hard 0. Final mathematical validation and current inventory are rechecked under api.lock.

Easy: three radio profiles in two mathematical prompt families (positive scalar and negative scalar); the unit negative layout is a separate singleton bank. Two blank sources contain undefined v(t), and the rational negative coefficient source has no fields. Moderate: two radio families (factored csc times a sum, and sine minus csc squared); only the first is usable because q-71666 has argument-free csc distractors. A third moderate source has no fields. Hard: one rated three-term sum with no fields. Unrated: two radio banks without correct designation or solutions. All templates have plot rating none; no image references or new plots exist.

classification.json identifies every source, field type and layout, exact prompt, fixed solution, original choice, complete bank profile and recipe. Source values and IDs remain unchanged. The canonical example supports expansion/linearity but is excluded from practice and novelty. No missing records or assets were guessed.
''')
(D/'template-extraction.md').write_text('''# Source templates and authored extension

The original per-question observations and every choice-to-field mapping are in classification.json; source.json retains exact complete source records. templates.json records fixed prose, expressions, signs, variable roles, optional unit coefficient rendering, ordered solution stages and observed parameter values.

q-113947: positive 5 csc²(theta), radio. Recall primitive, pull coefficient out, substitute -cot, simplify. Complete bank: -a csc cot, a sec tan, -a cot (correct), -a tan, a cot. q-71663: negative 3 csc²(y), radio, same three calculation stages. Bank: a tan, a cot (correct), -a tan, -a cot, a csc cot. q-71664: negative unit csc²(y), different bank sec tan, tan, -tan, cot (correct), -cot; exact singleton replay only. These banks remain separate rather than pooling recipes.

q-49121: csc(x)(3 cot(x)+2 csc(x)), radio. Two recalled primitives, expansion, split sum, pull coefficients, substitute, simplify. Bank: -a csc-b cot (correct); -b cos+b tan; a csc-b sec; -a csc-b tan; a sin³-b cot. The fixed exponent 3 is retained separately from coefficient a. These are observed expression patterns; interpretations of the compound errors are unresolved. Every full original value and correct designation replays exactly. Proposed finite parameter bounds: positive integers 1..9; q-71663 a=2..9 preserves its nonunit layout. The observed signs and variables are retained. Different coefficients change the exact integral; variable names, order, profile and seed never establish novelty.

Hard authored extension: rated q-113958 contains sec(x)tan(x)-2 csc²(x)+sin(x) and its complete solution, but has no answer field. Under generate/principles.md, a new radio response follows the existing KP radio convention; this is not a claim of original bank fidelity. Extend positive coefficients a,b,c in 1..9, preserving three recall formulas, split/signed linearity, substitution and simplification. Correct primitive is a sec+b cot-c cos+C. The authored complete five-option bank has the correct value, individual sign flips of each of its three terms, and simultaneous sign flips of all terms. All distractors are differentiated and proven incorrect and inequivalent. The original hard prompt replays at (1,2,1); its calculation block is exact. Repair only the missing x in the source recall integral of sin, supported by the prompt, calculation and derivative of -cos(x). The original source remains unchanged.

Domains: real connected intervals excluding zeros of sin(x) and, when sec appears, cos(x); C arbitrary. No poles are crossed, no new arguments, chain rule, branches or prerequisite skill are added. Easy, moderate and hard retain respectively one, two and three primitive terms or expansion stages at their observed ratings. All plots are none; plot extraction and generation are inapplicable.

Incomplete q-2037 and q-49093 retain literal full banks but are unrated and lack correct/solution data. q-113948 and q-113952 lack fields. q-143522 and q-167569 have complete blank fields but no definition of v(t), so generated variants cannot faithfully reproduce a self-contained question. q-71666 has two incomplete mathematical choices (-csc+5tan(x)+C and csc-5tan(x)+C); exclude rather than silently invent their arguments. All exclusions remain visible and source records are preserved.
''')
cap={'knowledgePoint':17592186064181,'source_basis':s['basis'],'lineage':s['lineage'],'supported_levels':['easy','moderate','hard'],'unsupported_levels':[],'sampling_bounds':'positive coefficient magnitudes 1..9; negative nonunit easy 2..9; unit negative singleton replay only','finite_distinct_task_domain':{'easy_new_sampling':17,'easy_with_replay':18,'moderate':81,'hard':729},'exceptions':[{'kind':'authored-extension','level':'hard','source':'q-113958','reason':'Rated prompt/solution have no fields. Explicitly authored five-option radio bank; no original answer-bank fidelity claim. Missing x in recall formula repaired in new content only.'},{'kind':'incomplete-source','profiles':['q-2037','q-49093','q-113948','q-113952','q-143522','q-167569'],'reason':'Unrated/missing fields, correct or solution, or undefined v(t). Original records preserved and excluded.'},{'kind':'malformed-source-bank','profile':'q-71666','reason':'Two distractors lack the argument of csc. Excluded; no invented source interpretation.'},{'kind':'finite-profile','profile':'q-71664','variant_limit':1,'reason':'Distinct source bank retained as exact singleton; not new sampling.'}], 'unsupported_levels_filled':False}
(D/'capabilities.json').write_text(json.dumps(cap,indent=2)+'\n')
(D/'README.md').write_text('''# KP 17592186064181 generator

Run the repository Python environment with ../17592186064181.py --difficulty hard --count 5 --seed 1 --format json. Easy and moderate are supported too; unsupported levels fail and bounded batches never pad. Run validate.py for full source-bank replay, exact derivative and ordered solution-step checks over all finite parameters, deterministic identity tests and actual native radio grading. Hard is an explicit authored bank extension grounded in the rated three-term source, not a recovered original bank.

replenish.py rechecks native inventory plus conservative gradable mathematical tasks, excluding retained presentations and reservations. It holds the application api.lock through preparation, deployed-spec preview, basis-guarded durable submission, exact receipt readback and inventory recheck. Requests and receipts remain in reference/replenishment. All source and learner history are preserved; only this KP receives additive generated content and generator registration.
''')
