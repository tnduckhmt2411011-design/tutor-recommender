import { useState } from 'react'
import { motion } from 'motion/react'
import StackedBarScore from './StackedBarScore'
import TutorAvatar from './TutorAvatar'
import SubjectIcon from './SubjectIcon'
import CriteriaIcon from './CriteriaIcon'
import {
  formatCurrencyVnd,
  formatScoreVi,
  formatTeachingMode,
  getTutorProfile,
} from '../data/tutorsCatalog'

function TutorCard({ item, priorities }) {
  const [activeCriterion, setActiveCriterion] = useState(null)
  const profile = getTutorProfile(item.tutor_id)

  const subjectsText =
    profile?.subjects?.length > 0
      ? profile.subjects.join(', ')
      : 'Theo hồ sơ đăng ký'

  const primarySubject = profile?.subjects?.[0] || 'Toán'

  const districtsText =
    profile?.districts?.length > 0
      ? profile.districts.join(', ')
      : 'Trực tuyến (không giới hạn khu vực)'

  const feeText = profile
    ? formatCurrencyVnd(profile.hourly_fee_vnd)
    : 'Theo thỏa thuận'

  const experienceText =
    profile?.years_experience !== undefined &&
    profile?.years_experience !== null
      ? `${profile.years_experience} năm kinh nghiệm`
      : 'Chưa cập nhật'

  const hasRating =
    profile?.avg_rating !== null && profile?.avg_rating !== undefined

  const ratingText = hasRating
    ? `${Number(profile.avg_rating).toFixed(1).replace('.', ',')} / 5,0`
    : 'Chưa có đánh giá (điểm trung tính 0,50)'

  const teachingModeText = profile
    ? formatTeachingMode(profile.teaching_mode)
    : 'Chưa cập nhật'

  const availabilityList = profile?.availability || []
  const isRealData = profile?.data_source === 'public_collected'
  const isRankOne = item.rank === 1

  return (
    <motion.article
      layout="position"
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.96 }}
      transition={{ type: 'spring', stiffness: 350, damping: 28 }}
      whileHover={{ y: -2, transition: { duration: 0.15 } }}
      className={`tutor-card ${isRankOne ? 'rank-1-hero' : ''}`}
      aria-label={`Hạng ${item.rank} - ${item.tutor_id}`}
    >
      <div className="tutor-card-header">
        <div className="tutor-rank-group">
          <div className={`rank-mark rank-${item.rank <= 3 ? item.rank : 'other'}`}>
            <span className="rank-num">#{item.rank}</span>
          </div>

          <TutorAvatar tutorId={item.tutor_id} fullName={item.full_name} size={46} />

          <div className="tutor-identity">
            <div className="tutor-title-line">
              <h3 className="tutor-name">
                {item.full_name || `Gia sư ${item.tutor_id}`}
              </h3>
              <code className="tutor-id-code">{item.tutor_id}</code>
              {isRankOne && (
                <span className="hero-best-badge">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                  </svg>
                  Khuyến nghị tốt nhất
                </span>
              )}
              {profile && (
                <span
                  className={`source-tag ${isRealData ? 'source-real' : 'source-sim'}`}
                >
                  {isRealData ? 'Dữ liệu thực tế' : 'Dữ liệu đối chứng'}
                </span>
              )}
            </div>
            <p className="tutor-meta-line">
              <span className="meta-item subject-meta-item">
                <SubjectIcon subject={primarySubject} size={14} className="meta-subject-icon" />
                <span className="meta-key">Môn dạy:</span> {subjectsText}
              </span>
              <span className="meta-sep">·</span>
              <span className="meta-item">
                <span className="meta-key">Hình thức:</span> {teachingModeText}
              </span>
            </p>
          </div>
        </div>

        <div className="tutor-total-score-box">
          <span className="total-score-label">Điểm tổng hợp S(g)</span>
          <strong className="total-score-value">
            {formatScoreVi(item.total_score, 3)}
          </strong>
          <span className="total-score-percent">
            Độ khớp {(Number(item.total_score) * 100).toFixed(1).replace('.', ',')}%
          </span>
        </div>
      </div>

      <div className="tutor-attributes-grid">
        <div
          className={`attr-item ${activeCriterion === 'fee' ? 'attr-highlighted' : ''}`}
          onMouseEnter={() => setActiveCriterion('fee')}
          onMouseLeave={() => setActiveCriterion(null)}
        >
          <span className="attr-label">
            <CriteriaIcon criterion="fee" size={13} className="attr-icon" />
            Học phí
          </span>
          <strong className="attr-value">{feeText}</strong>
        </div>
        <div
          className={`attr-item ${activeCriterion === 'experience' ? 'attr-highlighted' : ''}`}
          onMouseEnter={() => setActiveCriterion('experience')}
          onMouseLeave={() => setActiveCriterion(null)}
        >
          <span className="attr-label">
            <CriteriaIcon criterion="experience" size={13} className="attr-icon" />
            Kinh nghiệm
          </span>
          <strong className="attr-value">{experienceText}</strong>
        </div>
        <div
          className={`attr-item ${activeCriterion === 'rating' ? 'attr-highlighted' : ''}`}
          onMouseEnter={() => setActiveCriterion('rating')}
          onMouseLeave={() => setActiveCriterion(null)}
        >
          <span className="attr-label">
            <CriteriaIcon criterion="rating" size={13} className="attr-icon" />
            Đánh giá
          </span>
          <strong className="attr-value attr-rating">
            {hasRating && (
              <span className="rating-star-icon" aria-hidden="true">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
                </svg>
              </span>
            )}
            {ratingText}
          </strong>
        </div>
        <div
          className={`attr-item ${activeCriterion === 'district' ? 'attr-highlighted' : ''}`}
          onMouseEnter={() => setActiveCriterion('district')}
          onMouseLeave={() => setActiveCriterion(null)}
        >
          <span className="attr-label">
            <CriteriaIcon criterion="district" size={13} className="attr-icon" />
            Khu vực dạy
          </span>
          <strong className="attr-value">{districtsText}</strong>
        </div>
      </div>

      {availabilityList.length > 0 && (
        <div
          className={`tutor-availability-row ${activeCriterion === 'availability' ? 'row-highlighted' : ''}`}
          onMouseEnter={() => setActiveCriterion('availability')}
          onMouseLeave={() => setActiveCriterion(null)}
        >
          <span className="attr-label">
            <CriteriaIcon criterion="availability" size={13} className="attr-icon" />
            Lịch rảnh:
          </span>
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
        activeCriterion={activeCriterion}
        onCriterionHover={setActiveCriterion}
      />

      <div className="tutor-explanation-box">
        <p className="explanation-reason">
          <strong className="reason-label">Lý do gợi ý:</strong> {item.reason}
        </p>

        {Array.isArray(item.notes) && item.notes.length > 0 && (
          <div className="explanation-notes">
            <span className="notes-label">Ghi chú:</span>
            {item.notes.map((note) => (
              <span key={note} className="note-pill">
                {note}
              </span>
            ))}
          </div>
        )}
      </div>
    </motion.article>
  )
}

export default TutorCard
