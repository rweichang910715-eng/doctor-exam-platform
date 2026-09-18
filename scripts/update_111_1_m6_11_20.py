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
# Q11: page 438 [370:1295]
write_img('public/explanations/cropped/111-1-醫學(六)-11_merged.png', read_img(438)[370:1295, 40:930])

# Q12: page 439 [350:765]
write_img('public/explanations/cropped/111-1-醫學(六)-12_merged.png', read_img(439)[350:765, 40:930])

# Q13: page 439 [955:1310] + page 440 [140:265]
p439_q13 = read_img(439)[955:1310, 40:930]
p440_q13 = read_img(440)[140:265, 40:930]
write_img('public/explanations/cropped/111-1-醫學(六)-13_merged.png', np.vstack([p439_q13, p440_q13]))

# Q14: page 441 [520:1240]
write_img('public/explanations/cropped/111-1-醫學(六)-14_merged.png', read_img(441)[520:1240, 40:930])

# Q15: page 440 [485:1310] + page 441 [140:320]
p440_q15 = read_img(440)[485:1310, 40:930]
p441_q15 = read_img(441)[140:320, 40:930]
write_img('public/explanations/cropped/111-1-醫學(六)-15_merged.png', np.vstack([p440_q15, p441_q15]))

# Q16: page 442 [435:680]
write_img('public/explanations/cropped/111-1-醫學(六)-16_merged.png', read_img(442)[435:680, 40:930])

# Q17: page 442 [1035:1260]
write_img('public/explanations/cropped/111-1-醫學(六)-17_merged.png', read_img(442)[1035:1260, 40:930])

# Q18: page 443 [550:1200]
write_img('public/explanations/cropped/111-1-醫學(六)-18_merged.png', read_img(443)[550:1200, 40:930])

# Q19: page 453 [760:1310] + page 454 [140:320]
p453_q19 = read_img(453)[760:1310, 40:930]
p454_q19 = read_img(454)[140:320, 40:930]
write_img('public/explanations/cropped/111-1-醫學(六)-19_merged.png', np.vstack([p453_q19, p454_q19]))

# Q20: page 454 [730:1100]
write_img('public/explanations/cropped/111-1-醫學(六)-20_merged.png', read_img(454)[730:1100, 40:930])

print('Cropped images generated successfully')

EXPLANATIONS = {
    11: {
        'text': '''Ankylosis spondylitis 併發的為急性前葡萄膜炎，單眼發作居多且容易交替性復發，雙眼同時發作很罕見，故答案為 (D)。葡萄膜炎很難背，但也蠻愛考的，可依影響部位分成前、中、後、全葡萄膜炎，也有單眼或雙眼發作的臨床表現，整理如下：

| 葡萄膜炎分類 | 細項 | 臨床特點與相關疾病 |
| :--- | :--- | :--- |
| 全葡萄膜炎 | | 也就是可以以前、中、後葡萄膜炎發作，需要作為任何一種葡萄膜炎的鑑別診斷，大多以雙眼發作：<br>• 感染性肉芽腫：TB、梅毒、蟠尾絲蟲症 (onchocerciasis)、萊姆病 (Lyme disease)<br>• 自體免疫：交感性眼炎 (sympathetic ophthalmia)、貝西氏症 (Behçet disease)、原田氏症 (Vogt-Koyanagi-Harada disease)<br>• 類肉瘤病 (sarcoidosis)<br>• 腫瘤相關：視網膜母細胞瘤 (retinoblastoma)、淋巴癌 (lymphoma) |
| 前葡萄膜炎 | 急性 | 多為單眼發作，如：HSV/CMV/VZV 感染、僵直性脊椎炎 (AS)、反應性關節炎 (ReA) |
| 前葡萄膜炎 | 慢性 | • 多為雙眼發作，如：寡關節炎型的青少年特發性關節炎 (Oligoarticular JIA)、乾癬性關節炎 (PsA)、發炎性腸炎 (IBD)、腎小管間質腎炎伴葡萄膜炎 (TINU)<br>• 福斯氏異色虹膜葡萄膜炎 (Fuchs heterochromic iridocyclitis) 的臨床表現以單眼居多 (90-95%) |
| 中葡萄膜炎 | | 雙眼發作居多 (80%)，相關疾病包含：多發性硬化症 (multiple sclerosis)、Lyme disease、類肉瘤病 |
| 後葡萄膜炎 | | • 單眼發作：CMV/HSV/VZV 感染、弓漿蟲 (toxoplasmosis)<br>• 雙眼發作：原田氏症、貝西氏症、霰彈狀脈絡視網膜炎 (Birdshot chorioretinitis) |''',
        'image': '/explanations/cropped/111-1-醫學(六)-11_merged.png'
    },
    12: {
        'text': '''新生兒結膜炎 (neonatal conjunctivitis) 的定義為：出生後 30 天內發生的結膜發炎反應；故 (D) 錯誤。另外其發病時間也可輔助鑑別診斷，淋病新生兒眼炎約出生 2-3 天後，而披衣菌感染約出生 5-12 天後。以下簡單補充其他選項：
(A) 流行性角結膜炎 (epidemic keratoconjunctivitis, EKC) 與咽結膜熱 (pharyngoconjunctival fever, PCF) 皆常見於腺病毒感染，以濾泡性結膜炎 (follicular conjunctivitis) 表現為主
(B) 乳突 (papillae) 為血管纖維性增生，較常見於過敏性或細菌性結膜炎
(C) 濾泡 (follicles) 為淋巴組織增生，較常見於病毒或披衣菌感染''',
        'image': '/explanations/cropped/111-1-醫學(六)-12_merged.png'
    },
    13: {
        'text': '''眼球屈光主要來自於角膜、水晶體的貢獻，而屈光不正一般是指以下四種狀況：
• 近視 (myopia)：眼軸太長 / 屈光度過大，成像在視網膜前
• 遠視 (hyperopia)：眼軸太短 / 屈光度不足，成像在視網膜後
• 散光 (astigmatism)：角膜不規則導致屈光不平均，無法聚焦於一點
• 老花眼 (presbyopia)：睫狀肌調節水晶體能力下降，而影響視力

故 (A) (B) (D) 皆為屈光不正的範疇，而 (C) 斜視與屈光本身並沒有直接關聯，故為答案

[ 另類解題思考 ] 屈光不正一般可以用眼鏡來矯正，(A) (B) (D) 基本上是常常造訪眼鏡行的原因，而 (C) 斜視一般不會只造訪眼鏡行靠鏡片解決''',
        'image': '/explanations/cropped/111-1-醫學(六)-13_merged.png'
    },
    14: {
        'text': '''新生兒溢淚 (epiphora)、畏光 (photophobia) 為典型先天性青光眼常見的症狀，因此根據此推測，(C) 較不是此疾病常見的特徵之一。以下簡單補充先天性青光眼 (congenital glaucoma)：
• 病因

| 原發性先天性青光眼 | 因前房隅角發育異常 |
| :--- | :--- |
| 前側區發育異常 | 除前房發育異常外，常伴隨虹膜、角膜異常，如：Axenfeld-Rieger Syndrome、Peters anomaly |
| 其他症候群 | 無虹膜 (aniridia)、Sturge-Weber syndrome（容易長血管瘤）、Neurofibromatosis-1、先天德國麻疹感染 |

• 臨床表現
  - 約 80% 病例在一歲前會診斷出來
  - 最常見表現為溢淚 (epiphora)，伴隨畏光與角膜失光澤 (corneal luster)，若不治療會早期就失明
  - 表徵：眼壓增高、牛眼 (buphthalmos)、角膜橫徑擴大、角膜水腫''',
        'image': '/explanations/cropped/111-1-醫學(六)-14_merged.png'
    },
    15: {
        'text': '''這題有點在考英文。Phacomorphic glaucoma 因白內障造成水晶體變形，將虹膜往前房推擠，因而造成隅角閉鎖，影響眼房水液吸收，故 (C) 為正確答案。Phacogenic glaucoma 是疾病的統稱，這類疾病可分成兩類：隅角閉鎖性 (angle-closure) 與隅角開放性 (open-angle)。其中 (A) (D) 造成 open-angle，而 (C) 造成 angle-closure。以下簡單整理此類「水晶體異常導致的青光眼」疾病，統稱為 Phacogenic glaucoma：

| 隅角分類 | 疾病名稱與機轉 |
| :--- | :--- |
| 次發性隅角閉鎖性青光眼 | • phacomorphic glaucoma：白內障病程中，水晶體腫脹 (intumescence) 壓迫虹膜導致<br>• ectopia lentis：水晶體脫位 (dislocation)，可能因創傷或是其他系統疾病（如：Marfan's syndrome、Weill-Marchesani syndrome）有關 |
| 隅角開放性青光眼 | • phacolytic glaucoma：白內障水晶體內變質的蛋白滲漏出，造成發炎反應，影響小樑組織 (trabecular meshwork) 吸收<br>• lens-particle glaucoma：水晶體破裂、白內障手術後，晶體內蛋白釋出，阻塞小樑組織<br>• phacoantigenic（舊稱為 phacoanaphylactic）glaucoma：因創傷或手術後，造成系統性致敏化，使得免疫反應啟動造成發炎 |

[ 另類解題法 ] 隅角閉鎖性青光眼與水晶體異常的關聯性，應是被水晶體壓迫導致。而各選項從「醫學命名」去推測可能的機制：
(A) -lytic 是溶解的意思，因溶解物質塞住小樑組織而影響吸收，與壓迫較無相關
(C) -morphic 是型態的意思，因形狀變化（腫脹）造成壓迫，導致隅角閉鎖
(D) -anaphylactic 是過敏的意思，為免疫反應的發炎，因此也與壓迫較無相關''',
        'image': '/explanations/cropped/111-1-醫學(六)-15_merged.png'
    },
    16: {
        'text': '''斜視眼會因避免產生複視，而生理性被降低訊號，影響神經發育造成弱視。斜視手術僅矯正眼球方向，仍需要透過遮住好眼或散瞳劑降低好眼視覺，來訓練弱視眼的發育，故 (C) 選項錯誤''',
        'image': '/explanations/cropped/111-1-醫學(六)-16_merged.png'
    },
    17: {
        'text': '''海綿狀血管瘤為成人最常見的良性眼窩腫瘤，較常見於女性，且大多不會自行消解需要手術切除，故 (D) 選項不正確

考題愛比較的是 (A) 眼眶的微血管瘤，常見於兒童，會在出現後的第一年快速變大，再隨年紀增加而變小、消失''',
        'image': '/explanations/cropped/111-1-醫學(六)-17_merged.png'
    },
    18: {
        'text': '''肉毒桿菌『素』（題目直接打肉毒桿菌太恐怖了 ... 但就是打肉毒桿菌素的意思，基本上不影響作答 ...）本身作用機制為「在神經肌肉間隙，阻斷運動神經末梢釋放乙醯膽鹼 (acetylcholine)」達到肌肉放鬆的效果，故可以治療此題案例的狀況。而肉毒桿菌素針對眼瞼內翻 (entropion) 可以放鬆眼輪匝肌避免刺激角膜造成傷害，但僅有治標效果，長期而言仍須手術修正才有治本效果；而打了肉毒桿菌素容易因眼瞼鬆弛導致下眼瞼外翻、下垂的問題，並不是改善。故綜合起來 (D) 敘述不完全正確

以下簡單整理良性眼瞼痙攣 (benign essential blepharospasm)：
• 流行病學：女＞男，好發於 40 歲以上
• 原因：不明，可能與基底核有關
• 臨床表現：不自主的眨眼，眼輪匝肌 / 降眉間肌 (procerus muscle)/ 皺眉肌 (corrugator muscle) 痙攣，嚴重的可能影響日常生活
• 治療
  - 肉毒桿菌素注射為首選，每 3-4 個月打一次
  - 若注射後反應不佳的才考慮手術：肌肉切除、顏面神經燒灼''',
        'image': '/explanations/cropped/111-1-醫學(六)-18_merged.png'
    },
    19: {
        'text': '''圖片所示為左耳的耳鏡圖（因 light reflex 在圖的左下方，表示耳膜的前下象限），又從選項很明確得知是要考膽脂瘤，所以看圖找相對應的病灶。可以很明顯地在耳鏡圖的下方看到有表面光滑的黃色病灶，且位置在耳道中，並未影響到耳膜本身，因此以 (D) 選項為最適合的診斷。以下簡單補充膽脂瘤種類與各自常見位置：
• 先天性膽脂瘤：為發育時胚外層的遺留組織，組織學上與顱內表皮囊腫 (epidermoid cyst)，好發在顳骨巖部頂端、鼓膜前上象限區
• 後天性膽脂瘤
  - 原發性：與慢性感染、鼓膜破損無關
  - 繼發性：最常見的原因，與中耳慢性感染相關
  - 此類膽脂瘤自鼓膜開始生長，延伸進入中耳破壞中耳的構造
• 耳道膽脂瘤：很少見，長在外耳道中，其發生原因與手術、發炎、創傷或放射線暴露有關''',
        'image': '/explanations/cropped/111-1-醫學(六)-19_merged.png'
    },
    20: {
        'text': '''鼓室成型術 (tympanoplasty) 總共分成 5 種分型，可以用損壞的範圍來記。中耳由外而內構造包含：鼓膜、錘骨 (malleus)、砧骨 (incus)、鐙骨 (stapes)。因此手術分型為：

| 手術分型 | 侵犯/損壞範圍 | 重建/修復方式 |
| :--- | :--- | :--- |
| Type I | 侵犯鼓膜 | 修復鼓膜 (=Myringoplasty) |
| Type II | 侵犯 malleus | 鼓膜修復後，貼附到 incus 上 |
| Type III | 侵犯到 incus | 鼓膜修復後，貼到 stapes head 上 |
| Type IV | 侵犯到 stapes | 鼓膜修復後，貼到 stapes footplate 上 |
| Type V | | 鼓膜修復後，將其置於側向半規管上 |''',
        'image': '/explanations/cropped/111-1-醫學(六)-20_merged.png'
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
