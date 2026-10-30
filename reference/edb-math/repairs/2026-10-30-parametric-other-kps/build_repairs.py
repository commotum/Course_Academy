"""Formatting-only replacements; prove every mathematical cell/key unchanged."""
import importlib.util,json,os,re,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from generate.parametric_layout_policy import validate_delivery_batch

def table_rows(text):
    result={'t':[],'x':[],'y':[]}
    for line in text.splitlines():
        if not line.startswith('|') or '---' in line:continue
        cells=[c.strip() for c in line.strip().strip('|').split('|')];key=cells[0].strip('*$ ')
        if key in result:result[key].extend(cells[1:])
    return result

def values(q):
    return [(f[':answer-field/key'],f[':answer-field/type'],[a[':answer/value'] for a in f[':answer-field/choices']]) for f in q[':question/answer-fields']]

def main():
    summary=[];render=[]
    for kp in (17592186087717,17592186087736):
        h=H/str(kp);records=[]
        for level in ('easy','moderate','hard'):
            def run(path):
                out=subprocess.run([sys.executable,str(path),'--difficulty',level,'--count','5','--seed','2026103087736'],check=True,capture_output=True,text=True,timeout=45,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
                return json.loads(out.stdout)
            # Original module uses package-local resources; execute it alongside
            # those immutable resource copies without changing its contents.
            original=h/'package/original_check.py';original.write_bytes((h/'original-generator.py').read_bytes())
            try:old=run(original)
            finally:original.unlink()
            new=run(h/'package/generator.py');assert len(old)==len(new)==5
            for a,b in zip(old,new):
                qa,qb=a['question'],b['question'];assert values(qa)==values(qb)
                if kp==17592186087717:
                    for key in (':question/problem',':question/worked-solution'):
                        assert table_rows(qa[key])==table_rows(qb[key])
                        assert '\n'.join(l for l in qa[key].splitlines() if l and not l.startswith('|'))=='\n'.join(l for l in qb[key].splitlines() if l and not l.startswith('|'))
                    for key in ('parameters','derivation','displayed_final','response_design'):assert a['generation'][key]==b['generation'][key]
                else:
                    assert qa[':question/worked-solution']==qb[':question/worked-solution']
                    for key in ('parameters','functions','domain_quarters','solution_path'):assert a['generation'][key]==b['generation'][key]
                    for axis in ('x','y'):
                        old_formula=re.search(axis+r'=(.*?)(?:,|\n)',qa[':question/problem'])[1]
                        assert '$$\n'+axis+'='+old_formula+'\n$$' in qb[':question/problem']
                assert qa[':question/difficulty']==qb[':question/difficulty']
            validate_delivery_batch(new,kp);records+=new;render.append(new[0]);print(kp,level,'math unchanged',flush=True)
        (h/'candidate-pool.json').write_text(json.dumps(records,indent=2)+'\n')
        summary.append({'kp':kp,'new_questions':15,'per_band':5,'same_seed_parameters_cells_derivations_and_answers_preserved':True})
    (H/'repair-render-input.json').write_text(json.dumps(render,indent=2)+'\n')
    (H/'repair-verification.json').write_text(json.dumps({'passed':True,'kps':summary},indent=2)+'\n')

if __name__=='__main__':main()
