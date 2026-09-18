# -*- coding: utf-8 -*-
import json
import os

MISSING_TEXT = '> ⚠️ **原書掃描缺頁**\n>\n> 本題原書對應頁碼於電子掃描檔中缺失，暫無收錄原書詳解'

# 1. Update questions.json
with open('src/data/questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

updated_q = 0
for q in questions:
    qid = q.get('id', '')
    if '111-2' in qid and '醫學(三)' in qid:
        num = int(q.get('number', 0))
        if 31 <= num <= 40:
            q['explanation'] = MISSING_TEXT
            q['explanation_image'] = None
            q['explanation_images'] = []
            updated_q += 1

with open('src/data/questions.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f'Updated {updated_q} questions in questions.json to missing page status')

# 2. Update explanations_map.json
with open('src/data/explanations_map.json', 'r', encoding='utf-8') as f:
    exp_map = json.load(f)

for num in range(31, 41):
    key = f'111-2-醫學(三)-{num}'
    exp_map[key] = {
        'explanation': MISSING_TEXT,
        'explanation_image': None,
        'explanation_images': []
    }

with open('src/data/explanations_map.json', 'w', encoding='utf-8') as f:
    json.dump(exp_map, f, ensure_ascii=False, indent=2)

print('Updated explanations_map.json successfully')

