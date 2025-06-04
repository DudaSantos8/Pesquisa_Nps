import hashlib
import os

def get_file_hash(path: str) -> str:
    if not os.path.exists(path):
        return ""
    hasher = hashlib.md5()
    with open(path, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()
