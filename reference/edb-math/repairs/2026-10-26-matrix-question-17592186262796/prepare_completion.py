import copy,hashlib,json,sys,uuid
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'));from migrate_learner_history import dumps,kw
qs=json.loads((H/'questions.json').read_text());byid={q[':db/id']:q for q in qs};opening='For a $2\\times 2$ matrix, the determinant is given by the formula\n\n$$\n\\begin{vmatrix}a & b \\\\ c & d\\end{vmatrix}=ad-bc.\n$$\n\nUsing the formula, we have:\n\n'
solutions={
17592186059981:opening+r'''$$
\begin{aligned}
\begin{vmatrix}\sqrt{2} & 5 \\ 1 & 3\end{vmatrix}
&=\sqrt{2}\cdot3-5\cdot1 \\
&=3\sqrt{2}-5.
\end{aligned}
$$''',
17592186060000:opening+r'''$$
\begin{aligned}
\begin{vmatrix}2 & -4 \\ -2 & 7\end{vmatrix}
&=2\cdot7-(-4)\cdot(-2) \\
&=14-8 \\
&=6.
\end{aligned}
$$''',
17592186060001:opening+r'''$$
\begin{aligned}
\det(C)&=\begin{vmatrix}2 & 3 \\ 5 & k\end{vmatrix} \\
&=2\cdot k-3\cdot5 \\
&=2k-15.
\end{aligned}
$$

Since $\det(C)=3$, we obtain:

$$
\begin{aligned}
2k-15&=3 \\
2k&=18 \\
k&=9.
\end{aligned}
$$''',
17592186060195:opening+r'''$$
\begin{aligned}
\det(A)&=\begin{vmatrix}1+t & 2t \\ -3 & 1-t\end{vmatrix} \\
&=(1+t)(1-t)-(2t)(-3) \\
&=1-t^2+6t.
\end{aligned}
$$

Since $\det(A)=10$, we obtain:

$$
\begin{aligned}
1-t^2+6t&=10 \\
t^2-6t+9&=0 \\
(t-3)^2&=0 \\
t&=3.
\end{aligned}
$$'''}
math={r['entity']:r for r in json.loads((H/'independent-math.json').read_text())};forms=[];fields=[];links=[]
for e,new in solutions.items():
 q=byid[e];old=q.get(':question/worked-solution');assert old is None or not old.strip();forms.append([kw('db/cas'),e,kw('question/worked-solution'),old,new]);fields.append({'entity':e,'attribute':'question/worked-solution','before':old,'after':new,'before_sha256':hashlib.sha256((old or'').encode()).hexdigest(),'after_sha256':hashlib.sha256(new.encode()).hexdigest()});q[':question/worked-solution']=new
 for f in q[':question/answer-fields']:
  correct=math[e]['fields'][0]['correct'];assert not f.get(':answer-field/correct');forms.append([kw('db/cas'),f[':db/id'],kw('answer-field/correct'),None,correct]);f[':answer-field/correct']=next(a for a in f[':answer-field/choices']if a[':db/id']==correct);links.append({'question':e,'field':f[':db/id'],'correct':correct,'value':f[':answer-field/correct'][':answer/value']});forms.append([kw('db/ensure'),f[':db/id'],kw('answer-field/validate')]);forms.append([kw('db/ensure'),correct,kw('answer/validate')])
 forms.append([kw('db/ensure'),e,kw('question/validate')])
# The existing practice item has a complete problem and solution but lost all
# response controls. Author one math blank for its unique solution x=4.
e=17592186233379;q=byid[e];assert not q.get(':question/answer-fields');assert math[e]['expected']=='4';old=q[':question/problem'];new=old+'\n\n$x=$ {{field-1}}';fid=uuid.uuid5(uuid.UUID(q[':question/id']),'source-fidelity-repair:field-1');aid=uuid.uuid5(fid,'correct:4')
answer={kw('db/id'):'answer',kw('answer/id'):aid,kw('answer/type'):kw('answer.type/math'),kw('answer/value'):'4'};field={kw('db/id'):'field',kw('answer-field/id'):fid,kw('answer-field/key'):'field-1',kw('answer-field/type'):kw('answer-field.type/blank'),kw('answer-field/choices'):['answer'],kw('answer-field/correct'):'answer'};forms.extend([answer,field,[kw('db/cas'),e,kw('question/problem'),old,new],[kw('db/add'),e,kw('question/answer-fields'),'field'],[kw('db/ensure'),'answer',kw('answer/validate')],[kw('db/ensure'),'field',kw('answer-field/validate')],[kw('db/ensure'),e,kw('question/validate')]]);fields.append({'entity':e,'attribute':'question/problem','before':old,'after':new,'before_sha256':hashlib.sha256(old.encode()).hexdigest(),'after_sha256':hashlib.sha256(new.encode()).hexdigest()});q[':question/problem']=new;q[':question/answer-fields']=[{':answer-field/id':str(fid),':answer-field/key':'field-1',':answer-field/type':{':db/ident':':answer-field.type/blank'},':answer-field/choices':[{':answer/id':str(aid),':answer/type':{':db/ident':':answer.type/math'},':answer/value':'4'}],':answer-field/correct':{':answer/id':str(aid),':answer/value':'4'}}]
# Overlay committed layout fixes for the final lesson/grade checks.
for f in json.loads((H/'format/fields.json').read_text()):
 if f['entity']in byid:byid[f['entity']][':'+f['attribute']]=f['after']
h=H/'completion';h.mkdir(exist_ok=True);(h/'fields.json').write_text(json.dumps(fields,indent=2)+'\n');(h/'transaction.edn').write_text(dumps(forms)+'\n');(h/'existing-links.json').write_text(json.dumps(links,indent=2)+'\n');(h/'new-control.json').write_text(json.dumps({'question':e,'field_uuid':str(fid),'answer_uuid':str(aid),'answer':'4','response_type_authored':True},indent=2)+'\n');(H/'repaired-questions.json').write_text(json.dumps(qs,indent=2)+'\n');print('Prepared four missing solutions/correct links and one authored math blank; existing answer values unchanged')
