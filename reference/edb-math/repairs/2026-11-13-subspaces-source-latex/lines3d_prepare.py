import json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup,Tag

ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'))
from import_historical_question_content import Renderer
from question_capture.math_format import normalize_source_tex

class SourceRenderer(Renderer):
    def math_node(self,n):
        if isinstance(n,Tag) and n.name=='mspace':
            width=n.get('width','')
            return {'1em':r'\quad ','2em':r'\qquad ','0.167em':r'\,','0.222em':r'\:','0.278em':r'\;'}.get(width,r'\hspace{'+width+'}')
        return super().math_node(n)

qs=json.loads((OUT/'lines3d-questions.json').read_text())
paths=[Path(p) for p in Path('/tmp/lines3d-source-paths.txt').read_text().splitlines()]
statepath=Path('reference/mathacademy/question-capture/14096346/state.json')
state=json.loads((ROOT/statepath).read_text())
def source(q,kind):
    mid=q[':question/math-academy-id'];num=mid[2:]
    if mid.startswith('e-'):
        p=Path('reference/mathacademy/capture/differential/14246322/observations/lesson-step-41660-f7ea9675e87221cd2f92.html')
        s=BeautifulSoup((ROOT/p).read_text(),'html.parser')
        return s.select_one('.exampleQuestion' if kind=='problem' else '.exampleExplanation'),str(p)
    if num in ('157375','157392'):
        k='before' if kind=='problem' else 'history'
        return BeautifulSoup(state['questions'][mid][k]['html'],'html.parser'),str(statepath)+'#questions.'+mid+'.'+k+'.html'
    prefix='history-q-' if kind=='problem' else 'history-solution-q-'
    candidates=[p for p in paths if p.name.startswith(prefix+num+'-') and p.suffix=='.html']
    candidates.sort(key=lambda p:('14246322' not in str(p),str(p)))
    p=candidates[0]
    s=BeautifulSoup((ROOT/p).read_text(),'html.parser')
    if kind=='problem':s=s.select_one('.questionText') or s
    return s,str(p)

def formulas(s):
    renderer=SourceRenderer(1853)
    result=[]
    for n in s.select('svg title, mjx-container'):
        if n.name=='mjx-container' and (n.find_parent('title') or n.find_parent('mjx-container')):continue
        if n.name=='title':
            # The original legacy SVG title can contain newer MathJax nodes;
            # replace those nodes with their own MathML-derived TeX before reading it.
            title=BeautifulSoup(str(n),'html.parser')
            for c in title.select('mjx-container'):
                c.replace_with(renderer.m(c.select_one('mjx-assistive-mml > math')))
            result.append(normalize_source_tex(title.get_text()).strip())
        else:result.append(normalize_source_tex(renderer.m(n.select_one('mjx-assistive-mml > math'))).strip())
    return result,renderer.errors

pattern=re.compile(r'\$\$([\s\S]*?)\$\$|\$([^$]*?)\$')
def texs(text):return [m[1] if m[1] is not None else m[2] for m in pattern.finditer(text)]
def bare(s):
    s=s.replace(r'\dfrac',r'\frac').replace(r'\neq',r'\ne').replace(r'\not\in',r'\notin')
    s=re.sub(r'\\(?:mathbf|mathbb|mathrm|mathit)\{([^{}]*)\}',r'\1',s)
    s=re.sub(r'\\color(?:\[[^\]]+\])?\{[^{}]*\}','',s)
    s=re.sub(r'\\(?:quad|qquad)\b|\\[,;:]|\\hspace\{[^{}]*\}','',s)
    s=re.sub(r'\s+','',s)
    s=re.sub(r'\\left|\\right','',s)
    s=s.replace(r'\begin{bmatrix}',r'[\begin{aligned}').replace(r'\end{bmatrix}',r'\end{aligned}]')
    s=s.replace(r'\begin{array}{c}',r'\begin{aligned}').replace(r'\end{array}',r'\end{aligned}')
    s=s.replace('{[','[').replace(']}',']')
    # TeX grouping around a token has no displayed effect. Iterating also removes nested groups.
    prev=None
    while prev!=s:
        prev=s;s=re.sub(r'\{([^{}]*)\}',lambda m:m[1] if not re.search(r'\\(?:begin|end|frac|hspace)$',s[:m.start()]) else m[0],s)
    return s

if __name__=='__main__':
    report=[]
    for q in qs:
        row={'entity':q[':db/id'],'ma':q[':question/math-academy-id'],'parts':{}}
        for kind in ('problem','worked-solution'):
            src,path=source(q,'problem' if kind=='problem' else 'solution')
            fs,errors=formulas(src);current=texs(q[':question/'+kind])
            row['parts'][kind]={'source':path,'formulas':fs,'current':current,'errors':errors,'source_html':str(src)}
        report.append(row)
    (OUT/'lines3d-extracted.json').write_text(json.dumps(report,indent=2))
    for q in report:
        print('\nQUESTION',q['ma'])
        for part,v in q['parts'].items():
            print(part,'source',len(v['formulas']),'current',len(v['current']))
            for i,t in enumerate(v['current']):
                matches=[j for j,s in enumerate(v['formulas']) if bare(t)==bare(s)]
                if not matches:print('UNMATCHED',i,t)
                elif t.strip()!=v['formulas'][matches[0]]:print('DIFF',i,t,'=>',v['formulas'][matches[0]])

    proposals=[];audit=[]
    for q,ex in zip(qs,report):
        sources={};formula_changes=[]
        for part,v in ex['parts'].items():
            assert not v['errors'],(q[':db/id'],v['errors'])
            for f in v['formulas']:
                sources.setdefault(bare(f),[]).append((f,v['source']))
        fields=[(q[':db/id'],':question/problem',q[':question/problem']),
                (q[':db/id'],':question/worked-solution',q[':question/worked-solution'])]
        for field in q.get(':question/answer-fields',[]):
            fields.append((field[':db/id'],':answer-field/key',field[':answer-field/key']))
            for answer in field.get(':answer-field/choices',[]):
                fields.append((answer[':db/id'],':answer/value',answer[':answer/value']))
        unmatched=[]
        for entity,attr,before in fields:
            changed=[]
            def repair(m):
                t=m[1] if m[1] is not None else m[2]
                candidates=sources.get(bare(t),[])
                if not candidates:
                    unmatched.append({'entity':entity,'attribute':attr,'formula':t});return m[0]
                # The canonical example already retains source formatting. Its
                # array/bmatrix spelling is equivalent and is left unchanged.
                if q[':question/math-academy-id'].startswith('e-'):return m[0]
                compact={re.sub(r'\s+','',s) for s,p in candidates}
                assert len(compact)==1,(entity,attr,t,candidates)
                s,path=candidates[0]
                if re.sub(r'\s+','',t)==re.sub(r'\s+','',s):return m[0]
                assert bare(t)==bare(s)
                changed.append({'before':t.strip(),'after':s,'source':path})
                return m[0][:2]+s+m[0][-2:] if m[1] is not None and not t.startswith('\n') else ('$$\n'+s+'\n$$' if m[1] is not None else '$'+s+'$')
            after=pattern.sub(repair,before)
            if after!=before:
                proposals.append({'entity':entity,'attribute':attr,'before':before,'after':after,
                    'reason':'Restore original MathML mathvariant (bold vectors and double-struck real-number space), and original red failure-marker color/1em spacing where present; preserve mathematical values and migrated statement references.',
                    'source':sorted(set(c['source'] for c in changed))})
                formula_changes.extend([dict(c,entity=entity,attribute=attr) for c in changed])
        assert not unmatched,(q[':db/id'],unmatched)
        audit.append({'entity':q[':db/id'],'math_academy_id':q[':question/math-academy-id'],
            'source_paths':sorted(set(v['source'] for v in ex['parts'].values())),
            'source_formula_counts':{k:len(v['formulas']) for k,v in ex['parts'].items()},
            'checked_fields':len(fields),'formula_changes':formula_changes,
            'finding':'Source and current mathematical expressions agree after removing presentation styling. Restored missing source styles only.' if formula_changes else 'Canonical source formulas, including nested MathJax inside SVG title elements, retain equivalent math and presentation styling; no edit needed.',
            'gaps':[]})
    (OUT/'lines3d-proposals.json').write_text(json.dumps(proposals,indent=2)+'\n')
    (OUT/'lines3d-audit.json').write_text(json.dumps({'knowledge_point':17592186119927,'basis':14584,
        'coverage':'All 12 bank questions plus canonical e-10977: prompts, worked solutions, all answer-field labels and all answer values.',
        'proposal_count':len(proposals),'formula_change_count':sum(len(x['formula_changes']) for x in audit),
        'gaps':[],'questions':audit},indent=2)+'\n')
    print('PROPOSALS',len(proposals),'FORMULAS',sum(len(x['formula_changes']) for x in audit))
