# -*- coding: utf-8 -*-
import json
import os

with open('src/data/questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

print('--- Checking questions.json for 111-2 醫學(三) Q21~30 ---')
all_pass = True
for q in questions:
    if '111-2' in q.get('id', '') and '醫學(三)' in q.get('id', ''):
        num = int(q.get('number', 0))
        if 21 <= num <= 30:
            exp = q.get('explanation', '')
            img = q.get('explanation_image', '')
            has_period = '。' in exp
            img_path = os.path.join('public', img.lstrip('/'))
            img_exists = os.path.exists(img_path)
            
            status = 'OK'
            if has_period or not img_exists or len(exp) == 0:
                status = 'FAIL'
                all_pass = False
            
            print(f'Q{num:02d}: status={status}, exp_len={len(exp)}, has_period={has_period}, img_exists={img_exists} ({img})')

with open('src/data/explanations_map.json', 'r', encoding='utf-8') as f:
    exp_map = json.load(f)

print('\n--- Checking explanations_map.json ---')
for num in range(21, 31):
    key = f'111-2-醫學(三)-{num}'
    if key not in exp_map:
        print(f'{key}: MISSING')
        all_pass = False
    else:
        item = exp_map[key]
        has_period = '。' in item.get('text', '')
        img_exists = os.path.exists(os.path.join('public', item.get('image', '').lstrip('/')))
        if has_period or not img_exists:
            print(f'{key}: FAIL - period={has_period}, img_exists={img_exists}')
            all_pass = False
        else:
            print(f'{key}: OK')

if all_pass:
    print('\nALL 10 QUESTIONS VERIFIED SUCCESSFULLY - 0 PERIODS, ALL IMAGES EXIST')
else:
    print('\nVERIFICATION FAILED')
