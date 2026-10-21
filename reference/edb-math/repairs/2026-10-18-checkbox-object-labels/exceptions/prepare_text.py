"""Prepare reviewed exceptional text presentations; read-only database evidence."""
import copy,json,re,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'mapping'))
from extract import solution_references, clean_prompt

OCCURRENCES={
17592186381826:[('x',r'The occurrence of $x$ in $xy=1$'),('z',r'The occurrence of $z$ immediately after $∀$'),('z',r'The occurrence of $z$ in $xz>3$')],
17592186381867:[('y',r'The occurrence of $y$ immediately after $∀$'),('x',r'The occurrence of $x$ in $y+x\le z$'),('z',r'The occurrence of $z$ on the right side of $y+x\le z$')],
17592186381874:[('n',r'The occurrence of $n$ in $x>n+1$'),('z',r'The occurrence of $z$ in ${z}^{3}-1=y$'),('y',r'The occurrence of $y$ on the right side of ${z}^{3}-1=y$')],
17592186390205:[('x',r'The occurrence of $x$ immediately after $∃$'),('x',r'The occurrence of $x$ in $2-x=w$'),('w',r'The occurrence of $w$ on the right side of $2-x=w$')],
17592186390212:[('m',r'The occurrence of $m$ immediately after $∃$'),('n',r'The occurrence of $n$ on the left side of $n\mid m$'),('m',r'The occurrence of $m$ on the right side of $n\mid m$')],
17592186407132:[('k',r'The occurrence of $k$ immediately after $∀$'),('n',r'The occurrence of $n$ in $n+{k}^{2}\ge k$'),('k',r'The occurrence of $k$ on the right side of $n+{k}^{2}\ge k$')],
17592186407134:[('x',r'The occurrence of $x$ immediately after $∀$ in the left-hand statement'),('x',r'The occurrence of $x$ in $x=\operatorname{sin} y$'),('y',r'The occurrence of $y$ in $\operatorname{sin} y$')],
}

def main():
    qs=json.loads((ROOT/'questions.json').read_text())
    history={h['id']:h for h in json.loads((HERE/'historical-exceptional.json').read_text())}
    cases=[]
    for q in qs:
        eid=q[':db/id'];h=history.get(eid,{})
        classification=h.get('classification');before=q[':question/problem'];sol=q.get(':question/worked-solution','')
        bylabel={f[':answer-field/key']:f for f in q[':question/answer-fields']}
        objects=[];after=before;solution=sol;edits=[]
        if classification=='finite_named_special_sets':
            source='Consider the following sets:\n\n$$\nN,\\,Z,\\,Q,\\,R,\\,C\n$$'
            assert source in before
            after=clean_prompt(before.replace(source,'',1)).replace('To which of these sets','To which of the following sets',1)
            names={'N':'Natural numbers','Z':'Integers','Q':'Rational numbers','R':'Real numbers','C':'Complex numbers'}
            for label in h['labels']:
                objects.append({'source_label':label,'field_id':bylabel[label][':db/id'],'content':f'{names[label]} (${label}$)','source_fragment':source})
        elif eid in OCCURRENCES:
            for label,(variable,content) in zip(('I','II','III'),OCCURRENCES[eid]):
                source=r'_{\begin{aligned} \\ ↑ \\ \text{'+label+r'}\end{aligned}}'
                assert before.count(source)==1
                after=after.replace(source,'',1)
                objects.append({'source_label':label,'field_id':bylabel[label][':db/id'],'content':content,'source_fragment':source})
                previous=f'Occurrence {label} of the variable ${variable}$'
                assert previous in solution
                solution=solution.replace(previous,content,1)
                edits.append({'before':previous,'after':content,'kind':'descriptive_occurrence_reference'})
            solution,more=solution_references(solution,objects);edits+=more
        elif classification=='finite_inline_roman_systems':
            block=re.search(r'\$\$\s*(\\text\{I\.\}[\s\S]+?)\s*\$\$',before)
            assert block
            parts=re.split(r'\\text\{(I|II|III)\.\}\\,',block[1])[1:]
            assert len(parts)==6
            for label,body in zip(parts[::2],parts[1::2]):
                body=re.sub(r'\\,\s*$','',body.strip())
                assert body.startswith(r'{\begin{aligned}') and body.endswith(r'\end{aligned}')
                # The captured source uses a lone { for the system fence. Make
                # the complete displayed system valid TeX while moving it.
                content='$'+r'\left\{'+body[1:]+r'\right.'+'$'
                objects.append({'source_label':label,'field_id':bylabel[label][':db/id'],'content':content,'source_fragment':body})
            after=clean_prompt(before[:block.start()]+before[block.end():])
            # The explanation's generic system has the same unbalanced fence.
            solution=re.sub(r'(?m)^\{(\\begin\{aligned\}[^\n]*\\end\{aligned\})$',lambda m:r'\left\{'+m[1]+r'\right.',solution)
            solution,edits=solution_references(solution,objects)
        else:continue
        afterq=copy.deepcopy(q);afterq[':question/problem']=after;afterq[':question/worked-solution']=solution
        lookup={o['field_id']:o['content']for o in objects}
        for field in afterq[':question/answer-fields']:field[':answer-field/key']=lookup[field[':db/id']]
        cases.append({'question_eid':eid,'math_academy_id':q.get(':question/math-academy-id'),'problem_before':before,'problem_after':after,'solution_before':sol,'solution_after':solution,'objects':objects,'solution_reference_edits':edits,'extraction':classification,'historical_plan':h.get('historical_plan'),'question_before':q,'question_after':afterq})
    (HERE/'text-cases.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2)+'\n')
    (HERE/'text-lint-input.json').write_text(json.dumps({'cases':[{'question':c['question_after'],'objects':c['objects']}for c in cases]},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'questions':len(cases),'fields':sum(len(c['objects'])for c in cases)}))
if __name__=='__main__':main()
