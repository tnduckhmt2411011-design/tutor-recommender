/**
 * CriteriaIcon — Component hiển thị biểu tượng vector SVG Lucide cho 5 tiêu chí chấm điểm:
 * fee (Học phí), district (Khu vực), experience (Kinh nghiệm), rating (Đánh giá), availability (Lịch rảnh).
 */

export default function CriteriaIcon({ criterion = '', size = 15, className = '', color = 'currentColor' }) {
  const norm = String(criterion).trim().toLowerCase()

  if (norm === 'fee') {
    // Coins
    return (
      <svg
        width={size}
        height={size}
        viewBox="0 0 24 24"
        fill="none"
        stroke={color}
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className={`criteria-icon icon-fee ${className}`}
        aria-hidden="true"
      >
        <circle cx="8" cy="8" r="6" />
        <path d="M18.09 10.37A6 6 0 1 1 10.34 18" />
        <path d="M7 6h1v4" />
        <path d="m16.71 13.88.7.71-2.82 2.82" />
      </svg>
    )
  }

  if (norm === 'district') {
    // MapPin
    return (
      <svg
        width={size}
        height={size}
        viewBox="0 0 24 24"
        fill="none"
        stroke={color}
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className={`criteria-icon icon-district ${className}`}
        aria-hidden="true"
      >
        <path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z" />
        <circle cx="12" cy="10" r="3" />
      </svg>
    )
  }

  if (norm === 'experience') {
    // Briefcase / Award
    return (
      <svg
        width={size}
        height={size}
        viewBox="0 0 24 24"
        fill="none"
        stroke={color}
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className={`criteria-icon icon-experience ${className}`}
        aria-hidden="true"
      >
        <rect width="20" height="14" x="2" y="7" rx="2" ry="2" />
        <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16" />
      </svg>
    )
  }

  if (norm === 'rating') {
    // Star
    return (
      <svg
        width={size}
        height={size}
        viewBox="0 0 24 24"
        fill="currentColor"
        stroke={color}
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
        className={`criteria-icon icon-rating ${className}`}
        aria-hidden="true"
      >
        <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
      </svg>
    )
  }

  if (norm === 'availability') {
    // Calendar / Clock
    return (
      <svg
        width={size}
        height={size}
        viewBox="0 0 24 24"
        fill="none"
        stroke={color}
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className={`criteria-icon icon-availability ${className}`}
        aria-hidden="true"
      >
        <circle cx="12" cy="12" r="10" />
        <polyline points="12 6 12 12 16 14" />
      </svg>
    )
  }

  return null
}
