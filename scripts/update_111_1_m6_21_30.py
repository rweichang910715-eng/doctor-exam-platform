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
# Q21: page 455 [125:500]
write_img('public/explanations/cropped/111-1-醫學(六)-21_merged.png', read_img(455)[125:500, 40:930])

# Q22: page 455 [1005:1310] + page 456 [140:245]
p455_q22 = read_img(455)[1005:1310, 40:930]
p456_q22 = read_img(456)[140:245, 40:930]
write_img('public/explanations/cropped/111-1-醫學(六)-22_merged.png', np.vstack([p455_q22, p456_q22]))

# Q23: page 457 [500:660]
write_img('public/explanations/cropped/111-1-醫學(六)-23_merged.png', read_img(457)[500:660, 40:930])

# Q24: page 456 [890:1310] + page 457 [140:215]
p456_q24 = read_img(456)[890:1310, 40:930]
p457_q24 = read_img(457)[140:215, 40:930]
write_img('public/explanations/cropped/111-1-醫學(六)-24_merged.png', np.vstack([p456_q24, p457_q24]))

# Q25: page 458 [115:545]
write_img('public/explanations/cropped/111-1-醫學(六)-25_merged.png', read_img(458)[115:545, 40:930])

# Q26: page 458 [1050:1280]
write_img('public/explanations/cropped/111-1-醫學(六)-26_merged.png', read_img(458)[1050:1280, 40:930])

# Q27: page 459 [335:1310] + page 460 [140:365]
p459_q27 = read_img(459)[335:1310, 40:930]
p460_q27 = read_img(460)[140:365, 40:930]
write_img('public/explanations/cropped/111-1-醫學(六)-27_merged.png', np.vstack([p459_q27, p460_q27]))

# Q28: page 272 [490:1310] + page 273 [140:595]
p272_q28 = read_img(272)[490:1310, 40:930]
p273_q28 = read_img(273)[140:595, 40:930]
write_img('public/explanations/cropped/111-1-醫學(六)-28_merged.png', np.vstack([p272_q28, p273_q28]))

# Q29: page 271 [460:895]
write_img('public/explanations/cropped/111-1-醫學(六)-29_merged.png', read_img(271)[460:895, 40:930])

# Q30: page 275 [650:1310] + page 276 [140:505]
p275_q30 = read_img(275)[650:1310, 40:930]
p276_q30 = read_img(276)[140:505, 40:930]
write_img('public/explanations/cropped/111-1-醫學(六)-30_merged.png', np.vstack([p275_q30, p276_q30]))

print('Cropped images generated successfully')

EXPLANATIONS = {
    21: {
        'text': '''噪音引發的永久性聽力損失 (Noise-induced Permanent Threshold Shift, NIPTS) 在噪音暴露早期影響 3~6 kHz 段最明顯，故選擇 (C)。以下簡單補充噪音引發聽損的病理機制：
• 暫時性聽力閥值變化 (temporary threshold shift, TTS)
  - 在暴露到音量大的噪音時，會產生暫時性的聽力喪失，並且會在 24 小時內完全恢復
  - 通常越高的頻率越敏感，也越容易受損
• 噪音引發永久性聽損 (NIPTS)
  - 長期噪音暴露，導致聽力並未能恢復
  - 初期聽損明顯的頻率段為 3~6 kHz，可能原因包含：人對高頻聲最敏感、保護性反射（即 acoustic reflex）僅針對 <2 kHz 聲音、耳蝸底部的外毛細胞對氧化壓力敏感
  - 隨著暴露繼續，其受損頻率範圍會往低頻處擴展；但若早期就停止噪音暴露，則聽損不太會繼續惡化''',
        'image': '/explanations/cropped/111-1-醫學(六)-21_merged.png'
    },
    22: {
        'text': '''Nasometry（鼻音測量）主要是用來間接評估顎咽閉合不全 (velopharyngeal insufficiency) 或是顎裂的病童，相對於侵入性的鼻內視鏡直接觀察軟顎與咽部在說話 / 唱歌時閉合情況，Nasometry 為非侵入性的，在說話 / 唱歌時接收鼻腔與口腔的壓力與氣流後，以此評估顎咽閉合狀況。以下為關於 Nasometry 的補充，其測量主要分成兩部分：
• 當受試者發母音時，可以藉此評估鼻腔共鳴 (nasalance)
• 當受試者發子音時，可以藉此評估異常的氣流自鼻洩出 (nasal emission)，暗示上顎裂或有顎咽閉合不全的問題

(A) acoustic rhinometry（聲反射鼻量計）：透過反射聲波測量鼻腔橫截面面積及鼻道容積
(B) rhinomanometry（鼻阻壓檢查）：測量吸氣及呼氣時，鼻子前端和後端的壓力差和氣流差，進而得鼻阻力＝壓力差 / 氣流差
(C) nasal peak flowmetry：評估最大吸氣量下鼻腔的氣流量''',
        'image': '/explanations/cropped/111-1-醫學(六)-22_merged.png'
    },
    23: {
        'text': '''原始答案為 (D)。急性化膿性中耳炎常見菌包含 S. pneumonia、H influenza、Moraxella catarrhalis，而 S. aureus 被列在不常培養出的細菌之中；而急性細菌性鼻竇炎常次發於急性病毒性鼻炎，教科書提及常見的菌種包含 S. penumoniae (20-43%)、H. influenza (22-35%)、M. catarrhalis (2-6%) 與厭氧菌 (<5%)，但 S. aureus 的比例並未多做說明。筆者覺得送分原因可能是 S. aureus 在急性鼻竇炎中並未明確說明其常見程度，又從文獻上搜尋仍處於未定論狀態，有的文章表示是 major pathogen，有的文章表示其培養出來量與健康人常在菌量無異，所以可能是 (D) 送分的原因''',
        'image': '/explanations/cropped/111-1-醫學(六)-23_merged.png'
    },
    24: {
        'text': '''看完題目敘述大致可以得到答案，關鍵字像是「糖尿病」暗示病人免疫力較差、「吸入式類固醇」說明口腔黏膜等處於免疫抑制的狀態，又見「瀰漫性喉部點狀白色病灶」，可以推斷最可能診斷為伺機性的 (D) 念珠菌感染。以下補充其他選項：
(A) 白斑 (leukoplakia)：為異常的上皮細胞增生與變異，好發位置在舌側與口腔壁，與鱗狀上皮癌相關。（此題從病史提供的資訊並不是很像此病灶的臨床特色）
(B) 乳突瘤病 (papillomatosis)：典型為外生型 (exophytic) 的病灶，與免疫缺陷、HPV 感染相關
(C) 白喉 (diphtheria)，為一種「急性」的上呼吸道感染症，除了喉嚨痛外，常會有淋巴結腫大，比較多發生於嬰兒童族群，並在口腔、喉部黏膜形成大片白色偽膜 (pseudomembrane)''',
        'image': '/explanations/cropped/111-1-醫學(六)-24_merged.png'
    },
    25: {
        'text': '''此題頗困難，一次考了四張圖。(B) 為聲帶息肉 (vocal polyp)：單側 / 雙側病灶，典型為外生型 (exophytic) 的乾淨病灶，有時可能有局部出血呈現紅色（如圖），為 hemorrhagic polyp。其餘圖片診斷如下：
• 圖一：應為聲帶結節 (vocal nodule)：主要長在聲帶中段、對稱性的雙側病灶
• 圖三：可能是聲帶囊腫 (vocal cyst)：為單側 / 雙側的病灶，長在聲帶表皮下區域或是靠近韌帶區
• 圖四：是聲帶肉芽腫 (vocal fold granuloma)：為一種慢性發炎導致的疾病，主要長在聲帶突 (vocal process)、靠近勺狀軟骨 (arytenoid cartilage) 處，可能與插管有關
(A) 聲帶白斑 (leukoplakia)：為白色斑點狀的病灶，零星分布在單側或雙側聲帶上
(D) 聲帶水腫 (Reinke edema)：雙側 / 單側，在聲帶表皮下區域產生膠狀的滲出液沉積。此狀況與喉咽逆流疾病 (laryngopharyngeal reflux disease)、vocal abuse、抽菸相關''',
        'image': '/explanations/cropped/111-1-醫學(六)-25_merged.png'
    },
    26: {
        'text': '''鼻咽癌 Stage II 病人通常是有淋巴轉移 (N1) 或是沒有淋巴轉移的 T2，就目前臨床研究證據以及 NCCN 指引，適用的治療是同步化放療 (concurrent systemic therapy)

至於 (C) 與 (D) 選項提及的其餘化療時機，通常是 Stage II 有 High-risk feature（腫瘤很大 / EBV DNA 量很高），或者是 T3-4、N1-3 時的狀況會考慮''',
        'image': '/explanations/cropped/111-1-醫學(六)-26_merged.png'
    },
    27: {
        'text': '''咽後淋巴結的引流區域包含鼻咽、耳咽管、軟顎、副鼻竇、中耳與咽部，因此 (A)、(C)、(D) 皆可能轉移至此。而舌頭（即口腔內）主要優先引流的淋巴結為 Level IA 的頷下淋巴結 (submental lymph node) 或 Level IB 的頜下淋巴結 (submandibular lymph node)，後續匯流至 Level IIA 的 Upper Jugular lymph node，再經 Level III 與 Level IV，不太會跑到咽後淋巴結，故 (B) 為最適合的答案。以下簡單補充頸部淋巴結分類與引流：

| Neck Level | LN group | 自____引流 | 流出往____ |
| :--- | :--- | :--- | :--- |
| Level IA | Submental | 臉頰、下唇、舌尖、口腔底 | Level IB, II, III |
| Level IB | Submandibular | 鼻、臉頰、前鼻腔、下唇、口腔、頜下腺 | Level II, III |
| Level IIA, IIB | Upper jugular chain | 耳廓、下頜骨角、口腔、鼻腔、鼻/口/下咽、腮腺、後咽 LN、枕後 LN | Level III~V |
| Level III | Middle jugular chain | 口腔、Level IA/IB/II | Level IV |
| Level IV | Lower jugular chain | 後側頭皮、頸部、氣管旁 LN、Level III | 胸管 |
| Level VA | Spinal accessory chain | 後側頭皮、頸部、鼻咽、後枕 LN、後咽 LN | Level IV |
| Level VB | Supraclavicular and Transverse cervical | 腋下 LN、Level II & III | Level IV |
| Level VI | Anterior jugular | 前側頸部、喉、下咽、甲狀腺、氣管、頸段食道 | Level II~IV |
| Other | Retroauricular | 顳側頭皮、耳後、外耳道 | Level II |
| Other | Facial(Buccal) | 臉頰、口腔 | Level IB, II |
| Other | Retropharyngeal | 鼻咽、耳咽管、軟顎、副鼻竇、中耳、咽 | Level II, V |''',
        'image': '/explanations/cropped/111-1-醫學(六)-27_merged.png'
    },
    28: {
        'text': '''此題考的是第一孕期「early pregnancy loss」相關敘述。依照題幹，「陰道出血」且「子宮頸口擴張」，並看到「有妊娠組織排出但仍有殘餘」，符合不完全性流產的定義，故選 (C)。以下補充其他種流產：

| 自發性流產種類 | 定義 | 後續處置 |
| :--- | :--- | :--- |
| 先兆性 (threatened) | 出血＋子宮頸關閉 | • 排除其他出血原因：外孕、感染、子宮頸癌變<br>• 確定子宮內胎兒的心跳<br>• 休息、觀察、給予 Progesterone（但 2019 NEJM 的 trial 發現給了並無更多好處） |
| 不完全性 (incomplete) | 出血＋子宮頸擴張＋子宮內有殘餘妊娠組織 | • GA >10 週者較難自行全部排出<br>• 可考慮：刮除 (D&C)、再觀察或給予 Misoprostol（一種 PGE1） |
| 完全性 (complete) | 妊娠組織完全排出 ⇒ 不再出血、子宮頸內口關閉 | • 檢查排出的是否為妊娠組織；或超音波檢查確定子宮內無殘餘組織<br>• 若無法排除有其他子宮外孕，可以 48 hr 後抽血評估 β-hCG |
| 過期 (missed) | 在 20 週前的胚胎或胎兒未存活，但過一段時間仍未排出妊娠組織；無出血＋子宮頸關閉 | • 先以超音波、序列性 β-hCG 評估（通常不會繼續上升或開始下降）<br>• 診斷後可考慮：等自己排出、D&C 或 Misoprostol |
| 不可避免性 (inevitable) | 出血＋子宮頸擴張；但生出來無法存活 | • 一般認為至少 GA 26 週出生後才可能存活<br>• 常見原因：子宮頸功能不全、早產早期破水 |

※ 第一孕期自發性流產的其他考點：
1. 原因
  a. 胎兒因素：50% 因染色體異常導致，其中又以三染色體 (Trisomy) 或單條 X 染色體 (monosomy X) 居多，懷孕早期便會流產
  b. 母親風險因子：懷孕年紀、流產病史、菸酒、肥胖、控制不佳的糖尿病、甲狀腺疾病、SLE 等
2. 反覆自發性流產的原因：遺傳疾病、子宮畸形（子宮中膈為風險最高者）、子宮肌瘤、子宮內膜沾黏 (=Asherman syndrome)、自體免疫疾病、血栓疾病（如：抗磷脂症候群）''',
        'image': '/explanations/cropped/111-1-醫學(六)-28_merged.png'
    },
    29: {
        'text': '''為背誦題，以下整理 methotrexate (MTX) 使用的禁忌症：

| 絕對禁忌 | 相對禁忌 |
| :--- | :--- |
| • 子宮內懷孕（= 殺寶寶不合倫理）<br>• 免疫缺失者（因骨髓抑制副作用）<br>• 貧血、血小板低下或白血球低下（因骨髓抑制副作用）<br>• 肝腎功能不佳（肝轉換成親水性代謝物 ⇒ 腎排出）<br>• 哺乳期<br>• 子宮外孕破裂<br>• 血液動力學不穩定者<br>• 無法配合醫療進行後續追蹤者 | • 胎兒有心跳<br>• 初始 β-hCG>5000 mIU/mL<br>• β-hCG 上升快速（48 hr 內 >50%）<br>• 子宮外孕囊 >4 cm |

簡單來說何時不能用：子宮內懷孕、血球免疫問題、肝腎不好、哺乳、Unstable 者

[ 其他解法 ] 雖為死背題，但依照 MTX 特性用刪去法還是可以選出來。MTX 可能進入乳汁影響寶寶所以 (B) 為禁忌；MTX 有骨髓抑制副作用，因此 (C)、(D) 狀況感覺都不太適合使用。MTX 沒有影響血糖的副作用，因此 (A) 可能是最佳的選項''',
        'image': '/explanations/cropped/111-1-醫學(六)-29_merged.png'
    },
    30: {
        'text': '''此題考「子宮外孕」（基本上是每年必考的內容）的相關處置，依照題幹所述可以得到幾點線索：
• 此女性 LMP 為 5 週前，因此預期胎齡最大為 GA 3 週
• 有流產＋子宮外孕病史，序列性 β-hCG 評估下上升的幅度 <50%，子宮內也無看到妊娠囊

因此腦中浮現的鑑別診斷：
• 優先排除子宮外孕，畢竟她是子宮外孕高風險者
• 子宮內懷孕，只是妊娠囊還看不到（畢竟胎齡最大才 GA 3 週）
• 其實根本沒有懷孕，而是長分泌 β-hCG 的腫瘤（如：絨毛膜細胞癌、妊娠滋養體疾病）⇒ 影像上無卵巢腫瘤、子宮內膜正常，故排除

因此下一步就合理性而言，選 (A) 是最合適的，再觀察選 β-hCG 上升情況
(B) Progesterone 一般只會在受孕前抽比較有意義（如：評估月經週期或排卵狀況），所以可刪
(C) 若有明確破裂、病人血液動力學不穩定，才會考慮腹腔鏡探查
(D) 抽肝腎功能與血紅素就穩定的病人而言，對於確立上述的診斷幫助有限

[ 子宮外孕的其他考點 ]
1. 臨床表現：腹痛、出血、無症狀的驗尿 β-hCG 陽性
2. 評估：內診、陰道超音波（找妊娠囊）、48 hr 的 β-hCG 上升幅度 <50%
3. 處置：Methotrexate 的藥物治療（適應症 / 禁忌症）；腹腔鏡的適應症''',
        'image': '/explanations/cropped/111-1-醫學(六)-30_merged.png'
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
