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
# Q41: page 285 [1055:1310] + page 286 [140:640]
p285_q41 = read_img(285)[1055:1310, 40:930]
p286_q41 = read_img(286)[140:640, 40:930]
write_img('public/explanations/cropped/111-1-醫學(六)-41_merged.png', np.vstack([p285_q41, p286_q41]))

# Q42: page 287 [1030:1310] + page 288 [140:810]
p287_q42 = read_img(287)[1030:1310, 40:930]
p288_q42 = read_img(288)[140:810, 40:930]
write_img('public/explanations/cropped/111-1-醫學(六)-42_merged.png', np.vstack([p287_q42, p288_q42]))

# Q43: page 286 [820:1220] + page 287 [140:720]
p286_q43 = read_img(286)[820:1220, 40:930]
p287_q43 = read_img(287)[140:720, 40:930]
write_img('public/explanations/cropped/111-1-醫學(六)-43_merged.png', np.vstack([p286_q43, p287_q43]))

# Q44: page 288 [1160:1310] + page 289 [140:765]
p288_q44 = read_img(288)[1160:1310, 40:930]
p289_q44 = read_img(289)[140:765, 40:930]
write_img('public/explanations/cropped/111-1-醫學(六)-44_merged.png', np.vstack([p288_q44, p289_q44]))

# Q45: page 290 [820:1310] + page 291 [140:715]
p290_q45 = read_img(290)[820:1310, 40:930]
p291_q45 = read_img(291)[140:715, 40:930]
write_img('public/explanations/cropped/111-1-醫學(六)-45_merged.png', np.vstack([p290_q45, p291_q45]))

# Q46: page 289 [970:1280]
write_img('public/explanations/cropped/111-1-醫學(六)-46_merged.png', read_img(289)[970:1280, 40:930])

# Q47: page 291 [1005:1310]
write_img('public/explanations/cropped/111-1-醫學(六)-47_merged.png', read_img(291)[1005:1310, 40:930])

# Q48: page 292 [415:750]
write_img('public/explanations/cropped/111-1-醫學(六)-48_merged.png', read_img(292)[415:750, 40:930])

# Q49: page 292 [1065:1310] + page 293 [140:710]
p292_q49 = read_img(292)[1065:1310, 40:930]
p293_q49 = read_img(293)[140:710, 40:930]
write_img('public/explanations/cropped/111-1-醫學(六)-49_merged.png', np.vstack([p292_q49, p293_q49]))

# Q50: page 293 [970:1340]
write_img('public/explanations/cropped/111-1-醫學(六)-50_merged.png', read_img(293)[970:1340, 40:930])

print('Cropped images generated successfully')

EXPLANATIONS = {
    41: {
        'text': '''此題考子宮肌瘤的藥物治療方式，Danazole 為一雄性激素類似物，具有抑制腦垂腺前葉的作用進而降低卵巢功能，但其目前用於子宮內膜異位症 (endometriosis)，並未用於子宮肌瘤的治療，以下簡單補充子宮肌瘤的藥物治療，包含症狀治療與病因控制：

| 治療目的 | 藥物分類 / 名稱 | 作用機轉與說明 |
| :--- | :--- | :--- |
| 症狀治療 | NSAID | 止痛，但對於大量經血沒有改善效果 |
| 症狀治療 | Tranexamic Acid | 可以改善子宮肌瘤造成大量經血的問題 |
| 病因控制 | GnRH Agonist | 因抑制 HPG 軸，進而降低 Estrogen 分泌 ⇒ 可降低子宮肌瘤大小，並改善大量經血症狀 |
| 病因控制 | GnRH Antagonist | 可以降低子宮肌瘤大小 |
| 病因控制 | Progesterone-mediated agents | • Mifepristone：抑制 Progesterone 作用，效果似 GnRH Agonist<br>• Ulipristal acetate（可造成肝傷害，目前停用）<br>• Levonorgestrel-releasing intrauterine system (LNG-IUS)：為子宮內植入物會釋放 progesterone，改善出血症狀，但無法減少子宮肌瘤大小 |''',
        'image': '/explanations/cropped/111-1-醫學(六)-41_merged.png'
    },
    42: {
        'text': '''在教科書 Berek & Novak's Gynecology 中有提及不少統計，諸如「在青春期前女孩，僅 6% 卵巢腫塊是惡性腫瘤」、「<10 歲女童的卵巢腫瘤有 1/3 是良性的」等等，雖然不是很清楚 (A) 選項「可能性很低」是指多低，但以上數字應該是不小的數字，因此 (A) 較為不適當，以下簡單補充腹骨盆腔腫塊在不同年紀常見的原因（改自 Table 9-5）：

| 年紀段 | 嬰兒期 | 青春期前 | 青春期 | 育齡期 | 停經期前 | 停經期 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 最常見 | 功能性囊腫 | | | | 纖維瘤 | 卵巢腫瘤 |
| 其他 | 生殖細胞瘤 | | 懷孕、良性畸胎瘤 / 其他生殖細胞癌、卵巢上皮腫瘤 | 懷孕、子宮肌瘤、卵巢上皮腫瘤 | 卵巢上皮腫瘤、功能性囊腫 | 功能性囊腫、其他癌症轉移 |

在兒童與青少女的卵巢腫塊中：
• 流行病學（因為各種研究的結果數字不太相同，因此講結論）：非腫瘤性囊腫為主；若是腫瘤也以良性的居多
• 卵巢腫瘤
  - 最常見的是生殖細胞瘤，約佔腫瘤的 1/2~ 2/3；卵巢上皮腫瘤很罕見
  - 年紀較小長出的腫瘤有較高機會是惡性的
• 檢查診斷：腹部超音波為最適用的初步評估，後續進階使用 CT、MRI 等檢查

[ 編按 ] 此題與【111-2(六)43】考點類似，同樣考兒童和青少女的卵巢腫瘤''',
        'image': '/explanations/cropped/111-1-醫學(六)-42_merged.png'
    },
    43: {
        'text': '''子宮鏡子宮肌瘤切除術 (hysteroscopic myomectomy) 最常使用於黏膜下子宮肌瘤 (submucous fibroids)，包含 Type 0（有蒂的長在子宮腔中）、<5 cm 的 Type 1（子宮壁侵犯 <50%）與侵犯深度較淺的 Type 2（子宮壁侵犯 ≥50%），故按照選項所給予有限的資訊，(A) 為最適當的答案

[ 另類解法 ] 子宮肌瘤分類總共為 FIGO Type 0-8，由子宮腔內至子宮體外依序編號（Type 8 是長在子宮體以外的地方，建議搭配圖片加深印象）；故藉由子宮鏡最容易切除的就是直接長在腔內的，Type 0 可能是最佳答案

FIGO Classification of Uterine Myoma：

| 類型 | FIGO | 說明 |
| :--- | :--- | :--- |
| Submucosal 黏膜下型 | 0 | 蒂連式子宮腔內肌瘤：有蒂且完全在子宮腔內 (pedunculated intracavitary) |
| Submucosal 黏膜下型 | 1 | 大部分在子宮腔內，<50% 在子宮肌層 |
| Submucosal 黏膜下型 | 2 | 少部分在子宮腔內，≥50% 在子宮肌層 |
| Intramural 壁間型 | 3 | 完全在子宮肌層，且有接觸到子宮內膜 (endometrium) |
| Intramural 壁間型 | 4 | 完全在子宮基層，但沒有接觸到子宮內膜 |
| Subserosal 漿膜下型 | 5 | 少部分在子宮肌層外，≥50% 在子宮肌層 |
| Subserosal 漿膜下型 | 6 | 大部分在子宮肌層外，<50% 在子宮肌層 |
| Subserosal 漿膜下型 | 7 | 蒂連式子宮漿膜層肌瘤：有蒂且完全在子宮肌層外 (subserosal pedunculated) |
| 其他 | 8 | 在子宮本體以外的部分，如子宮頸內、闊韌帶中 |''',
        'image': '/explanations/cropped/111-1-醫學(六)-43_merged.png'
    },
    44: {
        'text': '''第二性徵發育遲緩與性腺激素分泌低下有關，如：先天性腺發育不良、卵巢早衰（如：透納氏症）、下視丘 / 腦垂腺分泌不足（如：卡門症候群 Kallmann syndrome）等；而 Müllerian duct 發育異常常見的原因與性激素較不相關，也因性腺功能無異常所以大多會表現第二性徵，故 (B) 敘述不適當，以下補充無月經伴隨正常第二性徵發育但骨盆腔解剖異常的常見原因：
• 先天穆勒氏管異常 (Müllerian anomalies)
  - 封閉處女膜 (Imperforate hymen)
  - 陰道橫向中膈 (transverse vaginal septum)
  - Mayer-Rokitansky-Küster-Hauser 症候群（= 先天無陰道＋各種程度的子宮發育）：佔原發性閉經 10-15% 病例，多伴隨腎臟、泌尿系統、骨骼、聽力發育異常
  - 先天無子宮內膜
• 後天性子宮內沾黏 (=Asherman syndrome)：多因子宮內膜刮除術 (D&C)、子宮頸手術、骨盆腔發炎疾病或結核菌感染所致
• 雄性素不敏感 (androgen insensitivity)：生理男 (46, XY) 但因雄性素異常導致外生殖器、第二性徵為女性表現，無穆勒氏管發育（因可分泌 AMH）
• 性發展障礙 (ovotesticular disorder)：很罕見，同時具有卵巢與睪丸，通常會半側 Mullerian 發育（像女）、半側 Wolffian 發育（像男），外生殖器雌雄難辨，通常會有乳房發育''',
        'image': '/explanations/cropped/111-1-醫學(六)-44_merged.png'
    },
    45: {
        'text': '''影像題，抓關鍵字與關鍵特徵：
• 關鍵字：經痛已 5 年（慢性＋週期性疼痛），止痛藥可緩解 ⇒ 週期性疼痛可以考慮原發性痛經與子宮內膜異位症 (endometriosis) 或 Müllerian anomalies【111-1(六)44】；若非週期性，可能會考慮腹骨盆腔沾黏、發炎或卵巢腫瘤，子宮內膜異位也可能是非週期性疼痛
• 影像（卵巢囊腫）
  - 「毛玻璃樣 (ground glass appearance)」的回音病灶，看起來沙沙的
  - 無明顯低回音或高回音部分，意即無固體組織或漿液成分
  - 無分膈，應屬於單腔室囊腫 (unilocular cyst)
  - 圖為 Color doppler 介面，也無看到血流
故從影像上可以得知，偏向卵巢子宮內膜異位瘤 (ovarian endometrioma) 特徵，較不像卵巢腫瘤（纖維瘤 / 卵巢癌）或是功能性囊腫

故綜合兩者，(B) 為最合適的診斷
(A) 卵巢濾泡囊腫 (ovarian follicular cyst)：大多無症狀；超音波下內部無回音，且通常可見後側回音增強 (posterior acoustic enhancement)
(C) 卵巢纖維瘤 (ovarian fibroma)：大多無症狀，但長到很大時可觸診到；在超音波下的型態通常為低回音的腫塊 (hypoechoic mass)
(D) 卵巢癌 (ovarian cancer)：若在超音波下出現以下特徵，病灶為惡性的機會較高：
  • 邊緣不規則的固態腫塊
  • 超音波下看到腹水
  • 看到多個乳突狀贅生物
  • 不規則、多腔室、直徑大 (>10 cm) 的腫塊
  • 都卜勒超音波下血流豐富''',
        'image': '/explanations/cropped/111-1-醫學(六)-45_merged.png'
    },
    46: {
        'text': '''Müllerian ducts 發育異常常伴隨腎臟泌尿道的異常，所以應一併進行檢查（關於 Müllerian anomalies 相關整理可見【111-1(六)44】的詳解）

[ 另類解題方式 ] 從胚胎學的角度來看，泌尿與生殖系統的發育是一起的，Woffian duct（男性保留）來自中腎管 (mesonephric duct) 構造，而 Müllerian duct（女性保留）來自副中腎管 (mesonephric duct)，而發育早期的中腎 (metanephron) 逐漸退化，故相較於其他選項，(C) 同時發生異常的機會較高，所以應一併檢查''',
        'image': '/explanations/cropped/111-1-醫學(六)-46_merged.png'
    },
    47: {
        'text': '''陰道常在菌叢包含乳酸菌（製造乳酸建立陰道酸性環境）、乙型鏈球菌等嗜氧菌；而細菌性陰道炎 (BV) 是陰道內厭氧菌過度增生，取代常在菌叢導致，其風險因子包含陰道灌洗或性行為（鹼性的精液），容易破壞常在菌叢或酸性環境

故刪去 (A) (B) (D) 敘述不正確的選項後，(C) 是剩餘最適當的選項

[ 編按 ] 暑考【111-2(六)48】同樣也考 BV！''',
        'image': '/explanations/cropped/111-1-醫學(六)-47_merged.png'
    },
    48: {
        'text': '''停經後子宮內異常出血常見的原因包含（取自 Berek & Novak's Gynecology, Table 10-13）：外源性雌激素 (30%)、萎縮性子宮內膜炎 / 陰道炎 (30%)、子宮內膜癌 (15%)、子宮內膜 / 子宮頸息肉 (10%)、子宮內膜增生 (5%)，故沒有服用荷爾蒙者，最常見的成因就是萎縮性子宮內膜炎，故選 (D)

[ 另類解題方式 ] 題幹所述「沒有服用荷爾蒙（未明示 estrogen 或 estrogen + progesterone）」的停經女性，而 (A) (B) (C) 的生長皆與荷爾蒙相關，因此 (D) 為可能的答案''',
        'image': '/explanations/cropped/111-1-醫學(六)-48_merged.png'
    },
    49: {
        'text': '''依照題目資訊：病理診斷是子宮頸癌，大小 1 cm、侵犯深度 5 mm，且病灶僅限於子宮頸而沒有侵犯至陰道（刪去 (B)）、鄰近構造（刪去 (C)）、遠端器官（刪去 (D)），故依照 2018 FIGO for Cervical Cancer 的分期為 Stage IB1（子宮頸內，深度 ≥ 5 mm、最大橫徑 <2 cm），以下簡單提供 2018 FIGO for Cervical Cancer 的記法：

| 期別 | 定義與侵犯範圍 | 細分期與腫瘤大小 |
| :--- | :--- | :--- |
| IA | 顯微鏡才看得到，侵犯深度 <5 mm ⇒ 比深度（往下） | IA1: <3 mm<br>IA2: ≥ 3, <5 mm |
| IB | 侵犯深度 ≥ 5 mm，且肉眼可見 ⇒ 比大小（往側） | IB1: <2 cm<br>IB2: ≥ 2, <4 cm<br>IB3: ≥ 4 cm |
| IIA | 侵犯出子宮體，往下至陰道上 2/3 部分 | IIA1：<4 cm<br>IIA2：≥ 4 cm |
| IIB | 侵犯出子宮體，往側向的鄰近構造 (parametrial involvement) | |
| IIIA | 往下至陰道下 1/3 部分 | |
| IIIB | 往側至骨盆腔壁，或因壓迫輸尿管造成腎水腫 / 腎衰竭 | |
| IIIC | 淋巴轉移至骨盆腔 / 主動脈旁淋巴結 | IIIC1：僅骨盆腔<br>IIIC2：主動脈旁 |
| IV | IVA: 其他骨盆腔器官；IVB: 轉移至遠端器官 | |

[ 編按 ] FIGO 有時真的不好記，子宮頸癌可依照其擴散方向的簡單記憶（上表粗體字）''',
        'image': '/explanations/cropped/111-1-醫學(六)-49_merged.png'
    },
    50: {
        'text': '''這題考名詞定義，neoadjuvant 治療指的是：在正式治癒性治療（通常是手術）之前，所進行的輔助治療，故 (A) 的敘述為最適當的答案
(B) 敘述為輔助性治療 (adjuvant therapy)，通常針對在治癒性治療後有高局部擴散或隱性全身擴散風險者所安排
(C) 敘述的化學治療較接近 adjuvant chemotherapy 的概念
(D) 敘述的是針對復發腫瘤以化學治療作為治癒性治療，而非輔助治療''',
        'image': '/explanations/cropped/111-1-醫學(六)-50_merged.png'
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
