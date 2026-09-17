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
# Q51: page 187 [460:925]
write_img('public/explanations/cropped/111-1-醫學(五)-51_merged.png', read_img(187)[460:925, 40:930])

# Q52: page 191 [118:515]
write_img('public/explanations/cropped/111-1-醫學(五)-52_merged.png', read_img(191)[118:515, 40:930])

# Q53: page 190 [118:470]
write_img('public/explanations/cropped/111-1-醫學(五)-53_merged.png', read_img(190)[118:470, 40:930])

# Q54: page 191 [730:1310] + page 192 [145:490]
p191_q54 = read_img(191)[730:1310, 40:930]
p192_q54 = read_img(192)[145:490, 40:930]
write_img('public/explanations/cropped/111-1-醫學(五)-54_merged.png', np.vstack([p191_q54, p192_q54]))

# Q55: page 194 [265:650]
write_img('public/explanations/cropped/111-1-醫學(五)-55_merged.png', read_img(194)[265:650, 40:930])

# Q57: page 389 [730:1310] + page 390 [145:265]
p389_q57 = read_img(389)[730:1310, 40:930]
p390_q57 = read_img(390)[145:265, 40:930]
write_img('public/explanations/cropped/111-1-醫學(五)-57_merged.png', np.vstack([p389_q57, p390_q57]))

# Q58: page 390 [560:1310] + page 391 [130:940]
p390_q58 = read_img(390)[560:1310, 40:930]
p391_q58 = read_img(391)[130:940, 40:930]
write_img('public/explanations/cropped/111-1-醫學(五)-58_merged.png', np.vstack([p390_q58, p391_q58]))

# Q59: page 392 [410:620]
write_img('public/explanations/cropped/111-1-醫學(五)-59_merged.png', read_img(392)[410:620, 40:930])

# Q60: page 392 [760:1310] + page 393 [145:540]
p392_q60 = read_img(392)[760:1310, 40:930]
p393_q60 = read_img(393)[145:540, 40:930]
write_img('public/explanations/cropped/111-1-醫學(五)-60_merged.png', np.vstack([p392_q60, p393_q60]))

print("Cropped images generated successfully")

EXPLANATIONS = {
    51: {
        "text": """（111-2 第 47 題也是隱睪症的考題，可一同參閱）

(A) 由於未下降的睪丸在嬰兒出生 6 個月後就可能產生了組織及形態上的變化，在 2 歲時就可能產生 Leydig cell 萎縮、輸精小管半徑減少及精蟲生成受損的問題，故患有隱睪症的幼兒應盡快在 2 歲前進行睪丸固定術，以避免造成更多不可逆的影響

(B) 如觸診及超音波檢查均未發現睪丸，須先鑑別是否為縮睪（又稱回縮性睪丸 retractile testes）。縮睪為過度活躍的提睪肌反射所致，使得睪丸從陰囊往上移動到腹股溝；大多會在青春期消失，也可藉由手法將睪丸從腹股溝管復位至陰囊中；若無法復位，則有可能是隱睪症，須進行進一步檢查並手術

(C) 患有隱睪症者得到睪丸癌的機率會比一般人高，且做睪丸固定手術後無法降低睪丸癌發生的風險，但手術可幫助提早偵測疾病

(D) 進行手術前，睪丸及內部構造的組織及形態可能早已產生變化，故不孕機率會比正常男性高""",
        "image": "/explanations/cropped/111-1-醫學(五)-51_merged.png"
    },
    52: {
        "text": """(A) 微血管回填充時間 (capillary refill time) 可作為判定組織是否有充足灌流量的標誌，若時間超過 2 秒，則表示組織灌流量不足

(B) 嬰兒的終末支氣管及肺泡會持續發育到 6~8 歲；早產兒因肺部發育尚未完全、分泌表面活性劑 (surfactant) 的第二型肺細胞 (type II pneumocyte) 不足而使得肺泡更容易塌陷、接受呼吸器治療時易產生氣壓傷 (barotrauma)，但現已可在早產兒出生後為其補充肺部的表面活性劑，而增加新生兒的存活率

(C) 新生兒較大的單位體重表面積和水分無感流失 (insensible fluid losses) 為其低體溫最大的危險因子

(D) 當新生兒失溫時，身體會以非顫抖性生熱 (nonshivering thermogenesis)，也就是透過代謝及耗氧過程中所產生的熱（而非藉由身體發抖產生熱）使體溫恢復""",
        "image": "/explanations/cropped/111-1-醫學(五)-52_merged.png"
    },
    53: {
        "text": """先天性斜頸 (torticollis) 為單側胸鎖乳突肌纖維化所致，可看到幼兒的頭頸向患側傾斜使耳朵貼近肩膀而臉部轉向對側。約有 2/3 的病人可在患側頸部摸到腫塊（又稱為 wry neck），也可以藉由超音波進行診斷。若未及時治療，可能影響幼兒動作發展、造成頸部活動不良、產生代償性脊椎側彎等。大多患者可藉由適當的物理治療加速肌肉軟化而痊癒，最適當的物理治療時機為六個月大前，六個月大後肌肉緊縮不對稱就不容易恢復。若在 2 歲後還是有斜頸症狀，可能須胸鎖乳突肌肌腱切開術或胸鎖乳突肌肌腱延長手術才能解決斜頸問題

(B) 因頭「轉向」右邊，可知左邊為患側

(C) 小於 2 歲的先天性斜頸患者會以物理治療作為初步治療，待 2 歲大若尚有症狀才考慮手術

(D) 應為胸鎖乳突肌纖維化""",
        "image": "/explanations/cropped/111-1-醫學(五)-53_merged.png"
    },
    54: {
        "text": """（111-2 第 46 題也是先天性橫膈膜疝氣的考題，可一同參閱）
先天性橫膈膜疝氣 (congenital diaphragmatic hernia, CDH) 為肋膜腔與後腹腔未正常關閉而導致腹腔器官經由此缺口疝脫而出的先天性疾病，目前成因未明

(A) 在 S. Kotecha, A. Barbato, A. Bush, F. Claus, M. Davenport, C. Delacourt, J. Deprest, E. Eber, B. Frenckner, A. Greenough, A.G. Nicholson, J.L. Antón-Pacheco, F. Midulla. Congenital Diaphragmatic hernia. European Respiratory Journal, Apr 2012, 39(4), 820-829. 這篇文章中有提到，在有些規模較大的醫院統計出的先天性橫膈膜疝氣患者的預後約 60~70%，但由於各種研究的條件都不同而有不同 bias，故目前尚無法確定實際數據

(B) 出生後不需依靠 ECMO 者可在出生後不久盡快進行手術修復；但呼吸窘迫嚴重到需要依靠 ECMO 者進行手術修復的時機點仍有爭議，有些學者主張在 on ECMO 的情況下就可以盡快手術，有些則認為在 weaning ECMO 再進行手術

(C) 患有先天性橫膈膜疝氣之新生兒，出生後應立即插管以保護呼吸道；使用經面罩式陽壓呼吸會使空氣繼續灌入腸胃道而加重病情

(D) 在出生後放置胃管，可減少腸胃脹氣對肺部的壓力；若未進行減壓，會導致疝脫的腹腔器官加重對肺臟的壓迫，甚至造成縱膈腔偏移 (mediastinal shift)、影響呼吸功能""",
        "image": "/explanations/cropped/111-1-醫學(五)-54_merged.png"
    },
    55: {
        "text": """在這裡直接列出也算常考的腹裂 (gastroschisis) 與臍膨出 (omphalocele) 的比較：

| 評估項目 | 腹裂 (gastroschisis) | 臍膨出 (omphalocele) |
| :--- | :--- | :--- |
| 外觀 | 臍帶與正常肚臍相連，跑出的腸子通常從臍帶右側的腹壁缺口跑出，且因沒有膜覆蓋而泡在羊水中 | 臍帶與膨出的囊狀物相連，且若未破裂則膨出器官有腹膜及羊膜覆蓋而不會直接泡在羊水中；若破裂則難與腹裂鑑別 |
| 腹壁缺損 | 通常較小 (<4 cm) | 通常較大 (>4 cm) |
| 膨出器官 | 小腸為主 | 肝臟、小腸 |
| 合併異常 | 較少發生，但約有 10% 會合併小腸閉鎖 (intestinal atresia) | 較常發生（約 60~70%） |
| 相關疾病 | | • Beckwith-Wiedemann syndrome：臍膨出、巨舌、內臟腫大、低血糖 |""",
        "image": "/explanations/cropped/111-1-醫學(五)-55_merged.png"
    },
    56: {
        "text": "缺頁",
        "image": None
    },
    57: {
        "text": """(A) 骨盆穩定骨折指的是骨盆環 (pelvic ring) 僅有一處斷裂，且斷面可以接得起來；大多骨盆骨折屬於此類，且通常給予止痛藥、抗凝血藥、使用助行器等保守治療即可

(B) 可能伴隨骨盆骨折的神經損傷包括 L4~S5 神經根損傷，因此骨盆骨折病人也須留意其有無會陰部麻木感、大小便失禁、肛門張力下降等問題

(C) 骨盆骨折較可能造成骨盆腔或腹腔的腔室症候群

(D) 不穩定骨折指的是骨盆環上有多處斷裂，且骨頭發生位移 (displacement)；此類通常需外固定手術、骨骼牽引、開放性復位及內固定手術；手術過程中若傷及周圍神經，有可能出現下背痛的後遺症""",
        "image": "/explanations/cropped/111-1-醫學(五)-57_merged.png"
    },
    58: {
        "text": """(A) Lauge-Hansen 分類法將腳踝損傷根據損傷處及機制分為幾種：

| 類型 | 佔比 | Stage |
| :--- | :--- | :--- |
| Supination-External rotation, SER<br>(旋後 - 外旋型) | 40~75% | • Stage 1：ATFL（前距腓韌帶）撕裂<br>• Stage 2：腓骨遠端斜形或螺旋形骨折<br>• Stage 3：後踝撕脫或 PTFL（後距腓韌帶）撕裂<br>• Stage 4：內踝骨折或三角韌帶損傷 |
| Supination-Adduction, SAD<br>(旋後 - 內收型) | 10~20% | • Stage 1：腓骨遠端橫行骨折<br>• Stage 2：內踝骨折 |
| Pronation-Abduction, PAB<br>(旋前 - 外展型) | 5~20% | • Stage 1：內踝骨折或三角韌帶損傷<br>• Stage 2：ATFL 或 PTFL 撕裂<br>• Stage 3：踝關節以上的腓骨橫行或粉碎骨折 |
| Pronation-External rotation, PER<br>(旋前 - 外旋型) | 5~20% | • Stage 1：內踝骨折或三角韌帶損傷<br>• Stage 2：ATFL（前距腓韌帶）撕裂<br>• Stage 3：腓骨遠端斜形或螺旋形骨折<br>• Stage 4：後踝撕脫或 PTFL（後距腓韌帶）撕裂 |

(B) Schatzker 分類法將脛骨平台 (tibial plateau) 骨折分為以下幾類：

| 類型 | 描述 | 佔比 | 好發族群 / 機制 |
| :--- | :--- | :--- | :--- |
| Type I | 外側平台的楔形骨折 (wedge-typed fracture of lateral plateau)，通常被擠壓或錯位 <4mm | 6% | 年輕人 |
| Type II | 關節面被擠壓的楔形骨折 (wedge fractures associated with depression of articular surface) | 25% | 40 歲後（骨質開始缺乏） |
| Type III | 外側平台中央被擠壓 (pure central depression of lateral plateau) | 36% | 40~59 歲 |
| Type IV | 內側平台骨折 (medial plateau fracture) | 10% | 年輕人受高能量外傷，為預後最差的一類 |
| Type V | 內外踝骨折 (pure bicondylar fracture) | 3% | 與高能量外傷有關 |
| Type VI | 脛骨骨折伴隨骨骺與骨幹端的分離 (tibial fracture with dissociation of tibial metaphysis & diaphysis) | 20% | 膝蓋受高能量外傷所致 |

(C) 張力帶鋼絲術 (tension band wiring) 會將骨折處的牽引力或剪力轉換成擠壓力，以促進癒合

(D) 股骨頸骨折分類：

| Garden classification | Pauwels classification |
| :--- | :--- |
| • Type I：不完全骨折<br>• Type II：完全骨折，但沒有移位<br>• Type III：完全骨折，且部份移位<br>• Type IV：完全骨折，且完全移位<br>→根據骨折的嚴重程度及移位程度分類 | • Type I：Pauwels 角 <30°<br>• Type II：Pauwels 角 =30°~50°<br>• Type III：Pauwels 角 >50°<br>*Pauwels 角：髖關節正位相下，遠段骨折線與水平線間的夾角（但易因照相時下肢角度擺放位置不同及不同量測者間的誤差而有不同結果） |""",
        "image": "/explanations/cropped/111-1-醫學(五)-58_merged.png"
    },
    59: {
        "text": """當肱二頭肌長頭近端肌腱斷裂時，肱二頭肌會在上臂縮成一團球狀，形似卡通卜派的上臂形狀 (Popeye appearance of the arm)，故此類損傷又可稱為 Popeye deformity。肌腱斷裂時通常會有斷裂聲，並且病人會有上臂疼痛、肩肘無力、肩膀或手臂肌肉痙攣等症狀。通常可採取保守治療（如：冰敷、止痛藥、休息、物理治療）待肌腱自癒，但當保守治療無效、肩膀有其他傷、工作會有手臂反覆施力的動作等情況下，則可考慮手術""",
        "image": "/explanations/cropped/111-1-醫學(五)-59_merged.png"
    },
    60: {
        "text": """111-2 又考了一次相同的概念。新生兒大腿內側不對稱的皮膚皺摺可能是髖關節發育不良 (developmental dysplasia of hip, DDH) 的標誌，可在新生兒出生後藉由以下身體檢查及早發現（以下檢查建議觀看影片以更直觀地了解檢查內容）：
(1) Galeazzi sign：請病人平躺後屈膝，若兩側膝蓋不同高則為 positive，且膝蓋腳矮的一側為先天性髖關節脫臼 (hip dislocation) 側
(2) Barlow test：將新生兒的膝蓋和髖關節屈曲後，握著新生兒的膝蓋，將整個大腿前屈下壓，若新生兒有 DDH 則股骨頭會滑脫到髖關節以外
(3) Ortolani test：做完 Barlow test 後，再將新生兒的整個大腿往外往下壓，若新生兒有 DDH 則在做 Barlow test 時滑脫的股骨頭會滑回髖關節中

除了身體檢查外，也可搭配影像檢查，4~6 個月大前的嬰兒由於關節組織多為軟骨而適合以超音波評估髖關節的結構及穩定度（篩檢），4~6 個月大後以 X 光為主要的診斷工具（因有微量輻射故不適合用以篩檢）

(A) Patrick test：為檢查 hip lesion 的身體檢查；請患者平躺，將患者膝關節屈曲 90 度後，將髖關節外轉並外展至受測肢之外踝平置於對側肢的膝關節上，並將患側膝蓋下壓，若腹股溝處產生疼痛，則為 positive""",
        "image": "/explanations/cropped/111-1-醫學(五)-60_merged.png"
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

print(f"Updated explanations_map.json with Q51-Q60")
