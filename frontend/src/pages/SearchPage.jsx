import { useState } from 'react'
import { SCENARIOS_CATALOG } from '../data/scenariosCatalog'
import {
  CRITERIA_LIST,
  DAYS_OF_WEEK,
  DEFAULT_PRIORITIES,
  DISTRICT_OPTIONS,
  LEARNING_MODE_OPTIONS,
  PRIORITY_OPTIONS,
  SESSIONS_OF_DAY,
  SUBJECT_OPTIONS,
} from '../services/api'

const SCHEDULE_PATTERNS = [
  {
    label: 'Tối cả tuần (T2-CN)',
    slots: ['T2-tối', 'T3-tối', 'T4-tối', 'T5-tối', 'T6-tối', 'T7-tối', 'CN-tối'],
  },
  {
    label: 'Hai ngày cuối tuần (T7-CN)',
    slots: ['T7-sáng', 'T7-chiều', 'T7-tối', 'CN-sáng', 'CN-chiều', 'CN-tối'],
  },
  {
    label: 'Tối ngày thường (T2-T6)',
    slots: ['T2-tối', 'T3-tối', 'T4-tối', 'T5-tối', 'T6-tối'],
  },
]

function formatBudgetInVietnameseWords(amount) {
  if (amount === undefined || amount === null || String(amount).trim() === '') {
    return ''
  }
  const num = Number(amount)
  if (!Number.isFinite(num) || num < 0) return ''
  if (num === 0) return '= 0 VNĐ / giờ (Miễn phí)'

  const digits = ['không', 'một', 'hai', 'ba', 'bốn', 'năm', 'sáu', 'bảy', 'tám', 'chín']
  const readTriple = (n, showZeroHundred = false) => {
    const h = Math.floor(n / 100)
    const t = Math.floor((n % 100) / 10)
    const u = n % 10
    const res = []
    if (h > 0 || showZeroHundred) {
      res.push(digits[h] + ' trăm')
    }
    if (t > 1) {
      res.push(digits[t] + ' mươi')
      if (u === 1) res.push('mốt')
      else if (u === 5) res.push('lăm')
      else if (u > 0) res.push(digits[u])
    } else if (t === 1) {
      res.push('mười')
      if (u === 5) res.push('lăm')
      else if (u > 0) res.push(digits[u])
    } else if (t === 0 && (h > 0 || showZeroHundred) && u > 0) {
      res.push('lẻ ' + digits[u])
    } else if (t === 0 && h === 0 && !showZeroHundred) {
      if (u > 0) res.push(digits[u])
    }
    return res.join(' ')
  }

  const scales = ['', 'nghìn', 'triệu', 'tỷ']
  let temp = Math.floor(num)
  const groups = []
  while (temp > 0) {
    groups.push(temp % 1000)
    temp = Math.floor(temp / 1000)
  }

  const parts = []
  for (let i = groups.length - 1; i >= 0; i--) {
    const g = groups[i]
    if (g > 0) {
      const showH = i < groups.length - 1
      const txt = readTriple(g, showH)
      if (txt) {
        parts.push(txt + (scales[i] ? ' ' + scales[i] : ''))
      }
    }
  }
  let words = parts.join(' ').trim()
  if (words) {
    words = words.charAt(0).toUpperCase() + words.slice(1) + ' đồng / giờ'
  }
  const formattedVnd = num.toLocaleString('vi-VN') + ' VNĐ / giờ'
  return `= ${formattedVnd} (${words})`
}

function SearchPage({
  searchForm,
  onChangeSearchForm,
  onSubmitSearch,
  onApplyScenario,
  isLoading = false,
  apiError = '',
}) {
  const [validationError, setValidationError] = useState('')
  const [autoRunScenario, setAutoRunScenario] = useState(true)

  const {
    subject,
    learningMode,
    preferredDistrict,
    maxBudgetVnd,
    timeSlots,
    priorities,
    topK,
    scenarioMeta,
  } = searchForm

  const isOnlineMode = learningMode === 'online'

  const updateField = (patch) => {
    setValidationError('')
    onChangeSearchForm({
      ...searchForm,
      ...patch,
    })
  }

  const handleLearningModeChange = (nextMode) => {
    updateField({
      learningMode: nextMode,
      preferredDistrict: nextMode === 'online' ? '' : preferredDistrict,
      scenarioMeta: null,
    })
  }

  const handleToggleTimeSlot = (slotKey) => {
    const nextSlots = timeSlots.includes(slotKey)
      ? timeSlots.filter((item) => item !== slotKey)
      : [...timeSlots, slotKey]
    updateField({
      timeSlots: nextSlots,
      scenarioMeta: null,
    })
  }

  const handleApplySchedulePattern = (patternSlots) => {
    updateField({
      timeSlots: patternSlots,
      scenarioMeta: null,
    })
  }

  const handleSelectScenario = (sc) => {
    setValidationError('')
    if (autoRunScenario) {
      onApplyScenario(sc)
    } else {
      onChangeSearchForm({
        ...searchForm,
        subject: sc.request.subject,
        learningMode: sc.request.learning_mode,
        preferredDistrict: sc.request.preferred_district || '',
        maxBudgetVnd:
          sc.request.max_budget_vnd !== undefined &&
          sc.request.max_budget_vnd !== null &&
          sc.request.max_budget_vnd !== ''
            ? String(sc.request.max_budget_vnd)
            : '',
        timeSlots: Array.isArray(sc.request.time_slots)
          ? [...sc.request.time_slots]
          : [],
        priorities: {
          ...DEFAULT_PRIORITIES,
          ...(sc.request.priorities || {}),
        },
        topK: 3,
        scenarioMeta: sc,
      })
    }
  }

  const handlePriorityChange = (criterionKey, level) => {
    updateField({
      priorities: {
        ...priorities,
        [criterionKey]: level,
      },
      scenarioMeta: null,
    })
  }

  const handleResetDefaults = () => {
    setValidationError('')
    onChangeSearchForm({
      subject: 'Toán',
      learningMode: 'in_person',
      preferredDistrict: 'Bình Thạnh',
      maxBudgetVnd: '200000',
      timeSlots: ['T2-tối', 'T4-tối'],
      priorities: { ...DEFAULT_PRIORITIES },
      topK: 3,
      scenarioMeta: null,
    })
  }

  const validateForm = () => {
    if (!String(subject || '').trim()) {
      return 'Vui lòng chọn môn học cần tìm gia sư.'
    }

    const rawBudget = String(maxBudgetVnd ?? '').trim()
    if (rawBudget !== '') {
      const parsedBudget = Number(rawBudget)
      if (!Number.isInteger(parsedBudget) || parsedBudget < 0) {
        return 'Ngân sách tối đa mỗi giờ phải là số nguyên không âm (VNĐ).'
      }
    }

    const parsedTopK = Number(topK)
    if (!Number.isInteger(parsedTopK) || parsedTopK < 1 || parsedTopK > 20) {
      return 'Số lượng kết quả gợi ý (Top-k) phải là số nguyên từ 1 đến 20.'
    }

    return ''
  }

  const handleSubmit = (event) => {
    event.preventDefault()
    setValidationError('')

    const errorMsg = validateForm()
    if (errorMsg) {
      setValidationError(errorMsg)
      return
    }

    onSubmitSearch(searchForm)
  }

  return (
    <div className="search-page">
      <header className="page-header">
        <h1>Tìm kiếm & Khuyến nghị Gia sư Đa tiêu chí</h1>
        <p className="subtitle">
          Mô-đun CN01 · Thiết lập điều kiện học tập và trọng số ưu tiên 5 tiêu chí để
          xếp hạng Top-k gia sư theo mô hình Weighted Scoring.
        </p>
      </header>

      <section
        className="scenario-strip-panel"
        aria-label="Nạp nhanh 14 kịch bản thực nghiệm Bảng 5.1"
      >
        <div className="scenario-strip-header">
          <div className="strip-title-group">
            <span className="strip-title">Kịch bản thực nghiệm (Bảng 5.1 · KB01 - KB14):</span>
            <label
              className="auto-run-toggle"
              title="Khi bật: Click kịch bản sẽ chạy và chuyển thẳng đến trang kết quả. Khi tắt: Nạp thông số vào biểu mẫu để tùy chỉnh."
            >
              <input
                type="checkbox"
                checked={autoRunScenario}
                onChange={(e) => setAutoRunScenario(e.target.checked)}
              />
              <span>Tự động chuyển kết quả</span>
            </label>
          </div>
          {scenarioMeta && (
            <div className="scenario-active-wrap">
              <span className="scenario-active-indicator">
                Đang nạp: <strong>{scenarioMeta.id}</strong> (Kỳ vọng: {scenarioMeta.expected_raw})
              </span>
              {!autoRunScenario && (
                <button
                  type="button"
                  className="btn-accent-sm"
                  onClick={() => onApplyScenario(scenarioMeta)}
                >
                  Xem kết quả ngay →
                </button>
              )}
            </div>
          )}
        </div>

        <div className="scenario-chip-scroller">
          {SCENARIOS_CATALOG.map((sc) => {
            const isSelected = scenarioMeta?.id === sc.id
            return (
              <button
                key={sc.id}
                type="button"
                disabled={isLoading}
                title={`${sc.title} - Kỳ vọng: ${sc.expected_raw}`}
                className={`scenario-chip ${isSelected ? 'active' : ''}`}
                onClick={() => handleSelectScenario(sc)}
              >
                <span className="sc-id">{sc.id}</span>
                <span className="sc-subj">{sc.request.subject}</span>
              </button>
            )
          })}
        </div>
      </section>

      <form className="search-form" onSubmit={handleSubmit} noValidate>
        <div className="workbench-columns">
          {/* Cột 1: Thông tin nhu cầu học tập & Lịch rảnh */}
          <section className="panel col-main">
            <div className="panel-header">
              <h2>1. Thông tin nhu cầu học tập (Bảng 3.4)</h2>
              <button
                type="button"
                className="btn-secondary"
                onClick={handleResetDefaults}
              >
                Đặt lại mặc định
              </button>
            </div>

            <div className="form-fields-grid">
              <div className="form-field">
                <label htmlFor="subject-select">
                  Môn học <span className="required">*</span>
                </label>
                <select
                  id="subject-select"
                  value={subject}
                  onChange={(e) =>
                    updateField({ subject: e.target.value, scenarioMeta: null })
                  }
                  required
                >
                  {SUBJECT_OPTIONS.map((subj) => (
                    <option key={subj} value={subj}>
                      {subj}
                    </option>
                  ))}
                </select>
                <span className="field-hint">
                  Điều kiện lọc bắt buộc: gia sư phải nhận dạy môn này.
                </span>
              </div>

              <div className="form-field">
                <label htmlFor="learning-mode-select">
                  Hình thức học <span className="required">*</span>
                </label>
                <select
                  id="learning-mode-select"
                  value={learningMode}
                  onChange={(e) => handleLearningModeChange(e.target.value)}
                >
                  {LEARNING_MODE_OPTIONS.map((mode) => (
                    <option key={mode.value} value={mode.value}>
                      {mode.label}
                    </option>
                  ))}
                </select>
                <span className="field-hint">
                  Khi học Trực tuyến, tiêu chí Khu vực tự động không áp dụng.
                </span>
              </div>

              {!isOnlineMode ? (
                <div className="form-field">
                  <label htmlFor="district-select">Khu vực mong muốn</label>
                  <select
                    id="district-select"
                    value={preferredDistrict}
                    onChange={(e) =>
                      updateField({
                        preferredDistrict: e.target.value,
                        scenarioMeta: null,
                      })
                    }
                  >
                    <option value="">-- Không giới hạn khu vực --</option>
                    {DISTRICT_OPTIONS.map((dist) => (
                      <option key={dist} value={dist}>
                        {dist}
                      </option>
                    ))}
                  </select>
                  <span className="field-hint">
                    Dùng để tính điểm khớp vị trí dạy trực tiếp.
                  </span>
                </div>
              ) : (
                <div className="form-field disabled-field">
                  <label htmlFor="district-disabled">Khu vực mong muốn</label>
                  <input
                    id="district-disabled"
                    type="text"
                    value="Không áp dụng khi học Trực tuyến (Online)"
                    disabled
                    readOnly
                  />
                  <span className="field-hint">
                    Tiêu chí khu vực được loại khỏi công thức tổng hợp điểm.
                  </span>
                </div>
              )}

              <div className="form-field">
                <label htmlFor="budget-input">
                  Ngân sách tối đa / giờ (VNĐ)
                </label>
                <input
                  id="budget-input"
                  type="number"
                  min="0"
                  step="10000"
                  placeholder="Ví dụ: 200000 (để trống nếu không giới hạn)"
                  value={maxBudgetVnd}
                  onChange={(e) =>
                    updateField({
                      maxBudgetVnd: e.target.value,
                      scenarioMeta: null,
                    })
                  }
                />
                {String(maxBudgetVnd ?? '').trim() !== '' && (
                  <div className="currency-humanizer-tag" role="status">
                    {formatBudgetInVietnameseWords(maxBudgetVnd)}
                  </div>
                )}
                <span className="field-hint">
                  Học phí trong ngân sách đạt điểm 1,00; vượt quá 1,5 lần nhận 0 điểm.
                </span>
              </div>

              <div className="form-field">
                <label htmlFor="topk-select">Số lượng gợi ý (Top-k)</label>
                <select
                  id="topk-select"
                  value={topK}
                  onChange={(e) =>
                    updateField({ topK: Number(e.target.value) })
                  }
                >
                  {[1, 2, 3, 5, 10].map((k) => (
                    <option key={k} value={k}>
                      Top {k} gia sư
                    </option>
                  ))}
                </select>
                <span className="field-hint">
                  Mặc định gợi ý Top 3 gia sư có điểm tổng hợp cao nhất.
                </span>
              </div>
            </div>

            <div className="schedule-section">
              <div className="schedule-header">
                <div>
                  <h3>Khung thời gian rảnh trong tuần</h3>
                  <p className="field-hint">
                    Đã chọn:{' '}
                    <strong>
                      {timeSlots.length > 0
                        ? timeSlots.join(', ')
                        : 'Chưa chọn (không tính tiêu chí lịch rảnh)'}
                    </strong>
                  </p>
                </div>
                {timeSlots.length > 0 && (
                  <button
                    type="button"
                    className="btn-text"
                    onClick={() =>
                      updateField({ timeSlots: [], scenarioMeta: null })
                    }
                  >
                    Bỏ chọn tất cả
                  </button>
                )}
              </div>

              <div className="schedule-power-bar" aria-label="Mẫu chọn nhanh khung giờ rảnh">
                <span className="power-bar-title">Mẫu chọn nhanh:</span>
                <div className="power-bar-buttons">
                  {SCHEDULE_PATTERNS.map((pattern) => (
                    <button
                      key={pattern.label}
                      type="button"
                      className="power-pill-btn"
                      onClick={() => handleApplySchedulePattern(pattern.slots)}
                    >
                      {pattern.label}
                    </button>
                  ))}
                </div>
              </div>

              <div className="schedule-table-wrap">
                <table className="schedule-table">
                  <thead>
                    <tr>
                      <th>Buổi</th>
                      {DAYS_OF_WEEK.map((day) => (
                        <th key={day.code}>{day.label}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {SESSIONS_OF_DAY.map((session) => (
                      <tr key={session.code}>
                        <td className="session-name">{session.label}</td>
                        {DAYS_OF_WEEK.map((day) => {
                          const slotKey = `${day.code}-${session.code}`
                          const isSelected = timeSlots.includes(slotKey)
                          return (
                            <td key={slotKey}>
                              <button
                                type="button"
                                className={`slot-button ${isSelected ? 'selected' : ''}`}
                                onClick={() => handleToggleTimeSlot(slotKey)}
                                aria-pressed={isSelected}
                              >
                                {slotKey}
                              </button>
                            </td>
                          )
                        })}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </section>

          {/* Cột 2: Mức độ ưu tiên 5 tiêu chí */}
          <section className="panel col-side">
            <div className="panel-header">
              <div>
                <h2>2. Mức độ ưu tiên cho 5 tiêu chí (Bảng 3.5)</h2>
                <p className="field-hint">
                  Trọng số: Không quan tâm (w = 0), Thấp (w = 1), Trung bình (w = 2, mặc định), Cao (w = 3).
                </p>
              </div>
            </div>

            <div className="criteria-stack">
              {CRITERIA_LIST.map((criterion) => {
                const isCriterionDisabled =
                  (criterion.key === 'district' &&
                    (isOnlineMode || !String(preferredDistrict).trim())) ||
                  (criterion.key === 'fee' && !String(maxBudgetVnd).trim()) ||
                  (criterion.key === 'availability' && timeSlots.length === 0)

                const currentLevel = priorities[criterion.key] || 'medium'

                return (
                  <div
                    key={criterion.key}
                    className={`criterion-card ${isCriterionDisabled ? 'disabled' : ''}`}
                  >
                    <div className="criterion-header">
                      <strong className="criterion-title">{criterion.label}</strong>
                      {isCriterionDisabled && (
                        <span className="inactive-badge">
                          Tự động bỏ qua
                        </span>
                      )}
                    </div>
                    <p className="criterion-desc">{criterion.description}</p>

                    <div
                      className="priority-segmented-control"
                      role="group"
                      aria-label={`Mức ưu tiên ${criterion.label}`}
                    >
                      {PRIORITY_OPTIONS.map((opt) => {
                        const isActive = currentLevel === opt.value
                        return (
                          <button
                            key={opt.value}
                            type="button"
                            disabled={isCriterionDisabled}
                            className={`seg-btn ${isActive ? 'active' : ''}`}
                            onClick={() =>
                              handlePriorityChange(criterion.key, opt.value)
                            }
                          >
                            <span className="seg-label">{opt.label}</span>
                            <span className="seg-weight">w={opt.weight}</span>
                          </button>
                        )
                      })}
                    </div>
                  </div>
                )
              })}
            </div>
          </section>
        </div>

        {validationError && (
          <div className="alert alert-error" role="alert">
            <strong>Lỗi kiểm tra dữ liệu:</strong> {validationError}
          </div>
        )}

        {apiError && (
          <div className="alert alert-error" role="alert">
            <strong>Lỗi gọi API:</strong> {apiError}
          </div>
        )}

        <div className="submit-bar">
          <button type="submit" className="btn-primary btn-large" disabled={isLoading}>
            {isLoading
              ? 'Đang tính điểm & xếp hạng...'
              : 'Tìm gia sư phù hợp →'}
          </button>
        </div>
      </form>
    </div>
  )
}

export default SearchPage
