"""Merge text explanations into the question bank.

Usage:
    python scripts/merge_explanations.py scripts/explanations/<batch>.json

The batch file maps question id (e.g. "114-1-醫學(三)-1") to explanation text.
Each explanation is written to both src/data/questions.json (field
"explanation") and src/data/explanations_map.json. Existing images on a
question are left untouched.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUESTIONS = ROOT / "src" / "data" / "questions.json"
EXPL_MAP = ROOT / "src" / "data" / "explanations_map.json"


def load(path):
    raw = path.read_bytes()
    text = raw.decode("utf-8")
    newline = "\r\n" if "\r\n" in text[:2000] else "\n"
    second_line = text.split(newline, 2)[1]
    indent = len(second_line) - len(second_line.lstrip(" "))
    fmt = {"newline": newline, "indent": indent, "trailing": text.endswith(newline)}
    return json.loads(text), fmt


def save(path, data, fmt):
    text = json.dumps(data, ensure_ascii=False, indent=fmt["indent"])
    text = text.replace("\n", fmt["newline"]) + (fmt["newline"] if fmt["trailing"] else "")
    path.write_bytes(text.encode("utf-8"))


def main(batch_path):
    batch = json.loads(Path(batch_path).read_text(encoding="utf-8"))
    questions, q_nl = load(QUESTIONS)
    expl_map, m_nl = load(EXPL_MAP)

    by_id = {q["id"]: q for q in questions}
    missing = [qid for qid in batch if qid not in by_id]
    if missing:
        sys.exit(f"Unknown question ids: {missing}")

    for qid, text in batch.items():
        by_id[qid]["explanation"] = text
        entry = expl_map.get(qid)
        if not isinstance(entry, dict):
            entry = {}
        entry["explanation"] = text
        expl_map[qid] = entry

    save(QUESTIONS, questions, q_nl)
    save(EXPL_MAP, expl_map, m_nl)
    print(f"Merged {len(batch)} explanations.")


if __name__ == "__main__":
    main(sys.argv[1])
