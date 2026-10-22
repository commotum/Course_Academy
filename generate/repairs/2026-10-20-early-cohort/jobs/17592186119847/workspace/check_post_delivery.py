"""Independent visible-record cue, counterfactual and grader preparation checks."""
import collections,json
from check_repair import E,g,inspect,save
from check_variation import summarize

def main():
    raw=[];accepted=[]
    for level in ['easy','moderate']:
        raw+=json.loads((E/f'root-cause/{level}-delivery-input.json').read_text())
        accepted+=json.loads((E/f'root-cause/delivery-{level}/accepted.json').read_text())
    before=summarize(raw);after=summarize(accepted);assert set(before)==set(after)
    surface_cues={}
    for stage,records in [('before',raw),('after',accepted)]:
        surface_cues[stage]={}
        for profile in [p for ps in g.PROFILES.values() for p in ps]:
            facts=[inspect(r) for r in records if r['generation']['bank_profile']==profile]
            # Easy count=pivots is the instructional definition. On moderate,
            # these isolated prompt numerals are insufficient answer rules.
            cues={cue:sum(f['rank']==f[cue] for f in facts) for cue in ['rows','columns','count']}
            if profile in g.PROFILES['moderate']:
                assert all(hits<len(facts) for hits in cues.values()),(stage,profile,cues)
            surface_cues[stage][profile]={'attempts':len(facts),'numeral_shortcut_successes':cues}
    subgroups={}
    for stage,records in [('before',raw),('after',accepted)]:
        collision=[r for r in records if r['generation']['bank_extension'].startswith('collision')]
        groups=collections.defaultdict(list)
        for r in collision:groups[r['generation']['bank_profile']].append(inspect(r))
        subgroups[stage]={}
        for profile,facts in groups.items():
            positions=collections.Counter(f['position'] for f in facts)
            orders=collections.Counter(f['numerical_order'] for f in facts)
            if stage=='before':
                assert len(positions)>1,(stage,profile,'fixed position')
                assert len(orders)>1,(stage,profile,'fixed numerical order')
            subgroups[stage][profile]={'n':len(facts),'positions':dict(positions),'orders':dict(orders)}
    # Cross-profile content duplicates are one learner-visible question. Check
    # the collision branch separately in each profile through the same filter.
    isolated={}
    for profile in subgroups['before']:
        records=json.loads((E/f'root-cause/isolated-{profile}/accepted.json').read_text())
        facts=[inspect(r) for r in records]
        positions=collections.Counter(f['position'] for f in facts)
        orders=collections.Counter(f['numerical_order'] for f in facts)
        assert len(positions)>1 and len(orders)>1,(profile,positions,orders)
        isolated[profile]={'accepted':len(records),'positions':dict(positions),'orders':dict(orders)}
    # Check relevant changes with dimensions, profile and RNG held constant.
    controls=[];control_records=[]
    for level,profiles in g.PROFILES.items():
        for profile in profiles:
            rs=[g.generate(level,17,parameters=dict(name='A',rows=6,columns=8,
                 count=c,kind='pivot' if level=='easy' else 'non-pivot'),bank_profile=profile) for c in (2,3,4)]
            facts=[inspect(r) for r in rs]
            assert [f['rank'] for f in facts]==([2,3,4] if level=='easy' else [6,5,4])
            controls.append({'profile':profile,'facts':facts});control_records+=rs
    # Full-row-rank and rank=nonpivots survive actual publisher filtering under
    # every moderate profile (including complete normalized records for grading).
    for profile in g.PROFILES['moderate']:
        group=[inspect(r) for r in json.loads((E/f'root-cause/isolated-{profile}/accepted.json').read_text())]
        assert any((f['rows'],f['columns'],f['count'])==(4,7,3) for f in group)
        assert any((f['rows'],f['columns'],f['count'])==(3,4,2) for f in group)
    requested=json.loads((E/'root-cause/requested-five.json').read_text())
    replay=json.loads((E/'validation-records.json').read_text())[:11]
    restrictions=json.loads((E/'root-cause/restriction-records.json').read_text())[:12]
    normalized=[]
    for profile in [p for ps in g.PROFILES.values() for p in ps]:
        group=[r for r in accepted if r['generation']['bank_profile']==profile]
        normalized+=group[:2]
        normalized += [r for r in group if (inspect(r)['rows'],inspect(r)['columns'],inspect(r)['count']) in [(4,7,3),(3,4,2)]]
    grading=[]
    for r in replay+restrictions+control_records+requested+normalized:
        fact=inspect(r);field=r['question'][':question/answer-fields'][0]
        grading.append({'label':r['question'][':question/id'],'record':r,'checks':[
          {'field_index':0,'submitted_answer_id':a[':answer/id'],
           'expected':'accepted' if int(a[':answer/value'])==fact['rank'] else 'rejected',
           'purpose':'Visible pivot/nonpivot count oracle, all correct/wrong choices'}
           for a in field[':answer-field/choices']]})
    save('root-cause/grader-input.json',grading)
    render=requested[:1]+[next(r for r in accepted if
             (inspect(r)['rows'],inspect(r)['columns'],inspect(r)['count'])==p) for p in [(4,7,3),(3,4,2)]]
    save('root-cause/render-records.json',render)
    save('root-cause/pedagogical-variation.json',{'status':'pass','before':before,'after':after,
         'collision_subgroups':subgroups,'isolated_profile_delivery':isolated,'surface_cues':surface_cues,'controls':controls,
         'generator_rejection':'Only out-of-bounds or mathematically infeasible ranks are rejected; distinct banks constructed afterward.',
         'delivery_counts':{'input':len(raw),'accepted':len(accepted)},
         'limits':['Finite 12 easy/98 moderate semantic tasks; cosmetic differences excluded from capacity.',
          'Low rank constrains negative-distance distractors; no claim of uniform numerical order.',
          'Easy rank=pivots is the intended definition, not an incidental count-reading cue.',
          'Moderate count grid changes correct rank at fixed rows/columns; fixed profile is insufficient.',
          'check_delivery uses captured basis 5404, not live learner history. question_selection.rs:122-190 uses difficulty weights and seeded draws without key/profile; unconfigured selection uses first eligible entity. Actual per-learner received coverage is untested.']})
    print(json.dumps({'status':'pass','input':len(raw),'accepted':len(accepted),'profiles':len(after),
                     'collision_profiles':len(subgroups['after']),'grader_records':len(grading),'render_records':len(render)}))

if __name__=='__main__':main()
