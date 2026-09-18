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

# 1. Image Cropping & Merging
# Q45: Book p.37 -> page 47 [138:990, 40:930]
write_img('public/explanations/cropped/111-2-醫學(三)-45_merged.png', read_img(47)[138:990, 40:930])

# Q46: Book p.39~40 -> page 49 [575:1235] + page 50 [145:710]
p49_q46 = read_img(49)[575:1235, 40:930]
p50_q46 = read_img(50)[145:710, 40:930]
write_img('public/explanations/cropped/111-2-醫學(三)-46_merged.png', np.vstack([p49_q46, p50_q46]))

# Q47: Book p.38 -> page 48 [138:425, 40:930]
write_img('public/explanations/cropped/111-2-醫學(三)-47_merged.png', read_img(48)[138:425, 40:930])

# Q48: Book p.40~41 -> page 50 [1070:1258, 40:930] + page 51 [174:745, 37:927]
p50_q48 = read_img(50)[1070:1258, 40:930]
p51_q48 = read_img(51)[174:745, 37:927]
write_img('public/explanations/cropped/111-2-醫學(三)-48_merged.png', np.vstack([p50_q48, p51_q48]))

# Q49: Book p.38 -> page 48 [1000:1240, 40:930]
write_img('public/explanations/cropped/111-2-醫學(三)-49_merged.png', read_img(48)[1000:1240, 40:930])

print('Cropped and merged images generated successfully')
