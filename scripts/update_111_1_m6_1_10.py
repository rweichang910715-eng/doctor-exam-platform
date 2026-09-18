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
# Q1: page 422 [1105:1310] + page 423 [140:390]
p422_q1 = read_img(422)[1105:1310, 40:930]
p423_q1 = read_img(423)[140:390, 40:930]
write_img('public/explanations/cropped/111-1-醫學(六)-1_merged.png', np.vstack([p422_q1, p423_q1]))

# Q2: page 421 [755:1270] + page 422 [140:740]
p421_q2 = read_img(421)[755:1270, 40:930]
p422_q2 = read_img(422)[140:740, 40:930]
write_img('public/explanations/cropped/111-1-醫學(六)-2_merged.png', np.vstack([p421_q2, p422_q2]))

# Q3: page 423 [805:1310] + page 424 [140:570]
p423_q3 = read_img(423)[805:1310, 40:930]
p424_q3 = read_img(424)[140:570, 40:930]
write_img('public/explanations/cropped/111-1-醫學(六)-3_merged.png', np.vstack([p423_q3, p424_q3]))

# Q4: page 424 [855:1310] + page 425 [140:740]
p424_q4 = read_img(424)[855:1310, 40:930]
p425_q4 = read_img(425)[140:740, 40:930]
write_img('public/explanations/cropped/111-1-醫學(六)-4_merged.png', np.vstack([p424_q4, p425_q4]))

# Q5: page 426 [330:1310] + page 427 [140:440]
p426_q5 = read_img(426)[330:1310, 40:930]
p427_q5 = read_img(427)[140:440, 40:930]
write_img('public/explanations/cropped/111-1-醫學(六)-5_merged.png', np.vstack([p426_q5, p427_q5]))

# Q6: page 425 [995:1260]
write_img('public/explanations/cropped/111-1-醫學(六)-6_merged.png', read_img(425)[995:1260, 40:930])

# Q7: page 427 [750:1270]
write_img('public/explanations/cropped/111-1-醫學(六)-7_merged.png', read_img(427)[750:1270, 40:930])

# Q8: page 428 [418:760]
write_img('public/explanations/cropped/111-1-醫學(六)-8_merged.png', read_img(428)[418:760, 40:930])

# Q9: page 428 [1140:1310] + page 429 [140:680]
p428_q9 = read_img(428)[1140:1310, 40:930]
p429_q9 = read_img(429)[140:680, 40:930]
write_img('public/explanations/cropped/111-1-醫學(六)-9_merged.png', np.vstack([p428_q9, p429_q9]))

# Q10: page 437 [755:1270]
write_img('public/explanations/cropped/111-1-醫學(六)-10_merged.png', read_img(437)[755:1270, 40:930])

print('Cropped images generated successfully')

EXPLANATIONS = {
    1: {
        'text': '''插管後確認位置，不只在刀房麻醉後，在病房、急診也是很重要的技能！
(A) 從邏輯上判斷即可得知是錯誤的。後頸部超音波僅能掃到皮下組織與脊椎韌帶，應以「前」頸部超音波較為合適

(B)、(C)、(D) 都是常用的方式，確認氣管內管位置有在呼吸道，而不是食道；以 (C) 為黃金診斷方式。另外 (B)(D) 也可以評估插管深度，避免單肺 (one-lung) 通氣。若不是在刀房，通常會在插管後申請一張胸腔 X 光看管尖位置，一般來說氣管內管在氣管分岔處 (carina) 上方約 2~3cm 為最適合的深度''',
        'image': '/explanations/cropped/111-1-醫學(六)-1_merged.png'
    },
    2: {
        'text': '''此題與【111-2(六)2】考點相同，出自 Miller's Anesthesia, 9/e Ch.36 的 Key Points

(A) Allen test 是確定手部尺動脈供應通暢，避免置入橈動脈動脈導管後造成問題，但並不能很好預測動脈導管後遺症發生（簡單來想，局部血腫、移位、感染其實與 Allen test 評估的沒什麼關係）。教科書說：相較於橈動脈或股動脈，置放導管於臂動脈較為安全
(B) 肺動脈導管監測（即 Swan-Ganz catheter）對於大多數重症病人並無存活的優勢，使用上並無那麼普及，通常僅用於開心手術、難治心衰竭與嚴重血液動力學不穩病人
(D) 臨床常使用 CVP（= 右心室末期舒張壓 RVEDP）作為評估右心 preload 的指標，但其實 pressure 與 volume 並沒有很明確的關聯，甚至在灌注 Normal saline 後也是

刪去後，故剩 (C) 為正確選項（直接貼自教科書）。以下簡單補充在 ICU 常用到的 Stroke Volume Variation (SVV) 動態測量：
• 在正壓呼吸下，SVV 的產生：
  - 吸氣時：肺泡微血管壓力 ↑ ⇒ 回左心血量 ↑ ⇒ 左心 SV ↑；而肺泡循環阻力 ↑ ⇒ 右心 SV ↓
  - 吐氣時：因吸氣時右心 SV ↓ ⇒ 左心回心血量 ↓ ↓ ⇒ 左心 SV ↓ ↓
  - 當血管內容積越低時，SV 變化狀況會更加明顯，SVV ↑
• 使用的前提：使用正壓呼吸器、竇性心律
• 計算：(SVmax - SVmin)/SV mean
• 數值評估
  - 基於 Frank-Starling Curve，為 Preload 與 SV 的關係圖
  - 簡單來說，當體液不足時，給予輸液後，SV 變化幅度較大；當體液充足或太多時，給予輸液後 SV 變化幅度較小 ⇒ 透過 SVV 間接判斷血管內水分含量
  - SVV<10-12% 表示有適當的 Preload（但實際臨床評估不能單看此數值！）''',
        'image': '/explanations/cropped/111-1-醫學(六)-2_merged.png'
    },
    3: {
        'text': '''(B) 麻醉前半小時先透過對流式的保溫毯 (convective forced-air warming blankets)，預熱病人，可以減少第 1 小時的體溫下降幅度，因為降低中央 - 周邊體溫差。故選項敘述「有效預防」為錯誤
(C) 小兒呼吸道體表面積較成人大，因此加溫加濕的氣體對於保溫效果應較成人高
(D) 區域麻醉可抑制血管壁肌肉收縮使血管舒張，造成周邊體溫下降，進而導致中心體溫降低（重新分布所致）

刪去後剩下 (A) 為正確敘述。以下補充關於麻醉中的體溫調節與監測：
• 原因：麻醉藥抑制下視丘的體溫調節反射，如：體溫太高時流汗、血管舒張；體溫太低時顫抖、血管收縮
• 麻醉後體溫變化：
  - Phase 1（麻醉後第 1 小時）：不論是全身、硬膜外或脊髓麻醉，會下降 1-2°C，主要因體溫重新分布所致（溫暖的中心體溫 vs. 冰冷的周邊體溫），可以透過麻醉前保溫毯預熱減少體溫下降
  - Phase 2（後續 3-4 hr）：體溫持續下降，主要是熱量散失於環境。刀房溫度太低、手術時間長、大範圍傷口皆為低溫症的風險因子。可以透過保溫毯、呼吸道保溫保濕、提高刀房溫度，減少熱量散失
  - Phase 3（平衡期）：體溫喪失與製造達到平衡
• 若術後低體溫 (BT< 36°C) 情況，給予體表加溫，如：保溫毯、烤燈''',
        'image': '/explanations/cropped/111-1-醫學(六)-3_merged.png'
    },
    4: {
        'text': '''此題考麻醉藥物的藥理學。(C) 不論是臨床使用或是動物實驗，常使用 epinephrine（一種 α agonist）造成局部血管「收縮」，使得局部麻醉劑不太被血流沖走，作用較局部，濃度也較高延長效果。以下簡單整理局部麻醉劑的特色：

藥物結構類似，以中央的官能基分成兩類：

| 特定官能基 | 醯胺類 (amides) | 酯類 (esters) |
| :--- | :--- | :--- |
| 特性 | 較少發生過敏、結構穩定，肝臟代謝緩慢 | 容易過敏、choline esterase 代謝快速 |
| 種類 | Lidocaine、Bupivacaine、Ropivacaine | Procaine、Benzocaine |

• MOA：與 Voltage-gated Na 離子通道結合，在 Open states 阻斷 Na 離子流入，進而提高產生動作電位所需的閾值
• 藥物動力學
  - 因為結合位置靠近細胞質側，因此脂溶性會增加局部麻醉劑效果
  - 本身為弱酸，在脫除 H⁺ 後可以穿過髓鞘達到作用
  - 阻斷神經衝動傳遞，隨著藥物作用依序阻斷：B fiber（交感）⇒ C fiber（溫痛覺）⇒ A fiber（觸 / 壓 / 本體感覺）
  ※ 註：越細的越容易被阻斷、有髓鞘的越容易阻斷（因主要阻斷蘭氏節）
  ※ C fiber 最細、A fiber 最粗；A、B fiber 有髓鞘
  - 影響藥物效果的因素：酸鹼值（環境太酸降低效果）、血液循環（血流豐富者降低效果）、給予途徑（IV ＞吸入＞硬膜外＞神經阻斷＞皮下）
• 毒性
  - 中樞：口腔金屬味、耳鳴、頭暈、噁心嘔吐、視幻覺
  - 心臟：心律不整、心肌抑制''',
        'image': '/explanations/cropped/111-1-醫學(六)-4_merged.png'
    },
    5: {
        'text': '''此題考術後噁心嘔吐 (Post-Operative Nausea/Vomiting, PONV)，是全身麻醉後最常見立即性的問題（約佔 30%），常使用的預防性藥物包含：

| 機制 | 種類 [成人劑量] | 備註 |
| :--- | :--- | :--- |
| 5-HT3 Antagonist | Ondansetron [4 mg]<br>Granisetron [0.01-0.04 mg/kg]<br>Dolasetron [12.5 mg] | 有很好的預防效果，作為治療則效果一般 |
| D2 Antagonist + 5-HT3 Antagonist | Metoclopramide [0.15 mg/kg] | 相對於 Setron 類藥物效果較弱，且有錐體外路徑副作用 |
| Anti-cholinergics | Scopolamine [Transdermal] | 效果不錯，但用在老人要小心副作用（口乾、尿液滯留、青光眼加劇等） |
| Steroid | Dexamethasone [4-10 mg, IV] | 麻醉前給予，除了止吐外，也有不等程度的止痛效果 |
| Neurokinin-1 Antagonist | Aprepitant(40 mg) | 在麻醉誘導前 3 小時給予 |

故 (A) 為可給予藥物之一
(B) 為 Cholinesterase Inhibitors，在麻醉上用於神經肌肉阻斷劑的拮抗劑
(C) Fentanyl 為類鴉片類藥物，為止痛劑，其副作用包含噁心嘔吐，應該不會拿來作為症狀預防
(D) Atracurium 為神經肌肉阻斷劑，主要用於輔助麻醉誘導，以及術中肌肉放鬆

以下補充術前預測 PONV 風險的量表——Apfel's simplified score：

| Risk factors | Point | Total |
| :--- | :--- | :--- |
| Post-operative opioid | 1 | 0~1 → 免給止吐藥物<br><br>2 → 給 1~2 種止吐藥物<br><br>3~4 → 給 3 種以上只吐藥物 |
| Non-smoker | 1 | |
| Female gender | 1 | |
| History of PONV/Motion sickness | 1 | |''',
        'image': '/explanations/cropped/111-1-醫學(六)-5_merged.png'
    },
    6: {
        'text': '''計算題。Doppler 超音波原理中，可以透過白努力定律 (Bernoulli equation)，以測得的流速推算兩個腔室間的壓力差，簡化後的公式為「Δp = 4v²」，其中 Δp= 壓力差，v = 流速 (m/s)。所以按照題目所給予 v = 3.5 m/s，放入計算後可得到 Δp = 49，故選 (D)''',
        'image': '/explanations/cropped/111-1-醫學(六)-6_merged.png'
    },
    7: {
        'text': '''從選項的敘述即可判斷。術後恢復的低血壓常常是低血容、左心室功能不佳或過量血管舒張劑導致，以低血容最常見（如：術中失血過多、引流液很多或輸液不足），故 (B) 敘述錯誤。另外 PACU 常見循環系統的問題也有高血壓、心律不整。術後的高血壓常常是傷口疼痛、拔管、膀胱鼓脹、術前停高血壓藥物所導致，也與低血氧、代謝酸中毒或腦壓過高有關；術後心律不整可能與呼吸或代謝性酸鹼不平衡、離子不平衡導致

(D) 部分抗生素與肌肉鬆弛劑的交互作用—加強 (potentiate) 效果，包含：Aminoglycoside 類（在神經肌肉間隙有類似 Mg 效果使肌肉放鬆）、Clindamycin（直接使肌肉舒張）、Tetracycline（會嵌合 Ca 導致放鬆）、Colistin、Metronidazole、Amphotericin B（誘發 Hypokalemia 加強肌肉鬆弛劑作用）

[ 參考 Morgan & Mikhail's Clinical Anesthesiology(7/e), Table 11-3]''',
        'image': '/explanations/cropped/111-1-醫學(六)-7_merged.png'
    },
    8: {
        'text': '''刪去法。(A) (C) (D) 皆在講同一件事情，透過硬膜外止痛，可以減少 Opioids 使用，進而減少 Opioids 相關的問題，如：腸胃道症狀（噁心、嘔吐或便秘）、呼吸抑制引發通氣不足 (hypoventilation)，或吸入性肺炎等。而 (B) 考用於硬膜外止痛的藥物【參考 111-1(六)4】，此類藥物優先阻斷交感傳出神經 (B fiber)，再來才是感覺神經 (C 與 A fiber)，有些藥物可能具部分運動阻斷的效果，因此「增加 sympathetic flow」及後續的敘述都是錯誤的''',
        'image': '/explanations/cropped/111-1-醫學(六)-8_merged.png'
    },
    9: {
        'text': '''首先要搞清楚題目詢問的是「呼吸道正壓治療 (positive "airway" pressure therapy)」，即我們常聽到使用侵入性呼吸器的 Positive End-Expiratory Pressure (PEEP) 或非侵入性氧療的 Continuous Positive Airway Pressure (CPAP)。PEEP 是在吐氣時氣流產生的壓力閥值，所以在吐氣結束後，仍維持一定氣道壓力使肺泡不會塌陷；而 CPAP 則是在自發性呼吸運動中都維持一定的壓力閥值，輔助吸氣與吐氣。這樣的方式可以增加功能性肺餘容積 (functional residual capacity, FRC) 以及改善肺部順應性 (compliance)，進而修正通氣能力以及氧氣交換能力。但過高的壓力值，可能會造成以下問題：
• 過度擴張肺泡 ⇒ 壓迫肺部微血管 ⇒ 肺血管阻力 ⇒ 右心 Afterload ↑
• 因微血管壓迫 ⇒ 增加有氣流但無血流的死腔 (deadspace)，因而通氣量減少
• 因微血管壓迫 ⇒ 左心回流降低，因而降低心輸出量
• 若壓力值 >20 cmH₂O，則會明顯增加 Barotrauma 的危險

故 (D) 選項描述錯誤，其餘皆為正確敘述''',
        'image': '/explanations/cropped/111-1-醫學(六)-9_merged.png'
    },
    10: {
        'text': '''(A) 雷射手術是改善視力，沒有矯正高度近視的根本原因，故黃斑部病變風險依舊存在
(B) 針對脈絡膜新生血管 (CNV) 的治療的首選，與老化相關黃斑部病變 (age-related macular degeneration, AMD) 一樣是 Anti-VEGF，只是施打的頻次沒有 AMD 高
(C) 所指應為「年輕病人因高度近視造成的 CNV，預後比 AMD 造成的 CNV 佳」
(D) 查詢 Kanski's 教科書，僅說明透過睡前 low dose atropine 滴劑可預防高度近視造成的黃斑部病變在兒童期的惡化，但並沒有明確說明葉黃素於脈絡膜血管新生併發症的預防。另外，葉黃素就目前研究上是建議使用 (10 mg/day)，但並沒有證實能夠預防年紀相關的眼睛疾病的發生 (age-related eye disease)

因此排除 (A) (B) (C) 正確選項後，此題答案應為 (D)''',
        'image': '/explanations/cropped/111-1-醫學(六)-10_merged.png'
    }
}

# 2. Update questions.json
with open('src/data/questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

updated_q = 0
for q in questions:
    qid = q.get('id', '')
    if '111-1' in qid and '醫學(六)' in qid:
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
    key = f'111-1-醫學(六)-{qnum}'
    exp_map[key] = {
        'text': item['text'],
        'image': item['image']
    }

with open('src/data/explanations_map.json', 'w', encoding='utf-8') as f:
    json.dump(exp_map, f, ensure_ascii=False, indent=2)

print('Updated explanations_map.json successfully')
