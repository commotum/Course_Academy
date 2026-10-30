import collections,json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path[:0]=[str(R/'scripts'),str(R/'reference/edb-math/repairs/2026-10-26-mixed-math-titles')]
from reconstruct import SourceRenderer
from question_capture.math_format import MATH,matrix_answer,matrix_equation,normalize_tex
S=json.loads((H/'current.json').read_text());sources=json.loads((H/'source-inventory.json').read_text());proposals=[];evidence=[];failed=[]
def value(cell):
 text=SourceRenderer(None).text(cell,True).strip()
 if re.fullmatch(r'\{\{field-\d+\}\}',text):return text
 spans=list(MATH.finditer(text));assert len(spans)==1 and spans[0][0]==text,repr(text)
 edge=2 if text.startswith(('$$',r'\(',r'\['))else 1
 return text[edge:-edge].strip()
for q in S['questions']:
 fs=q.get(':question/answer-fields',[])
 if 'Find the values of $a' in q[':question/problem']:continue
 if not fs or not all(f[':answer-field/type'][':db/ident']==':answer-field.type/blank'for f in fs):continue
 mid=q[':question/math-academy-id'];options=[]
 for src in [r for r in sources if r['identity']==mid and r['attribute']=='question/problem']:
  try:
   raw=json.loads(Path(src['path']).read_text());node=BeautifulSoup(src['html'],'html.parser');keys=[]
   for field in raw.get('fields',[]):
    control=node.find(id=field.get('dom_id'))
    if field.get('type')=='blank'and control is not None:control.replace_with('{{'+field['key']+'}}');keys.append(field['key'])
   assert set(keys)=={f[':answer-field/key']for f in fs},keys
   tables=[t for t in node.find_all('table')if not t.find('table')];grids=[];labels=[]
   for table in tables:
    if len(table.find_all('tr'))<2:continue
    rows=[];label=None
    for i,tr in enumerate(table.find_all('tr')):
     cs=tr.find_all(['td','th'],recursive=False)
     if i==0 and cs[0].has_attr('rowspan'):label=value(cs.pop(0))
     assert not cs[0].get_text(strip=True)and not cs[-1].get_text(strip=True)
     rows.append([value(c)for c in cs[1:-1]])
    grids.append(rows);labels.append(label)
   inverse='Find the inverse'in q[':question/problem']
   if inverse:
    assert len(grids)==1 and len(grids[0])==4 and all(len(r)==4 for r in grids[0]);label=labels[0];assert label;label=re.sub(r'=.*$','',label).strip();replacement=matrix_answer(label,grids[0]);cut=q[':question/problem'].index('$$',q[':question/problem'].index('$$')+2)+2;new=q[':question/problem'][:cut]+'\n\n'+replacement
   else:
    assert len(grids)==2 and len(grids[0])==2 and len(grids[0][0])==2 and len(grids[1][0])==1
    matrixkeys=set(re.findall(r'\{\{([^{}]+)\}\}',str(grids)));outside=set(keys)-matrixkeys;assert len(outside)==1;scalar='{{'+outside.pop()+'}}';replacement=matrix_equation([r'\mathbf{x}=',scalar,*grids]);replacement=replacement.replace('$'+scalar+'$',scalar)
    phrase='can be represented using matrix notation as';assert phrase in q[':question/problem'];cut=q[':question/problem'].index(phrase)+len(phrase);new=q[':question/problem'][:cut]+'\n\n'+replacement
   assert collections.Counter(re.findall(r'\{\{([^{}]+)\}\}',new))==collections.Counter(keys)
   options.append({'path':src['path'],'after':new,'grids':grids,'source_label':labels,'fields':keys})
  except Exception as e:failed.append({'question':q[':db/id'],'path':src['path'],'error':str(e)})
 if not options:print('NO OPTIONS',q[':db/id']);continue
 assert len({r['after']for r in options})==1,(mid,'sources differ');o=options[0]
 if o['after']!=q[':question/problem']:proposals.append({'entity':q[':db/id'],'attribute':'question/problem','before':q[':question/problem'],'after':o['after'],'reason':'Restore archived matrix cells, external scalar control and brackets as one responsive equation; preserve control keys and identities.'})
 evidence.append({'entity':q[':db/id'],'identity':mid,**o})
(H/'layout-proposals.json').write_text(json.dumps(proposals,indent=2)+'\n');(H/'layout-evidence.json').write_text(json.dumps({'verified':evidence,'rejected_source_probes':failed},indent=2)+'\n');print('Restored',len(proposals),'layouts;',len(failed),'rejected probes')
