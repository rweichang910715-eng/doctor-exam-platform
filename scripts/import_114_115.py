import fitz, os, sys, re, json
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\yuwei\Desktop\歷屆試題'
years = ['114-1', '114-2', '115-1', '115-2']
subjects = ['醫學(三)', '醫學(四)', '醫學(五)', '醫學(六)']
json_path = 'src/data/questions.json'

def parse_answer_pdf(ans_path, mod_path=None):
    ans_doc = fitz.open(ans_path)
    ans_dict = {}
    note_dict = {}
    
    page = ans_doc[0]
    tables = page.find_tables().tables
    
    for t in tables:
        rows = t.extract()
        if len(rows) >= 2:
            for h, v in zip(rows[0], rows[1]):
                if h and re.match(r'^\d+$', str(h).strip()):
                    qnum = int(str(h).strip())
                    v_str = str(v).strip() if v else ''
                    ans_dict[qnum] = v_str
                    
    fw_map = {'Ａ': 'A', 'Ｂ': 'B', 'Ｃ': 'C', 'Ｄ': 'D', '＃': '#'}
    for qnum in ans_dict:
        val = ans_dict[qnum]
        ans_dict[qnum] = fw_map.get(val, val)
        
    if mod_path and os.path.exists(mod_path):
        mod_doc = fitz.open(mod_path)
        mod_page = mod_doc[0]
        mod_text = mod_page.get_text()
        
        mod_tables = mod_page.find_tables().tables
        for t in mod_tables:
            rows = t.extract()
            if len(rows) >= 2:
                for h, v in zip(rows[0], rows[1]):
                    if h and re.match(r'^\d+$', str(h).strip()):
                        qnum = int(str(h).strip())
                        v_str = str(v).strip() if v else ''
                        v_char = fw_map.get(v_str, v_str)
                        if v_char and v_char != '#':
                            ans_dict[qnum] = v_char

        rem_match = re.search(r'備\s*註\s*[:：](.*)', mod_text, re.DOTALL)
        if rem_match:
            remarks = rem_match.group(1).replace('\n', '').strip()
            matches = re.finditer(r'第\s*(\d+)\s*題\s*([，,、]?[^第]+)', remarks)
            for m in matches:
                qnum = int(m.group(1))
                content = m.group(2).strip().lstrip('，,、').rstrip('，；;,')
                note_dict[qnum] = f"考選部更正：{content}"
                if '一律給分' in content or '其餘均給分' in content:
                    ans_dict[qnum] = 'ALL'
                elif '答' in content and '均給分' in content:
                    letters = set()
                    ans_seg_match = re.search(r'答\s*([^者]+)\s*者均給分', content)
                    target_seg = ans_seg_match.group(1) if ans_seg_match else content
                    for ch in target_seg:
                        if ch in ['Ａ', 'A']: letters.add('A')
                        if ch in ['Ｂ', 'B']: letters.add('B')
                        if ch in ['Ｃ', 'C']: letters.add('C')
                        if ch in ['Ｄ', 'D']: letters.add('D')
                    if letters:
                        ans_dict[qnum] = ','.join(sorted(list(letters)))
                    else:
                        ans_dict[qnum] = 'ALL'
                elif '更正為' in content:
                    m_ans = re.search(r'更正為\s*([Ａ-ＤA-D])', content)
                    if m_ans:
                        ans_dict[qnum] = fw_map.get(m_ans.group(1), m_ans.group(1))

    return ans_dict, note_dict

def extract_exam_data(pdf_path):
    doc = fitz.open(pdf_path)
    items = []
    
    for pno in range(len(doc)):
        page = doc[pno]
        page_h = page.rect.height
        blocks = page.get_text("blocks")
        for b in blocks:
            x0, y0, x1, y1, text, bno, btype = b
            if btype == 0:
                t = text.strip()
                if not t: continue
                if pno == 0 and ('專門職業及技術人員' in t or '代  號：' in t or '類科名稱：' in t or '科目名稱：' in t or '考試時間：' in t or '座號：' in t or '禁止使用電子計算器' in t or '單一選擇題' in t):
                    continue
                if y0 < 35 and ('代號：' in t or '頁次：' in t or '類科：' in t or '科目：' in t):
                    continue
                if y1 > page_h - 35 and ('頁次：' in t or re.match(r'^\d+\s*-\s*\d+$', t)):
                    continue
                items.append({
                    'type': 'text',
                    'page': pno,
                    'y0': y0,
                    'x0': x0,
                    'text': t
                })
                
        img_list = page.get_images()
        for idx, img_info in enumerate(img_list):
            xref = img_info[0]
            rects = page.get_image_rects(xref)
            rect = rects[0] if rects else fitz.Rect(0, 0, 100, 100)
            items.append({
                'type': 'image',
                'page': pno,
                'y0': rect.y0,
                'x0': rect.x0,
                'rect': rect,
                'xref': xref,
                'img_idx': idx
            })
            
    items.sort(key=lambda it: (it['page'], it['y0'], it['x0']))
    
    questions = {}
    current_qnum = 0
    current_state = None
    
    q_start_re = re.compile(r'^\s*([1-9]\d?)\s*[\.、](.*)', re.DOTALL)
    opt_inline_re = re.compile(r'([A-D])\s*[\.、]\s*')
    
    for item in items:
        if item['type'] == 'image':
            if current_qnum > 0:
                if 'images' not in questions[current_qnum]:
                    questions[current_qnum]['images'] = []
                questions[current_qnum]['images'].append(item)
            continue
            
        lines = item['text'].split('\n')
        for line in lines:
            line_str = line.strip()
            if not line_str: continue
            
            m_q = q_start_re.match(line_str)
            if m_q and int(m_q.group(1)) == current_qnum + 1:
                current_qnum = int(m_q.group(1))
                questions[current_qnum] = {
                    'number': current_qnum,
                    'text': m_q.group(2).strip(),
                    'options': {},
                    'images': []
                }
                current_state = 'TEXT'
                continue
                
            if current_qnum > 0:
                m_opt = re.match(r'^([A-D])\s*[\.、]\s*(.*)$', line_str)
                if m_opt:
                    opt_letter = m_opt.group(1)
                    opt_val = m_opt.group(2).strip()
                    questions[current_qnum]['options'][opt_letter] = opt_val
                    current_state = f'OPT_{opt_letter}'
                else:
                    split_opts = list(opt_inline_re.finditer(line_str))
                    if split_opts and split_opts[0].start() == 0:
                        for i, sm in enumerate(split_opts):
                            letter = sm.group(1)
                            start_idx = sm.end()
                            end_idx = split_opts[i+1].start() if i + 1 < len(split_opts) else len(line_str)
                            val = line_str[start_idx:end_idx].strip()
                            questions[current_qnum]['options'][letter] = val
                            current_state = f'OPT_{letter}'
                    else:
                        if current_state == 'TEXT':
                            if questions[current_qnum]['text']:
                                questions[current_qnum]['text'] += '\n' + line_str
                            else:
                                questions[current_qnum]['text'] = line_str
                        elif current_state and current_state.startswith('OPT_'):
                            letter = current_state.split('_')[1]
                            questions[current_qnum]['options'][letter] = (questions[current_qnum]['options'].get(letter, '') + ' ' + line_str).strip()

    return questions

def classify_question(subj, num, text, options_text):
    full = text + " " + options_text
    
    if subj == '醫學(四)':
        if 1 <= num <= 35:
            return '第三篇 婦兒科', '小兒科'
        elif 36 <= num <= 44:
            return '第四篇 其他科', '皮膚科'
        elif 45 <= num <= 64:
            return '第一篇 內科學', '神經內科'
        else:
            if any(k in full for k in ['倫理', '自主', '知情同意', '告知後同意', '醫療法', '刑法']):
                return '第四篇 其他科', '醫學倫理與醫療決策'
            return '第四篇 其他科', '精神科'
            
    elif subj == '醫學(六)':
        if 1 <= num <= 10:
            return '第四篇 其他科', '麻醉科'
        elif 11 <= num <= 20:
            return '第四篇 其他科', '眼科'
        elif 21 <= num <= 30:
            return '第四篇 其他科', '耳鼻喉科'
        elif 31 <= num <= 65:
            return '第三篇 婦兒科', '婦產科'
        elif 66 <= num <= 75:
            return '第四篇 其他科', '復健科'
        else:
            return '第四篇 其他科', '醫學倫理與醫療決策'
            
    elif subj == '醫學(五)':
        if 51 <= num <= 65:
            return '第四篇 其他科', '骨科'
        elif 66 <= num <= 75:
            return '第四篇 其他科', '泌尿科'
        elif 76 <= num <= 80:
            if any(k in full for k in ['倫理', '自主', '同意書', '知情同意', '法律', '安寧']):
                return '第四篇 其他科', '醫學倫理與醫療決策'
            return '第二篇 外科學', '急診外傷科'
        else:
            if any(k in full for k in ['早產兒', '新生兒', '膽道閉鎖', '先天性巨結腸', '臍膨出', '腹壁裂', '肥厚性幽門', '腸套疊']):
                return '第二篇 外科學', '小兒外科'
            if any(k in full for k in ['移植', '排斥', '腦死', '器官捐贈', 'cyclosporine', 'tacrolimus']):
                return '第二篇 外科學', '移植科'
            if any(k in full for k in ['心臟', '主動脈', '瓣膜', '冠狀動脈', 'CABG', '體外循環', '心包', '心室', '心房', '主動脈剝離']):
                return '第二篇 外科學', '心臟外科'
            if any(k in full for k in ['肺癌', '氣胸', '食道', '縱膈腔', '胸腺', '胸部鈍傷', '血胸', '肋骨骨折', '氣管']):
                return '第二篇 外科學', '胸腔外科'
            if any(k in full for k in ['顱內', '硬腦膜', '腦出血', '腦瘤', '水腦', '脊髓', '椎間盤', '腦壓', '開顱', '動靜脈畸形', '動脈瘤破裂']):
                return '第二篇 外科學', '神經外科'
            if any(k in full for k in ['大腸', '直腸', '闌尾', '肛門', '結腸', '痔瘡', '憩室', '瘻管', '息肉']):
                return '第二篇 外科學', '大腸直腸科'
            if any(k in full for k in ['燒傷', '燙傷', '植皮', '皮瓣', '褥瘡', '顏面骨折', '顯微手術', '斷指', '黑素瘤']):
                return '第二篇 外科學', '整形外科'
            if any(k in full for k in ['創傷', '外傷', 'ATLS', '休克', '腹部鈍傷']):
                return '第二篇 外科學', '急診外傷科'
            if any(k in full for k in ['手術前', '術後', '無菌', '傷口癒合', '縫線', '外科感染', '止血', '水份電解質']):
                return '第二篇 外科學', '外科概論'
            return '第二篇 外科學', '一般外科'
            
    elif subj == '醫學(三)':
        if 74 <= num <= 80 or any(k in full for k in ['倫理', '自主', '知情同意', '安寧緩和', '病人自主權利法', '健保', '醫師法', '醫療法', '告知後同意']):
            if num >= 66:
                return '第四篇 其他科', '醫學倫理與醫療決策'
        if 66 <= num <= 75:
            if any(k in full for k in ['家醫', '預防醫學', '篩檢', '疫苗', '戒菸', '動機性晤談', '家庭評估', '老年', '安寧', '臨終', '緩和']):
                return '第四篇 其他科', '家庭醫學科'
            if num >= 74:
                return '第四篇 其他科', '醫學倫理與醫療決策'
            return '第四篇 其他科', '家庭醫學科'
        else:
            scores = {
                '心臟內科': sum(full.count(w) for w in ['心', '冠狀動脈', '心電圖', '心衰竭', '心律不整', '瓣膜', '高血壓', '昏厥', '主動脈', 'troponin', 'VT', 'AF', 'STEMI']),
                '胸腔內科': sum(full.count(w) for w in ['肺', '氣喘', 'COPD', '咳', '肋膜', '結核', '呼吸', '哮鳴', 'ARDS', '氣胸', '支氣管']),
                '肝膽腸胃科': sum(full.count(w) for w in ['肝', '胃', '腸', '膽', '胰', '食道', '腹水', '黃疸', '潰瘍', '消化', '內視鏡', '大便', '腹痛', '嘔吐']),
                '腎臟科': sum(full.count(w) for w in ['腎', '尿', '透析', '蛋白尿', '血尿', '肌酸酐', 'creatinine', '鉀', '鈉', '酸中毒', 'GFR', '水腫']),
                '新陳代謝科': sum(full.count(w) for w in ['糖尿病', '血糖', '甲狀腺', '胰島素', '副甲狀腺', '腎上腺', '骨質疏鬆', '腦下垂體', 'Cushing', 'TSH']),
                '血液腫瘤科': sum(full.count(w) for w in ['貧血', '白血病', '淋巴瘤', '骨髓', '血小板', '血紅素', '化學治療', '標靶', '癌', '腫瘤', '凝血', '出血']),
                '免疫風濕科': sum(full.count(w) for w in ['關節', '狼瘡', 'SLE', '自體免疫', '風濕', '痛風', '血管炎', '乾燥症', 'ANA', 'HLA-B27', '類風濕']),
                '感染科': sum(full.count(w) for w in ['感染', '菌', '抗生素', '發燒', '病毒', 'HIV', '黴菌', '蜂窩性組織炎', '敗血', '梅毒', '疫苗'])
            }
            best_cat = max(scores, key=scores.get)
            if scores[best_cat] > 0:
                return '第一篇 內科學', best_cat
            if 1 <= num <= 14: return '第一篇 內科學', '心臟內科'
            if 15 <= num <= 24: return '第一篇 內科學', '肝膽腸胃科'
            if 25 <= num <= 32: return '第一篇 內科學', '腎臟科'
            if 33 <= num <= 38: return '第一篇 內科學', '免疫風濕科'
            if 39 <= num <= 46: return '第一篇 內科學', '血液腫瘤科'
            if 47 <= num <= 54: return '第一篇 內科學', '胸腔內科'
            if 55 <= num <= 60: return '第一篇 內科學', '新陳代謝科'
            return '第一篇 內科學', '感染科'

print("=== 正在讀取現有 questions.json ===")
with open(json_path, 'r', encoding='utf-8') as f:
    questions_db = json.load(f)

print(f"現有題目總數：{len(questions_db)}")

# 檢查是否已有 114 或 115 考題，若有先過濾以防重複
existing_ids = set(q['id'] for q in questions_db)
new_questions = []

for y in years:
    yp = os.path.join(base, y)
    files = os.listdir(yp)
    print(f"\n>>> 正在處理年度考期：{y} <<<")
    for s in subjects:
        q_f = [f for f in files if s in f and not 'ANS' in f and not 'MOD' in f and f.endswith('.pdf')][0]
        ans_f = [f for f in files if s in f and 'ANS' in f and f.endswith('.pdf')][0]
        mod_f = [f for f in files if s in f and 'MOD' in f and f.endswith('.pdf')]
        
        qp = os.path.join(yp, q_f)
        ans_p = os.path.join(yp, ans_f)
        mod_p = os.path.join(yp, mod_f[0]) if mod_f else None
        
        ans_dict, note_dict = parse_answer_pdf(ans_p, mod_p)
        raw_qs = extract_exam_data(qp)
        
        doc = fitz.open(qp)
        out_img_dir = f'public/images/{y}/{s}'
        os.makedirs(out_img_dir, exist_ok=True)
        
        exam_new_qs = []
        for num in range(1, 81):
            q_data = raw_qs.get(num)
            if not q_data:
                raise ValueError(f"CRITICAL: 找不到題目 {y} {s} Q{num}")
                
            ans_val = ans_dict.get(num, '')
            if not ans_val:
                raise ValueError(f"CRITICAL: 找不到答案 {y} {s} Q{num}")
                
            sec, chap = classify_question(s, num, q_data['text'], " ".join(q_data['options'].values()))
            
            # Save clinical images
            img_paths = []
            for img_it in q_data['images']:
                xref = img_it['xref']
                base_img = doc.extract_image(xref)
                ext = base_img['ext']
                fname = f"page_{img_it['page']+1}_img_{img_it['img_idx']+1}.{ext}"
                fpath = os.path.join(out_img_dir, fname)
                with open(fpath, 'wb') as f_img:
                    f_img.write(base_img['image'])
                img_paths.append(f"/images/{y}/{s}/{fname}")
                
            q_id = f"{y}-{s}-{num}"
            q_entry = {
                "id": q_id,
                "year": y,
                "subject": s,
                "number": num,
                "text": q_data['text'],
                "options": q_data['options'],
                "answer": ans_val,
                "explanation": "",
                "explanation_image": None,
                "explanation_images": None,
                "section": sec,
                "chapter": chap,
                "category": chap
            }
            if img_paths:
                q_entry["images"] = img_paths
            if num in note_dict:
                q_entry["note"] = note_dict[num]
                
            exam_new_qs.append(q_entry)
            
        print(f"  {s}: 成功解析 80 題，附圖題目共 {sum(1 for q in exam_new_qs if 'images' in q)} 題，更正答案共 {len([q for q in exam_new_qs if 'note' in q])} 題")
        new_questions.extend(exam_new_qs)

print(f"\n新題目總計生成：{len(new_questions)} 題")

# 合併回資料庫（移除舊的 114/115 避免重複導入）
clean_db = [q for q in questions_db if q.get('year') not in years]
merged_db = clean_db + new_questions

print(f"合併後題庫總題數：{len(merged_db)}")

# 驗證所有題目結構完整性
for idx, q in enumerate(merged_db):
    assert 'id' in q and q['id'], f"Q at index {idx} missing id"
    assert 'year' in q and q['year'], f"Q {q['id']} missing year"
    assert 'subject' in q and q['subject'], f"Q {q['id']} missing subject"
    assert 'number' in q and q['number'], f"Q {q['id']} missing number"
    assert 'text' in q and q['text'], f"Q {q['id']} missing text"
    assert 'options' in q and len(q['options']) == 4, f"Q {q['id']} does not have 4 options"
    assert 'answer' in q and q['answer'], f"Q {q['id']} missing answer"
    assert 'section' in q and q['section'], f"Q {q['id']} missing section"
    assert 'chapter' in q and q['chapter'], f"Q {q['id']} missing chapter"
    if 'images' in q:
        for p in q['images']:
            local_p = os.path.join('public', p.lstrip('/'))
            assert os.path.exists(local_p), f"Image file not found: {local_p}"

print("所有題目與附圖驗證通過！")

# 寫入 questions.json
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(merged_db, f, ensure_ascii=False, indent=2)

print(f"已成功寫入 {json_path}！")
