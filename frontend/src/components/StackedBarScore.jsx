import { useState } from 'react'
import { motion } from 'motion/react'
import {
  CRITERIA_META,
  PRIORITY_LABEL_MAP,
  PRIORITY_WEIGHT_MAP,
  formatScoreVi,
} from '../data/tutorsCatalog'

function StackedBarScore({
  criteriaScores = {},
  contributions = {},
  totalScore = 0,
  priorities = {},
  activeCriterion = null,
  onCriterionHover = null,
}) {
  const [internalActiveKey, setInternalActiveKey] = useState(null)
  const activeKey = activeCriterion ?? internalActiveKey

  const handleCriterionEnter = (key) => {
    setInternalActiveKey(key)
    if (onCriterionHover) {
      onCriterionHover(key)
    }
  }

  const handleCriterionLeave = () => {
    setInternalActiveKey(null)
    if (onCriterionHover) {
      onCriterionHover(null)
    }
  }

  const segments = CRITERIA_META.map((meta) => {
    const rawContribution = contributions?.[meta.key]
    const rawScore = criteriaScores?.[meta.key]
    const priorityLevel = priorities?.[meta.key] || 'medium'
    const weight = PRIORITY_WEIGHT_MAP[priorityLevel] ?? 2
    const isApplied =
      rawContribution !== null &&
      rawContribution !== undefined &&
      !Number.isNaN(Number(rawContribution))

    const contributionValue = isApplied ? Number(rawContribution) : 0
    const scoreValue =
      rawScore !== null && rawScore !== undefined ? Number(rawScore) : null
    const widthPercent = Math.max(0, Math.min(100, contributionValue * 100))
    const shareInTotalPercent =
      isApplied && Number(totalScore) > 0
        ? (contributionValue / Number(totalScore)) * 100
        : 0

    return {
      ...meta,
      isApplied,
      contributionValue,
      scoreValue,
      priorityLevel,
      weight,
      widthPercent,
      shareInTotalPercent,
    }
  })

  const appliedSegments = segments.filter((seg) => seg.isApplied)
  const excludedSegments = segments.filter((seg) => !seg.isApplied)
  const activeSegment =
    appliedSegments.find((seg) => seg.key === activeKey) || null

  return (
    <div className="stacked-bar-container">
      <div className="stacked-bar-header">
        <span className="stacked-bar-title">
          Phân rã mức đóng góp tiêu chí (<var>C_i = w_i · s_i / ∑w_i</var>)
        </span>
        <span className="stacked-bar-total">
          Tổng điểm <strong>S = {formatScoreVi(totalScore, 3)}</strong> (
          {(Number(totalScore) * 100).toFixed(1).replace('.', ',')}%)
        </span>
      </div>

      <div
        className="stacked-bar-track"
        role="img"
        aria-label={`Biểu đồ thanh xếp chồng điểm tổng hợp ${formatScoreVi(totalScore, 3)} trên thang 1,000`}
      >
        {appliedSegments.map((seg) => {
          if (seg.widthPercent <= 0) {
            return null
          }
          const tooltipText = `${seg.label}: s_i = ${formatScoreVi(seg.scoreValue, 3)} | ${PRIORITY_LABEL_MAP[seg.priorityLevel] || `w=${seg.weight}`} | Đóng góp C_i = ${formatScoreVi(seg.contributionValue, 3)} (${seg.shareInTotalPercent.toFixed(1).replace('.', ',')}% tổng điểm)`
          const isHovered = activeKey === seg.key

          return (
            <motion.button
              key={seg.key}
              type="button"
              className={`stacked-bar-segment ${isHovered ? 'is-active' : ''}`}
              initial={{ width: 0 }}
              animate={{ width: `${seg.widthPercent.toFixed(3)}%` }}
              transition={{ duration: 0.5, ease: 'easeOut' }}
              style={{
                backgroundColor: seg.color,
              }}
              title={tooltipText}
              aria-label={tooltipText}
              onMouseEnter={() => handleCriterionEnter(seg.key)}
              onMouseLeave={handleCriterionLeave}
              onFocus={() => handleCriterionEnter(seg.key)}
              onBlur={handleCriterionLeave}
            >
              {seg.widthPercent >= 10 && (
                <span className="segment-inline-label">
                  {formatScoreVi(seg.contributionValue, 2)}
                </span>
              )}
            </motion.button>
          )
        })}
      </div>

      {activeSegment ? (
        <div
          className="stacked-bar-tooltip"
          role="status"
          aria-live="polite"
        >
          <div className="tooltip-head">
            <span
              className="legend-dot"
              style={{ backgroundColor: activeSegment.color }}
            />
            <strong>{activeSegment.label}</strong>
            <span className="tooltip-badge">
              {PRIORITY_LABEL_MAP[activeSegment.priorityLevel]}
            </span>
          </div>
          <div className="tooltip-metrics">
            <span>
              Điểm chuẩn hóa <var>s_i</var>:{' '}
              <strong>{formatScoreVi(activeSegment.scoreValue, 3)}</strong>
            </span>
            <span>
              Mức ưu tiên <var>w_i</var>:{' '}
              <strong>{activeSegment.weight}</strong>
            </span>
            <span>
              Đóng góp <var>C_i</var>:{' '}
              <strong>{formatScoreVi(activeSegment.contributionValue, 3)}</strong>
            </span>
            <span>
              Tỷ trọng: <strong>{activeSegment.shareInTotalPercent.toFixed(1).replace('.', ',')}%</strong>
            </span>
          </div>
        </div>
      ) : (
        <div className="stacked-bar-hint">
          Di chuột hoặc nhấn phím Tab vào từng phân đoạn màu để xem chi tiết điểm thành phần <var>s_i</var>, trọng số <var>w_i</var> và mức đóng góp <var>C_i</var>.
        </div>
      )}

      <div className="stacked-bar-legend">
        {appliedSegments.map((seg) => (
          <button
            key={seg.key}
            type="button"
            className={`legend-pill ${activeKey === seg.key ? 'is-active' : ''}`}
            onMouseEnter={() => handleCriterionEnter(seg.key)}
            onMouseLeave={handleCriterionLeave}
            onFocus={() => handleCriterionEnter(seg.key)}
            onBlur={handleCriterionLeave}
          >
            <span
              className="legend-dot"
              style={{ backgroundColor: seg.color }}
            />
            <span className="legend-label">{seg.shortLabel}:</span>
            <strong className="legend-val">
              C = {formatScoreVi(seg.contributionValue, 3)}
            </strong>
            <span className="legend-sub">
              (s={formatScoreVi(seg.scoreValue, 2)}, w={seg.weight})
            </span>
          </button>
        ))}

        {excludedSegments.map((seg) => (
          <span key={seg.key} className="legend-pill is-excluded">
            <span className="legend-dot is-empty" />
            <span className="legend-label">{seg.shortLabel}:</span>
            <span className="legend-sub">Không áp dụng</span>
          </span>
        ))}
      </div>
    </div>
  )
}

export default StackedBarScore
