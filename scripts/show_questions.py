"""Print questions for one exam/subject range: python scripts/show_questions.py 114-1 醫學(三) 21 30"""
import json, sys
sys.stdout.reconfigure(encoding="utf-8")
year, subject, lo, hi = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
for q in json.load(open("src/data/questions.json", encoding="utf-8")):
    if q["year"] == year and q["subject"] == subject and lo <= q["number"] <= hi:
        print(q["number"], q["answer"], q.get("chapter"), "|", q["text"].replace("\n", " "))
        for k, v in q["options"].items():
            print("  ", k, v)
        if q.get("images"):
            print("   IMG", q["images"])
