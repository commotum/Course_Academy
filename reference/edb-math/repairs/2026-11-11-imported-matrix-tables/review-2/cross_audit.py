#!/usr/bin/env python3
"""Independent token/patch QA of peer proposals; no DB access or peer edits."""
from pathlib import Path
import collections,html,json,re,sys
from bs4 import BeautifulSoup
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
ROOT=next(p for p in HERE.parents if (p/'scripts/question_capture/math_format.py').exists());sys.path.insert(0,str(ROOT))
from scripts.question_capture.math_format import MATH,validate_prose
MARKER=re.compile(r'\{\{(?:answer-field:)?field-\d+\}\}')
def inventory(s):
 out=[]
 for m in MATH.finditer(html.unescape(s)):
  t=m[0];t=t[2:-2] if t.startswith(('$$',r'\(',r'\[')) else t[1:-1];out.append(t.strip())
 return collections.Counter(out)
def norm(s):return s.replace('[','').replace(']','')
results={};families=[]
for shard in ['review-1','review-3']:
 ps=json.loads((BASE/shard/'proposals.json').read_text());rs=json.loads((BASE/shard/'reviews.json').read_text());aa=json.loads((BASE/shard/'assigned.json').read_text());rm={r['candidate_index']:r for r in rs}
 counts=collections.Counter();exceptions=[]
 for pr in ps:
  counts['proposal_fields_checked']+=1
  a=inventory(pr['before']);b=inventory(pr['after']);lost=a-b;gain=b-a
  if lost or gain:
   duplicates=pr.get('duplicate_import_artifact_candidates',[])
   if duplicates:
    expected=collections.Counter();removed_markers=collections.Counter()
    for idx in duplicates:
     ev=rm[idx]['evidence']['duplicate_import_artifact'];assert ev['complete_operands_first_copy']==ev['complete_operands_second_copy']
     for op in ev['complete_operands_first_copy']:
      expected[op['label']]+=1
      for val in op['cells']:
       if MARKER.fullmatch(val):removed_markers[val]+=1
       else:expected[val]+=1
    assert lost==expected and not gain
    assert collections.Counter(MARKER.findall(pr['before']))==collections.Counter(MARKER.findall(pr['after']))+removed_markers
    kind='exact_repeated_complete_SVD_operands_collapsed';counts['duplicate_fields_checked']+=1
   elif lost:
    # Only literal fence characters move into external CSS brackets.
    na=collections.Counter();nb=collections.Counter()
    for k,v in a.items():
     if norm(k):na[norm(k)]+=v
    for k,v in b.items():
     if norm(k):nb[norm(k)]+=v
    assert na==nb,(shard,pr['entity'],lost,gain)
    kind='Newton_literal_fences_replaced_by_CSS';counts['Newton_fence_fields_checked']+=1
   else:
    assert gain==collections.Counter({'.':1})
    assert any(re.search(r'(?:>|\|)\s*\.\s*(?:<|\|)',patch['before']) for patch in pr['replacements'])
    kind='original_ordinary_period_delimited_as_math';counts['period_fields_checked']+=1
   exceptions.append({'entity':pr['entity'],'attribute':pr['attribute'],'candidate_indices':pr['candidate_indices'],'kind':kind,'math_inventory_removed':dict(lost),'math_inventory_added':dict(gain)})
  if not pr.get('duplicate_import_artifact_candidates'):
   assert collections.Counter(MARKER.findall(pr['before']))==collections.Counter(MARKER.findall(pr['after']))
  after=pr['before'];last=-1
  for patch in sorted(pr['replacements'],key=lambda x:x['start']):
   assert patch['start']>=last;last=patch['end'];assert pr['before'][patch['start']:patch['end']]==patch['before']
  for patch in sorted(pr['replacements'],key=lambda x:x['start'],reverse=True):after=after[:patch['start']]+patch['after']+after[patch['end']:]
  assert after==pr['after'];validate_prose(after)
  for patch in pr['replacements']:
   for m in MATH.finditer(patch['after']):assert not MARKER.search(m[0])
   soup=BeautifulSoup(patch['after'],'html.parser')
   for tb in soup.select('.matrix-answer-brackets > table'):
    widths={len(row.find_all('td',recursive=False)) for row in tb.find_all('tr')};assert len(widths)==1 and 0 not in widths
    assert all(td.get_text(strip=True) for td in tb.find_all('td'));counts['rectangular_nonempty_grids_checked']+=1
  counts['patch_replay_prose_and_marker_checks_passed']+=1
 d=collections.defaultdict(list)
 for x in aa:
  if rm[x['candidate_index']]['status']=='confirmed':d[tuple(x['titles'])].append(x['candidate_index'])
 for titles,ids in d.items():families.append({'shard':shard,'titles':titles,'confirmed_candidate_count':len(ids),'candidate_indices':ids})
 counts['confirmed_census_candidates']=sum(r['status']=='confirmed' for r in rs)
 results[shard]={'counts':dict(counts),'expected_inventory_changes':exceptions}
manual=[
 {'family':'SVD independent columns, intermediate vectors and Gram-Schmidt scalars','candidates':[261,268,267,276,285,632,637,643,660,662,664,665,672,724],'conclusion':'Stored preceding derivations identify 3x1 columns u1/u2/u3 and scaled c2. All three duplicate cases contain two exactly identical complete labeled operand pairs with identical field keys and constants; one pair preserves the intended two columns. Nested HTML cases remain two distinct 3x1 operands. Current source steps 32049 and 32872 establish these dimensions and normalization/orthogonalization roles; historical values are retained from storage.'},
 {'family':'Newton optimization equations and iterate vectors','candidates':[119,120,121,693,694,695,696,697,698,699,700],'conclusion':'Rowspanned [, ](x1-x0)=[, and ] are fences/operators, leaving a 2x2 matrix and 2x1 RHS. Lower-row entries remain in those respective operands. Iterate answers remain 2x1. Source 5377 raw cells confirm spanning fences; inventory normalization removes only literal fence characters.'},
 {'family':'Integral IVP formula','candidates':[140,141,617,618,631],'conclusion':'Source 6691 question 334540 has rowspanned x(t)=, integral sign and ds surrounding two separate 2x1 groups. The first lower component and zero integrand component remain under their respective top entries.'},
 {'family':'Variation-of-parameters two equalities','candidates':[103,104,230,231,232,233,247,248,352,353,357,380],'conclusion':'Raw source 3187 question 330893 shows a first bracketed 2x1 vector, a rowspanned comma, a second rowspanned xp(t)= label and second bracketed vector. Proposed groups preserve -10 exp(-2t), supplied 2 and both component fields.'},
 {'family':'ODE coefficient matrix plus forcing vector','candidates':[93,101,102,197,198,199,200,304,383,384,390],'conclusion':'Stored ODE intent requires a 2x2 coefficient matrix before x(t) and a 2x1 forcing vector afterward. Raw source 3189 question 329266 independently confirms that the x(t)+exp(3t) label spans rows and separates the bracket groups.'},
 {'family':'Scalar answer control before particular-solution vector','candidates':[100,201,202,278,381,570,614,615,616,636,648,671,677],'conclusion':'The scalar field remains before the multiplication dot and outside the 2x1 bracketed vector. Component control remains inside its original vector row. No replacement puts a field marker inside TeX.'},
 {'family':'Centered labels in diagonal/Jordan matrix functions and transformation matrices','candidates':[94,95,97,165,166,167,168,169,354],'conclusion':'Jordan source 2927 question 252926 centers its label using rowspan=2 across the middle two physical rows; four populated rows give a 4x4 matrix. Other centered labels similarly do not add matrix rows. Transformation T label-only rows disappear while their two populated rows form 2x2. Matrix-power signs -1, 1, 11, -3 remain in original 3x3 cells.'},
 {'family':'Fundamental/matrix exponentials and unit-vector scalar factors','candidates':[204,207,246,400,131,132,133,143,144,174],'conclusion':'Label-carried 1/2, 1/5 and exponential prefactors remain outside their matrices. Given normalized vector components remain in the correct first/second/third rows. Full math-token inventories cover every variant, including negative coefficients.'},
 {'family':'Linearized system right multiplication and derivative/gradient/transposition grids','candidates':[134,135,124,125,126,127,455],'conclusion':'The trailing u multiplier remains after the 2x2 Jacobian and its definition stays ordinary prose. Derivative/gradient labels are separated from their nonempty supplied-entry rows; U transpose retains its two rows and three columns. All expression inventories and row-major table cells remain intact.'}
]
output={'reviewer':'review-2 independent peer QA','basis':14371,'result':'pass','defects':[],'proposal_fields_checked':sum(r['counts']['proposal_fields_checked'] for r in results.values()),'confirmed_census_candidates_checked':sum(r['counts']['confirmed_census_candidates'] for r in results.values()),'rectangular_nonempty_replacement_grids_checked':sum(r['counts']['rectangular_nonempty_grids_checked'] for r in results.values()),'mechanical_checks':results,'family_inventory':families,'manual_risky_family_conclusions':manual,'source_files_independently_opened':['5377/Source/5377.html','6378/Source/6378.html','6691/Source/6691.html','3187/Source/3187.html','3189/Source/3189.html','2927/Source/2927.html','3133/Source/3133.json'],'limitations':'Current MA snapshots do not contain all historical free-response variants. Family evidence is used only for intent/dimensions; supplied entries and field positions are assessed from stored content. No DB writes or peer-file edits.'}
(BASE/'cross-review.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:output[k] for k in ['result','proposal_fields_checked','confirmed_census_candidates_checked','rectangular_nonempty_replacement_grids_checked','defects']},indent=2))
