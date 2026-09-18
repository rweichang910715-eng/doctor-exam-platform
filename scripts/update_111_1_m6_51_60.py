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
# Q51: page 296 [165:580]
write_img('public/explanations/cropped/111-1-醫學(六)-51_merged.png', read_img(296)[165:580, 40:930])

# Q52: page 294 [1055:1310] + page 295 [140:805]
p294_q52 = read_img(294)[1055:1310, 40:930]
p295_q52 = read_img(295)[140:805, 40:930]
write_img('public/explanations/cropped/111-1-醫學(六)-52_merged.png', np.vstack([p294_q52, p295_q52]))

# Q53: page 294 [320:635]
write_img('public/explanations/cropped/111-1-醫學(六)-53_merged.png', read_img(294)[320:635, 40:930])

# Q54: page 296 [970:1300]
write_img('public/explanations/cropped/111-1-醫學(六)-54_merged.png', read_img(296)[970:1300, 40:930])

# Q55: page 297 [415:865]
write_img('public/explanations/cropped/111-1-醫學(六)-55_merged.png', read_img(297)[415:865, 40:930])

# Q56: page 297 [1160:1310] + page 298 [140:495]
p297_q56 = read_img(297)[1160:1310, 40:930]
p298_q56 = read_img(298)[140:495, 40:930]
write_img('public/explanations/cropped/111-1-醫學(六)-56_merged.png', np.vstack([p297_q56, p298_q56]))

# Q57: page 299 [1025:1320]
write_img('public/explanations/cropped/111-1-醫學(六)-57_merged.png', read_img(299)[1025:1320, 40:930])

# Q58: page 469 [665:1080]
write_img('public/explanations/cropped/111-1-醫學(六)-58_merged.png', read_img(469)[665:1080, 40:930])

# Q59: page 470 [165:600]
write_img('public/explanations/cropped/111-1-醫學(六)-59_merged.png', read_img(470)[165:600, 40:930])

# Q60: page 470 [765:1080]
write_img('public/explanations/cropped/111-1-醫學(六)-60_merged.png', read_img(470)[765:1080, 40:930])

print('Cropped images generated successfully')

EXPLANATIONS = {
    51: {
        'text': '''此題就是翻譯教科書原文出題

(A) 懷孕併侵襲性子宮頸癌的發生率約「1.2/10,000」
(B) 第一妊娠期進行 Conization 後，流產率「高達 33%」，故一般在陰道鏡檢查符合侵襲癌的特徵 / 切片有微浸潤癌 / 細胞學檢查高度懷疑侵襲癌的孕婦，conization 不得早過第二孕期進行
(C) 在癌症侵犯深度 3-5 mm，但有淋巴血管侵犯的病人，得以「追蹤至胎兒足月或肺部成熟後進行分娩，合併修正式子宮全切除 (modified radical hysterectomy) 與骨盆腔淋巴切除 (pelvic lymphadenectomy)」，並不需要立即生產
故僅 (D) 是正確選項''',
        'image': '/explanations/cropped/111-1-醫學(六)-51_merged.png'
    },
    52: {
        'text': '''（暑考【111-2(六)53】也出了子宮內膜癌兩種 type 的比較！）

組織學型態 Non-endometrioid type 佔子宮內膜癌 10%，有較高的復發與遠端轉移的風險；又 Type I 組織學為 Endometrioid type，故 (D) 選項較適當敘述應為「Type II 預後較 Type I 子宮內膜癌差」，以下簡單補充 Type I 與 Type II 子宮內膜癌的特色：

| 比較特性 | Type I | Type II |
| :--- | :--- | :--- |
| 流行病學 | 較常見，發生於停經前（年紀較輕） | 發生於停經後（年紀較大） |
| 雌激素風險 | 非對抗性雌激素 (unopposed estrogen)#、肥胖 | 相關性較低 |
| 前驅病灶 | Endometrial hyperplasia ⇒ Atypical hyperplasia | Endometrial atrophy ⇒ Endometrial intraepithelial carcinoma |
| 病理型態原型 | Endometrioid | Serous |
| 其他病理型態 | Mucinous, Endometrioid with squamous differentiation | Clear cell（部分） |
| 腫瘤分級 | Low Grade | High Grade |
| 基因變異 | • PTEN 與 PIK3CA 突變<br>• 微衛星不穩定 (microsatellite instability)*<br>• KRAS 突變 | • P53 突變，佔此 type 約 90%<br>• 部分觀察到 HER-2/neu、CMYC 的過量表現 |

# 非對抗性雌激素：指使用 HRT 時，並未使用 Progestin 對抗雌激素在子宮內膜的作用
* 部分 Type I 的病理機制來自 microsatellite instability (MSI)，其中一群為遺傳性的 Lynch syndrome，其機制與相關癌症是醫學（三）腫瘤科、醫學（五）大腸直腸科考點！''',
        'image': '/explanations/cropped/111-1-醫學(六)-52_merged.png'
    },
    53: {
        'text': '''此題的 Choriocarcinoma 應該是考妊娠滋養體腫瘤，而非自卵巢長出的，最常見轉移的位置是肺 (80%)，其次為陰道 (30%)、骨盆腔 (20%)、肝臟 (10%) 與腦 (10%)，故答案選擇 (A)

[ 另類思考 ] 若是不確定最常轉移至哪，FIGO Stage 也有提供一點暗示，Stage III 明示其「侵犯肺臟」即屬之（不論有無生殖道侵犯），而「所有其他轉移位置」才是 Stage IV，可見肺轉移的重要性''',
        'image': '/explanations/cropped/111-1-醫學(六)-53_merged.png'
    },
    54: {
        'text': '''（暑考【111-2(六)54】也考了 ovarian reserve 的觀念！）

一般正常生理女性 25 歲時 AMH 約 3 ng/mL，35-37 歲者會降到約 1 ng/mL，因此通常評估時會納入年紀作考量，此外一般而言 <1.5 ng/mL 暗示低卵巢存量，故 (B) 選項不太正確

(A) 所述是 AMH 相較於其他卵巢功能評估的優點，因為其分泌不受月經影響，所以在月經任何一天抽血都可，其他 (C) (D) 的檢查則需要在月經第三天進行''',
        'image': '/explanations/cropped/111-1-醫學(六)-54_merged.png'
    },
    55: {
        'text': '''此題考生殖內分泌的生理學，外生殖器的預設發育是往女性表徵方向發育，男嬰因有雄性素刺激，因此發育成為男性表徵的性器，故原始答案為 (D)
(A) 根據「Two-cell-Two-gonadotropin theory」，由 LH 刺激 Theca cell 製造 testosterone 後，再由 FSH/LH 刺激 granulosa cell 將 testosterone 轉換成 estrogen
(B) 除了卵巢外，腎上腺也會產生雄性素

[ 爭議點 ] 依照 Berek & Novak's 教科書所述「停經後的卵巢仍繼續製造雄性素，因為停經並未影響到卵巢基質與囊鞘細胞 (theca cell)」，同時也說明「停經後女性的雄性素濃度比育齡女性低」，因此 (C) 描述為「雄性素維持不減」，並未說明是「製造」抑或是「濃度」，有爭議而給分''',
        'image': '/explanations/cropped/111-1-醫學(六)-55_merged.png'
    },
    56: {
        'text': '''(C) 所進行的是測量竇卵泡數目 (Antral Follicle Count, AFC)，可以了解卵巢功能，屬於不孕症評估的一環，並不能檢查排卵，以下簡單補充判斷排卵的方式：
• 紀錄基礎體溫 (basal body temperature, BBT)：排卵後因 Progesterone 分泌增加，體溫會略為增加 0.9-1.8 ℃
• 監測尿液 LH：用以監測 LH surge 發生，而排卵約在其之後 48 hr 內，最佳受孕時間為 LH surge 的前一天與當天
• 黃體中期（約為月經之前一週），血液 Progesterone 3 ng/mL 可確認已排卵，但數值低不代表沒排卵
• 陰道超音波檢查：監測 Dominant follicule 於排卵前後的變化，一般排卵前的濾泡約 17-19 mm，排卵後濾泡會變小，且可在 cul-de-sac 看到液體回音訊號

[ 另類思考 ] 依照生殖生理學，排卵時間在月經週期的第 14 天左右，所以 (C) 描述「第五天」有點怪怪的，應該不太適合判斷是否有排卵''',
        'image': '/explanations/cropped/111-1-醫學(六)-56_merged.png'
    },
    57: {
        'text': '''（寒考【111-2(六)57】一樣考尿失禁手術，可相互參照！）

TOT 與 TVT 皆屬於 Midurethral Slings 方式，將吊帶置於尿道中段，作為輔助性結構支持，答案為 (C)，根據 Petros and Ulmsten (1993 年) 的理論，正常支持性構造包含恥骨尿道韌帶 (pubourethral ligaments)、尿道下陰道吊床 (suburethral vaginal hammock) 與恥骨尾骨肌 (pubococcygeus muscle)，而吊帶手術是輔助這些支持性結構，改善尿失禁症狀''',
        'image': '/explanations/cropped/111-1-醫學(六)-57_merged.png'
    },
    58: {
        'text': '''題幹所述的為 Bobath 提出的 (B) 神經發展技術，此技術基於「自發性動作出自高階皮質中心，原始反射出自低階皮質中心」的想法，藉由矯正不正常的姿勢與動作，抑制其反射，並增加獨立的肌肉動作促進高階皮質功能，其餘也是中風復健的治療技術：
(A) 透過協調肌肉的攣縮狀況，將中風後分成不同 Brunnstrom Stage 觀察恢復情況
(C) 本體神經誘發術是兼具感覺刺激及運動訓練，並且強調統合與完整的復健計畫
(D) 為透過任務導向性的動作訓練，除了訓練肌力以外，也作為認知功能方面的復健''',
        'image': '/explanations/cropped/111-1-醫學(六)-58_merged.png'
    },
    59: {
        'text': '''這題有兩個關鍵字：
• 肱骨螺旋溝（spiral groove，題目打錯了），又稱 radial groove，上面走的神經是 radial nerve
• 手腕下垂 (dropped wrist) 無法背屈，指伸腕肌群（前臂背側區）無力；此處肌肉由 radial nerve 控制

故答案為 (B)，其餘選項神經運動支的控制：
(A) 尺神經：負責手掌屈肌群的尺側屈腕肌 (flexor carpi ulnaris) 與屈指伸肌 (flexor digitorum profundus)
(C) 正中神經：負責上述兩條肌肉以外的手掌屈肌群
(D) 肌皮神經：負責上臂屈肌的喙肱肌 (coracobrachialis)、肱二頭肌 (biceps brachii) 與肱肌 (brachialis)''',
        'image': '/explanations/cropped/111-1-醫學(六)-59_merged.png'
    },
    60: {
        'text': '''運動單元 (motor unit) 指單一條運動神經所支配的肌肉纖維群；越大肌肉就由越多的肌肉纖維組成，因此有更大的運動單元，附帶一提，當運動單元越大，此肌肉所能控制的動作就越粗糙，反之越小的運動單元較能控制肌肉進行精細動作，如：眼外肌群 (extraocular muscles)，這題理解「運動單元」的概念，就很好解題了，(B) 選項跟其餘三者比起來有最多的肌肉纖維組成，其運動單元應是最大的''',
        'image': '/explanations/cropped/111-1-醫學(六)-60_merged.png'
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
