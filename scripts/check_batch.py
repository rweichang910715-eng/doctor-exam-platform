"""Check rewritten batches: ids exist and the stated answer matches the site answer.
Usage: python scripts/check_batch.py <batch.json> [...]"""
import json, re, sys
qs = {q['id']: q for q in json.load(open('src/data/questions.json', encoding='utf8'))}
for p in sys.argv[1:]:
    for k, v in json.load(open(p, encoding='utf8')).items():
        if k not in qs:
            print('MISSING', k); continue
        m = re.match(r'答案 \(([A-E])\)(?:\(([A-E])\))?', v)
        stated = ''.join(x for x in (m.groups() if m else ()) if x)
        site = qs[k]['answer']
        if not m or stated.replace(',', '') != site.replace(',', '').replace('、', '').replace(' ', ''):
            print('ANSWER?', k, 'stated', stated, 'site', site)
