"""Prepare text-only, role-aware import repairs. Never connects to EDB."""
import json,re,collections
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
AUDIT=ROOT/'reference/edb-math/audits/2026-10-30-latex-quality/topic-17592186049485'
snapshot=json.loads((AUDIT/'snapshot.json').read_text())
fields=json.loads((AUDIT/'render-input.json').read_text())
font_proof=json.loads((AUDIT/'vector-formatting-evidence.json').read_text())
direct={(f['entity'],f['attribute']) for f in font_proof['direct_source_confirmed_fields']}
contexts={}
for ki,kp in enumerate(snapshot['kps']):
 for q in [kp[':knowledge-point/canonical-example'],*kp[':knowledge-point/questions']]:
  # Every line equation calls r a position vector and v a direction vector.
  roles={'r','v'}
  if ki in (0,1):
   # A point's lower-case position vector is explicitly identified in prose.
   roles.update(re.findall(r'\$([a-z])\$ is the position vector',q.get(':question/worked-solution','')))
   roles.add('p') if q[':db/id'] in (17592186105463,17592186105464) else None
  elif ki==2:roles.add('p')
  elif ki==3:roles.update(('p','i','j','k'))
  evidence={'knowledge_point':kp[':db/id'],'question':q[':db/id'],'math_academy_id':q.get(':question/math-academy-id'),'vector_symbols':sorted(roles),'basis':11863,
   'role_evidence':('The solution explicitly defines '+','.join(sorted(roles-{'r','v'}))+' as position vector(s); r is the line position vector, v its direction vector.' if ki<2 else 'The line formula r=p+tv identifies r,p,v as vectors.' if ki==2 else 'The line formula identifies r,p,v as vectors; i,j,k are Cartesian basis vectors. Unknown coefficients a,b,c and parameter t remain scalars.')}
  contexts[q[':db/id']]=(roles,evidence)
  for af in q.get(':question/answer-fields',[]):
   for a in af.get(':answer-field/choices',[]):contexts[a[':db/id']]=({'r'},dict(evidence,role_evidence='The answer is a vector equation: r is the position vector. Coordinates and scalar t are unchanged.'))
for eid in (17592186107157,17592186107158,17592186107159):
 contexts[eid]=({'r','p','q','v'},{'tutorial':eid,'basis':11863,'role_evidence':'The tutorial explicitly identifies p,q,r as position vectors and v as direction vector; original tutorial MathML/screenshots preserve bold vector symbols. Parameter t remains scalar.'})

def braced_end(s,start):
 assert s[start]=='{'
 level=1;i=start+1
 while level:
  if s[i]=='\\':i+=2;continue
  if s[i]=='{':level+=1
  if s[i]=='}':level-=1
  i+=1
 return i

def format_math(s,roles):
 out=[];i=0;count=0
 # Commands/styles/environments are tokens, never sequences of variables.
 protected={'mathbf','boldsymbol','mathbfit','mathrm','mathit','mathsf','mathtt','mathcal','mathbb','text','textrm','operatorname','begin','end'}
 while i<len(s):
  if s[i]=='\\':
   m=re.match(r'\\(?:[A-Za-z]+|.)',s[i:]);token=m[0];end=i+len(token)
   if token[1:] in protected:
    j=end
    while j<len(s) and s[j].isspace():j+=1
    if j<len(s) and s[j]=='{':end=braced_end(s,j)
    elif j<len(s):end=j+1
   out.append(s[i:end]);i=end
  elif s[i] in roles:
   out.append('\\mathbf{'+s[i]+'}');count+=1;i+=1
  else:out.append(s[i]);i+=1
 return ''.join(out),count

def math_only(s,roles,bare):
 if bare:return format_math(s,roles)
 out=[];pos=0;count=0
 for m in re.finditer(r'\$\$[\s\S]*?\$\$|(?<!\\)\$(?:\\.|[^$])*?(?<!\\)\$',s):
  n=2 if m[0].startswith('$$') else 1
  value,num=format_math(m[0][n:-n],roles)
  out.extend((s[pos:m.start()],m[0][:n]+value+m[0][-n:]));count+=num;pos=m.end()
 out.append(s[pos:]);return ''.join(out),count

def notation(s):
 # Each overset base is braced, including O{A}_{1}; retain the full base.
 stats=collections.Counter();out=[];pos=0
 pattern=re.compile(r'\\overset\{(\\to\s*|―|\\longleftrightarrow)\}\{')
 for m in pattern.finditer(s):
  if m.start()<pos:continue
  end=braced_end(s,m.end()-1);base=s[m.end():end-1]
  kind='arrow' if m[1].startswith('\\to') else 'segment_bar' if m[1]=='―' else 'line_arrow'
  command={'arrow':'overrightarrow','segment_bar':'overline','line_arrow':'overleftrightarrow'}[kind]
  out.extend((s[pos:m.start()],'\\'+command+'{'+base+'}'));pos=end;stats[kind]+=1
 out.append(s[pos:]);result=''.join(out)
 if 'PQ^(―)' in result:result=result.replace('PQ^(―)',r'\overline{PQ}');stats['malformed_segment']+=1
 return result,stats

def remove_approved_formatting(s):
 # Canonicalize only the approved decorations, then remove vector font wrappers.
 s=notation(s)[0]
 s=re.sub(r'\\mathbf\s*\{([A-Za-z])\}',r'\1',s)
 s=re.sub(r'\\mathbf\s+([A-Za-z])',r'\1',s)
 return s

changes=[];render=[];totals=collections.Counter();unresolved=[]
for f in fields:
 if f['entity'] not in contexts:continue
 roles,evidence=contexts[f['entity']]
 after,font_count=math_only(f['value'],roles,f.get('bare_math',False))
 after,counts=notation(after)
 if after==f['value']:continue
 assert remove_approved_formatting(after)==remove_approved_formatting(f['value']),(f['entity'],f['attribute'])
 assert after.count(r'\pm')==f['value'].count(r'\pm')
 # Source-inherited square-root derivations and all scalar coefficients remain exact.
 evidence=dict(evidence,direct_source_font_confirmation=(f['entity'],f['attribute']) in direct,source_audit=str(AUDIT.relative_to(ROOT)/'vector-formatting-evidence.json'))
 if counts:
  evidence['decoration_evidence']='Original source MathML uses vector displacement arrows and segment overbars; bases are unchanged, including subscripted endpoints. See source-evidence/ original MathML and screenshots.'
 reasons=[]
 if font_count:reasons.append('Restore source vector boldface using explicit local vector/scalar roles')
 if counts.get('arrow'):reasons.append('Use a stretching displacement-vector arrow rather than fixed overset arrow')
 if counts.get('segment_bar'):reasons.append('Restore a segment bar spanning its entire endpoint label')
 if counts.get('line_arrow'):reasons.append('Use a stretching two-headed line arrow')
 if counts.get('malformed_segment'):reasons.append('Replace pseudo-TeX superscript parentheses with the source segment overbar')
 changes.append({'entity':f['entity'],'attribute':f['attribute'],'before':f['value'],'after':after,'reason':'; '.join(reasons),'source_evidence':evidence})
 render.append(dict(f,value=after));totals.update(counts);totals['vector_font_tokens']+=font_count
assert len(changes)==217,len(changes)
candidate_keys={(f['entity'],f['attribute']) for f in font_proof['same_pattern_candidate_fields']}
assert candidate_keys=={(f['entity'],f['attribute']) for f in changes}
for name,value in [('changes.json',changes),('unresolved.json',unresolved),('render-input.json',render),('verification.json',{'basis':11863,'changes':len(changes),'entities':len(set(c['entity'] for c in changes)),'attributes':dict(collections.Counter(c['attribute'] for c in changes)),'decoration_counts':dict(totals),'all217_candidate_fields_resolved':True,'equivalence_after_removing_only_approved_formatting':True,'sqrt_derivation_pm_tokens_preserved':True,'database_writes':0,'missing_fields_added':0,'answer_refs_changed':0})]:
 (HERE/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'fields':len(changes),'counts':dict(totals)}))
