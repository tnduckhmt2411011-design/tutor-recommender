import { motion } from 'motion/react'

/**
 * SkeletonLoader — Khung xương phát sáng động (Shimmer Pulse)
 * hiển thị khi đang tính toán & xếp hạng gia sư qua API.
 */

export default function SkeletonLoader({ count = 3 }) {
  return (
    <div className="skeleton-cards-list" aria-label="Đang nạp kết quả gợi ý...">
      {Array.from({ length: count }).map((_, i) => (
        <motion.div
          key={i}
          className="skeleton-card"
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: i * 0.1 }}
        >
          <div className="skeleton-header">
            <div className="skeleton-avatar pulse-anim" />
            <div className="skeleton-meta">
              <div className="skeleton-line-title pulse-anim" />
              <div className="skeleton-line-sub pulse-anim" />
            </div>
            <div className="skeleton-score-box pulse-anim" />
          </div>

          <div className="skeleton-grid">
            <div className="skeleton-grid-item pulse-anim" />
            <div className="skeleton-grid-item pulse-anim" />
            <div className="skeleton-grid-item pulse-anim" />
            <div className="skeleton-grid-item pulse-anim" />
          </div>

          <div className="skeleton-bar pulse-anim" />
          <div className="skeleton-reason pulse-anim" />
        </motion.div>
      ))}
    </div>
  )
}
