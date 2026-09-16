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
# Q31: page 165 [478:1320]
write_img('public/explanations/cropped/111-1-醫學(五)-31_merged.png', read_img(165)[478:1320, 40:930])

# Q32: page 136 [162:1170]
write_img('public/explanations/cropped/111-1-醫學(五)-32_merged.png', read_img(136)[162:1170, 40:930])

# Q33: page 167 [168:480]
write_img('public/explanations/cropped/111-1-醫學(五)-33_merged.png', read_img(167)[168:480, 40:930])

# Q35: page 164 [168:1285]
write_img('public/explanations/cropped/111-1-醫學(五)-35_merged.png', read_img(164)[168:1285, 40:930])

print("Cropped images generated successfully")

EXPLANATIONS = {
    31: {
        "text": """#### 縱膈腔炎
| | 急性縱膈腔炎 | 慢性縱膈腔炎 (包含硬化性或纖維性縱膈腔炎) |
| :--- | :--- | :--- |
| 成因 | • 食道破裂<br>• 胸骨感染<br>• 口咽或頸部感染、頸部蜂窩組織炎或化膿性淋巴結炎<br>• 口腔底蜂窩組織炎 (Ludwig's angina)<br>• 扁桃腺炎<br>• 咽後膿瘍 (retropharyngeal abscess)<br>• 肺部或肋膜發炎、膈下膿瘍 (subphrenic abscess)<br>• 肋骨或脊椎骨髓炎<br>• 齒齦發炎<br>• 血源性 (hematogenous) 或轉移性膿瘍 | 慢性淋巴結炎所致的縱膈腔慢性發炎最終可能造成硬化性或纖維性縱膈腔炎，而慢性淋巴結炎可能由組織胞漿菌病 (histoplasmosis) 或肺結核導致的肉芽腫感染所致 |
| 處置 | • 安排 CT，了解影響範圍，並且可作為引流的導引工具<br>• 急性縱膈腔炎需進行緊急手術，盡快解決導致縱膈腔炎的成因<br>• 另需輸液、給抗生素以及根據病人情況決定是否進行清創 | • 沒有最佳的處置方法<br>• 手術僅適合用以診斷、緩解呼吸道或食道阻塞、重建血管<br>• 在某些研究中顯示，Ketoconazole 有助於控制疾病進展 |

*(整理自 2019 Schwartz's Principles of Surgery Chapter 19)*

(D) 急性縱膈腔炎需進行緊急手術解決 underlying，不可只給抗生素作為唯一治療手段""",
        "image": "/explanations/cropped/111-1-醫學(五)-31_merged.png"
    },
    32: {
        "text": """| 首要步驟：評估呼吸道、呼吸、循環 (ABC: airway, breathing, circulation) | 狀況 | 處置與檢查 | 後續處置 |
| :--- | :--- | :--- | :--- |
| | 狀況穩定 | PE 及胸部 X 光排除氣胸 / 血胸<br>• 若為氣胸 / 血胸 → 執行胸腔引流 (tube thoracostomy)，之後進入右述步驟<br>• 若否，直接進入右述步驟 | 確認受傷位置是否會進入心臟處或穿過縱膈腔<br>• 若有，安排心臟超音波、胸部電腦斷層血管攝影、支氣管鏡、食道攝影進行評估 **<br>• 若否，且病人有插胸管，則監測引流量 |
| | 狀況不穩 | 啟動急救復甦 (resuscitation)、PE<br>→呼吸音變小聲則胸腔引流→監測引流量是否 ≥1500 mL | • 引流量 <1500 mL 則掃 FAST sono → 沒有異常發現則監控病人對急救復甦有無反應→有反應則監測引流量並考慮是否進行縱膈腔評估<br>• 引流量 ≥1500 mL、FAST sono 發現異常、病人對急救復甦無反應都須考慮進行緊急手術 |
| | 心跳停止 | 進行緊急手術 | |

*(整理自 Sabiston Chapter 17 - figure17.16: Algorithm for the management of penetrating thoracic injuries)*

** 若進行心臟與縱膈腔評估後，發現有如下列的緊急狀況，也須給予相應處置：
• 心包膜填塞 (cardiact tamponade)
→盡快做心包膜腔穿刺 (pericardiocentesis)，清除積液以減少對心臟的壓迫
• 大血管損傷→緊急手術
• 食道破裂→清除致污物、引流、控制感染源 (放置食道支架、修補食道破裂處)
(食道破裂題目可見於 111-2 第 25 題)""",
        "image": "/explanations/cropped/111-1-醫學(五)-32_merged.png"
    },
    33: {
        "text": """(A) 根據 NCCN guideline，早期為侵犯周邊淋巴結的小細胞肺癌也建議以肺葉切除術 (lobectomy) 及縱膈腔淋巴結取樣或切除作為一線治療方法

(B) 早期肺癌若有侵犯周邊淋巴結，在術後還是會建議加做化療

(D) 若遠端轉移僅有腦部一處，可做立體定位放射手術 (stereotactic radiosurgery, SRS)，且可根據病人狀況 (病人症狀、作為診斷手段) 做肺部腫瘤切除""",
        "image": "/explanations/cropped/111-1-醫學(五)-33_merged.png"
    },
    34: {
        "text": "缺頁",
        "image": None
    },
    35: {
        "text": """#### Esophageal cancer TNM staging
| 分類 | 代號 | 定義 |
| :--- | :--- | :--- |
| T: primary tumor | Tx | 腫瘤無法評估 |
| | T0 | 沒有證據顯示有腫瘤 |
| | Tis | 高度分化異常 (high grade dysplasia) |
| | T1a | 侵犯 lamina propria 或 muscularis mucosa |
| | T1b | 侵犯 submucosa |
| | T2 | 侵犯到但不超過 muscularis propria |
| | T3 | 侵犯 adventitia |
| | T4a | 侵犯周邊通常可被切除的構造 (橫膈、肋膜、奇靜脈、腹膜、心包膜) |
| | T4b | 侵犯周邊通常不可被切除的構造 (主動脈、椎體、氣管) |
| N: regional lymph nodes | Nx | 局部淋巴結無法評估 |
| | N0 | 沒有侵犯到局部淋巴結 |
| | N1 | 侵犯 1~2 個局部淋巴結 |
| | N2 | 侵犯 3~6 個局部淋巴結 |
| | N3 | 侵犯 ≥ 7 個局部淋巴結 |
| M: distant metastasis | M0 | 沒有遠端轉移 |
| | M1 | 有遠端轉移 |
| G: histologic grade | Gx | 無法評估組織學等級 |
| | G1 | 高度分化 (well differentiated) |
| | G2 | 中度分化 |
| | G3 | 低度分化或未分化 (poorly differentiated or undifferentiated) |
| L: location (只適用於 squamous cell carcinoma) | Lx | 不明位置 |
| | Upper | 頸段食道 (cervical esophagus) 到奇靜脈 (azygos vein) 下緣 |
| | Middle | 奇靜脈下緣到下肺靜脈 (inferior pulmonary vein) 下緣 |
| | Lower | 下肺靜脈下緣到胃 (包含食道 - 胃接合處) |""",
        "image": "/explanations/cropped/111-1-醫學(五)-35_merged.png"
    },
    36: {
        "text": "缺頁",
        "image": None
    },
    37: {
        "text": "缺頁",
        "image": None
    },
    38: {
        "text": "缺頁",
        "image": None
    },
    39: {
        "text": "缺頁",
        "image": None
    },
    40: {
        "text": "缺頁",
        "image": None
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

    print("All Q31-Q40 explanation texts and images passed validation")

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

    print("Successfully finished updating Q31-Q40")

if __name__ == "__main__":
    main()
