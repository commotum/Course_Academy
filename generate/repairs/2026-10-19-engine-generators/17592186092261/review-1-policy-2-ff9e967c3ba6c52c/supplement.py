from review import *
rs=[];pairs=[];grades=[]
for qid in ['q-48659','q-107463']:
 p=g.default_params(qid);pp={**p,'point':'0' if qid=='q-107463' else str(-s.Rational(p['point']))}
 a=g.generate(g.SPECS[qid]['level'],seed=877131,template=qid,parameters=p);b=g.generate(g.SPECS[qid]['level'],seed=877131,template=qid,parameters=pp);rs.extend([a,b]);fa,va=expected(a);fb,vb=expected(b)
 pairs.append({'kind':'relevant','change':'point only','template':qid,'before':a,'after':b,'before_response':str(va),'after_response':str(vb),'passed':not eq(va,vb)})
 for tag,r in [('before',a),('after',b)]:
  _,v=expected(r);fld=r['question'][':question/answer-fields'][0]
  grades.append({'label':qid+' point '+tag,'record':r,'checks':[{'submitted_answer_id':an[':answer/id'],'expected':'accepted' if eq(parse(an[':answer/value']),v) else 'rejected','purpose':'point change recomputes tangent slope/line'} for an in fld[':answer-field/choices']]})
# Canonical multiplier dependency exercised by the closest scaled profile (degree2);
# exact canonical scaled-linear is absent; no edited package/synthetic key is used.
save('point-pairs.json',pairs);save('point-grader-input.json',grades)
cmd=[str(ROOT/'generate/runs/current/check-engine'),str(E/'point-grader-input.json'),str(E/'point-grading.json')];r=subprocess.run(cmd,capture_output=True,text=True);(E/'point-grading.log').write_text(json.dumps(cmd)+'\n'+r.stdout+r.stderr)
# Render records not included by the preview tool's default six-record limit, plus point pairs and grading failure instance.
old=json.load(open('render-records.json'));failure=next(c['record'] for c in json.load(open('grader-input.json')) if c['label']=='record-82');render=old[6:]+rs+[failure];save('render-extra-records.json',render)
cmd=[sys.executable,str(ROOT/'generate/pipeline/render_preview.py'),'--input',str(E/'render-extra-records.json'),'--output',str(E/'render-extra'),'--asset-root',str(E),'--limit',str(len(render))]
r=subprocess.run(cmd,capture_output=True,text=True);(E/'render-extra.log').write_text(json.dumps(cmd)+'\n'+r.stdout+r.stderr);print(r.returncode,r.stdout[-500:],r.stderr[-1000:])
# Targeted failure has both key-normal notation and log-power equivalent for a clear differential.
checks=[{'submitted':r'-15x^2\ln(4)','expected':'accepted','purpose':'same source-base coefficient accepted'},{'submitted':r'-30x^2\ln(2)','expected':'unresolved','purpose':'mathematically valid log-power equivalent is a demonstrated defect, desired accepted'}]
save('grading-failure-input.json',[{'label':'base4 coefficient equivalent','record':failure,'checks':checks}]);cmd=[str(ROOT/'generate/runs/current/check-engine'),str(E/'grading-failure-input.json'),str(E/'grading-failure.json')];r=subprocess.run(cmd,capture_output=True,text=True);(E/'grading-failure.log').write_text(json.dumps(cmd)+'\n'+r.stdout+r.stderr);print(r.returncode,r.stdout,r.stderr[:1000])
