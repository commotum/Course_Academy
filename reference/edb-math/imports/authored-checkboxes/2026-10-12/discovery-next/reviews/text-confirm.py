import json,re,collections,runpy
from pathlib import Path
BASE=Path('reference/edb-math/imports/authored-checkboxes/2026-10-12/discovery-next');OUT=BASE/'reviews'; f=OUT/'text-cases.json';data=json.load(open(f));LABEL=r'(?:VIII|VII|VI|IV|III|II|IX|X|V|I|[A-Z])';LS=LABEL+r'(?:\s*(?:,\s*(?:and\s+)?|and\s+|&\s*)'+LABEL+r')*'
for q in data['questions']:
 ev=q['key_evidence'];sol=ev['worked_solution'];s=re.sub(r'\*|\$','',sol);U=[a['label']for a in q['atomic_options']];key=set(q['correct_labels']or []);evidence=[];conflict=[]
 # Explicit unquoted final answer.
 for m in re.finditer(r'correct answer is\s*["“‘\']*('+LS+r')(?: only)?',s,re.I):
  ls=re.findall(r'\b'+LABEL+r'\b',m.group(1));
  if set(ls)<=set(U):(evidence if set(ls)==key else conflict).append(m.group(0))
 # Conclusion sentence contains source objects and requested predicate; unique subset follows only/exactly.
 for paragraph in sol.split('\n\n'):
  if not re.search(r'\b(?:therefore|in conclusion|as a result|so, only)\b',paragraph,re.I):continue
  n=re.sub(r'\*|\$','',paragraph)
  m=re.search(r'\bonly\s+(?:(?:statements?|equations?|integrals?|functions?|choices?|options?|matrices|sequence|sequences|series|occurrences?)\s+)?('+LS+r')\b',n,re.I)
  if m:
   ls=re.findall(r'\b'+LABEL+r'\b',m.group(1))
   if set(ls)<=set(U):(evidence if set(ls)==key else conflict).append(paragraph)
  elif re.search(r'\bnone of (?:the |these )?(?:given |listed )?(?:statements?|equations?|integrals?|functions?|matrices|sequence|sequences|series|values|occurrences?)\b',n,re.I):
   (evidence if not key else conflict).append(paragraph)
  elif re.search(r'\ball (?:of )?(?:the |these )?(?:given |listed )?(?:values|statements?|equations?|angles|functions?|matrices|sequence|sequences|series)\b',n,re.I):
   (evidence if key==set(U)else conflict).append(paragraph)
  elif q['classification']=='finite_named_matrices':
   ls=re.findall(r'\b'+LABEL+r'\b',n)
   if ls and set(ls)<=set(U):(evidence if set(ls)==key else conflict).append(paragraph)
 # Per-statement truth verdicts only applicable when prompt asks true/false.
 verdicts=collections.defaultdict(set)
 if re.search(r'which of the following statements are (true|false)',q['source_problem'],re.I):
  requested=bool(re.search(r'statements are true',q['source_problem'],re.I))
  for m in re.finditer(r'\bstatements?\s+('+LS+r')\s+(?:is|are)\s+(true|false)\b',s,re.I):
   if re.search(r'\bnot (?:both |all )?$',s[max(0,m.start()-25):m.start()],re.I):continue
   for l in re.findall(r'\b'+LABEL+r'\b',m.group(1)):verdicts[l].add((m.group(2).lower()=='true')==requested)
  for l,v in verdicts.items():
   if l in U and len(v)==1 and (l in key)not in v:conflict.append('Source verdict '+l+'='+str(list(v)))
  if set(verdicts)==set(U)and all(len(v)==1 for v in verdicts.values()):evidence.append('Complete source statement verdicts: '+str(dict(verdicts)))
 ev['solution_confirmation']+=list(dict.fromkeys(evidence));ev['solution_conflicts']+=list(dict.fromkeys(conflict));q['solution_needs_manual_review']=not ev['solution_confirmation']
 if conflict and q['decision']=='convert':q['decision']='needs_evidence';q['reason']='Worked solution verdict or explicit conclusion conflicts with database key; investigate content separately.';q['proposed_prompt']=q['source_problem']
 if q['ma_id']=='q-31919':q['decision']='retain_radio';q['reason']='One matrix is classified into mutually exclusive invertible/not-invertible/singular alternatives. Keep the single classification response despite combination distractors.';q['proposed_prompt']=q['source_problem']
data['counts']['decisions']=dict(collections.Counter(q['decision']for q in data['questions']));data['counts']['without_formulaic_solution_confirmation']=sum(q['solution_needs_manual_review']for q in data['questions'])
f.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
(OUT/'text-unconfirmed.json').write_text(json.dumps([q for q in data['questions']if q['solution_needs_manual_review']and q['decision']=='convert'],indent=2,ensure_ascii=False)+'\n')
print(json.dumps(data['counts'],indent=2));print('new conflicts',[(q['ma_id'],q['key_evidence']['solution_conflicts'])for q in data['questions']if q['reason'].startswith('Worked solution verdict')])
