"""Expose a redacted remote rejection code from an exact EDB CLI replay.

The CLI remains responsible for encoding requests and validating receipts. A
one-request local relay observes the response without altering either frame.
Used only when the CLI reports transport/remote-error without its remote code.
"""
import hashlib
import re
import socket
import subprocess
import tempfile
import threading
from pathlib import Path


def rejection_code(frame):
    # EDB canonical blob v3, submission outcome v6. Unknown formats stay unknown.
    if (len(frame) < 51 or frame[:8] != b'EDBC\x0c\x00\x03\x00' or
            int.from_bytes(frame[8:16], 'big') != len(frame)-48 or
            hashlib.sha256(frame[:-32]).digest() != frame[-32:]):
        return None
    body = frame[16:-32]
    if body[:2] != b'\x06\x01':
        return None
    length = int.from_bytes(body[3:7], 'big')
    if length > 128 or len(body) < 7+length:
        return None
    try:
        code = body[7:7+length].decode('ascii')
    except UnicodeDecodeError:
        return None
    return code if re.fullmatch(r'[a-z][a-z0-9-]*/[a-z][a-z0-9-]*', code) else None


def replay(command, *, env, timeout=210):
    """Run the same request once, preserving stdout and any ambiguous outcome."""
    command = list(map(str, command))
    position = command.index('--endpoint')+1
    endpoint = command[position]
    observed = []

    def frame(stream):
        def read(size):
            chunks = bytearray()
            while len(chunks) < size:
                chunk = stream.recv(size-len(chunks))
                if not chunk:
                    raise EOFError('EDB relay disconnected')
                chunks.extend(chunk)
            return bytes(chunks)
        header = read(8)
        length = int.from_bytes(header, 'big')
        if not 48 <= length <= 64*1024*1024+48:
            raise ValueError('EDB relay frame size')
        return header, read(length)

    with tempfile.TemporaryDirectory(prefix='ma-edb-') as temporary:
        with socket.socket(socket.AF_UNIX) as listener:
            address = str(Path(temporary)/'relay.sock')
            listener.bind(address)
            listener.listen(1)
            listener.settimeout(timeout)
            command[position] = address

            def relay():
                try:
                    with listener.accept()[0] as client, socket.socket(socket.AF_UNIX) as server:
                        client.settimeout(timeout)
                        server.settimeout(timeout)
                        server.connect(endpoint)
                        header, request = frame(client)
                        server.sendall(header+request)
                        header, response = frame(server)
                        observed.append(rejection_code(response))
                        client.sendall(header+response)
                except (OSError, EOFError, ValueError):
                    # CLI classifies disconnected/lost replies as unknown outcomes.
                    pass

            thread = threading.Thread(target=relay, daemon=True)
            thread.start()
            try:
                result = subprocess.run(command, env=env, capture_output=True, text=True, timeout=timeout)
            finally:
                listener.close()
                thread.join(timeout=1)
    if result.returncode:
        stderr = result.stderr
        if observed and observed[0] and re.search(
                r'^ERROR category=Conflict code=transport/remote-error(?:\s|$)', stderr, re.M):
            stderr += '\nremote_code='+observed[0]+'\n'
        raise subprocess.CalledProcessError(result.returncode, command, result.stdout, stderr)
    return result.stdout
