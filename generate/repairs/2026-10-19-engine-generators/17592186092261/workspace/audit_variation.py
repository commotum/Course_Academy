"""Within-template surface-cue probes on actual records before/after delivery."""
import collections,json,pathlib,re,sys
import sympy as sp
X=sp.Symbol("x",real=True)
REFERENCE={}

def audit(records):
    groups=collections.defaultdict(list)
    for r in records:groups[r['generation']['template']].append(r)
    out={}
    for template,rows in groups.items():
        params=[r['generation']['parameters'] for r in rows]
        report={'instances':len(rows),'semantic_instances':len({r['generation']['mathematical_fingerprint'] for r in rows}),'slots':{k:sorted({str(p[k]) for p in params}) for k in params[0]},'bank_roles':sorted({r['generation'].get('bank_role') for r in rows if r['generation'].get('bank_role')}),'cue_probes':{}}
        radios=[r for r in rows if r['question'][':question/answer-fields'][0][':answer-field/type'].endswith('/radio')]
        for r in radios:
            f=r['question'][':question/answer-fields'][0];options=f[':answer-field/choices'];correct=f[':answer-field/correct'][1]
            lengths=[len(re.sub(r'\\[a-zA-Z]+|[{}\s]', '',a[':answer/value'])) for a in options]
            rawlengths=[len(a[':answer/value']) for a in options]
            reference=REFERENCE.get((r['generation']['template'],json.dumps(r['generation']['parameters'],sort_keys=True),r['generation']['seed']),r)
            original_fields=reference['question'][':question/answer-fields'][0]
            math_by_text={a[':answer/value']:reference['generation']['answer_math'][a[':answer/id']] for a in original_fields[':answer-field/choices']}
            values=[]
            for a in options:
                expression=sp.sympify(math_by_text[a[':answer/value']],locals={'x':X})
                if r['question'][':question/difficulty'].endswith('/hard'):expression=sp.diff(expression,X)
                values.append(float(expression.subs(X,1)))
            for name,scores in [('visible-length',lengths),('tex-length',rawlengths),('signed-value',values),('absolute-value',[abs(v) for v in values])]:
                for rank in range(5):
                    val=sorted(scores)[rank];eligible=[a for a,v in zip(options,scores) if v==val]
                    # Tie split is expected accuracy, without cherry-picking a tie.
                    success=sum(a[':answer/id']==correct for a in eligible)/len(eligible)
                    key=name+'-rank-'+str(rank+1)
                    probe=report['cue_probes'].setdefault(key,{'successes':0,'attempts':0,'baseline':0.2});probe['successes']+=success;probe['attempts']+=1
            frequencies=collections.Counter(abs(v) for v in values)
            for name,count in [('singleton-magnitude',1),('paired-magnitude',2)]:
                eligible=[a for a,v in zip(options,values) if frequencies[abs(v)]==count]
                success=sum(a[':answer/id']==correct for a in eligible)/len(eligible) if eligible else 0
                probe=report['cue_probes'].setdefault(name,{'successes':0,'attempts':0,'baseline':0.2});probe['successes']+=success;probe['attempts']+=1
            for i,a in enumerate(options):
                probe=report['cue_probes'].setdefault('position-'+str(i+1),{'successes':0,'attempts':0,'baseline':0.2});probe['successes']+=a[':answer/id']==correct;probe['attempts']+=1
            for name,predicate in [('negative-text',lambda t:'-' in t),('positive-text',lambda t:'-' not in t),('contains-log',lambda t:r'\ln' in t),('no-log',lambda t:r'\ln' not in t)]:
                eligible=[a for a in options if predicate(a[':answer/value'])]
                success=sum(a[':answer/id']==correct for a in eligible)/len(eligible) if eligible else 0
                probe=report['cue_probes'].setdefault(name,{'successes':0,'attempts':0,'baseline':0.2});probe['successes']+=success;probe['attempts']+=1
        report['deterministic_surface_predictors']=[k for k,v in report['cue_probes'].items() if v['successes']==v['attempts'] and v['attempts']>=4]
        # A constant blank response is tested by exact mathematical fingerprint of
        # answer value, not question UUID or option position.
        keys=[]
        for r in rows:
            f=r['question'][':question/answer-fields'][0];keys.append(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]))
        report['distinct_correct_values']=len(set(keys))
        report['largest_constant_response_frequency']=max(collections.Counter(keys).values())
        out[template]=report
    return out
if __name__=='__main__':
    raw=json.load(open(sys.argv[1]))
    reference=json.load(open('evidence/test-records.json'))
    REFERENCE={(r['generation']['template'],json.dumps(r['generation']['parameters'],sort_keys=True),r['generation']['seed']):r for r in reference}
    conditional={}
    for sign in (-1,1):
        rows=[r for r in raw if (1 if r['generation']['parameters']['a']>0 else -1)==sign]
        conditional[str(sign)]=audit(rows)
    out={'input':sys.argv[1],'templates':audit(raw),'conditional_a_sign':conditional}
    pathlib.Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'records':len(raw),'templates':len(out['templates']),'deterministic_cues':{k:v['deterministic_surface_predictors'] for k,v in out['templates'].items() if v['deterministic_surface_predictors']}}))
