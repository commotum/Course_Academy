import collections,copy,json,re,sys
from pathlib import Path
sys.path.insert(0,'scripts');from question_capture.math_format import MATH,matrix_answer,matrix_tex,validate_math_structure,ENV,environment,cells
H=Path(__file__).resolve().parent;D=json.loads((H/'snapshot.json').read_text());F={(f['entity'],f['attribute']):f for f in json.loads((H/'fields.json').read_text())};S=json.loads((H/'source-records.json').read_text());props={};unresolved=[]
def propose(e,a,after,reason,evidence,confidence='high'):
 before=F[e,a]['value'];assert after!=before;validate_math_structure(after);assert sorted(re.findall(r'\{\{[^{}]+\}\}',before))==sorted(re.findall(r'\{\{[^{}]+\}\}',after))
 props[e,a]={'entity':e,'attribute':a,'before':before,'after':after,'reason':reason,'evidence':evidence,'confidence':confidence}
def replace_formulas(e,a,replacements,reason,evidence):
 text=props.get((e,a),{}).get('after',F[e,a]['value']);matches=list(MATH.finditer(text))
 for i,tex in reversed(sorted(replacements.items())):
  m=matches[i];text=text[:m.start()]+('$$\n'+tex+'\n$$'if m[0].startswith('$$')else'$'+tex+'$')+text[m.end():]
 propose(e,a,text,reason,evidence)
for c in json.loads((H/'source-highlight-candidates.json').read_text()):
 if c['entity']in (17592186642471,17592186602424,17592186101959):continue
 key=(c['entity'],c['attribute'])
 if key in props:assert props[key]['after']==c['after'];continue
 propose(*key,c['after'],c['reason'],c['evidence'])
manual={17592186060935:[10],17592186061006:[2],17592186093403:[9],17592186107082:[2],17592186121022:[6],17592186121024:[0],17592186121046:[3,5],17592186121057:[9]}
for e,indices in manual.items():
 s=next(s for s in S if s['entity']==e and s['attribute']=='tutorial/content');rep={i:s['formulas'][i]for i in indices}
 # Keep determinant an operator when its MathML source spells the literal letters.
 if e in (17592186121022,17592186121024):rep={i:re.sub(r'(?<![A-Za-z\\])det(?=\(|\\begin)',r'\\det',t)for i,t in rep.items()}
 replace_formulas(e,'tutorial/content',rep,'Restore source mathematical roles, instructional highlighting, or the augmented-matrix divider lost during import.',{'path':s['path'],'identity':s['source_identity'],'formula_indices':indices})
# Selected-entry solutions: retain current extracted row/dot-product stages,
# restore the source's grey suppression of unselected operand entries.
kpids={r[2]for r in D['links']if r[1]==17592186100873}
def grids(tex):
 out=[]
 for m in ENV.finditer(tex):
  if m.groups()==('begin','bmatrix'):
   span=environment(tex,m.start());out.append((m.start(),span[2],cells(tex[span[0]:span[1]])))
 return out
def plain(s):return re.sub(r'\s+|[{}]','',re.sub(r'\\color\{[^{}]+\}','',s))
for q in D['questions']:
 e=q[':db/id'];a='question/worked-solution'
 if e not in kpids or ':'+a not in q:continue
 ss=[s for s in S if s['entity']==e and s['attribute']==a];text=q[':'+a];matches=[m for m in MATH.finditer(text)if len(grids(m[0]))>=2];first=matches[0];gs=grids(first[0])[:2];assert len(gs)==2
 target=re.search(r'\{?([a-z])\}?_\{([1-5])([1-5])\}',q[':question/problem']);assert target;letter,i,j=target.groups();i,j=int(i),int(j)
 source_mats=None
 for s in ss:
  for tex in s['formulas']:
   gg=grids(tex)
   if len(gg)>=2 and all([[plain(c)for c in r]for r in x[2]]==[[plain(c)for c in r]for r in y[2]]for x,y in zip(gs,gg))and r'\color'in tex:
    source_mats=[tex[x[0]:x[1]]for x in gg[:2]];evidence={'path':s['path'],'identity':s['source_identity'],'target':[i,j],'source_operand_matrices_match':True};break
  if source_mats:break
 if not source_mats:
  source_mats=[]
  for k,g in enumerate(gs):source_mats.append(matrix_tex([[v if (ri==i-1 if k==0 else ci==j-1)else r'{\color{lightgray}{'+v+'}}'for ci,v in enumerate(row)]for ri,row in enumerate(g[2])]))
  evidence={'question':e,'target':[i,j],'family_source_examples':['e-4407','q-130111'],'source_status':'authored visual completion from indexed row/column; exact source capture absent'}
 newfirst=first[0]
 for g,v in reversed(list(zip(gs,source_mats))):newfirst=newfirst[:g[0]]+v+newfirst[g[1]:]
 after=text[:first.start()]+newfirst+text[first.end():];propose(e,a,after,'Restore the source selected-entry focus while preserving all row/column extraction and dot-product stages.',evidence)
# Tables flattened from source brackets. Read only existing cells/field placeholders.
def unmath(s):return s[1:-1].strip()if s.startswith('$')and s.endswith('$')else s
for q in D['questions']:
 text=q[':question/problem'];e=q[':db/id'];m=re.search(r'(?m)^\|[^\n]+(?:\n\|[^\n]+)+',text)
 if not m:continue
 lines=[line for line in m[0].splitlines()if not re.match(r'^\|\s*---',line)];rows=[[c.strip()for c in line.strip('|').split('|')]for line in lines];ev={'source_identity':q.get(':question/math-academy-id'),'rows':len(rows),'columns':len(rows[0]),'field_order_preserved':True};ss=[s for s in S if s['entity']==e and s['attribute']=='question/problem'];ev['path']=ss[0]['path']if ss else None;ev['source_status']='retained raw table inspected'if ss else'original capture absent; existing full cell grid and system specify matrix role'
 if len(rows)==3 and all(len(r)==15 for r in rows):
  coeff=[[unmath(c)for c in row[2:5]]for row in rows];rhs=[[unmath(row[12])]for row in rows];assert [unmath(row[8])for row in rows]==['x','y','z']
  left=matrix_answer('A',coeff);left=re.sub(r'<span class="matrix-answer-label">.*?</span>\n','',left,count=1)
  right=matrix_answer('b',rhs);right=re.sub(r'<span class="matrix-answer-label">.*?</span>\n','',right,count=1)
  variable=matrix_answer('x',[['x'],['y'],['z']]);variable=re.sub(r'<span class="matrix-answer-label">.*?</span>\n','',variable,count=1)
  unnest=lambda v:v.removeprefix('<div class="matrix-answer">\n').removesuffix('\n</div>')
  replacement='<div class="matrix-answer">\n'+unnest(left)+'\n'+unnest(variable)+'\n<span class="matrix-answer-label">$=$</span>\n'+unnest(right)+('\n<span class="matrix-answer-label">.</span>'if any(row[14]=='.'for row in rows)else'')+'\n</div>'
 elif len(rows)==3 and all(len(r)==4 for r in rows):replacement=matrix_answer('x',[[row[2]]for row in rows])
 else:unresolved.append({'entity':e,'reason':'unrecognized Markdown answer table','rows':rows});continue
 propose(e,'question/problem',text[:m.start()]+replacement+text[m.end():],'Restore matrix brackets and aligned cells lost when the source answer table was flattened into a Markdown table.',ev)
# One retained legacy HTML matrix not in the shared parent's scope.
e=17592186647103;q=next(q for q in D['questions']if q[':db/id']==e);text=q[':question/problem'];m=re.search(r'<table\b[\s\S]*?</table>',text);assert m
replacement=matrix_answer('AB',[['{{field-1}}','{{field-2}}'],['{{field-3}}','{{field-4}}']]);propose(e,'question/problem',text[:m.start()]+replacement+text[m.end():],'Restore bracketed two-row matrix layout from the legacy source table, preserving all field identities.',{'source_identity':q.get(':question/math-academy-id'),'original_capture':'not retained in source index','existing_html_table':'two rows, rowspanned AB label, two editable columns'})
(H/'proposals.json').write_text(json.dumps(list(props.values()),indent=2));(H/'unresolved-layouts.json').write_text(json.dumps(unresolved,indent=2));print('proposals',len(props),collections.Counter(p['attribute']for p in props.values()))
