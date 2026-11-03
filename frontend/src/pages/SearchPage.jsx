import { useState } from 'react'
import { motion } from 'motion/react'
import { SCENARIOS_CATALOG } from '../data/scenariosCatalog'
import SubjectIcon from '../components/SubjectIcon'
import CriteriaIcon from '../components/CriteriaIcon'
import SkeletonLoader from '../components/SkeletonLoader'
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
      updateField({
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
      timeSlots: [],
      priorities: { ...DEFAULT_PRIORITIES },
      topK: 3,
      scenarioMeta: null,
    })
  }

  const handleSubmit = (e) => {
    e.preventDefault()

    if (!subject || !String(subject).trim()) {
      setValidationError('Vui lòng chọn môn học mong muốn.')
      return
    }

    if (!learningMode) {
      setValidationError('Vui lòng chọn hình thức học.')
      return
    }

    if (learningMode === 'in_person' && (!preferredDistrict || !String(preferredDistrict).trim())) {
      setValidationError('Hình thức học Trực tiếp (In-person) bắt buộc chọn khu vực Quận/Huyện mong muốn.')
      return
    }

    if (maxBudgetVnd !== '' && maxBudgetVnd !== undefined && maxBudgetVnd !== null) {
      const budgetNum = Number(maxBudgetVnd)
      if (Number.isNaN(budgetNum) || budgetNum < 0) {
        setValidationError('Ngân sách tối đa phải là một số không âm hợp lệ.')
        return
      }
    }

    setValidationError('')
    onSubmitSearch(searchForm)
  }

  const budgetVietnameseWords = formatBudgetInVietnameseWords(maxBudgetVnd)

  return (
    <div className="search-page">
      {/* Hero Banner Section */}
      <motion.header
        className="hero-banner"
        initial={{ opacity: 0, y: -12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
      >
        <div className="hero-content">
          <div className="hero-badge">
            <span className="hero-sparkle" aria-hidden="true">✦</span>
            <span>Mô hình Tối ưu Đa tiêu chí Thông minh (Weighted Scoring)</span>
          </div>
          <h1 className="hero-title">Tìm kiếm & Khuyến nghị Gia sư Lý tưởng</h1>
          <p className="hero-subtitle">
            Cá nhân hóa điều kiện học tập, tối ưu hóa điểm số <var>S(g)</var> dựa trên 5 tiêu chí: Học phí, Khu vực, Kinh nghiệm, Đánh giá và Lịch rảnh.
          </p>
          <div className="hero-stats-row">
            <span className="hero-stat-pill"><strong>16</strong> Hồ sơ gia sư</span>
            <span className="hero-stat-pill"><strong>14</strong> Kịch bản thực nghiệm</span>
            <span className="hero-stat-pill"><strong>5</strong> Tiêu chí chuẩn hóa</span>
            <span className="hero-stat-pill highlight-pill"><strong>100%</strong> Minh bạch đóng góp</span>
          </div>
        </div>
      </motion.header>

      {/* Scenario Strip Panel */}
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
              <motion.button
                whileHover={{ scale: 1.03 }}
                whileTap={{ scale: 0.94 }}
                key={sc.id}
                type="button"
                disabled={isLoading}
                title={`${sc.title} - Kỳ vọng: ${sc.expected_raw}`}
                className={`scenario-chip ${isSelected ? 'active' : ''}`}
                onClick={() => handleSelectScenario(sc)}
              >
                <span className="sc-id">{sc.id}</span>
                <span className="sc-subj">{sc.request.subject}</span>
              </motion.button>
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
                <label htmlFor="subject-select" className="label-with-icon">
                  <SubjectIcon subject={subject} size={15} color="var(--accent)" />
                  <span>Môn học <span className="required">*</span></span>
                </label>
                <select
                  id="subject-select"
                  value={subject}
                  onChange={(e) =>
                    updateField({ subject: e.target.value, scenarioMeta: null })
                  }
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
                  {LEARNING_MODE_OPTIONS.map((opt) => (
                    <option key={opt.value} value={opt.value}>
                      {opt.label}
                    </option>
                  ))}
                </select>
                <span className="field-hint">
                  {isOnlineMode
                    ? 'Khi học Trực tuyến, tiêu chí Khu vực tự động không áp dụng.'
                    : 'Học trực tiếp tại nhà học viên ở các quận/huyện đã chọn.'}
                </span>
              </div>

              <div className={`form-field ${isOnlineMode ? 'disabled-field' : ''}`}>
                <label htmlFor="district-select">
                  Khu vực mong muốn
                </label>
                <select
                  id="district-select"
                  value={preferredDistrict}
                  disabled={isOnlineMode}
                  onChange={(e) =>
                    updateField({
                      preferredDistrict: e.target.value,
                      scenarioMeta: null,
                    })
                  }
                >
                  <option value="">-- Chọn quận/huyện (tùy chọn) --</option>
                  {DISTRICT_OPTIONS.map((dist) => (
                    <option key={dist} value={dist}>
                      {dist}
                    </option>
                  ))}
                </select>
                <span className="field-hint">
                  {isOnlineMode
                    ? 'Không áp dụng khi học trực tuyến (tự động bỏ qua).'
                    : 'Dùng để tính điểm khớp vị trí dạy trực tiếp.'}
                </span>
              </div>

              <div className="form-field">
                <label htmlFor="budget-input">
                  Ngân sách tối đa / giờ (VNĐ)
                </label>
                <input
                  id="budget-input"
                  type="number"
                  min="0"
                  step="10000"
                  placeholder="Ví dụ: 200000"
                  value={maxBudgetVnd}
                  onChange={(e) =>
                    updateField({
                      maxBudgetVnd: e.target.value,
                      scenarioMeta: null,
                    })
                  }
                />
                {budgetVietnameseWords ? (
                  <div className="currency-humanizer-tag" role="status">
                    {budgetVietnameseWords}
                  </div>
                ) : (
                  <span className="field-hint">
                    Học phí trong ngân sách đạt điểm 1,00; vượt quá 1,5 lần nhận 0 điểm.
                  </span>
                )}
              </div>

              <div className="form-field">
                <label htmlFor="topk-select">
                  Số lượng gợi ý (Top-k)
                </label>
                <select
                  id="topk-select"
                  value={topK}
                  onChange={(e) =>
                    updateField({
                      topK: Number(e.target.value),
                    })
                  }
                >
                  <option value={3}>Top 3 gia sư</option>
                  <option value={5}>Top 5 gia sư</option>
                  <option value={10}>Top 10 gia sư</option>
                </select>
                <span className="field-hint">
                  Mặc định gợi ý Top 3 gia sư có điểm tổng hợp cao nhất.
                </span>
              </div>
            </div>

            {/* Schedule Section */}
            <div className="schedule-section">
              <div className="schedule-header">
                <h3>Khung thời gian rảnh trong tuần</h3>
                <span className="field-hint">
                  {timeSlots.length > 0
                    ? `Đã chọn: ${timeSlots.length} buổi`
                    : 'Đã chọn: Chưa chọn (không tính tiêu chí lịch rảnh)'}
                </span>
              </div>

              <div className="schedule-power-bar">
                <span className="power-bar-title">Mẫu chọn nhanh:</span>
                <div className="power-bar-buttons">
                  {SCHEDULE_PATTERNS.map((pattern) => (
                    <motion.button
                      whileTap={{ scale: 0.94 }}
                      key={pattern.label}
                      type="button"
                      className="power-pill-btn"
                      onClick={() => handleApplySchedulePattern(pattern.slots)}
                    >
                      {pattern.label}
                    </motion.button>
                  ))}
                  <motion.button
                    whileTap={{ scale: 0.94 }}
                    type="button"
                    className="power-pill-btn"
                    onClick={() => handleApplySchedulePattern([])}
                  >
                    Bỏ chọn tất cả
                  </motion.button>
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
                              <motion.button
                                whileTap={{ scale: 0.92 }}
                                type="button"
                                className={`slot-button ${isSelected ? 'selected' : ''}`}
                                onClick={() => handleToggleTimeSlot(slotKey)}
                                aria-pressed={isSelected}
                              >
                                {slotKey}
                              </motion.button>
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
                  Trọng số: Bỏ qua (w = 0), Thấp (w = 1), Trung bình (w = 2, mặc định), Cao (w = 3).
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
                      <div className="criterion-title-wrap">
                        <CriteriaIcon criterion={criterion.key} size={15} className="criterion-header-icon" />
                        <strong className="criterion-title">{criterion.label}</strong>
                      </div>
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
                          <motion.button
                            whileTap={!isCriterionDisabled ? { scale: 0.95 } : undefined}
                            key={opt.value}
                            type="button"
                            disabled={isCriterionDisabled}
                            className={`seg-btn ${isActive ? 'active' : ''}`}
                            onClick={() =>
                              handlePriorityChange(criterion.key, opt.value)
                            }
                            style={{ position: 'relative' }}
                          >
                            {isActive && (
                              <motion.div
                                layoutId={`search-pill-${criterion.key}`}
                                className="active-pill-background"
                                transition={{ type: 'spring', stiffness: 450, damping: 32 }}
                              />
                            )}
                            <span className="seg-label" style={{ position: 'relative', zIndex: 1 }}>{opt.shortLabel || opt.label}</span>
                            <span className="seg-weight" style={{ position: 'relative', zIndex: 1 }}>w={opt.weight}</span>
                          </motion.button>
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

        {isLoading && (
          <div className="loading-preview-wrap">
            <div className="loading-badge">
              <span className="spinner-icon" aria-hidden="true" />
              <span>Đang kết nối API và tối ưu hóa thứ hạng gia sư...</span>
            </div>
            <SkeletonLoader count={2} />
          </div>
        )}

        <div className="submit-bar">
          <motion.button
            whileTap={!isLoading ? { scale: 0.98 } : undefined}
            whileHover={!isLoading ? { y: -1 } : undefined}
            type="submit"
            className="btn-primary btn-large"
            disabled={isLoading}
          >
            {isLoading ? (
              <span className="btn-loading-content">
                <span className="spinner-icon" aria-hidden="true" />
                <span>Đang tính điểm & xếp hạng...</span>
              </span>
            ) : (
              <span>Tìm gia sư phù hợp →</span>
            )}
          </motion.button>
        </div>
      </form>
    </div>
  )
}

export default SearchPage
