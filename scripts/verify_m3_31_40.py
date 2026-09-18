# -*- coding: utf-8 -*-
import json
import os

with open('src/data/questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

print('--- Checking questions.json for 111-2 醫學(三) Q31~40 ---')
all_pass = True
for q in questions:
    if '111-2' in q.get('id', '') and '醫學(三)' in q.get('id', ''):
        num = int(q.get('number', 0))
        if 31 <= num <= 40:
            exp = q.get('explanation', '')
            has_period = '。' in exp
            is_missing_format = '原書掃描缺頁' in exp
            
            status = 'OK'
            if has_period or not is_missing_format:
                status = 'FAIL'
                all_pass = False
            
            print(f'Q{num:02d}: status={status}, exp_len={len(exp)}, has_period={has_period}, is_missing={is_missing_format}')

with open('src/data/explanations_map.json', 'r', encoding='utf-8') as f:
    exp_map = json.load(f)

print('\n--- Checking explanations_map.json ---')
for num in range(31, 41):
    key = f'111-2-醫學(三)-{num}'
    if key not in exp_map:
        print(f'{key}: MISSING')
        all_pass = False
    else:
        item = exp_map[key]
        exp_text = item.get('explanation', item.get('text', ''))
        has_period = '。' in exp_text
        is_missing_format = '原書掃描缺頁' in exp_text
        if has_period or not is_missing_format:
            print(f'{key}: FAIL - period={has_period}, is_missing={is_missing_format}')
            all_pass = False
        else:
            print(f'{key}: OK (Missing page status correctly set)')

if all_pass:
    print('\nALL 10 QUESTIONS VERIFIED SUCCESSFULLY - 0 PERIODS, MISSING PAGE STATUS SET')
else:
    print('\nVERIFICATION FAILED')

