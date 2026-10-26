import importlib.util,json,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3]
if len(sys.argv)>1:
 p=Path(sys.argv[1]);sys.path.insert(0,str(p.parent));s=importlib.util.spec_from_file_location('interest_generator',p);g=importlib.util.module_from_spec(s);s.loader.exec_module(g);rs=g.generate(10,37);Path(sys.argv[2]).write_text(json.dumps(rs,indent=2)+'\n');sys.exit()
sys.path.insert(0,str(R));from scripts.generator_packages import verify_package
from scripts.generator_publish import validate_question
reports=[];samples=[]
for reg in json.loads((H/'generators.json').read_text()):
 p=Path('/media/jake/SSD/EDB/math')/reg[':question-generator/script'];pkg=verify_package(p.parent);out=H/('generator-'+str(reg[':db/id'])+'.json');subprocess.run([sys.executable,'-B',str(Path(__file__).resolve()),str(p),str(out)],check=True,capture_output=True,text=True);rs=json.loads(out.read_text());assert len(rs)==10
 for rec in rs:validate_question(rec['question'])
 samples.extend(rs);reports.append({'generator_entity':reg[':db/id'],'script':reg[':question-generator/script'],'package_sha256':pkg.digest,'sampled_records':10,'seed':37,'shared_publication_validation_passed':True,'changes_required':False})
(H/'generator-verification.json').write_text(json.dumps(reports,indent=2)+'\n');(H/'generator-samples.json').write_text(json.dumps(samples,indent=2)+'\n');print('Verified three unchanged generator packages and 30 fresh records with the shared publication validator')
