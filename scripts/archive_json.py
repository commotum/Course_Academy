"""Read and update cold JSON exports stored as plain text or lossless gzip."""
import gzip
import hashlib
import os
from pathlib import Path
import tempfile


def exists(path):
    path=Path(path)
    return path.exists() or path.with_name(path.name+'.gz').exists()


def read_text(path):
    path=Path(path)
    if path.exists():return path.read_text()
    return gzip.decompress(path.with_name(path.name+'.gz').read_bytes()).decode('utf-8')


def _publish(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    fd,temporary=tempfile.mkstemp(prefix='.'+path.name+'.',dir=path.parent)
    try:
        with os.fdopen(fd,'wb')as stream:
            stream.write(data);stream.flush();os.fsync(stream.fileno())
        os.replace(temporary,path)
        descriptor=os.open(path.parent,os.O_DIRECTORY)
        try:os.fsync(descriptor)
        finally:os.close(descriptor)
    finally:
        if os.path.exists(temporary):os.unlink(temporary)


def write_text(path,text):
    path=Path(path);compressed=path.with_name(path.name+'.gz')
    if compressed.exists():
        if path.exists():raise ValueError('Both plain and compressed exports exist: '+str(path))
        _publish(compressed,gzip.compress(text.encode('utf-8'),compresslevel=6,mtime=0))
    else:_publish(path,text.encode('utf-8'))


def compress(path):
    path=Path(path)
    if path.is_symlink():raise ValueError('Refusing to replace a symlink: '+str(path))
    before=path.stat();data=path.read_bytes();target=path.with_name(path.name+'.gz')
    digest=hashlib.sha256(data).hexdigest()
    if target.exists() and gzip.decompress(target.read_bytes())!=data:
        raise ValueError('Distinct compressed export already exists: '+str(target))
    if not target.exists():_publish(target,gzip.compress(data,compresslevel=6,mtime=0))
    if hashlib.sha256(gzip.decompress(target.read_bytes())).hexdigest()!=digest:
        raise ValueError('Compressed export failed verification: '+str(target))
    now=path.stat()
    if (before.st_ino,before.st_mtime_ns,before.st_ctime_ns)!=(now.st_ino,now.st_mtime_ns,now.st_ctime_ns):
        raise ValueError('Export changed during compression: '+str(path))
    path.unlink()
    return {'original':str(path),'compressed':str(target),'sha256':digest,
            'before_bytes':len(data),'after_bytes':target.stat().st_size}
