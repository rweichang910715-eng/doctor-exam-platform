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
# Q21: Book p.62 -> page 72 [795:1315]
write_img('public/explanations/cropped/111-2-醫學(三)-21_merged.png', read_img(72)[795:1315, 40:930])

# Q22: Book p.63 -> page 73 [420:1035]
write_img('public/explanations/cropped/111-2-醫學(三)-22_merged.png', read_img(73)[420:1035, 40:930])

# Q23: Book p.64 -> page 74 [170:980]
write_img('public/explanations/cropped/111-2-醫學(三)-23_merged.png', read_img(74)[170:980, 40:930])

# Q24: Book p.77 -> page 87 [170:1310]
write_img('public/explanations/cropped/111-2-醫學(三)-24_merged.png', read_img(87)[170:1310, 40:930])

# Q25: Book p.78 -> page 88 [420:740]
write_img('public/explanations/cropped/111-2-醫學(三)-25_merged.png', read_img(88)[420:740, 40:930])

# Q26: Book p.79 -> page 89 [170:420]
write_img('public/explanations/cropped/111-2-醫學(三)-26_merged.png', read_img(89)[170:420, 40:930])

# Q27: Book p.80 -> page 90 [1120:1330]
write_img('public/explanations/cropped/111-2-醫學(三)-27_merged.png', read_img(90)[1120:1330, 40:930])

# Q28: Book p.79~80 -> page 89 [870:1315] + page 90 [170:760]
p89_q28 = read_img(89)[870:1315, 40:930]
p90_q28 = read_img(90)[170:760, 40:930]
write_img('public/explanations/cropped/111-2-醫學(三)-28_merged.png', np.vstack([p89_q28, p90_q28]))

# Q29: Book p.81 -> page 91 [420:850]
write_img('public/explanations/cropped/111-2-醫學(三)-29_merged.png', read_img(91)[420:850, 40:930])

# Q30: Book p.82 -> page 92 [170:760]
write_img('public/explanations/cropped/111-2-醫學(三)-30_merged.png', read_img(92)[170:760, 40:930])

print('Cropped images generated successfully')

EXPLANATIONS = {
    21: {
        'text': '''胰腺癌 (pancreatic adenocarcinoma) 最常發生在胰臟頭部，其症狀包含：上腹痛（因吃東西或躺平加劇）、背痛、體重減輕、黃疸、白色糞便、出現新的糖尿病、憂鬱情緒、肝腫大、靜脈炎 (Trousseau\'s syndrome)、無痛性腫大膽囊 (Courvoisier\'s sign)、脾腫大（若有 portal v. thrombosis）等，血糖應該會偏高而不是出現低血糖，故本題選 (D)

< 其他考點 >
胰臟癌的危險因子、非危險因子是近年各科愛考的重點：
1. 胰臟癌危險因子：抽菸、年紀、高油高糖飲食、BBQ 燒肉【108-2】
2. 胰臟癌相關基因之風險倍率：STK11 (76~140x) > PRSS1/SPIN11 (53x) > microsatellite (9~30x) > BRCA2 (2~6x)
3. 非胰臟癌危險因子：H. pylori、咖啡、中度酒精攝取
4. 胰臟癌的 tumor marker：CA-199、CEA，如果兩個都陰性 → 抽 CA-125
5. 胰臟管腺癌最常見的突變：KRAS''',
        'image': '/explanations/cropped/111-2-醫學(三)-21_merged.png'
    },
    22: {
        'text': '''肝細胞癌 (hepatocellular carcinoma, HCC) 的危險因子包含：肝硬化、HBV/HCV 感染、酒精濫用、代謝症候群（→ NASH）、血鐵沉著症 (hemochromatosis) 等；肝鈣化點通常是良性的，與過去的感染或肉芽疾病有關（如：TB），故本題選 (C)

< 其他考點 >
流病數字沒看過實在很難猜，以下整理一些課本中的數據供大家參考：
1. 肝細胞癌病人中 80% 有肝硬化
2. 肝硬化者有 1/3 的人在其一生中會得到肝癌
3. NASH 引起的 HCC 有 25~30% 並沒有出現肝硬化
4. 因為 HBV/HCV 引起的肝硬化，每年得到 HCC 的風險：3～8%
5. 因為其他原因引起的肝硬化，每年得到 HCC 的風險：1～3%
6. HBV 感染引起的 HCC：佔亞洲族群 60%、歐美族群僅 20%
7. 歐美族群 HCC 致病因子：HCV (30%) > HBV (20%) > NASH (15~20%)''',
        'image': '/explanations/cropped/111-2-醫學(三)-22_merged.png'
    },
    23: {
        'text': '''肝移植的禁忌症包含以下幾種，絕對與相對禁忌症是 Harrison 的分法，而原因的分類只是筆者自己分的，大家可以照自己覺得好懂的方法記憶

| 絕對禁忌 | 相對禁忌 |
| :--- | :--- |
| **有立即危險** | 不受控制的肝外感染、進行中的敗血症、危及生命的系統性疾病 | - |
| **移植後有風險** | 死亡率很高：肝外癌症（不含 non-melanoma 皮膚癌）、轉移到肝臟的其他癌症、膽管癌、無法改正且影響壽命的先天疾病、嚴重心肺疾病、AIDS | 死亡率偏高，但有機會改善：年紀 > 70、portal v. 栓塞、腎衰竭、之前有肝外癌症、嚴重肥胖、嚴重營養不良、HIV 控制差、肝內敗血症、PAH > 35 mmHg、PO₂ < 50 mmHg |
| **自理有困難** | 正在物質濫用 | 藥物順從性差、活動性精神病 |

故只有 (D) 選項是相對禁忌之一，其他都可以進行肝移植

< 其他考點 >
1. hepatic vein thrombosis 是肝移植適應症，但 portal vein thrombosis 是相對禁忌症喔！
2. 嚴重肝腎症候群 (hepato-renal syndrome) 不是肝移植的禁忌症（此時也只剩移植可以救這樣的病人了...）【109 重專】''',
        'image': '/explanations/cropped/111-2-醫學(三)-23_merged.png'
    },
    24: {
        'text': '''T cell 的活化主要有兩種訊號：signal 1 為抗原呈現、signal 2 為 costimulation，Belatacept 會先佔據 CD80/86，抗原呈現細胞的 CD28 就不能與 T cell 上的 CD80/86 結合，T cell 沒有 costimulation signal 就會進入 anergy → apoptosis，Abatacept 也是結合 CD80/86，但效果不及 belatacept，目前主要適應症是拿來治療 RA、JIA；2021 年 12 月美國 FDA 新核准的用途是預防造血幹細胞移植後的 acute GVHD（搭配 MTX + calcineurin inhibitor）

| | T cell | 抗原呈現細胞 (APC) |
| :--- | :--- | :--- |
| signal 1（抗原呈現） | T cell receptor (CD4, CD8) | MHC (II, I) + Ag |
| signal 2 (costimulation) | costimulatory ligands (CD80/86 = B7.1/B7.2) | CD28 |

考試當下還以為是風濕免疫科考題，但其實這是腎臟科的題目，近幾年腎臟科很愛考抗排斥藥，整理如下

| 免疫抑制劑 | 作用機制 | 副作用 |
| :--- | :--- | :--- |
| Glucocorticoids | 抑制 IL-1、IL-2、IL-3、IL-6、TNF-α、IFN-γ 的生成 | 高血壓、葡萄糖耐受不良、骨質疏鬆、脂質代謝異常 |
| Cyclosporine (CsA) | 結合 cyclophilin A → 抑制 calcineurin → IL-2 減少 | 腎毒性、高血壓、脂質代謝異常、多毛、牙齦增生 |
| Tacrolimus (FK506) | 結合 FKBP-12 → 抑制 calcineurin → IL-2 減少 | 類似 CsA，但更容易有糖尿病、較不會多毛或牙齦增生 |
| Azathioprine | 抑制 purine 合成 | 骨髓抑制 (WBC>RBC>PLT) |
| Mycophenolate mofetil (MMF) | 轉為 MPA → 抑制 IMPDH → 抑制 purine 合成 | 腹瀉、腹痛、輕微骨髓抑制 |
| Sirolimus (rapamycin) / everolimus | 結合 FKBP-12 → 抑制 mTOR → 停在 G1 phase | 高血脂、血小板低下 |
| Belatacept | 結合 CD80/86 → 阻擋 CD28 → 缺乏 costimulation → T cell 無法有效活化 | post-transplant lymphoproliferative disease (PTLD) |''',
        'image': '/explanations/cropped/111-2-醫學(三)-24_merged.png'
    },
    25: {
        'text': '''馬兜鈴酸腎病變 (aristolochic acid nephropathy, AAN) 即中藥腎病變、巴爾幹腎病變 (Balkan nephropathy)，會導致慢性腎小管間質性腎炎 (chronic tubulointerstitial nephritis)，其造成的病理及臨床特色為腎臟間質纖維化、稀疏細胞浸潤、微量蛋白尿，以及不成比例的貧血 (disproportionate anemia)，馬兜鈴酸不只是腎毒素，還是致癌物，其引起的典型 DNA 損傷為 A:T-to-T:A transversion，因此有馬兜鈴酸腎病變的人也會有較高上泌尿道泌尿上皮癌的風險，綜合以上所述，本題選 (A)，蛋白尿並不明顯，因此也不會有明顯的 protein-energy malnutrition''',
        'image': '/explanations/cropped/111-2-醫學(三)-25_merged.png'
    },
    26: {
        'text': '''腰痛、血尿、發燒 → 急性腎盂腎炎，打 constrast 前的圖可以看到左邊輸尿管中有顆 radiopaque 的物體；打完 contrast 後，可以看到從那一段以上的輸尿管以及腎盂都擴張了（水腎）→ 那顆是塞住輸尿管的結石，因為輸尿管阻塞導致的 UTI 是 medical emergency，需要立即介入處置，可以會診泌尿科醫師在輸尿管放 stent 或做經皮腎造口 (PCN)，本題選 (B)''',
        'image': '/explanations/cropped/111-2-醫學(三)-26_merged.png'
    },
    27: {
        'text': '''孕婦不可以用 ACE-i，真的已經考到稀爛了...... 其他選項 methyldopa、labetalol、nifedipine (CCB) 都是懷孕期間可使用的降血壓藥，婦產科也會考，要背起來！
(D) 如果要預防 pre-eclampsia 的發生，可給予低劑量 (80-100 mg/day) aspirin''',
        'image': '/explanations/cropped/111-2-醫學(三)-27_merged.png'
    },
    28: {
        'text': '''Focal segmental glomerulosclerosis (FSGS) 是一種局部腎絲球結疤 (scarring) 的疾病，其發生率正在增加，已佔目前成人腎病症候群的 1/3

| Focal segmental glomerulosclerosis (FSGS) | |
| :--- | :--- |
| 病理特徵 | 1. 位置：主要病變在 corticomedullary junction 的腎絲球（切片太淺可能被誤認成 MCD）<br>2. 類型：局部細胞增生伴隨嚴重蛋白尿、節段或全體塌陷型（預後差）、腎絲球尖端型 (glomerular tip lesion，預後好) |
| 臨床表現 | 1. 血尿、高血壓、任何嚴重度的蛋白尿、腎衰竭<br>2. 預後差的表現：腎病症候群程度蛋白尿、腎衰竭 |
| 治療 | 很少自己好，但治療可改善預後<br>1. 必須包含 RAAS inhibitors<br>2. primary FSGS 出現大量蛋白尿：steroids<br>3. secondary FSGS：治療 underlying、控制蛋白尿、不建議使用 steroids 或 cyclosporine<br>4. 移植後 recurrent FSGS：plasmapheresis |

（參考 Harrison 21/e Ch. 314）

(C) 節段或全體塌陷型 (segmental or global collapse) 的預後比較差，腎絲球尖端型 (glomerular tip lesion) 才是預後好的（以常理推論，全部塌光光的預後大概不會好到哪去......）

< 其他考點 >
1. FSGS 的致病機轉跟免疫複合物沈澱 (immune complex) 無關
2. 對類固醇治療反應不佳，目前 rituximab、mycophenolate mofetil 都沒有治療角色，cyclosporine 有可能可以讓對類固醇有反應的人達到 remission 但證據不充分，且一停藥就容易復發
3. FSGS 腎移植後又出現 FSGS 的機率：primary > secondary > genetic
4. 塌陷型 FSGS 一般常見於 HIV 相關的腎絲球疾病''',
        'image': '/explanations/cropped/111-2-醫學(三)-28_merged.png'
    },
    29: {
        'text': '''集尿管主細胞 (principle cell) 的 basolateral membrane 會表現 V2 receptor，接受抗利尿激素 (ADH = vasopressin = AVP) 的刺激 → 增加細胞內的 cAMP 濃度 → 把水通道蛋白 2 (aquaporin 2) 插到 apical membrane → 增加對水的通透性，原答案只給 (D)，但因為一階國考用書 Guyton and Hall 14/e Ch. 29 有提到遠端腎小管的末端也有相同功能，故經申覆開放 (C)(D) 均可

< 其他考點 >
1. 腎小管對水分通透性最低處：Henle 氏環上行枝
2. ADH 除了增加對水的通透外，也可以增加 urea 在集尿管的通透度''',
        'image': '/explanations/cropped/111-2-醫學(三)-29_merged.png'
    },
    30: {
        'text': '''| 顯影劑腎病變 (contrast induced nephropathy) | |
| :--- | :--- |
| 顯影劑類型 | 含碘顯影劑、高劑量 group 1 Gadolinium 顯影劑 |
| 風險因子 | CKD、multiple myeloma、既存腎臟問題、脫水 |
| 臨床表現 | 注射後 24~48 hr 出現 creatinine 升高 → 3~5 天達高峰 → 1 週恢復 |
| 致病機轉 | 1. 小血管受損 → 外層髓質缺氧<br>2. 游離自由基、高滲透壓 → 直接傷害細胞<br>3. 顯影劑結晶 → 暫時性腎小管阻塞 |

（參考 Harrison 21/e Ch. 310）

< 其他考點 >
1. 預防顯影劑引發 AKI 的方法：isotonic saline volume expansion、注射前 48hr 停用 metformin，鹼化尿液無預防效果 (PRESERVE trial)【108、109 內專】
2. DM 本身跟肥胖都不是顯影劑腎病變的風險因子，但糖尿病腎病變是重要風險因子之一''',
        'image': '/explanations/cropped/111-2-醫學(三)-30_merged.png'
    }
}

# 2. Update questions.json
with open('src/data/questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

updated_q = 0
for q in questions:
    qid = q.get('id', '')
    if '111-2' in qid and '醫學(三)' in qid:
        num = int(q.get('number', 0))
        if num in EXPLANATIONS:
            clean_text = EXPLANATIONS[num]['text'].replace('。', '')
            q['explanation'] = clean_text
            q['explanation_image'] = EXPLANATIONS[num]['image']
            updated_q += 1

with open('src/data/questions.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f'Updated {updated_q} questions in questions.json')

# 3. Update explanations_map.json
with open('src/data/explanations_map.json', 'r', encoding='utf-8') as f:
    exp_map = json.load(f)

for qnum, item in EXPLANATIONS.items():
    key = f'111-2-醫學(三)-{qnum}'
    clean_text = item['text'].replace('。', '')
    exp_map[key] = {
        'text': clean_text,
        'image': item['image']
    }

with open('src/data/explanations_map.json', 'w', encoding='utf-8') as f:
    json.dump(exp_map, f, ensure_ascii=False, indent=2)

print('Updated explanations_map.json successfully')
