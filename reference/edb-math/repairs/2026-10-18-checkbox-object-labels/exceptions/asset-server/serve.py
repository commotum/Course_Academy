"""Temporary read-only canonical-image server for checkbox render verification."""
from __future__ import annotations
import datetime,json,mimetypes,os,re,signal,sys,threading
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs,urlsplit

HERE=Path(__file__).resolve().parent
MATH_ROOT=Path('/media/jake/SSD/EDB/math').resolve()
IMAGE_ROOT=(MATH_ROOT/'images').resolve()
CANONICAL=re.compile(r'images/([0-9a-f]{2})/([0-9a-f]{64})\.(png|jpg|jpeg|gif|webp|svg)\Z')
LOG_LOCK=threading.Lock()

class Handler(BaseHTTPRequestHandler):
    server_version='ReadOnlyCheckboxAssets/1.0'
    def log_message(self,format,*args):
        pass
    def record(self,status,path=None):
        record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':status,'path':path}
        with LOG_LOCK:
            with (HERE/'requests.jsonl').open('a') as output:output.write(json.dumps(record)+'\n')
    def reject(self,status):
        self.send_response(status);self.send_header('Content-Length','0');self.end_headers();self.record(status)
    def do_GET(self):
        request=urlsplit(self.path)
        if request.path!='/api/asset':return self.reject(404)
        try:query=parse_qs(request.query,keep_blank_values=True,strict_parsing=True)
        except ValueError:return self.reject(400)
        if set(query)!={'path'} or len(query['path'])!=1:return self.reject(400)
        requested=query['path'][0]
        # Both the app's normal relative canonical references and a canonical
        # absolute image path resolve to the same strictly bounded image store.
        if requested.startswith(str(MATH_ROOT)+'/'):requested=requested[len(str(MATH_ROOT))+1:]
        match=CANONICAL.fullmatch(requested)
        if not match or match[1]!=match[2][:2]:return self.reject(403)
        candidate=(MATH_ROOT/requested).resolve()
        if not candidate.is_relative_to(IMAGE_ROOT):return self.reject(403)
        try:
            if not candidate.is_file():return self.reject(404)
            data=candidate.read_bytes()
        except (OSError,ValueError):return self.reject(404)
        self.send_response(200)
        self.send_header('Content-Type',mimetypes.guess_type(candidate.name)[0]or'application/octet-stream')
        self.send_header('Content-Length',str(len(data)))
        self.send_header('Cache-Control','public, max-age=31536000, immutable')
        self.send_header('X-Content-Type-Options','nosniff')
        self.end_headers()
        try:self.wfile.write(data)
        except (BrokenPipeError,ConnectionResetError):pass
        self.record(200,requested)
    def do_POST(self):self.reject(405)
    def do_PUT(self):self.reject(405)
    def do_DELETE(self):self.reject(405)
    def do_PATCH(self):self.reject(405)
    def do_HEAD(self):self.reject(405)

server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
server.daemon_threads=True
info={'status':'running','pid':os.getpid(),'host':'127.0.0.1','port':server.server_address[1],'origin':f'http://127.0.0.1:{server.server_address[1]}','route':'GET /api/asset?path=images/<prefix>/<sha256>.<extension>','root':str(IMAGE_ROOT),'database_writes':False,'asset_writes':False,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
(HERE/'server-info.json').write_text(json.dumps(info,indent=2)+'\n')
(HERE/'port').write_text(str(info['port'])+'\n')
print(json.dumps(info),flush=True)
def stop(signum,frame):
    threading.Thread(target=server.shutdown,daemon=True).start()
signal.signal(signal.SIGTERM,stop);signal.signal(signal.SIGINT,stop)
try:server.serve_forever(poll_interval=.25)
finally:
    server.server_close();info['status']='stopped';info['stopped_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();(HERE/'server-info.json').write_text(json.dumps(info,indent=2)+'\n')
