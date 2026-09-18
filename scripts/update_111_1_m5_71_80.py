# -*- coding: utf-8 -*-
import json
import os
import cv2
import numpy as np

def read_img(p):
    return cv2.imdecode(np.fromfile(f\'scratch/pages_2022/page_{p}.jpg\', dtype=np.uint8), cv2.IMREAD_COLOR)

def write_img(path, img):
    ext = os.path.splitext(path)[1]
    res, buf = cv2.imencode(ext, img)
    with open(path, \'wb\') as f:
        f.write(buf)

os.makedirs(\'public/explanations/cropped\', exist_ok=True)

# 1. Image Cropping
# Q71: page 413 [500:990]
write_img(\'public/explanations/cropped/111-1-醫學(五)-71_merged.png\', read_img(413)[500:990, 40:930])

# Q72: page 111 [175:1310] + page 112 [140:385]
p111_q72 = read_img(111)[175:1310, 40:930]
p112_q72 = read_img(112)[140:385, 40:930]
write_img(\'public/explanations/cropped/111-1-醫學(五)-72_merged.png\', np.vstack([p111_q72, p112_q72]))

# Q73: page 109 [175:760]
write_img(\'public/explanations/cropped/111-1-醫學(五)-73_merged.png\', read_img(109)[175:760, 40:930])

# Q74: page 112 [890:1300]
write_img(\'public/explanations/cropped/111-1-醫學(五)-74_merged.png\', read_img(112)[890:1300, 40:930])

# Q75: page 178 [440:1310]
write_img(\'public/explanations/cropped/111-1-醫學(五)-75_merged.png\', read_img(178)[440:1310, 40:930])

# Q76: page 412 [1140:1310]
write_img(\'public/explanations/cropped/111-1-醫學(五)-76_merged.png\', read_img(412)[1140:1310, 40:930])

# Q77: page 113 [370:510]
write_img(\'public/explanations/cropped/111-1-醫學(五)-77_merged.png\', read_img(113)[370:510, 40:930])

# Q78: page 498 [1040:1310] + page 499 [140:600]
p498_q78 = read_img(498)[1040:1310, 40:930]
p499_q78 = read_img(499)[140:600, 40:930]
write_img(\'public/explanations/cropped/111-1-醫學(五)-78_merged.png\', np.vstack([p498_q78, p499_q78]))

# Q79: page 499 [1130:1310]
write_img(\'public/explanations/cropped/111-1-醫學(五)-79_merged.png\', read_img(499)[1130:1310, 40:930])

# Q80: page 500 [388:735]
write_img(\'public/explanations/cropped/111-1-醫學(五)-80_merged.png\', read_img(500)[388:735, 40:930])

print(\'Cropped images generated successfully\')

EXPLANATIONS = {
    71: {
        \'text\': \'\'\'Duplex ultrasound 表複合式超音波，由 real time（實況）及 Doppler 超音波所組成，用於男性勃起障礙功能的血管功能評估時可測量陰莖血管的大小、形狀及血流速度

(A) 在檢查前，會先往陰莖海綿體注射如前列腺素 E1 (Prostaglandin E1)、罌粟鹼 (Papaverine) 的血管舒張劑，使海綿體動脈擴張，達到勃起的條件，在此情況下使用超音波觀察血管搏動情形及血流速度的改變

(B) (C) RI（阻力指數）可判斷靜脈閉鎖是否正常，原則上希望 RI>0.75，當 RI<0.75 時表病人極有可能有靜脈漏的狀況

(D) 承 (A)，在給予血管舒張劑後，cavernous artery（海綿體動脈）的 peak systolic velocity (PSV) 為最能判斷陰莖動脈疾病的指標，當 PSV<25 cm/s 時，表可能有 arterial insufficiency 的情況\'\'\',
        \'image\': \'/explanations/cropped/111-1-醫學(五)-71_merged.png\'
    },
    72: {
        \'text\': \'\'\'病人主訴為吞嚥困難時，可先根據吞嚥困難的型態進行初步的鑑別診斷：

### 吞嚥困難

| Oropharyngeal 口咽問題 | Esophageal 食道問題 |
| :--- | :--- |
| 感覺食物卡在頸部、飲入液體易嗆到鼻子 (nasal regurgitation)、易嗆到、相關耳鼻喉症狀 | 感覺食物卡在頸部或胸骨處、食物嵌塞 (food impaction) |
| **結構問題** | **結構問題（固體食物吞嚥困難）** |
| • 腫瘤<br>• 咽部感染<br>• 近端食管蹼 (proximal esophageal webs)<br>• Zenker\'s diverticulum（憩室） | • 腫瘤<br>• 食道狹窄<br>• 食道裂孔疝氣 (hiatal hernia)<br>• 食道感染發炎 |
| **神經肌肉問題** | **神經肌肉問題（固體液體皆吞嚥困難）** |
| • 中風<br>• 帕金森氏症<br>• 脊髓側索硬化 (amyotropic lateral sclerosis, ALS)<br>• 中樞神經腫瘤<br>• 腦性麻痺 | • 胃食道逆流<br>• 食道弛緩不能 (achalasia)<br>• 瀰漫性食道痙攣 (diffuse esophageal spasm)<br>• 硬皮症 (scleroderma) |

（整理自 Harrison 20th ed. Chapter 40）

(A) achalasia（食道弛緩不能）：為遠端食道無法蠕動、食道下括約肌 (low esophageal sphincter) 無法舒張而導致食物無法順利吞嚥的疾病，在上消化道鋇劑攝影中可看到鳥嘴狀的影像（如題幹附圖右圖）

(B) GERD（胃食道逆流）：胃內食物及胃酸逆流回食道造成不適的疾病，有些人可能會覺得咽部有異物感；為症狀診斷的疾病，可藉由病人臨床症狀推測 GERD 的可能性，若進一步做內視鏡發現食道有發炎的情形可診斷為 reflux esophagitis（內視鏡診斷）；內視鏡發現異常病灶且病理報告顯示胃黏膜腸上皮化生 (intestinal metaplasia，指的是食道原有的扁平上皮被腸道柱狀上皮所取代)，可診斷為 Barrett\'s esophagus（病理診斷）

(C) gastric lymphoma（胃淋巴癌）可能藉由上消化道鋇劑攝影初步判定胃部是否有異常病灶，而後須藉由內視鏡加上切片檢查證實，並且透過內視鏡超音波評估胃壁侵犯範圍，另外搭配電腦斷層及骨髓檢查等評估是否有局部淋巴結或遠端轉移

(D) hiatal hernia（食道裂孔疝氣）：當食道 - 胃交界處的韌帶鬆掉時，腹部器官通過橫膈進入縱膈腔的疾病，在上消化道鋇劑攝影中可以看到一部分的胃穿過橫膈脫出，也可藉由電腦斷層或胃鏡進行診斷\'\'\',
        \'image\': \'/explanations/cropped/111-1-醫學(五)-72_merged.png\'
    },
    73: {
        \'text\': \'\'\'由附圖中可見 gallbladder 以下有明顯的 acoustic shadow，表 gallbladder 中的塊狀異物極有可能為石頭或鈣化物，故此題選 (D)

(A) 產氣性膽囊炎在超音波中的影像可分為 3 級：

| Stage I | 膽囊中可見氣體，且通常會有膽囊中充滿氣體時出現高回聲顯影與遠端迴響假影 (a dense band of hyperreflective echoes with distal reverberation) |
| :--- | :--- |
| Stage II | 膽囊壁可見氣體，膽囊壁會出現高回聲顯影與迴響假影 (an area of high reflectivity in the gallbladder wall) 且會隨患者不同動作而改變位置 |
| Stage III | 膽囊中及周圍組織可見氣體，表已出現壞疽 (gangrene) 或膽囊破裂 (perforation) |

(B) 肝膿瘍在超音波下可能為高回聲或低回聲影像，有時可見氣泡 (gas bubbles)；在都卜勒下不會看到血液灌流；產氣性肝膿瘍在電腦斷層下較可辨別氣體的產生

(C) 膽囊癌在超音波下通常可見膽囊壁異常增厚、膨脹不全，且常合併膽囊發炎，可能可在膽囊中看到異常的贅生物\'\'\',
        \'image\': \'/explanations/cropped/111-1-醫學(五)-73_merged.png\'
    },
    74: {
        \'text\': \'\'\'大多後腹膜腔腫瘤皆為惡性，且其中約 1/3 屬於軟組織肉瘤 (soft tissue sarcoma)，軟組織肉瘤中又以脂肪肉瘤 (liposarcoma, 70%) 佔大多數、其次為平滑肌肉瘤 (leiomyosarcoma, 15%)。其他常見的鑑別診斷包括：原發性生殖細胞瘤 (germ cell tumor，包括精細胞瘤 seminoma 及非精細胞瘤 non-seminoma)、淋巴瘤 (lymphoma) 及睪丸癌轉移病灶 (metastatic testicular cancer)

(B) 神經膠質瘤 (glioblastoma) 為最常見的中樞神經系統原發性惡性腫瘤，顱外轉移非常少見（約 <2%）且相對而言較常見於成年男性，與其他三個選項相比之下為較不可能出現於中年男性後腹腔腫瘤的鑑別診斷\'\'\',
        \'image\': \'/explanations/cropped/111-1-醫學(五)-74_merged.png\'
    },
    75: {
        \'text\': \'\'\'（此部分建議自行上網查找圖片搭配下述文字說明加深印象～）

首先要先回顧幾個重要的神經傳導路徑：

| 上行<br>(sensory) | 由 posterior spinal artery 支配（脊髓後 2/3，posterior cord） | Dorsal column | 在 medulla 交叉 | 本體感覺、震動覺、輕觸覺 |
| :--- | :--- | :--- | :--- | :--- |
| | 由 anterior spinal artery 支配（脊髓前 2/3，anterior cord） | Spinothalamic tract | 在 spinal cord 交叉 | 溫覺、痛覺 |
| 下行<br>(motor) | | Corticospinal tract | 在 medulla 交叉 | 肌肉運動 |

下列列出幾個 incomplete spinal cord injury 的種類：

| | | Central cord syndrome | Anterior cord syndrome | Posterior cord syndrome | Brown-Séquard syndrome |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 感覺喪失 | 震動覺、輕觸覺 | 若影響範圍大，雙側皆會喪失 | 正常 | 雙側喪失 | 同側喪失 |
| | 溫覺、痛覺 | | 雙側喪失 | 正常 | 對側喪失 |
| 動作喪失 | | | | | 同側喪失 |

(B) 中心脊髓症候群：除了有如上表所列之感覺及動作喪失的情況外，另一典型特徵為上肢通常比下肢嚴重，另外可以注意的是病人的排尿功能通常會是正常的 (sacral sparing)

(D) 馬尾症候群：當馬尾受到壓迫時，患者常會有下背、下肢麻木疼痛及神經功能缺損，且大小便的括約肌功能也可能受到影響，有些人可能出現性功能障礙。常見的成因包括椎間盤突出、脊椎管狹窄、外傷等\'\'\',
        \'image\': \'/explanations/cropped/111-1-醫學(五)-75_merged.png\'
    },
    76: {
        \'text\': \'\'\'若癌症轉移到脊椎附近壓迫脊髓，稱之為 metastatic spinal cord compression。症狀包括下肢或背部酸痛無力、四肢末端刺麻感、大小便失禁等。在此情況下，可給予病人止痛藥及給予 Dexamethasone 進行減壓以減緩症狀\'\'\',
        \'image\': \'/explanations/cropped/111-1-醫學(五)-76_merged.png\'
    },
    77: {
        \'text\': \'\'\'Compartment syndrome 以腔室內壓力 >30 mmHg 或腔室內壓力與舒張壓的差距在 10-30 mmHg 來診斷\'\'\',
        \'image\': \'/explanations/cropped/111-1-醫學(五)-77_merged.png\'
    },
    78: {
        \'text\': \'\'\'(A) (C) (D)
根據人類免疫缺乏病毒傳染防治及感染者權益保障條例第 13 條第 1 項：「醫事人員發現感染者應於 24 小時內向地方主管機關通報；其通報程序與內容，由中央主管機關訂定之。」第 14 條寫道：「主管機關、醫事機構、醫事人員及其他因業務知悉感染者之姓名及病歷等有關資料者，除依法律規定或基於防治需要者外，對於該項資料，不得洩漏。」法律並沒有明令規定需要告知患者家人或配偶，但對於可能有被傳染之虞的配偶、性伴侶或有可能發生性接觸者，理應享有知情權，好能有效地預防和控制愛滋病毒的傳播，也可幫助可能被傳染的人提早獲知感染事實，以維護其健康權。綜合上述，此議題中，法律雖沒有硬性規定醫師須告知愛滋病患者的可能性接觸者其得病的事實，但也基於健康權的維護，在醫師告知上述相關人士的情況下可免除侵害病人隱私權的法律責任。回到題目選項，此題最適當的選項為 (C)，醫師可告知病人太太，但並沒有非告知不可。(A) 相對而言有較硬性規定的感覺，或許這也是其非正解的原因

(B) 第 12 條第 3 像也明令：「感染者提供其感染事實後，醫事機構及醫事人員不得拒絕提供服務。」故醫師不可婉拒治療\'\'\',
        \'image\': \'/explanations/cropped/111-1-醫學(五)-78_merged.png\'
    },
    79: {
        \'text\': \'\'\'在這樣的情況下，應以病人個人意願為第一優先，雖題幹中病人已無清楚的意識可進行表達，但有明確證據顯示病人是極度拒絕輸血的，故即便情況危急，仍應尊重病人的自主權\'\'\',
        \'image\': \'/explanations/cropped/111-1-醫學(五)-79_merged.png\'
    },
    80: {
        \'text\': \'\'\'一般利益衝突的處置原則包括
(1) 公開揭露 (disclosure)：詳實具體地將所有利益關係公開揭露，為利益衝突管理的先決條件
(2) 審核 (review) 與核准 (authorization)：利益關係公開揭露後，由倫理委員會進行審核研究設計、過程極可能存在的倫理問題，並判定利益衝突是否影響臨床操作
(3) 禁止 (prohibition)：若利益衝突的情況可能傷害科學研究的廉政性或醫病關係的信賴，應予以明文禁止\'\'\',
        \'image\': \'/explanations/cropped/111-1-醫學(五)-80_merged.png\'
    }
}

# Check trailing periods rule
period_violations = []
for qnum, item in EXPLANATIONS.items():
    text = item[\'text\']
    for line_idx, line in enumerate(text.split(\'\n\'), 1):
        line = line.strip()
        if line.endswith(\'。\'):
            period_violations.append((qnum, line_idx, line))

if period_violations:
    print(\'ERROR: Trailing periods found:\')
    for v in period_violations:
        print(f\'  Q{v[0]} L{v[1]}: {v[2]}\')
    exit(1)
else:
    print(\'Zero trailing periods verified\')

# Check image paths exist
for qnum, item in EXPLANATIONS.items():
    img_path = item[\'image\']
    if img_path:
        local_path = \'public\' + img_path
        if not os.path.exists(local_path):
            print(f\'ERROR: Image not found on disk: {local_path}\')
            exit(1)

print(\'All referenced images exist on disk\')

# 2. Update questions.json
with open(\'src/data/questions.json\', \'r\', encoding=\'utf-8\') as f:
    questions = json.load(f)

updated_q_count = 0
for q in questions:
    qid = q.get(\'id\', \'\')
    if \'111-1\' in qid and \'醫學(五)\' in qid:
        num = int(q.get(\'number\', 0))
        if num in EXPLANATIONS:
            q[\'explanation\'] = EXPLANATIONS[num][\'text\']
            q[\'explanation_image\'] = EXPLANATIONS[num][\'image\']
            updated_q_count += 1

with open(\'src/data/questions.json\', \'w\', encoding=\'utf-8\') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f\'Updated {updated_q_count} questions in questions.json\')

# 3. Update explanations_map.json
with open(\'src/data/explanations_map.json\', \'r\', encoding=\'utf-8\') as f:
    exp_map = json.load(f)

for num, data in EXPLANATIONS.items():
    key = f\'111-1-醫學(五)-{num}\'
    exp_map[key] = {
        \'text\': data[\'text\'],
        \'image\': data[\'image\']
    }

with open(\'src/data/explanations_map.json\', \'w\', encoding=\'utf-8\') as f:
    json.dump(exp_map, f, ensure_ascii=False, indent=2)

print(\'Updated explanations_map.json with Q71-Q80\')
