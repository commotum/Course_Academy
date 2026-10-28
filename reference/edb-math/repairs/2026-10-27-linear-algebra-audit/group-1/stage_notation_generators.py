import difflib,hashlib,json,re,shutil,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R));from scripts.generator_packages import package_digest
D=json.loads((H/'current.json').read_text());G=dict(D['generators']);wanted=[17592186119805,17592186119806,17592186119854,17592186119857];candidates=[];diff=[]
helper=r'''"""Source vector fonts at the TeX authoring boundary, before content identities."""
import re
from math_format import MATH

def _tex(value, names):
    protected=[]
    for command in re.finditer(r'\\(?:mathbf|mathbb|text|operatorname|mathrm)\s*\{',value):
        i=command.end();depth=1
        while depth and i<len(value):
            if value[i]=='\\' and i+1<len(value) and value[i+1] in '{}':i+=2;continue
            depth+=(value[i]=='{')-(value[i]=='}');i+=1
        if not depth:protected.append((command.start(),i))
    def replace(match):
        if match[0] not in names or any(a<=match.start()<b for a,b in protected):return match[0]
        # x_i denotes a scalar component/coefficient; x denotes the vector.
        if match[0]=='x' and re.match(r'\s*\}?\s*_',value[match.end():]):return match[0]
        return r'\mathbf{'+match[0]+'}'
    return re.sub(r'(?<![A-Za-z\\])([abx])(?![A-Za-z])',replace,value)

def vector_prose(value,names='ab'):
    return MATH.sub(lambda match:_tex(match[0],names),value)

def plain_vector_prose(value):
    # Parsing mathematical parameters must ignore authored font changes.
    return MATH.sub(lambda match:re.sub(r'\\mathbf\{([abx])\}',r'\1',match[0]),value)
'''
for kp in wanted:
 old=Path('/media/jake/SSD/EDB/math')/G[kp][':question-generator/script'];manifest=json.loads((old.parent/'generator-package.json').read_text());dest=H/('generator-notation-'+str(kp));dest.mkdir(exist_ok=True)
 for name in manifest['files']:
  target=dest/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(old.parent/name,target);target.chmod(0o644)
 shutil.copyfile(R/'scripts/question_capture/math_format.py',dest/'math_format.py');files=list(manifest['files']);files+=['math_format.py']if'math_format.py'not in files else[]
 p=dest/old.name;s=p.read_text();before=s
 s=re.sub(r"VERSION\s*=\s*'([^']+)'",lambda m:"VERSION='"+m[1]+"-notation-v1'",s,count=1)
 if kp!=17592186119857:
  s=s.replace('import sympy as sp','import sympy as sp\nfrom vector_notation import vector_prose, plain_vector_prose',1);(dest/'vector_notation.py').write_text(helper);files.append('vector_notation.py')
 if kp==17592186119805:
  oldreturn='    return problem,sol,correct,bank';assert oldreturn in s;s=s.replace(oldreturn,oldreturn,1)
  start=s.index('def render(sid,p):');end=s.index('def fingerprint(',start);chunk=s[start:end]
  chunk=chunk.replace('{a}_{1}',r'{\mathbf{a}}_{1}').replace('{a}_{2}',r'{\mathbf{a}}_{2}')
  chunk=chunk.replace("('0' if moderate","(r'\\mathbf{0}' if moderate")
  chunk=chunk.replace('=b',r'=\mathbf{b}').replace("else 'b'", "else r'\\mathbf{b}'").replace(r'\,b=',r'\,\mathbf{b}=')
  s=s[:start]+chunk+s[end:]
  s=s.replace("text=q[':question/problem'];a,u,*bs=vectors(text)","text=plain_vector_prose(q[':question/problem']);a,u,*bs=vectors(text)")
  oldid='json.dumps([sid,p,bank],sort_keys=True)';assert oldid in s;s=s.replace(oldid,'json.dumps([VERSION,sid,p,bank],sort_keys=True)',1)
 elif kp==17592186119806:
  s=s.replace('def parse_problem(problem):\n','def parse_problem(problem):\n    problem=plain_vector_prose(problem)\n',1)
  marker='    bank=sorted(map(tex,values));content=';assert marker in s;s=s.replace(marker,"    problem=vector_prose(problem,'abx');solution=vector_prose(solution,'abx')\n"+marker,1)
 elif kp==17592186119854:
  marker=' return normalize_prose(p),normalize_prose(s)';assert marker in s;s=s.replace(marker,' return normalize_prose(vector_prose(p)),normalize_prose(vector_prose(s))',1)
 else:
  # Only authored mathematical labels change, before both ID derivation paths.
  s=s.replace("r'B=\\left\\{'","r'\\mathcal{B}=\\left\\{'")
  s=s.replace("'a_{'+str", "r'\\mathbf{a}_{'+str")
  s=s.replace("Find a basis $B$",r"Find a basis $\\mathcal{B}$")
  s=s.replace("giving $B=\\\\{",r"giving $\\mathcal{B}=\\{")
 p.write_text(s);assert before!=s
 evidence={'kind':'Source-backed notation repair before authored content identities','basis_t':9047,'kp':kp,'changes':'Restore source vector boldface; for pivot-basis package restore calligraphic basis name in prompts, solutions and all math choice values. Numeric entries, algorithms, sampling domains and bank recipes are unchanged.','identity':'Version bumped; KP19805identity payload explicitly includes the version. All newly formatted content receives new authored identities; existing EDB IDs are untouched.','source_replay':'Original-parameter evidence replay now retains repaired source notation and is documented as authored presentation repair, not byte-identical observation.'};(dest/'repair-evidence.json').write_text(json.dumps(evidence,indent=2));files.append('repair-evidence.json');files=sorted(set(files));deps=manifest['dependencies'];digest=package_digest(dest,old.name,files,dependencies=deps)
 candidates.append({'kp':kp,'old_reference':G[kp][':question-generator/script'],'old_entity':G[kp][':db/id'],'directory':str(dest),'entrypoint':old.name,'files':files,'dependencies':deps,'approved_digest':digest});diff.extend(difflib.unified_diff(before.splitlines(True),s.splitlines(True),fromfile=str(old),tofile=str(p)))
(H/'notation-generator.diff').write_text(''.join(diff));(H/'generator-candidates.json').write_text(json.dumps(candidates,indent=2));print('staged',len(candidates),'packages')
