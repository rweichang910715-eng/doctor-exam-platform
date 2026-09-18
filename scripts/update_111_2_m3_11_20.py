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
# Q11: page 35 [170:930]
write_img('public/explanations/cropped/111-2-醫學(三)-11_merged.png', read_img(35)[170:930, 40:930])

# Q12: page 36 [170:730]
write_img('public/explanations/cropped/111-2-醫學(三)-12_merged.png', read_img(36)[170:730, 40:930])

# Q13: page 36 [1015:1315] + page 37 [170:330]
p36_q13 = read_img(36)[1015:1315, 40:930]
p37_q13 = read_img(37)[170:330, 40:930]
write_img('public/explanations/cropped/111-2-醫學(三)-13_merged.png', np.vstack([p36_q13, p37_q13]))

# Q14: page 37 [920:1315] + page 38 [170:450]
p37_q14 = read_img(37)[920:1315, 40:930]
p38_q14 = read_img(38)[170:450, 40:930]
write_img('public/explanations/cropped/111-2-醫學(三)-14_merged.png', np.vstack([p37_q14, p38_q14]))

# Q15: page 65 [715:1315] + page 66 [170:520]
p65_q15 = read_img(65)[715:1315, 40:930]
p66_q15 = read_img(66)[170:520, 40:930]
write_img('public/explanations/cropped/111-2-醫學(三)-15_merged.png', np.vstack([p65_q15, p66_q15]))

# Q16: page 67 [1130:1315] + page 68 [170:1310]
p67_q16 = read_img(67)[1130:1315, 40:930]
p68_q16 = read_img(68)[170:1310, 40:930]
write_img('public/explanations/cropped/111-2-醫學(三)-16_merged.png', np.vstack([p67_q16, p68_q16]))

# Q17: page 66 [920:1315] + page 67 [170:810]
p66_q17 = read_img(66)[920:1315, 40:930]
p67_q17 = read_img(67)[170:810, 40:930]
write_img('public/explanations/cropped/111-2-醫學(三)-17_merged.png', np.vstack([p66_q17, p67_q17]))

# Q18: page 71 [435:1080]
write_img('public/explanations/cropped/111-2-醫學(三)-18_merged.png', read_img(71)[435:1080, 40:930])

# Q19: page 69 [490:1315] + page 70 [170:1310]
p69_q19 = read_img(69)[490:1315, 40:930]
p70_q19 = read_img(70)[170:1310, 40:930]
write_img('public/explanations/cropped/111-2-醫學(三)-19_merged.png', np.vstack([p69_q19, p70_q19]))

# Q20: page 72 [170:600]
write_img('public/explanations/cropped/111-2-醫學(三)-20_merged.png', read_img(72)[170:600, 40:930])

print('Cropped images generated successfully')

EXPLANATIONS = {
    11: {
        'text': '''| CHA₂DS₂-VASc score | | |
| :--- | :--- | :--- |
| | 分數 內容 | 說明 |
| C | 1 Congestive heart failure | 包含 HCM、中度以上 LV dysfunction |
| H | 1 Hypertension | 包含正在使用降血壓藥者 |
| A₂ | 2 Age ≥ 75 歲 | |
| D | 1 Diabetes mellitus | 包含正在使用降血糖藥者 |
| S₂ | 2 Prior stroke or TIA | |
| V | 1 Vascular disease | 包含 CAD、MI、PAD、aortic plaque，但不包含 DVT！ |
| A | 1 Age 65 ~ 74 歲 | |
| Sc | 1 Sex category（女） | AF 盛行率男 > 女，但女性 AF 病人較容易中風，請注意！ |

1. 男生 0、女生 1 才可不做 thromboemoblic prevention，其他都需要
2. AF 持續 > 48 小時或時間不明者，血栓機率明顯增加，故在進行 cardioversion 前就要開始用 anticoagulant

(D) 深部靜脈血栓並不在評分項目中，當初在定義的時候 vascular disease 就是“prior myocardial infarction, peripheral arterial disease or aortic plaque”，DVT 不算喔！''',
        'image': '/explanations/cropped/111-2-醫學(三)-11_merged.png'
    },
    12: {
        'text': '''(A) 正確，姿態性低血壓的定義是從平躺到站立後、或執行傾斜試驗第 3 分鐘時，收縮壓下降 >20 mmHg，或舒張壓下降 >10 mmHg
(B) 正確，右上胸骨旁是升主動脈的位置，也是 aortic valve 的聽診區，故如果出現 pulsation，可合理懷疑有升主動脈瘤
(C) 錯誤，pulsus paradoxus 是指吸氣時血壓下降的幅度 >10 mmHg（正常吸氣也會下降，但不會降太多）。可見於阻塞性肺疾或 cardiac tamponade 的病人，如果出現在阻塞性肺病患者身上時，是瀕臨呼吸衰竭 (impending respiratory failure) 的徵兆。選項所述的脈搏每跳之間有差異叫做“pulsus alternans”，代表心室收縮功能差（不是 electrical alternans 喔！那是 ECG 上出現 QRS 忽大忽小、忽正忽反的情形）
(D) 正確，bifid pulse 又稱 pulsus bisferiens，是指在一個心跳週期中，aortic wave 有兩個波峰，可見於 aortic regurgitation (+/- aortic stenosis) 以及 hypertrophic obstructive cardiomyopathy (HOCM) 的病人身上''',
        'image': '/explanations/cropped/111-2-醫學(三)-12_merged.png'
    },
    13: {
        'text': '''可以改善 HFrEF 預後之藥物：
1. RAAS antagonist：ACE-i、ARB（孕婦不可以用，考到稀爛）→ (A)
2. MR antagonist：spironolactone、eplerenone → (B)
3. ARNI：valsartan/sacubitril（Entresto，孕婦不可以用）→ (D)
4. SGLT2 inhibitors：dapagliflozin、empagliflozin
故本題選 (C)

< 補充 >
1. 會惡化心衰竭的藥：non-DHP CCB、TZD、COX2-inhibitor
2. 無法減少 HFrEF 死亡率的治療：digoxin（可改善症狀）、ivabradine（可降低住院率）''',
        'image': '/explanations/cropped/111-2-醫學(三)-13_merged.png'
    },
    14: {
        'text': '''本題出自 Harrison 21/e Ch. 258 “Sudden cardiac death prevention in heart failure”
(A) 正確，心衰竭約一半是因為心室性心律不整過世，尤其是在 HFrEF 的早期
(B) 正確，猝死發作後活下來的病人有很高機率再次發作，因此應該安裝 ICD
(C)(D) 適合預防性安裝 ICD 的兩種情況：(1) NYHA class II/III 且 LVEF ≤ 35% (2) 無論是否有症狀，在 AMI 後搭配最佳藥物治療 (optimal medical therapy) 但 LVEF 仍 ≤ 30% 者，故 (C) 錯誤

< 其他考點 >
1. 心臟衰竭預後：5 年存活率 50%、嚴重 HF 患者 1 年死亡率 40%
2. 非冠狀動脈疾病導致的 systolic HF 患者使用預防性 ICD，即便是有症狀的病人使用，也不會顯著降低死亡率
3. 末期病人、預期餘命 <6 個月、NYHA class IV 且對藥物治療反應不佳又不適合心臟移植者，須審慎評估裝 ICD 進行多次電擊的壞處與益處''',
        'image': '/explanations/cropped/111-2-醫學(三)-14_merged.png'
    },
    15: {
        'text': '''| C 型肝炎 | | |
| :--- | :--- | :--- |
| HCV 基本資料 | linear、單股、positive sense 的 RNA 病毒 | 備註 |
| | genotype (基因型)：6，以數字表示 | 台灣狀況：1b (70%) > 2a (20%) > 2b (10%) |
| | subtype (基因亞型)：> 50，以字母表示 | |
| 傳播途徑 | 主要：輸血、共用針頭<br>少見：性行為、垂直傳染 | 針扎感染率有 3%（HBV 則高達 30%） |
| 疾病進程 | 急性後 85% 會慢性化、20~25% 會肝硬化 | 慢性化比例高於 HBV |
| 治療 | • 舊藥：PEG-IFN-a + ribavirin，適合不同 genotype 的 RNA polymerase inhibitors<br>• 新藥：5 種口服 direct-acting antiviral (DAA) agents，已成為目前主流 | |
| 預後 | type 1：RNA 濃度最高、藥物反應最差<br>type 2：RNA 濃度低、藥物反應好 | 日本多為 type 2 |

(A)(D) 雖然這個病人還沒進展到肝硬化，但急性期後有高達 85% 病人會慢性化、20~25% 會肝硬化、肝硬化有 3~6% 會進展成肝癌。肝硬化的病人在清除病毒後，可以有效降低死亡率、肝衰竭、肝移植、肝細胞癌的機率；然而風險會持續存在，故仍應定期追蹤腹部超音波與胎兒蛋白
(B)(C) 從 2017 年起，開始推動「C 型肝炎全口服新藥健保給付執行計畫」，並在 2019 年開始放寬給付對象條件。目前主流是使用療程短 (12~24 週)、效果好（治癒率超過 90%）、抗藥性低、副作用較小且病人順從性高的口服 DAA，已經不是 PEG-IFN + ribavirin 了。【107 內專】''',
        'image': '/explanations/cropped/111-2-醫學(三)-15_merged.png'
    },
    16: {
        'text': '''The Knodell histologic activity index (HAI) 是美國使用的肝炎評分系統，歐洲使用的是 METAVIR score。HAI 最高總分 18 分、METAVIR 分為 A0 ~ A3 共四級，選項中只有 (B) 沒有列入評分項目。表格中的 bridging necrosis 是一種血管間的融合性壞死 (confluent necrosis)，會導致肝小葉的網狀架構出現塌陷

| 慢性肝炎嚴重度評分系統 | | | | |
| :--- | :--- | :--- | :--- | :--- |
| | histologic activity index (HAI) | | METAVIR | |
| necrosis (grade) | 嚴重度 | 分數 | 嚴重度 | 分數 |
| periportal | none | 0 | none | 0 |
| | mild | 1 | mild | 1 |
| | mild ~ moderate | 2 | moderate | 2 |
| | moderate | 3 | severe | 3 |
| | severe | 4 | bridging necrosis | Y / N |
| intralobular | none | 0 | none ~ mild | 0 |
| | focal | 1 | moderate | 1 |
| | some zone 3 | 2 | severe | 2 |
| | most zone 3 | 3 | | |
| | zone 3 + few bridging | 4 | | |
| | zone 3 + multiple bridging | 5 | | |
| | panacinar / multiacinar | 6 | | |
| focal (10x field) | none | 0 | x | |
| | < 1 focus | 1 | | |
| | 2 ~ 4 foci | 2 | | |
| | 5 ~ 10 foci | 3 | | |
| | > 10 foci | 4 | | |
| 門脈發炎 | none | 0 | x | |
| | mild | 1 | | |
| | moderate | 2 | | |
| | moderate ~ marked | 3 | | |
| | marked | 4 | | |
| fibrosis (stage) | | | | |
| | none | 0 | F0 | |
| | some portal fibrosis | 1 | F1 | |
| | mostly portal fibrosis | 2 | F2 | |
| | few bridging fibrosis | 3 | F3 | |
| | many bridging fibrosis | 4 | F4 | |
| | incomplete cirrhosis | 5 | F5 | |
| | cirrhosis | 6 | F6 | |''',
        'image': '/explanations/cropped/111-2-醫學(三)-16_merged.png'
    },
    17: {
        'text': '''依照 Rome IV 的診斷標準，題目敘述的症狀符合腸躁症 (irritable bowel syndrome, IBS)。以前超愛考 Ulcerative Colitis vs. Crohn Disease，但從 108 起 IBS 比較受寵，即使如此外科還是很愛考 IBD 的比較，所以還是要複習一下喔！

IBS 可影響各年齡層，但第一次發作通常早於 45 歲、較常見於女性 (2~3x)。除題幹所述的表現外，IBS 患者也常伴隨脹氣、打嗝、消化不良、火燒心、噁心嘔吐、頭痛背痛等症狀。診斷方法主要靠臨床診斷 + 排除器質性問題，calprotectin 是看腸道發炎的程度，為診斷 inflammatory bowel disease (IBD) 的生物標記，也可監測疾病活性，不是 IBS 的 marker → (B) 錯誤

| Rome IV criteria for IBS | |
| :--- | :--- |
| 必須有的表現 | 以下三條件符合其二 |
| 過去三個月，每週至少一天反覆腹痛 | 與排便有關（拉完可變好或變壞） |
| | 排便頻率出現變化 |
| | 排便型態出現變化（可為便秘或腹瀉） |

病理機轉目前認為與腸道蠕動異常、腸道痛覺敏感 (hyperalgesia)、心理社會因素、菌腦腸軸 (brain-gut interaction) 異常、腸道感染（→ leaky gut dysbiosis）、基因問題、膽鹽吸收不良等有關

< 其他考點 >
1. 嚴重 IBS 患者約 80% 是女性、感染性腸炎後的 IBS 較常見於年輕女性。【109-2】
2. 依照 Rome IV criteria，「必須出現腹痛」的症狀，所以如果是無痛的腹瀉或便秘是不符合診斷的！
3. 低 FODMAP (fermentable oligosaccharides, disaccharides, monosaccharides, and polyols) 飲食可降低大腸細菌產氣，已被證實對於改善 IBS 有幫助''',
        'image': '/explanations/cropped/111-2-醫學(三)-17_merged.png'
    },
    18: {
        'text': '''(A) 錯誤，長在右側的預後比較差。過去的說法是腫瘤長在右側症狀比較不明顯 → 晚發現 → 預後差；但近年比較支持的說法是：好發於右側的腫瘤 molecular patterns 比好發於左側的更惡性
(B) 錯誤，淋巴結、肝臟是大腸癌最常轉移的地方（透過 portal venous circulation），因此最容易轉移的內臟器官應該是肝臟。而且大腸癌在轉移到肝臟前，極少會轉移到肺臟、鎖骨上淋巴結、骨頭或腦
(C) 篩檢大腸癌的主流方式是糞便潛血 (occult blood, OB) 檢查跟 DRE。篩檢的重點要符合經濟效益，測 CEA 很貴，不適合作為篩檢指標。但近年大腸癌有往近端大腸跑的趨勢（DRE 截不到），所以 NCCN guideline 開始建議以每年一次 OB + 5 年一次 sigmoidoscopy 或 10 年一次 colonoscopy 為篩檢的首選
(D) 正確，大多數大腸癌的切除後復發會在前四年內，所以五年存活率是治癒的可靠指標。五年存活率與 stage 有關，且至少需要拿到 12 顆 lymph nodes 才能執行正確 staging''',
        'image': '/explanations/cropped/111-2-醫學(三)-18_merged.png'
    },
    19: {
        'text': '''胃腺癌依照組織型態可分為兩種類型，整理如下表：

| 胃腺癌 (gastric adenocarcinoma) | | |
| :--- | :--- | :--- |
| | 瀰漫型 (diffuse type) | 腸道型 (intestinal type) |
| 流行病學 | 較少見 (20~30%)、年輕女性 | 較常見 (70~80%)、年長男性 |
| 風險因子 | CDH1 突變（E-cadherin 減少） | H.pylori 感染、萎縮性胃炎 |
| 環境因子 | 影響較小 | 影響較大（低社經地位者較易得） |
| 胃鏡表現 | 皮革胃 (linitis plastica) | 潰瘍腫塊 (ulcerated mass) |
| 分化程度 | 差 (poorly differentiated) | 好 (well differentiated glands) |
| 預後 | 很差 | 比 diffuse type 好 |

但最近 Asian cancer research group (ACRG) 開始用分子型態、基因來分型：

| ACRG 的胃癌分型 | | |
| :--- | :--- | :--- |
| 分型 | 突變 | 說明 |
| CIN (chromosomal instability) | TP53 mut.、RTK-RAS 活化 | 傳統上的腸道型 |
| GS (genomic stable) | CDH1 mut.、RHOA mut.、CLDN18-ARHGAP 融合 | 傳統上的瀰漫型、預後最差 |
| MSI (microsatellite instability-associated) | MLH1 silencing | 預後最好 |
| EBV（跟 EBV 相關） | PIK3CA mut.、PD-L1 過度表現、CDKN2A silencing | 約 8~10% 病人切片出來是 EBV positive |

(D) 錯誤，Krukenberg tumor 是指病理型態為 signet-ring cell 的癌症轉移到「卵巢」，常見的來源是腸胃道癌

< 其他考點 >
1. 消化性潰瘍 (peptic ulcer disease, PUD) 分兩大種，主要跟 H. pylori 感染還有 NSAID 的使用有關。PUD 最常見的併發症是流血 (15%)，其次為穿孔破裂 (6~7%)，胃出口阻塞 (gastric outlet obstruction, 1~2%) 相對少見

| 消化性潰瘍 (peptic ulcer disease, PUD) 比較 | | |
| :--- | :--- | :--- |
| | 胃潰瘍 (GU) | 十二指腸潰瘍 (DU) |
| 年紀 (peak) | 較晚，60 歲 | 較早，因症狀明顯 → 易發現 |
| 惡性率 | 較高（尤其是長在 fundus、超過 3 cm、有伴隨腫塊的） | 極低 |
| H.pylori 比例 | 較低（但仍是主因之一） | 較高 |
| 吃東西後 | 不會減輕 | 飯後比較不痛（半夜會痛） |
| 侵蝕方向 | 往左肝方向破出去 | 往後侵蝕 → 可能導致胰臟炎 |

2. 胃潰瘍 (GU) 可再細分為 4 型，整體趨勢：越靠近十二指腸的胃酸分泌越多

| 胃潰瘍 (gastric ulcer, GU) | | |
| :--- | :--- | :--- |
| 胃酸分泌 | 類型 | 發生位置 |
| 偏少 | type 1（最多） | 胃體 (gastric body) |
| | type 4 | 賁門 (cardia) |
| 少 ~ 正常 | type 2 | 胃竇 (antrum) |
| 正常 ~ 高 | type 3 | 距離 pylorus 3 cm 以內，常伴隨有 DU |''',
        'image': '/explanations/cropped/111-2-醫學(三)-19_merged.png'
    },
    20: {
        'text': '''不同營養素的吸收位置蠻常考的，要記熟！(B) 維他命 B12 (cobalamin) 主要在迴腸吸收，與其結合以抵禦水解酶的內在因子 (intrinsic factor) 是在胃部 parietal cells 製造的，都跟十二指腸無關，故切除十二指腸對其影響最小

| 營養素的吸收部位【107-2、109-2】 | |
| :--- | :--- |
| 部位 | 吸收的營養素 |
| 胃部 | 酒精 |
| 十二指腸 | Ca、Fe²⁺、葉酸（維他命 B9，在近端空腸也會吸收） |
| 迴腸 | 維他命 B12、膽鹽 |''',
        'image': '/explanations/cropped/111-2-醫學(三)-20_merged.png'
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
            q['explanation'] = EXPLANATIONS[num]['text']
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
    exp_map[key] = {
        'text': item['text'],
        'image': item['image']
    }

with open('src/data/explanations_map.json', 'w', encoding='utf-8') as f:
    json.dump(exp_map, f, ensure_ascii=False, indent=2)

print('Updated explanations_map.json successfully')
