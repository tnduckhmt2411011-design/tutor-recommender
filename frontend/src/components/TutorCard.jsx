import StackedBarScore from './StackedBarScore'
import {
  formatCurrencyVnd,
  formatScoreVi,
  formatTeachingMode,
  getTutorProfile,
} from '../data/tutorsCatalog'

function TutorCard({ item, priorities }) {
  const profile = getTutorProfile(item.tutor_id)

  const subjectsText =
    profile?.subjects?.length > 0
      ? profile.subjects.join(', ')
      : 'Theo hồ sơ đăng ký'

  const districtsText =
    profile?.districts?.length > 0
      ? profile.districts.join(', ')
      : 'Trực tuyến (không giới hạn quận/huyện)'

  const feeText = profile
    ? formatCurrencyVnd(profile.hourly_fee_vnd)
    : 'Theo thỏa thuận'

  const experienceText =
    profile?.years_experience !== undefined &&
    profile?.years_experience !== null
      ? `${profile.years_experience} năm kinh nghiệm`
      : 'Chưa cập nhật'

  const ratingText =
    profile?.avg_rating !== null && profile?.avg_rating !== undefined
      ? `${Number(profile.avg_rating).toFixed(1).replace('.', ',')} / 5,0 ★`
      : 'Chưa có đánh giá (điểm trung tính 0,50)'

  const teachingModeText = profile
    ? formatTeachingMode(profile.teaching_mode)
    : 'Chưa cập nhật'

  const availabilityList = profile?.availability || []
  const isRealData = profile?.data_source === 'public_collected'

  return (
    <article className="tutor-card" aria-label={`Hạng ${item.rank} - ${item.tutor_id}`}>
      <div className="tutor-card-header">
        <div className="tutor-rank-group">
          <span className={`rank-medal rank-${item.rank <= 3 ? item.rank : 'other'}`}>
            Hạng #{item.rank}
          </span>
          <div>
            <div className="tutor-title-line">
              <h3 className="tutor-name">
                {item.full_name || `Gia sư ${item.tutor_id}`}
              </h3>
              <code className="tutor-id-code">{item.tutor_id}</code>
              {profile && (
                <span
                  className={`source-badge ${isRealData ? 'source-real' : 'source-sim'}`}
                >
                  {isRealData ? 'Hồ sơ thực tế' : 'Hồ sơ đối chứng'}
                </span>
              )}
            </div>
            <p className="tutor-Quick-meta">
              <strong>Môn dạy:</strong> {subjectsText} •{' '}
              <strong>Hình thức:</strong> {teachingModeText}
            </p>
          </div>
        </div>

        <div className="tutor-total-score-box">
          <span className="total-score-label">Điểm phù hợp S(g)</span>
          <strong className="total-score-value">
            {formatScoreVi(item.total_score, 3)}
          </strong>
          <span className="total-score-percent">
            Mức độ khớp {(Number(item.total_score) * 100).toFixed(1).replace('.', ',')}%
          </span>
        </div>
      </div>

      <div className="tutor-attributes-grid">
        <div className="attr-item">
          <span className="attr-label">Học phí tham khảo</span>
          <strong className="attr-value">{feeText}</strong>
        </div>
        <div className="attr-item">
          <span className="attr-label">Kinh nghiệm giảng dạy</span>
          <strong className="attr-value">{experienceText}</strong>
        </div>
        <div className="attr-item">
          <span className="attr-label">Điểm đánh giá trung bình</span>
          <strong className="attr-value">{ratingText}</strong>
        </div>
        <div className="attr-item">
          <span className="attr-label">Khu vực nhận dạy</span>
          <strong className="attr-value">{districtsText}</strong>
        </div>
      </div>

      {availabilityList.length > 0 && (
        <div className="tutor-availability-row">
          <span className="attr-label">Khung giờ rảnh của gia sư:</span>
          <div className="slot-badge-list">
            {availabilityList.map((slot) => (
              <span key={slot} className="slot-mini-badge">
                {slot}
              </span>
            ))}
          </div>
        </div>
      )}

      <StackedBarScore
        criteriaScores={item.criteria_scores}
        contributions={item.contributions}
        totalScore={item.total_score}
        priorities={priorities}
      />

      <div className="tutor-explanation-box">
        <p className="explanation-reason">
          <strong>Lý do gợi ý:</strong> {item.reason}
        </p>

        {Array.isArray(item.notes) && item.notes.length > 0 && (
          <div className="explanation-notes">
            <span className="notes-label">Ghi chú dữ liệu:</span>
            {item.notes.map((note) => (
              <span key={note} className="note-pill">
                {note}
              </span>
            ))}
          </div>
        )}
      </div>
    </article>
  )
}

export default TutorCard
