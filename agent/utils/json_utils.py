import json
import re
from typing import Any, Dict

def parse_json_loose(text: str) -> Dict[str, Any]:
    """
    Essaye de parser un JSON.
    - d'abord JSON strict
    - sinon extrait le premier bloc {...} ou [...]
    - sinon lève ValueError
    """
    text = text.strip()

    # 1) JSON strict
    try:
        data = json.loads(text)
        return data if isinstance(data, dict) else {"data": data}
    except Exception:
        pass

    # 2) Extrait un bloc JSON
    m = re.search(r"(\{.*\}|\[.*\])", text, flags=re.DOTALL)
    if not m:
        raise ValueError("No JSON found in model output")

    raw = m.group(1)
    data = json.loads(raw)
    return data if isinstance(data, dict) else {"data": data}


def to_json(data: Dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)