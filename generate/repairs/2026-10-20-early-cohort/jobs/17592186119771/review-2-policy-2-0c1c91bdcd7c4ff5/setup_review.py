import pathlib,json,shutil,hashlib
E=pathlib.Path(__file__).resolve().parent;P=E.parent/'review-1-policy-2-0e9bf2a26bc3c6cc'
for f in ['review_checks.py','test_single_witness.py']:
 shutil.copyfile(P/f,E/f)
p=E/'review_checks.py';s=p.read_text();s=s.replace("g.batch('easy',12,739)+[g.generate('easy',s) for s in range(2401,2449)]","g.batch('easy',18,9187)+[g.generate('easy',s) for s in range(8501,8513)]")
s=s.replace("base=[[2,0,0],[3,-4,0],[5,0,6]]","base=[[-2,0,0],[6,-1,0],[0,0,0]]").replace("irrelevant=[[0,0,0],[-3,7,0],[-5,0,-8]]","irrelevant=[[0,0,0],[-6,7,0],[0,0,-8]]")
s=s.replace("'preflight':'absent','retained_findings':[]","'preflight':'../repair-preflight.json','retained_findings':['dbcd1ab741c06c08a3a5']")
s=s.replace("'rule':'level_guard and catalog require at least ceil(n(n-1)/4) nonzero off-diagonal entries; all sole-witness 3x3 triangular matrices excluded.'","'rule':'Current generator must accept all these formerly rejected sparse cases.'")
s=s.replace("'Independent source account saved before package inspection. Independent sampling (60 records), exact batch (5), 4 controlled records, 11 source replays, packaging/relocation and parameter rejection completed. Sparse 3x3 canonical and sole-far-witness rejection demonstrated. Grader inputs prepared. Next: native grading, delivery filtering, actual UI rendering and selection/probe analysis.\\n'","'Source account verified before package inspection. Current sampling (30), exact batch (5), sparse counterfactuals (4), 11 source replays, relocation and rejection checks complete. Next native grading, delivery, rendering and changed support-domain checks.\\n'")
p.write_text(s)
(E/'provenance.json').write_text(json.dumps({'previous_review':str(P),'reused_scripts':['review_checks.py','test_single_witness.py'],'changes':'Fresh seeds, smaller regression sample with full easy support coverage, sparse controlled counterfactuals, current preflight references and assertions updated. Earlier source account verified first.','old_entrypoint':str(P/'relocated/17592186119771.py')},indent=2)+'\n')
