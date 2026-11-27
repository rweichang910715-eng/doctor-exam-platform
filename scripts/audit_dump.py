"""Print site explanation and book crop paths for a range of questions.
Usage: python scripts/audit_dump.py <exam> <subject-digit> <lo> <hi>"""
import json, sys
exam, subj, lo, hi = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
name = {'3': '醫學(三)', '4': '醫學(四)', '5': '醫學(五)', '6': '醫學(六)'}[subj]
qs = {q['id']: q for q in json.load(open('src/data/questions.json', encoding='utf8'))}
for n in range(lo, hi + 1):
    q = qs.get(f'{exam}-{name}-{n}')
    if not q:
        continue
    print(f"### {q['id']} ans={q['answer']} imgs={q.get('explanation_images')}")
    print(q['text'][:80].replace('\n', ' '))
    print(q['explanation'])
    print()
