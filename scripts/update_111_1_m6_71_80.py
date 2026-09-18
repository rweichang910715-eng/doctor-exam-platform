# -*- coding: utf-8 -*-
import json
import os
import cv2
import numpy as np

def read_img(p):
    return cv2.imdecode(np.fromfile(f'scratch/pages_2022/page_{p}.jpg', dtype=np.uint8), cv2.IMREAD_COLOR)

def write_img(path, img):
    ext = os.path.splitext(path)[1]
    res, buf = cv2.imencode(ext, img)
    with open(path, 'wb') as f:
        f.write(buf)

os.makedirs('public/explanations/cropped', exist_ok=True)

# 1. Image Cropping
# Q71: page 476 [1170:1315] + page 477 [170:255]
p476_q71 = read_img(476)[1170:1315, 40:930]
p477_q71 = read_img(477)[170:255, 40:930]
write_img('public/explanations/cropped/111-1-醫學(六)-71_merged.png', np.vstack([p476_q71, p477_q71]))

# Q72: page 460 [1060:1315] + page 461 [170:555]
p460_q72 = read_img(460)[1060:1315, 40:930]
p461_q72 = read_img(461)[170:555, 40:930]
write_img('public/explanations/cropped/111-1-醫學(六)-72_merged.png', np.vstack([p460_q72, p461_q72]))

# Q73: page 477 [945:1315] + page 478 [170:350]
p477_q73 = read_img(477)[945:1315, 40:930]
p478_q73 = read_img(478)[170:350, 40:930]
write_img('public/explanations/cropped/111-1-醫學(六)-73_merged.png', np.vstack([p477_q73, p478_q73]))

# Q74: page 478 [1030:1315] + page 479 [170:950]
p478_q74 = read_img(478)[1030:1315, 40:930]
p479_q74 = read_img(479)[170:950, 40:930]
write_img('public/explanations/cropped/111-1-醫學(六)-74_merged.png', np.vstack([p478_q74, p479_q74]))

# Q75: page 480 [145:760]
write_img('public/explanations/cropped/111-1-醫學(六)-75_merged.png', read_img(480)[145:760, 40:930])

# Q76: page 429 [895:1315] + page 430 [170:500]
p429_q76 = read_img(429)[895:1315, 40:930]
p430_q76 = read_img(430)[170:500, 40:930]
write_img('public/explanations/cropped/111-1-醫學(六)-76_merged.png', np.vstack([p429_q76, p430_q76]))

# Q77: page 298 [915:1315] + page 299 [170:760]
p298_q77 = read_img(298)[915:1315, 40:930]
p299_q77 = read_img(299)[170:760, 40:930]
write_img('public/explanations/cropped/111-1-醫學(六)-77_merged.png', np.vstack([p298_q77, p299_q77]))

# Q78: page 501 [145:490]
write_img('public/explanations/cropped/111-1-醫學(六)-78_merged.png', read_img(501)[145:490, 40:930])

# Q79: page 501 [790:985]
write_img('public/explanations/cropped/111-1-醫學(六)-79_merged.png', read_img(501)[790:985, 40:930])

# Q80: page 502 [145:490]
write_img('public/explanations/cropped/111-1-醫學(六)-80_merged.png', read_img(502)[145:490, 40:930])

print('Cropped images generated successfully')

# 2. Load explanations
with open('scratch/exp_71_80.json', 'r', encoding='utf-8') as f:
    explanations = json.load(f)

# 3. Update questions.json
with open('src/data/questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

updated_q = 0
for q in questions:
    qid = q.get('id', '')
    if '111-1' in qid and '醫學(六)' in qid:
        num = str(q.get('number', 0))
        if num in explanations:
            img_rel = f'/explanations/cropped/111-1-醫學(六)-{num}_merged.png'
            q['explanation'] = explanations[num]
            q['explanation_image'] = img_rel
            q['explanation_images'] = [img_rel]
            updated_q += 1

with open('src/data/questions.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f'Updated {updated_q} questions in questions.json')

# 4. Update explanations_map.json
with open('src/data/explanations_map.json', 'r', encoding='utf-8') as f:
    exp_map = json.load(f)

for num, exp_text in explanations.items():
    key = f'111-1-醫學(六)-{num}'
    img_rel = f'/explanations/cropped/111-1-醫學(六)-{num}_merged.png'
    exp_map[key] = {
        'explanation': exp_text,
        'explanation_image': img_rel,
        'explanation_images': [img_rel]
    }

with open('src/data/explanations_map.json', 'w', encoding='utf-8') as f:
    json.dump(exp_map, f, ensure_ascii=False, indent=2)

print('Updated explanations_map.json successfully')
