"""Map 111 questions to 2022 book PDF pages by English-token overlap + question-number marker.
Writes scripts/map_2022.json {id: pdf_page_index}."""
import fitz, json, re, collections
d = fitz.open('2022 醫師國考試題詳解-臨床醫學.pdf')
pages = [p.get_text() for p in d]
ptoks = [set(w.lower() for w in re.findall(r'[A-Za-z]{4,}', t)) for t in pages]
df = collections.Counter(w for s in ptoks for w in s)
qs = [q for q in json.load(open('src/data/questions.json', encoding='utf8')) if q['year'].startswith('111')]
out = {}
low = []
for q in qs:
    txt = q['text'] + ' ' + ' '.join(q['options'].values())
    toks = set(w.lower() for w in re.findall(r'[A-Za-z]{4,}', txt))
    best = (0, -1)
    for i, s in enumerate(ptoks):
        sc = sum(1 / df[w] for w in toks & s)
        if re.search(r'(^|\n)\s*%d\s*\.' % q['number'], pages[i]):
            sc += 0.3
        best = max(best, (sc, i))
    out[q['id']] = best[1]
    if best[0] < 0.5:
        low.append((q['id'], round(best[0], 2), best[1]))
json.dump(out, open('scripts/map_2022.json', 'w', encoding='utf8'), ensure_ascii=False, indent=0)
print('low confidence', len(low))
for x in low: print(x)
