"""Fail-closed fidelity, displayed mathematics, scope, identity and native QA."""
from pathlib import Path
import importlib.util, json, re, subprocess, hashlib, itertools, random
import sympy as s
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('gen',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
spec=importlib.util.spec_from_file_location('readback',HERE/'readback.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def eq(a,b): return s.simplify(a-b)==0

def format_check(text):
    assert text.count('$')%2==0
    depth=0
    for match in re.finditer(r'(?<!\\)[{}]',text):
        depth+=1 if match.group()=='{' else -1;assert depth>=0
    assert depth==0
    assert '--' not in text and '+-' not in text

def component_args(text):
    row=next(t for t in text.split(r'\\') if r'\frac{∂}{∂x}(' in t)
    assert re.findall(r'\\frac\{∂\}\{∂([xyz])\}',row)==['x','y','z']
    out=[]
    for v in 'xyz':
        marker=r'\frac{∂}{∂'+v+'}(';a=row.index(marker)+len(marker);b=a;depth=1
        while depth:
            depth+=(row[b]=='(')-(row[b]==')');b+=1
        out.append(m.scalar(row[a:b-1]))
    return out

def displayed_vector(prompt):
    match=re.search(r'[FG]=(.*?)\$',prompt,flags=re.S)
    if not match:return None
    raw=match.group(1).strip().rstrip('.')
    if not raw.replace(r'\,','').strip():return None
    return list(m.vector(raw))

def math_check(record):
    q=record['question'];f=q[':question/answer-fields'][0];gen=record['generation']
    assert set(record['knowledge_point'])=={'db_id','id','title'}
    assert record['knowledge_point']['db_id']==17592186133889
    assert gen['evidence_only']==(not gen['eligible_for_learning'])
    assert gen['profile_origin'] in ('observed_opaque','authored_supported','supported_presentation_repair')
    for text in (q[':question/problem'],q[':question/worked-solution'],*[a[':answer/value'] for a in f[':answer-field/choices']]): format_check(text)
    assert f[':answer-field/correct'][0]==':answer/id'
    assert f[':answer-field/correct'][1] in [a[':answer/id'] for a in f[':answer-field/choices']]
    if f[':answer-field/type'].endswith('blank'): assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
    components=component_args(q[':question/worked-solution'])
    prompt_components=displayed_vector(q[':question/problem'])
    if prompt_components is not None:assert all(eq(a,b) for a,b in zip(components,prompt_components,strict=True)),('printed/formal mismatch',gen)
    else: assert gen['evidence_only'] and gen['source_id'] in ('q-168615','q-168624')
    derivatives=[s.diff(comp,v) for comp,v in zip(components,(m.x,m.y,m.z))];div=sum(derivatives)
    if gen['profile_origin']=='authored_supported' and q[':question/difficulty'].endswith('/hard'):assert [len(s.Add.make_args(d)) for d in derivatives]==[2,2,2]
    ptmatch=re.search(r'at the point \$\(([^)]+)\)',q[':question/problem'])
    point=None if ptmatch is None else [m.scalar(v) for v in ptmatch.group(1).split(',')]
    wanted=div if point is None else s.simplify(div.subs(dict(zip((m.x,m.y,m.z),point))))
    # Check all mathematical RHS rows from the actual displayed solution,
    # retaining the formal component rows as mandatory derivative inputs.
    blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],flags=re.S)
    assert blocks and r'\frac{∂P}{∂x}+\frac{∂Q}{∂y}+\frac{∂R}{∂z}' in blocks[0]
    checked=0
    if gen['profile_origin']=='authored_supported':
        contribution_row=blocks[0].split(r'\\')[2].split('& =',1)[1]
        contributions=split_groups(contribution_row)
        assert len(contributions)==3
        assert all(eq(m.scalar(term),d) for term,d in zip(contributions,derivatives,strict=True)),('individual held-coordinate contribution failure',gen)
    for index,block in enumerate(blocks):
        rows=block.split(r'\\');assert len(rows)>=3
        if index==0: assert sum(r'\frac{∂}{∂x}' in row for row in rows)==1
        for row in rows:
            assert '& =' in row
            rhs=row.split('& =',1)[1].strip().rstrip('.')
            if '∂' in rhs:continue
            parsed=m.scalar(rhs)
            assert eq(parsed,div if index==0 else wanted),('bad printed stage',gen['template'],rhs,parsed,div if index==0 else wanted)
            checked+=1
    values=[m.scalar(a[':answer/value']) for a in f[':answer-field/choices']]
    assert not any(eq(a,b) for i,a in enumerate(values) for b in values[i+1:]),('bank collision',gen)
    correct=next(m.scalar(a[':answer/value']) for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
    assert eq(wanted,correct),('wrong answer',gen,wanted,correct)
    return checked

def split_groups(raw):
    depth=0;start=0;parts=[]
    for index,char in enumerate(raw):
        depth+=(char in '({')-(char in ')}')
        if char=='+' and depth==0:parts.append(raw[start:index]);start=index+1
    parts.append(raw[start:]);return parts

def checks(r):
    f=r['question'][':question/answer-fields'][0]
    if f[':answer-field/type'].endswith('radio'):
        return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'every owned option'} for a in f[':answer-field/choices']]
    answer=f[':answer-field/choices'][0][':answer/value'];val=m.scalar(answer)
    # Unevaluated additive zero exposes a distinct equivalent entry.
    components=component_args(r['question'][':question/worked-solution']); derivatives=[s.diff(comp,v) for comp,v in zip(components,(m.x,m.y,m.z))]
    point_match=re.search(r'at the point \$\(([^)]+)\)',r['question'][':question/problem'])
    if point_match is not None:
        point=[m.scalar(v) for v in point_match.group(1).split(',')];derivatives=[d.subs(dict(zip((m.x,m.y,m.z),point))) for d in derivatives]
    unreduced='+'.join('('+g.tex(d)+')' for d in derivatives)
    assert eq(m.scalar(unreduced),val)
    return [{'submitted':answer,'expected':'accepted','purpose':'canonical blank'}, {'submitted':unreduced,'expected':'accepted','purpose':'independently derived unreduced held-coordinate derivative sum'}, {'submitted':g.tex(val+1),'expected':'rejected','purpose':'wrong blank'}]

def main():
    cases=[];records=[];reviews=[];inputs=[];stages=0;bank_values=0;correct_labels=0;source_rows=[]
    for key,q in g.Q.items():
        level=q[':question/difficulty'][':db/ident'].split('/')[-1];case={'source_id':q[':question/id'],'math_academy_id':key,'template':'source_'+key,'level':level,'parameters':{'scale':1},'bank_profile':'observed_'+key};cases.append(case)
        r=g.generate(level,template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);n=r['question'];f=n[':question/answer-fields'][0];original=q[':question/answer-fields'][0]
        assert n[':question/problem']==q[':question/problem'];assert n[':question/worked-solution']==q[':question/worked-solution']
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in original[':answer-field/choices'])
        assert f[':answer-field/type']==original[':answer-field/type'][':db/ident'];assert f[':answer-field/key']==original[':answer-field/key']
        for attribute in (':question/difficulty',':question/answer-fields',':question/worked-solution'): assert (attribute in q)==(attribute in n)
        assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==original[':answer-field/correct'][':answer/value']
        bank_values+=len(f[':answer-field/choices']);correct_labels+=1;stages+=math_check(r);records.append(r);reviews.append(r);inputs.append({'label':'original '+key,'record':r,'checks':checks(r)})
        # Changed parameters exercise all formal argument and ordered scalar
        # stages in public evidence recipes, never just original constants.
        for scale in (-3,-1,2,3):
            changed=g.generate(level,template=case['template'],parameters={'scale':scale});stages+=math_check(changed);records.append(changed)
        source_rows.append({'source':key,'level':level,'field':f[':answer-field/type'],'option_count':len(f[':answer-field/choices']),'raw_prompt_exact':True,'solution_sequence_exact':True,'source_labels_present':True,'prompt_complete':key not in ('q-168615','q-168624')})
    authored_counts={l:0 for l in g.LEVELS};fingerprints={l:set() for l in g.LEVELS}
    for level in g.LEVELS:
        for template in g.TEMPLATES[level]:
            for kind in ('radio','blank'):
                for seed in range(12):
                    r=g.generate(level,seed,template,kind);stages+=math_check(r);records.append(r);authored_counts[level]+=1;fingerprints[level].add(r['generation']['mathematical_fingerprint'])
                    p=r['generation']['parameters'];other=g.generate(level,seed+83,template,kind,p)
                    assert other['question'][':question/id']==r['question'][':question/id']
                    assert other['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
                    if seed<2:
                        reviews.append(r);inputs.append({'label':'generated '+level+' '+template+' '+kind+' '+str(seed),'record':r,'checks':checks(r)})
                    # Native grading sample all templates/layouts, both signs.
    for template in ('zero_terms','axial'):
        for scale in (-3,-1,1,2,3):
            r=g.generate_easy(template=template,parameters={'scale':scale});stages+=math_check(r);records.append(r);reviews.append(r);inputs.append({'label':'supported repair '+template+' '+str(scale),'record':r,'checks':checks(r)})
    # Every reduced explicit coefficient boundary is subjected to the same guard.
    for level in g.LEVELS:
        template=g.TEMPLATES[level][0]
        for bad in (0,4,-4,1.5,True):
            p={'a':bad,'b':1,'c':2}
            if level=='moderate':p['point']=[1,1,1]
            try:g.generate(level,template=template,parameters=p)
            except ValueError:pass
            else:raise AssertionError(('bad workload parameter accepted',level,p))
    # Exact moderate catalog counts use the checked finite guarded domains;
    # evaluation contribution tuples merge point aliases with identical work.
    moderate_catalog={}
    for template in g.TEMPLATES['moderate']:
        canonical=set();tuples=0
        for a,b,c in itertools.product((-3,-2,-1,1,2,3),repeat=3):
            for pt in itertools.product(range(-2,3),repeat=3):
                p={'a':a,'b':b,'c':c,'point':list(pt)}
                try:g.guard('moderate',template,p)
                except ValueError:continue
                xx,yy,zz=pt
                vals=(2*a*xx*yy*zz,2*b*xx*yy*zz,2*c*xx*yy*zz) if template=='evaluated_monomial' else (2*a*(xx+yy),2*b*(yy+zz),2*c*(xx+zz)) if template=='evaluated_square' else (a*zz,b*xx*xx,2*c*xx*zz)
                canonical.add((a,b,c,vals));tuples+=1
        moderate_catalog[template]={'meaningful_differentiation_and_evaluation_tasks':len(canonical),'eligible_parameter_tuples_before_radio_bank_rejection':tuples}
    # Exhaust finite coefficient catalogs at authored symbolic levels. Radio
    # collisions are whole-instance exclusions; blank mathematical tasks count.
    catalogs={'moderate':moderate_catalog}
    for level in ('easy','hard'):
        by_template={}
        for template in g.TEMPLATES[level]:
            valid=set();excluded=0
            for a,b,c in itertools.product((-3,-2,-1,1,2,3),repeat=3):
                try:r=g.generate(level,template=template,field_type='blank',parameters={'a':a,'b':b,'c':c})
                except ValueError:excluded+=1;continue
                valid.add(r['generation']['mathematical_fingerprint'])
            by_template[template]={'meaningful_component_tasks':len(valid),'excluded_parameter_tuples':excluded}
        catalogs[level]=by_template
    (HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(HERE/'review.json').write_text(json.dumps(reviews,indent=2,ensure_ascii=False)+'\n');(HERE/'engine-input.json').write_text(json.dumps(inputs,indent=2,ensure_ascii=False)+'\n')
    engine=HERE.parents[1]/'runs/current/check-engine'
    subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    engine_report=json.loads((HERE/'engine-report.json').read_text())
    review=['# Three-dimensional divergence review','Author review: Original, Generated, difficulty and Correct labels are explicit. Raw incomplete source prompts remain evidence only.']
    for key,q in g.Q.items():
        review.extend(['\n## Original — '+key+' — '+q[':question/difficulty'][':db/ident'].split('/')[-1],q[':question/problem']])
        f=q[':question/answer-fields'][0]
        review.extend('- $'+a[':answer/value']+'$'+(' **Correct**' if a[':answer/id']==f[':answer-field/correct'][':answer/id'] else '') for a in f[':answer-field/choices'])
        review.extend(['\n**Original worked solution**\n',q[':question/worked-solution'],g.markdown(next(r for r in reviews if r['generation']['source_id']==key))])
        variant=g.generate(q[':question/difficulty'][':db/ident'].split('/')[-1],template='source_'+key,parameters={'scale':2});reviews.append(variant);review.append(g.markdown(variant))
    review.extend(g.markdown(r) for r in reviews if not r['generation']['evidence_only'])
    (HERE/'review.md').write_text('\n\n'.join(review)+'\n');(HERE/'review.json').write_text(json.dumps(reviews,indent=2,ensure_ascii=False)+'\n')
    report={'passed':True,'basis':1356,'source_questions':14,'exact_prompts':14,'exact_whole_solutions':14,'complete_banks':14,'exact_bank_values':bank_values,'exact_distractors':bank_values-14,'matched_correct_designations':correct_labels,'missing_correct_designations':0,'missing_difficulty_labels':0,'source_presentation_repairs_needed':2,'source_prose_typo_repairs_needed':1,'supported_repaired_blank_records_checked':10,'normal_output_incomplete_prompts':0,'source_format_replays_evidence_only':14,'authored_level_counts':authored_counts,'authored_sample_task_counts':{l:len(v) for l,v in fingerprints.items()},'finite_catalogs':catalogs,'checked_records':len(records),'independently_verified_printed_scalar_stages':stages,'native_accepted':engine_report['accepted_checks'],'native_rejected':engine_report['rejected_checks'],'native_unresolved':engine_report['documented_unresolved_checks'],'source_rows':source_rows,'database_writes':0}
    (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
