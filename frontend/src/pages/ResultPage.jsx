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
      <header className="result-page-header">
        <div>
          <span className="badge">
            CN02 & CN03 — Kết quả xếp hạng Top-{topK} & Điều chỉnh ưu tiên tức thì
          </span>
          <h2>Kết quả gợi ý gia sư phù hợp</h2>
          <p className="subtitle">
            Xếp hạng theo tổng điểm có trọng số <var>S(g)</var> giảm dần (phá hòa
            theo mã hồ sơ <var>tutor_id</var> tăng dần). Thay đổi mức ưu tiên bên
            dưới để cập nhật lại thứ hạng ngay lập tức.
          </p>
        </div>

        <div className="result-header-actions">
          {latencyMs !== null && (
            <span
              className={`latency-badge ${latencyMs < 1000 ? 'latency-fast' : 'latency-slow'}`}
              title="Thời gian phản hồi toàn trình từ lúc gửi request đến khi nhận kết quả"
            >
              ⚡ Phản hồi API: {latencyMs.toFixed(1).replace('.', ',')} ms (
              {latencyMs < 1000 ? '< 1 giây' : '≥ 1 giây'})
            </span>
          )}

          {onBackToSearch && (
            <button
              type="button"
              className="btn-secondary"
              onClick={onBackToSearch}
            >
              ← Chỉnh sửa điều kiện tìm kiếm (CN01)
            </button>
          )}
        </div>
      </header>

      <div className="query-summary-banner">
        <div className="query-summary-items">
          {scenarioMeta && (
            <span className="summary-chip scenario-active-chip">
              <strong>Kịch bản:</strong> {scenarioMeta.id} (Kỳ vọng Bảng 5.1:{' '}
              {scenarioMeta.expected_raw})
            </span>
          )}
          <span className="summary-chip">
            <strong>Môn học:</strong> {subject}
          </span>
          <span className="summary-chip">
            <strong>Hình thức:</strong> {formatTeachingMode(learningMode)}
          </span>
          <span className="summary-chip">
            <strong>Khu vực:</strong>{' '}
            {isOnlineMode
              ? 'Không áp dụng (Online)'
              : preferredDistrict || 'Không giới hạn'}
          </span>
          <span className="summary-chip">
            <strong>Ngân sách tối đa:</strong>{' '}
            {String(maxBudgetVnd).trim() !== ''
              ? formatCurrencyVnd(Number(maxBudgetVnd))
              : 'Không giới hạn'}
          </span>
          <span className="summary-chip">
            <strong>Khung giờ:</strong>{' '}
            {timeSlots.length > 0 ? timeSlots.join(', ') : 'Không giới hạn'}
          </span>
        </div>

        <div className="candidate-funnel">
          <span>
            Kho dữ liệu: <strong>{totalCandidates}</strong> hồ sơ
          </span>
          <span className="funnel-arrow">→</span>
          <span>
            Qua lọc bắt buộc: <strong>{qualifiedCandidates}</strong> ứng viên
          </span>
          <span className="funnel-arrow">→</span>
          <span>
            Hiển thị Top-{topK}: <strong>{results.length}</strong> gia sư
          </span>
        </div>
      </div>

      {onUpdatePriorities && (
        <section
          className="cn03-priority-panel"
          aria-label="CN03 — Điều chỉnh nhanh mức ưu tiên tiêu chí"
        >
          <div className="cn03-panel-header">
            <div>
              <div className="cn03-title-row">
                <span className="cn03-tag">CN03 — Tương tác trực tiếp</span>
                <h3>Điều chỉnh mức ưu tiên & Cập nhật thứ hạng tức thì</h3>
                {isUpdatingPriorities && (
                  <span className="updating-pill" role="status">
                    Đang tính lại điểm...
                  </span>
                )}
              </div>
              <p className="field-hint">
                Bấm chọn mức ưu tiên mới cho bất kỳ tiêu chí nào để tự động gọi
                lại <code>POST /api/recommend</code> và quan sát sự thay đổi thứ
                hạng cùng thanh điểm xếp chồng ngay trên trang.
              </p>
            </div>

            <div className="cn03-preset-actions">
              <button
                type="button"
                className="btn-mini"
                disabled={isUpdatingPriorities}
                onClick={() => handleQuickPreset({ ...DEFAULT_PRIORITIES })}
              >
                Mặc định (Tất cả w=2)
              </button>
              <button
                type="button"
                className="btn-mini"
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
                Ưu tiên Học phí (w=3)
              </button>
              <button
                type="button"
                className="btn-mini"
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
                Ưu tiên Kinh nghiệm & Đánh giá
              </button>
              <button
                type="button"
                className="btn-mini btn-mini-warn"
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
                Thử ∑w_i = 0 (zero_weight)
              </button>
            </div>
          </div>

          <div className="cn03-grid">
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
                  className={`cn03-criterion-box ${isCriterionInactive ? 'inactive' : ''}`}
                >
                  <div className="cn03-criterion-head">
                    <span className="cn03-criterion-label">
                      {criterion.label}
                    </span>
                    {isCriterionInactive && (
                      <span className="cn03-inactive-note">
                        Không áp dụng ở truy vấn này
                      </span>
                    )}
                  </div>

                  <div
                    className="cn03-btn-group"
                    role="group"
                    aria-label={`Đổi nhanh mức ưu tiên ${criterion.label}`}
                  >
                    {PRIORITY_OPTIONS.map((opt) => {
                      const isActive = currentLevel === opt.value
                      return (
                        <button
                          key={opt.value}
                          type="button"
                          disabled={isUpdatingPriorities}
                          className={`cn03-btn ${isActive ? 'active' : ''}`}
                          onClick={() =>
                            handleCriterionPriorityClick(
                              criterion.key,
                              opt.value
                            )
                          }
                        >
                          <span>{opt.label}</span>
                          <small>w={opt.weight}</small>
                        </button>
                      )
                    })}
                  </div>
                </div>
              )
            })}
          </div>
        </section>
      )}

      {apiError && (
        <div className="alert alert-error" role="alert">
          <strong>Lỗi khi cập nhật kết quả từ máy chủ:</strong> {apiError}
        </div>
      )}

      {status === 'success' && results.length > 0 && (
        <div className="tutor-card-list">
          {results.map((item) => {
            const delta = rankDeltas[item.tutor_id]
            return (
              <div key={item.tutor_id} className="tutor-card-wrapper">
                {delta !== undefined && delta !== 0 && (
                  <div
                    className={`rank-delta-banner ${delta > 0 ? 'delta-up' : 'delta-down'}`}
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
            🔍
          </div>
          <h3>Không tìm thấy gia sư thỏa mãn điều kiện</h3>
          <p className="state-message">
            {message ||
              'Không có gia sư nào trong kho dữ liệu đáp ứng đồng thời các điều kiện lọc bắt buộc hoặc ngưỡng dữ liệu tối thiểu.'}
          </p>

          {insufficientDataCandidates.length > 0 && (
            <div className="candidate-fallback-box">
              <h4>
                Ứng viên qua lọc bắt buộc nhưng chưa đủ ngưỡng dữ liệu tối thiểu
                ({insufficientDataCandidates.length}):
              </h4>
              <div className="fallback-candidate-grid">
                {insufficientDataCandidates.map((id) => {
                  const prof = getTutorProfile(id)
                  return (
                    <div key={id} className="fallback-candidate-item">
                      <strong>{id}</strong>
                      {prof && (
                        <span>
                          {prof.subjects.join(', ')} •{' '}
                          {formatCurrencyVnd(prof.hourly_fee_vnd)}
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
              <strong>Gợi ý điều chỉnh:</strong> Thử mở rộng khung giờ rảnh,
              chọn hình thức <em>Không yêu cầu (Cả hai)</em> hoặc chọn môn học
              khác để tìm thêm ứng viên.
            </p>
            {onBackToSearch && (
              <button
                type="button"
                className="btn-primary"
                onClick={onBackToSearch}
              >
                Quay lại điều chỉnh tiêu chí tìm kiếm
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
            ⚖️
          </div>
          <h3>Chưa thể xếp hạng do tổng trọng số bằng 0 (∑w_i = 0)</h3>
          <p className="state-message">
            {message ||
              'Tất cả các tiêu chí đang áp dụng đều ở mức "Không quan tâm" (w = 0). Vui lòng đặt ít nhất một tiêu chí ở mức Thấp, Trung bình hoặc Cao ngay trên bảng CN03 phía trên để hệ thống tính điểm xếp hạng.'}
          </p>

          {unrankedCandidates.length > 0 && (
            <div className="candidate-fallback-box">
              <h4>
                Danh sách {unrankedCandidates.length} gia sư đã vượt qua bước lọc
                điều kiện bắt buộc (chưa xếp hạng):
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
                          Môn: {prof.subjects.join(', ')} • Học phí:{' '}
                          {formatCurrencyVnd(prof.hourly_fee_vnd)} • KN:{' '}
                          {prof.years_experience} năm
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
    </section>
  )
}

export default ResultPage
