# -*- coding: utf-8 -*-
import json
import os

EXPLANATIONS = {
    11: {
        "text": """(A) 大腸菌叢可幫助維持 epithelial integrity，並且與大腸中澱粉和蛋白質的分解、膽紅素 / 膽酸 / 雌性激素 / 膽固醇的代謝、維生素 K 等的製造皆有關

(B) 厭氧菌佔大腸細菌的大宗，其中最多的是 Bacteroides 並且佔大腸細菌的 2/3；而最多的嗜氧菌則為 E. coli

(C) 大腸菌叢富有尿素分解酵素 (urease)，可將尿素代謝成氨，進入血液運輸至 portal circulation，再進入肝細胞的 urea cycle (約 85%) 或直接進入體循環 (約 15%)，故可幫助 urea recycling 的進行。但當病人發生肝臟衰竭時，肝臟無法重複使用從大腸回收的尿素氮 (urea nitrogen)，因此它們將大量進入體循環，通過 BBB 造成肝性腦病變或肝昏迷

(D) 大腸為胃腸道中吸收能力最佳的部分，每天可吸收高達 5L 的水分，但由於在正常的生理狀況下，大量水分會先在小腸吸收，最後流往大腸的約只剩 1~2L 左右，故大腸一般來說每天吸收的水分並不會到 5L 那麼多""",
        "image": "/explanations/cropped/111-1-醫學(五)-11_merged.png"
    },
    12: {
        "text": "缺頁",
        "image": None
    },
    13: {
        "text": "缺頁",
        "image": None
    },
    14: {
        "text": "缺頁",
        "image": None
    },
    15: {
        "text": """腦血管痙攣 (cerebral vasospasm) 通常發生於血管暴露於血液之中，可能和血塊溶解時產生的血管收縮物質相關，常發生於腦動脈瘤破裂出血後造成的 SAH，腦血管痙攣後可能導致腦部缺氧

(A) 發生 SAH 後數分鐘到數小時就可能發生早期 vasospasm，延遲性 vasospasm 通常發生於 4~14 天後，其中最多會發生於 SAH 的 6~10 天後

(B) 腦動脈瘤破裂出血後造成之 SAH 的嚴重程度，可用 Hunt and Hess clinical grading scale 描述之，並且可藉由此 grading scale 預測病人預後：

| Hunt & Hess | 臨床特徵 | 存活率 |
| :--- | :--- | :--- |
| Grade 0 | • 動脈瘤未破裂，且無症狀 | |
| Grade 1 | • 無症狀或輕微頭痛，且伴有輕微頸部僵硬 | 70% |
| Grade 2 | • 中度到重度頭痛且伴有頸部僵硬<br>• 除顱神經麻痺 (cranial nerve palsy) 外，無其他神經學異常 | 60% |
| Grade 3 | • 嗜睡 (drowsy)<br>• 輕微神經學異常 | 50% |
| Grade 4 | • 木僵無反應 (stupor)<br>• 中度到重度半癱 (hemiparesis)<br>• 可能有早期去大腦性僵直、瀕臨植物人狀態的情況 (early decerebrate rigidity and vegetative disturbance) | 20% |
| Grade 5 | • 昏迷 (deep coma)、去大腦性僵直、垂死 (moribund) | 10% |

另有 Fisher Grade 藉由在 CT 上看到的出血量預測 symptomatic cerebral vasospasm 的風險並加以分級：

#### Modified Fisher Grade
| | 臨床特徵 | 有症狀的腦血管痙攣發生率 |
| :--- | :--- | :--- |
| Grade 1 | 無 SAH 或 IVH | 21% |
| Grade 2 | 廣泛性 <1 mm 的 SAH、無血塊 | 25% |
| Grade 3 | 有局部血塊或 >1 mm 厚的 SAH；無 IVH | 37% |
| Grade 4 | 有廣泛性 SAH 或無 SAH；有 IVH 或 ICH | 31% |

*\\*SAH: subarachnoid hemorrhage 蜘蛛網膜下出血*<br>*\\*IVH: intraventricular hemorrhage 腦室內出血*<br>*\\*ICH: intracerebral hemorrhage 腦實質出血*

相較之下，Fisher Grade 以 CT 下看到的出血量進行分級，故可較直接地預測腦血管痙攣發生的機率；Hunt and Hess 主要為 SAH 嚴重程度的分級，而 SAH 越嚴重其發生後續併發症的機率較高也算是合理的敘述

(C) 由於腦血管痙攣為血管暴露於血液中所致，因此可推知基底腦池出血量越多，發生腦血管痙攣的機會也就會越高

(D) 腦血管痙攣的預防及處置方法：

| 類別 | 內容 |
| :--- | :--- |
| 預防 | • 稍微提高血壓以及適度補充體液 (mild hypervolemia)，以維持足夠灌流量<br>• 給予 nimodipine (為一種可降低血管痙攣發生率與發生程度的 CCB 藥物，但其作用機制仍有爭議) |
| 處置 | • 給予 papaverine (罌粟鹼) 或 nicardipine<br>• 以氣球擴張術 (balloon angioplasty) 維持較大的血管管徑<br>• hemodynamic augmentation: 增加腦內灌流量<br>\\*以往以 HHH therapy (hypertension, hypervolemia, hemodilution) 為治療首選，藉由維持灌流充足避免腦血管痙攣後的腦部缺氧，但 hemodilution 治療仍存有些許爭議 |""",
        "image": "/explanations/cropped/111-1-醫學(五)-15_merged.png"
    },
    16: {
        "text": """(A) 水平方向躍視 (horizontal saccade)：以雙眼向左側看為例，此同向共軛凝視 (conjugate gaze) 由對側 (右) 額葉眼區 (Brodmann area 8 = frontal eye field, FEF) 啟動同側 (左) 橋腦旁正中網狀結構 (paramedian pontine reticular formation, PPRF)，進一步通過興奮爆裂性神經元 (burst neurones) 而啟動鄰近同側 (左) 外直肌的外展神經運動神經，再上升進入內側縱束 (MLF) 到達對側 (右) 動眼神經核內直肌，因此產生雙眼同方向朝左看 (levoversion) 時，左眼外直肌及右眼內直肌會同時作用移動雙眼注視目標 (可上網搜尋 "horizontal conjugate gaze pathway"，看圖更清楚)。由此可知，當出血位置影響右側 Brodmann area 8 時，便會影響共軛凝視的路徑，導致雙眼向左側看的機制受到影響，而使雙眼只能偏向右側

(B) 癲癇發作的第一線藥物通常為 BZD 類藥物，給予 3~5 分鐘後觀察仍有癲癇發作則可給予第二線藥物，包括 Phenytoin 及 Valproic acid 等。若使用到第二線藥物後仍有癲癇發作，則應考慮插管並考慮給予麻醉藥物 (如：Phenobarbital, Midazolam, Propofol 等)""",
        "image": "/explanations/cropped/111-1-醫學(五)-16_merged.png"
    },
    17: {
        "text": """(B) Ulnar nerve 才是走在 Guyon's canal 內的神經""",
        "image": "/explanations/cropped/111-1-醫學(五)-17_merged.png"
    },
    18: {
        "text": """CPP = MAP - ICP
故此題的 CPP = (1/3 × 150 + 2/3 × 90) - 25 = 110 - 25 = 85""",
        "image": "/explanations/cropped/111-1-醫學(五)-18_merged.png"
    },
    19: {
        "text": """#### Cerebral vascular disease
| 分類 | 疾病類型 |
| :--- | :--- |
| 先天性 (congenital) | • 動靜脈畸形與廔管 (arteriovenous malformation and fistula)<br>• 海綿竇畸形 (cavernous malformation)<br>• 毛細血管擴張 (telangiectasia)<br>• 腦部靜脈異常 (venous anomaly, angioma) |
| 後天性 (acquired) | • 創傷性：部分動靜脈廔管 (如 type I carotid-cavernous fistula)、創傷性動脈瘤 (traumatic aneurysm)<br>• 退化性：動脈粥狀硬化導致的血管阻塞性疾病、大部分腦部漿果動脈瘤 (cerebral berry aneurysm)、部分動脈剝離 (arterial dissection)、自發性腦內出血 (spontaneous intracerebral hemorrhage)<br>• 感染性：感染性動脈瘤 (mycotic aneurysm) |
| 病因不明 (idiopathic) | • 毛毛樣血管疾病 (moyamoya)<br>• 部分動靜脈廔管 (如 dural AVM-like 或 type II carotid-cavernous fistula) |

*(整理自 2021 Sabiston BOX 68.1)*""",
        "image": "/explanations/cropped/111-1-醫學(五)-19_merged.png"
    },
    20: {
        "text": """腦脊髓液 (CSF) 由脈絡叢 (choroid plexus) 分泌，每天定量製造 500 mL (相當於 20.83 mL/hr)，並回收等量的 CSF，但任何時間下腦室及蜘蛛膜下腔的 CSF 只有約 150 mL，因此每天會循環 3~4 次。其流向為：側腦室 → 通過腦室間孔 (interventricular foramina = foramen of Monro) → 第三腦室 → 塞爾維氏大腦導水管 (central aqueduct of Sylvius) → 第四腦室 → 通過正中孔 (medial aperture = foramen of Magendie) 及 2 個外側孔 (lateral aperture = foramen of Luschka) 分別進入小腦延髓池 (cisterna magna) 及橋腦池 (pontine cisterna) → 進入脊髓及其他蜘蛛膜下腔的空間。CSF 可經由蜘蛛膜絨毛 (arachnoid villi) 吸收回到靜脈系統""",
        "image": "/explanations/cropped/111-1-醫學(五)-20_merged.png"
    }
}

def main():
    # 1. Validation of explanations before saving
    for qn, data in EXPLANATIONS.items():
        text = data["text"]
        img = data["image"]
        
        # Check trailing period on lines
        for idx, line in enumerate(text.split("\n")):
            line_str = line.strip()
            if line_str.endswith("。"):
                raise ValueError(f"Q{qn} line {idx+1} ends with period: {line_str}")
        
        # Check LaTeX
        if "$" in text:
            raise ValueError(f"Q{qn} contains LaTeX $: {text}")
        
        # Check image existence if not None
        if img is not None:
            local_img_path = os.path.join("public", img.lstrip("/"))
            if not os.path.exists(local_img_path):
                raise FileNotFoundError(f"Image not found for Q{qn}: {local_img_path}")

    print("All explanation texts and images passed validation")

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

    print("Successfully finished updating Q11-Q20")

if __name__ == "__main__":
    main()
