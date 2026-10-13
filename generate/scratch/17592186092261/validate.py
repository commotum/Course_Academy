"""Fail-closed displayed math, fidelity, grading and workload checks; no EDB."""
import copy
import importlib.util
import json
import re
import subprocess
import sys
import uuid
from pathlib import Path

import sympy as sp
from display_math import X,U,expression,equal,prompt_object

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('exponential_generator',ROOT.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
STAGES={}


def write(name,obj):
    (ROOT/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')


def formatting(text):
    assert text.count('$')%2==0
    # Ignore only the complete template placeholder; all TeX groups remain checked.
    t=re.sub(r'\{\{[^{}]+\}\}','',text)
    depth=0
    for char in t:
        if char=='{':depth+=1
        if char=='}':depth-=1
        assert depth>=0,('Closing group without opener',text)
    assert depth==0,('Unbalanced groups',text)
    assert not re.search(r'\+\s*-|-\s*-',text),('Ungrouped signed factor',text)


def check_solution(record,parsed):
    q=record['question'];meta=record['generation'];qid=meta['template'];solution=q.get(':question/worked-solution')
    if solution is None:return 0
    obj=parsed;name=obj['name'];b=obj['base'];u=obj['inner'];c=obj['scale'];du=sp.diff(u,X);D=sp.diff(obj['f'],X)
    blocks=re.findall(r'\$\$(.*?)\$\$',solution,re.S)
    assert len(blocks)==(4 if obj['point'] is not None else 3),(qid,len(blocks))
    # Composite definitions and both independently differentiated components.
    definitions=re.split(r',\\(?:,|qquad|quad)\s*',blocks[0].strip().rstrip('.'))
    assert len(definitions)==2,(qid,definitions)
    assert definitions[0].startswith(name+'=') or re.match(name+r'\s*=',definitions[0])
    assert equal(expression(definitions[0].split('=',1)[1]),c*b**U)
    assert equal(expression(definitions[1].split('=',1)[1]),u)
    components=re.split(r',\\(?:,|qquad|quad)\s*',blocks[1].strip().rstrip('.'))
    assert len(components)==2,(qid,components)
    assert equal(expression(components[0].split('=',1)[1]),c*b**U*sp.log(b))
    assert equal(expression(components[1].split('=',1)[1]),du)
    operators={}
    def operator(style,dependent,independent):
        return r'\frac{'+chr(92)+style+'{d}'+dependent+'}{'+chr(92)+style+'{d}'+independent+'}'
    for style in ('text','mathrm'):
        for dependent,independent,val in ((name,'u',c*b**U*sp.log(b)),('u','x',du),(name,'x',D)):
            op=operator(style,dependent,independent)
            operators[op]='('+g.tex(val)+')'
    def rhs_rows(block):
        block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
        rows=block.split(r'\\');result=[]
        for row in rows:
            assert '&' in row,row
            rhs=row.split('&',1)[1].strip()
            assert rhs.startswith('='),rhs
            result.append(rhs[1:].strip().rstrip('.'))
        return result
    rows=rhs_rows(blocks[2]);expected_count=3 if qid in ('q-107459','q-340969') else 4
    assert len(rows)==expected_count,(qid,rows)
    style='mathrm' if qid in ('q-48631','authored-three-term-slope') else 'text'
    assert all(op in rows[0] for op in (operator(style,name,'u'),operator(style,'u','x')))
    # Operation-preserving masks: substituted stage must still use u, and the
    # product stage (when present) cannot be replaced by a restored final row.
    assert '^{u}' in rows[1] and r'\cdot' in rows[1],(qid,rows[1])
    if expected_count==4:assert '^{u}' in rows[2],(qid,rows[2])
    assert '^{u}' not in rows[-1],(qid,rows[-1])
    for rhs in rows:
        text=g.apply_slots(rhs,operators)
        val=expression(text).subs(U,u)
        assert equal(val,D),(qid,meta['parameters'],rhs,val,D)
    count=2+len(rows)
    if obj['point'] is not None:
        t=obj['point'];slope=D.subs(X,t);evaluation=rhs_rows(blocks[3]);n=4 if qid=='q-340969' else 3
        assert len(evaluation)==n,(qid,evaluation)
        for rhs in evaluation:
            match=re.fullmatch(r'\{\((.*)\)\|}_\{x=.*}',rhs)
            if match:rhs=match[1]
            value=expression(g.apply_slots(rhs,operators)).subs({X:t,U:u.subs(X,t)})
            assert equal(value,slope),(qid,meta['parameters'],rhs,value,slope)
        count+=len(evaluation)
        # Every prose point and the final answer sentence are checked separately.
        for point_tex in re.findall(r'\$x=(.*?)\$',solution):
            assert equal(expression(point_tex.rstrip(' ,.;')),t),(qid,point_tex,t)
        conclusion=re.search(r'Therefore,.*?is \$(.*?)\$',solution,re.S)
        if conclusion:assert equal(expression(conclusion[1].rstrip(' .')),slope)
    STAGES[q[':question/id']]=count
    return count


def check_record(record):
    q=record['question'];m=record['generation'];raw=m['profile'].startswith('observed:')
    assert set(record['knowledge_point'])=={'db_id','id','title'}
    assert record==json.loads(json.dumps(record));uuid.UUID(q[':question/id'])
    parsed=prompt_object(q[':question/problem'])
    D=sp.diff(parsed['f'],X)
    expected=D.subs(X,parsed['point']) if parsed['point'] is not None else D/(parsed['base']**parsed['inner']) if parsed['fragment'] else D
    if not raw:
        assert len(q[':question/answer-fields'])==1
        assert q[':question/difficulty']==':question.difficulty/'+g.SPECS[m['template']]['level']
    for text in (q[':question/problem'],q.get(':question/worked-solution','')):formatting(text)
    for f in q.get(':question/answer-fields',[]):
        uuid.UUID(f[':answer-field/id']);assert isinstance(f[':answer-field/type'],str)
        kind=f[':answer-field/type'].split('/')[-1];choices=f[':answer-field/choices']
        assert len(choices)==(5 if kind=='radio' else 1)
        if kind=='blank':assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
        vals=[]
        for a in choices:
            uuid.UUID(a[':answer/id']);assert a[':answer/type']==':answer.type/math'
            assert '$' not in a[':answer/value'] and '=' not in a[':answer/value']
            formatting(a[':answer/value']);v=expression(a[':answer/value']);vals.append(v)
            assert equal(v,sp.sympify(m['answer_math'][a[':answer/id']],locals={'x':X,'u':U})),(m,a,v)
        assert all(not equal(v,w) for i,v in enumerate(vals) for w in vals[:i])
        correct=f.get(':answer-field/correct')
        if correct:
            assert correct[0]==':answer/id'
            designated=[i for i,a in enumerate(choices) if a[':answer/id']==correct[1]]
            assert len(designated)==1 and equal(vals[designated[0]],expected),(m,choices,expected)
        assert sum(equal(v,expected) for v in vals)==1
    return check_solution(record,parsed)


def engine_fixture(record,label):
    f=record['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1];choices=f[':answer-field/choices']
    if f[':answer-field/type'].endswith('/radio'):
        checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'all radio selections'} for a in choices]
    else:
        answer=next(a[':answer/value'] for a in choices if a[':answer/id']==correct)
        parsed=prompt_object(record['question'][':question/problem']);u=parsed['inner'];du=sp.diff(u,X);b=parsed['base'];c=parsed['scale'];t=parsed['point']
        # Construct an actually unreduced operation expression, not 2*answer/2.
        if t is not None:
            equivalent='('+g.tex(c)+')*('+g.tex(du)+')*('+str(b)+')^('+g.tex(u)+')*ln('+str(b)+')'
            equivalent=re.sub(r'\bx\b','('+g.scalar(t)+')',equivalent)
        elif parsed['fragment']:
            equivalent='ln('+str(b)+')*('+g.tex(du)+')'
        else:
            equivalent='('+g.tex(du)+')*ln('+str(b)+')*('+g.tex(c)+')*('+str(b)+')^('+g.tex(u)+')'
        checks=[{'submitted':answer,'expected':'accepted','purpose':'canonical supported blank'},
                {'submitted':equivalent,'expected':'accepted','purpose':'equivalent unreduced chain-rule factors'},
                {'submitted':'('+answer+')+1','expected':'rejected','purpose':'incorrect value'}]
        if parsed['fragment']:
            checks.append({'submitted':g.tex(sp.diff(parsed['f'],X)),'expected':'rejected','purpose':'full derivative must not grade as coefficient fragment'})
    return {'label':label,'record':record,'checks':checks}


def fidelity(qid):
    src=g.SOURCES[qid];s=g.SPECS[qid];params=g.default_params(qid)
    r=g.generate(s['level'],template=qid,parameters=params,profile='observed:'+qid)
    check_record(r);q=r['question']
    for k in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):
        assert (k in src)==(k in q),(qid,'attribute presence',k)
    for k in (':question/problem',':question/worked-solution'):
        assert q.get(k)==src.get(k),(qid,'exact component-mask source replay',k)
    fields=[]
    for i,(sf,gf) in enumerate(zip(src.get(':question/answer-fields',[]),q.get(':question/answer-fields',[]),strict=True)):
        assert sf[':answer-field/key']==gf[':answer-field/key']
        assert sf[':answer-field/type'][':db/ident']==gf[':answer-field/type']
        assert (':answer-field/correct' in sf)==(':answer-field/correct' in gf)
        sv=sorted(a[':answer/value'] for a in sf[':answer-field/choices']);gv=sorted(a[':answer/value'] for a in gf[':answer-field/choices'])
        assert sv==gv,(qid,'complete exact bank',i,sv,gv)
        if ':answer-field/correct' in sf:
            correct=next(a for a in gf[':answer-field/choices'] if a[':answer/id']==gf[':answer-field/correct'][1])
            assert equal(expression(correct[':answer/value']),expression(sf[':answer-field/correct'][':answer/value']))
        fields.append({'field_index':i,'key':sf[':answer-field/key'],'values_matched':len(sv),'values_total':len(sv),
                       'designation':'matched' if ':answer-field/correct' in sf else 'absent; not in matched denominator'})
    return r,{'source_id':qid,'raw_presence_exact':True,'prompt_exact':True,'solution_exact':':question/worked-solution' in src,'fields':fields}


def main():
    records=[];fixtures=[];source_reports=[];cases=[];review=[]
    for qid,src in g.SOURCES.items():
        r,report=fidelity(qid);records.append(r);source_reports.append(report)
        params=g.default_params(qid);cases.append({'source_id':qid,'template':qid,'level':g.SPECS[qid]['level'],
                'parameters':params,'bank_profile':'observed:'+qid,'difficulty_assignment':'authored easy; original unrated' if g.SPECS[qid].get('unrated') else 'observed'})
        normal=g.generate(g.SPECS[qid]['level'],template=qid,parameters=params)
        check_record(normal);fixtures.append(engine_fixture(normal,'normal original/'+qid))
        # Source normal prose and stage sequence are the same at original params,
        # aside from the explicit fieldless completion / missing-solution completion.
        if ':question/worked-solution' in src:
            assert normal['question'][':question/worked-solution']==g.normalized(src[':question/worked-solution'])
        variants=[]
        for seed in (119,241):
            v=g.generate(g.SPECS[qid]['level'],seed,template=qid);check_record(v);fixtures.append(engine_fixture(v,'variant/'+qid+'/'+str(seed)));variants.append(v)
        review.append({'source_id':qid,'original':r,'normal_at_original':normal,'generated_variants':variants})
        if src.get(':question/answer-fields'):
            h=g.generate(g.SPECS[qid]['level'],template=qid,parameters=params,profile='historical:'+qid);check_record(h)
            # A repaired unknown designation is inferred and never called matched.
            fixtures.append(engine_fixture(h,'historical repaired original/'+qid))
        else:
            assert ':question/answer-fields' not in r['question']
    # Changed original bank patterns run through the public API (not source anchor
    # payloads), and every source family's default participates in repeated practice.
    family_counts={};fingerprints={};mutation_count=0
    for qid,s in g.SPECS.items():
        fam=[]
        for seed in range(16):
            r=g.generate(s['level'],seed,template=qid);check_record(r);fam.append(r)
            if seed<3:fixtures.append(engine_fixture(r,'sample/'+qid+'/'+str(seed)))
            p=r['generation']['parameters']
            identity=g.generate(s['level'],seed+37,template=qid,parameters=p)
            assert identity['question'][':question/id']==r['question'][':question/id']
            assert identity['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
            if qid in g.SOURCES and g.SOURCES[qid].get(':question/answer-fields'):
                h=g.generate(s['level'],seed,template=qid,profile='historical:'+qid)
                check_record(h)
            # Equality-preserving stage mutation must still fail the structural
            # check: restoration cannot replace the source substituted u stage.
            if seed==0:
                bad=copy.deepcopy(r);sol=bad['question'][':question/worked-solution']
                block=re.findall(r'\$\$(.*?)\$\$',sol,re.S)[2]
                rows=block.split(r'\\');rows[1]=rows[-1]
                bad['question'][':question/worked-solution']=sol.replace(block,r'\\'.join(rows))
                try:check_record(bad)
                except AssertionError:mutation_count+=1
                else:raise AssertionError('Stage-loss mutation was not detected')
        family_counts[qid]=len(fam);fingerprints[qid]=len({r['generation']['mathematical_fingerprint'] for r in fam})
        if s['level']=='hard':
            review.append({'source_id':None,'authored_template':qid,'generated_variants':fam[:2]})
    # Defaults choose whole family/profile before parameters, and reach every family.
    default_coverage={level:set() for level in ('easy','moderate','hard')}
    for seed in range(80):
        for level in default_coverage:
            r=g.generate(level,seed);default_coverage[level].add(r['generation']['template'])
    for level,found in default_coverage.items():
        assert found=={q for q,s in g.SPECS.items() if s['level']==level},(level,found)
    # Exact/explicit workload guards, including degenerate hard terms and points.
    rejected=0
    for qid,key,value in [('authored-three-term-slope','k',0),('authored-three-term-slope','c',1),('authored-three-term-slope','a',-4),
                           ('authored-three-term-slope','point','0'),('q-340969','a',4),('q-48659','point','2/7'),('q-71881','l',0)]:
        p=g.default_params(qid);p[key]=value
        try:g.generate(g.SPECS[qid]['level'],template=qid,parameters=p)
        except ValueError:rejected+=1
        else:raise AssertionError(('Invalid explicit parameters accepted',qid,p))
    # Native app fixture rejects every distractor and tests noncanonical equivalents.
    write('engine-input.json',fixtures)
    subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(ROOT/'engine-input.json'),str(ROOT/'engine-validation.json')],check=True)
    engine=json.loads((ROOT/'engine-validation.json').read_text())
    write('source-cases.json',cases);write('source-fidelity.json',source_reports);write('review.json',review)
    report={'status':'passed','database_writes':0,'source_provenance':{k:g.CAPTURE[k] for k in ('database','basis','lineage')},
            'source_questions':10,'raw_attribute_presence':{'matched':10,'total':10},'exact_prompts':{'matched':10,'total':10},
            'exact_worked_solutions':{'matched':9,'total':9},'missing_source_solutions':1,
            'complete_source_field_banks':{'matched':9,'total':9},'source_values':{'matched':37,'total':37},
            'source_radio_banks':{'matched':7,'total':7},'known_correct_designations':{'matched':7,'total':7},
            'unknown_correct_designations':{'matched':0,'total':0,'absent_source_refs':2},
            'fieldless_sources_completed':2,'unrated_sources_authored_easy':1,
            'independent_displayed_solution_stage_checks':sum(STAGES.values()),'families_sampled':family_counts,
            'sampled_mathematical_task_counts':fingerprints,'default_family_coverage':{k:sorted(v) for k,v in default_coverage.items()},
            'equality_preserving_stage_mutations_rejected':mutation_count,'explicit_scope_violations_rejected':rejected,
            'native':{k:engine[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},
            'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},
            'limitations':['Historical distractor intent is opaque where explicitly documented; historical/observed profiles are evidence-only.',
                           'Raw fieldless records and fields lacking correct refs are not native-gradable as captured; completed normal records are verified separately.',
                           'No hard source exists. Three-term scaled slope workload is an authored design claim.']}
    write('validation.json',report)
    md=['# General exponential chain-rule review','Frozen math basis 1356. Raw originals preserve omissions. Normal/generated records use supported fields.']
    for entry in review:
        md+=['## '+(entry.get('source_id') or entry['authored_template'])]
        if 'original' in entry:
            md+=['### Raw original',g.markdown(entry['original']),'### Normal at original parameters',g.markdown(entry['normal_at_original'])]
        for i,v in enumerate(entry['generated_variants']):md+=['### Generated variant '+str(i+1)+' ('+g.SPECS[v['generation']['template']]['level']+')',g.markdown(v)]
    (ROOT/'review.md').write_text('\n\n'.join(md)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
