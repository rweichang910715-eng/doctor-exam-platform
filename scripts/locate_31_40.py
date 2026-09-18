# -*- coding: utf-8 -*-
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

missing = [q for q in questions if '原書掃描缺頁' in q.get('explanation', '') or '缺頁' in q.get('explanation', '')]
print(f'Total missing page questions: {len(missing)}')
for q in missing[:5]:
    print(f"ID: {q.get('id')}")
    print(f"Explanation: {repr(q.get('explanation'))}")
    print(f"Image: {q.get('explanation_image')}")
    print(f"Images: {q.get('explanation_images')}")
    print('-'*40)


with open('src/data/explanations_map.json', 'r', encoding='utf-8') as f:
    exp_map = json.load(f)

for q in missing[:5]:
    qid = q.get('id')
    print(f"explanations_map[{qid}]: {exp_map.get(qid)}")




















