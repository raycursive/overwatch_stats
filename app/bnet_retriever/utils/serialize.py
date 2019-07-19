import json
from base64 import b64encode, b64decode
from typing import Dict


def tostr(obj: Dict) -> str:
    return b64encode(json.dumps(obj).encode()).decode()


def fromstr(s: str) -> Dict:
    return json.loads(b64decode(s.encode()))
