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
# Q61: page 471 [145:830]
write_img('public/explanations/cropped/111-1-醫學(六)-61_merged.png', read_img(471)[145:830, 40:930])

# Q62: page 471 [1060:1315] + page 472 [170:585]
p471_q62 = read_img(471)[1060:1315, 40:930]
p472_q62 = read_img(472)[170:585, 40:930]
write_img('public/explanations/cropped/111-1-醫學(六)-62_merged.png', np.vstack([p471_q62, p472_q62]))

# Q63: page 472 [910:1315] + page 473 [170:275]
p472_q63 = read_img(472)[910:1315, 40:930]
p473_q63 = read_img(473)[170:275, 40:930]
write_img('public/explanations/cropped/111-1-醫學(六)-63_merged.png', np.vstack([p472_q63, p473_q63]))

# Q64: page 473 [560:760]
write_img('public/explanations/cropped/111-1-醫學(六)-64_merged.png', read_img(473)[560:760, 40:930])

# Q65: page 473 [1030:1305]
write_img('public/explanations/cropped/111-1-醫學(六)-65_merged.png', read_img(473)[1030:1305, 40:930])

# Q66: page 474 [345:685]
write_img('public/explanations/cropped/111-1-醫學(六)-66_merged.png', read_img(474)[345:685, 40:930])

# Q67: page 475 [390:675]
write_img('public/explanations/cropped/111-1-醫學(六)-67_merged.png', read_img(475)[390:675, 40:930])

# Q68: page 474 [985:1300]
write_img('public/explanations/cropped/111-1-醫學(六)-68_merged.png', read_img(474)[985:1300, 40:930])

# Q69: page 475 [925:1300]
write_img('public/explanations/cropped/111-1-醫學(六)-69_merged.png', read_img(475)[925:1300, 40:930])

# Q70: page 476 [680:950]
write_img('public/explanations/cropped/111-1-醫學(六)-70_merged.png', read_img(476)[680:950, 40:930])

print('Cropped images generated successfully')

# 2. Load explanations
with open('scratch/exp_61_70.json', 'r', encoding='utf-8') as f:
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
