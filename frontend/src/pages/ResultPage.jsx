import TutorCard from '../components/TutorCard'
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
          <div className="academic-label">
            Mô-đun CN02 & CN03 · Kết quả xếp hạng Top-{topK} & Điều chỉnh ưu tiên
          </div>
          <h1>Kết quả Gợi ý Gia sư Phù hợp</h1>
          <p className="subtitle">
            Xếp hạng theo tổng điểm có trọng số <var>S(g)</var> giảm dần (phá hòa theo mã hồ sơ <var>tutor_id</var>).
            Sử dụng bảng điều khiển CN03 bên trái để cập nhật lại thứ hạng ngay lập tức.
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

      {/* KPI & Summary Strip */}
      <div className="workbench-kpi-strip">
        <div className="kpi-chips">
          {scenarioMeta && (
            <div className="kpi-chip kpi-scenario">
              <span className="kpi-label">Kịch bản:</span>
              <strong className="kpi-val">{scenarioMeta.id}</strong>
              <span className="kpi-note">(Kỳ vọng: {scenarioMeta.expected_raw})</span>
            </div>
          )}
          <div className="kpi-chip">
            <span className="kpi-label">Môn:</span>
            <strong className="kpi-val">{subject}</strong>
          </div>
          <div className="kpi-chip">
            <span className="kpi-label">Hình thức:</span>
            <span className="kpi-val">{formatTeachingMode(learningMode)}</span>
          </div>
          <div className="kpi-chip">
            <span className="kpi-label">Khu vực:</span>
            <span className="kpi-val">
              {isOnlineMode
                ? 'Không áp dụng (Online)'
                : preferredDistrict || 'Không giới hạn'}
            </span>
          </div>
          <div className="kpi-chip">
            <span className="kpi-label">Ngân sách:</span>
            <span className="kpi-val">
              {String(maxBudgetVnd).trim() !== ''
                ? formatCurrencyVnd(Number(maxBudgetVnd))
                : 'Không giới hạn'}
            </span>
          </div>
          <div className="kpi-chip">
            <span className="kpi-label">Lịch:</span>
            <span className="kpi-val">
              {timeSlots.length > 0 ? timeSlots.join(', ') : 'Không giới hạn'}
            </span>
          </div>
        </div>

        <div className="kpi-funnel">
          <span className="funnel-step">
            Kho: <strong>{totalCandidates}</strong> hồ sơ
          </span>
          <span className="funnel-sep">→</span>
          <span className="funnel-step">
            Hợp lệ: <strong>{qualifiedCandidates}</strong> ứng viên
          </span>
          <span className="funnel-sep">→</span>
          <span className="funnel-step">
            Top-{topK}: <strong>{results.length}</strong> gợi ý
          </span>
        </div>
      </div>

      {apiError && (
        <div className="alert alert-error" role="alert">
          <strong>Lỗi máy chủ:</strong> {apiError}
        </div>
      )}

      {/* 2-Column Workbench Layout: Left = CN03 Interactive Rail, Right = Ranked Results */}
      <div className="result-workbench-layout">
        {onUpdatePriorities && (
          <aside
            className="cn03-rail panel"
            aria-label="CN03 - Điều chỉnh nhanh mức ưu tiên tiêu chí"
          >
            <div className="cn03-rail-head">
              <div>
                <span className="academic-label">Mô-đun CN03 · Tương tác</span>
                <h3 className="rail-title">Điều chỉnh mức ưu tiên</h3>
              </div>
              {isUpdatingPriorities && (
                <span className="updating-status" role="status">
                  Đang tính lại...
                </span>
              )}
            </div>
            <p className="rail-desc">
              Thay đổi mức ưu tiên cho bất kỳ tiêu chí nào để gọi lại API và cập nhật thứ hạng tức thì.
            </p>

            <div className="cn03-presets-list">
              <span className="presets-label">Nạp nhanh trọng số:</span>
              <div className="presets-buttons">
                <button
                  type="button"
                  className="preset-pill"
                  disabled={isUpdatingPriorities}
                  onClick={() => handleQuickPreset({ ...DEFAULT_PRIORITIES })}
                >
                  Mặc định (w=2)
                </button>
                <button
                  type="button"
                  className="preset-pill"
                  disabled={isUpdatingPriorities}
                  onClick={() =>
                    handleQuickPreset({
                      fee: 'high',
                      district: 'low',
                      experience: 'low',
                      rating: 'low',
                      availability: 'low',
                    })
                  }
                >
                  Ưu tiên Học phí
                </button>
                <button
                  type="button"
                  className="preset-pill"
                  disabled={isUpdatingPriorities}
                  onClick={() =>
                    handleQuickPreset({
                      fee: 'low',
                      district: 'low',
                      experience: 'high',
                      rating: 'high',
                      availability: 'low',
                    })
                  }
                >
                  Ưu tiên KN & Đánh giá
                </button>
                <button
                  type="button"
                  className="preset-pill preset-pill-warn"
                  disabled={isUpdatingPriorities}
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

            <div className="cn03-controls-stack">
              {CRITERIA_LIST.map((criterion) => {
                const isCriterionInactive =
                  (criterion.key === 'district' &&
                    (isOnlineMode || !String(preferredDistrict).trim())) ||
                  (criterion.key === 'fee' && !String(maxBudgetVnd).trim()) ||
                  (criterion.key === 'availability' && timeSlots.length === 0)

                const currentLevel = priorities[criterion.key] || 'medium'

                return (
                  <div
                    key={criterion.key}
                    className={`cn03-item ${isCriterionInactive ? 'item-inactive' : ''}`}
                  >
                    <div className="cn03-item-head">
                      <span className="cn03-item-name">{criterion.label}</span>
                      {isCriterionInactive && (
                        <span className="item-inactive-tag">Không áp dụng</span>
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
                            disabled={isUpdatingPriorities}
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
            <div className="tutor-cards-list">
              {results.map((item) => {
                const delta = rankDeltas[item.tutor_id]
                return (
                  <div key={item.tutor_id} className="tutor-card-container">
                    {delta !== undefined && delta !== 0 && (
                      <div
                        className={`rank-delta-indicator ${delta > 0 ? 'delta-up' : 'delta-down'}`}
                      >
                        {delta > 0
                          ? `↑ Tăng ${delta} bậc sau khi điều chỉnh mức ưu tiên (CN03)`
                          : `↓ Giảm ${Math.abs(delta)} bậc sau khi điều chỉnh mức ưu tiên (CN03)`}
                      </div>
                    )}
                    <TutorCard item={item} priorities={priorities} />
                  </div>
                )
              })}
            </div>
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

              <div className="state-suggestions">
                <p>
                  <strong>Gợi ý điều chỉnh:</strong> Mở rộng khung giờ rảnh, chọn hình thức <em>Không yêu cầu (Cả hai)</em> hoặc môn học khác.
                </p>
                {onBackToSearch && (
                  <button
                    type="button"
                    className="btn-primary"
                    onClick={onBackToSearch}
                  >
                    Quay lại điều chỉnh điều kiện tìm kiếm
                  </button>
                )}
              </div>
            </div>
          )}

          {status === 'zero_weight' && (
            <div
              className="friendly-state-card state-zero-weight"
              role="region"
              aria-label="Tổng trọng số bằng 0"
            >
              <div className="state-icon" aria-hidden="true">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M12 3v18M6 8l6-5 6 5M6 8l-3 7h6l-3-7zm12 0l-3 7h6l-3-7z" />
                </svg>
              </div>
              <h3>Chưa thể xếp hạng do tổng trọng số bằng 0 (∑w_i = 0)</h3>
              <p className="state-message">
                {message ||
                  'Tất cả các tiêu chí đang áp dụng đều ở mức "Không quan tâm" (w = 0). Vui lòng đặt ít nhất một tiêu chí ở mức Thấp, Trung bình hoặc Cao trên thanh điều khiển CN03 bên trái.'}
              </p>

              {unrankedCandidates.length > 0 && (
                <div className="candidate-fallback-box">
                  <h4>
                    Danh sách {unrankedCandidates.length} gia sư đã vượt qua bước lọc bắt buộc (chưa xếp hạng):
                  </h4>
                  <div className="fallback-candidate-grid">
                    {unrankedCandidates.map((id) => {
                      const prof = getTutorProfile(id)
                      return (
                        <div key={id} className="fallback-candidate-item">
                          <div className="fallback-item-head">
                            <code>{id}</code>
                            {prof && (
                              <span>{formatTeachingMode(prof.teaching_mode)}</span>
                            )}
                          </div>
                          {prof && (
                            <p className="fallback-item-meta">
                              Môn: {prof.subjects.join(', ')} · Học phí: {formatCurrencyVnd(prof.hourly_fee_vnd)} · KN: {prof.years_experience} năm
                            </p>
                          )}
                        </div>
                      )
                    })}
                  </div>
                </div>
              )}
            </div>
          )}
        </main>
      </div>
    </section>
  )
}

export default ResultPage
