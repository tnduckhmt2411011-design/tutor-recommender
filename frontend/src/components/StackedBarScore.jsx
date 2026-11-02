import { useState } from 'react'
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
}) {
  const [activeKey, setActiveKey] = useState(null)

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
            <button
              key={seg.key}
              type="button"
              className={`stacked-bar-segment ${isHovered ? 'is-active' : ''}`}
              style={{
                width: `${seg.widthPercent.toFixed(3)}%`,
                backgroundColor: seg.color,
              }}
              title={tooltipText}
              aria-label={tooltipText}
              onMouseEnter={() => setActiveKey(seg.key)}
              onMouseLeave={() => setActiveKey(null)}
              onFocus={() => setActiveKey(seg.key)}
              onBlur={() => setActiveKey(null)}
            >
              {seg.widthPercent >= 10 && (
                <span className="segment-inline-label">
                  {formatScoreVi(seg.contributionValue, 2)}
                </span>
              )}
            </button>
          )
        })}
      </div>

      {activeSegment ? (
        <div
          className="stacked-bar-tooltip"
          role="status"
          aria-live="polite"
          style={{ borderLeftColor: activeSegment.color }}
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
              Trọng số <var>w_i</var>: <strong>{activeSegment.weight}</strong>
            </span>
            <span>
              Đóng góp <var>C_i</var>:{' '}
              <strong>
                +{formatScoreVi(activeSegment.contributionValue, 3)}
              </strong>
            </span>
            <span>
              Tỷ trọng trong <var>S</var>:{' '}
              <strong>
                {activeSegment.shareInTotalPercent.toFixed(1).replace('.', ',')}%
              </strong>
            </span>
          </div>
        </div>
      ) : (
        <p className="stacked-bar-hint">
          Di chuột hoặc nhấn phím Tab vào từng phân đoạn màu để xem chi tiết
          điểm thành phần <var>s_i</var>, trọng số <var>w_i</var> và mức đóng
          góp <var>C_i</var>.
        </p>
      )}

      <div className="stacked-bar-legend">
        {appliedSegments.map((seg) => (
          <button
            key={seg.key}
            type="button"
            className={`legend-chip ${activeKey === seg.key ? 'active' : ''}`}
            onMouseEnter={() => setActiveKey(seg.key)}
            onMouseLeave={() => setActiveKey(null)}
            onFocus={() => setActiveKey(seg.key)}
            onBlur={() => setActiveKey(null)}
          >
            <span
              className="legend-dot"
              style={{ backgroundColor: seg.color }}
            />
            <span className="legend-name">{seg.label}:</span>
            <span className="legend-val">
              C = {formatScoreVi(seg.contributionValue, 3)}
            </span>
            <small className="legend-sub">
              (s={formatScoreVi(seg.scoreValue, 2)}, w={seg.weight})
            </small>
          </button>
        ))}

        {excludedSegments.map((seg) => (
          <span key={seg.key} className="legend-chip legend-excluded">
            <span className="legend-dot excluded-dot" />
            <span className="legend-name">{seg.label}:</span>
            <small>Không áp dụng</small>
          </span>
        ))}
      </div>
    </div>
  )
}

export default StackedBarScore
