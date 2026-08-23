import os
import sys
import re
import json
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

# 自動安裝依賴套件 pypdf
try:
    import pypdf
except ImportError:
    print("正在自動為您安裝 pypdf 套件...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pypdf"])
    import pypdf

# 檔案路徑定義
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
pdf_path = os.path.join(script_dir, "exam.pdf")
json_path = os.path.join(project_dir, "src", "data", "questions.json")

print("--- 醫師國考二階題目自動導入系統 ---")

if not os.path.exists(pdf_path):
    print(f"錯誤：找不到考試 PDF 檔案。")
    print(f"請下載 113年第一次 醫學(五) 官方考卷，將其命名為 exam.pdf 並存放在以下位置：")
    print(f"   {pdf_path}")
    print("請放入 PDF 檔案後重新執行此腳本")
    sys.exit(1)

if not os.path.exists(json_path):
    print(f"錯誤：找不到專案的 questions.json 檔案，請確認專案路徑正確")
    sys.exit(1)

# 1. 讀取 PDF 文字
print("1. 正在讀取 PDF 檔案內容...")
reader = pypdf.PdfReader(pdf_path)
full_text = ""
for page_idx, page in enumerate(reader.pages):
    text = page.extract_text()
    if text:
        full_text += text + "\n"

print(f"   成功提取 {len(reader.pages)} 頁，共 {len(full_text)} 個字元")

# 2. 解析考卷題目
# 國考題目的特徵通常是: "\n41 關於..." 或 "\n41. 關於..." 
# 選項特徵通常是: "(A)... (B)... (C)... (D)..."
print("2. 正在解析試卷題目與選項...")

# 我們將全文按行拆分，並進行狀態機掃描
lines = full_text.split("\n")
raw_questions = {} # { pdf_q_num: { text: "", options: [] } }
current_q_num = None
current_q_text = []
current_options = []

# 匹配題號開頭，例如 "41 " 或是 "41."
q_start_pattern = re.compile(r"^(\d+)[\s\.\、](.*)$")
# 匹配選項，例如 "(A)", "(B)", "(C)", "(D)"
opt_pattern = re.compile(r"\(([A-D])\)\s*([^(\n]+)")

for line in lines:
    line_stripped = line.strip()
    if not line_stripped:
        continue
        
    # 檢查是否為新題目的開始
    match_q = q_start_pattern.match(line_stripped)
    if match_q:
        # 保存上一題
        if current_q_num is not None:
            raw_questions[current_q_num] = {
                "text": " ".join(current_q_text).strip(),
                "options": current_options
            }
            
        current_q_num = int(match_q.group(1))
        current_q_text = [match_q.group(2).strip()]
        current_options = []
        continue
        
    if current_q_num is not None:
        # 檢查該行是否包含選項
        opts_in_line = opt_pattern.findall(line_stripped)
        if opts_in_line:
            # 如果這行含有選項，我們將其加入選項列表
            for letter, content in opts_in_line:
                current_options.append(f"{letter}. {content.strip()}")
        else:
            # 如果沒有選項，且這行不是新題目，則屬於題目內文
            # 如果還沒有選項，就加到題目文字；如果已經有選項，則可能是選項的換行
            if not current_options:
                current_q_text.append(line_stripped)
            else:
                # 選項的補充說明
                if current_options:
                    current_options[-1] += " " + line_stripped

# 保存最後一題
if current_q_num is not None:
    raw_questions[current_q_num] = {
        "text": " ".join(current_q_text).strip(),
        "options": current_options
    }

print(f"   共解析出 {len(raw_questions)} 題題目")

# 3. 讀取現有的 questions.json
with open(json_path, "r", encoding="utf-8") as f:
    questions_db = json.load(f)

# 4. 進行題目與詳解的智能配對
# 我們知道這 64 題詳解對應的正確答案
# 對於 questions.json 中的每一題 (1 到 64)：
# 我們在其正確答案符合的 PDF 題目中，計算文字與詳解的關鍵字重合度
print("3. 正在進行題目與共筆詳解的智能配對...")

matched_count = 0
for db_q in questions_db:
    db_id = db_q["id"]
    correct_ans = db_q["correctAnswer"]
    expl_text = db_q["explanation"].lower()
    
    # 提取詳解中的專有名詞與關鍵字 (中文詞組與英文字)
    # 我們把詳解中大於 2 個字的英文字以及中文名詞作為關鍵字
    keywords = set(re.findall(r'[a-zA-Z]{3,}', expl_text))
    # 簡單切分中文詞
    chinese_words = re.findall(r'[\u4e00-\u9fa5]{2,4}', expl_text)
    keywords.update(chinese_words[:15]) # 拿前 15 個中文字組
    
    best_match_qnum = None
    best_score = -1
    
    # 在所有解析出的 PDF 題目中尋找匹配
    for pdf_qnum, pdf_data in raw_questions.items():
        # 如果 PDF 解析出的選項小於 4 個，可能解析不完整，但我們仍可以配對
        # 計算重疊度
        pdf_q_full = (pdf_data["text"] + " ".join(pdf_data["options"])).lower()
        
        score = 0
        for kw in keywords:
            if kw in pdf_q_full:
                score += 1
                
        if score > best_score:
            best_score = score
            best_match_qnum = pdf_qnum
            
    # 如果找到了足夠好的匹配 (重合度得分 > 2)
    if best_score > 2 and best_match_qnum is not None:
        matched_pdf = raw_questions[best_match_qnum]
        
        # 覆寫題目與選項
        db_q["questionText"] = f"【第 {db_id} 題】(國考第 {best_match_qnum} 題) {matched_pdf['text']}"
        
        # 如果 PDF 的選項解析完整，就使用 PDF 的選項，否則保留原樣
        if len(matched_pdf["options"]) >= 4:
            db_q["options"] = matched_pdf["options"][:4]
        
        matched_count += 1
        # 從待匹配池中移除已配對的 PDF 題，防止重複配對
        del raw_questions[best_match_qnum]

print(f"   智能配對完成，成功導入 {matched_count} / {len(questions_db)} 題題目與選項")

# 5. 寫回 json 檔案
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(questions_db, f, ensure_ascii=False, indent=2)

print(f"4. 已成功更新專案題目資料庫：{json_path}")
print("--- 導入程序順利結束 ---")
