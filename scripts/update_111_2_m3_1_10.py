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
# Q1: page 86 [465:1000]
write_img('public/explanations/cropped/111-2-醫學(三)-1_merged.png', read_img(86)[465:1000, 40:930])

# Q2: page 25 [715:880]
write_img('public/explanations/cropped/111-2-醫學(三)-2_merged.png', read_img(25)[715:880, 40:930])

# Q3: page 25 [1130:1315] + page 26 [170:640]
p25_q3 = read_img(25)[1130:1315, 40:930]
p26_q3 = read_img(26)[170:640, 40:930]
write_img('public/explanations/cropped/111-2-醫學(三)-3_merged.png', np.vstack([p25_q3, p26_q3]))

# Q4: page 27 [730:1315] + page 28 [170:1315] + page 29 [170:790]
p27_q4 = read_img(27)[730:1315, 40:930]
p28_q4 = read_img(28)[170:1315, 40:930]
p29_q4 = read_img(29)[170:790, 40:930]
write_img('public/explanations/cropped/111-2-醫學(三)-4_merged.png', np.vstack([p27_q4, p28_q4, p29_q4]))

# Q5: page 26 [920:1315] + page 27 [170:500]
p26_q5 = read_img(26)[920:1315, 40:930]
p27_q5 = read_img(27)[170:500, 40:930]
write_img('public/explanations/cropped/111-2-醫學(三)-5_merged.png', np.vstack([p26_q5, p27_q5]))

# Q6: page 30 [170:780]
write_img('public/explanations/cropped/111-2-醫學(三)-6_merged.png', read_img(30)[170:780, 40:930])

# Q7: page 30 [1215:1315] + page 31 [170:715]
p30_q7 = read_img(30)[1215:1315, 40:930]
p31_q7 = read_img(31)[170:715, 40:930]
write_img('public/explanations/cropped/111-2-醫學(三)-7_merged.png', np.vstack([p30_q7, p31_q7]))

# Q8: page 32 [170:700]
write_img('public/explanations/cropped/111-2-醫學(三)-8_merged.png', read_img(32)[170:700, 40:930])

# Q9: page 34 [170:980]
write_img('public/explanations/cropped/111-2-醫學(三)-9_merged.png', read_img(34)[170:980, 40:930])

# Q10: page 32 [1015:1285]
write_img('public/explanations/cropped/111-2-醫學(三)-10_merged.png', read_img(32)[1015:1285, 40:930])

print('Cropped images generated successfully')

EXPLANATIONS = {
    1: {
        'text': '''第一步先算 mOsm/d：450 (mOsm/L) × 3.5 (L/d) = 1575 > 1000 → 選 (A)，收工。如果今天算出來 < 800 就是 water diuresis，可再分為 primary polydipsia、central DI 與 nephrogenic DI

| 多尿 (polyuria) | | | |
| :--- | :--- | :--- | :--- |
| > 1000 mOsm/d | < 800 mOsm/d | | |
| 溶質性利尿<br>(osmotic, solute diuresis) | 水利尿 (water diuresis) | | |
| | 血 Na < 136、限水後尿 Osm 上升 | 血 Na > 143、限水後尿 Osm 差不多 | |
| | primary polydipsia | 尿崩症 (diabetes insipidus, DI) | |
| | | dDAVP 反應好 | dDAVP 反應差 |
| | | central DI | nephrogenic DI |''',
        'image': '/explanations/cropped/111-2-醫學(三)-1_merged.png'
    },
    2: {
        'text': '''懷孕期間的高血壓用藥包含 methyldopa、labetalol、nifedipine、hydralazine 等。孕婦不可以使用 ACE-i、ARB 或 ARNI，(A) 選項給他選下去，同一次考試考了兩次一樣的觀念，現賺 2.5 分''',
        'image': '/explanations/cropped/111-2-醫學(三)-2_merged.png'
    },
    3: {
        'text': '''急性主動脈症候群 (acute aortic syndrome) 會出現 sudden onset 撕裂性的嚴重胸痛。若發生在升主動脈，疼痛部位在前胸正中間；發生在降主動脈者，疼痛位置大多在後背。其產生與以下幾種原因相關：外傷、高血壓、懷孕、bicuspid aortic valve、感染、先天結締組織疾病（如：Marfan、Ehlers-Danlos），本題選 (D)

< 其他考點 >
急性主動脈症候群可細分為以下三種類型：

| 類型 | 特徵 |
| :--- | :--- |
| 急性主動脈剝離<br>(acute aortic dissection) | 內膜層有破口 (intimal tear) → 在主動脈壁 adventitia 及 media 間形成 false lumen |
| 急性主動脈壁內血腫<br>(acute intramural hematoma, IMH) | 供應管壁營養的小血管 vasa vasorum 破裂 |
| 穿透性粥狀動脈潰瘍 (penetrating atherosclerotic ulcer, PAU) | 1. 粥狀動脈硬化斑塊侵蝕 aortic media<br>2. 常發生於降胸主動脈的中端～遠端 |''',
        'image': '/explanations/cropped/111-2-醫學(三)-3_merged.png'
    },
    4: {
        'text': '''(A) Chvostek\'s sign (Chvostek-Weiss sign) 是低血鈣的表現，透過輕敲病人耳前的 facial n. → 引發嘴周 (circumoral) 肌肉痙攣。低血鈣會出現 QT prolong，嚴重者可出現癲癇以及各種神經興奮的 spasm 如：carpopedal spasm、bronchospasm、laryngospasm 等
(B) 主動脈逆流 (aortic regurgitation) 有一堆人名 sign，已經考過的整理如下表。本選項的 Duroziez\'s sign 是指在用聽診器輕壓 femoral a. 時可聽到 to-and-fro murmur

| 搏動 | 表現 | 心音 sign | 表現 |
| :--- | :--- | :--- | :--- |
| Corrigan\'s pulse | water-hammer pulse | Traube\'s sign | pistol-shot boom |
| Quincke\'s pulse | 按甲床時忽白忽紅 | Duroziez\'s sign | to-and-fro murmur |
| De Musset\'s sign | 每拍心跳會伴隨點頭，像鳥在走路 | Austin-Flint murmur | 低頻 rumbling 舒張中後期雜音 |

＊尚未考過：Müller\'s sign（看到 uvula 搏動）、Gerhardt\'s sign（= Sailer\'s sign，摸到 spleen 搏動）、Hill\'s sign（popliteal 收縮壓比 brachial 的高 ≥ 60 mmHg）、Landolfi\'s sign（瞳孔隨心搏縮放）、Becker\'s sign（眼底鏡可見視網膜小動脈搏動）

(C) Kussmaul\'s sign 跟 Kussmaul\'s breathing 是不一樣的喔！Kussmaul\'s sign 可見於 constrictive pericarditis 的病人，是吸氣時 JVP「沒有下降、甚至上升」的表現；Kussmaul\'s breathing 才跟代謝酸中毒有關（如 DKA），下表為常考的異常呼吸型態：

| 異常呼吸型態 | | |
| :--- | :--- | :--- |
| 呼吸 | 型態 | 可見於何種病人 |
| Cheyne-Stokes<br>(週期性、潮式呼吸) | 淺慢 → 變深變快 → 又變淺慢 → 暫停 | 兩側大腦半球損傷（多伴隨輕度 coma）、鬱血性心衰竭、OSA |
| Biot\'s respiration | 深度、速率都不規則 | 延腦損傷或受壓迫、鴉片中毒 |
| Kussmaul\'s breathing | 深且快<br>(↑ tidal volume) | 代謝酸中毒 (DKA)、橋腦中腦損傷 |
| agonal breathing | 呼吸困難並有怪異發聲 | 延腦損傷、臨終病人 |
| paradoxical breathing | 吸氣胸腔下陷、腹腔上升（跟腹式呼吸相反） | 連枷胸、橫膈肌受損或麻痺 |

(D) Romberg\'s test 用來測試本體感覺與平衡，閉眼會晃為 Romberg sign (+)，代表有感覺性共濟失調 (sensory ataxia)。小腦損傷的張眼閉眼都會晃；脊髓後柱損傷的閉眼時會特別晃

< 其他考點 >
1. 相似的現象：

| 現象 | 說明 |
| :--- | :--- |
| electrical alternans | ECG 上 V2 ~ V4 的 QRS 忽大忽小<br>（暗示有心包積液，所以 tamponade 患者可能有） |
| pulsus alternans | 脈搏忽大忽小（暗示有嚴重左心衰竭） |
| pulsus paradoxus | 吸氣時 SBP 下降 > 10 mmHg<br>（cardiac tamponade、COPD、低血容休克等可見） |
| Kussmaul\'s sign | 吸氣時 JVP 沒有下降，甚至上升<br>（constrictive pericarditis 可見，tamponade 沒有！） |
| paradoxical breathing | 吸氣胸腔下陷、腹腔上升（可見於連枷胸） |

2. cardiac tamponade：
a. 經典症狀：Beck\'s triad（低血壓 + JVP 上升 + distant heart sounds）
b. 可出現：electrical alternans、pulsus paradoxus
c. 不會出現：Kussmaul\'s sign

3. Trousseau\'s 的比較：

| 徵候 | 說明 |
| :--- | :--- |
| Trousseau\'s sign<br>(低血鈣的表現) | 用量血壓的 cuff 充氣到病人 SBP+20 mmHg 維持 3 min → 引發手部肌肉痙攣（拇指 adduction、MCP flexion、IP joint extension、手腕 flexion） |
| Trousseau\'s syndrome | 即 migratory thrombophlebitis，屬 paraneoplastic syndrome，與 GI 癌症有關（特別是胰臟癌） |''',
        'image': '/explanations/cropped/111-2-醫學(三)-4_merged.png'
    },
    5: {
        'text': '''傷害感受器 (nociceptor) 的初級神經元經由 dorsal root 進入脊髓、終止於 dorsal horn、釋放出訊號傳給次級神經元（如：glutamate、substance P、CGRP）。每一個初級神經元會傳訊給數個次級神經元，而每一個次級神經元也會接受多個初級神經元的訊號，這就是轉移痛的重點機制，因為不同部位會共用同一個次級神經元，大腦分不出來到底 primary 在哪，就會認定是比較常發出訊號的來源（通常是同 segment 相對應的體表）在發出疼痛訊號
(A)(B)(C) 正確

| 原發疼痛位置 | 轉移痛位置 |
| :--- | :--- |
| 橫膈、肝臟 | 肩膀 (C3-C4) |
| 胸腔（心、肺） | 左頸、左肩、上腹部 |
| 膽道發炎 | 右鎖骨上、右肩胛骨下端 |
| 脾臟受傷、膿瘍 | 左肩 (Kehr\'s sign) |

(D) 錯誤，轉移痛的區域就是被大腦判定同 segment 比較常發出訊號的區域，壓他會加重那個地方繼續痛，但不會讓原發處變明顯''',
        'image': '/explanations/cropped/111-2-醫學(三)-5_merged.png'
    },
    6: {
        'text': '''(A) 正確，典型心絞痛的病人在休息時的靜態標準十二導程 ECG 可能是正常的，而且 ST segment、T wave 的變化並不 specific，也可能在心包膜異常的患者身上出現，故無法用於確診。但運動心電圖如果出現 ST segment downsloping 下降超過 0.1 mV、且持續超過 0.08 s，就可以確診
(B) 錯誤，運動心電圖檢查的死亡風險不高，約只有 1/10000；發生非致命性並發症的風險約 2/100000，但檢查場所還是要準備急救器材
(C) 正確，藥物催迫性核醫心肌灌注造影可以檢查心肌缺氧以及心肌受傷後瘢痕組織，目前較常使用的是 Dipyridamole（舊商品名 Persantine），另外也可用 adenosine 或是 inotropic agents 模擬運動狀態
(D) 錯誤，心臟電腦斷層鈣化指數較高者，通常的確有較高機率是阻塞性 CAD；但有症狀的病人如果鈣化指數 < 400，就比較沒辦法準確排除 CAD，尤其是有心絞痛的年輕患者，主要會是非鈣化、或鈣化不嚴重的粥狀動脈斑塊，故不一定準確''',
        'image': '/explanations/cropped/111-2-醫學(三)-6_merged.png'
    },
    7: {
        'text': '''判讀運動心電圖時，要參考平時休息的狀態以及 risk factors 來判斷 CAD 的可能性。通常那種休息時正常，運動時才出現異常的，就有比較高的機率是真的有冠心病；本來就有其他心臟問題的，在運動心電圖時出現異常不見得是冠狀動脈問題

| Stress ECG 結果判讀 | |
| :--- | :--- |
| 高機率是 CAD | > 50 歲有 typical angina 的男性，運動過程中出現胸部不適 |
| 偽陽性機率高 | < 40 歲無症狀男性 |
| | 無其他風險因子的停經前女性 |
| | 有在使用 digitalis 或抗心律不整藥 → (D) |
| | 有心室內傳導異常 → (A) |
| | 心室肥厚 → (B) |
| | 靜態心電圖就有 ST segment 升高或 T wave 異常 |
| | 血鉀異常 |
| 偽陰性機率高 | 只有 circumflex artery 阻塞（12 導程 ECG 無法良好反應 posterolateral 區的缺血狀況） |

（參考 Harrison 21/e Ch.273）''',
        'image': '/explanations/cropped/111-2-醫學(三)-7_merged.png'
    },
    8: {
        'text': '''(A) 正確，電腦斷層高鈣化指數者有較高粥狀動脈硬化的風險，心血管疾病死亡率也較高。根據 Agatston score 可分為 minimal (0-10)、mild (10-100)、moderate (100-400)、severe (>400) 等，較嚴重者建議安排運動心電圖或壓力催迫性核醫心肌灌流檢查，以量化缺血程度、組織存活率，以便評估是否要接受 revascularization
(B) 正確，非心臟手術的術前評估項目包含：手術時間、術式、麻醉方式、病人年紀以及心血管疾病風險因子、是否有心雜音、胸痛、喘、周邊水腫等異常
(C) 錯誤，雖然如果 SPECT 顯示為 normal，每年發生重大心血管事件的機率的確很低 (<1%)，但還是需要追蹤
(D) 正確，雖然壓力催迫性核醫心肌造影的 negative predictive value 很高，但 AMI 不一定只發生在冠狀動脈阻塞的病人身上，如果 plaque 結構不穩定，一樣有可能會破裂產生血栓''',
        'image': '/explanations/cropped/111-2-醫學(三)-8_merged.png'
    },
    9: {
        'text': '''居然考這個 ( • _ • )
在核醫的檢查結果中，【圖一】的 MPI 可見左心室側壁 (lateral wall) 與心尖 (apex) 的灌流較差，前壁灌流很好；而在【圖二】[18F]FDG PET 可見存活 (viable) 心肌，包含休眠 (hibernating) 心肌，在心尖、側壁、心中膈與後壁，而前壁已經多是瘢痕組織。大部分是休眠心肌的且灌流不佳者，可以考慮 revascularization，像側壁；休眠混合瘢痕的再通血管的效果就比較差，像是下壁與心尖。至於 (B) 前壁多為瘢痕心肌，但灌流很好，應為題幹所敘述的先前冠狀動脈疾病導致，以及繞道手術 (CABG) 的結果，掃描顯示其繞道手術的血管仍通暢，應該不需要做血管再通治療

< 補充核醫影像 >
1. 影像切面：不論是 MPI 或是 FDG 都以 3 種切面（共 8 行）表示
a. Short axis view（上 4 行）：從心尖往上切到心底，可見甜甜圈樣的心室
b. Vertical-lateral axis view：垂直的從中膈往側壁切
c. Horizontal-anterior axis view：水平的從後壁往前壁切
2. 心肌灌注掃描 (Myocardial Perfusion Image, MPI)：透過 Tl-201 或 Tc-99m MIBI 觀察血流灌注至心肌的狀況。若有血管狹窄、阻塞，則心肌吸收核種的量就會降低
3. F-18 FDG 正電子攝影：FDG 為葡萄糖類似物，可以觀察心肌細胞的活性，藉以辨別心肌的存活狀況（另外，FDG PET 也常應用在腫瘤的分期或治療後評估）''',
        'image': '/explanations/cropped/111-2-醫學(三)-9_merged.png'
    },
    10: {
        'text': '''窄的 QRS (≤ 120 ms) → 源自 His bundle 以上；看到是 regular → 排除不規則的 atrial fibrillation (AF)、multifocal atrial tachycardia (MAT)。雖然有的時候 supraventricular origin 的也可能出現寬的 QRS，如：有 LBBB、RBBB、或 accessory pathway，不過本題心室頻脈是最不可能出現 regular narrow QRS tachycardia 的心律不整，故選 (D)''',
        'image': '/explanations/cropped/111-2-醫學(三)-10_merged.png'
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
