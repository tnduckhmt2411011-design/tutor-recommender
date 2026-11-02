import TutorCard from '../components/TutorCard'
import {
  formatCurrencyVnd,
  formatTeachingMode,
  getTutorProfile,
} from '../data/tutorsCatalog'

function ResultPage({
  recommendationResult,
  searchContext,
  onBackToSearch,
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

  const priorities = searchContext?.priorities || {}
  const subject = searchContext?.subject || 'Chưa chọn'
  const learningMode = searchContext?.learningMode || 'in_person'
  const preferredDistrict = searchContext?.preferredDistrict || ''
  const maxBudgetVnd = searchContext?.maxBudgetVnd || ''
  const timeSlots = searchContext?.timeSlots || []
  const topK = searchContext?.topK || 3

  return (
    <section className="result-page" aria-live="polite">
      <header className="result-page-header">
        <div>
          <span className="badge">
            CN02 — Danh sách Top-{topK} gia sư & Giải thích đa tiêu chí
          </span>
          <h2>Kết quả gợi ý gia sư phù hợp</h2>
          <p className="subtitle">
            Xếp hạng theo tổng điểm có trọng số <var>S(g)</var> giảm dần (phá hòa
            theo mã hồ sơ <var>tutor_id</var> tăng dần).
          </p>
        </div>

        {onBackToSearch && (
          <button
            type="button"
            className="btn-secondary"
            onClick={onBackToSearch}
          >
            ← Chỉnh sửa điều kiện tìm kiếm (CN01)
          </button>
        )}
      </header>

      <div className="query-summary-banner">
        <div className="query-summary-items">
          <span className="summary-chip">
            <strong>Môn học:</strong> {subject}
          </span>
          <span className="summary-chip">
            <strong>Hình thức:</strong> {formatTeachingMode(learningMode)}
          </span>
          <span className="summary-chip">
            <strong>Khu vực:</strong>{' '}
            {learningMode === 'online'
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

      {status === 'success' && results.length > 0 && (
        <div className="tutor-card-list">
          {results.map((item) => (
            <TutorCard
              key={item.tutor_id}
              item={item}
              priorities={priorities}
            />
          ))}
        </div>
      )}

      {status === 'no_match' && (
        <div className="friendly-state-card state-no-match" role="region" aria-label="Không tìm thấy gia sư phù hợp">
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
        <div className="friendly-state-card state-zero-weight" role="region" aria-label="Tổng trọng số bằng 0">
          <div className="state-icon" aria-hidden="true">
            ⚖️
          </div>
          <h3>Chưa thể xếp hạng do tổng trọng số bằng 0 (∑w_i = 0)</h3>
          <p className="state-message">
            {message ||
              'Tất cả các tiêu chí đang áp dụng đều ở mức "Không quan tâm" (w = 0). Vui lòng đặt ít nhất một tiêu chí ở mức Thấp, Trung bình hoặc Cao để hệ thống tính điểm xếp hạng.'}
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
