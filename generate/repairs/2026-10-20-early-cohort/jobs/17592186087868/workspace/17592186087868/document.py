import importlib.util,json
from pathlib import Path
H=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('g',H.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
rows=[]
for mid,q in g.SOURCES.items():
 eq=g.prompt_equations(q)
 rows.append({'source_question':mid,'db_id':q[':db/id'],'difficulty':g.level(q),'template':mid,'plot_rating':'none','observed_k':1,'components':{'problem':q[':question/problem'],'worked_solution':q[':question/worked-solution'],'normalized_equations':[{'key':key,'P':str(p),'Q':str(v),'homogeneous':v==0} for key,(p,v) in eq]},'fields':[{'key':f[':answer-field/key'],'type':'checkbox','profile':'true-false','source_field_id':f[':answer-field/id'],'choices':[{'source_answer_id':a[':answer/id'],'value':a[':answer/value'],'recipe':'Literal '+a[':answer/value'],'reproduces_original':True} for a in f[':answer-field/choices']],'correct':f[':answer-field/correct'][':answer/value']} for f in q[':question/answer-fields']]})
(H/'classification.json').write_text(json.dumps({'basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'knowledge_point':g.KP_ID,'levels':{'easy':{'sources':6,'templates':6,'field_types':['checkbox','checkbox','checkbox']},'moderate':{'sources':6,'templates':6,'field_types':['checkbox','checkbox','checkbox']},'hard':{'sources':0,'templates':0,'status':'unsupported in this bounded package'}},'templates':rows},indent=2))
(H/'classification.md').write_text(f'''# Classification at basis {g.SOURCE['basis']}

KP {g.KP_ID}: {g.TITLE}. All twelve practice records have complete three-field checkbox banks. Six are easy (select homogeneous); six moderate (select inhomogeneous). Each field has text false/true choices and its own correct answer. No blank, mixed-type or missing fields occur. The canonical example supports the definitions but has no practice fields and is excluded from inventory.

Retain six source-layout templates at each observed level, rather than merging different equation order, constant/polynomial forcing, coefficient signs, rearrangement wording and solution grouping. Every source maps to its own template in classification.json. Each has one profile: three separate true/false banks. No unmapped choice recipes or unresolved mathematical errors occur. All plots: none; source Markdown contains no assets and no new diagrams are needed.

No hard-rated question exists in the captured KP. Hard is unsupported by this generator version, not declared mathematically impossible. New source evidence must reopen classification.
''')
(H/'template-extraction.md').write_text('''# Template extraction

Every source's specific prompt, equation objects, field layout, complete choices and solution are retained in source.json/source.edn and classification.json. The shared move is to collect all y-terms on the left, then check whether Q(x) is identically zero. A forcing monomial that vanishes at a single x is still inhomogeneous.

Each source question is its own reusable Markdown/value template. Fixed: all original instructional sentences, equation/solution ordering, y-prime coefficient 1, boolean field keys I/II/III and all observed constants and signs. Variable: each explicit x monomial's degree d becomes d*k, k in integers 1..6. P(x)/Q(x) remain arbitrary-function notation. At k=1, the complete Markdown and worked solution replay exactly. Higher k is an explicit sampling extension, not an observed range. There is no coefficient sampling that might invalidate a sign or produce zero forcing. Every coefficient and every rearranged intermediate in the solution receives the same substitution. Since powers are nonnegative integers this preserves real polynomial domains and first-order linear form; the zero/nonzero-forcing distinction is unchanged.

Choice recipes are literal text false/true, separately owned by each checkbox field. Correct selection is computed after symbolic collection of y-terms. There are no imported distractor explanations. Full bank replay compares both values, their types and correct designation for every field of every original; no pooling of choices or mixed-profile banks occurs.

All original numeric coefficients, signs, degrees and constant/polynomial forcing forms are covered at k=1. Samples with k=2..6 extend degrees only. Different source solution sequences remain separate. Identity hashes the unordered set of normalized complete ODEs; neither equation ordering, seed nor response-choice ordering creates a new task. Source examples and all current KP members are excluded from generated commits by that same mathematical key.

Validation exhausts every template and k, checks every rendered numeric ODE in the worked solutions for equivalence with a prompt equation, verifies all selection values and summary text, and invokes the application learner grader for every checkbox field's correct and incorrect authored choice. Original/variant pairs are in review.md.
''')
(H/'plot-extraction.md').write_text('# Plot extraction\n\nNo source image, plot or diagram references occur. Rating none for all twelve templates. No generated assets or publishing requests. LaTeX equations are mathematical notation, not plots.\n')
caps={'supported_levels':['easy','moderate'],'finite_policy':{'k':list(g.DOMAIN),'source_templates':12,'unique_tasks_by_level':{l:len(g.candidates(l)) for l in g.SUPPORTED_LEVELS}},'exceptions':[{'difficulty':'hard','status':'unsupported','bounded_scope':'this generator version','evidence':'All 12 source practice questions at basis '+str(g.SOURCE['basis'])+' are rated easy or moderate. No source-backed hard layout/bank or distinct harder operation is available. Increasing polynomial degree preserves classification method and does not justify relabeling it hard.','nominal_shortage':5,'filled':False,'reopen_on':'New rated source evidence or separately reviewed hard template'}]}
(H/'capabilities.json').write_text(json.dumps(caps,indent=2))
