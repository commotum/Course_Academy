"""Visible-record regressions for both retained review findings; no services/writes to runtime."""
import importlib.util,json,re,sys,unittest
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parents[1]
SOURCE=W.parent/'source/source.json'
SPEC=importlib.util.spec_from_file_location('candidate',W/'17592186184219.py')
G=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(G)
QS=json.loads(SOURCE.read_text())['material']['kp'][':knowledge-point/questions']

def read(record):
    q=record.get('question',record); text=q[':question/problem']
    m,n=map(int,re.search(r'(\d+)\s*\\times\s*(\d+)',text).groups())
    k=int(re.search(r'=(\d+)',text).group(1))
    target='rank' if text.rfind('rank')>text.rfind('nullity') else 'nullity'
    f=q[':question/answer-fields'][0];key=f[':answer-field/correct']
    cid=key[':answer/id'] if isinstance(key,dict) else key[1]
    choices=f[':answer-field/choices'];values=[int(a[':answer/value']) for a in choices]
    c=next(int(a[':answer/value']) for a in choices if a[':answer/id']==cid)
    return dict(m=m,n=n,k=k,target=target,c=c,values=values)

def math_check(r):
    d=read(r);m,n,k,t,c=(d[x] for x in ['m','n','k','target','c'])
    assert c==n-k and min(k,c)>=0
    rank=c if t=='rank' else k
    assert rank<=min(m,n)
    assert len(d['values'])==len(set(d['values']))==5 and min(d['values'])>=0
    q=r['question'];sol=re.sub(r'\s','',q[':question/worked-solution'])
    assert f'$n={n}.$' in sol
    lhs=(r'\text{rank}(A)+'+str(k)) if t=='rank' else (str(k)+r'+\text{nullity}(A)')
    assert lhs+f'&={n}' in sol
    assert r'\text{'+t+r'}(A)&='+f'{n}-{k}' in sol and f'&={c}.' in sol
    return d

def witnesses():
    result=[]
    for q in QS:
        d=read(q);bank=sorted(d['values']);bank=[v-bank[0]+2 for v in bank]
        for role,c in enumerate(bank):
            p=dict(m=12,n=12,k=12-c,target=d['target'])
            r=G.generate('easy',seed=20261022,template=d['target'],profile=q[':question/math-academy-id'],parameters=p,bank_role=role)
            got=math_check(r)
            assert sorted(got['values'])==bank and got['c']==c
            result.append(r)
    return result

class GeneratorRegressions(unittest.TestCase):
    def test_all_current_source_banks_replay(self):
        for q in QS:
            with self.subTest(source=q[':question/id']):
                d=read(q);p={k:d[k] for k in ['m','n','k','target']}
                r=G.generate('easy',seed=61403,template=q[':question/math-academy-id'],parameters=p)
                got=math_check(r)
                self.assertEqual(sorted(got['values']),sorted(d['values']))
                self.assertEqual(got['c'],d['c'])
                for key in [':question/problem',':question/worked-solution']:
                    self.assertEqual(re.sub(r'\s','',r['question'][key]),re.sub(r'\s','',q[key]))

    def test_rank_consecutive_bank_does_not_fix_correct_role(self):
        hits=[]
        for seed in range(829001,829017):
            d=math_check(G.generate('easy',seed=seed,template='rank',profile='q-141220'))
            bank=sorted(d['values'])
            self.assertEqual([b-a for a,b in zip(bank,bank[1:])],[1]*4)
            hits.append(d['c']==bank[-2])
        self.assertTrue(hits)
        self.assertLess(sum(hits),len(hits))

    def test_normal_sampler_can_assign_every_bank_role_without_rejection(self):
        for q in QS:
            with self.subTest(profile=q[':question/math-academy-id']):
                target=read(q)['target']
                rs=[G.generate('easy',seed=20261022,template=target,profile=q[':question/math-academy-id'],bank_role=role) for role in range(5)]
                ds=[math_check(r) for r in rs]
                self.assertEqual({d['c'] for d in ds},set(ds[0]['values']))
                self.assertEqual(len({(d['m'],d['n'],tuple(sorted(d['values']))) for d in ds}),1)
                for d in ds:
                    for candidate in d['values']:
                        rank=candidate if target=='rank' else d['n']-candidate
                        self.assertTrue(0<=rank<=min(d['m'],d['n']))

    def test_each_profile_changes_answer_with_same_complete_bank_and_shape(self):
        rows=witnesses()
        self.assertEqual(len(rows),5*len(QS))
        for index,q in enumerate(QS):
            ds=[math_check(r) for r in rows[5*index:5*index+5]]
            self.assertEqual({d['c'] for d in ds},set(ds[0]['values']))
            self.assertEqual(len({tuple(sorted(d['values'])) for d in ds}),1)
            self.assertEqual(len({(d['m'],d['n'],d['target']) for d in ds}),1)
            self.assertEqual(len({r['question'][':question/worked-solution'] for r in rows[5*index:5*index+5]}),5)

if __name__=='__main__':unittest.main(verbosity=2)
