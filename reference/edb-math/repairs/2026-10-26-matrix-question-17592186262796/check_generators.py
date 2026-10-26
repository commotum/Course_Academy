import importlib.util,json,re,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3]
if len(sys.argv)>1:
 p=Path(sys.argv[1]);sys.path.insert(0,str(p.parent));spec=importlib.util.spec_from_file_location('scoped_generator',p);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g);out=[]
 for name,t in g.TEMPLATES.items():
  levels=t.get('levels',[t.get('level')])if isinstance(t,dict)else[t[0]]
  for level in levels:
   for seed in [11,39]:
    out.append(g.generate(level,seed=seed,template=name))
 Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n');print('generated',len(out));sys.exit()
sys.path[:0]=[str(H),str(R/'scripts')];from check_math import solve,scalar
from question_capture.math_format import MATH,_matrix_layouts
from generator_packages import verify_package
records=[];report=[]
for reg in json.loads((H/'generators.json').read_text()):
 p=Path('/media/jake/SSD/EDB/math')/reg[':question-generator/script'];package=verify_package(p.parent);output=H/('generator-'+str(reg[':db/id'])+'.json');subprocess.run([sys.executable,'-B',str(Path(__file__).resolve()),str(p),str(output)],check=True,capture_output=True,text=True);rs=json.loads(output.read_text())
 for r in rs:
  q=r['question'];q[':db/id']=-len(records)-1;_,_,expected,_=solve(q,r['knowledge_point']['db_id']==17592186059750)
  for attr in [':question/problem',':question/worked-solution']:
   for m in MATH.finditer(q.get(attr,'')):assert _matrix_layouts(m[0])==m[0],(p,attr,'malformed fenced matrix')
  f=q[':question/answer-fields'][0];correct=f[':answer-field/correct'][1];choice=next(a for a in f[':answer-field/choices']if a[':answer/id']==correct);import sympy as s;assert s.simplify(scalar(choice[':answer/value'].split('=')[-1])-expected)==0
  q.pop(':db/id');records.append(r)
 report.append({'generator':reg[':db/id'],'script':reg[':question-generator/script'],'verified_package_sha256':package.digest,'sampled_records':len(rs),'all_supported_template_levels':True,'seeds':[11,39],'matrix_notation_normalized':True,'independent_math_passed':True})
(H/'generator-check.json').write_text(json.dumps(report,indent=2)+'\n');(H/'generator-samples.json').write_text(json.dumps(records,indent=2)+'\n');print('Verified current generators:',len(report),'fresh records:',len(records))
