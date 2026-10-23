import os,pathlib,importlib.util,json,re,hashlib,difflib
os.environ['MPLCONFIGDIR']=str(pathlib.Path('mpl-cache').resolve())
s=importlib.util.spec_from_file_location('g','runtime/17592186129197.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
a=json.load(open('../workspace/17592186129197/reference/replenishment/basis-2715/generated.json'))[0];m=a['generation'];stored=next(q for q in json.load(open('../source/inventory.json'))['questions'] if q[':question/id']==a['question'][':question/id']);plot=g.plot;g.plot=lambda *args:m['plot'];r=g.generate('easy',m['seed'],template=m['template'],parameters=m['parameters'])
old_image=re.search(r'!\[\]\((.*?)\)',stored[':question/worked-solution']).group(1);r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace(m['plot'],old_image)
fresh=pathlib.Path(plot(m['template'],m['parameters'],g.model(m['template'],m['parameters'])));canonical=pathlib.Path('/media/jake/SSD/EDB/math')/old_image
print('image',fresh,canonical, canonical.exists());print('hashes',hashlib.sha256(fresh.read_bytes()).hexdigest(),hashlib.sha256(canonical.read_bytes()).hexdigest())
print('meta',r['generation']==m,'ids',r['question'][':question/id']==stored[':question/id'],'prompt',r['question'][':question/problem']==stored[':question/problem'],'solution',r['question'][':question/worked-solution']==stored[':question/worked-solution'])
print('\n'.join(difflib.unified_diff(r['question'][':question/worked-solution'].splitlines(),stored[':question/worked-solution'].splitlines()))[:5000])
