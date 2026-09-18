# -*- coding: utf-8 -*-
import json
import os
import cv2
import numpy as np

def read_img(p):
    return cv2.imdecode(np.fromfile(f\'scratch/pages_2022/page_{p}.jpg\', dtype=np.uint8), cv2.IMREAD_COLOR)

def write_img(path, img):
    ext = os.path.splitext(path)[1]
    res, buf = cv2.imencode(ext, img)
    with open(path, \'wb\') as f:
        f.write(buf)

os.makedirs(\'public/explanations/cropped\', exist_ok=True)

# 1. Image Cropping
# Q61: page 393 [985:1310] + page 394 [145:505]
p393_q61 = read_img(393)[985:1310, 40:930]
p394_q61 = read_img(394)[145:505, 40:930]
write_img(\'public/explanations/cropped/111-1-醫學(五)-61_merged.png\', np.vstack([p393_q61, p394_q61]))

# Q62: page 394 [930:1310] + page 395 [130:800]
p394_q62 = read_img(394)[930:1310, 40:930]
p395_q62 = read_img(395)[130:800, 40:930]
write_img(\'public/explanations/cropped/111-1-醫學(五)-62_merged.png\', np.vstack([p394_q62, p395_q62]))

# Q63: page 396 [134:1310] + page 397 [140:715]
p396_q63 = read_img(396)[134:1310, 40:930]
p397_q63 = read_img(397)[140:715, 40:930]
write_img(\'public/explanations/cropped/111-1-醫學(五)-63_merged.png\', np.vstack([p396_q63, p397_q63]))

# Q64: page 407 [510:1200]
write_img(\'public/explanations/cropped/111-1-醫學(五)-64_merged.png\', read_img(407)[510:1200, 40:930])

# Q65: page 409 [930:1310] + page 410 [140:580]
p409_q65 = read_img(409)[930:1310, 40:930]
p410_q65 = read_img(410)[140:580, 40:930]
write_img(\'public/explanations/cropped/111-1-醫學(五)-65_merged.png\', np.vstack([p409_q65, p410_q65]))

# Q66: page 408 [340:1310]
write_img(\'public/explanations/cropped/111-1-醫學(五)-66_merged.png\', read_img(408)[340:1310, 40:930])

# Q67: page 409 [428:635]
write_img(\'public/explanations/cropped/111-1-醫學(五)-67_merged.png\', read_img(409)[428:635, 40:930])

# Q68: page 179 [335:935]
write_img(\'public/explanations/cropped/111-1-醫學(五)-68_merged.png\', read_img(179)[335:935, 40:930])

# Q69: page 410 [855:1310] + page 411 [140:990]
p410_q69 = read_img(410)[855:1310, 40:930]
p411_q69 = read_img(411)[140:990, 40:930]
write_img(\'public/explanations/cropped/111-1-醫學(五)-69_merged.png\', np.vstack([p410_q69, p411_q69]))

# Q70: page 412 [134:805]
write_img(\'public/explanations/cropped/111-1-醫學(五)-70_merged.png\', read_img(412)[134:805, 40:930])

print(\'Cropped images generated successfully\')

EXPLANATIONS = {
    61: {
        \'text\': \'\'\'遠端橈尺關節炎 (distal radioulnar joint arthritis = DRUJ arthritis) 時，通常手腕背側會疼痛，且手腕旋轉會有困難，手握拳的力量也會降低

(A) Darrach procedure 為透過去除尺骨頭端 (ulnar head) 緩解橈尺骨關節疼痛或改善其不穩定的狀況；由於會影響手腕活動，通常用於日後手腕活動量不高的老年人

(B) hemi-resection arthroplasty 為切除尺骨頭端，但保有骨幹 (shaft) 和莖突 (styloid) 的手術，通常會在 Darrach procedure 前進行

(C) DRUJ 的穩定度主要由三角纖維軟骨複合體 (triangular fibrocartilage complex, TFCC) 所提供（TFCC 包括遠端橈尺骨韌帶、三角韌帶軟骨、尺側韌帶及掌尺韌帶）；Adam procedure 旨在藉由重建韌帶以保有 DRUJ 的活動與功能，但此術式不適用於 DRUJ arthritis 病人，因其若只進行韌帶重建仍無法緩解疼痛

(D) Sauvé-Kapandji procedure 包括遠端橈尺關節融合術與使用一限制型人工關節固定於尺骨頸 (ulnar neck)，術後多數病人的遠端橈尺關節疼痛可以得到改善，前臂的迴旋轉動也可以保留，但術後可能有尺骨殘段不穩定的問題\'\'\',
        \'image\': \'/explanations/cropped/111-1-醫學(五)-61_merged.png\'
    },
    62: {
        \'text\': \'\'\'化膿性脊椎感染可分為四大類：脊椎硬腦膜外囊腫 / 感染 (spinal epidural abscess/infection)、脊椎脊髓炎或椎間盤炎 (vertebral osteomyelitis/discitis)、敗血性脊椎面關節炎 (septic facet joint infection)、脊椎周邊構造感染（如肌肉或脊椎周邊膿瘍）

(A) 約有一半的化膿性脊椎感染發生於腰椎，其次為胸椎，僅約 1 成發生於頸椎

(B) 最常見的致病菌為金黃色葡萄球菌 (Staphylococcus aureus)，其次為 Streptococcus species

(C) 主要可由三種路徑發生感染，其中以血行性感染最為常見：

| 感染途徑 | 特徵 |
| :--- | :--- |
| 發源於遠端的血行性感染 (hematogenous spread from remote site) | • 椎體終板 (vertebral endplate) 最先被感染，之後再接續感染到臨近椎間盤或椎體<br>• 造成骨髓炎最常見的感染途徑 |
| 手術或外傷後直接感染 (direct external inoculation after trauma) | 可能源自於脊椎手術、椎間盤攝影術 (discography) 或脊椎處的穿刺傷 |
| 周邊組織感染後瀰散而來 (dissemination from contiguous tissue) | 原發感染源包括主動脈、食道、腸子 |

(D) 手術適應症包括：非手術治療無效、鑑別致病性微生物、有神經功能缺失 (neurologic deficit) 或脊椎不穩定 (spinal instability)、處於敗血症狀態、發現有脊髓管膿瘍 (spinal canal abscess)、脊椎周邊膿瘍 (paravertebral abscess)>2.5 cm 等

參考資料：
Tsantes AG, Papadopoulos DV, Vrioni G, Sioutis S, Sapkas G, Benzakour A, Benzakour T, Angelini A, Ruggieri P, Mavrogenis AF on behalf of the World Association against Infection in Orthopedics and Trauma (W.A.I.O.T.) Study Group on Bone and Joint Infection Definitions. Spinal Infections: An Update. Microorganisms. 2020; 8(4):476.\'\'\',
        \'image\': \'/explanations/cropped/111-1-醫學(五)-62_merged.png\'
    },
    63: {
        \'text\': \'\'\'Adams forward bending test（亞當前彎測試）為一種檢測脊椎側彎的檢查，作法為：請受試者前彎 90 度，兩手平肩下垂，醫師站在受試者身後與側面觀察背部外觀，若背部脊椎呈現側向彎曲或左右背部高度不一的情形則懷疑有脊椎側彎。脊椎側彎的確診仍須依靠 X 光，其中測量脊椎上方與下方最傾斜的椎體間之垂直線交叉所得角度稱為 Cobb angle，可藉此判定脊椎側彎的嚴重度

另外，醫師可藉骨盆 X 光判斷患者的 Risser grade，將長骨由外到內分為各 25% 的四個區域，依據腸骨生長板骨化情形分為 0~5 級，作為骨頭生長可能性的參考依據：

| | 生長板骨化程度 | 骨頭成熟度 | 脊椎側彎惡化可能性 | 備註 |
| :--- | :--- | :--- | :--- | :--- |
| Risser grade 0 | 尚未骨化 | X | 大<br>↓<br>↓<br>↓<br>↓<br>↓<br>↓<br>↓<br>小 | |
| Risser grade 1 | 0~25% | 剛發育<br>↓<br>↓<br>↓<br>↓<br>↓<br>發育成熟 | | |
| Risser grade 2 | 25~50% | | | 骨骼發育較完全且仍保有可塑性，較適合手術 |
| Risser grade 3 | 50~75% | | | |
| Risser grade 4 | 75~100% | | | |
| Risser grade 5 | 100% | | | |

青少年脊椎側彎後續處置方式如下：

| Cobb angle | Risser grade | 追蹤 / 轉診 | 治療 |
| :--- | :--- | :--- | :--- |
| 10°~19° | 0~1 | 每半年追蹤 X 光，不需轉診 | 觀察 |
| 10°~19° | 2~4 | | |
| 20°~29° | 0~1 | 每半年追蹤 X 光，轉診至骨科或復健科 | 穿戴背架 |
| 20°~29° | 2~4 | | • Risser grade 4：觀察<br>• 其他：穿戴背架 |
| 29°~40° | 0~1 | 轉診至骨科或復健科 | 穿戴背架，部分手術治療 |
| 29°~40° | 2~4 | | 穿戴背架 |
| >40° | 0~4 | | 手術治療 |

根據上表可知，Cobb angle 45°、Risser grade 2、已來月經的國一女生應進行手術。手術方式以後側骨融合手術最常見，乃利用鋼條 (rods)、螺釘 (screw)、脊椎鉤 (hooks)、鋼圈 (wire) 放置在脊椎內導正脊椎，再由患者身上取出一部份骨頭（大部份取自骨盆的髂骨）安置在脊椎骨頭之間使之相互融合，變成一整塊骨頭，形成穩固的結構

(D) 前側椎體間骨融合 (anterior interbody fusion) 因可預防曲軸現象 (crankshaft phenomenon)，故較適合骨骼發育尚不成熟的青少年。但以現今技術而言，大多狀況都可藉由後側融合手術進行處理，無需合併前測融合手術\'\'\',
        \'image\': \'/explanations/cropped/111-1-醫學(五)-63_merged.png\'
    },
    64: {
        \'text\': \'\'\'尿路結石的形成大致可分為幾個階段：

| 晶體成核 (nucleation) | 尿液中的溶質濃度增加，超過溶解度時，形成結晶 |
| :--- | :--- |
| 晶體生長 (growth) | 飽和尿液中的離子不斷沉積到晶核的表面，結合到晶格中，使晶體逐漸長大 |
| 晶體聚集 (aggregation) | 尿中的結晶相互聚集成更大的晶體顆粒簇 |
| 晶體滯留 (retention) | |

其中，促進及抑制結晶生成的物質分別如下：

| 促進因子<br>(promoter) | • 尿液容積小、尿液 pH 值低：身體缺水、尿酸、尿濃較易形成結石<br>• 鈣、鈉<br>• 草酸 (oxalate)、尿酸 (uric acid)、胱胺酸 (cystine)<br>• 基質 (matrix)：可作為輔助結晶結合的物質 (binding agent) |
| :--- | :--- |
| 抑制因子<br>(inhibitor) | • 鎂、檸檬酸 (citrate)、焦磷酸 (pyrophosphate)<br>• 糖氨聚醣 (glycosaminoglycan)<br>• 腎鈣素 (nephrocalcin)、尿橋蛋白 (uropontin) |\'\'\',
        \'image\': \'/explanations/cropped/111-1-醫學(五)-64_merged.png\'
    },
    65: {
        \'text\': \'\'\'膀胱癌依照是否侵犯逼尿肌可分為非肌肉侵犯型 (nonmuscle invasive bladder cancer, NMIBC) 及肌肉侵犯型 (muscle invasive bladder cancer, MIBC)，其中約 70% 為 NMIBC

(A) 可能有一半的病人在接受膀胱根除手術 (radical cystectomy) 後在 2 年內仍會發生復發或轉移

(B) 標準治療應為術前化療後再進行膀胱根除手術

(D) 膀胱根除性切除後，膀胱重建的方式主要包括迴腸導管尿路改道術 (ileal conduit) 及原位新膀胱重建術 (orthotopic neobladder)：

| | 迴腸導管尿路改道術 | 原位新膀胱重建術 |
| :--- | :--- | :--- |
| 作法 | 取一段約 15~20 cm 的迴腸，一端接於輸尿管，另一端拉到腹壁上做成一個造廔口使尿液由此排出 | 取一段約 60 cm 的小腸塑形成球狀，與尿道與輸尿管相接成為儲存尿液的人工膀胱 |
| 特徵 | • 手術簡單，但不美觀<br>• 病人需長期貼附集尿袋收集尿液，且不可憋尿 | • 術後病人需透過腹壓訓練練習排空膀胱<br>• 可像正常人一樣排尿，但可能有失禁、排不乾淨的情況 |
| 適用對象 | • 腎功能不全者（腎功能不全為原味新膀胱重建術的禁忌症） | • 可承受較長手術時間者<br>• 自身照顧能力、行動能力佳者 |\'\'\',
        \'image\': \'/explanations/cropped/111-1-醫學(五)-65_merged.png\'
    },
    66: {
        \'text\': \'\'\'睪丸癌好發於 20~40 歲男性。患者起初的主訴常為無痛睪丸腫塊，有時也可能直接出現轉移後產生的症狀，如下背痛、腹部腫塊、呼吸喘、咳血等。發現有無痛睪丸腫塊的病人，一線診斷工具為超音波，並且可抽一些腫瘤指標初步判定可能為保種睪丸癌。最常見的睪丸癌為生殖細胞瘤 (germ cell tumor, GCT)，又可依病理型態分為精細胞瘤 (seminomatous GCT, SGCT = seminoma) 及非精細胞瘤 (non-SGCT, NSGCT) 兩大類

| | | AFP | β-HCG |
| :--- | :--- | :--- | :--- |
| 精原細胞瘤 | | 正常 | 可能 ↑ |
| NSGCT | yolk sac tumor | ↑ ↑ ↑ | 正常 |
| | choriocarcinoma | 正常 | ↑ ↑ ↑ |
| | embryonal carcinoma | ↑ | ↑ |
| | teratoma | 正常 | 正常 |

(A) 睪丸癌的危險因子：隱睪症、睪丸癌家族史、睪丸切片發現 intratubular germ cell neoplasia（為一種癌前病灶，5 年內轉為睪丸癌的機率可高達 50%）

(B) 生殖細胞瘤佔睪丸癌的 95% 左右，其餘主要為性腺間質瘤

(C) 絨毛膜癌早期便容易透過血行轉移到遠端器官；常見的睪丸癌遠端轉移器官包括肺臟、肝臟、腦、骨頭、腎臟、腎上腺

(D) 睪丸癌的淋巴轉移通常從後腹腔淋巴開始，並會跳過腹股溝及骨盆腔淋巴腺

參考資料：Sabiston Textbook of Surgery: The Biological Basis of Modern Surgical Basis (2021). Chapter 74\'\'\',
        \'image\': \'/explanations/cropped/111-1-醫學(五)-66_merged.png\'
    },
    67: {
        \'text\': \'\'\'張先生有明顯的下泌尿道症狀，且肛門指診發現前列腺肥大，可做尿液常規檢查判斷是否為泌尿道感染所致，亦可安排前列腺特定抗原檢測判斷是否有攝護腺癌的可能。由於題目要選的是「最不需要立即進行」的檢查，因此選擇相對較與該敘述鑑別診斷相關性較低的 (A) 和 (B)\'\'\',
        \'image\': \'/explanations/cropped/111-1-醫學(五)-67_merged.png\'
    },
    68: {
        \'text\': \'\'\'| 排尿<br>(micturition) | T11~L2 交感<br>hypogastric nerve | 向膀胱輸出抑制性訊號，使得膀胱放鬆、尿道外括約肌收縮而抑制排尿 |
| :--- | :--- | :--- |
| | S2~S4 副交感<br>pelvic nerve | 向膀胱輸出刺激性訊號，使得膀胱收縮而排尿 |
| | S2~S4 體神經<br>pudendal nerve | 抑制外括約肌收縮，促進排尿 |

當膀胱反射開始收縮時，膀胱頸與尿道後段平滑肌會在交感神經與副交感神經間的協調下放鬆，促進排尿；當要終止排尿時，交感神經會對逼尿肌核產生抑制作用，使膀胱停止收縮、膀胱頸關閉

排尿的控制中樞位於橋腦、膀胱的反射中樞位於 S2~S4

若排尿反射中樞 (S2~S4) 以上的地方有脊髓損傷或病變，使神經訊號傳導產生中斷，就會導致排尿時逼尿肌與尿道外括約肌共濟失調，或產生交感神經反射亢進的現象

由上述可知，在 S2~S4 以上的脊髓完全損傷均會造成逼尿肌反射亢進，故此題選 (D)\'\'\',
        \'image\': \'/explanations/cropped/111-1-醫學(五)-68_merged.png\'
    },
    69: {
        \'text\': \'\'\'### Diagnostic Approach to UTI

| 臨床表現 | 病患特徵 | 可能診斷 |
| :--- | :--- | :--- |
| 急性泌尿道症狀<br>(小便疼痛、急尿、頻尿) | 健康未懷孕女性 | 非複雜性膀胱炎<br>(uncomplicated cystitis) |
| | 有性傳染病病史或高風險的女性 | 非複雜性膀胱炎或性傳染病 |
| | 會陰、骨盆或攝護腺疼痛的男性 | 急性攝護腺炎<br>(acute prostatitis) |
| | 置留有導尿管的病人 | 導尿管相關泌尿道感染<br>(catheter-associated UTI) |
| | 其他 | 複雜性 UTI |
| 急性背痛、噁心嘔吐或發燒 | 健康未懷孕女性 | 非複雜性腎盂腎炎<br>(pyelonephritis) |
| | 其他 | 腎盂腎炎、攝護腺炎 |
| 全身性症狀<br>(發燒、意識改變、白血球增多) | 年長者、脊髓損傷患者、免疫低下患者、排除其他診斷 | 複雜性 UTI |
| 沒有相關泌尿道症狀 | 以下族群且尿液培養 (+)：孕婦、接受過腎臟移植、近期做侵入性泌尿道處置 | 無症狀菌尿症 (asymptomatic bacteriuria, ASB) |
| | 置留有導尿管的病人且尿液培養 (+) | 導尿管相關無症狀菌尿症<br>(catheter-associated ASB) |
| | 其他族群且尿液培養 (+) | 無症狀菌尿症 |
| 反覆急性泌尿道症狀 | 健康未懷孕女性 | 反覆性膀胱炎 |
| | 男性 | 慢性細菌性攝護腺炎 |

（整理自 Harrison 20th ed. Chapter 130）

(A) 長達一個月的無痛性血尿，有可能為泌尿道癌症所致

(B) 左腰急性絞痛合併血尿，很可能為腎結石所致

(C) 停經婦女出現無痛性血尿及血塊排出，除了考慮泌尿道癌症外，還需排除婦科問題

(D) 除了有突發性血尿外，另有泌尿道感染常見的泌尿道症狀，相較上述幾個選項，有更高的機會是由尿路感染所致\'\'\',
        \'image\': \'/explanations/cropped/111-1-醫學(五)-69_merged.png\'
    },
    70: {
        \'text\': \'\'\'| | 急性副睪炎 | 睪丸扭轉 |
| :--- | :--- | :--- |
| 成因 | UTI 上行性經由輸精管造成副睪感染；35 歲前常為 Chlamydia trachomatis 感染（通常有性傳染病感染源）、35 歲後常為 E. coli 感染 | 提睪肌將睪丸提高、扭轉，精索受扭轉後，其內的血管會受到阻斷，為一急症 |
| 臨床表現 | • 發病突然<br>• 副睪或陰囊紅腫熱痛，常合併發燒<br>• 泌尿道症狀、常見膿尿<br>• 將陰囊捧起可減緩疼痛<br>⇒ Prehn\'s sign positive<br>• 通常仍有提睪反射 (cremasteric reflex) | • 症狀逐漸加重<br>• 噁心嘔吐、紅腫痛<br>• 將陰囊捧起疼痛加劇<br>⇒ Prehn\'s sign negative<br>• 提睪反射 (cremasteric reflex) 下降或消失<br>• 外觀：橫躺如鐘擺 (bell-clapper deformity)、睪丸位置上縮 |
| 影像 | Doppler 超音波下血流增加 | Doppler 超音波下血流減少 |
| 治療 | • 陰囊抬高、冰敷<br>• 藥物：NSAID 止痛、抗生素 | • 盡快（4~6 hr 內）進行陰囊探查手術，將睪丸復位；復位後視情況進行睪丸固定術 (orchiopexy)<br>• 若延誤就醫，睪丸已缺血壞死，須切除壞死睪丸 |

* 提睪反射：觸摸大腿皮膚上方，會使得同側提睪肌收縮\'\'\',
        \'image\': \'/explanations/cropped/111-1-醫學(五)-70_merged.png\'
    }
}

# Check trailing periods rule
period_violations = []
for qnum, item in EXPLANATIONS.items():
    text = item[\'text\']
    for line_idx, line in enumerate(text.split(\'\n\'), 1):
        line = line.strip()
        if line.endswith(\'。\'):
            period_violations.append((qnum, line_idx, line))

if period_violations:
    print(\'ERROR: Trailing periods found:\')
    for v in period_violations:
        print(f\'  Q{v[0]} L{v[1]}: {v[2]}\')
    exit(1)
else:
    print(\'Zero trailing periods verified\')

# Check image paths exist
for qnum, item in EXPLANATIONS.items():
    img_path = item[\'image\']
    if img_path:
        local_path = \'public\' + img_path
        if not os.path.exists(local_path):
            print(f\'ERROR: Image not found on disk: {local_path}\')
            exit(1)

print(\'All referenced images exist on disk\')

# 2. Update questions.json
with open(\'src/data/questions.json\', \'r\', encoding=\'utf-8\') as f:
    questions = json.load(f)

updated_q_count = 0
for q in questions:
    qid = q.get(\'id\', \'\')
    if \'111-1\' in qid and \'醫學(五)\' in qid:
        num = int(q.get(\'number\', 0))
        if num in EXPLANATIONS:
            q[\'explanation\'] = EXPLANATIONS[num][\'text\']
            q[\'explanation_image\'] = EXPLANATIONS[num][\'image\']
            updated_q_count += 1

with open(\'src/data/questions.json\', \'w\', encoding=\'utf-8\') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f\'Updated {updated_q_count} questions in questions.json\')

# 3. Update explanations_map.json
with open(\'src/data/explanations_map.json\', \'r\', encoding=\'utf-8\') as f:
    exp_map = json.load(f)

for num, data in EXPLANATIONS.items():
    key = f\'111-1-醫學(五)-{num}\'
    exp_map[key] = {
        \'text\': data[\'text\'],
        \'image\': data[\'image\']
    }

with open(\'src/data/explanations_map.json\', \'w\', encoding=\'utf-8\') as f:
    json.dump(exp_map, f, ensure_ascii=False, indent=2)

print(\'Updated explanations_map.json with Q61-Q70\')
