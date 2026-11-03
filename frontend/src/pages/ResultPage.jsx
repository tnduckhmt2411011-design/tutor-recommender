import { motion, AnimatePresence } from 'motion/react'
import TutorCard from '../components/TutorCard'
import CriteriaIcon from '../components/CriteriaIcon'
import {
  CRITERIA_LIST,
  DEFAULT_PRIORITIES,
  PRIORITY_OPTIONS,
} from '../services/api'
import {
  formatCurrencyVnd,
  formatTeachingMode,
  getTutorProfile,
} from '../data/tutorsCatalog'

function ResultPage({
  recommendationResult,
  searchContext,
  onBackToSearch,
  onUpdatePriorities,
  isUpdatingPriorities = false,
  latencyMs = null,
  apiError = '',
  rankDeltas = {},
}) {
  if (!recommendationResult) {
    return null
  }

  const {
    status,
    message,
    total_candidates: totalCandidates = 0,
    qualified_candidates: qualifiedCandidates = 0,
    results = [],
    unranked_candidates: unrankedCandidates = [],
    insufficient_data_candidates: insufficientDataCandidates = [],
  } = recommendationResult

  const priorities = searchContext?.priorities || DEFAULT_PRIORITIES
  const subject = searchContext?.subject || 'Chưa chọn'
  const learningMode = searchContext?.learningMode || 'in_person'
  const preferredDistrict = searchContext?.preferredDistrict || ''
  const maxBudgetVnd = searchContext?.maxBudgetVnd ?? ''
  const timeSlots = searchContext?.timeSlots || []
  const topK = searchContext?.topK || 3
  const scenarioMeta = searchContext?.scenarioMeta || null

  const isOnlineMode = learningMode === 'online'

  const totalActiveWeight = CRITERIA_LIST.reduce((sum, crit) => {
    const isInactive =
      (crit.key === 'district' &&
        (isOnlineMode || !String(preferredDistrict).trim())) ||
      (crit.key === 'fee' && !String(maxBudgetVnd).trim()) ||
      (crit.key === 'availability' && timeSlots.length === 0)
    if (isInactive) return sum
    const level = priorities[crit.key] || 'medium'
    const w = PRIORITY_OPTIONS.find((opt) => opt.value === level)?.weight ?? 2
    return sum + w
  }, 0)

  const handleCriterionPriorityClick = (criterionKey, nextLevel) => {
    if (!onUpdatePriorities) return
    const nextPriorities = {
      ...priorities,
      [criterionKey]: nextLevel,
    }
    onUpdatePriorities(nextPriorities)
  }

  const handleQuickPreset = (presetPriorities) => {
    if (!onUpdatePriorities) return
    onUpdatePriorities(presetPriorities)
  }

  return (
    <section className="result-page" aria-live="polite">
      <header className="page-header result-page-header">
        <div>
          <h1>Kết quả Gợi ý Gia sư Phù hợp</h1>
          <p className="subtitle">
            Mô-đun CN02 & CN03 · Xếp hạng theo tổng điểm có trọng số <var>S(g)</var> giảm dần (phá hòa theo mã hồ sơ <var>tutor_id</var>).
            Sử dụng bảng điều khiển bên trái để cập nhật lại thứ hạng tức thì.
          </p>
        </div>

        <div className="header-actions">
          {latencyMs !== null && (
            <span
              className={`latency-indicator ${latencyMs < 1000 ? 'latency-good' : 'latency-warn'}`}
              title="Thời gian phản hồi toàn trình API"
            >
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" aria-hidden="true">
                <circle cx="12" cy="12" r="10" />
                <polyline points="12 6 12 12 16 14" />
              </svg>
              <span>{latencyMs.toFixed(1).replace('.', ',')} ms</span>
            </span>
          )}

          {onBackToSearch && (
            <button
              type="button"
              className="btn-secondary"
              onClick={onBackToSearch}
            >
              ← Điều chỉnh điều kiện tìm kiếm (CN01)
            </button>
          )}
        </div>
      </header>

      {/* KPI Strip */}
      <div className="workbench-kpi-strip">
        <div className="kpi-chips">
          {scenarioMeta && (
            <span className="kpi-chip kpi-scenario">
              <span className="kpi-chip-label">Kịch bản:</span>{' '}
              <strong>{scenarioMeta.id}</strong>{' '}
              <span className="kpi-chip-detail">({scenarioMeta.expected_raw})</span>
            </span>
          )}
          <span className="kpi-chip">
            <span className="kpi-chip-label">Môn:</span> <strong>{subject}</strong>
          </span>
          <span className="kpi-chip">
            <span className="kpi-chip-label">Hình thức:</span>{' '}
            <strong>{formatTeachingMode(learningMode)}</strong>
          </span>
          {learningMode !== 'online' && preferredDistrict && (
            <span className="kpi-chip">
              <span className="kpi-chip-label">Khu vực:</span>{' '}
              <strong>{preferredDistrict}</strong>
            </span>
          )}
          {maxBudgetVnd && (
            <span className="kpi-chip">
              <span className="kpi-chip-label">Ngân sách:</span>{' '}
              <strong>{Number(maxBudgetVnd).toLocaleString('vi-VN')} VNĐ/giờ</strong>
            </span>
          )}
          <span className="kpi-chip">
            <span className="kpi-chip-label">Lịch:</span>{' '}
            <strong>
              {timeSlots.length > 0 ? `${timeSlots.length} buổi` : 'Không giới hạn'}
            </strong>
          </span>
        </div>

        <div className="kpi-funnel">
          <span className="funnel-step">Kho: <strong>{totalCandidates}</strong> hồ sơ</span>
          <span className="funnel-arrow">→</span>
          <span className="funnel-step">Hợp lệ: <strong>{qualifiedCandidates}</strong> ứng viên</span>
          <span className="funnel-arrow">→</span>
          <span className="funnel-step funnel-highlight">Top-3: <strong>{results.length}</strong> gợi ý</span>
        </div>
      </div>

      {apiError && (
        <div className="alert alert-error" role="alert">
          <strong>Lỗi khi gửi yêu cầu tới máy chủ:</strong> {apiError}
        </div>
      )}

      {/* 2-Column Result Workbench */}
      <div className="results-workbench">
        {/* CN03 Rail Bên Trái */}
        {status === 'success' && (
          <aside className="cn03-rail" aria-label="Bảng điều chỉnh mức ưu tiên trực tiếp CN03">
            <div className="rail-header">
              <h3>Điều chỉnh mức ưu tiên (CN03)</h3>
              <p className="rail-hint">
                Thay đổi mức ưu tiên cho bất kỳ tiêu chí nào để gọi lại API và cập nhật thứ hạng tức thì.
              </p>
            </div>

            {totalActiveWeight === 0 && (
              <div className="zero-weight-warning" role="alert">
                <span className="warning-icon" aria-hidden="true">⚠️</span>
                <div>
                  <strong>Tổng trọng số ∑w_i = 0</strong>
                  <p>Tất cả tiêu chí đang ở mức w=0. Hệ thống phá hòa theo thứ tự mã hồ sơ gia sư.</p>
                </div>
              </div>
            )}

            {/* Nạp nhanh trọng số */}
            <div className="rail-presets-box">
              <span className="presets-label">Nạp nhanh trọng số:</span>
              <div className="presets-buttons">
                <button
                  type="button"
                  className="preset-btn"
                  onClick={() =>
                    handleQuickPreset({
                      fee: 'medium',
                      district: 'medium',
                      experience: 'medium',
                      rating: 'medium',
                      availability: 'medium',
                    })
                  }
                >
                  Mặc định (w=2)
                </button>
                <button
                  type="button"
                  className="preset-btn"
                  onClick={() =>
                    handleQuickPreset({
                      fee: 'high',
                      district: 'low',
                      experience: 'none',
                      rating: 'none',
                      availability: 'low',
                    })
                  }
                >
                  Ưu tiên Học phí
                </button>
                <button
                  type="button"
                  className="preset-btn"
                  onClick={() =>
                    handleQuickPreset({
                      fee: 'none',
                      district: 'none',
                      experience: 'high',
                      rating: 'high',
                      availability: 'none',
                    })
                  }
                >
                  Ưu tiên KN &amp; Đánh giá
                </button>
                <button
                  type="button"
                  className="preset-btn preset-danger"
                  onClick={() =>
                    handleQuickPreset({
                      fee: 'none',
                      district: 'none',
                      experience: 'none',
                      rating: 'none',
                      availability: 'none',
                    })
                  }
                >
                  Thử ∑w_i = 0
                </button>
              </div>
            </div>

            {/* Danh sách 5 tiêu chí CN03 */}
            <div className="cn03-criteria-list">
              {CRITERIA_LIST.map((criterion) => {
                const isInactive =
                  (criterion.key === 'district' &&
                    (isOnlineMode || !String(preferredDistrict).trim())) ||
                  (criterion.key === 'fee' && !String(maxBudgetVnd).trim()) ||
                  (criterion.key === 'availability' && timeSlots.length === 0)

                const currentLevel = priorities[criterion.key] || 'medium'

                return (
                  <div
                    key={criterion.key}
                    className={`cn03-criterion-item ${isInactive ? 'is-inactive' : ''}`}
                  >
                    <div className="item-title-row">
                      <div className="criterion-name-with-icon">
                        <CriteriaIcon criterion={criterion.key} size={14} className="rail-criteria-icon" />
                        <strong className="item-name">{criterion.label}</strong>
                      </div>
                      {isInactive && (
                        <span className="item-inactive-tag">
                          Không áp dụng
                        </span>
                      )}
                    </div>

                    <div
                      className="cn03-btn-segmented"
                      role="group"
                      aria-label={`Mức ưu tiên ${criterion.label}`}
                    >
                      {PRIORITY_OPTIONS.map((opt) => {
                        const isActive = currentLevel === opt.value
                        return (
                          <button
                            key={opt.value}
                            type="button"
                            disabled={isInactive || isUpdatingPriorities}
                            className={`cn03-step-btn ${isActive ? 'active' : ''}`}
                            onClick={() =>
                              handleCriterionPriorityClick(
                                criterion.key,
                                opt.value
                              )
                            }
                          >
                            <span className="step-label">{opt.label}</span>
                            <span className="step-w">w={opt.weight}</span>
                          </button>
                        )
                      })}
                    </div>
                  </div>
                )
              })}
            </div>
          </aside>
        )}

        <main className="results-main">
          {status === 'success' && results.length > 0 && (
            <motion.div layout className="tutor-cards-list">
              <AnimatePresence mode="popLayout">
                {results.map((item, idx) => {
                  const delta = rankDeltas[item.tutor_id]
                  return (
                    <motion.div
                      layout
                      key={item.tutor_id}
                      className="tutor-card-container"
                      initial={{ opacity: 0, y: 18 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, scale: 0.95 }}
                      transition={{
                        type: 'spring',
                        stiffness: 320,
                        damping: 26,
                        delay: idx * 0.08,
                      }}
                    >
                      {delta !== undefined && delta !== 0 && (
                        <motion.div
                          layout="position"
                          initial={{ opacity: 0, scale: 0.95 }}
                          animate={{ opacity: 1, scale: 1 }}
                          className={`rank-delta-indicator ${delta > 0 ? 'delta-up' : 'delta-down'}`}
                        >
                          {delta > 0
                            ? `↑ Tăng ${delta} bậc sau khi điều chỉnh mức ưu tiên (CN03)`
                            : `↓ Giảm ${Math.abs(delta)} bậc sau khi điều chỉnh mức ưu tiên (CN03)`}
                        </motion.div>
                      )}
                      <TutorCard item={item} priorities={priorities} />
                    </motion.div>
                  )
                })}
              </AnimatePresence>
            </motion.div>
          )}

          {status === 'no_match' && (
            <div
              className="friendly-state-card state-no-match"
              role="region"
              aria-label="Không tìm thấy gia sư phù hợp"
            >
              <div className="state-icon" aria-hidden="true">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="11" cy="11" r="8" />
                  <path d="M21 21l-4.35-4.35" />
                </svg>
              </div>
              <h3>Không tìm thấy gia sư thỏa mãn điều kiện</h3>
              <p className="state-message">
                {message ||
                  'Không có gia sư nào trong cơ sở dữ liệu đáp ứng đồng thời các điều kiện lọc bắt buộc hoặc ngưỡng dữ liệu tối thiểu.'}
              </p>

              {insufficientDataCandidates.length > 0 && (
                <div className="candidate-fallback-box">
                  <h4>
                    Ứng viên qua lọc bắt buộc nhưng chưa đủ ngưỡng dữ liệu tối thiểu ({insufficientDataCandidates.length}):
                  </h4>
                  <div className="fallback-candidate-grid">
                    {insufficientDataCandidates.map((id) => {
                      const prof = getTutorProfile(id)
                      return (
                        <div key={id} className="fallback-candidate-item">
                          <code>{id}</code>
                          {prof && (
                            <span className="fallback-meta">
                              {prof.subjects.join(', ')} · {formatCurrencyVnd(prof.hourly_fee_vnd)}
                            </span>
                          )}
                        </div>
                      )
                    })}
                  </div>
                </div>
              )}
            </div>
          )}

          {status === 'error' && (
            <div className="friendly-state-card state-error" role="alert">
              <h3>Đã xảy ra lỗi khi gợi ý</h3>
              <p>{message || 'Vui lòng kiểm tra lại thông số đầu vào và thử lại.'}</p>
            </div>
          )}

          {unrankedCandidates.length > 0 && (
            <div className="unranked-summary">
              <span className="summary-label">
                Ứng viên hợp lệ khác trong kho nhưng ngoài Top-{topK}:
              </span>{' '}
              {unrankedCandidates.map((id) => (
                <code key={id} className="candidate-tag">
                  {id}
                </code>
              ))}
            </div>
          )}
        </main>
      </div>
    </section>
  )
}

export default ResultPage
