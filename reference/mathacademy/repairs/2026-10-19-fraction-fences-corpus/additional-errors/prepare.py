"""Recover the four preexisting bad formulas from retained MathML evidence."""
import copy,importlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;PARENT=HERE.parent
base=importlib.import_module('reference.mathacademy.repairs.2026-10-19-fraction-fences-corpus.analyze')
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2,ensure_ascii=False,default=str)+'\n')
def run():
    source=json.loads((HERE/'source-records.json').read_text());global_changes={(c['entity'],c['attribute']):c for c in json.loads((PARENT/'changes.json').read_text())};changes=[];records=[]
    for r in source:
        e=r['entity'];record=copy.deepcopy(r['record']);attr=':tutorial/content' if ':tutorial/id' in record else ':question/worked-solution';before=global_changes[(e,attr)]['after'];after=before
        if e in (17592186192595,17592186192596):
            for v in ('x','y'):
                old=v+r'^{2}^(―)';assert after.count(old)==1;after=after.replace(old,r'\overline{'+v+r'^{2}}')
                old=v+r'^(―)^{2}';assert after.count(old)==1;after=after.replace(old,r'\overline{'+v+r'}^{2}')
        else:
            target=next(m for m in base.fmt.MATH.finditer(before) if '[math]' in m[0] and '#' in m[0])
            if e==17592186163206:
                formula=(r'\begin{aligned}P(X=2) &= \frac{\substack{\text{\# of samples of size 3}\\\text{with precisely 2 blue candies}}}{\text{\# of samples of size 3}}'
                         r' \\ &= \frac{\binom{4}{2}\cdot\binom{6}{1}}{\binom{10}{3}} \\ &= \frac{3}{10}\end{aligned}')
            else:
                formula=(r'\begin{aligned}&\text{\# of samples with }x\text{ veteran players}'
                         r' \\ &= \left(\substack{\text{\# of ways to select }x\\\text{veteran players}}\right)\cdot\left(\substack{\text{\# of ways to select }(6-x)\\\text{beginners}}\right)'
                         r' \\ &= \binom{12}{x}\cdot\binom{6}{6-x}\end{aligned}')
            after=before[:target.start()]+'\n\n$$\n'+formula+'\n$$\n\n'+before[target.end():]
        assert after!=before;record[attr]=after;changes.append({'entity':e,'attribute':attr,'before':before,'after':after,'source_evidence':str(HERE/'source-evidence.json')})
        if attr==':tutorial/content':q={':question/problem':after,':question/worked-solution':'',':question/answer-fields':[]}
        else:q={':question/problem':record[':question/problem'],':question/worked-solution':after,':question/answer-fields':[]}
        records.append({'question':q})
    save('changes.json',changes);save('render-input.json',records);print('Prepared four source-backed formula reconstructions.')
if __name__=='__main__':run()
