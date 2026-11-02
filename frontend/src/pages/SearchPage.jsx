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

function SearchPage({
  searchForm,
  onChangeSearchForm,
  onSubmitSearch,
  onApplyScenario,
  isLoading = false,
  apiError = '',
}) {
  const [validationError, setValidationError] = useState('')

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
        <div className="academic-label">Mô-đun CN01 · Thiết lập nhu cầu & Trọng số ưu tiên</div>
        <h1>Tìm kiếm & Khuyến nghị Gia sư Đa tiêu chí</h1>
        <p className="subtitle">
          Nhập điều kiện học tập và thiết lập trọng số ưu tiên cho 5 tiêu chí để
          xếp hạng Top-k gia sư theo mô hình Weighted Scoring.
        </p>
      </header>

      <section
        className="scenario-strip-panel"
        aria-label="Nạp nhanh 14 kịch bản thực nghiệm Bảng 5.1"
      >
        <div className="scenario-strip-header">
          <span className="strip-title">Kịch bản thực nghiệm (Bảng 5.1 · KB01 - KB14):</span>
          {scenarioMeta && (
            <span className="scenario-active-indicator">
              Đang chọn: <strong>{scenarioMeta.id}</strong> (Kỳ vọng: {scenarioMeta.expected_raw})
            </span>
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
                onClick={() => {
                  setValidationError('')
                  onApplyScenario(sc)
                }}
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
