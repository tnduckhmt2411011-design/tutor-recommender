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
        <span className="badge">CN01 — Thiết lập nhu cầu & Trọng số ưu tiên</span>
        <h1>Hệ thống khuyến nghị gia sư đa tiêu chí</h1>
        <p className="subtitle">
          Nhập điều kiện học tập và điều chỉnh mức độ ưu tiên cho 5 tiêu chí để
          xếp hạng Top-k gia sư theo mô hình Weighted Scoring.
        </p>
      </header>

      <section
        className="scenario-preset-card"
        aria-label="Nạp nhanh 14 kịch bản thực nghiệm Bảng 5.1"
      >
        <div className="scenario-preset-header">
          <div>
            <h2>Nạp nhanh 14 kịch bản thực nghiệm (Bảng 5.1 — KB01 đến KB14)</h2>
            <p className="field-hint">
              Chọn một kịch bản để tự động điền thông số truy vấn và chạy đối
              chiếu trực tiếp với kết quả kỳ vọng trong đề cương.
            </p>
          </div>
          {scenarioMeta && (
            <span className="scenario-selected-badge">
              Đang chọn: <strong>{scenarioMeta.id}</strong> — Kỳ vọng:{' '}
              {scenarioMeta.expected_raw}
            </span>
          )}
        </div>

        <div className="scenario-chip-list">
          {SCENARIOS_CATALOG.map((sc) => {
            const isSelected = scenarioMeta?.id === sc.id
            return (
              <button
                key={sc.id}
                type="button"
                disabled={isLoading}
                title={sc.title}
                className={`scenario-chip ${isSelected ? 'active' : ''}`}
                onClick={() => {
                  setValidationError('')
                  onApplyScenario(sc)
                }}
              >
                <strong>{sc.id}</strong>
                <span>{sc.request.subject}</span>
              </button>
            )
          })}
        </div>
      </section>

      <form className="search-form" onSubmit={handleSubmit} noValidate>
        <section className="form-card">
          <div className="card-header">
            <h2>1. Thông tin nhu cầu học tập (Bảng 3.4)</h2>
            <button
              type="button"
              className="btn-secondary"
              onClick={handleResetDefaults}
            >
              Đặt lại mẫu mặc định
            </button>
          </div>

          <div className="form-grid">
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
                Khi chọn Trực tuyến, tiêu chí Khu vực sẽ tự động không áp dụng.
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
                  Dùng để chấm điểm mức độ khớp khu vực dạy trực tiếp.
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
                placeholder="Để trống nếu không giới hạn (ví dụ: 200000)"
                value={maxBudgetVnd}
                onChange={(e) =>
                  updateField({
                    maxBudgetVnd: e.target.value,
                    scenarioMeta: null,
                  })
                }
              />
              <span className="field-hint">
                Học phí trong ngân sách đạt điểm tối đa 1,00; vượt quá 1,5 lần
                ngân sách nhận 0 điểm.
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
                Mặc định lấy Top 3 gia sư có điểm tổng hợp cao nhất.
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
                      : 'Chưa chọn (không lọc theo lịch rảnh)'}
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
                  Bỏ chọn tất cả khung giờ
                </button>
              )}
            </div>

            <div className="schedule-grid-wrapper">
              <table className="schedule-table">
                <thead>
                  <tr>
                    <th>Buổi / Thứ</th>
                    {DAYS_OF_WEEK.map((day) => (
                      <th key={day.code}>{day.label}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {SESSIONS_OF_DAY.map((session) => (
                    <tr key={session.code}>
                      <td className="session-label">{session.label}</td>
                      {DAYS_OF_WEEK.map((day) => {
                        const slotKey = `${day.code}-${session.code}`
                        const isSelected = timeSlots.includes(slotKey)
                        return (
                          <td key={slotKey}>
                            <button
                              type="button"
                              className={`slot-chip ${isSelected ? 'selected' : ''}`}
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

        <section className="form-card">
          <div className="card-header">
            <div>
              <h2>2. Mức độ ưu tiên cho 5 tiêu chí (Bảng 3.5)</h2>
              <p className="field-hint">
                Quy đổi trọng số: Không quan tâm (w = 0), Thấp (w = 1), Trung
                bình (w = 2, mặc định), Cao (w = 3).
              </p>
            </div>
          </div>

          <div className="criteria-list">
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
                  className={`criterion-row ${isCriterionDisabled ? 'inactive' : ''}`}
                >
                  <div className="criterion-info">
                    <div className="criterion-title-row">
                      <span className="criterion-name">{criterion.label}</span>
                      {isCriterionDisabled && (
                        <span className="inactive-pill">
                          Tự động bỏ qua do chưa nhập điều kiện tương ứng
                        </span>
                      )}
                    </div>
                    <p className="criterion-desc">{criterion.description}</p>
                  </div>

                  <div
                    className="priority-group"
                    role="group"
                    aria-label={`Mức ưu tiên ${criterion.label}`}
                  >
                    {PRIORITY_OPTIONS.map((option) => {
                      const isActive = currentLevel === option.value
                      return (
                        <button
                          key={option.value}
                          type="button"
                          className={`priority-btn ${isActive ? 'active' : ''}`}
                          onClick={() =>
                            handlePriorityChange(criterion.key, option.value)
                          }
                        >
                          <span>{option.label}</span>
                          <small>w={option.weight}</small>
                        </button>
                      )
                    })}
                  </div>
                </div>
              )
            })}
          </div>
        </section>

        {validationError && (
          <div className="alert alert-error" role="alert">
            <strong>Lỗi kiểm tra biểu mẫu:</strong> {validationError}
          </div>
        )}

        {apiError && (
          <div className="alert alert-error" role="alert">
            <strong>Lỗi gọi API:</strong> {apiError}
          </div>
        )}

        <div className="submit-bar">
          <button type="submit" className="btn-primary" disabled={isLoading}>
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
