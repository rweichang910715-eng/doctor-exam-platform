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
# Q21: page 151 [628:1145]
write_img('public/explanations/cropped/111-1-醫學(五)-21_merged.png', read_img(151)[628:1145, 40:930])

# Q22: page 153 [368:990]
write_img('public/explanations/cropped/111-1-醫學(五)-22_merged.png', read_img(153)[368:990, 40:930])

# Q23: page 388 [1010:1320] + page 389 [160:285]
q23 = np.vstack([read_img(388)[1010:1320, 40:930], read_img(389)[160:285, 40:930]])
write_img('public/explanations/cropped/111-1-醫學(五)-23_merged.png', q23)

# Q24: page 152 [490:1240]
write_img('public/explanations/cropped/111-1-醫學(五)-24_merged.png', read_img(152)[490:1240, 40:930])

# Q25: page 154 [162:425]
write_img('public/explanations/cropped/111-1-醫學(五)-25_merged.png', read_img(154)[162:425, 40:930])

# Q26: page 133 [758:1285]
write_img('public/explanations/cropped/111-1-醫學(五)-26_merged.png', read_img(133)[758:1285, 40:930])

# Q27: page 134 [678:1175]
write_img('public/explanations/cropped/111-1-醫學(五)-27_merged.png', read_img(134)[678:1175, 40:930])

# Q28: page 135 [618:850]
write_img('public/explanations/cropped/111-1-醫學(五)-28_merged.png', read_img(135)[618:850, 40:930])

# Q29: page 137 [865:1285] + page 138 [162:575]
q29 = np.vstack([read_img(137)[865:1285, 40:930], read_img(138)[162:575, 40:930]])
write_img('public/explanations/cropped/111-1-醫學(五)-29_merged.png', q29)

# Q30: page 188 [582:1240] + page 189 [165:890]
q30 = np.vstack([read_img(188)[582:1240, 40:930], read_img(189)[165:890, 40:930]])
write_img('public/explanations/cropped/111-1-醫學(五)-30_merged.png', q30)

print("Images cropped successfully")

EXPLANATIONS = {
    21: {
        "text": """(A) 燒燙傷傷口的感染預防，以局部塗抹的抗生素藥膏為主

(B) 初期主要感染菌株為革蘭氏陽性菌

(C) (D) 磺胺銀 (Silver sulfadiazine) 可對抗革蘭氏陽性菌、大部分革蘭氏陰性菌及部分真菌，且塗抹時較不會造成疼痛、病人接受度高，但須每天換藥而可能增加換藥時疼痛的次數、可能造成白血球低下，並且無法穿透焦痂；醋酸磺胺米隆 (Mafenide acetate) 亦為廣效藥膏，且尤其對具抗性的 Pseudomonas 及 Enterococcus 效果佳，亦可穿透焦痂，但缺點是塗抹時非常疼痛、可能造成皮膚過敏以及大面積塗抹時可能導致代謝性酸中毒 (因具有抑制碳酸酐酶 carbonic anhydrase 的特性)，因此較適合用於小面積全層 (full-thickness) 傷口

參考資料：Sabiston Textbook of Surgery: The Biological Basis of Modern Surgical Basis (2021). Chapter 20""",
        "image": "/explanations/cropped/111-1-醫學(五)-21_merged.png"
    },
    22: {
        "text": """傷口癒合主要會經歷止血期 (coagulation and hemostasis phase) → 發炎期 (inflammation phase) → 增生期 (proliferation phase)，其中肉芽組織會在增生期形成，為纖維母細胞 (fibroblast)、血管內皮細胞 (vascular endothelial cells) 及巨噬細胞 (macrophage) 所組成

| 階段 | 特徵 |
| :--- | :--- |
| 止血期 (coagulation and hemostasis phase) | • 一旦受傷，便啟動凝血機制<br>• 血小板與 fibrin 凝成血塊避免持續出血 |
| 發炎期 (inflammation phase) | • 受傷後 3 天內發生<br>• 前 48 小時，主要由 neutrophil 負責抵禦感染<br>• 受傷第 4 天後，neutrophil 漸漸被 macrophage 取代，其會吞噬傷口殘骸及存在的病原菌 |
| 增生期 (proliferation phase) | • 受傷後 3 天左右，可持續數週<br>• fibroblast 分泌 type III collagen，提供細胞增生的骨架<br>• myofibroblast 為幫助傷口縮合的主要細胞<br>• 上皮細胞會由傷口邊緣漸漸移行到傷口中央，將其覆蓋住 |
| 再塑期 (remodeling phase) | • 約受傷後 2-3 週開始，可持續數週 ~ 數年<br>• type III collagen 會被排列較整齊的 type I collagen 取代；形成疤痕 |""",
        "image": "/explanations/cropped/111-1-醫學(五)-22_merged.png"
    },
    23: {
        "text": """(A) 手腕彎曲時會壓迫到正中神經，進而加重症狀

(B) 腕隧道症候群的治療方法可分為保守治療及手術治療：

| 保守治療 | 手術治療 |
| :--- | :--- |
| • 減少反覆的手腕動作<br>• 手腕反覆動作後冰敷<br>• 戴護腕輔具，減少手部不自主活動壓迫神經的機會<br>• 止痛藥 | 切斷正中神經上的腕橫韌帶，減少腕隧道受到的壓迫，改善症狀；可直接開刀或者透過微創手術完成 |

(C) 魚際肌萎縮應為嚴重、慢性腕隧道症候群會出現的症狀

(D) 副木治療屬於保守治療的一種，當保守治療皆無效時才考慮手術治療""",
        "image": "/explanations/cropped/111-1-醫學(五)-23_merged.png"
    },
    24: {
        "text": """Skin graft 分為分層皮膚移植 (split thickness skin graft, STSG) 及全層皮膚移植 (full thickness skin graft, FTSG)，二者的比較如下表：

| | STSG（薄） | STSG（厚） | FTSG |
| :--- | :--- | :--- | :--- |
| 組成 | 表皮層+部分真皮層 | 表皮層+部分真皮層 | 表皮層+整個真皮層 (+部分皮膚附屬器官) |
| 供皮區選擇 | 可取自皮膚各處，原則上以平坦處為佳，常見如大腿、背部、腹部、臀部、頭皮等 | 可取自皮膚各處，原則上以平坦處為佳，常見如大腿、背部、腹部、臀部、頭皮等 | 通常選擇皮膚較薄處，如鼠蹊無毛處、上眼眶、手肘、耳後、鎖骨上 |
| 移植難度 | 較易成功 | 較易成功 | 較易失敗 |
| 美觀 | 較不美觀、易色素沉澱 | 較不美觀、易色素沉澱 | 較美觀、不易色素沉澱 |
| 初級攣縮 (primary contraction) | + | ++ | +++ |
| 次級攣縮 (secondary contraction) | +++ | ++ | + |

*(整理自 2021 Sabiston Chapter 69 及 2019 Schwartz's Principles of Surgery Chapter 45)*

(D) 頭皮下的毛囊豐富，毛囊中的上皮細胞可快速增生、分化，形成新的表皮，可作為 STSG 的供皮區，且頭皮是唯一不會留下疤痕的供皮區，但缺點是必須剃掉頭髮且較缺乏彈性、脆弱不耐壓磨""",
        "image": "/explanations/cropped/111-1-醫學(五)-24_merged.png"
    },
    25: {
        "text": """(C) 除非是影響到腦部或危及生命的顏面骨折，否則大多不需立即進行手術復位及固定，可待病人其他受傷部分處理好之後再進行即可

(D) 顏面外傷若撞擊到眼眶，可能導致眼壓升高、眼球破壞、眼球外血腫壓迫或間接外傷壓迫性眼神經受損而導致視力受損""",
        "image": "/explanations/cropped/111-1-醫學(五)-25_merged.png"
    },
    26: {
        "text": """當發生瓣膜功能不全時，起初會先以藥物改善心臟功能，當藥物作用開始無法維持心臟功能時，便會評估是否適合進行瓣膜手術，包括瓣膜修補及瓣膜置換。當瓣膜已確定無法修補，則可考慮以人工瓣膜做置換，人工瓣膜主要可分為以下兩類：

| | 機械性瓣膜 | 生物性瓣膜 |
| :--- | :--- | :--- |
| 主要材料 | 碳纖維、金屬 | 豬瓣膜、牛瓣膜 |
| 一般耐用年限 | 耐用期較長 (接近終身) | 耐用期較短 (約 15-20 年) |
| 口服抗凝血劑 | 終身使用 | 使用 3 個月 |
| 適用族群 | • 使用期長且較便宜，但須終身服用抗凝血劑，故適合餘命較長的年輕人<br>• 若患者原就患有心房顫動等需長期口服抗凝血劑的疾病，則適合機械性瓣膜<br>• 不適合無法配合服用抗凝血劑者 | • 雖價格昂貴且較不耐用，但血栓機率較低，適合老年人、有重大疾病者<br>• 因僅需使用 3 個月的口服抗凝血劑，故適合有懷孕計畫者<br>• 適合無法配合使用抗凝血劑、有出血傾向者 |""",
        "image": "/explanations/cropped/111-1-醫學(五)-26_merged.png"
    },
    27: {
        "text": """#### 冠狀動脈繞道手術 (coronary artery bypass grafting, CABG)
| | 有幫浦停跳 (on-pump) | 無幫浦不停跳 (off-pump) |
| :--- | :--- | :--- |
| 特徵 | 使用心肺機，為病患做體外心肺循環，可在術中使心跳暫時停止 | 使用心臟穩定器穩定心臟，在心臟跳動的情況下吻合血管 |
| 優點 | 增加冠狀動脈吻合的準確度 | 不會有使用心肺機的種種缺點，較適合中風風險高的患者 |
| 缺點 | 心肺機的使用 (1) 易使免疫系統受刺激而產生發炎反應 (2) 耗損凝血因子、破壞血小板、破壞紅血球導致溶血 (3) 心臟暫時停止跳動，造成心臟短暫缺血 | 冠狀動脈吻合的準確度較低，手術困難度較高 |
| 總體比較 | 二者在短期存活率、再次需要介入性治療的機率沒有顯著差異，但對於中風高風險患者，建議可使用 off-pump CABG | 二者在短期存活率、再次需要介入性治療的機率沒有顯著差異，但對於中風高風險患者，建議可使用 off-pump CABG |""",
        "image": "/explanations/cropped/111-1-醫學(五)-27_merged.png"
    },
    28: {
        "text": """IABP 乃將氣球導管經由鼠蹊部股動脈引導至降主動脈靠近主動脈弓處 (圖中 III)。當心臟收縮時氣球會塌陷而減輕心臟的 afterload，使血液較易供應到全身；當心臟舒張時則氣球膨脹，將血液壓回升主動脈，並增加冠狀動脈灌流，使供應心臟的血液足夠""",
        "image": "/explanations/cropped/111-1-醫學(五)-28_merged.png"
    },
    29: {
        "text": """(A) 診斷應為內頸動脈狹窄

(B) 聽診時聽到頸動脈雜音 (carotid bruit) 可能暗示有頸動脈狹窄，但並非所有頸動脈狹窄的人一定會聽到頸動脈雜音，頸動脈狹窄的標準診斷工具為血管攝影，能精確指出狹窄位置及狹窄程度，唯其為一侵入性檢查故具有潛在危險性；其他診斷工具包括頸動脈都卜勒超音波 (carotid Duplex ultrasonography, DUS)、電腦斷層血管攝影 (CTA)、腦血管核磁共振 (MRA) 等

(C) 當內頸動脈狹窄時，由於眼動脈血流會受影響，而會發生單側、同側暫時性黑矇症 (amaurosis fugax = 短暫的視野變暗或失明)

(D) 頸動脈內膜摘除術 (carotid endarterectomy, CEA) 為切開頸動脈後將粥狀斑塊切除的手術，比起單純藥物治療可減少腦中風的發生率""",
        "image": "/explanations/cropped/111-1-醫學(五)-29_merged.png"
    },
    30: {
        "text": """動脈導管 (ductus ateriosus) 為連接肺動脈與主動脈的血管，一般而言會在新生兒出生後的數天內關閉，若未關閉就會出現開放性動脈導管 (patent ductus ateriosus)，使得充氧血與缺氧血混合，導致肺高壓、低血氧、心律不整等情況。前列腺素 E1 會使動脈導管保持開放狀態。以下的先天性心臟病反而需要動脈導管的開放以暫時緩解血氧下降及發紺的危況，故而需給予前列腺素 E1，根據狀況可分為 3 類：

| 分類 | 疾病類型 |
| :--- | :--- |
| (1) 肺動脈血流嚴重受限 (severe restriction of pulmonary blood flow)<br>→缺氧血無法流到肺循環，使得身體缺乏足夠充氧血而發紺、低血氧 | • 肺動脈瓣閉鎖 (pulmonary atresia)<br>• 三尖瓣閉鎖 (tricuspid atresia)<br>• 法洛氏四重症 (tetralogy of Fallot) |
| (2) 全身血流嚴重受限 (severe restriction of systemic blood flow)<br>→充氧血無法順利打出到各器官系統，造成低灌流、嚴重鬱積型心衰竭 | • 主動脈狹窄 (aortic stenosis)<br>• 主動脈窄縮 (coarctation of the aorta)<br>• 主動脈弓中斷 (interrupted aortic arch)：主動脈轉彎處發生中斷，使血液無法打往下肢<br>• 左心發育不良症候群 (left heart hypoplastic syndrome)：心臟左側發育不良，循環發生嚴重阻塞 |
| (3) 心臟結構異常 (cardiac anomalies) | • 大動脈轉位 (transposition of great arteries, TGA)：主動脈源於右心室，缺氧血直接打入體循環；肺動脈源於左心室，接受來自肺靜脈的充氧血並回到肺循環，使組織缺氧；當合併心房中膈缺損、心室中膈缺損時，充氧血與缺氧血會混合，稍微減緩發紺的情形 |

(C) 全肺靜脈回流異常 (total anomalous pulmonary venous return, TAPVR)：胚胎發育時，肺靜脈未能順利與左心房相連，而是經由其他通道連接到右心房，再藉由新生兒尚開啟的卵圓孔或心房中膈缺損灌入左心房後流往全身；當回流的途徑阻塞時，血液就會積在肺臟，無法正常回到左心房，其中又以心下型發生回流阻塞時最為嚴重 (因肺靜脈回流會通過橫膈膜再到門靜脈系統，相對而言是很長的路徑)

| 類型 | 特徵 |
| :--- | :--- |
| 心上型 (supracardiac type) | 肺靜脈與上腔靜脈 (SVC) 相連 |
| 心臟型 (cardiac type) | 肺靜脈與右心室相連 |
| 心下型 (infracardiac type) | 肺靜脈與門靜脈相連 |

由上述可知，TAPVR 發生阻塞時，即使給予前列腺素 E1 保持動脈導管暢通 (使血液可在肺靜脈與主動脈間流通)，血液仍無法順利回到左心，此種情況必須進行緊急手術將不正常的肺靜脈接回左心房並關閉心房中膈，使血液循環恢復正常""",
        "image": "/explanations/cropped/111-1-醫學(五)-30_merged.png"
    }
}

def main():
    # 1. Validation
    for qn, data in EXPLANATIONS.items():
        text = data["text"]
        img = data["image"]
        for idx, line in enumerate(text.split("\n")):
            line_str = line.strip()
            if line_str.endswith("。"):
                raise ValueError(f"Q{qn} line {idx+1} ends with period: {line_str}")
        if "$" in text:
            raise ValueError(f"Q{qn} contains LaTeX $: {text}")
        if img is not None:
            local_img_path = os.path.join("public", img.lstrip("/"))
            if not os.path.exists(local_img_path):
                raise FileNotFoundError(f"Image not found for Q{qn}: {local_img_path}")

    print("All Q21-Q30 explanation texts and images passed validation")

    # 2. Update questions.json
    with open("src/data/questions.json", "r", encoding="utf-8") as f:
        questions = json.load(f)

    updated_count = 0
    for q in questions:
        qid = q.get("id", "")
        if qid.startswith("111-1-醫學(五)-"):
            num = int(qid.split("-")[-1])
            if num in EXPLANATIONS:
                q["explanation"] = EXPLANATIONS[num]["text"]
                q["explanation_image"] = EXPLANATIONS[num]["image"]
                updated_count += 1

    print(f"Updated {updated_count} questions in questions.json")
    with open("src/data/questions.json", "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

    # 3. Update explanations_map.json
    with open("src/data/explanations_map.json", "r", encoding="utf-8") as f:
        exp_map = json.load(f)

    map_updated_count = 0
    for num, data in EXPLANATIONS.items():
        qid = f"111-1-醫學(五)-{num}"
        exp_map[qid] = {
            "explanation": data["text"],
            "explanation_image": data["image"]
        }
        map_updated_count += 1

    print(f"Updated {map_updated_count} entries in explanations_map.json")
    with open("src/data/explanations_map.json", "w", encoding="utf-8") as f:
        json.dump(exp_map, f, ensure_ascii=False, indent=2)

    print("Successfully finished updating Q21-Q30")

if __name__ == "__main__":
    main()
