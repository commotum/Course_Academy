"""Independent numeric keys, actual delivery, native grading and relocation."""
import copy,json,os,re,shutil,subprocess,sys,tempfile,uuid
from pathlib import Path
import sympy as S
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from generate.pipeline.check_delivery import audit

def math_record(value):
    qid=str(uuid.uuid5(uuid.NAMESPACE_URL,'equilibrium-visible-math/'+value))
    answer={':answer/id':qid,':answer/type':':answer.type/math',':answer/value':value}
    return {'knowledge_point':{'title':'Independent printed-equation check'},'generation':{'template':'visible mathematics'},'question':{
        ':question/problem':'Check the printed expression.',':question/answer-fields':[{
            ':answer-field/key':'value',':answer-field/type':':answer-field.type/blank',
            ':answer-field/choices':[answer],':answer-field/correct':[':answer/id',qid]}]}}

def main():
    records=json.loads((H/'candidate-pool.json').read_text());source=json.loads((H/'source/source.json').read_text());inventory=json.loads((H/'source/inventory.json').read_text())
    accepted=[];deliveries=[]
    for band in ('easy','moderate','hard'):
        rows=[r for r in records if r['question'][':question/difficulty'].endswith('/'+band)]
        result=audit(rows,inventory,source,band,H/'delivery'/band,H,Path('/media/jake/SSD/EDB/math'))
        assert result['accepted_count']==5 and result['duplicate_count']==0
        delivered=json.loads((H/'delivery'/band/'accepted.json').read_text());accepted+=delivered;deliveries.append(result)
    cases=[];numeric=[];y=S.Symbol('y',real=True)
    for index,r in enumerate(accepted):
        checks=[];q=r['question'];g=r['generation'];truths=[]
        lhs,rhs=[S.sympify(g['original_equation'][side],locals={'y':y},evaluate=False) for side in ('lhs','rhs')]
        for i,(field,text) in enumerate(zip(q[':question/answer-fields'],g['parameters']['candidates'])):
            c=S.sympify(text)
            # Evaluate the ORIGINAL sides numerically, including log arguments
            # and denominators, independently of generator decision()/path keys.
            domain=True
            for expr in (lhs,rhs):
                for f in expr.atoms(S.log):domain &= float(f.args[0].subs(y,c).evalf(60))>0
                for p in expr.atoms(S.Pow):
                    if p.exp.is_negative:domain &= abs(complex(p.base.subs(y,c).evalf(60)))>1e-30
            delta=complex((rhs.subs(y,c)-lhs.subs(y,c)).evalf(60)) if domain else None
            yes=bool(domain and abs(delta)<1e-30);truths.append(yes)
            by_value={a[':answer/value']:a[':answer/id'] for a in field[':answer-field/choices']}
            assert field[':answer-field/correct'][1]==by_value[str(yes).lower()]
            checks += [{'field_index':i,'submitted_answer_id':by_value[str(b).lower()],
                       'expected':'accepted' if b==yes else 'rejected','purpose':'independent original-equation key' if b==yes else 'flip this Boolean answer'} for b in (False,True)]
            # Read the visible label, not the solution-path copy of it.
            label=field[':answer-field/key'].strip('$').split('=',1)[1].replace('\\\\','\\')
            canonical=S.latex(c,ln_notation=True)
            cases.append({'label':f'{index} visible candidate {i}','record':math_record(canonical),'checks':[
                {'submitted':label,'expected':'accepted','purpose':'visible candidate equals independent candidate value'}]})
        cases.append({'label':f'{index} {g["template"]}','record':r,'checks':checks})
        numeric.append({'index':index,'family':g['template'],'truths':truths,'original_domain_checked':True})
        block=re.findall(r'\$\$(.*?)\$\$',q[':question/problem'],re.S)[0]
        block=block.replace(r'\begin{gathered}','').replace(r'\end{gathered}','').replace(r'\\',' ').strip().rstrip('.')
        left,right=block.split('=',1)
        left=re.sub(r'\\frac\{dy\}\{d[tx]\}','',left).strip() or '0'
        expression='('+right.strip()+')-('+left+')'
        canonical=S.latex(rhs-lhs,ln_notation=True)
        cases.append({'label':f'{index} printed ODE','record':math_record(canonical),'checks':[
            {'submitted':expression,'expected':'accepted','purpose':'visible original equation agrees with mathematical model'},
            {'submitted':expression+'+1','expected':'rejected','purpose':'detect a changed sign or constant in printed ODE'}]})
    (H/'native-grading-input.json').write_text(json.dumps(cases,indent=2)+'\n')
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(H/'native-grading-input.json'),str(H/'native-grading.json')],check=True)
    # Execute outside the repository with no ancestor imports or generator caches.
    with tempfile.TemporaryDirectory(prefix='equilibrium-relocate-') as tmp:
        package=Path(tmp)/'package';shutil.copytree(H/'package',package)
        for i,band in enumerate(('easy','moderate','hard')):
            env={**os.environ,'PYTHONPATH':'','PYTHONDONTWRITEBYTECODE':'1','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(Path(tmp)/'output')}
            output=subprocess.check_output([sys.executable,str(package/'generator.py'),'--difficulty',band,'--count','5','--seed',str(202611020+i),'--format','json'],cwd=tmp,env=env,text=True)
            assert json.loads(output)==[r for r in records if r['question'][':question/difficulty'].endswith('/'+band)]
    result={'passed':True,'numeric_original_equation_cases':numeric,'delivery_counts':[d['accepted_count'] for d in deliveries],
            'relocation_all_three_bands_equal':True,'native_report':'native-grading.json','source_bands':{'easy':5,'unclassified_incomplete':1,'moderate':0,'hard':0}}
    (H/'repair-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':True,'questions':len(records),'delivered':len(accepted),'native_cases':len(cases)}))

if __name__=='__main__':main()
