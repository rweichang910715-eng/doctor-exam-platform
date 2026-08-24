import React, { useState, useEffect } from 'react'
import questionsData from './data/questions.json'
import explanationsMap from './data/explanations_map.json'
import './App.css'

// Common non-medical English words list to exclude when matching English prefixes in disease search
const NON_MEDICAL_ENGLISH_WORDS = new Set([
  'appear', 'appears', 'appeared', 'appearing', 'appearance', 'appearances',
  'approach', 'approaches', 'approached', 'approaching',
  'appropriate', 'inappropriate', 'appropriateness', 'appropriately',
  'apply', 'applies', 'applied', 'applying', 'application', 'applications',
  'apparatus', 'apparatuses',
  'approximate', 'approximately', 'approximation',
  'apparent', 'apparently',
  'appetite', 'appraisal', 'approval', 'approve', 'approved',
  'applicable', 'applicability',
  'appendage', 'appendages'
])

const escapeRegExp = (string) => {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

// Map questions to medical subspecialties (腎臟內科, 胸腔內科, 心臟內科, etc.)
const getQuestionSubspecialty = (q) => {
  if (!q) return '一般臨床醫學'
  const sub = q.subject || ''
  const num = q.number || 0
  const fullText = [
    q.text || '',
    ...Object.values(q.options || {}),
    q.explanation || '',
    q.note || ''
  ].join(' ')

  if (sub === '醫學(三)') {
    if (num >= 69 || /倫理|自主權|病情告知|安寧|隱私|病人自主|同意書|beauchamp|倫理原則|安寧緩和/i.test(fullText)) {
      return '醫學倫理與法規'
    }
    if (num >= 56 && num <= 68 && /家醫|預防保健|疫苗|篩檢|社區|老人/i.test(fullText)) {
      return '家庭醫學科'
    }
    if (/腎|腎臟|kidney|renal|dialysis|透析|蛋白尿|egfr|creatinine|肌酸酐|尿毒|電解質|glomerular|腎小球|腎絲球/i.test(fullText)) {
      return '腎臟內科'
    }
    if (/胸腔|氣管|肺|copd|asthma|氣喘|肺炎|pneumonia|呼吸|cough|咳嗽|pleural|胸水|氣胸|abg|pao2/i.test(fullText)) {
      return '胸腔內科'
    }
    if (/心臟|心肌|心律|ecg|st段|高血壓|hypertension|心衰竭|cardiac|heart|murmur|心雜音|冠狀動脈|troponin|af|心房顫動/i.test(fullText)) {
      return '心臟內科'
    }
    if (/肝|胃|腸|膽|胰|hepatitis|cirrhosis|肝硬化|潰瘍|ulcer|ascites|腹水|黃疸|jaundice|內視鏡|gastro/i.test(fullText)) {
      return '腸胃肝膽科'
    }
    if (/糖尿病|diabetes|甲狀腺|thyroid|腎上腺|adrenal|副甲狀腺|hba1c|胰島素|insulin|cushing|aldosterone/i.test(fullText)) {
      return '內分泌新陳代謝科'
    }
    if (/貧血|anemia|白血病|leukemia|淋巴瘤|lymphoma|化療|chemotherapy|血小板|platelet|neutropenia/i.test(fullText)) {
      return '血液腫瘤科'
    }
    if (/sle|紅斑性狼瘡|類風濕|rheumatoid|lupus|痛風|gout|血管炎|vasculitis|scleroderma|硬皮症|ana|anti-dsdna/i.test(fullText)) {
      return '風濕免疫科'
    }
    if (/感染|敗血症|sepsis|發燒|fever|抗生素|antibiotic|hiv|愛滋|結核|tb|tuberculosis|fungal/i.test(fullText)) {
      return '感染科'
    }

    if (num <= 10) return '心臟內科'
    if (num <= 18) return '胸腔內科'
    if (num <= 26) return '腸胃肝膽科'
    if (num <= 34) return '腎臟內科'
    if (num <= 40) return '內分泌新陳代謝科'
    if (num <= 46) return '血液腫瘤科'
    if (num <= 50) return '風濕免疫科'
    if (num <= 55) return '感染科'
    if (num <= 68) return '家庭醫學科'
    return '醫學倫理與法規'
  }

  if (sub === '醫學(四)') {
    if (/皮|皮疹|蕁麻疹|濕疹|癬|derma|rash|melanoma|psoriasis|乾癬|天疱瘡/i.test(fullText)) {
      return '皮膚科'
    }
    if (/小兒|兒童|新生兒|早產兒|pediatric|infant|newborn|川崎|kawasaki|腸病毒/i.test(fullText)) {
      return '小兒科'
    }
    if (/精神|憂鬱|思覺失調|躁鬱|schizophrenia|depression|bipolar|phobia|強迫症|dementia|失智/i.test(fullText)) {
      return '精神科'
    }
    if (/神經|中風|stroke|癲癇|seizure|parkinson|巴金森|腦膜炎|頭痛|neuropathy|als/i.test(fullText)) {
      return '神經科'
    }

    if (num <= 30) return '小兒科'
    if (num <= 42) return '皮膚科'
    if (num <= 62) return '神經科'
    return '精神科'
  }

  if (sub === '醫學(五)') {
    if (/骨|骨折|fracture|脫臼|dislocation|韌帶|ligament|膝|髖|關節鏡|ortho|scoliosis/i.test(fullText)) {
      return '骨科'
    }
    if (/泌尿|攝護腺|prostate|腎結石|膀胱|bladder|血尿|hematuria|包莖|睾丸|testis/i.test(fullText)) {
      return '泌尿科'
    }
    if (/一般外科|疝氣|hernia|闌尾炎|appendicitis|乳癌|breast|膽囊|cholecystitis|胃切除/i.test(fullText)) {
      return '一般外科'
    }

    if (num <= 40) return '一般外科'
    if (num <= 60) return '骨科'
    return '泌尿科'
  }

  if (sub === '醫學(六)') {
    if (/眼|視力|青光眼|glaucoma|白內障|cataract|視網膜|retina|角膜|結膜/i.test(fullText)) {
      return '眼科'
    }
    if (/耳|鼻|喉|聽力|hearing|眩暈|vertigo|鼻竇|sinus|會厭|epiglottitis|中耳/i.test(fullText)) {
      return '耳鼻喉科'
    }
    if (/婦|產|懷孕|pregnancy|胎兒|fetal|子宮|uterus|卵巢|ovary|陰道|產檢|避孕/i.test(fullText)) {
      return '婦產科'
    }
    if (/麻醉|anesthesia|插管|intubation|鎮靜|sedation|肌肉鬆弛/i.test(fullText)) {
      return '麻醉科'
    }
    if (/復健|rehabilitation|巴氏量表|barthel|輔具|關節活動度|物理治療/i.test(fullText)) {
      return '復健科'
    }

    if (num <= 15) return '婦產科'
    if (num <= 30) return '眼科'
    if (num <= 45) return '耳鼻喉科'
    if (num <= 65) return '婦產科'
    if (num <= 75) return '復健科'
    return '醫學倫理與法規'
  }

  return '一般臨床醫學'
}

const SUBSPECIALTY_GROUPS = [
  {
    category: '🫀 內科系',
    items: ['腎臟內科', '胸腔內科', '心臟內科', '腸胃肝膽科', '內分泌新陳代謝科', '血液腫瘤科', '風濕免疫科', '感染科', '家庭醫學科']
  },
  {
    category: '👶 兒神皮精',
    items: ['小兒科', '皮膚科', '神經科', '精神科']
  },
  {
    category: '🔪 外科系',
    items: ['一般外科', '骨科', '泌尿科']
  },
  {
    category: '🤰 婦產科',
    items: ['婦產科']
  },
  {
    category: '🩺 專科醫學',
    items: ['麻醉科', '眼科', '耳鼻喉科', '復健科']
  },
  {
    category: '⚖️ 醫學倫理與法規',
    items: ['醫學倫理與法規']
  }
]

// Helper function to get data from local storage
const getLocalStorage = (key, defaultValue) => {
  const stored = localStorage.getItem(key)
  if (stored) {
    try {
      return JSON.parse(stored)
    } catch (e) {
      return defaultValue
    }
  }
  return defaultValue
}

function formatInlineMarkdown(str) {
  if (!str) return ''
  const parts = str.split(/(\*\*.*?\*\*)/g)
  return parts.map((part, i) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={i}>{part.slice(2, -2)}</strong>
    }
    return part
  })
}

function FormattedExplanation({ text }) {
  if (!text) return null
  const blocks = text.split(/\n\n+/)
  return (
    <div className="formatted-explanation">
      {blocks.map((block, bIdx) => {
        const trimmed = block.trim()
        const lines = trimmed.split('\n').map(l => l.trim()).filter(Boolean)
        const isTable = lines.length >= 2 && lines.some(l => l.startsWith('|') && l.endsWith('|'))

        if (isTable) {
          const tableLines = lines.filter(l => l.startsWith('|') && l.endsWith('|'))
          const headerLine = tableLines[0]
          const contentLines = tableLines.slice(1).filter(l => !l.includes('---') && !l.includes(':---'))
          const headers = headerLine.split('|').slice(1, -1).map(h => h.trim())
          const rows = contentLines.map(r => r.split('|').slice(1, -1).map(c => c.trim()))

          return (
            <div key={bIdx} style={{ overflowX: 'auto', margin: '0.75rem 0' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.88rem', border: '1px solid var(--border-color)' }}>
                <thead>
                  <tr style={{ background: 'var(--bg-secondary)', borderBottom: '2px solid var(--border-color)' }}>
                    {headers.map((h, i) => (
                      <th key={i} style={{ padding: '0.5rem 0.75rem', textAlign: 'left', fontWeight: 600 }}>
                        {formatInlineMarkdown(h)}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {rows.map((row, rIdx) => (
                    <tr key={rIdx} style={{ borderBottom: '1px solid var(--border-color)', background: rIdx % 2 === 1 ? 'var(--bg-secondary)' : 'transparent' }}>
                      {row.map((cell, cIdx) => (
                        <td key={cIdx} style={{ padding: '0.5rem 0.75rem' }}>
                          {formatInlineMarkdown(cell)}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )
        }

        return (
          <div key={bIdx} style={{ marginBottom: '0.75rem', lineHeight: '1.75' }}>
            {lines.map((l, lIdx) => (
              <span key={lIdx}>
                {formatInlineMarkdown(l)}
                {lIdx < lines.length - 1 && <br />}
              </span>
            ))}
          </div>
        )
      })}
    </div>
  )
}

// Book Explanation Component to render page scan image when available
function BookExplanation({ q }) {
  const [activePageIdx, setActivePageIdx] = useState(0)
  const [isFullScreen, setIsFullScreen] = useState(false)
  const [imgError, setImgError] = useState(false)
  
  const hasTextExplanation = !!q.explanation
  const explanationPages = q.explanation_pages || []
  
  const lookupKey = `${q.year}-${q.subject}-${q.number}`
  const fallbackPageNum = explanationsMap[lookupKey]
  const pagesToRender = explanationPages.length > 0 
    ? explanationPages 
    : (fallbackPageNum ? [fallbackPageNum] : [])
    
  const croppedImages = q.explanation_images || (q.explanation_image ? [q.explanation_image] : [])
  const hasCroppedImage = croppedImages.length > 0 && !imgError

  // Hide image box only for 113-2 Med 4, Med 5, Med 6
  const isExcludedSubject = q.year === '113-2' && ['醫學(四)', '醫學(五)', '醫學(六)'].includes(q.subject)
  const showImageContainer = !isExcludedSubject && (pagesToRender.length > 0 || hasCroppedImage)
  
  if (!hasTextExplanation && !showImageContainer) return null
  
  const activePageNum = pagesToRender[activePageIdx] || pagesToRender[0]
  const imgUrl = hasCroppedImage 
    ? croppedImages[Math.min(activePageIdx, croppedImages.length - 1)] 
    : `/explanations/page_${activePageNum}.jpg`
  
  return (
    <div className="book-explanation-container" style={{ marginTop: '1rem', borderTop: '1px dashed var(--border-color)', paddingTop: '1rem' }}>
      {/* 1. OCR Text Explanation */}
      {hasTextExplanation && (
        <div className="text-explanation-box" style={{ marginBottom: showImageContainer ? '1rem' : '0' }}>
          <div style={{ fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: '0.35rem', color: 'var(--accent-color)', fontSize: '0.95rem' }}>
            📖 完整解說文字
          </div>
          <div 
            style={{ 
              marginTop: '0.5rem', 
              fontSize: '0.92rem', 
              color: 'var(--text-primary)',
              background: 'var(--bg-tertiary)',
              padding: '1rem',
              borderRadius: '6px',
              border: '1px solid var(--border-color)',
              maxHeight: '450px',
              overflowY: 'auto'
            }}
          >
            <FormattedExplanation text={q.explanation} />
          </div>
        </div>
      )}
      
      {/* 2. Original Book Scans (restored for all except 113-2 Med 4, 5, 6) */}
      {showImageContainer && (
        <div className="book-scans-box">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
            <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
              {hasCroppedImage 
                ? (croppedImages.length > 1 ? `🖼️ 對照原書詳解截圖 (共 ${croppedImages.length} 頁)` : '🖼️ 對照原書詳解截圖') 
                : `🖼️ 對照原書圖文與表格 (第 ${activePageNum} 頁)`}
            </span>
            
            {/* Page Tabs Selector */}
            {pagesToRender.length > 1 && !hasCroppedImage && (
              <div style={{ display: 'flex', gap: '0.25rem' }}>
                {pagesToRender.map((pageNum, idx) => (
                  <button
                    key={pageNum}
                    className={`btn btn-sm ${activePageIdx === idx ? 'btn-primary' : 'btn-secondary'}`}
                    style={{ padding: '0.2rem 0.5rem', fontSize: '0.75rem', borderRadius: '4px' }}
                    onClick={() => setActivePageIdx(idx)}
                  >
                    第 {pageNum} 頁
                  </button>
                ))}
              </div>
            )}
            {hasCroppedImage && croppedImages.length > 1 && (
              <div style={{ display: 'flex', gap: '0.25rem' }}>
                {croppedImages.map((_, idx) => (
                  <button
                    key={idx}
                    className={`btn btn-sm ${activePageIdx === idx ? 'btn-primary' : 'btn-secondary'}`}
                    style={{ padding: '0.2rem 0.5rem', fontSize: '0.75rem', borderRadius: '4px' }}
                    onClick={() => setActivePageIdx(idx)}
                  >
                    第 {idx + 1} 頁
                  </button>
                ))}
              </div>
            )}
          </div>
          
          <div className="book-explanation-image-box animate-fade-in" style={{ position: 'relative', width: '100%', background: '#ffffff', borderRadius: '4px', border: '1px solid var(--border-color)', padding: '0.5rem' }}>
            {hasCroppedImage && croppedImages.length > 1 ? (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                {croppedImages.map((cropUrl, idx) => (
                  <div key={idx} style={{ position: 'relative', borderBottom: idx < croppedImages.length - 1 ? '1px dashed var(--border-color)' : 'none', paddingBottom: idx < croppedImages.length - 1 ? '0.75rem' : '0' }}>
                    <div style={{ fontSize: '0.75rem', fontWeight: 'bold', color: 'var(--accent-color)', marginBottom: '0.35rem' }}>
                      📄 詳解第 {idx + 1} 頁截圖：
                    </div>
                    <img 
                      src={cropUrl} 
                      alt={`原書詳解截圖 ${idx + 1}`}
                      style={{ width: '100%', height: 'auto', display: 'block', borderRadius: '4px', cursor: 'zoom-in', background: '#ffffff' }}
                      onError={() => setImgError(true)}
                      onClick={() => {
                        setActivePageIdx(idx)
                        setIsFullScreen(true)
                      }}
                    />
                  </div>
                ))}
              </div>
            ) : (
              <img 
                src={imgUrl} 
                alt={`原書詳解`}
                style={{ width: '100%', height: 'auto', display: 'block', borderRadius: '4px', cursor: 'zoom-in', background: '#ffffff' }}
                onError={() => setImgError(true)}
                onClick={() => setIsFullScreen(true)}
              />
            )}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '0.5rem', padding: '0 0.25rem', fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
              <span>點擊圖片可放大閱讀</span>
              <button 
                className="btn-link"
                style={{ color: 'var(--accent-color)', cursor: 'pointer', border: 'none', background: 'none', padding: 0 }}
                onClick={() => setIsFullScreen(true)}
              >
                🔍 全螢幕檢視
              </button>
            </div>
          </div>
        </div>
      )}
      
      {/* Fullscreen Overlay Modal */}
      {isFullScreen && showImageContainer && (
        <div 
          className="modal-overlay" 
          style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.75)', display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 1000, cursor: 'zoom-out', padding: '1rem' }}
          onClick={() => setIsFullScreen(false)}
        >
          <div 
            style={{ position: 'relative', maxWidth: '900px', width: '100%', maxHeight: '90vh', overflowY: 'auto', display: 'flex', flexDirection: 'column', alignItems: 'center', background: '#ffffff', padding: '1.5rem', borderRadius: '8px', boxShadow: '0 8px 30px rgba(0,0,0,0.5)' }}
            onClick={e => e.stopPropagation()}
          >
            <button 
              style={{ position: 'absolute', top: '0.5rem', right: '0.75rem', color: '#333333', background: 'none', border: 'none', fontSize: '1.2rem', cursor: 'pointer', fontWeight: 'bold' }}
              onClick={() => setIsFullScreen(false)}
            >
              ✕ 關閉
            </button>
            
            {hasCroppedImage && croppedImages.length > 1 && (
              <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem' }}>
                {croppedImages.map((_, idx) => (
                  <button
                    key={idx}
                    className={`btn btn-sm ${activePageIdx === idx ? 'btn-primary' : 'btn-secondary'}`}
                    onClick={() => setActivePageIdx(idx)}
                  >
                    第 {idx + 1} 頁截圖
                  </button>
                ))}
              </div>
            )}
            
            <img 
              src={imgUrl} 
              alt="全螢幕詳解" 
              style={{ width: '100%', height: 'auto', display: 'block', borderRadius: '4px', background: '#ffffff' }}
              onClick={() => setIsFullScreen(false)}
            />
            <p style={{ color: '#555555', marginTop: '0.75rem', fontSize: '0.85rem', textAlign: 'center' }}>
              {hasCroppedImage 
                ? (croppedImages.length > 1 ? `原書詳解截圖 (第 ${activePageIdx + 1} / ${croppedImages.length} 頁)` : '原書詳解截圖') 
                : `原書第 ${activePageNum} 頁 - 2024年醫師國考試題詳解 臨床醫學`}
            </p>
          </div>
        </div>
      )}
    </div>
  )
}




// User Custom Note Box Component for any question
function UserNoteBox({ questionId, userNotes, onSaveNote }) {
  const note = userNotes[questionId] || ''
  const [editingText, setEditingText] = useState(note)
  const [isEditing, setIsEditing] = useState(false)

  useEffect(() => {
    setEditingText(note)
  }, [note])

  return (
    <div className="user-note-box" style={{ marginTop: '0.75rem', background: 'var(--bg-tertiary)', border: '1px solid var(--border-color)', borderRadius: '6px', padding: '0.75rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.4rem' }}>
        <span style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--accent-color)', display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
          📝 個人備註與筆記
        </span>
        {!isEditing && (
          <button 
            className="btn btn-secondary btn-sm"
            style={{ padding: '0.15rem 0.45rem', fontSize: '0.75rem' }}
            onClick={() => setIsEditing(true)}
          >
            {note ? '✏️ 編輯筆記' : '➕ 新增筆記'}
          </button>
        )}
      </div>

      {isEditing ? (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          <textarea
            style={{ 
              width: '100%', 
              minHeight: '75px', 
              padding: '0.5rem 0.75rem', 
              fontSize: '0.88rem', 
              lineHeight: '1.5',
              background: 'var(--bg-primary)',
              color: 'var(--text-primary)',
              border: '1px solid var(--accent-color)',
              borderRadius: '4px',
              resize: 'vertical',
              fontFamily: 'inherit'
            }}
            placeholder="點擊在此輸入您個人的重點筆記、記憶口訣或觀念補充..."
            value={editingText}
            onChange={(e) => setEditingText(e.target.value)}
          />
          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.4rem' }}>
            {note && (
              <button 
                className="btn btn-secondary btn-sm"
                style={{ padding: '0.2rem 0.5rem', fontSize: '0.75rem', color: 'var(--danger)' }}
                onClick={() => {
                  onSaveNote(questionId, '')
                  setEditingText('')
                  setIsEditing(false)
                }}
              >
                刪除筆記
              </button>
            )}
            <button 
              className="btn btn-primary btn-sm"
              style={{ padding: '0.2rem 0.6rem', fontSize: '0.75rem' }}
              onClick={() => {
                onSaveNote(questionId, editingText)
                setIsEditing(false)
              }}
            >
              儲存筆記
            </button>
          </div>
        </div>
      ) : (
        note ? (
          <div 
            style={{ 
              fontSize: '0.9rem', 
              color: 'var(--text-primary)', 
              whiteSpace: 'pre-line', 
              lineHeight: '1.6',
              cursor: 'pointer',
              padding: '0.2rem 0'
            }}
            onClick={() => setIsEditing(true)}
          >
            {note}
          </div>
        ) : (
          <div 
            style={{ fontSize: '0.8rem', color: 'var(--text-tertiary)', fontStyle: 'italic', cursor: 'pointer' }}
            onClick={() => setIsEditing(true)}
          >
            尚無筆記，點擊「➕ 新增筆記」紀錄這題的重點口訣與檢討...
          </div>
        )
      )}
    </div>
  )
}

function App() {
  // Page states: 'dashboard' | 'exam' | 'result' | 'review' | 'search' | 'bookmarks' (Database updated)
  const [currentPage, setCurrentPage] = useState('dashboard')
  
  // Selected year term for subject selector modal
  const [selectedYearTerm, setSelectedYearTerm] = useState(null)
  
  // Theme state: 'light' | 'dark'
  const [theme, setTheme] = useState(() => getLocalStorage('med-exam-theme', 'light'))
  
  // Bookmarks state (cleared)
  const [bookmarks, setBookmarks] = useState([])
  
  // Wrong questions state (array of question IDs)
  const [wrongQuestions, setWrongQuestions] = useState(() => getLocalStorage('med-exam-wrong', []))

  // User custom notes state { [questionId: string]: string }
  const [userNotes, setUserNotes] = useState(() => getLocalStorage('med-exam-user-notes', {}))
  
  // Completed exam history records
  const [history, setHistory] = useState(() => getLocalStorage('med-exam-history', []))
  
  // Active test/practice session state
  const [currentExam, setCurrentExam] = useState(null)
  
  // Search query state
  const [searchQuery, setSearchQuery] = useState('')
  const [searchMode, setSearchMode] = useState('disease') // 'disease' | 'fulltext'
  const [searchResults, setSearchResults] = useState([])
  const [searchAnswers, setSearchAnswers] = useState({}) // { questionId: selectedOption }
  
  // Bookmarks practice state
  const [bookmarkAnswers, setBookmarkAnswers] = useState({}) // { questionId: selectedOption }
  
  // Wrong questions practice state
  const [wrongAnswers, setWrongAnswers] = useState({}) // { questionId: selectedOption }
  const [wrongFilterSubject, setWrongFilterSubject] = useState('all')

  // Apply theme to document element
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
    localStorage.setItem('med-exam-theme', JSON.stringify(theme))
  }, [theme])

  // Sync bookmarks, wrong questions, and history to localStorage
  useEffect(() => {
    localStorage.setItem('med-exam-bookmarks', JSON.stringify(bookmarks))
  }, [bookmarks])

  useEffect(() => {
    localStorage.setItem('med-exam-wrong', JSON.stringify(wrongQuestions))
  }, [wrongQuestions])

  useEffect(() => {
    localStorage.setItem('med-exam-history', JSON.stringify(history))
  }, [history])

  useEffect(() => {
    localStorage.setItem('med-exam-user-notes', JSON.stringify(userNotes))
  }, [userNotes])

  const handleSaveUserNote = (questionId, noteText) => {
    setUserNotes(prev => {
      const updated = { ...prev }
      if (noteText && noteText.trim()) {
        updated[questionId] = noteText.trim()
      } else {
        delete updated[questionId]
      }
      return updated
    })
  }

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light')
  }

  // Check if user answer is correct (handles ALL and multiple answers like B,D)
  const isAnswerCorrect = (q, userAns) => {
    if (!userAns) return false
    if (q.answer === 'ALL') return true
    const correctOptions = q.answer.split(',')
    return correctOptions.includes(userAns)
  }

  // Get unique list of years and subjects in database
  const yearsList = [...new Set(questionsData.map(q => q.year))].sort().reverse()
  const subjectsList = ['醫學(三)', '醫學(四)', '醫學(五)', '醫學(六)']

  // Start new test or practice session
  const startSession = (year, subject, mode) => {
    const filtered = questionsData.filter(q => q.year === year && q.subject === subject)
    
    // Sort by question number sequentially
    const sorted = [...filtered].sort((a, b) => a.number - b.number)
    
    if (sorted.length === 0) {
      alert('無此考期的題目資料')
      return
    }

    setCurrentExam({
      name: `${year}年 ${subject} 測驗`,
      year: year,
      subject: subject,
      questions: sorted,
      currentIndex: 0,
      answers: {}, // { questionId: selectedOption }
      flagged: {}, // { questionId: boolean }
      timeLeft: mode === 'exam' ? 120 * 60 : null, // 120 minutes for exam mode
      totalQuestions: sorted.length,
      mode: mode // 'exam' | 'practice'
    })
    
    setCurrentPage('exam')
  }

  // Quick Random Quiz
  const startQuickQuiz = (numQuestions, subjectFilter, mode) => {
    let pool = [...questionsData]
    if (subjectFilter !== 'all') {
      pool = pool.filter(q => q.subject === subjectFilter)
    }
    
    // Shuffle and pick
    const shuffled = pool.sort(() => Math.random() - 0.5).slice(0, numQuestions)
    
    setCurrentExam({
      name: `快速隨機測驗 - ${subjectFilter === 'all' ? '不限考科' : subjectFilter} (${numQuestions}題)`,
      year: '隨機',
      subject: subjectFilter === 'all' ? '混合' : subjectFilter,
      questions: shuffled,
      currentIndex: 0,
      answers: {},
      flagged: {},
      timeLeft: mode === 'exam' ? numQuestions * 90 : null, // 90 seconds per question for exam mode
      totalQuestions: shuffled.length,
      mode: mode
    })
    
    setCurrentPage('exam')
  }

  // Timer logic for exam mode
  useEffect(() => {
    if (currentPage !== 'exam' || !currentExam || currentExam.mode !== 'exam') return

    const timer = setInterval(() => {
      setCurrentExam(prev => {
        if (!prev) return null
        if (prev.timeLeft <= 1) {
          clearInterval(timer)
          handleSubmitExam(prev)
          return null
        }
        return {
          ...prev,
          timeLeft: prev.timeLeft - 1
        }
      })
    }, 1000)

    return () => clearInterval(timer)
  }, [currentPage, currentExam])

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }

  const handleSelectOption = (questionId, optionLetter) => {
    setCurrentExam(prev => ({
      ...prev,
      answers: {
        ...prev.answers,
        [questionId]: optionLetter
      }
    }))
  }

  const handleToggleFlag = (questionId) => {
    setCurrentExam(prev => ({
      ...prev,
      flagged: {
        ...prev.flagged,
        [questionId]: !prev.flagged[questionId]
      }
    }))
  }

  const toggleBookmark = (questionId) => {
    setBookmarks(prev => {
      if (prev.includes(questionId)) {
        return prev.filter(id => id !== questionId)
      } else {
        return [...prev, questionId]
      }
    })
  }

  const handleSubmitExam = (examToSubmit = currentExam) => {
    if (!examToSubmit) return

    let correctCount = 0
    const incorrectIds = []
    
    examToSubmit.questions.forEach(q => {
      const userAns = examToSubmit.answers[q.id]
      if (isAnswerCorrect(q, userAns)) {
        correctCount++
      } else {
        incorrectIds.push(q.id)
      }
    })

    const score = Math.round((correctCount / examToSubmit.totalQuestions) * 100)
    const dateStr = new Date().toLocaleString('zh-TW', { hour12: false })

    const newRecord = {
      id: Date.now(),
      name: examToSubmit.name,
      date: dateStr,
      score: score,
      correctCount: correctCount,
      totalQuestions: examToSubmit.totalQuestions,
      answers: examToSubmit.answers,
      questions: examToSubmit.questions
    }

    setHistory(prev => [newRecord, ...prev])
    
    // Add wrong question IDs to wrongQuestions list
    setWrongQuestions(prev => {
      const updated = [...prev]
      incorrectIds.forEach(id => {
        if (!updated.includes(id)) {
          updated.push(id)
        }
      })
      return updated
    })

    setCurrentExam(newRecord) // Store result in currentExam to display in results page
    setCurrentPage('result')
  }

  const viewHistoryDetail = (record) => {
    setCurrentExam(record)
    setCurrentPage('result')
  }

  // Handle Search Input with Disease/Medical Term Filter
  const triggerSearch = (query = searchQuery, mode = searchMode) => {
    const qTrim = query.trim()
    if (!qTrim) {
      setSearchResults([])
      return
    }

    const qLower = qTrim.toLowerCase()
    const isAscii = /^[\x00-\x7F]+$/.test(qTrim)

    const results = []

    questionsData.forEach(q => {
      const fullText = [
        q.text,
        ...Object.values(q.options || {}),
        q.note || '',
        q.explanation || ''
      ].join(' ')
      const fullTextLower = fullText.toLowerCase()

      if (mode === 'disease') {
        if (isAscii) {
          // Word boundary prefix search for English medical terms: \bquery[a-z0-9_-]*
          const pattern = new RegExp(`\\b${escapeRegExp(qLower)}[a-z0-9_-]*\\b`, 'gi')
          const matches = fullText.match(pattern) || []
          
          const validMatches = new Set()
          matches.forEach(m => {
            const mLower = m.toLowerCase()
            if (mLower === qLower || !NON_MEDICAL_ENGLISH_WORDS.has(mLower)) {
              validMatches.add(m)
            }
          })

          if (validMatches.size > 0) {
            results.push({
              ...q,
              matchedTerms: Array.from(validMatches)
            })
          }
        } else {
          // Chinese search: direct substring match
          if (fullTextLower.includes(qLower)) {
            results.push({
              ...q,
              matchedTerms: [qTrim]
            })
          }
        }
      } else {
        // Fulltext mode: naive substring match
        if (fullTextLower.includes(qLower)) {
          results.push({
            ...q,
            matchedTerms: [qTrim]
          })
        }
      }
    })

    setSearchResults(results)
    setSearchAnswers({})
  }

  // Dashboard Renderer
  const renderDashboard = () => {
    const avgScore = history.length > 0 
      ? Math.round(history.reduce((sum, r) => sum + r.score, 0) / history.length) 
      : 0

    return (
      <div className="dashboard-container animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
        {/* Statistics Grid */}
        <div className="dashboard-grid">
          <div className="card stat-card glass-card">
            <div className="stat-info">
              <p>題庫總數</p>
              <h3>{questionsData.length} 題</h3>
            </div>
            <div className="stat-icon icon-blue">🩺</div>
          </div>
          
          <div className="card stat-card glass-card">
            <div className="stat-info">
              <p>錯題本累積</p>
              <h3>{wrongQuestions.length} 題</h3>
            </div>
            <div className="stat-icon icon-red">✕</div>
          </div>

          <div className="card stat-card glass-card">
            <div className="stat-info">
              <p>歷次平均得分</p>
              <h3>{avgScore} 分</h3>
            </div>
            <div className="stat-icon icon-green">★</div>
          </div>
        </div>

        {/* Quick Quiz Card */}
        <div className="card">
          <h3 className="section-card-title">快速隨機練習</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginTop: '1rem' }}>
            <div>
              <label style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', display: 'block', marginBottom: '0.5rem' }}>設定題數</label>
              <select id="quick-num" className="option-button" style={{ padding: '0.5rem', background: 'var(--bg-tertiary)' }} defaultValue="20">
                <option value="10">10 題</option>
                <option value="20">20 題</option>
                <option value="40">40 題</option>
                <option value="80">80 題</option>
              </select>
            </div>
            <div>
              <label style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', display: 'block', marginBottom: '0.5rem' }}>選擇考科</label>
              <select id="quick-sub" className="option-button" style={{ padding: '0.5rem', background: 'var(--bg-tertiary)' }} defaultValue="all">
                <option value="all">混合全部</option>
                <option value="醫學(三)">醫學(三) - 內科/家醫/倫理</option>
                <option value="醫學(四)">醫學(四) - 小兒/皮/神/精</option>
                <option value="醫學(五)">醫學(五) - 外科/骨科/泌尿</option>
                <option value="醫學(六)">醫學(六) - 麻醉/眼/耳鼻喉/婦產/復健</option>
              </select>
            </div>
            <div style={{ display: 'flex', alignItems: 'flex-end', gap: '0.5rem' }}>
              <button className="btn btn-primary" style={{ flex: 1, padding: '0.6rem' }} onClick={() => {
                const num = parseInt(document.getElementById('quick-num').value)
                const sub = document.getElementById('quick-sub').value
                startQuickQuiz(num, sub, 'practice')
              }}>循序練習</button>
              <button className="btn btn-outline" style={{ flex: 1, padding: '0.6rem' }} onClick={() => {
                const num = parseInt(document.getElementById('quick-num').value)
                const sub = document.getElementById('quick-sub').value
                startQuickQuiz(num, sub, 'exam')
              }}>模擬考試</button>
            </div>
          </div>
        </div>

        {/* Exam Library */}
        <div className="dashboard-sections">
          <div className="card">
            <h3 className="section-card-title">歷屆試題庫</h3>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '1rem' }}>選擇您要挑戰的年度考期，點選進入後可進一步選擇科目進行練習或模擬考</p>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '1rem' }}>
              {yearsList.map(year => (
                <div 
                  key={year} 
                  className="subject-item animate-fade-in" 
                  style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '1.5rem', textAlign: 'center' }}
                  onClick={() => setSelectedYearTerm(year)}
                >
                  <span style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>📄</span>
                  <span className="subject-name" style={{ fontSize: '1.05rem', color: 'var(--accent-color)' }}>{year}</span>
                  <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '0.25rem' }}>{year.replace('-', '年第')}次國考二階</span>
                </div>
              ))}
            </div>
          </div>

          {/* History */}
          <div className="card">
            <h3 className="section-card-title">近期測驗記錄</h3>
            {history.length === 0 ? (
              <p style={{ color: 'var(--text-tertiary)', textAlign: 'center', margin: '2rem 0', fontSize: '0.9rem' }}>尚無測驗記錄</p>
            ) : (
              <div className="history-list" style={{ marginTop: '1rem' }}>
                {history.slice(0, 8).map((record) => (
                  <div key={record.id} className="history-item" style={{ padding: '0.5rem 0' }}>
                    <div className="history-info">
                      <p style={{ fontSize: '0.85rem' }}>{record.name}</p>
                      <p style={{ fontSize: '0.75rem' }}>{record.date}</p>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <span className="history-score" style={{ color: record.score >= 60 ? 'var(--success)' : 'var(--danger)', fontSize: '0.9rem' }}>
                        {record.score}分
                      </span>
                      <button className="btn btn-secondary btn-sm" style={{ padding: '0.2' }} onClick={() => viewHistoryDetail(record)}>詳解</button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    )
  }

  // Active Session Renderer (Exam Mode or Practice Mode)
  const renderExam = () => {
    if (!currentExam) return null

    const q = currentExam.questions[currentExam.currentIndex]
    const userSelected = currentExam.answers[q.id]
    const isFlagged = currentExam.flagged[q.id]
    const isBookmarked = bookmarks.includes(q.id)

    // In practice mode, we can show immediate answer check
    const answered = userSelected !== undefined

    return (
      <div className="exam-layout animate-fade-in">
        <div className="card question-card">
          <div className="question-header">
            <div>
              <span className="question-meta-badge" style={{ marginRight: '0.5rem' }}>{currentExam.name}</span>
              <span className="question-meta-badge">第 {currentExam.currentIndex + 1} / {currentExam.totalQuestions} 題</span>
            </div>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <button 
                className={`btn btn-secondary`} 
                style={{ padding: '0.4rem 0.8rem', fontSize: '0.85rem', color: isBookmarked ? 'var(--success)' : '' }}
                onClick={() => toggleBookmark(q.id)}
              >
                {isBookmarked ? '★ 已收藏' : '☆ 收藏題目'}
              </button>
              {currentExam.mode === 'exam' && (
                <button 
                  className={`btn ${isFlagged ? 'btn-primary' : 'btn-secondary'}`} 
                  style={{ padding: '0.4rem 0.8rem', fontSize: '0.85rem', backgroundColor: isFlagged ? 'var(--warning)' : '' }}
                  onClick={() => handleToggleFlag(q.id)}
                >
                  {isFlagged ? '★ 已標記' : '☆ 標記此題'}
                </button>
              )}
            </div>
          </div>

          <div className="question-body">
            <div className="question-text">
              <span style={{ color: 'var(--accent-color)', marginRight: '0.5rem' }}>Q{q.number}.</span>
              {q.text}
            </div>
            
            {/* Clinical Images */}
            {q.images && q.images.length > 0 && (
              <div style={{ marginBottom: '1.5rem', display: 'flex', flexWrap: 'wrap', gap: '1rem' }}>
                {q.images.map((imgSrc, idx) => (
                  <img 
                    key={idx}
                    src={imgSrc}
                    alt={`題目附圖 ${idx + 1}`}
                    style={{ maxWidth: '100%', maxHeight: '280px', objectFit: 'contain', borderRadius: '4px', border: '1px solid var(--border-color)' }}
                  />
                ))}
              </div>
            )}

            {/* Options List */}
            <div className="options-list">
              {Object.entries(q.options).map(([letter, text]) => {
                let optClass = ''
                if (currentExam.mode === 'practice' && answered) {
                  // In practice mode, show correct/incorrect styles immediately
                  const isCorrectOpt = isAnswerCorrect(q, letter)
                  if (letter === userSelected) {
                    optClass = isCorrectOpt ? 'correct' : 'incorrect'
                  } else if (isCorrectOpt) {
                    optClass = 'correct' // Highlight the correct option
                  }
                } else {
                  // In exam mode, just show selected state
                  if (userSelected === letter) {
                    optClass = 'selected'
                  }
                }

                return (
                  <button
                    key={letter}
                    className={`option-button ${optClass}`}
                    disabled={currentExam.mode === 'practice' && answered} // Disable option changing in practice mode
                    onClick={() => handleSelectOption(q.id, letter)}
                  >
                    <strong style={{ marginRight: '0.5rem' }}>({letter})</strong> {text}
                  </button>
                )
              })}
            </div>

            {/* Note & Remarks shown immediately in practice mode */}
            {currentExam.mode === 'practice' && answered && (
              <div className="explanation-box animate-fade-in" style={{ marginTop: '1.5rem' }}>
                <div className="explanation-title" style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span>💡 答案與更正說明</span>
                  <span style={{ color: isAnswerCorrect(q, userSelected) ? 'var(--success)' : 'var(--danger)' }}>
                    {isAnswerCorrect(q, userSelected) ? '答對了！' : '答錯了！'} 正確答案：{q.answer.replace('ALL', '一律給分')}
                  </span>
                </div>
                {q.note ? (
                  <div className="explanation-text" style={{ color: 'var(--warning)', fontWeight: 600 }}>備註：{q.note}</div>
                ) : (
                  <div className="explanation-text" style={{ color: 'var(--text-secondary)' }}>此題目前尚無詳細解析對照，請溫習相關臨床講義</div>
                )}
                <BookExplanation q={q} />
              </div>
            )}
          </div>

          <div className="question-footer">
            <button
              className="btn btn-secondary"
              disabled={currentExam.currentIndex === 0}
              onClick={() => setCurrentExam(prev => ({ ...prev, currentIndex: prev.currentIndex - 1 }))}
            >
              上一題
            </button>
            
            {currentExam.mode === 'exam' ? (
              <button className="btn btn-danger" onClick={() => {
                if (window.confirm('確定要退出考試交卷嗎？')) {
                  handleSubmitExam()
                }
              }}>
                交卷
              </button>
            ) : (
              <button className="btn btn-secondary" onClick={() => {
                if (window.confirm('確定要退出練習回首頁嗎？')) {
                  setCurrentPage('dashboard')
                  setCurrentExam(null)
                }
              }}>
                退出練習
              </button>
            )}

            {currentExam.currentIndex === currentExam.totalQuestions - 1 ? (
              currentExam.mode === 'exam' ? (
                <button className="btn btn-primary" onClick={() => handleSubmitExam()}>
                  交卷
                </button>
              ) : (
                <button className="btn btn-primary" onClick={() => {
                  alert('練習完成！')
                  setCurrentPage('dashboard')
                  setCurrentExam(null)
                }}>
                  結束練習
                </button>
              )
            ) : (
              <button
                className="btn btn-primary"
                onClick={() => setCurrentExam(prev => ({ ...prev, currentIndex: prev.currentIndex + 1 }))}
              >
                下一題
              </button>
            )}
          </div>
        </div>

        {/* Sidebar */}
        <div className="exam-sidebar">
          {currentExam.mode === 'exam' && (
            <div className="card timer-card glass-card">
              <h4>剩餘時間</h4>
              <div className="timer-display" style={{ color: currentExam.timeLeft < 180 ? 'var(--danger)' : 'var(--text-primary)' }}>
                {formatTime(currentExam.timeLeft)}
              </div>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>考試進行中</p>
            </div>
          )}

          <div className="card" style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
            <h4 style={{ marginBottom: '0.75rem', fontSize: '0.95rem' }}>題目導覽</h4>
            <div className="question-nav-grid" style={{ gridTemplateColumns: 'repeat(5, 1fr)' }}>
              {currentExam.questions.map((question, idx) => {
                const answered = currentExam.answers[question.id] !== undefined
                const flagged = currentExam.flagged[question.id]
                const current = currentExam.currentIndex === idx
                
                let btnClass = ''
                if (flagged) btnClass = 'flagged'
                else if (answered) btnClass = 'answered'
                if (current) btnClass += ' current'

                return (
                  <button
                    key={question.id}
                    className={`nav-grid-btn ${btnClass}`}
                    onClick={() => setCurrentExam(prev => ({ ...prev, currentIndex: idx }))}
                  >
                    {idx + 1}
                  </button>
                )
              })}
            </div>
            <div style={{ marginTop: '1rem', display: 'flex', gap: '0.5rem', flexWrap: 'wrap', fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
              <span style={{ display: 'inline-flex', alignItems: 'center', gap: '0.25rem' }}>
                <span style={{ width: '10px', height: '10px', backgroundColor: 'var(--accent-color)', borderRadius: '2px' }}></span> 已答
              </span>
              <span style={{ display: 'inline-flex', alignItems: 'center', gap: '0.25rem' }}>
                <span style={{ width: '10px', height: '10px', backgroundColor: 'var(--warning)', borderRadius: '2px' }}></span> 標記
              </span>
              <span style={{ display: 'inline-flex', alignItems: 'center', gap: '0.25rem' }}>
                <span style={{ width: '10px', height: '10px', backgroundColor: 'var(--bg-tertiary)', border: '1px solid var(--border-color)', borderRadius: '2px' }}></span> 未答
              </span>
            </div>
          </div>
        </div>
      </div>
    )
  }

  // Result Summary Renderer
  const renderResult = () => {
    if (!currentExam) return null

    return (
      <div className="result-container animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
        <div className="card result-header-card" style={{ textAlign: 'center', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1rem' }}>
          <h2>測驗結果報告</h2>
          <div className="result-score-circle">
            <span>{currentExam.score}</span>
            <span>得分</span>
          </div>
          <div className="result-meta-grid" style={{ display: 'flex', gap: '2rem', justifyContent: 'center', width: '100%', maxWidth: '600px', marginTop: '1rem' }}>
            <div className="result-meta-item" style={{ flex: 1 }}>
              <p style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{currentExam.correctCount} / {currentExam.totalQuestions}</p>
              <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>答對題數</p>
            </div>
            <div className="result-meta-item" style={{ flex: 1 }}>
              <p style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{currentExam.totalQuestions - currentExam.correctCount}</p>
              <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>答錯題數</p>
            </div>
            <div className="result-meta-item" style={{ flex: 1 }}>
              <p style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{Math.round((currentExam.correctCount / currentExam.totalQuestions) * 100)}%</p>
              <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>正確率</p>
            </div>
          </div>
        </div>

        <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem' }}>
          <button className="btn btn-primary" onClick={() => {
            setCurrentPage('dashboard')
            setCurrentExam(null)
          }}>
            回首頁
          </button>
          <button className="btn btn-outline" onClick={() => startSession(currentExam.year || '113-2', currentExam.subject || '醫學(三)', 'exam')}>
            重新挑戰
          </button>
        </div>

        <div className="card">
          <h3 style={{ marginBottom: '1.5rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem' }}>答題明細與檢討</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
            {currentExam.questions.map((q, idx) => {
              const userAns = currentExam.answers[q.id]
              const isCorrect = isAnswerCorrect(q, userAns)
              const bookmarked = bookmarks.includes(q.id)
              
              return (
                <div key={q.id} style={{ borderBottom: '1px solid var(--border-color)', paddingBottom: '1.5rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.75rem' }}>
                    <h4 style={{ fontSize: '1.05rem', maxWidth: '80%', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <span style={{ color: 'var(--accent-color)' }}>Q{idx + 1}.</span> {q.text}
                    </h4>
                    <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                      <button 
                        className="btn btn-secondary btn-sm" 
                        style={{ padding: '0.2rem 0.4rem', fontSize: '0.75rem', color: bookmarked ? 'var(--success)' : '' }}
                        onClick={() => toggleBookmark(q.id)}
                      >
                        {bookmarked ? '★ 已收藏' : '☆ 收藏'}
                      </button>
                      <span className={`tag ${isCorrect ? 'tag-green' : 'tag-red'}`} style={{ backgroundColor: isCorrect ? 'var(--success-light)' : 'var(--danger-light)', color: isCorrect ? 'var(--success)' : 'var(--danger)', padding: '0.2rem 0.5rem', borderRadius: '4px', fontSize: '0.8rem', fontWeight: 'bold' }}>
                        {isCorrect ? '答對' : '答錯'}
                      </span>
                    </div>
                  </div>

                  {q.images && q.images.length > 0 && (
                    <div style={{ marginBottom: '1rem', display: 'flex', gap: '0.5rem' }}>
                      {q.images.map((imgSrc, imgIdx) => (
                        <img 
                          key={imgIdx}
                          src={imgSrc}
                          alt={`附圖`}
                          style={{ maxWidth: '100%', maxHeight: '200px', objectFit: 'contain', borderRadius: '4px', border: '1px solid var(--border-color)' }}
                        />
                      ))}
                    </div>
                  )}

                  <div className="options-list" style={{ pointerEvents: 'none' }}>
                    {Object.entries(q.options).map(([letter, text]) => {
                      let optClass = ''
                      const isCorrectOpt = isAnswerCorrect(q, letter)
                      if (letter === userAns) {
                        optClass = isCorrectOpt ? 'correct' : 'incorrect'
                      } else if (isCorrectOpt) {
                        optClass = 'correct'
                      }

                      return (
                        <div key={letter} className={`option-button ${optClass}`} style={{ marginBottom: '0.25rem', padding: '0.6rem 1rem', fontSize: '0.9rem' }}>
                          <strong>({letter})</strong> {text}
                        </div>
                      )
                    })}
                  </div>

                  {q.note && (
                    <div className="explanation-box" style={{ marginTop: '0.75rem' }}>
                      <div className="explanation-title">💡 更正備註</div>
                      <div className="explanation-text" style={{ color: 'var(--warning)', fontWeight: 600 }}>{q.note}</div>
                    </div>
                  )}
                  <BookExplanation q={q} />
                </div>
              )
            })}
          </div>
        </div>
      </div>
    )
  }

  // Keyword Search Renderer
  const renderSearch = () => {
    const quickKeywords = [
      { label: '闌尾炎 (app / appendicitis)', query: 'app' },
      { label: 'SLE (紅斑性狼瘡)', query: 'sle' },
      { label: 'Heparin (肝素)', query: 'heparin' },
      { label: 'Kawasaki (川崎氏症)', query: 'kawasaki' },
      { label: 'DVT (深層靜脈栓塞)', query: 'dvt' },
      { label: 'Pneumonia (肺炎)', query: 'pneumonia' },
      { label: 'Graves (甲狀腺機能亢進)', query: 'graves' },
      { label: 'TB (結核病)', query: 'tb' }
    ]

    return (
      <div className="search-container animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.5rem', marginBottom: '0.75rem' }}>
            <h3 className="section-card-title" style={{ margin: 0 }}>題庫關鍵字檢索</h3>
            
            {/* Search Mode Toggle */}
            <div style={{ display: 'flex', gap: '0.25rem', background: 'var(--bg-tertiary)', padding: '0.2rem', borderRadius: '6px', border: '1px solid var(--border-color)' }}>
              <button 
                className={`btn btn-sm ${searchMode === 'disease' ? 'btn-primary' : 'btn-secondary'}`}
                style={{ padding: '0.25rem 0.6rem', fontSize: '0.8rem', borderRadius: '4px' }}
                onClick={() => {
                  setSearchMode('disease')
                  if (searchQuery.trim()) triggerSearch(searchQuery, 'disease')
                }}
              >
                🩺 疾病與醫學術語
              </button>
              <button 
                className={`btn btn-sm ${searchMode === 'fulltext' ? 'btn-primary' : 'btn-secondary'}`}
                style={{ padding: '0.25rem 0.6rem', fontSize: '0.8rem', borderRadius: '4px' }}
                onClick={() => {
                  setSearchMode('fulltext')
                  if (searchQuery.trim()) triggerSearch(searchQuery, 'fulltext')
                }}
              >
                🌐 全文模式
              </button>
            </div>
          </div>

          <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '1rem' }}>
            {searchMode === 'disease' 
              ? '【疾病術語模式】依字首與詞界比對疾病與醫學單字（例如輸入 app 僅匹配 appendicitis / appendectomy，自動過濾 appearance, approach 等非醫學字詞）' 
              : '【全文模式】比對題目與選項中所有出現的字串或子字詞'}
          </p>

          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <input 
              type="text" 
              className="option-button" 
              style={{ flex: 1, padding: '0.75rem 1rem', background: 'var(--bg-tertiary)', border: '1px solid var(--border-color)', borderRadius: 'var(--radius-sm)' }}
              placeholder="輸入疾病、藥物、英文術語前綴（例如：app, sle, heparin, 闌尾炎...）" 
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') triggerSearch(searchQuery)
              }}
            />
            <button className="btn btn-primary" onClick={() => triggerSearch(searchQuery)}>搜尋</button>
          </div>

          {/* Quick Keyword Chips */}
          <div style={{ marginTop: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', fontWeight: 600 }}>快速熱門關鍵字：</span>
            {quickKeywords.map(item => (
              <button
                key={item.query}
                className="btn btn-secondary btn-sm"
                style={{ padding: '0.2rem 0.5rem', fontSize: '0.75rem', borderRadius: '12px', background: 'var(--bg-tertiary)' }}
                onClick={() => {
                  setSearchQuery(item.query)
                  triggerSearch(item.query)
                }}
              >
                {item.label}
              </button>
            ))}
          </div>
        </div>

        {searchResults.length > 0 && (
          <div className="card">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <h3 style={{ fontSize: '1.1rem', margin: 0 }}>搜尋結果 ({searchResults.length} 題)</h3>
              <span className="question-meta-badge" style={{ fontSize: '0.75rem' }}>
                模式: {searchMode === 'disease' ? '🩺 疾病與醫學術語' : '🌐 全文模式'}
              </span>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
              {searchResults.map((q, idx) => {
                const userSelected = searchAnswers[q.id]
                const answered = userSelected !== undefined
                const bookmarked = bookmarks.includes(q.id)

                return (
                  <div key={q.id} style={{ borderBottom: '1px solid var(--border-color)', paddingBottom: '1.5rem' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.75rem', flexWrap: 'wrap', gap: '0.5rem' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
                        <span className="question-meta-badge">{q.year}年 / {q.subject} / Q{q.number}</span>
                        {q.matchedTerms && q.matchedTerms.length > 0 && (
                          <span className="tag tag-green" style={{ backgroundColor: 'var(--success-light)', color: 'var(--success)', fontSize: '0.75rem', fontWeight: 600 }}>
                            🎯 匹配術語: {q.matchedTerms.join(', ')}
                          </span>
                        )}
                      </div>
                      <button 
                        className="btn btn-secondary btn-sm" 
                        style={{ padding: '0.2rem 0.4rem', fontSize: '0.75rem', color: bookmarked ? 'var(--success)' : '' }}
                        onClick={() => toggleBookmark(q.id)}
                      >
                        {bookmarked ? '★ 已收藏' : '☆ 收藏'}
                      </button>
                    </div>

                    <div className="question-text" style={{ fontSize: '1.05rem', fontWeight: 600 }}>{q.text}</div>
                    
                    {q.images && q.images.length > 0 && (
                      <div style={{ marginBottom: '1rem', display: 'flex', gap: '0.5rem' }}>
                        {q.images.map((imgSrc, imgIdx) => (
                          <img 
                            key={imgIdx}
                            src={imgSrc}
                            alt={`附圖`}
                            style={{ maxWidth: '100%', maxHeight: '200px', objectFit: 'contain', borderRadius: '4px', border: '1px solid var(--border-color)' }}
                          />
                        ))}
                      </div>
                    )}

                    <div className="options-list">
                      {Object.entries(q.options).map(([letter, text]) => {
                        let optClass = ''
                        if (answered) {
                          const isCorrectOpt = isAnswerCorrect(q, letter)
                          if (letter === userSelected) {
                            optClass = isCorrectOpt ? 'correct' : 'incorrect'
                          } else if (isCorrectOpt) {
                            optClass = 'correct'
                          }
                        }

                        return (
                          <button
                            key={letter}
                            className={`option-button ${optClass}`}
                            style={{ padding: '0.6rem 1rem', fontSize: '0.9rem' }}
                            disabled={answered}
                            onClick={() => setSearchAnswers(prev => ({ ...prev, [q.id]: letter }))}
                          >
                            <strong>({letter})</strong> {text}
                          </button>
                        )
                      })}
                    </div>

                    {answered && (
                      <div className="explanation-box animate-fade-in" style={{ marginTop: '0.5rem' }}>
                        <div className="explanation-title">💡 答案對照</div>
                        <div className="explanation-text" style={{ color: 'var(--text-secondary)' }}>
                          答案：<strong>{q.answer.replace('ALL', '一律給分')}</strong>
                          {q.note && <div style={{ color: 'var(--warning)', marginTop: '0.25rem', fontWeight: 'bold' }}>更正備註：{q.note}</div>}
                        </div>
                        <BookExplanation q={q} />
                      </div>
                    )}
                  </div>
                )
              })}
            </div>
          </div>
        )}
      </div>
    )
  }

  // Bookmarks Renderer
  const renderBookmarks = () => {
    const bookmarkedList = questionsData.filter(q => bookmarks.includes(q.id))

    return (
      <div className="bookmarks-container animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
        <div className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h3>收藏夾 ({bookmarkedList.length} 題)</h3>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>您在測驗或練習中標記為重要的歷屆試題會收錄在此</p>
          </div>
          {bookmarks.length > 0 && (
            <button className="btn btn-outline" style={{ color: 'var(--danger)', borderColor: 'var(--danger)' }} onClick={() => {
              if (window.confirm('確定要清空所有收藏嗎？')) setBookmarks([])
            }}>清空全部</button>
          )}
        </div>

        {bookmarkedList.length === 0 ? (
          <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
            <p style={{ color: 'var(--text-tertiary)', fontSize: '1.1rem' }}>📭 目前收藏夾空空如也，在做題時點選「收藏題目」即可加入</p>
          </div>
        ) : (
          <div className="card">
            <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
              {bookmarkedList.map((q) => {
                const userSelected = bookmarkAnswers[q.id]
                const answered = userSelected !== undefined

                return (
                  <div key={q.id} style={{ borderBottom: '1px solid var(--border-color)', paddingBottom: '1.5rem' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.75rem' }}>
                      <span className="question-meta-badge">{q.year}年 / {q.subject} / Q{q.number}</span>
                      <button 
                        className="btn btn-secondary btn-sm" 
                        style={{ padding: '0.2rem 0.4rem', fontSize: '0.75rem', color: 'var(--danger)' }}
                        onClick={() => toggleBookmark(q.id)}
                      >
                        移除收藏
                      </button>
                    </div>

                    <div className="question-text" style={{ fontSize: '1.05rem', fontWeight: 600 }}>{q.text}</div>
                    
                    {q.images && q.images.length > 0 && (
                      <div style={{ marginBottom: '1rem', display: 'flex', gap: '0.5rem' }}>
                        {q.images.map((imgSrc, imgIdx) => (
                          <img 
                            key={imgIdx}
                            src={imgSrc}
                            alt={`附圖`}
                            style={{ maxWidth: '100%', maxHeight: '200px', objectFit: 'contain', borderRadius: '4px', border: '1px solid var(--border-color)' }}
                          />
                        ))}
                      </div>
                    )}

                    <div className="options-list">
                      {Object.entries(q.options).map(([letter, text]) => {
                        let optClass = ''
                        if (answered) {
                          const isCorrectOpt = isAnswerCorrect(q, letter)
                          if (letter === userSelected) {
                            optClass = isCorrectOpt ? 'correct' : 'incorrect'
                          } else if (isCorrectOpt) {
                            optClass = 'correct'
                          }
                        }

                        return (
                          <button
                            key={letter}
                            className={`option-button ${optClass}`}
                            style={{ padding: '0.6rem 1rem', fontSize: '0.9rem' }}
                            disabled={answered}
                            onClick={() => setBookmarkAnswers(prev => ({ ...prev, [q.id]: letter }))}
                          >
                            <strong>({letter})</strong> {text}
                          </button>
                        )
                      })}
                    </div>

                    {answered && (
                      <div className="explanation-box animate-fade-in" style={{ marginTop: '0.5rem' }}>
                        <div className="explanation-title" style={{ display: 'flex', justifyContent: 'space-between' }}>
                          <span>💡 詳解對照</span>
                          <button 
                            className="btn btn-secondary btn-sm"
                            style={{ padding: '0.2rem', fontSize: '0.7rem' }}
                            onClick={() => setBookmarkAnswers(prev => {
                              const updated = { ...prev }
                              delete updated[q.id]
                              return updated
                            })}
                          >
                            重新回答
                          </button>
                        </div>
                        <div className="explanation-text" style={{ color: 'var(--text-secondary)' }}>
                          答案：<strong>{q.answer.replace('ALL', '一律給分')}</strong>
                          {q.note && <div style={{ color: 'var(--warning)', marginTop: '0.25rem', fontWeight: 'bold' }}>更正備註：{q.note}</div>}
                        </div>
                        <BookExplanation q={q} />
                      </div>
                    )}

                    {/* Personal User Note */}
                    <UserNoteBox questionId={q.id} userNotes={userNotes} onSaveNote={handleSaveUserNote} />
                  </div>
                )
              })}
            </div>
          </div>
        )}
      </div>
    )
  }

  // Wrong Questions (錯題本) Renderer
  const renderReview = () => {
    const wrongList = questionsData.filter(q => wrongQuestions.includes(q.id))
    const filteredWrong = wrongFilterSubject === 'all' 
      ? wrongList 
      : wrongList.filter(q => q.subject === wrongFilterSubject || getQuestionSubspecialty(q) === wrongFilterSubject)

    // Handle Wrong Question Retry
    const handleRetryWrong = (questionId, letter, correctAnswer) => {
      const qObj = questionsData.find(q => q.id === questionId)
      const correct = isAnswerCorrect(qObj, letter)
      
      setWrongAnswers(prev => ({
        ...prev,
        [questionId]: {
          selected: letter,
          isCorrect: correct
        }
      }))
    }

    return (
      <div className="wrong-questions-layout animate-fade-in">
        {/* Filter Sidebar */}
        <div className="filter-sidebar">
          <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div>
              <h4 className="filter-section-title" style={{ marginBottom: '0.5rem' }}>錯題分類篩選</h4>
              <button 
                className={`filter-btn ${wrongFilterSubject === 'all' ? 'active' : ''}`}
                style={{ width: '100%', marginBottom: '0.5rem', fontWeight: 'bold' }}
                onClick={() => setWrongFilterSubject('all')}
              >
                全部錯題 ({wrongList.length})
              </button>
            </div>

            {/* Filter by Exam Subject */}
            <div>
              <h5 style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '0.4rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.2rem' }}>
                📋 國考大科
              </h5>
              <div className="filter-list" style={{ gap: '0.25rem' }}>
                {subjectsList.map(subject => {
                  const count = wrongList.filter(q => q.subject === subject).length
                  if (count === 0) return null
                  return (
                    <button
                      key={subject}
                      className={`filter-btn ${wrongFilterSubject === subject ? 'active' : ''}`}
                      style={{ fontSize: '0.82rem', padding: '0.35rem 0.6rem' }}
                      onClick={() => setWrongFilterSubject(subject)}
                    >
                      {subject} ({count})
                    </button>
                  )
                })}
              </div>
            </div>

            {/* Filter by Subspecialty / Department */}
            {SUBSPECIALTY_GROUPS.map(group => {
              const availableItems = group.items.filter(item => {
                return wrongList.some(q => getQuestionSubspecialty(q) === item)
              })

              if (availableItems.length === 0) return null

              return (
                <div key={group.category}>
                  <h5 style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '0.4rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.2rem' }}>
                    {group.category}
                  </h5>
                  <div className="filter-list" style={{ gap: '0.25rem' }}>
                    {availableItems.map(item => {
                      const count = wrongList.filter(q => getQuestionSubspecialty(q) === item).length
                      return (
                        <button
                          key={item}
                          className={`filter-btn ${wrongFilterSubject === item ? 'active' : ''}`}
                          style={{ fontSize: '0.82rem', padding: '0.35rem 0.6rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}
                          onClick={() => setWrongFilterSubject(item)}
                        >
                          <span>{item}</span>
                          <span style={{ fontSize: '0.75rem', opacity: 0.8 }}>({count})</span>
                        </button>
                      )
                    })}
                  </div>
                </div>
              )
            })}
          </div>
        </div>

        {/* Wrong Questions List */}
        <div className="wrong-list">
          <div className="card" style={{ padding: '1rem 1.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.5rem' }}>
            <div>
              <h3 style={{ margin: 0, fontSize: '1.1rem' }}>
                錯題清單 - {wrongFilterSubject === 'all' ? '全部科別' : wrongFilterSubject} ({filteredWrong.length} 題)
              </h3>
              <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>答對後題目會繼續保留在錯題本中，需要時可點選「移出錯題本」</span>
            </div>
            {wrongFilterSubject !== 'all' && (
              <button 
                className="btn btn-secondary btn-sm"
                onClick={() => setWrongFilterSubject('all')}
              >
                顯示全部錯題
              </button>
            )}
          </div>

          {filteredWrong.length === 0 ? (
            <div className="card" style={{ textAlign: 'center', padding: '3rem', marginTop: '1rem' }}>
              <p style={{ color: 'var(--text-tertiary)', fontSize: '1.1rem' }}>🎉 太棒了！【{wrongFilterSubject}】目前沒有錯題</p>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginTop: '1rem' }}>
              {filteredWrong.map((q) => {
                const retryState = wrongAnswers[q.id]
                const answered = retryState !== undefined
                const subspec = getQuestionSubspecialty(q)

                return (
                  <div key={q.id} className="card wrong-item-card">
                    <div className="wrong-item-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.75rem', flexWrap: 'wrap', gap: '0.5rem' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', flexWrap: 'wrap' }}>
                        <span className="tag tag-green" style={{ backgroundColor: 'var(--success-light)', color: 'var(--success)', fontWeight: 600 }}>
                          🩺 {subspec}
                        </span>
                        <span className="tag tag-blue">{q.year}年 / {q.subject}</span>
                        <span className="tag tag-red">Q{q.number}</span>
                      </div>
                      <button 
                        className="btn btn-secondary" 
                        style={{ padding: '0.25rem 0.5rem', fontSize: '0.8rem', color: 'var(--danger)' }}
                        onClick={() => {
                          setWrongQuestions(prev => prev.filter(id => id !== q.id))
                        }}
                      >
                        移出錯題本
                      </button>
                    </div>

                    <div className="question-text" style={{ fontSize: '1.05rem', marginBottom: '1rem' }}>
                      {q.text}
                    </div>

                    {q.images && q.images.length > 0 && (
                      <div style={{ marginBottom: '1rem', display: 'flex', gap: '0.5rem' }}>
                        {q.images.map((imgSrc, imgIdx) => (
                          <img 
                            key={imgIdx}
                            src={imgSrc}
                            alt={`錯題附圖`}
                            style={{ maxWidth: '100%', maxHeight: '200px', objectFit: 'contain', borderRadius: '4px', border: '1px solid var(--border-color)' }}
                          />
                        ))}
                      </div>
                    )}

                    <div className="options-list">
                      {Object.entries(q.options).map(([letter, text]) => {
                        let optClass = ''
                        if (answered) {
                          const isCorrectOpt = isAnswerCorrect(q, letter)
                          if (letter === retryState.selected) {
                            optClass = retryState.isCorrect ? 'correct' : 'incorrect'
                          } else if (isCorrectOpt) {
                            optClass = 'correct'
                          }
                        }

                        return (
                          <button
                            key={letter}
                            className={`option-button ${optClass}`}
                            style={{ padding: '0.6rem 1rem', fontSize: '0.9rem' }}
                            disabled={answered}
                            onClick={() => handleRetryWrong(q.id, letter, q.answer)}
                          >
                            <strong>({letter})</strong> {text}
                          </button>
                        )
                      })}
                    </div>

                    {answered && (
                      <div className="explanation-box" style={{ marginTop: '0.5rem' }}>
                        <div className="explanation-title" style={{ display: 'flex', justifyContent: 'space-between' }}>
                          <span>💡 詳解對照</span>
                          {retryState.isCorrect ? (
                            <span style={{ color: 'var(--success)' }}>✓ 答對了！題目保留在錯題本中</span>
                          ) : (
                            <span style={{ color: 'var(--danger)' }}>✕ 答錯了，請溫習相關說明</span>
                          )}
                        </div>
                        <div className="explanation-text" style={{ color: 'var(--text-secondary)' }}>
                          正確答案為：<strong>{q.answer.replace('ALL', '一律給分')}</strong>
                          {q.note && <div style={{ color: 'var(--warning)', marginTop: '0.25rem', fontWeight: 'bold' }}>更正備註：{q.note}</div>}
                        </div>
                        <BookExplanation q={q} />
                      </div>
                    )}

                    {/* Personal User Note */}
                    <UserNoteBox questionId={q.id} userNotes={userNotes} onSaveNote={handleSaveUserNote} />
                  </div>
                )
              })}
            </div>
          )}
        </div>
      </div>
    )
  }

  return (
    <div className="app-container">
      <header className="app-navbar">
        <div className="brand" onClick={() => {
          setCurrentPage('dashboard')
          setCurrentExam(null)
          setSelectedYearTerm(null)
        }}>
          🩺 醫師二階國考模擬平台
        </div>
        <nav className="nav-links">
          <button 
            className={`nav-item ${currentPage === 'dashboard' ? 'active' : ''}`}
            onClick={() => {
              setCurrentPage('dashboard')
              setCurrentExam(null)
              setSelectedYearTerm(null)
            }}
          >
            儀表板
          </button>
          <button 
            className={`nav-item ${currentPage === 'search' ? 'active' : ''}`}
            onClick={() => {
              setCurrentPage('search')
              setCurrentExam(null)
              setSelectedYearTerm(null)
            }}
          >
            題庫搜尋
          </button>
          <button 
            className={`nav-item ${currentPage === 'review' ? 'active' : ''}`}
            onClick={() => {
              setWrongAnswers({})
              setCurrentPage('review')
              setCurrentExam(null)
              setSelectedYearTerm(null)
            }}
          >
            錯題本 ({wrongQuestions.length})
          </button>
          <button className="theme-toggle-btn" onClick={toggleTheme} aria-label="切換主題" style={{ background: 'none', border: 'none', cursor: 'pointer', fontSize: '1.2rem', padding: '0 0.5rem' }}>
            {theme === 'light' ? '🌙' : '☀️'}
          </button>
        </nav>
      </header>

      <main className="main-content">
        {currentPage === 'dashboard' && renderDashboard()}
        {currentPage === 'exam' && renderExam()}
        {currentPage === 'result' && renderResult()}
        {currentPage === 'review' && renderReview()}
        {currentPage === 'search' && renderSearch()}
        {currentPage === 'bookmarks' && renderBookmarks()}
      </main>

      {/* Modal for selecting subject */}
      {selectedYearTerm && (
        <div className="modal-overlay animate-fade-in" onClick={() => setSelectedYearTerm(null)}>
          <div className="card modal-content" onClick={e => e.stopPropagation()} style={{ maxWidth: '650px', width: '100%' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.75rem' }}>
              <h3 style={{ fontSize: '1.2rem' }}>📅 {selectedYearTerm.replace('-', '年第')}次專技高考二階 試題</h3>
              <button 
                className="btn btn-secondary" 
                style={{ padding: '0.25rem 0.5rem', fontSize: '0.85rem' }} 
                onClick={() => setSelectedYearTerm(null)}
              >
                ✕ 關閉
              </button>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {subjectsList.map(subject => {
                const count = questionsData.filter(q => q.year === selectedYearTerm && q.subject === subject).length
                if (count === 0) return null
                return (
                  <div key={subject} className="subject-item" style={{ padding: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', cursor: 'default' }}>
                    <div style={{ flex: 1, paddingRight: '1rem' }}>
                      <span className="subject-name" style={{ fontSize: '1rem', color: 'var(--text-primary)' }}>{subject}</span>
                      <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '0.25rem', lineHeight: '1.4' }}>
                        {subject === '醫學(三)' && '內科、家庭醫學科等科目及其臨床實例與醫學倫理'}
                        {subject === '醫學(四)' && '小兒科、皮膚科、神經科、精神科等科目及其臨床實例與醫學倫理'}
                        {subject === '醫學(五)' && '外科、骨科、泌尿科等科目及其臨床實例與醫學倫理'}
                        {subject === '醫學(六)' && '麻醉科、眼科、耳鼻喉科、婦產科、復健科等科目及其臨床實例與醫學倫理'}
                      </p>
                      <span className="question-meta-badge" style={{ marginTop: '0.5rem', display: 'inline-block', fontSize: '0.75rem' }}>共 {count} 題</span>
                    </div>
                    <div style={{ display: 'flex', gap: '0.5rem', flexShrink: 0 }}>
                      <button className="btn btn-secondary btn-sm" onClick={() => {
                        startSession(selectedYearTerm, subject, 'practice')
                        setSelectedYearTerm(null)
                      }}>循序練習</button>
                      <button className="btn btn-primary btn-sm" onClick={() => {
                        startSession(selectedYearTerm, subject, 'exam')
                        setSelectedYearTerm(null)
                      }}>模擬考試</button>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default App
