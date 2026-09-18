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
# Q31: page 274 [165:1220]
write_img('public/explanations/cropped/111-1-醫學(六)-31_merged.png', read_img(274)[165:1220, 40:930])

# Q32: page 276 [865:1310] + page 277 [140:665]
p276_q32 = read_img(276)[865:1310, 40:930]
p277_q32 = read_img(277)[140:665, 40:930]
write_img('public/explanations/cropped/111-1-醫學(六)-32_merged.png', np.vstack([p276_q32, p277_q32]))

# Q33: page 277 [925:1310] + page 278 [140:695]
p277_q33 = read_img(277)[925:1310, 40:930]
p278_q33 = read_img(278)[140:695, 40:930]
write_img('public/explanations/cropped/111-1-醫學(六)-33_merged.png', np.vstack([p277_q33, p278_q33]))

# Q34: page 280 [165:900]
write_img('public/explanations/cropped/111-1-醫學(六)-34_merged.png', read_img(280)[165:900, 40:930])

# Q35: page 278 [1055:1310] + page 279 [140:930]
p278_q35 = read_img(278)[1055:1310, 40:930]
p279_q35 = read_img(279)[140:930, 40:930]
write_img('public/explanations/cropped/111-1-醫學(六)-35_merged.png', np.vstack([p278_q35, p279_q35]))

# Q36: page 280 [1165:1310] + page 281 [140:965]
p280_q36 = read_img(280)[1165:1310, 40:930]
p281_q36 = read_img(281)[140:965, 40:930]
write_img('public/explanations/cropped/111-1-醫學(六)-36_merged.png', np.vstack([p280_q36, p281_q36]))

# Q37: page 282 [165:1055]
write_img('public/explanations/cropped/111-1-醫學(六)-37_merged.png', read_img(282)[165:1055, 40:930])

# Q38: page 284 [165:980]
write_img('public/explanations/cropped/111-1-醫學(六)-38_merged.png', read_img(284)[165:980, 40:930])

# Q39: page 283 [165:995]
write_img('public/explanations/cropped/111-1-醫學(六)-39_merged.png', read_img(283)[165:995, 40:930])

# Q40: page 285 [165:720]
write_img('public/explanations/cropped/111-1-醫學(六)-40_merged.png', read_img(285)[165:720, 40:930])

print('Cropped images generated successfully')

EXPLANATIONS = {
    31: {
        'text': '''本題考「Biophysical Profile (BPP)」評估算分後的處置：

| 評估項目 *5 | 滿足條件者，2 分 | 0 分 |
| :--- | :--- | :--- |
| 羊水量 | 最深垂直深度 >2 cm | 不滿足條件者 |
| Non-stress Test | 20 分鐘內有 2 次心跳加速，上升 >15 bpm 持續 15 秒 | 不滿足條件者 |
| 胎兒肌張力 | 30 分鐘內，>1 次的上肢 / 脊椎由 extension 變成 flexion | 不滿足條件者 |
| 胎動 | 30 分鐘內，>3 次的肢體活動 | 不滿足條件者 |
| 胎兒呼吸 | 30 分鐘內，>1 次呼吸運動，持續 30 秒 | 不滿足條件者 |

| 算分數後的處置 | Normal | Equivocal | Abnormal |
| :--- | :--- | :--- | :--- |
| 羊水量正常 | 8-10 分 | 6 分 | 0-4 |
| 羊水量異常 | X | 8 分（單純羊水不足） | 6 |

• Normal：考慮規則進行 BPP 即可，約每週一次，因 BPP 對 72-96 hr 後寶寶的存活率有較高的陰性預測值
• Equivocal：若 GA>36 週則建議分娩；GA<36 週者，於 24 hr 後再做一次 BPP，若分數未進步則須考慮分娩
• Abnormal：考慮分娩

依照題幹敘述，BPP=10 分，所以觀察即可，選 (A) 最為合適

[ 胎兒評估的其他考點 ]
1. 胎兒臍動脈超音波判讀：舒張期血流停止 (AEDV)、舒張期逆流 (REDV)、收縮 / 舒張比率 (S/D ratio)
  • 出現 AEDV：34 週以上考慮生產
  • 出現 REDV：32 週以上考慮生產
  • S/D ratio>3（28 週後，此為懷孕不良預後的高風險族群）：每週追蹤臍動脈都卜勒超音波，若持續升高可評估 BPP
2. 連續性心率監測 (cardiotocography, CTG)：胎心音的速率、變異性，以及與宮縮的關係（加速 / 早期減速 / 晚期減速）''',
        'image': '/explanations/cropped/111-1-醫學(六)-31_merged.png'
    },
    32: {
        'text': '''背誦題，剖腹產的適應症分別會考慮母親、胎兒與胎盤臍帶：

| 分類 | 適應症內容 |
| :--- | :--- |
| 母親 | • 先前有子宮手術或前胎為剖腹產<br>• 產道阻塞，如：太大的疣 (condyloma)<br>• 生殖道有 active HSV/HIV infection（感染高風險）<br>• 產程遲滯 (labor dystocia)<br>• 子宮頸侵襲癌 |
| 胎兒 | • 胎心音監測下發現 Non-reassuring Fetal Status<br>• 胎位不正 (Malpresentation)<br>• 胎兒形狀異常，如：巨嬰 (>5000 kg)、水腦 (Hydrocephalus) 或其他先天畸形，經陰道會卡住 |
| 胎盤臍帶 | • 前置胎盤 (placenta previa)<br>• 植入性胎盤 (placenta accreta)<br>• 臍帶脫垂 (umbilical prolapse) 或前置臍帶 (vasa previa) |

小結：寶寶不對勁、媽媽不穩定、胎盤臍帶位置不太對，或曾經努力過但生不出來；但要知道有些 C/S 適應症並不是「絕對」的

所以依照上述，(A)、(B)、(D) 皆為適應症，(C) 不是
(A) 要趕快拉出寶寶，經陰道產太慢，所以須考慮
(B) 都已經生不出來了，再卡下去寶寶就會窘迫給你看，當然要考慮
(C) GBS(+) 只告訴我們寶寶出來時要小心新生兒感染甚至敗血症 (Neonatal sepsis)，可在產前給予預防性抗生素避免嚴重感染，並非不適合經陰道生產（※ 補：陰道 HPV 感染的母親也不是 C/S 的適應症，因為這樣感染的機會不高）
(D) 若經陰道，胎盤馬上拖出來直接大出血，非常不適合，所以須考慮（※ 註：類似道理，第三孕期出血的孕婦，在排除前置胎盤前，也不可以逕自地做指診！）''',
        'image': '/explanations/cropped/111-1-醫學(六)-32_merged.png'
    },
    33: {
        'text': '''這題直接考定義，無法用邏輯判斷，以下附上 2017 年 ACOG Practice Bulletin 的內文：Postpartum hemorrhage as cumulative blood loss greater than or equal to 1,000 mL or blood loss accompanied by signs or symptoms of hypovolemia within 24 hours after the birth process (includes intrapartum loss) regardless of route of delivery. 產後出血定義為不論生產的方式，在生產結束 24 小時內（包含生產時出血量），累計失血量 ≥ 1000 mL 或失血伴隨低血容的症狀與徵候），故 (B) 為答案
(A) 經陰道產者出血量 >500 mL 為舊的 PPH 定義，但 2017 這篇文章有提示，這類病人雖不包含於新的定義中，仍屬於異常的需要密切注意
(C) 舊時也定義 Hematocrit 下降 >10% 時可做為替代性的指標；但新的考量抽血評估容易延遲發現，因此也從定義中移除
(D) 雖然新的定義有說「伴隨低血容症狀與徵候」，但失血量需到一定程度（約 25% 血量，1500 mL），才會開始心跳加速 (tachycardia) 或血壓下降 (hypotension)；因此選擇 (B) 應更為合適

[ 產後大出血的其他考點 ]
1. 風險因子 (111-1(六)34)
2. 鑑別診斷 The 4 Ts：Tone、Trauma、Tissue、Thrombin
   ⇒ 其中以 uterine atony 最為常見 (70-80%)
3. 後續處置：子宮無力（子宮按摩 / 藥物）、子宮撕裂傷 / 破裂（手術）、殘餘胎盤組織（超音波評估 / 刮除）、凝血異常（矯正血小板 / 凝血因子）''',
        'image': '/explanations/cropped/111-1-醫學(六)-33_merged.png'
    },
    34: {
        'text': '''承 111-1(六)33，同一篇 2017 ACOG Practice Bulletin 也有整理關於 PPH 的風險因子（改寫＋翻譯自該篇 Table 1）：

| 4T 原因 | 鑑別診斷 | 風險因子 |
| :--- | :--- | :--- |
| Tone | 子宮無力 (Uterine Atony) | Oxytocin 用太久、產程遲滯、高產次 (high parity)、絨毛膜炎、全身麻醉 |
| Tone | 子宮過度擴張 (uterine overdistention) | 多胞胎、羊水過多、巨嬰 |
| Tone | 子宮纖維瘤 (fibrioid uterus=子宮肌瘤) | 長很多顆，影響收縮 |
| Trauma | 會陰切開術 (Episiotomy) | 未良好止血 |
| Trauma | 子宮破裂或其他生殖道撕裂傷 | 緊急生產 (precipitous delivery) |
| Tissue | 殘餘胎盤組織 (retained placenta)、植入性胎盤 (placenta accreta) | 副胎盤 (placenta succenturiate)、之前子宮手術病史 |
| Thrombin | 凝血功能異常 (coagulopathy) | 嚴重子癇前症、HELLP 症候群、胎盤早期剝離、敗血症 |

故 (A)、(B)、(D) 皆為子宮相關的 PPH 風險因子之一；而子宮畸形並不在其中

[ 其他考點 ] 子宮畸形可能造成不孕，特別是：子宮中膈 (uterine septum)''',
        'image': '/explanations/cropped/111-1-醫學(六)-34_merged.png'
    },
    35: {
        'text': '''此題考絨毛膜取樣 (chorionic villus sampling, CVS) 的適應症、進行方式與風險

以下整理兩種診斷性的基因檢測：
• 適應症：超音波檢查異常、家族有已知的遺傳疾病、唐氏症篩檢風險 >1/270 時
• 主要有兩種方式

| 方法 | 絨毛膜取樣 CVS | 羊膜穿刺 Amniocentesis |
| :--- | :--- | :--- |
| 施行時機 | GA 10-13 週 | GA 15-20 週，但在此時期之後仍可執行 |
| 抽吸方式 | 經腹部 (transabdominal) 或經子宮頸 (transcervical) | 經腹部，以 22G 腰椎穿刺針抽吸 |
| 取的組織 | 胎盤絨毛 | 羊水 |
| 優點 | 比羊膜穿刺更早得到診斷，特別是本來就懷疑有遺傳異常者 | 除了基因檢測外，也進行先天感染、Anti-D 的檢測 |
| 風險 | 陰道出血，而感染或羊水滲漏很少見<br>經腹部 / 子宮頸抽吸的風險沒有差別<br>肢體發育不良 | 陰道出血、羊水滲漏 |
| 流產 (C) | 約 0.22%（逐年下降） | 約 0.1-0.3%（逐年下降） |

• 相關檢測：染色體核型分析 (karyotype)、染色體微序列分析 (Chromosome Microarray Analysis)
• 若本身是進行人工生殖的夫妻，在胚胎植入前也會先進行診斷性的檢驗

(D) 研究發現，CVS 有肢體發育不良 (limb-reduction defects) 的風險，特別是在 GA <10 週進行，GA >10 週後取樣的風險並不會高於一般受孕族群；所以後段所述不正確''',
        'image': '/explanations/cropped/111-1-醫學(六)-35_merged.png'
    },
    36: {
        'text': '''此題考生產時的胎位相關知識：
• 臀位 (Breech)：胎兒臀部或腿側靠近骨盆口，寶寶在足月前大多是這種姿態，但僅佔足月單胞胎妊娠 (singleton delivery) 的 2-5%
• 按照寶寶的狀態可分成 Frank、Complete、Incomplete
  - Frank（高難度瑜珈動作）：髖關節 flexion ＋膝關節 extension，臉靠近腿
  - Complete：髖關節 Flexion ＋膝關節（至少一隻）Flexion
  - Incomplete：至少一側髖關節 Extension ⇒ 生產時腿先出
• 風險因子：羊水量異常、胎兒畸形、子宮結構異常、前置胎盤、初產婦 (nulliparity)、高齡產婦、先前有臀位產過、Small for Gestational Age (SGA)
• 生產方式選擇
  - 原則上可以經陰道產最佳，而 Frank breech 是最適合者
  - 偏好剖腹產者：胎兒太大 (>3800 g)、嚴重發育受限 (<2500 g)、羊水太少 (oligohydramnios)、Incomplete breech、前一胎是剖腹產

(D) 若前胎剖腹產，會偏好此胎臀位也剖腹產，但並非絕對不能經陰道產，前一胎剖腹產者，在下一胎可以進行 Trial of Labor After Caesarean Section (TOLAC)，嘗試進行陰道分娩 (vaginal birth after cesarean, VBAC)，而指引建議 TOLAC 在具有能力進行急救與緊急剖腹的醫療單位進行，這項試驗是在挑戰過往一直有的觀念「Once a cesarean, always a cesarean.(Cragin, 1916)」，但仍存在著爭議（因為統計看來併發症風險比反覆剖腹產者高），且也並不是適用於所有族群

※ 有興趣可以查查關於剖腹產的 TOLAC 與 ERCD''',
        'image': '/explanations/cropped/111-1-醫學(六)-36_merged.png'
    },
    37: {
        'text': '''其實單看題幹本身不知道在講什麼，不過理解 HAPO Study 的研究方法就知道，題目只是要考你知道不知道妊娠高血糖對於周產期的影響有哪些而已（所以就算不知道 HAPO Study 還是可以靠僅有的知識答題！），關於 HAPO Study：
• 目的：評估第三孕期母親血糖耐受值與周產期不良事件的關聯性
• 方法：血糖數值分成七類群，與周產期不良事件指標的比率做關聯性分析
• 周產期不良事件：出生體重 >90th 百分位、剖腹生產、新生兒低血糖與臍帶血 C-peptide 數值 >90th 百分位

(A) 妊娠高血糖孕婦產下的寶寶大多會是 Large for Gestational Age (LGA)
(B) 因為常常胎兒太大（ACOG 建議 >4500 gm 時），因擔心肩難產而考慮剖腹生產
(C) (D) 因為長期處在母親提供的高糖環境，胎兒自己的胰島素產量會很高，所以臨床表現以「新生兒低血糖 (neonatal hypoglycemia)」為主，且 C-peptide 數值很高（表示自產胰島素很多）

[ 妊娠高血糖的其他考點 ]
• 篩檢時機：GA 24-28 週
• 篩檢方式：75-g 口服糖水 (1 step)、50-g/100-g 口服糖水 (2 steps)
  ※ 目前 ADA 支持以 1 step 為主要篩檢（同一般人）；但 ACOG 仍有建議 2-steps
• 治療：飲食生活調整、藥物（胰島素或是 Metformin）
• 可能的胎兒併發症：巨嬰、新生兒低血糖''',
        'image': '/explanations/cropped/111-1-醫學(六)-37_merged.png'
    },
    38: {
        'text': '''考關於硫酸鎂的藥物特性，以下整理硫酸鎂針對 Preeclampsia with severe feature 的使用：
• 藥物動力學：Mg²⁺（離子）由腎臟排出，與肝臟代謝 / 膽汁排出無關
  ⇒ 因此腎功能不佳者要小心
• 針對 Preeclampsia with severe features 的病人，以 MgSO₄ 作為癲癇預防用藥
  - Loading dose：IV 注射 4~6 g over 15-20 minutes
  - Maintenance：IV 給予 2 g/hr
  - 若尿量減少、腎功能下降、Creatinine 上升，需調降劑量
  - 一般會持續給藥到產後 24 hr 再停藥
• 濃度監測

| 濃度 | 臨床表現 / 意義 |
| :--- | :--- |
| 4-6 mEq/L | 治療劑量 (therapeutic range) |
| 8-10 mEq/L | 喪失 deep tendon reflex |
| 12 mEq/L | 呼吸抑制 |
| >12 mEq/L | ECG 變化 ⇒ 意識改變 |

• 中毒時：停藥、給 Calcium gluconate，並可考慮給予利尿劑

(A)(B) 就題目而言，足夠尿量 (50 c.c./hr) 以及正常的腎功能，不必調整 MgSO₄ 劑量
(D) 要到心臟毒性（應該是只造成 ECG 變化），需要 >12 mEq/L，並非治療劑量''',
        'image': '/explanations/cropped/111-1-醫學(六)-38_merged.png'
    },
    39: {
        'text': '''考 TTTS 的病理機制，所以若沒細究過可能只能用猜的（見後面 [ 另類解題方式 ]），關於 TTTS 整理於下：
• 發生於單一絨毛膜 (monochorionic) 或是雙絨毛膜但胎盤融合的雙胞胎
• 因動靜脈吻合，導致 recipient twin 灌流過多 (hyperperfusion)、donor twin 灌流過少 (hypoperfusion)，造成不一致發育 (growth discordance)
• Donor Twin：脫水 ⇒ 無尿 ⇒ 羊水稀少 / 無羊水
• Recipient Twin：水腫 ⇒ 尿量多 ⇒ 羊水過多
• 處置主要減少羊水差異造成的後續問題：血管吻合雷射電燒、序列羊水抽吸 (sequential reduction amniocentesis)、羊水中膈造口術 (amniotic septostomy)

在單絨毛膜的胎盤上，以 A-A anastomosis 為最常見的血管畸形，V-V anastomosis 最少見；而 A-V anastomosis 才是造成 TTTS 主因，故選擇 (D)

(A) 帆狀臍帶插入 (velamentous cord insertion)：指臍帶插入胎兒膜上就分支，而呈現帆狀的膜，正常臍帶應在插入胎盤後才分支，這些血管因缺乏臍帶外圍 Wharton's jelly 與結締組織保護，很容易受傷出血、壓扁、栓塞

[ 另類解題方式 ] 若單純從胎兒血液循環角度思考，A 胎兒的血流流出（靜脈）後，被 B 胎兒的掠奪回體內（動脈），所以選擇 (D) 選項較符合病生理機轉''',
        'image': '/explanations/cropped/111-1-醫學(六)-39_merged.png'
    },
    40: {
        'text': '''腹腔鏡手術灌氣後造成的腹內壓力，與血糖的調控並無直接關聯，故 (D) 高血糖應為最適合的答案，腹腔鏡手術可能的併發症：
• 因需要是頭高腳低的姿勢（如：Trendelenburg position），加上麻醉藥的作用使肌肉放鬆，容易造成胃內容物逆流，因而增加吸入 (aspiration)、肺炎的風險（所以術前禁食很重要啊！）
• 因需要灌氣體（通常是 CO₂）創造氣腹 (pneumoperitoneum) 以利手術或診斷進行，若腹內壓力過高，會造成 hypoventilation（因壓迫胸腔）、hypercapnia（因 CO₂ 進入血液）、hypotension（因腹內壓壓迫周邊或內臟靜脈），進而造成 respiratory acidosis、cardiac arrhythmia，或是循環不良導致休克
• CO₂ 最常被使用的原因是其溶解度大容易吸收，但若大量的 CO₂ 直接進入中心靜脈，或腹內壓力過高，仍是會發生氣體栓塞 (air emboli)''',
        'image': '/explanations/cropped/111-1-醫學(六)-40_merged.png'
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
