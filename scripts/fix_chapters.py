"""Set chapter/category/section of questions to the 合記 book chapter they appear in.

Usage: python scripts/fix_chapters.py <chapter name> <batch.json> [<chapter> <batch.json> ...]
Every question id in a batch file gets that chapter. Prints each change.
"""
import json, sys
sys.path.insert(0, "scripts")
from merge_explanations import load, save, QUESTIONS

SECTION = {
    "第一篇 內科學": ["免疫風濕科", "心臟內科", "急診內科", "感染科", "新陳代謝科", "神經內科", "肝膽腸胃科", "胸腔內科", "腎臟科", "血液腫瘤科"],
    "第二篇 外科學": ["一般外科", "外科概論", "大腸直腸科", "小兒外科", "心臟外科", "急診外傷科", "整形外科", "神經外科", "移植科", "胸腔外科"],
    "第三篇 婦兒科": ["婦產科", "小兒科"],
    "第四篇 其他科": ["家庭醫學科", "復健科", "泌尿科", "皮膚科", "眼科", "精神科", "耳鼻喉科", "醫學倫理與醫療決策", "骨科", "麻醉科"],
}
section_of = {c: s for s, cs in SECTION.items() for c in cs}

questions, fmt = load(QUESTIONS)
by_id = {q["id"]: q for q in questions}
args = sys.argv[1:]
changed = 0
for chapter, path in zip(args[0::2], args[1::2]):
    assert chapter in section_of, chapter
    for qid in json.load(open(path, encoding="utf-8")):
        q = by_id[qid]
        if q.get("chapter") != chapter:
            print(f"{qid}: {q.get('chapter')} -> {chapter}")
            changed += 1
        q["chapter"] = q["category"] = chapter
        q["section"] = section_of[chapter]
save(QUESTIONS, questions, fmt)
print("changed", changed)
