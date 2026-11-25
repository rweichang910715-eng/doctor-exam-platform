"""Set official answers. Usage: python scripts/set_answers.py <id>=<answer> [...]"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from merge_explanations import load, save
p = Path("src/data/questions.json")
data, fmt = load(p)
by_id = {q["id"]: q for q in data}
for arg in sys.argv[1:]:
    qid, ans = arg.split("=")
    print(qid, by_id[qid]["answer"], "->", ans)
    by_id[qid]["answer"] = ans
save(p, data, fmt)
