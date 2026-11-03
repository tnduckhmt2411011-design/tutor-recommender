/**
 * SubjectIcon — Component hiển thị biểu tượng vector SVG chuẩn Lucide cho các môn học.
 * Sắc nét, tương thích hoàn hảo với cả Dark & Light mode.
 */

export default function SubjectIcon({ subject = '', size = 16, className = '', color = 'currentColor' }) {
  const norm = String(subject).trim().toLowerCase()

  if (norm.includes('toán')) {
    // Lucide: Calculator / Compass
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
        className={`subject-icon icon-math ${className}`}
        aria-hidden="true"
      >
        <rect width="16" height="20" x="4" y="2" rx="2" />
        <line x1="8" x2="16" y1="6" y2="6" />
        <line x1="16" x2="16" y1="14" y2="18" />
        <path d="M16 10h.01" />
        <path d="M12 10h.01" />
        <path d="M8 10h.01" />
        <path d="M12 14h.01" />
        <path d="M8 14h.01" />
        <path d="M12 18h.01" />
        <path d="M8 18h.01" />
      </svg>
    )
  }

  if (norm.includes('lý') || norm.includes('vật lý')) {
    // Lucide: Atom
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
        className={`subject-icon icon-physics ${className}`}
        aria-hidden="true"
      >
        <circle cx="12" cy="12" r="1" />
        <path d="M20.2 20.2c2.04-2.03.02-7.36-4.5-11.9-4.54-4.52-9.87-6.54-11.9-4.5-2.04 2.03-.02 7.36 4.5 11.9 4.54 4.52 9.87 6.54 11.9 4.5Z" />
        <path d="M15.7 15.7c4.52-4.54 6.54-9.87 4.5-11.9-2.03-2.04-7.36-.02-11.9 4.5-4.52 4.54-6.54 9.87-4.5 11.9 2.03 2.04 7.36.02 11.9-4.5Z" />
      </svg>
    )
  }

  if (norm.includes('hóa')) {
    // Lucide: FlaskConical
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
        className={`subject-icon icon-chemistry ${className}`}
        aria-hidden="true"
      >
        <path d="M10 2v7.527a2 2 0 0 1-.211.896L4.72 20.55a1 1 0 0 0 .9 1.45h12.76a1 1 0 0 0 .9-1.45l-5.069-10.127A2 2 0 0 1 14 9.527V2" />
        <path d="M8.5 2h7" />
        <path d="M7 16h10" />
      </svg>
    )
  }

  if (norm.includes('anh') || norm.includes('tiếng anh') || norm.includes('nhật') || norm.includes('trung')) {
    // Lucide: Languages / Globe
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
        className={`subject-icon icon-language ${className}`}
        aria-hidden="true"
      >
        <path d="m5 8 6 6" />
        <path d="m4 14 6-6 2-3" />
        <path d="M2 5h12" />
        <path d="M7 2h1" />
        <path d="m22 22-5-10-5 10" />
        <path d="M14 18h6" />
      </svg>
    )
  }

  if (norm.includes('tin') || norm.includes('lập trình')) {
    // Lucide: Code
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
        className={`subject-icon icon-code ${className}`}
        aria-hidden="true"
      >
        <polyline points="16 18 22 12 16 6" />
        <polyline points="8 6 2 12 8 18" />
      </svg>
    )
  }

  if (norm.includes('sinh')) {
    // Lucide: Dna
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
        className={`subject-icon icon-bio ${className}`}
        aria-hidden="true"
      >
        <path d="m8 16 1.5-1.5" />
        <path d="M14.5 9.5 16 8" />
        <path d="m6 10 12 4" />
        <path d="m10 6 4 12" />
        <path d="m6 14 1.5-1.5" />
        <path d="M16.5 11.5 18 10" />
        <path d="M2 15c6.667-6 13.333 0 20-6" />
        <path d="M20 9c-6.667 6-13.333 0-20 6" />
      </svg>
    )
  }

  // Mặc định hoặc Văn học: BookOpen
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
      className={`subject-icon icon-book ${className}`}
      aria-hidden="true"
    >
      <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z" />
      <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z" />
    </svg>
  )
}
