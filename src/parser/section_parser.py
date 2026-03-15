import re
from typing import Dict, List, Union


SECTION_RE = re.compile(
    r"^\[(FACT|TECHNIQUE|HYP|ONTO|RESONANCE|ROLLBACK|SAFETY|CHECKLIST|3C|GLOSS)\]\s*$"
)


def parse_sections(lines: List[str]) -> Dict[str, Union[List[str], str]]:
    current = None
    out: Dict[str, Union[List[str], str]] = {}

    for raw in lines:
        line = raw.rstrip("\n")
        m = SECTION_RE.match(line.strip())
        if m:
            current = m.group(1)
            out[current] = [] if current != "GLOSS" else ""
            continue

        if current is None:
            continue

        if current == "GLOSS":
            prev = out[current]
            out[current] = (prev + "\n" + line).strip() if prev else line
        else:
            if line.strip():
                out[current].append(line.strip())

    return out
