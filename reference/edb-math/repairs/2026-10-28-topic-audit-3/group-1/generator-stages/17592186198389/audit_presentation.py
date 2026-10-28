"""Audited presentation boundaries; raw source evidence remains separate."""
import hashlib,re
from pathlib import Path
from math_format import normalize_prose,normalize_tex,MATH

def prose(value):return normalize_prose(value) if value is not None else None

def problem(value):
    value=prose(value)
    # A whole displayed task integral after an explicit calculation/setup cue.
    # Assumptions, small integral references, banks and blank fragments stay inline.
    def replace(m):
        if m[0].startswith(('$$',r'\[',r'\(')):return m[0]
        body=m[0][1:-1].strip();prefix=value[max(0,m.start()-90):m.start()]
        if not re.match(r'(?:\\displaystyle\s*)?(?:\{?\\(?:int|iint|iiint|oint)|[∫∬∭∮])',body):return m[0]
        if not re.search(r'(?:[Ee]valuate|[Cc]alculate|[Ww]hat is|[Ee]xpress(?: the following)?(?: triple)? integral|[Ff]ind the (?:following )?(?:line |double |triple )?integral)\s*$',prefix):return m[0]
        return '\n\n$$\n'+body+'\n$$\n\n'
    return MATH.sub(replace,value)

def values(bank):return [normalize_tex(v) for v in bank]

def question(q):
    q[':question/problem']=problem(q[':question/problem'])
    if ':question/worked-solution'in q:q[':question/worked-solution']=prose(q[':question/worked-solution'])
    return q

def identity_material(value):
    if isinstance(value,dict):return {k:identity_material(v)for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [identity_material(v)for v in value]
    if not isinstance(value,str):return value
    def replace(m):
        p=Path(m[1])
        if not p.is_file():return m[0]
        return m[0][:m[0].rfind('](')+2]+'sha256:'+hashlib.sha256(p.read_bytes()).hexdigest()+')'
    return re.sub(r'!\[[^\]]*\]\(([^)]+)\)',replace,value)


def asset_output(path):
    # Immutable packages never write generated plots or caches into themselves.
    import os,tempfile
    base=Path(os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR',str(Path(tempfile.gettempdir())/'course-academy-generator-assets')))
    result=base / '17592186198389' / Path(path).name
    result.parent.mkdir(parents=True,exist_ok=True)
    return result
