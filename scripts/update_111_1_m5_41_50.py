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
# Q42: page 102 [134:1290] + page 103 [145:320]
p102_q42 = read_img(102)[134:1290, 40:930]
p103_q42 = read_img(103)[145:320, 40:930]
write_img('public/explanations/cropped/111-1-醫學(五)-42_merged.png', np.vstack([p102_q42, p103_q42]))

# Q43: page 104 [134:725]
p104_q43 = read_img(104)[134:725, 40:930]
write_img('public/explanations/cropped/111-1-醫學(五)-43_merged.png', p104_q43)

# Q44: page 103 [580:1055]
p103_q44 = read_img(103)[580:1055, 40:930]
write_img('public/explanations/cropped/111-1-醫學(五)-44_merged.png', p103_q44)

# Q45: page 105 [555:1310]
p105_q45 = read_img(105)[555:1310, 40:930]
write_img('public/explanations/cropped/111-1-醫學(五)-45_merged.png', p105_q45)

# Q46: page 104 [970:1310] + page 105 [145:380]
p104_q46 = read_img(104)[970:1310, 40:930]
p105_q46 = read_img(105)[145:380, 40:930]
write_img('public/explanations/cropped/111-1-醫學(五)-46_merged.png', np.vstack([p104_q46, p105_q46]))

# Q47: page 106 [550:1310] + page 107 [130:1315]
p106_q47 = read_img(106)[550:1310, 40:930]
p107_q47 = read_img(107)[130:1315, 40:930]
write_img('public/explanations/cropped/111-1-醫學(五)-47_merged.png', np.vstack([p106_q47, p107_q47]))

# Q48: page 108 [390:895]
p108_q48 = read_img(108)[390:895, 40:930]
write_img('public/explanations/cropped/111-1-醫學(五)-48_merged.png', p108_q48)

# Q49: page 109 [980:1305] + page 110 [120:690]
p109_q49 = read_img(109)[980:1305, 40:930]
p110_q49 = read_img(110)[120:690, 40:930]
write_img('public/explanations/cropped/111-1-醫學(五)-49_merged.png', np.vstack([p109_q49, p110_q49]))

# Q50: page 154 [770:1295] + page 155 [130:760]
p154_q50 = read_img(154)[770:1295, 40:930]
p155_q50 = read_img(155)[130:760, 40:930]
write_img('public/explanations/cropped/111-1-醫學(五)-50_merged.png', np.vstack([p154_q50, p155_q50]))

print("Cropped images generated successfully")

EXPLANATIONS = {
    41: {
        "text": "缺頁",
        "image": None
    },
    42: {
        "text": """有 GERD 的病人一般來說會先建議進行生活習慣調整以及服用 PPI 治療，若症狀未見改善，可進一步評估是否適合進行手術，相關檢查包括食道酸鹼值檢查 (pH testing)、食道壓力計 (esophageal manometry)、食道攝影 (video esophagram) 及上消化道內視鏡檢查與切片 (upper endoscopy with biopsy)。另外也可考慮胃排空檢查 (gastric emptying study) 或 CT

#### GERD 術前檢查
| 檢查項目 | 意義與評估重點 |
| :--- | :--- |
| 食道酸鹼值檢查<br>(pH testing) | 可確認胃食道逆流的存在，並了解逆流程度與臨床症狀的相關性 |
| 食道壓力計<br>(esophageal manometry) | 評估食道蠕動功能及下食道括約肌壓力<br>• 當食道蠕動功能差且酸鹼值檢查顯示有胃食道逆流情形，則患者相較於 full wrap (完全包埋)，會更適合短鬆或局部 (floppy or partial) 胃底部折疊術 (fundoplication)<br>• 下食道括約肌壓力低時，表病人對藥物治療的失敗率或復發率較高，可建議進行手術 |
| 食道 or 上消化道攝影<br>(video esophagram) | 若攝影中發現逆流情況，可加以輔助診斷，雖此法的特異性和敏感度低，但可同時診斷裂孔疝氣、食道狹窄或食道其他構造上的病變 |
| 上消化道內視鏡檢查與切片 (upper endoscopy with biopsy) | 為逆流性食道炎的黃金診斷標準，可評估逆流嚴重程度，也可透過切片判定是否有 Barrett's esophagus 或食道癌等 |

*(整理自 2021 Sabiston Chapter 42)*

在確定病人症狀源自於胃酸逆流後，可評估病人臨床狀況是否能夠承受手術，其中 Nissen fundoplication 為標準的抗胃酸逆流手術

(A) Heller esophageal myotomy（Heller 氏賁門肌肉切開術）：透過切除下食道括約肌及胃賁門局部肌肉緩解壓力，為治療食道弛緩不能 (achalasia) 的手術手段之一

(B) sleeve gastrectomy（袖狀胃切除術）：為減肥手術的一種；將囊狀胃裁切掉胃大彎側的一部分，使胃容量減少及影響腸道荷爾蒙分泌與能量消耗，以協助病人達到減重的目的（詳見 111-2 第 52 題）

(C) biliopancreatic diversion（膽胰分流術）：亦為減肥手術的一種（同上，詳見 111-2 第 52 題）

(D) Nissen fundoplication（胃底折疊術）：將賁門附近胃組織包覆在下食道外圍並用縫線固定，增加食道下端壓力，以減緩胃食道逆流""",
        "image": "/explanations/cropped/111-1-醫學(五)-42_merged.png"
    },
    43: {
        "text": """胃、食道靜脈瘤為肝硬化常見的併發症，若經藥物及內視鏡治療 (ligation) 後仍反覆出血者，可考慮 TIPS 或手術分流 (surgical shunt) 控制肝門脈高壓，肝臟移植則為唯一有機會根治肝硬化的方法

(A) TIPS：經由頸靜脈將分流支架放置於肝臟內，建立門經脈與肝靜脈間的新通道，使血液不會積聚於肝臟中，藉此改善肝門脈高壓造成他處靜脈曲張甚至出血的情況，只能控制無法根治

(B) Warren shunt：又稱為 selective distal splenorenal shunt（選擇性遠端脾腎靜脈分流術），作法為游離脾靜脈並結紮脾靜脈進入胰腺的細小靜脈、腸繫膜下靜脈、冠狀靜脈等，同時游離腎靜脈並結紮左腎上腺靜脈，最後將脾靜脈與腎靜脈吻合；如此一來，門脈高壓時流向脾靜脈的血液會被分流到腎靜脈，可避免靜脈瘤繼續變大破裂而出血

(D) 肝臟移植為根本解決肝硬化問題的唯一方法""",
        "image": "/explanations/cropped/111-1-醫學(五)-43_merged.png"
    },
    44: {
        "text": """(A) 肝細胞腺瘤 (liver cell adenoma) 主要發生於年輕女性且常與長期類固醇激素的使用（如避孕藥）有關，常見出血及壞死，另外也可能轉變為惡性的肝細胞癌

(B) 肝血管瘤 (hemangioma) 為肝臟中最常見的良性腫瘤，好發於中年女性，通常沒什麼症狀，但達一定大小可能壓迫腹部造成不適；自發性破裂或出血非常罕見

(C) 肝臟局部增生性結節 (focal nodular hyperplasia) 為肝臟中繼肝血管瘤第二常見的良性腫瘤，通常沒什麼症狀，出血、破裂等情況也非常罕見

(D) 肝臟單純囊腫 (simple cyst) 為充滿液體的囊狀物，通常無症狀，且增大緩慢；可能因受到感染而破裂，僅極少數未進行治療的肝囊腫會演進為癌症""",
        "image": "/explanations/cropped/111-1-醫學(五)-44_merged.png"
    },
    45: {
        "text": """甲狀腺癌 TNM staging :

#### <55 歲
| T | N | M |
| :--- | :--- | :--- |
| I 任何腫瘤大小 | 任何淋巴結轉移狀況 | 沒有遠端轉移 |
| II | | 有遠端轉移 |

#### ≥ 55 歲
| T | N | M |
| :--- | :--- | :--- |
| I 腫瘤 ≤ 4cm 且侷限於甲狀腺 | 沒有淋巴結轉移 | 沒有遠端轉移 |
| II 任何腫瘤大小且有淋巴結轉移或帶狀肌群侵犯 (strap muscle: sternohyoid, sternothyroid, thyrohyoid, omohyoid) | | |
| III 侵犯至皮下轉組織、喉、氣管、食道或喉返神經 | 任何淋巴結轉移狀況 | |
| IVa 侵犯至椎前筋膜或包覆頸動脈或包覆縱隔血管 | | |
| IVb 任何腫瘤大小 | | 有遠端轉移 |

由此可見，腫瘤大小、遠端轉移的有無及病人年齡都會影響甲狀腺癌的 staging，進而影響預後""",
        "image": "/explanations/cropped/111-1-醫學(五)-45_merged.png"
    },
    46: {
        "text": """甲狀腺切除術的三大術後併發症：
(1) 傷及 recurrent laryngeal nerve：可能導致聲帶麻痺、吞嚥困難、易嗆到等；當傷及雙側 recurrent laryngeal nerve 時，肌肉可能因麻痺而緊靠，造成呼吸困難
(2) 副甲狀腺功能低下 (hypoparathyroidism)：為甲狀腺手術最常見的併發症，由於副甲狀腺緊貼於甲狀腺後外側，在將甲狀腺切除後會一併去掉副甲狀腺而造成病人易有血鈣低的問題
(3) 術後頸部血腫：當手術部位出血並於頸部產生血腫，容易壓迫到氣管造成呼吸困難

(D) 困難插管造成的 laryngeal edema 不僅限於甲狀腺切除術，若病人因困難插管而導致 laryngeal edema，無論術式為何都可能會有呼吸困難的併發症發生""",
        "image": "/explanations/cropped/111-1-醫學(五)-46_merged.png"
    },
    47: {
        "text": """(A) Neuroendocrine tumors 所引起的特定症候群 (包括 insulinoma) 不可靠單靠免疫染色進行診斷，而是應搭配臨床症狀才能下診斷

#### 常見的 GI NET syndromes
| 功能性症候群 | 分泌胜肽類型 | 發生率 | 惡性率 | 主要症狀 |
| :--- | :--- | :--- | :--- | :--- |
| Carcinoid syndrome 類癌症候群 | serotonin (血清素) | 0.5~2% | 95~100% | • 腹瀉 (32~84%)<br>• 臉潮紅 (63~75%)<br>• 疼痛 (10~34%)<br>• 氣喘 (4~18%)<br>• 心臟疾病 (11~41%) |
| Zollinger-Ellison syndrome | gastrin (促胃泌素) | 0.5~1.5% | 60~90% | • 疼痛 (79~100%)<br>• 腹瀉 (30~75%)<br>• 食道症狀 (如：胃食道逆流，31~56%) |
| Insulinoma 胰島素瘤症候群 | insulin | 1~2% | <10% | • 低血糖症狀——Whipple triad：低血糖值、低血糖症狀、補充糖分症狀緩解 |
| VIPoma 血管活性腸道胜肽瘤症候群 | vasoactive intestinal peptide | 0.05~0.2% | 40~70% | • 腹瀉 (90~100%)<br>• 低血鉀 (80~100%)<br>• 脫水 (83%) |
| Glucagonoma 升糖素瘤症候群 | glucagon | 0.01~0.1% | 50~80% | • 皮膚紅疹 (67~90%)<br>• 葡萄糖耐受不良 (38~87%)<br>• 體重減輕 (66~96%) |

*(整理自 Harrison 20th ed. Chapter 80)*

(B) 患有 glucagonoma 的病人約有 67~90% 都會有特殊的皮膚病變——壞死溶解性游走狀紅斑 (necrolytic migrating erythema)，並且通常伴隨葡萄糖耐受不良 (glucose intolerance, 38~87%)、體重減輕 (66~96%)、貧血 (33~85%)、腹瀉 (15~29%)、血栓栓塞 (thromboembolism, 11~24%) 等症狀

(C) 神經內分泌瘤的病理分級如下：

#### NET grading
| 分類 | 病理分級 (grade) | 核分裂計量 (mitotic count, per 10 HPF) | Ki-67 指數 |
| :--- | :--- | :--- | :--- |
| NET | G1 (low grade) | <2 | ≥ 2% |
| NET | G2 (intermediate grade) | 2~20 | 3~20% |
| NEC (neuroendocrine carcinoma) | G3 (high grade) | >20 | >20% |

*(整理自 Harrison 20th ed. Chapter 80)*

(D) 神經內分泌腫瘤為功能性或非功能性，取決於是否會產生荷爾蒙症候群，因此即使會分泌胜肽的腫瘤只要不會造成荷爾蒙症狀就可被歸類到非功能性神經內分泌腫瘤；chromogranin 為在大型分泌顆粒 (large secretory granules) 中可見到的酸性單體可溶性蛋白質 (acidic monomeric soluble protein)，在非功能性神經內分泌腫瘤中也有 9 成以上可能分泌 chromogranin，可協助診斷與追蹤""",
        "image": "/explanations/cropped/111-1-醫學(五)-47_merged.png"
    },
    48: {
        "text": """Paget disease 又稱為乳頭濕疹樣乳癌，為位在乳頭及乳暈周圍外觀似濕疹的疾病，可能伴隨皮膚發癢，甚至演進變為硬皮 (crusting)、產生潰瘍 (ulceration)。雖然 Paget disease 僅佔乳癌病人 1% 左右，但有 80% 病人診斷出 Paget disease 後可能在後續檢查中診斷出乳癌。一半的病人觸診可摸到腫塊，這類病人中又有 90% 會被發現有侵襲性乳癌 (invasive breast cancer)

Paget disease 本身為原位癌 (carcinoma in situ)，屬於零期乳癌，預後好，手術後幾乎可痊癒。但若合併有腫塊，由於常合併侵襲性乳癌而須根據分期進行後續的治療安排。一般來說，合併有腫塊或影像學有異常的 Paget disease 患者較適合乳房全切除術＋腋下淋巴結廓清；若沒有合併腫塊也沒有影像學上的明顯病灶則可考慮局部切除＋腋下淋巴結廓清＋後續放射線治療避免復發""",
        "image": "/explanations/cropped/111-1-醫學(五)-48_merged.png"
    },
    49: {
        "text": """#### BI-RADS (Breast Imaging Reporting and Data System final assessment category)
| Category | 代表意義 | 後續安排 |
| :--- | :--- | :--- |
| 0 | Incomplete assessment<br>評估未完成 | 需要再做其他影像學檢查或與更早以前做的乳房攝影結果進行比較 |
| 1 | Negative 沒有特定異常發現 | 通常建議每年追蹤一次 |
| 2 | Benign finding 良性病灶發現 | |
| 3 | Probably benign finding (<2% malignant)<br>可能為良性病灶 | 建議 short-interval 追蹤 (通常 6 個月一次) |
| 4 | Suspicious abnormality (2%~95% malignant)<br>懷疑有惡性病灶<br>• 4A：低度懷疑 (2~10%)<br>• 4B：中度懷疑 (10~50%)<br>• 4C：高度懷疑 (50~95%) | 建議取得組織樣本進行化驗 |
| 5 | Highly suggestive of malignancy (>95% malignant) 高度懷疑為惡性病灶 | |
| 6 | Known biopsy 已有組織報告證明為惡性腫瘤 | 根據惡性腫瘤型態進行後續治療 |""",
        "image": "/explanations/cropped/111-1-醫學(五)-49_merged.png"
    },
    50: {
        "text": """TRAM flap 為乳房重建最常使用的皮瓣之一，術中將腹部的腹直肌連同皮膚、皮下脂肪構成的皮瓣直接經由皮下轉移至乳房，過程中不需顯微手術接血管。另一常取用的皮瓣為 LD flap (LD = Latissimus Dorsi 闊背肌)，作法為將闊背肌肌肉連同皮膚轉移至胸部。下列表格列舉此二種 flap 的比較：

| 評估項目 | TRAM flap | LD flap |
| :--- | :--- | :--- |
| 適應症 | • 各種尺寸的乳房<br>• 乳房下垂 (breast ptosis) | • 較小的乳房<br>• 輕微乳房下垂<br>• 因有疤或組織不足等問題而無法取得腹部皮瓣<br>• 過去乳房重建的再次修補 (salvage of previous breast reconstruction) |
| 相對禁忌症 | • 抽菸<br>• 腹部抽脂手術<br>• 腹部開過刀<br>• 肺部疾病<br>• 肥胖 | • 預定術後進行放射線治療<br>• 雙側乳房重建<br>• 嚴重乳房下垂 |
| 絕對禁忌症 | • 曾做過腹部成型術 (abdominoplasty)<br>• 病人無法接受 4~6 週的恢復期<br>• 病人無法承受長時間手術 | • 側開胸 (lateral thoracotomy)<br>• 欲重建範圍較大的患者 (very large breast in patients who does not require reduction) |
| 優點 | • 重建的乳房較自然、對稱、柔軟<br>• 成功率高<br>• 免顯微接血管 | • 手術時間短、術後恢復快<br>• 成功率高 |
| 缺點 | • 可能有部分脂肪或皮瓣壞死<br>• 腹部後遺症，如疝氣、腹部無力<br>• 術後腹部疼痛 | • 皮瓣量經常不夠且易萎縮<br>• 觸感不好（較硬）、肩部有時會緊緊的 |

*(整理自 Sabiston Chapter 36)*""",
        "image": "/explanations/cropped/111-1-醫學(五)-50_merged.png"
    }
}

# Check trailing periods rule
period_violations = []
for qnum, item in EXPLANATIONS.items():
    text = item['text']
    for line_idx, line in enumerate(text.split('\n'), 1):
        line = line.strip()
        if line.endswith('。'):
            period_violations.append((qnum, line_idx, line))

if period_violations:
    print("ERROR: Trailing periods found:")
    for v in period_violations:
        print(f"  Q{v[0]} L{v[1]}: {v[2]}")
    exit(1)
else:
    print("Zero trailing periods verified")

# Check image paths exist
for qnum, item in EXPLANATIONS.items():
    img_path = item['image']
    if img_path:
        local_path = 'public' + img_path
        if not os.path.exists(local_path):
            print(f"ERROR: Image not found on disk: {local_path}")
            exit(1)

print("All referenced images exist on disk")

# 2. Update questions.json
with open('src/data/questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

updated_q_count = 0
for q in questions:
    qid = q.get('id', '')
    if '111-1' in qid and '醫學(五)' in qid:
        num = int(q.get('number', 0))
        if num in EXPLANATIONS:
            q['explanation'] = EXPLANATIONS[num]['text']
            q['explanation_image'] = EXPLANATIONS[num]['image']
            updated_q_count += 1

with open('src/data/questions.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"Updated {updated_q_count} questions in questions.json")

# 3. Update explanations_map.json
with open('src/data/explanations_map.json', 'r', encoding='utf-8') as f:
    exp_map = json.load(f)

for num, data in EXPLANATIONS.items():
    key = f"111-1-醫學(五)-{num}"
    exp_map[key] = {
        "text": data["text"],
        "image": data["image"]
    }

with open('src/data/explanations_map.json', 'w', encoding='utf-8') as f:
    json.dump(exp_map, f, ensure_ascii=False, indent=2)

print(f"Updated explanations_map.json with Q41-Q50")
