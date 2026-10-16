"""Inspect cached visible MA HTML and public JS; never export profile data."""
import ctypes
import gzip
import hashlib
import json
from pathlib import Path
import re
import struct

ROOT = Path(__file__).resolve().parent
REPO = Path('/home/jake/Developer/Course_Academy')
TARGETS = ['122027','122033','124400','124403','73003','73005','73014']
MAGIC = bytes.fromhex('d8410d97456ffaf4')
decoder = ctypes.CDLL('libbrotlidec.so.1').BrotliDecoderDecompress
decoder.argtypes = [ctypes.c_size_t,ctypes.c_void_p,ctypes.POINTER(ctypes.c_size_t),ctypes.c_void_p]
decoder.restype = ctypes.c_int

def read_entry(path):
    data = path.read_bytes()
    if len(data)<48:
        return
    keylen = struct.unpack_from('<I',data,12)[0]
    key = data[24:24+keylen].decode(errors='replace')
    if not re.match(r'\d+/\d+/https://mathacademy\.com/(?:learn(?:\?|$)|topics/|js/task-answers\.js)',key):
        return
    tail = data.find(MAGIC,24+keylen)
    if tail<0:
        return
    body = data[24+keylen:tail]
    metadata = data[tail+24:-24]
    if b'content-encoding:br' in metadata:
        out=ctypes.create_string_buffer(20000000)
        n=ctypes.c_size_t(len(out))
        if decoder(len(body),body,ctypes.byref(n),out)!=1:
            return
        body=out.raw[:n.value]
    elif b'content-encoding:gzip' in metadata:
        body=gzip.decompress(body)
    return key,body,hashlib.sha256(data).hexdigest()

def main():
    profiles=[REPO/'.local/question_capture/browser-profile']
    profiles+=list((REPO/'.local/question_capture-workers').glob('*/browser-profile'))
    result={'selection':'cached /learn, /topics HTML and public task-answers JS only; no internal API responses or credentials', 'profiles':[], 'visible_html':[], 'matching_question_html':[], 'renderer':[]}
    for profile in profiles:
        cache=profile/'Default/Cache/Cache_Data'
        result['profiles'].append({'path':str(profile.relative_to(REPO)), 'history_database_present':(profile/'Default/History').exists()})
        for p in cache.glob('*_0'):
            try:
                entry=read_entry(p)
                if not entry:
                    continue
                key,body,sha=entry
                if key.endswith('/js/task-answers.js'):
                    name='task-answers-'+hashlib.sha256(body).hexdigest()[:16]+'.js'
                    (ROOT/name).write_bytes(body)
                    result['renderer'].append({'source_url':key.split('/',2)[2], 'cache_sha256':sha, 'body_sha256':hashlib.sha256(body).hexdigest(),'source_path':name})
                    continue
                item={'source_url':key.split('/',2)[2], 'cache_sha256':sha,'body_bytes':len(body),'target_ids':[q for q in TARGETS if re.search(rb'(?:question-|questionid=["\x27])'+q.encode()+rb'\b',body,re.I)]}
                result['visible_html'].append(item)
                if item['target_ids']:
                    name='cached-visible-'+hashlib.sha256(body).hexdigest()[:16]+'.html'
                    (ROOT/name).write_bytes(body)
                    result['matching_question_html'].append({**item,'source_path':name})
            except Exception as e:
                result.setdefault('decode_errors',[]).append({'file':str(p.relative_to(REPO)),'error':str(e)})
    (ROOT/'cache-inspection.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({'cached_visible_html':len(result['visible_html']), 'matching_question_html':len(result['matching_question_html']),'public_renderers':len(result['renderer']), 'errors':len(result.get('decode_errors',[]))}))

if __name__=='__main__':
    main()
