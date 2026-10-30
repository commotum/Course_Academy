import json,re,sys,collections,hashlib
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path('/home/jake/Developer/Course_Academy');A=ROOT/'reference/edb-math/audits/2026-10-30-latex-quality/topic-17592186048780';D=ROOT/'reference/edb-math/repairs/2026-10-30-vector-topic-latex/topic-17592186048780'
E=json.loads((A/'entities.json').read_text());F=json.loads((A/'fields.json').read_text());proofs=json.loads((D/'source-proofs.json').read_text());old_candidates=json.loads((A/'findings.json').read_text())['findings'][1]['fields'];candidate_keys={(f['entity'],f['attribute'])for f in old_candidates}
p=Path('/home/jake/Developer/MA/DATA/Lessons/1106/Source/1106.html');s=BeautifulSoup(p.read_text(),'html.parser');n=s.select_one('#question-42659');proofs['17592186097240']={'path':str(p),'selector':'#question-42659','bold_vector_letters':sorted({x.get_text()for x in n.select('[mathvariant=bold]')if re.fullmatch('[a-z]',x.get_text())}),'raw_html_sha256':hashlib.sha256(str(n).encode()).hexdigest()};(D/'source-question-42659.html').write_text(str(n))

# Exact source-text matches are unavailable for these retained variants. Their
# labeled arrow diagrams and existing defining vector equalities prove the roles.
diagram_proofs=json.loads((D/'remaining-diagram-proof.json').read_text())
for dp in diagram_proofs:
 i=str(dp['question']);q=E[i]
 if i in proofs:continue
 letters={'17592186302111':['d','e'],'17592186302117':['k','z'],'17592186302118':['a','q'],'17592186302257':['r','a','b']}.get(i,['a','b','c'] if 'c='in q[':question/problem'] else ['a','b'])
 proofs[i]={'proof_type':'mathematical-role-and-diagram','path':'reference/edb-math/audits/2026-10-30-latex-quality/topic-17592186048780/entities.json','question':int(i),'basis':11863,'vector_letters':letters,'source_diagram':dp['source_diagram'],'visual_review':'remaining-source-diagrams.png','role_evidence':q[':question/problem'],'source_text_match':False,'justification':'Diagram labels denote directed arrows. In the ratio items, the existing origin-to-point vector equalities define the lowercase vector names. In grid items, the named arrow vectors are combined with scalar lambda/mu; lowercase vector names are distinct from uppercase point labels. Only these named vector symbols are styled; scalar parameters remain ordinary.'}

# All author answer entities inherit the vector symbol roles of their owning source question.
owner={}
for e in E.values():
 if ':question/id'not in e:continue
 owner[e[':db/id']]=e[':db/id']
 for af in e.get(':question/answer-fields',[]):
  for av in af.get(':answer-field/choices',[])+[af.get(':answer-field/correct',{})]:
   if ':db/id'in av:owner[av[':db/id']]=e[':db/id']
mathpat=re.compile(r'\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)[^$]*?(?<!\\)\$')
token=re.compile(r'\\(?:begin|end|text|mathrm|mathbf|mathit|mathbb|operatorname)\{[^{}]*\}|\\[A-Za-z]+|\\.|[a-z]')
def style_math(body,letters):
 body=re.sub(r'([A-Z]{2})\^\(→\)',lambda m:r'\overrightarrow{'+m[1]+'}',body)
 body=re.sub(r'([A-Z]{2})\^\(―\)',lambda m:r'\overline{'+m[1]+'}',body)
 body=re.sub(r'\\overset\{―\}\{([A-Z]{2})\}',lambda m:r'\overline{'+m[1]+'}',body)
 return token.sub(lambda m:r'\mathbf{'+m[0]+'}'if len(m[0])==1 and m[0]in letters else m[0],body)
def inverse(s):return re.sub(r'\\mathbf\{([a-z])\}',r'\1',s)
changes=[];unresolved=[]
for f in F:
 key=f['entity'],f['attribute']
 if key not in candidate_keys:continue
 oq=owner[f['entity']];proof=proofs.get(str(oq));before=f['value'];letters=set(proof.get('vector_letters',proof.get('bold_vector_letters',[])))if proof else set()
 if not proof:
  unresolved.append({'entity':f['entity'],'attribute':f['attribute'][1:],'reason':'No matching preserved source MathML found yet; vector-font convention left unchanged.','question':oq});continue
 if not letters:
  unresolved.append({'entity':f['entity'],'attribute':f['attribute'][1:],'reason':'Matched source lacks bold-vector metadata; leave unchanged.','question':oq});continue
 after=style_math(before,letters)if f.get('bare_math')else mathpat.sub(lambda m:style_math(m[0],letters),before)
 if after==before:continue
 # Reverse only permitted typography/accents and ensure every other character is identical.
 def unaccent(t):
  t=re.sub(r'\\overrightarrow\{([A-Z]{2})\}',lambda m:m[1]+'^(→)'if m[1]+'^(→)'in before else m[0],t)
  t=re.sub(r'\\overline\{([A-Z]{2})\}',lambda m:m[1]+'^(―)'if m[1]+'^(―)'in before else r'\overset{―}{'+m[1]+'}',t)
  return t
 # Existing bold content is unchanged; comparison strips it on both sides.
 assert inverse(unaccent(after))==inverse(before),(f['entity'],f['attribute'])
 changes.append({'entity':f['entity'],'attribute':f['attribute'][1:],'before':before,'after':after,'reason':('Style unambiguously named vectors using mathematical-role and diagram evidence'if proof.get('proof_type')=='mathematical-role-and-diagram'else 'Restore source MathML bold vector symbols')+('; restore proper vector/segment accent grouping'if '^(→)'in before or '^(―)'in before or '\\overset{―}'in before else ''),'source_evidence':proof})
(D/'source-proofs.json').write_text(json.dumps(proofs,indent=2)+'\n');(D/'changes.json').write_text(json.dumps(changes,indent=2)+'\n');(D/'unresolved.json').write_text(json.dumps(unresolved,indent=2)+'\n')
fields=[dict(f,value=next(c['after']for c in changes if c['entity']==f['entity']and ':'+c['attribute']==f['attribute']))for f in F if any(c['entity']==f['entity']and ':'+c['attribute']==f['attribute']for c in changes)]
(D/'proposed-fields.json').write_text(json.dumps(fields,indent=2)+'\n');print('changes',len(changes),'unresolved',len(unresolved),'questions source matched',len(proofs),'attributes',dict(collections.Counter(c['attribute']for c in changes)))
