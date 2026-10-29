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
// Map questions to medical subspecialties (32 Chapters across 4 Sections)
const getQuestionSubspecialty = (q) => {
  if (!q) return '一般外科'
  if (q.chapter) return q.chapter
  if (q.category) return q.category
  return '一般外科'
}

const SUBSPECIALTY_GROUPS = [
  {
    category: '📖 第一篇 內科學',
    items: ['心臟內科', '胸腔內科', '肝膽腸胃科', '腎臟科', '血液腫瘤科', '新陳代謝科', '感染科', '免疫風濕科', '神經內科', '急診內科']
  },
  {
    category: '🔪 第二篇 外科學',
    items: ['外科概論', '一般外科', '心臟外科', '大腸直腸科', '整形外科', '胸腔外科', '神經外科', '小兒外科', '急診外傷科', '移植科']
  },
  {
    category: '👶 第三篇 婦兒科',
    items: ['小兒科', '婦產科']
  },
  {
    category: '🩺 第四篇 其他科',
    items: ['家庭醫學科', '皮膚科', '精神科', '骨科', '泌尿科', '麻醉科', '眼科', '耳鼻喉科', '復健科', '醫學倫理與醫療決策']
  }
]

// Marker / Flag types for exam navigation (三角形、正方形、圓形)
const FLAG_TYPES = [
  { key: 'triangle', icon: '▲', label: '三角形', color: '#f59e0b', bg: 'rgba(245, 158, 11, 0.12)', border: '#f59e0b' },
  { key: 'square', icon: '■', label: '正方形', color: '#ec4899', bg: 'rgba(236, 72, 153, 0.12)', border: '#ec4899' },
  { key: 'circle', icon: '●', label: '圓形', color: '#10b981', bg: 'rgba(16, 185, 129, 0.12)', border: '#10b981' },
]

const FLAG_MAP = {
  triangle: FLAG_TYPES[0],
  square: FLAG_TYPES[1],
  circle: FLAG_TYPES[2],
  // Backward compatibility
  flag: FLAG_TYPES[0],
  doubt: FLAG_TYPES[0],
  trap: FLAG_TYPES[1],
  star: FLAG_TYPES[2],
  true: FLAG_TYPES[0]
}

// Helper to extract official exam title and meta for PDF export
const getExamTitleMeta = (exam) => {
  const yearStr = exam?.year || '113-2'
  const parts = yearStr.split('-')
  const yearNum = parts[0] || '113'
  const termNum = parts[1] === '1' ? '一' : '二'
  
  const title = `${yearNum}年第${termNum}次專門職業及技術人員高等考試醫師牙醫師中醫師藥師考試分階段考試、醫事檢驗師、醫事放射師、物理治療師考試`
  
  const subject = exam?.subject || '醫學(三)'
  
  let code = '1301'
  let category = '醫師(二)'
  let fullSubjectName = `${subject}`
  
  if (subject.includes('醫學(一)')) {
    code = '1101'
    category = '醫師(一)'
    fullSubjectName = '醫學（一）（包括解剖學、胚胎學、組織學、生理學、生物化學等科目知識及其臨床之應用）'
  } else if (subject.includes('醫學(二)')) {
    code = '1102'
    category = '醫師(一)'
    fullSubjectName = '醫學（二）（包括微生物學、免疫學、寄生蟲學、藥理學、病理學、公共衛生學等科目知識及其臨床之應用）'
  } else if (subject.includes('醫學(三)')) {
    code = '1301'
    category = '醫師(二)'
    fullSubjectName = '醫學（三）（包括內科、家庭醫學科等科目知識及其臨床之應用）'
  } else if (subject.includes('醫學(四)')) {
    code = '1302'
    category = '醫師(二)'
    fullSubjectName = '醫學（四）（包括小兒科、皮膚科、神經科、精神科等科目知識及其臨床之應用）'
  } else if (subject.includes('醫學(五)')) {
    code = '1303'
    category = '醫師(二)'
    fullSubjectName = '醫學（五）（包括外科、骨科、泌尿科等科目知識及其臨床之應用）'
  } else if (subject.includes('醫學(六)')) {
    code = '1304'
    category = '醫師(二)'
    fullSubjectName = '醫學（六）（包括麻醉科、眼科、耳鼻喉科、婦產科、復健科等科目知識及其臨床之應用）'
  }
  
  return { title, code, category, fullSubjectName }
}

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
  const cleaned = str
    .replace(/\\text\{([^}]+)\}/g, '$1')
    .replace(/\$?(\\ge|\\geq)\$?/g, '≥')
    .replace(/\$?(\\le|\\leq)\$?/g, '≤')
    .replace(/\$?(\\times)\$?/g, '×')
    .replace(/\$?(\\rightarrow)\$?/g, '→')
    .replace(/\$?(\\mu)\$?/g, 'μ')
    .replace(/\$?(\\Delta)\$?/g, 'Δ')
    .replace(/\$?(\\pm)\$?/g, '±')
    .replace(/\\\*/g, '*')
    .replace(/\$([^$\n]+)\$/g, '$1')

  const brParts = cleaned.split(/<br\s*\/?>/gi)
  return brParts.map((sub, brIdx) => {
    const parts = sub.split(/(\*\*.*?\*\*)/g)
    const rendered = parts.map((part, i) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return <strong key={i}>{part.slice(2, -2)}</strong>
      }
      return part
    })
    return (
      <span key={brIdx}>
        {rendered}
        {brIdx < brParts.length - 1 && <br />}
      </span>
    )
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
                  {rows.map((row, rIdx) => {
                    const colSpanForLast = row.length < headers.length ? headers.length - row.length + 1 : 1
                    return (
                      <tr key={rIdx} style={{ borderBottom: '1px solid var(--border-color)', background: rIdx % 2 === 1 ? 'var(--bg-secondary)' : 'transparent' }}>
                        {row.map((cell, cIdx) => {
                          const colSpan = cIdx === row.length - 1 ? colSpanForLast : 1
                          return (
                            <td key={cIdx} colSpan={colSpan} style={{ padding: '0.5rem 0.75rem' }}>
                              {formatInlineMarkdown(cell)}
                            </td>
                          )
                        })}
                      </tr>
                    )
                  })}
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

  useEffect(() => {
    setImgError(false)
    setActivePageIdx(0)
  }, [q?.id, q?.explanation_image, q?.explanation_images])
  
  const hasTextExplanation = !!q.explanation
  const explanationPages = q.explanation_pages || []
  
  const lookupKey = `${q.year}-${q.subject}-${q.number}`
  const fallbackPageNum = explanationsMap[lookupKey]
  const pagesToRender = explanationPages.length > 0 
    ? explanationPages 
    : (fallbackPageNum ? [fallbackPageNum] : [])
    
  const croppedImages = q.explanation_images || (q.explanation_image ? [q.explanation_image] : [])
  const hasCroppedImage = croppedImages.length > 0 && !imgError

  // Show image container if cropped images exist, or fallback page scans for legacy exams
  const isExcludedSubject = 
    ['111-1', '111-2', '112-1', '112-2', '113-1', '113-2'].includes(q.year)
  const showImageContainer = hasCroppedImage || (!isExcludedSubject && pagesToRender.length > 0)
  
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

  // When there is no note and not editing, only show "+ 新增筆記" button
  if (!note && !isEditing) {
    return (
      <div style={{ marginTop: '0.75rem', display: 'flex', justifyContent: 'flex-start' }}>
        <button 
          className="btn btn-secondary btn-sm"
          style={{ 
            padding: '0.3rem 0.7rem', 
            fontSize: '0.8rem', 
            borderRadius: '6px',
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.35rem',
            color: 'var(--text-secondary)',
            border: '1px dashed var(--border-color)',
            background: 'var(--bg-tertiary)'
          }}
          onClick={() => {
            setEditingText('')
            setIsEditing(true)
          }}
        >
          ➕ 新增筆記
        </button>
      </div>
    )
  }

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
            ✏️ 編輯筆記
          </button>
        )}
      </div>

      {isEditing ? (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          <textarea
            autoFocus
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
            placeholder="在此輸入您個人的重點筆記、記憶口訣或觀念補充..."
            value={editingText}
            onChange={(e) => setEditingText(e.target.value)}
          />
          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.4rem' }}>
            <button 
              className="btn btn-secondary btn-sm"
              style={{ padding: '0.2rem 0.5rem', fontSize: '0.75rem' }}
              onClick={() => {
                setEditingText(note)
                setIsEditing(false)
              }}
            >
              取消
            </button>
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
                onSaveNote(questionId, editingText.trim())
                setIsEditing(false)
              }}
            >
              儲存筆記
            </button>
          </div>
        </div>
      ) : (
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
  const [bookmarks, setBookmarks] = useState(() => getLocalStorage('med-exam-bookmarks', []))
  
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
  const [wrongFilterYear, setWrongFilterYear] = useState('all')

  // Result page filter state ('all' | 'wrong' | 'correct' | specific chapter name)
  const [resultFilter, setResultFilter] = useState('all')

  // Clear usage records modal and toast state
  const [showClearModal, setShowClearModal] = useState(false)
  const [clearOptions, setClearOptions] = useState({
    history: true,
    wrong: true,
    notes: true,
    bookmarks: true
  })
  const [toastMessage, setToastMessage] = useState('')

  // PDF Export Modal State
  const [showPdfExport, setShowPdfExport] = useState(false)
  const [pdfExamData, setPdfExamData] = useState(null)

  const handleOpenPdfExport = (examRecord = currentExam) => {
    if (!examRecord) return
    setPdfExamData(examRecord)
    setShowPdfExport(true)
  }

  // 考選部 CBT 模式狀態
  const [cbtMode, setCbtMode] = useState(() => getLocalStorage('med-exam-cbt-mode', false))
  const [cbtFontSize, setCbtFontSize] = useState(() => getLocalStorage('med-exam-cbt-fontsize', 'md'))
  const [eliminatedOptions, setEliminatedOptions] = useState({}) // { [questionId]: ['A', 'B'] }
  const [isFullscreen, setIsFullscreen] = useState(false)

  useEffect(() => {
    localStorage.setItem('med-exam-cbt-mode', JSON.stringify(cbtMode))
  }, [cbtMode])

  useEffect(() => {
    localStorage.setItem('med-exam-cbt-fontsize', JSON.stringify(cbtFontSize))
  }, [cbtFontSize])

  useEffect(() => {
    const handleFsChange = () => {
      setIsFullscreen(Boolean(document.fullscreenElement))
    }
    document.addEventListener('fullscreenchange', handleFsChange)
    return () => document.removeEventListener('fullscreenchange', handleFsChange)
  }, [])

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

  // Clear usage records handler
  const handleClearRecords = () => {
    const hasSelected = clearOptions.history || clearOptions.wrong || clearOptions.notes || clearOptions.bookmarks
    if (!hasSelected) return

    if (clearOptions.history) {
      setHistory([])
      localStorage.removeItem('med-exam-history')
    }
    if (clearOptions.wrong) {
      setWrongQuestions([])
      setWrongAnswers({})
      localStorage.removeItem('med-exam-wrong')
    }
    if (clearOptions.notes) {
      setUserNotes({})
      localStorage.removeItem('med-exam-user-notes')
    }
    if (clearOptions.bookmarks) {
      setBookmarks([])
      setBookmarkAnswers({})
      localStorage.removeItem('med-exam-bookmarks')
    }

    setShowClearModal(false)
    setToastMessage('已成功清除所選使用紀錄')
    setTimeout(() => {
      setToastMessage('')
    }, 3000)
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

  // Start new exam session
  const startSession = (year, subject, mode = 'exam') => {
    const filtered = questionsData.filter(q => q.year === year && q.subject === subject)
    
    // Sort by question number sequentially
    const sorted = [...filtered].sort((a, b) => a.number - b.number)
    
    if (sorted.length === 0) {
      alert('無此考期的題目資料')
      return
    }

    setEliminatedOptions({})

    setCurrentExam({
      name: `${year}年 ${subject} 測驗`,
      year: year,
      subject: subject,
      questions: sorted,
      currentIndex: 0,
      answers: {}, // { questionId: selectedOption }
      flagged: {}, // { questionId: boolean }
      timeLeft: 120 * 60, // 120 minutes for exam mode
      totalQuestions: sorted.length,
      mode: 'exam'
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

  // Keyboard navigation & shortcuts for CBT & Modern Exam (A/B/C/D, 1/2/3/4, Arrow keys)
  useEffect(() => {
    if (currentPage !== 'exam' || !currentExam) return

    const handleKeyDown = (e) => {
      if (['INPUT', 'TEXTAREA'].includes(e.target.tagName)) return

      const q = currentExam.questions?.[currentExam.currentIndex]
      if (!q) return

      const key = e.key.toUpperCase()
      const keyMap = { '1': 'A', '2': 'B', '3': 'C', '4': 'D', 'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D' }

      if (keyMap[key] && q.options && q.options[keyMap[key]]) {
        handleSelectOption(q.id, keyMap[key])
        return
      }

      if (e.key === 'ArrowLeft') {
        if (currentExam.currentIndex > 0) {
          setCurrentExam(prev => ({ ...prev, currentIndex: prev.currentIndex - 1 }))
        }
      } else if (e.key === 'ArrowRight') {
        if (currentExam.currentIndex < currentExam.totalQuestions - 1) {
          setCurrentExam(prev => ({ ...prev, currentIndex: prev.currentIndex + 1 }))
        }
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [currentPage, currentExam?.currentIndex, currentExam?.questions])

  const handleSelectOption = (questionId, optionLetter) => {
    // Un-eliminate when selected
    setEliminatedOptions(prev => {
      const list = prev[questionId]
      if (list && list.includes(optionLetter)) {
        return { ...prev, [questionId]: list.filter(l => l !== optionLetter) }
      }
      return prev
    })

    setCurrentExam(prev => ({
      ...prev,
      answers: {
        ...prev.answers,
        [questionId]: optionLetter
      }
    }))
  }

  const handleToggleEliminate = (questionId, letter, e) => {
    if (e) {
      e.stopPropagation()
      e.preventDefault()
    }
    setEliminatedOptions(prev => {
      const list = prev[questionId] || []
      if (list.includes(letter)) {
        return { ...prev, [questionId]: list.filter(l => l !== letter) }
      } else {
        return { ...prev, [questionId]: [...list, letter] }
      }
    })
  }

  const handleToggleFullscreen = () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().then(() => setIsFullscreen(true)).catch(() => {})
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen().then(() => setIsFullscreen(false)).catch(() => {})
      }
    }
  }

  const handleSetFlag = (questionId, flagKey) => {
    setCurrentExam(prev => {
      if (!prev) return null
      const currentFlag = prev.flagged?.[questionId]
      const newFlagged = { ...(prev.flagged || {}) }
      
      // If clicking the same flag, toggle it off
      if (currentFlag === flagKey || (flagKey === 'triangle' && (currentFlag === 'flag' || currentFlag === true))) {
        delete newFlagged[questionId]
      } else if (flagKey) {
        newFlagged[questionId] = flagKey
      } else {
        delete newFlagged[questionId]
      }
      
      return {
        ...prev,
        flagged: newFlagged
      }
    })
  }

  const handleToggleFlag = (questionId, flagKey = 'triangle') => {
    handleSetFlag(questionId, flagKey)
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
      questions: examToSubmit.questions,
      flagged: examToSubmit.flagged || {}
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

        {/* Exam Library */}
        <div className="dashboard-sections">
          <div className="card">
            <h3 className="section-card-title">歷屆試題庫</h3>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '1rem' }}>選擇您要挑戰的年度考期，點選進入後可進一步選擇科目進行模擬考試</p>
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
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.5rem', marginBottom: '0.5rem' }}>
              <h3 className="section-card-title" style={{ margin: 0 }}>近期測驗記錄</h3>
              <button 
                className="btn btn-secondary btn-sm"
                style={{ color: 'var(--danger)', fontSize: '0.8rem', padding: '0.25rem 0.6rem', display: 'inline-flex', alignItems: 'center', gap: '0.35rem' }}
                onClick={() => setShowClearModal(true)}
              >
                🗑️ 一鍵清除紀錄
              </button>
            </div>
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
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                      <span className="history-score" style={{ color: record.score >= 60 ? 'var(--success)' : 'var(--danger)', fontSize: '0.9rem' }}>
                        {record.score}分
                      </span>
                      <button className="btn btn-secondary btn-sm" style={{ padding: '0.2rem 0.5rem', fontSize: '0.8rem' }} onClick={() => viewHistoryDetail(record)}>詳解</button>
                      <button 
                        className="btn btn-secondary btn-sm" 
                        style={{ padding: '0.2rem 0.5rem', fontSize: '0.8rem' }} 
                        onClick={(e) => {
                          e.stopPropagation()
                          handleOpenPdfExport(record)
                        }}
                        title="匯出此份試卷 PDF"
                      >
                        匯出PDF
                      </button>
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

  // 考選部 CBT 擬真畫面渲染
  const renderCbtExam = (q, userSelected, currentFlagKey, qEliminated) => {
    const answeredCount = Object.keys(currentExam.answers).length
    const unansweredCount = currentExam.totalQuestions - answeredCount
    
    const fontSizes = {
      sm: { text: '1rem', option: '0.95rem', title: '1.05rem' },
      md: { text: '1.12rem', option: '1.05rem', title: '1.15rem' },
      lg: { text: '1.25rem', option: '1.15rem', title: '1.28rem' }
    }
    const currentFont = fontSizes[cbtFontSize] || fontSizes.md

    return (
      <div className="cbt-fullscreen-wrapper animate-fade-in">
        {/* 考選部經典頂部資訊列 */}
        <div className="cbt-topbar">
          <div className="cbt-topbar-left">
            <span className="cbt-topbar-badge">🏛️ 考選部國家考試電腦化測驗 (CBT)</span>
            <span className="cbt-topbar-info">
              <strong>科目：</strong>{currentExam.subject}
            </span>
            <span className="cbt-topbar-info">
              <strong>題號：</strong>第 {currentExam.currentIndex + 1} / {currentExam.totalQuestions} 題
            </span>
          </div>

          {/* 倒數計時器 */}
          <div className="cbt-topbar-center">
            <div className="cbt-timer-block">
              <span className="cbt-timer-label">剩餘時間</span>
              <span className="cbt-timer-digits" style={{ color: currentExam.timeLeft < 300 ? '#ef4444' : '#22c55e' }}>
                {formatTime(currentExam.timeLeft)}
              </span>
            </div>
          </div>

          {/* 右側操作工具 */}
          <div className="cbt-topbar-right">
            {/* 字體大小切換 */}
            <div className="cbt-font-controls">
              <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>字級:</span>
              <button 
                type="button"
                className={`cbt-font-btn ${cbtFontSize === 'sm' ? 'active' : ''}`}
                onClick={() => setCbtFontSize('sm')}
              >
                小
              </button>
              <button 
                type="button"
                className={`cbt-font-btn ${cbtFontSize === 'md' ? 'active' : ''}`}
                onClick={() => setCbtFontSize('md')}
              >
                中
              </button>
              <button 
                type="button"
                className={`cbt-font-btn ${cbtFontSize === 'lg' ? 'active' : ''}`}
                onClick={() => setCbtFontSize('lg')}
              >
                大
              </button>
            </div>

            {/* 全螢幕切換 */}
            <button 
              type="button"
              className="cbt-action-btn"
              onClick={handleToggleFullscreen}
              title={isFullscreen ? '結束全螢幕' : '全螢幕切換'}
            >
              {isFullscreen ? '⛶ 視窗' : '⛶ 全螢幕'}
            </button>

            {/* 切換現代模式 */}
            <button 
              type="button"
              className="cbt-action-btn"
              onClick={() => setCbtMode(false)}
              title="切換回現代版面"
            >
              🎨 現代版
            </button>

            {/* 離開測驗 */}
            <button 
              type="button"
              className="cbt-action-btn"
              onClick={() => {
                if (window.confirm('確定要中途離開測驗並返回儀表板嗎？（未交卷將不記錄成績）')) {
                  setCurrentPage('dashboard')
                  setCurrentExam(null)
                  setSelectedYearTerm(null)
                }
              }}
              title="中途結束測驗返回儀表板"
              style={{ color: '#cbd5e1' }}
            >
              ✕ 離開
            </button>

            {/* 提前交卷按鈕 */}
            <button 
              type="button"
              className="cbt-submit-btn"
              onClick={() => {
                if (window.confirm('確定要提前交卷結束考試嗎？')) {
                  handleSubmitExam()
                }
              }}
            >
              提前交卷
            </button>
          </div>
        </div>

        {/* 考選部主畫面佈局：左側作答區、右側 80 題試題導覽 */}
        <div className="cbt-body-layout">
          {/* 左側題目卡片 */}
          <div className="cbt-question-panel">
            <div className="cbt-panel-header">
              <div className="cbt-q-number-title" style={{ fontSize: currentFont.title }}>
                【題號 {currentExam.currentIndex + 1}】 (單選題)
              </div>

              {/* 標記此題工具 */}
              <div className="cbt-flag-selector">
                <span style={{ fontSize: '0.8rem', color: '#475569', fontWeight: 600 }}>標記:</span>
                {FLAG_TYPES.map(f => {
                  const isSelected = currentFlagKey === f.key || (f.key === 'triangle' && (currentFlagKey === 'flag' || currentFlagKey === true))
                  return (
                    <button
                      key={f.key}
                      type="button"
                      className={`cbt-flag-btn ${isSelected ? 'active' : ''}`}
                      style={isSelected ? {
                        backgroundColor: f.bg,
                        borderColor: f.color,
                        color: f.color
                      } : {}}
                      onClick={() => handleSetFlag(q.id, f.key)}
                      title={isSelected ? `取消標記` : `標記 ${f.icon}`}
                    >
                      <span>{f.icon}</span>
                    </button>
                  )
                })}
                {currentFlagKey && (
                  <button
                    type="button"
                    className="cbt-flag-clear"
                    onClick={() => handleSetFlag(q.id, null)}
                    title="清除標記"
                  >
                    ✕
                  </button>
                )}
              </div>
            </div>

            {/* 題目內文 */}
            <div className="cbt-question-content" style={{ fontSize: currentFont.text }}>
              <div className="cbt-question-stem">
                {q.text}
              </div>

              {/* 題目圖片 */}
              {q.images && q.images.length > 0 && (
                <div className="cbt-question-images">
                  {q.images.map((imgSrc, idx) => (
                    <img 
                      key={idx}
                      src={imgSrc}
                      alt={`題目附圖 ${idx + 1}`}
                      className="cbt-img-preview"
                    />
                  ))}
                </div>
              )}

              {/* 選項列表 (CBT Radio Style with Strikethrough) */}
              <div className="cbt-options-list">
                {Object.entries(q.options).map(([letter, text]) => {
                  const isSelected = userSelected === letter
                  const isEliminated = qEliminated.includes(letter)

                  return (
                    <div
                      key={letter}
                      className={`cbt-option-row ${isSelected ? 'selected' : ''} ${isEliminated ? 'eliminated' : ''}`}
                      onClick={() => handleSelectOption(q.id, letter)}
                      onContextMenu={(e) => handleToggleEliminate(q.id, letter, e)}
                    >
                      <div className="cbt-radio-icon">
                        {isSelected ? '●' : '○'}
                      </div>
                      <div className="cbt-option-text" style={{ fontSize: currentFont.option }}>
                        <span className="cbt-option-letter">({letter})</span>
                        <span className="cbt-option-body">{text}</span>
                      </div>
                      <button
                        type="button"
                        className={`cbt-eliminate-btn ${isEliminated ? 'active' : ''}`}
                        onClick={(e) => handleToggleEliminate(q.id, letter, e)}
                        title={isEliminated ? '復原此選項' : '刪去此選項 (亦可右鍵點選)'}
                      >
                        {isEliminated ? '復原' : '✕'}
                      </button>
                    </div>
                  )
                })}
              </div>

              {/* 鍵盤操作指引提示 */}
              <div className="cbt-keyboard-hint">
                💡 快速鍵提示：鍵盤按 <strong>A / B / C / D</strong> 或 <strong>1 / 2 / 3 / 4</strong> 選答；<strong>← / →</strong> 切換題號；對選項點右鍵或點 ✕ 可劃掉刪去選項
              </div>
            </div>

            {/* 底部導覽控制列 */}
            <div className="cbt-panel-footer">
              <button
                type="button"
                className="cbt-nav-btn"
                disabled={currentExam.currentIndex === 0}
                onClick={() => setCurrentExam(prev => ({ ...prev, currentIndex: prev.currentIndex - 1 }))}
              >
                ◀ 上一題
              </button>

              <button
                type="button"
                className="cbt-nav-btn cbt-submit-footer-btn"
                onClick={() => {
                  if (window.confirm('確定要提前交卷嗎？')) {
                    handleSubmitExam()
                  }
                }}
              >
                交卷
              </button>

              {currentExam.currentIndex === currentExam.totalQuestions - 1 ? (
                <button 
                  type="button"
                  className="cbt-nav-btn cbt-primary-nav" 
                  onClick={() => handleSubmitExam()}
                >
                  交卷
                </button>
              ) : (
                <button
                  type="button"
                  className="cbt-nav-btn cbt-primary-nav"
                  onClick={() => setCurrentExam(prev => ({ ...prev, currentIndex: prev.currentIndex + 1 }))}
                >
                  下一題 ▶
                </button>
              )}
            </div>
          </div>

          {/* 右側 80 題快速導覽面板 */}
          <div className="cbt-sidebar-panel">
            <div className="cbt-sidebar-header">
              <h4>試題總覽 ({currentExam.totalQuestions}題)</h4>
              <div className="cbt-status-summary">
                <span className="cbt-stat-tag answered">已答: {answeredCount}</span>
                <span className="cbt-stat-tag unanswered">未答: {unansweredCount}</span>
              </div>
            </div>

            <div className="cbt-palette-grid">
              {currentExam.questions.map((question, idx) => {
                const answered = currentExam.answers[question.id] !== undefined
                const flagKey = currentExam.flagged?.[question.id]
                const flagInfo = flagKey ? (FLAG_MAP[flagKey] || FLAG_MAP['triangle']) : null
                const current = currentExam.currentIndex === idx

                let btnClass = ''
                if (answered) btnClass += ' answered'
                if (flagInfo) btnClass += ' has-flag'
                if (current) btnClass += ' current'

                return (
                  <button
                    key={question.id}
                    className={`cbt-palette-btn ${btnClass}`}
                    style={flagInfo ? { borderColor: flagInfo.color } : {}}
                    onClick={() => setCurrentExam(prev => ({ ...prev, currentIndex: idx }))}
                    title={`第 ${idx + 1} 題${answered ? ' (已答)' : ' (未答)'}${flagInfo ? ` [${flagInfo.icon}]` : ''}`}
                  >
                    <span className="cbt-palette-num">{idx + 1}</span>
                    {flagInfo && (
                      <span className="cbt-palette-flag" style={{ color: flagInfo.color }}>
                        {flagInfo.icon}
                      </span>
                    )}
                  </button>
                )
              })}
            </div>

            {/* 標記統計圖例 */}
            <div className="cbt-sidebar-legend">
              <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap', marginBottom: '0.5rem' }}>
                <span className="cbt-legend-item"><span className="cbt-legend-box answered"></span> 已作答</span>
                <span className="cbt-legend-item"><span className="cbt-legend-box unanswered"></span> 未作答</span>
                <span className="cbt-legend-item"><span className="cbt-legend-box current"></span> 目前題</span>
              </div>
              <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap' }}>
                {FLAG_TYPES.map(f => {
                  const count = currentExam.questions.filter(q => {
                    const fl = currentExam.flagged?.[q.id]
                    return fl === f.key || (f.key === 'triangle' && (fl === 'flag' || fl === true))
                  }).length
                  return (
                    <span key={f.key} className="cbt-legend-flag" style={{ color: f.color }}>
                      {f.icon} {count}
                    </span>
                  )
                })}
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  // 現代簡潔模式渲染
  const renderModernExam = (q, userSelected, currentFlagKey, qEliminated) => {
    return (
      <div className="exam-layout animate-fade-in">
        <div className="card question-card">
          <div className="question-header">
            <div>
              <span className="question-meta-badge" style={{ marginRight: '0.5rem' }}>{currentExam.name}</span>
              <span className="question-meta-badge">第 {currentExam.currentIndex + 1} / {currentExam.totalQuestions} 題</span>
            </div>
            <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center', flexWrap: 'wrap' }}>
              <button
                type="button"
                className="btn btn-secondary btn-sm"
                style={{ display: 'inline-flex', alignItems: 'center', gap: '0.3rem', fontSize: '0.8rem', padding: '0.35rem 0.65rem' }}
                onClick={() => setCbtMode(true)}
                title="切換為考選部電腦化測驗 (CBT) 擬真介面"
              >
                <span>🏛️</span> 考選部模式
              </button>

              <div className="flag-toolbar">
                {FLAG_TYPES.map(f => {
                  const isSelected = currentFlagKey === f.key || (f.key === 'triangle' && (currentFlagKey === 'flag' || currentFlagKey === true))
                  return (
                    <button
                      key={f.key}
                      type="button"
                      className={`flag-toolbar-btn ${isSelected ? 'active' : ''}`}
                      style={isSelected ? {
                        backgroundColor: f.bg,
                        borderColor: f.color,
                        color: f.color
                      } : {}}
                      onClick={() => handleSetFlag(q.id, f.key)}
                      title={isSelected ? `取消標記` : `標記 ${f.icon}`}
                    >
                      <span style={{ fontSize: '0.95rem' }}>{f.icon}</span>
                    </button>
                  )
                })}
                {currentFlagKey && (
                  <button
                    type="button"
                    className="flag-toolbar-clear"
                    onClick={() => handleSetFlag(q.id, null)}
                    title="清除標記"
                  >
                    ✕
                  </button>
                )}
              </div>
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
                const isSelected = userSelected === letter
                const isEliminated = qEliminated.includes(letter)

                return (
                  <div key={letter} style={{ position: 'relative', display: 'flex', alignItems: 'center' }}>
                    <button
                      className={`option-button ${isSelected ? 'selected' : ''}`}
                      style={isEliminated ? { textDecoration: 'line-through', opacity: 0.45 } : {}}
                      onClick={() => handleSelectOption(q.id, letter)}
                      onContextMenu={(e) => handleToggleEliminate(q.id, letter, e)}
                    >
                      <strong style={{ marginRight: '0.5rem' }}>({letter})</strong> {text}
                    </button>
                    <button
                      type="button"
                      onClick={(e) => handleToggleEliminate(q.id, letter, e)}
                      style={{
                        position: 'absolute',
                        right: '12px',
                        background: 'transparent',
                        border: 'none',
                        color: isEliminated ? 'var(--danger)' : 'var(--text-tertiary)',
                        cursor: 'pointer',
                        fontSize: '0.75rem',
                        padding: '4px',
                        zIndex: 2
                      }}
                      title={isEliminated ? '復原此選項' : '刪去此選項 (亦可右鍵點選)'}
                    >
                      {isEliminated ? '復原' : '✕'}
                    </button>
                  </div>
                )
              })}
            </div>

            <div style={{ fontSize: '0.75rem', color: 'var(--text-tertiary)', marginTop: '0.5rem', textAlign: 'right' }}>
              💡 提示：按鍵盤 A/B/C/D 選答、←/→ 換題，對選項右鍵可劃線刪去
            </div>
          </div>

          <div className="question-footer">
            <button
              className="btn btn-secondary"
              disabled={currentExam.currentIndex === 0}
              onClick={() => setCurrentExam(prev => ({ ...prev, currentIndex: prev.currentIndex - 1 }))}
            >
              上一題
            </button>
            
            <button className="btn btn-danger" onClick={() => {
              if (window.confirm('確定要退出考試交卷嗎？')) {
                handleSubmitExam()
              }
            }}>
              交卷
            </button>

            {currentExam.currentIndex === currentExam.totalQuestions - 1 ? (
              <button className="btn btn-primary" onClick={() => handleSubmitExam()}>
                交卷
              </button>
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
          <div className="card timer-card glass-card">
            <h4>剩餘時間</h4>
            <div className="timer-display" style={{ color: currentExam.timeLeft < 180 ? 'var(--danger)' : 'var(--text-primary)' }}>
              {formatTime(currentExam.timeLeft)}
            </div>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>考試進行中</p>
          </div>

          <div className="card" style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
              <h4 style={{ margin: 0, fontSize: '0.95rem' }}>題目導覽</h4>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                {Object.keys(currentExam.answers).length} / {currentExam.totalQuestions} 已答
              </span>
            </div>

            <div className="question-nav-grid" style={{ gridTemplateColumns: 'repeat(5, 1fr)' }}>
              {currentExam.questions.map((question, idx) => {
                const answered = currentExam.answers[question.id] !== undefined
                const flagKey = currentExam.flagged?.[question.id]
                const flagInfo = flagKey ? (FLAG_MAP[flagKey] || FLAG_MAP['triangle']) : null
                const current = currentExam.currentIndex === idx
                
                let btnClass = ''
                if (answered) btnClass += ' answered'
                if (flagInfo) btnClass += ' has-flag'
                if (current) btnClass += ' current'

                return (
                  <button
                    key={question.id}
                    className={`nav-grid-btn ${btnClass}`}
                    style={flagInfo ? { borderColor: flagInfo.color } : {}}
                    onClick={() => setCurrentExam(prev => ({ ...prev, currentIndex: idx }))}
                    title={`第 ${idx + 1} 題${answered ? ' (已作答)' : ' (未作答)'}${flagInfo ? ` [${flagInfo.icon} ${flagInfo.label}]` : ''}`}
                  >
                    <span className="nav-btn-num">{idx + 1}</span>
                    {flagInfo && (
                      <span className="nav-btn-flag" style={{ color: flagInfo.color }}>
                        {flagInfo.icon}
                      </span>
                    )}
                  </button>
                )
              })}
            </div>

            {/* Status Legend & Flag Breakdown */}
            <div style={{ marginTop: '1rem', borderTop: '1px solid var(--border-color)', paddingTop: '0.75rem', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              <div style={{ display: 'flex', gap: '0.6rem', flexWrap: 'wrap', fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                <span style={{ display: 'inline-flex', alignItems: 'center', gap: '0.25rem' }}>
                  <span style={{ width: '10px', height: '10px', backgroundColor: 'var(--accent-color)', borderRadius: '2px' }}></span> 已答
                </span>
                <span style={{ display: 'inline-flex', alignItems: 'center', gap: '0.25rem' }}>
                  <span style={{ width: '10px', height: '10px', backgroundColor: 'var(--bg-tertiary)', border: '1px solid var(--border-color)', borderRadius: '2px' }}></span> 未答
                </span>
              </div>
              
              <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap', fontSize: '0.75rem' }}>
                {FLAG_TYPES.map(f => {
                  const count = currentExam.questions.filter(q => {
                    const fl = currentExam.flagged?.[q.id]
                    return fl === f.key || (f.key === 'triangle' && (fl === 'flag' || fl === true))
                  }).length
                  return (
                    <span 
                      key={f.key} 
                      style={{ 
                        display: 'inline-flex', 
                        alignItems: 'center', 
                        gap: '0.25rem',
                        backgroundColor: count > 0 ? f.bg : 'var(--bg-tertiary)',
                        padding: '0.15rem 0.4rem',
                        borderRadius: '4px',
                        border: count > 0 ? `1px solid ${f.color}` : '1px solid var(--border-color)',
                        color: count > 0 ? f.color : 'var(--text-tertiary)',
                        fontWeight: count > 0 ? 600 : 'normal'
                      }}
                      title={`${f.icon} 題數: ${count}`}
                    >
                      <span style={{ fontSize: '0.85rem' }}>{f.icon}</span>
                      <strong>{count}</strong>
                    </span>
                  )
                })}
              </div>
            </div>
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
    const currentFlagKey = currentExam.flagged?.[q.id]
    const qEliminated = eliminatedOptions[q.id] || []

    if (cbtMode) {
      return renderCbtExam(q, userSelected, currentFlagKey, qEliminated)
    }

    return renderModernExam(q, userSelected, currentFlagKey, qEliminated)
  }

  // Result Summary Renderer with Specialty Breakdown
  const renderResult = () => {
    if (!currentExam) return null

    const totalWrongCount = currentExam.totalQuestions - currentExam.correctCount

    // Compute specialty/chapter statistics
    const specialtyStatsMap = {}
    currentExam.questions.forEach((q, idx) => {
      const chap = q.chapter || getQuestionSubspecialty(q) || '一般外科'
      const sec = q.section || (
        SUBSPECIALTY_GROUPS.find(g => g.items.includes(chap))?.category?.replace(/^[^\s]+\s/, '') || '其他科'
      )
      const userAns = currentExam.answers[q.id]
      const isCorrect = isAnswerCorrect(q, userAns)

      if (!specialtyStatsMap[chap]) {
        specialtyStatsMap[chap] = {
          chapter: chap,
          section: sec,
          total: 0,
          correct: 0,
          wrong: 0,
          questions: [],
          items: []
        }
      }

      specialtyStatsMap[chap].total += 1
      if (isCorrect) {
        specialtyStatsMap[chap].correct += 1
      } else {
        specialtyStatsMap[chap].wrong += 1
      }
      specialtyStatsMap[chap].items.push({
        idx: idx + 1,
        question: q,
        isCorrect
      })
      specialtyStatsMap[chap].questions.push(q)
    })

    // Sort: specialties with wrong answers first, descending by wrong count
    const specialtyList = Object.values(specialtyStatsMap).sort((a, b) => {
      if (b.wrong !== a.wrong) return b.wrong - a.wrong
      return b.total - a.total
    })

    // Filter questions to render in review list
    const filteredQuestions = currentExam.questions.map((q, idx) => ({ q, idx })).filter(({ q }) => {
      const userAns = currentExam.answers[q.id]
      const isCorrect = isAnswerCorrect(q, userAns)
      const chap = q.chapter || getQuestionSubspecialty(q)

      if (resultFilter === 'all') return true
      if (resultFilter === 'wrong') return !isCorrect
      if (resultFilter === 'correct') return isCorrect
      return chap === resultFilter
    })

    return (
      <div className="result-container animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
        {/* Main Score Card */}
        <div className="card result-header-card" style={{ textAlign: 'center', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1rem' }}>
          <h2>測驗結果報告</h2>
          <div className="result-score-circle">
            <span>{currentExam.score}</span>
            <span>得分</span>
          </div>
          <div className="result-meta-grid" style={{ display: 'flex', gap: '2rem', justifyContent: 'center', width: '100%', maxWidth: '600px', marginTop: '1rem' }}>
            <div className="result-meta-item" style={{ flex: 1 }}>
              <p style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'var(--success)' }}>{currentExam.correctCount} / {currentExam.totalQuestions}</p>
              <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>答對題數</p>
            </div>
            <div className="result-meta-item" style={{ flex: 1 }}>
              <p style={{ fontSize: '1.5rem', fontWeight: 'bold', color: totalWrongCount > 0 ? 'var(--danger)' : 'var(--success)' }}>{totalWrongCount}</p>
              <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>答錯題數</p>
            </div>
            <div className="result-meta-item" style={{ flex: 1 }}>
              <p style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{Math.round((currentExam.correctCount / currentExam.totalQuestions) * 100)}%</p>
              <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>正確率</p>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem', flexWrap: 'wrap' }}>
          <button className="btn btn-primary" onClick={() => {
            setCurrentPage('dashboard')
            setCurrentExam(null)
            setResultFilter('all')
          }}>
            回首頁
          </button>
          <button className="btn btn-outline" onClick={() => startSession(currentExam.year || '113-2', currentExam.subject || '醫學(三)', 'exam')}>
            重新挑戰
          </button>
          <button 
            className="btn btn-secondary"
            style={{ 
              backgroundColor: 'var(--card-bg)', 
              borderColor: 'var(--accent-color)', 
              color: 'var(--accent-color)', 
              fontWeight: 600,
              display: 'inline-flex',
              alignItems: 'center',
              gap: '0.4rem'
            }}
            onClick={() => handleOpenPdfExport(currentExam)}
          >
            <span>📄</span> 一鍵匯出 PDF
          </button>
        </div>

        {/* Specialty Breakdown Card */}
        <div className="card" style={{ padding: '1.5rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.5rem', marginBottom: '1.25rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.75rem' }}>
            <div>
              <h3 style={{ margin: 0, fontSize: '1.2rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <span>📊 各專科錯題與落點分析</span>
                <span style={{ fontSize: '0.85rem', fontWeight: 'normal', color: 'var(--text-secondary)' }}>
                  (共涵蓋 {specialtyList.length} 個專科)
                </span>
              </h3>
              <p style={{ margin: '0.35rem 0 0 0', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                點擊專科卡片或題號標籤，可直接過濾下方題目進行精準弱點檢討
              </p>
            </div>

            {resultFilter !== 'all' && (
              <button 
                className="btn btn-secondary btn-sm" 
                style={{ fontSize: '0.8rem', padding: '0.3rem 0.6rem' }}
                onClick={() => setResultFilter('all')}
              >
                ✕ 清除篩選（顯示全部）
              </button>
            )}
          </div>

          {/* Specialty Grid */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '1rem' }}>
            {specialtyList.map(spec => {
              const accuracy = Math.round((spec.correct / spec.total) * 100)
              const isSelected = resultFilter === spec.chapter
              const progressColor = accuracy >= 80 ? 'var(--success)' : (accuracy >= 60 ? 'var(--warning)' : 'var(--danger)')

              return (
                <div 
                  key={spec.chapter} 
                  className="card"
                  style={{
                    padding: '1rem',
                    background: isSelected ? 'var(--bg-tertiary)' : 'var(--bg-secondary)',
                    border: isSelected ? '2px solid var(--accent-color)' : '1px solid var(--border-color)',
                    borderRadius: 'var(--radius-md)',
                    cursor: 'pointer',
                    transition: 'all 0.2s ease',
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'space-between',
                    gap: '0.75rem',
                    boxShadow: isSelected ? 'var(--shadow-md)' : 'none'
                  }}
                  onClick={() => setResultFilter(isSelected ? 'all' : spec.chapter)}
                >
                  {/* Card Header */}
                  <div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.4rem' }}>
                      <span style={{ fontWeight: 700, fontSize: '1.05rem', color: 'var(--text-primary)' }}>
                        🩺 {spec.chapter}
                      </span>
                      <span className="tag" style={{ fontSize: '0.72rem', background: 'var(--bg-tertiary)', color: 'var(--text-secondary)', padding: '0.15rem 0.4rem' }}>
                        {spec.section}
                      </span>
                    </div>

                    {/* Wrong vs Total Display */}
                    <div style={{ display: 'flex', alignItems: 'baseline', gap: '0.5rem', marginBottom: '0.5rem' }}>
                      {spec.wrong > 0 ? (
                        <span style={{ color: 'var(--danger)', fontWeight: 800, fontSize: '1.2rem' }}>
                          ❌ 錯 {spec.wrong} 題
                        </span>
                      ) : (
                        <span style={{ color: 'var(--success)', fontWeight: 800, fontSize: '1.2rem' }}>
                          🎉 全對 0 錯
                        </span>
                      )}
                      <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                        / 共 {spec.total} 題
                      </span>
                    </div>

                    {/* Accuracy Bar */}
                    <div style={{ marginBottom: '0.5rem' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.78rem', color: 'var(--text-secondary)', marginBottom: '0.2rem' }}>
                        <span>正確率</span>
                        <span style={{ fontWeight: 600, color: progressColor }}>{accuracy}% ({spec.correct}/{spec.total})</span>
                      </div>
                      <div style={{ width: '100%', height: '6px', background: 'var(--bg-tertiary)', borderRadius: '3px', overflow: 'hidden' }}>
                        <div style={{ width: `${accuracy}%`, height: '100%', background: progressColor, borderRadius: '3px', transition: 'width 0.4s ease' }} />
                      </div>
                    </div>
                  </div>

                  {/* Question Number Badges */}
                  <div>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginBottom: '0.3rem' }}>
                      題號分佈（紅標為錯題）：
                    </div>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.3rem' }}>
                      {spec.items.map(item => (
                        <span
                          key={item.idx}
                          style={{
                            fontSize: '0.72rem',
                            fontWeight: 600,
                            padding: '0.15rem 0.35rem',
                            borderRadius: '4px',
                            background: item.isCorrect ? 'var(--success-light)' : 'var(--danger-light)',
                            color: item.isCorrect ? 'var(--success)' : 'var(--danger)',
                            border: item.isCorrect ? '1px solid transparent' : '1px solid var(--danger)'
                          }}
                          onClick={(e) => {
                            e.stopPropagation()
                            setResultFilter(spec.chapter)
                            setTimeout(() => {
                              const el = document.getElementById(`result-q-${item.question.id}`)
                              if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' })
                            }, 50)
                          }}
                        >
                          Q{item.idx} {item.isCorrect ? '✓' : '✗'}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        </div>

        {/* Question Review Section with Filter Tabs */}
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.75rem', marginBottom: '1.5rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '1rem' }}>
            <div>
              <h3 style={{ margin: 0, fontSize: '1.2rem' }}>
                答題明細與檢討
                {resultFilter !== 'all' && (
                  <span style={{ fontSize: '0.9rem', color: 'var(--accent-color)', marginLeft: '0.5rem' }}>
                    （已篩選：{resultFilter === 'wrong' ? '僅看錯題' : (resultFilter === 'correct' ? '僅看答對' : `專科 - ${resultFilter}`)}，共 {filteredQuestions.length} 題）
                  </span>
                )}
              </h3>
            </div>

            {/* Filter Buttons */}
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem' }}>
              <button 
                className={`btn btn-sm ${resultFilter === 'all' ? 'btn-primary' : 'btn-secondary'}`}
                style={{ fontSize: '0.8rem', padding: '0.3rem 0.6rem' }}
                onClick={() => setResultFilter('all')}
              >
                全部 ({currentExam.totalQuestions})
              </button>
              <button 
                className={`btn btn-sm ${resultFilter === 'wrong' ? 'btn-primary' : 'btn-secondary'}`}
                style={{ fontSize: '0.8rem', padding: '0.3rem 0.6rem', color: resultFilter === 'wrong' ? '#fff' : 'var(--danger)' }}
                onClick={() => setResultFilter('wrong')}
              >
                ❌ 僅看錯題 ({totalWrongCount})
              </button>
              <button 
                className={`btn btn-sm ${resultFilter === 'correct' ? 'btn-primary' : 'btn-secondary'}`}
                style={{ fontSize: '0.8rem', padding: '0.3rem 0.6rem', color: resultFilter === 'correct' ? '#fff' : 'var(--success)' }}
                onClick={() => setResultFilter('correct')}
              >
                ✨ 僅看答對 ({currentExam.correctCount})
              </button>
            </div>
          </div>

          {/* Questions List */}
          {filteredQuestions.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '3rem 1rem', color: 'var(--text-secondary)' }}>
              <p style={{ fontSize: '1.1rem' }}>🎉 此篩選條件下沒有題目</p>
              <button className="btn btn-secondary btn-sm" style={{ marginTop: '0.5rem' }} onClick={() => setResultFilter('all')}>
                顯示全部題目
              </button>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
              {filteredQuestions.map(({ q, idx }) => {
                const userAns = currentExam.answers[q.id]
                const isCorrect = isAnswerCorrect(q, userAns)
                const bookmarked = bookmarks.includes(q.id)
                const chap = q.chapter || getQuestionSubspecialty(q) || '一般外科'
                const sec = q.section || '專科'
                
                return (
                  <div key={q.id} id={`result-q-${q.id}`} style={{ borderBottom: '1px solid var(--border-color)', paddingBottom: '1.5rem' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.75rem', flexWrap: 'wrap', gap: '0.5rem' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
                        <span style={{ fontSize: '1.1rem', fontWeight: 'bold', color: 'var(--accent-color)' }}>
                          Q{idx + 1}.
                        </span>
                        <span className="tag tag-green" style={{ backgroundColor: 'var(--success-light)', color: 'var(--success)', fontWeight: 600, fontSize: '0.8rem' }}>
                          🩺 {chap}
                        </span>
                        <span className="tag" style={{ background: 'var(--bg-tertiary)', color: 'var(--text-secondary)', fontSize: '0.75rem' }}>
                          {sec}
                        </span>
                        <span className="tag tag-blue" style={{ fontSize: '0.75rem' }}>
                          {q.year}年 / {q.subject}
                        </span>
                        {(() => {
                          const fKey = currentExam.flagged?.[q.id]
                          const fInfo = fKey ? (FLAG_MAP[fKey] || FLAG_MAP['flag']) : null
                          if (!fInfo) return null
                          return (
                            <span 
                              className="tag" 
                              style={{ 
                                backgroundColor: fInfo.bg, 
                                color: fInfo.color, 
                                border: `1px solid ${fInfo.color}`,
                                fontWeight: 700,
                                fontSize: '0.8rem'
                              }}
                            >
                              {fInfo.icon}
                            </span>
                          )
                        })()}
                      </div>

                      <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                        <button 
                          className="btn btn-secondary btn-sm" 
                          style={{ padding: '0.2rem 0.4rem', fontSize: '0.75rem', color: bookmarked ? 'var(--success)' : '' }}
                          onClick={() => toggleBookmark(q.id)}
                        >
                          {bookmarked ? '★ 已收藏' : '☆ 收藏'}
                        </button>
                        <span 
                          className={`tag ${isCorrect ? 'tag-green' : 'tag-red'}`} 
                          style={{ 
                            backgroundColor: isCorrect ? 'var(--success-light)' : 'var(--danger-light)', 
                            color: isCorrect ? 'var(--success)' : 'var(--danger)', 
                            padding: '0.2rem 0.5rem', 
                            borderRadius: '4px', 
                            fontSize: '0.8rem', 
                            fontWeight: 'bold' 
                          }}
                        >
                          {isCorrect ? '✓ 答對' : '✗ 答錯'}
                        </span>
                      </div>
                    </div>

                    <h4 style={{ fontSize: '1rem', fontWeight: 500, lineHeight: 1.6, marginBottom: '0.75rem', color: 'var(--text-primary)' }}>
                      {q.text}
                    </h4>

                    {q.images && q.images.length > 0 && (
                      <div style={{ marginBottom: '1rem', display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                        {q.images.map((imgSrc, imgIdx) => (
                          <img 
                            key={imgIdx}
                            src={imgSrc}
                            alt={`附圖 ${imgIdx + 1}`}
                            style={{ maxWidth: '100%', maxHeight: '240px', objectFit: 'contain', borderRadius: '4px', border: '1px solid var(--border-color)' }}
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
                            {letter === userAns && (
                              <span style={{ marginLeft: '0.5rem', fontSize: '0.8rem', opacity: 0.9 }}>
                                {isCorrectOpt ? '（您的作答 ✓）' : '（您的作答 ✗）'}
                              </span>
                            )}
                            {letter !== userAns && isCorrectOpt && (
                              <span style={{ marginLeft: '0.5rem', fontSize: '0.8rem', color: 'var(--success)' }}>
                                （正確答案）
                              </span>
                            )}
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
          )}
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

                    {/* Personal User Note - Only show after answering */}
                    {answered && (
                      <UserNoteBox questionId={q.id} userNotes={userNotes} onSaveNote={handleSaveUserNote} />
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

  // Wrong Questions (錯題本) Renderer
  const renderReview = () => {
    const wrongList = questionsData.filter(q => wrongQuestions.includes(q.id))
    
    // Filter by both Year and Subject/Subspecialty
    const filteredWrong = wrongList.filter(q => {
      if (wrongFilterYear !== 'all' && q.year !== wrongFilterYear) {
        return false
      }
      if (wrongFilterSubject !== 'all') {
        const isSubjectMatch = q.subject === wrongFilterSubject
        const isSubspecMatch = (q.chapter === wrongFilterSubject) || (getQuestionSubspecialty(q) === wrongFilterSubject)
        if (!isSubjectMatch && !isSubspecMatch) {
          return false
        }
      }
      return true
    })

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

    const isFiltered = wrongFilterYear !== 'all' || wrongFilterSubject !== 'all'

    return (
      <div className="wrong-questions-layout animate-fade-in">
        {/* Filter Sidebar */}
        <div className="filter-sidebar">
          <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div>
              <h4 className="filter-section-title" style={{ marginBottom: '0.5rem' }}>錯題分類篩選</h4>
              <button 
                className={`filter-btn ${!isFiltered ? 'active' : ''}`}
                style={{ width: '100%', marginBottom: '0.5rem', fontWeight: 'bold' }}
                onClick={() => {
                  setWrongFilterYear('all')
                  setWrongFilterSubject('all')
                }}
              >
                全部錯題 ({wrongList.length})
              </button>
            </div>

            {/* 1. Filter by Exam Year */}
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.4rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.2rem' }}>
                <h5 style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', margin: 0 }}>
                  📅 考試年份
                </h5>
                {wrongFilterYear !== 'all' && (
                  <button
                    style={{ background: 'none', border: 'none', color: 'var(--accent-color)', fontSize: '0.72rem', cursor: 'pointer', padding: 0 }}
                    onClick={() => setWrongFilterYear('all')}
                  >
                    全部年份
                  </button>
                )}
              </div>
              <div className="filter-list" style={{ gap: '0.25rem' }}>
                <button
                  className={`filter-btn ${wrongFilterYear === 'all' ? 'active' : ''}`}
                  style={{ fontSize: '0.82rem', padding: '0.35rem 0.6rem' }}
                  onClick={() => setWrongFilterYear('all')}
                >
                  不限年份 ({wrongList.length})
                </button>
                {yearsList.map(year => {
                  const count = wrongList.filter(q => q.year === year).length
                  if (count === 0) return null
                  return (
                    <button
                      key={year}
                      className={`filter-btn ${wrongFilterYear === year ? 'active' : ''}`}
                      style={{ fontSize: '0.82rem', padding: '0.35rem 0.6rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}
                      onClick={() => setWrongFilterYear(wrongFilterYear === year ? 'all' : year)}
                    >
                      <span>{year}年</span>
                      <span style={{ fontSize: '0.75rem', opacity: 0.8 }}>({count})</span>
                    </button>
                  )
                })}
              </div>
            </div>

            {/* 2. Filter by Exam Subject */}
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.4rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.2rem' }}>
                <h5 style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', margin: 0 }}>
                  📋 國考大科
                </h5>
                {subjectsList.includes(wrongFilterSubject) && (
                  <button
                    style={{ background: 'none', border: 'none', color: 'var(--accent-color)', fontSize: '0.72rem', cursor: 'pointer', padding: 0 }}
                    onClick={() => setWrongFilterSubject('all')}
                  >
                    全部科目
                  </button>
                )}
              </div>
              <div className="filter-list" style={{ gap: '0.25rem' }}>
                {subjectsList.map(subject => {
                  const count = wrongList.filter(q => {
                    const yearMatch = wrongFilterYear === 'all' || q.year === wrongFilterYear
                    return yearMatch && q.subject === subject
                  }).length
                  if (count === 0 && wrongFilterYear === 'all') return null
                  return (
                    <button
                      key={subject}
                      className={`filter-btn ${wrongFilterSubject === subject ? 'active' : ''}`}
                      style={{ fontSize: '0.82rem', padding: '0.35rem 0.6rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}
                      onClick={() => setWrongFilterSubject(wrongFilterSubject === subject ? 'all' : subject)}
                    >
                      <span>{subject}</span>
                      <span style={{ fontSize: '0.75rem', opacity: 0.8 }}>({count})</span>
                    </button>
                  )
                })}
              </div>
            </div>

            {/* 3. Filter by Subspecialty / Department */}
            {SUBSPECIALTY_GROUPS.map(group => {
              const availableItems = group.items.filter(item => {
                return wrongList.some(q => {
                  const yearMatch = wrongFilterYear === 'all' || q.year === wrongFilterYear
                  return yearMatch && getQuestionSubspecialty(q) === item
                })
              })

              if (availableItems.length === 0) return null

              return (
                <div key={group.category}>
                  <h5 style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '0.4rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.2rem' }}>
                    {group.category}
                  </h5>
                  <div className="filter-list" style={{ gap: '0.25rem' }}>
                    {availableItems.map(item => {
                      const count = wrongList.filter(q => {
                        const yearMatch = wrongFilterYear === 'all' || q.year === wrongFilterYear
                        return yearMatch && getQuestionSubspecialty(q) === item
                      }).length
                      return (
                        <button
                          key={item}
                          className={`filter-btn ${wrongFilterSubject === item ? 'active' : ''}`}
                          style={{ fontSize: '0.82rem', padding: '0.35rem 0.6rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}
                          onClick={() => setWrongFilterSubject(wrongFilterSubject === item ? 'all' : item)}
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
                錯題清單 - {wrongFilterYear === 'all' ? '全部年份' : `${wrongFilterYear}年`} / {wrongFilterSubject === 'all' ? '全部科別' : wrongFilterSubject} ({filteredWrong.length} 題)
              </h3>
              <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>答對後題目會繼續保留在錯題本中，需要時可點選「移出錯題本」</span>
            </div>
            {isFiltered && (
              <button 
                className="btn btn-secondary btn-sm"
                onClick={() => {
                  setWrongFilterYear('all')
                  setWrongFilterSubject('all')
                }}
              >
                ✕ 清除篩選（顯示全部錯題）
              </button>
            )}
          </div>

          {filteredWrong.length === 0 ? (
            <div className="card" style={{ textAlign: 'center', padding: '3rem', marginTop: '1rem' }}>
              <p style={{ color: 'var(--text-tertiary)', fontSize: '1.1rem' }}>
                🎉 太棒了！【{wrongFilterYear === 'all' ? '' : `${wrongFilterYear}年 `}{wrongFilterSubject === 'all' ? '此條件' : wrongFilterSubject}】目前沒有錯題
              </p>
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

                    {/* Personal User Note - Only show after answering */}
                    {answered && (
                      <UserNoteBox questionId={q.id} userNotes={userNotes} onSaveNote={handleSaveUserNote} />
                    )}
                  </div>
                )
              })}
            </div>
          )}
        </div>
      </div>
    )
  }

  const isCbtActive = currentPage === 'exam' && cbtMode

  return (
    <div className={`app-container ${isCbtActive ? 'cbt-active-view' : ''}`}>
      {!isCbtActive && (
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
            <button 
              className="btn btn-secondary btn-sm"
              onClick={() => setShowClearModal(true)}
              style={{ 
                color: 'var(--danger)', 
                borderColor: 'rgba(239, 68, 68, 0.35)', 
                padding: '0.25rem 0.6rem', 
                fontSize: '0.8rem',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '0.3rem'
              }}
              title="一鍵清除使用紀錄"
            >
              🗑️ 清除紀錄
            </button>
            <button className="theme-toggle-btn" onClick={toggleTheme} aria-label="切換主題" style={{ background: 'none', border: 'none', cursor: 'pointer', fontSize: '1.2rem', padding: '0 0.5rem' }}>
              {theme === 'light' ? '🌙' : '☀️'}
            </button>
          </nav>
        </header>
      )}

      <main className={`main-content ${isCbtActive ? 'cbt-main-content' : ''}`}>
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
                    <div style={{ display: 'flex', gap: '0.5rem', flexShrink: 0, flexWrap: 'wrap', justifyContent: 'flex-end' }}>
                      <button 
                        className="btn btn-secondary btn-sm"
                        style={{ display: 'inline-flex', alignItems: 'center', gap: '0.3rem' }}
                        onClick={() => {
                          setCbtMode(true)
                          startSession(selectedYearTerm, subject, 'exam')
                          setSelectedYearTerm(null)
                        }}
                        title="以考選部電腦化測驗擬真介面進行考試"
                      >
                        🏛️ 考選部模式
                      </button>
                      <button 
                        className="btn btn-primary btn-sm" 
                        onClick={() => {
                          setCbtMode(false)
                          startSession(selectedYearTerm, subject, 'exam')
                          setSelectedYearTerm(null)
                        }}
                        title="以現代版卡片介面進行考試"
                      >
                        模擬考試
                      </button>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        </div>
      )}

      {/* Modal for clearing usage records */}
      {showClearModal && (
        <div className="modal-overlay animate-fade-in" onClick={() => setShowClearModal(false)}>
          <div className="card modal-content" onClick={e => e.stopPropagation()} style={{ maxWidth: '500px', width: '100%', padding: '1.5rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.75rem' }}>
              <h3 style={{ fontSize: '1.2rem', margin: 0, color: 'var(--danger)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                🗑️ 一鍵清除使用紀錄
              </h3>
              <button 
                className="btn btn-secondary btn-sm" 
                style={{ padding: '0.2rem 0.5rem', fontSize: '0.85rem' }} 
                onClick={() => setShowClearModal(false)}
              >
                ✕
              </button>
            </div>

            <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '1rem', lineHeight: '1.5' }}>
              請勾選您想要清除的使用紀錄項目。請注意：<strong>資料清除後無法復原</strong>，請確認後再執行！
            </p>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', marginBottom: '1.25rem' }}>
              {/* Option: History */}
              <label style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0.65rem 0.85rem', background: 'var(--bg-tertiary)', borderRadius: '6px', cursor: 'pointer' }}>
                <span style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', fontSize: '0.9rem' }}>
                  <input 
                    type="checkbox" 
                    checked={clearOptions.history} 
                    onChange={e => setClearOptions(prev => ({ ...prev, history: e.target.checked }))} 
                  />
                  <span>📊 歷次測驗歷史紀錄</span>
                </span>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{history.length} 筆</span>
              </label>

              {/* Option: Wrong Questions */}
              <label style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0.65rem 0.85rem', background: 'var(--bg-tertiary)', borderRadius: '6px', cursor: 'pointer' }}>
                <span style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', fontSize: '0.9rem' }}>
                  <input 
                    type="checkbox" 
                    checked={clearOptions.wrong} 
                    onChange={e => setClearOptions(prev => ({ ...prev, wrong: e.target.checked }))} 
                  />
                  <span>❌ 錯題本累積題庫</span>
                </span>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{wrongQuestions.length} 題</span>
              </label>

              {/* Option: User Notes */}
              <label style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0.65rem 0.85rem', background: 'var(--bg-tertiary)', borderRadius: '6px', cursor: 'pointer' }}>
                <span style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', fontSize: '0.9rem' }}>
                  <input 
                    type="checkbox" 
                    checked={clearOptions.notes} 
                    onChange={e => setClearOptions(prev => ({ ...prev, notes: e.target.checked }))} 
                  />
                  <span>📝 個人重點備註與筆記</span>
                </span>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{Object.keys(userNotes).length} 則</span>
              </label>

              {/* Option: Bookmarks */}
              <label style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0.65rem 0.85rem', background: 'var(--bg-tertiary)', borderRadius: '6px', cursor: 'pointer' }}>
                <span style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', fontSize: '0.9rem' }}>
                  <input 
                    type="checkbox" 
                    checked={clearOptions.bookmarks} 
                    onChange={e => setClearOptions(prev => ({ ...prev, bookmarks: e.target.checked }))} 
                  />
                  <span>⭐️ 題目收藏清單</span>
                </span>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{bookmarks.length} 題</span>
              </label>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '0.5rem', borderTop: '1px solid var(--border-color)', paddingTop: '1rem', flexWrap: 'wrap' }}>
              <div style={{ display: 'flex', gap: '0.4rem' }}>
                <button
                  type="button"
                  className="btn btn-secondary btn-sm"
                  style={{ fontSize: '0.75rem', padding: '0.2rem 0.5rem' }}
                  onClick={() => setClearOptions({ history: true, wrong: true, notes: true, bookmarks: true })}
                >
                  全選
                </button>
                <button
                  type="button"
                  className="btn btn-secondary btn-sm"
                  style={{ fontSize: '0.75rem', padding: '0.2rem 0.5rem' }}
                  onClick={() => setClearOptions({ history: false, wrong: false, notes: false, bookmarks: false })}
                >
                  全不選
                </button>
              </div>

              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <button 
                  className="btn btn-secondary" 
                  onClick={() => setShowClearModal(false)}
                >
                  取消
                </button>
                <button 
                  className="btn btn-primary"
                  style={{ background: 'var(--danger)', borderColor: 'var(--danger)', color: '#fff' }}
                  disabled={!clearOptions.history && !clearOptions.wrong && !clearOptions.notes && !clearOptions.bookmarks}
                  onClick={handleClearRecords}
                >
                  確認一鍵清除
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Toast Notification */}
      {toastMessage && (
        <div style={{
          position: 'fixed',
          top: '20px',
          left: '50%',
          transform: 'translateX(-50%)',
          background: 'var(--success)',
          color: '#fff',
          padding: '0.65rem 1.25rem',
          borderRadius: '8px',
          boxShadow: '0 4px 12px rgba(0,0,0,0.25)',
          zIndex: 3000,
          fontWeight: 600,
          fontSize: '0.9rem',
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem',
          pointerEvents: 'none'
        }}>
          <span>✓</span> {toastMessage}
        </div>
      )}

      {/* PDF Export & Print Modal */}
      {showPdfExport && pdfExamData && (() => {
        const meta = getExamTitleMeta(pdfExamData)
        const score = pdfExamData.score !== undefined
          ? pdfExamData.score 
          : Math.round(((pdfExamData.correctCount || 0) / (pdfExamData.totalQuestions || 80)) * 100)
        
        const triangleCount = (pdfExamData.questions || []).filter(q => {
          const f = pdfExamData.flagged?.[q.id]
          return f === 'triangle' || f === 'flag' || f === true
        }).length

        const squareCount = (pdfExamData.questions || []).filter(q => {
          const f = pdfExamData.flagged?.[q.id]
          return f === 'square' || f === 'trap'
        }).length

        const circleCount = (pdfExamData.questions || []).filter(q => {
          const f = pdfExamData.flagged?.[q.id]
          return f === 'circle' || f === 'star'
        }).length

        const sortedQuestions = [...(pdfExamData.questions || [])].sort((a, b) => a.number - b.number)

        return (
          <div className="pdf-modal-overlay">
            {/* Top Toolbar (Hidden when printing) */}
            <div className="pdf-modal-toolbar no-print">
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', flexWrap: 'wrap' }}>
                <h3 style={{ margin: 0, fontSize: '1.1rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                  <span>📄</span> 考卷預覽與匯出 PDF
                </h3>
                <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                  ({pdfExamData.name} · 得分：{score} 分)
                </span>
              </div>
              <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
                <button
                  type="button"
                  className="btn btn-primary"
                  style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', padding: '0.45rem 1.1rem', fontSize: '0.9rem', fontWeight: 600 }}
                  onClick={() => window.print()}
                >
                  <span>🖨️</span> 列印 / 儲存為 PDF
                </button>
                <button
                  type="button"
                  className="btn btn-secondary"
                  style={{ padding: '0.45rem 1rem', fontSize: '0.9rem' }}
                  onClick={() => setShowPdfExport(false)}
                >
                  ✕ 關閉預覽
                </button>
              </div>
            </div>

            {/* Scroll Area showing realistic A4 Paper */}
            <div className="pdf-modal-scroll-area">
              <div id="pdf-printable-doc" className="pdf-paper-sheet">
                {/* Exam Official Header */}
                <div className="pdf-exam-header">
                  <h1 className="pdf-exam-title">
                    {meta.title}
                  </h1>

                  <div className="pdf-header-body">
                    <div className="pdf-header-left">
                      <div className="pdf-meta-line">
                        <strong>代&emsp;&emsp;號：</strong>{meta.code}
                      </div>
                      <div className="pdf-meta-line">
                        <strong>類科名稱：</strong>{meta.category}
                      </div>
                      <div className="pdf-meta-line">
                        <strong>科目名稱：</strong>{meta.fullSubjectName}
                      </div>
                      <div className="pdf-meta-line" style={{ display: 'flex', justifyContent: 'space-between', maxWidth: '480px' }}>
                        <span><strong>考試時間：</strong>2小時</span>
                        <span><strong>座號：</strong>_______________</span>
                      </div>
                      <div className="pdf-meta-line" style={{ color: '#444', fontSize: '9pt', marginTop: '4px' }}>
                        ※注意：本試題禁止使用電子計算器
                      </div>
                      <div className="pdf-meta-line" style={{ color: '#444', fontSize: '9pt' }}>
                        ※本試題為單一選擇題，請選出一個正確或最適當答案。
                      </div>
                    </div>

                    {/* Score & Flag Summary (Right side) */}
                    <div className="pdf-header-right">
                      <div className="pdf-score-badge">
                        {score}/100
                      </div>
                      <div className="pdf-flag-stat-row">
                        <span style={{ color: '#f59e0b' }}>▲</span>
                        <span style={{ color: '#d32f2f' }}>{triangleCount}</span>
                      </div>
                      <div className="pdf-flag-stat-row">
                        <span style={{ color: '#10b981' }}>●</span>
                        <span style={{ color: '#d32f2f' }}>{circleCount}</span>
                      </div>
                      <div className="pdf-flag-stat-row">
                        <span style={{ color: '#ec4899' }}>■</span>
                        <span style={{ color: '#2563eb' }}>{squareCount}</span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Questions List */}
                <div className="pdf-questions-container">
                  {sortedQuestions.map((q, idx) => {
                    const userAns = pdfExamData.answers?.[q.id]
                    const isCorrect = isAnswerCorrect(q, userAns)
                    const flagKey = pdfExamData.flagged?.[q.id]
                    const flagInfo = flagKey ? (FLAG_MAP[flagKey] || FLAG_MAP['triangle']) : null

                    return (
                      <div key={q.id} className="pdf-question-item">
                        {/* Left Margin Answer Column */}
                        <div className="pdf-answer-col">
                          {isCorrect ? (
                            <div className="pdf-ans-row">
                              <span className="pdf-ans-letter">
                                {userAns || q.answer}
                              </span>
                              {flagInfo && (
                                <span className="pdf-ans-flag" style={{ color: flagInfo.color }}>
                                  {flagInfo.icon}
                                </span>
                              )}
                            </div>
                          ) : (
                            <div className="pdf-ans-wrong-block">
                              <div className="pdf-ans-row">
                                <span className="pdf-ans-letter wrong-slashed">
                                  {userAns || '—'}
                                </span>
                                {flagInfo && (
                                  <span className="pdf-ans-flag" style={{ color: flagInfo.color }}>
                                    {flagInfo.icon}
                                  </span>
                                )}
                              </div>
                              <div className="pdf-correct-letter">
                                {q.answer ? q.answer.replace('ALL', '一律給分') : ''}
                              </div>
                            </div>
                          )}
                        </div>

                        {/* Right Question Text & Options */}
                        <div className="pdf-question-body">
                          <div className="pdf-q-title">
                            <span className="pdf-q-num">{idx + 1}.</span>
                            <span>{q.text}</span>
                          </div>

                          {q.images && q.images.length > 0 && (
                            <div className="pdf-q-images">
                              {q.images.map((imgSrc, imgIdx) => (
                                <img key={imgIdx} src={imgSrc} alt={`題目附圖 ${imgIdx + 1}`} className="pdf-inline-img" />
                              ))}
                            </div>
                          )}

                          <div className="pdf-q-options">
                            {Object.entries(q.options || {}).map(([optLetter, optText]) => (
                              <div key={optLetter} className="pdf-option-line">
                                <span className="pdf-opt-label">{optLetter}.</span>
                                <span className="pdf-opt-content">{optText}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>
                    )
                  })}
                </div>
              </div>
            </div>
          </div>
        )
      })()}
    </div>
  )
}

export default App
