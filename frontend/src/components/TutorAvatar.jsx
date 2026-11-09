import { useState } from 'react'

/**
 * TutorAvatar — Hiển thị ảnh chân dung gia sư người thật chuẩn học đường (WebP),
 * hỗ trợ đầy đủ `alt="Gia sư {tutorId}"`, và tự động fallback sang Monogram Initials
 * nếu tệp ảnh thiếu hoặc lỗi mạng.
 */

// Bảng màu gradient sang trọng cho fallback initials
const FALLBACK_GRADIENTS = [
  'linear-gradient(135deg, #10b981 0%, #047857 100%)', // Emerald
  'linear-gradient(135deg, #0ea5e9 0%, #0369a1 100%)', // Sky
  'linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%)', // Violet
  'linear-gradient(135deg, #f59e0b 0%, #b45309 100%)', // Amber
  'linear-gradient(135deg, #06b6d4 0%, #0e7490 100%)', // Cyan
  'linear-gradient(135deg, #6366f1 0%, #4338ca 100%)', // Indigo
  'linear-gradient(135deg, #14b8a6 0%, #0f766e 100%)', // Teal
]

function getFallbackColor(tutorId = '') {
  let hash = 0
  for (let i = 0; i < tutorId.length; i++) {
    hash = (hash << 5) - hash + tutorId.charCodeAt(i)
    hash |= 0
  }
  const idx = Math.abs(hash) % FALLBACK_GRADIENTS.length
  return FALLBACK_GRADIENTS[idx]
}

export default function TutorAvatar({ tutorId = '', fullName = '', size = 52, className = '' }) {
  const [imgError, setImgError] = useState(false)

  const avatarSrc = `/avatars/${tutorId}.webp?v=sprint6`
  const shortCode = tutorId.replace(/^GS-?/, '') || 'GS'
  const altText = `Gia sư ${tutorId}`
  const gradient = getFallbackColor(tutorId)

  return (
    <div
      className={`tutor-avatar-wrap ${className}`}
      style={{
        width: size,
        height: size,
        borderRadius: '12px',
        overflow: 'hidden',
        flexShrink: 0,
        position: 'relative',
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'var(--surface-muted)',
        border: '1px solid var(--border-subtle)',
        boxShadow: '0 2px 8px -2px rgba(0, 0, 0, 0.28)',
      }}
      title={`${fullName || `Gia sư ${tutorId}`} (Ảnh minh họa hồ sơ)`}
    >
      {!imgError ? (
        <img
          src={avatarSrc}
          alt={altText}
          width={size}
          height={size}
          loading="lazy"
          decoding="async"
          onError={() => setImgError(true)}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            display: 'block',
            imageRendering: '-webkit-optimize-contrast',
          }}
        />
      ) : (
        <div
          className="tutor-avatar-initials"
          style={{
            width: '100%',
            height: '100%',
            background: gradient,
            color: '#ffffff',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontFamily: 'var(--mono)',
            fontWeight: 700,
            fontSize: size >= 48 ? '16px' : '13px',
            letterSpacing: '-0.02em',
            textTransform: 'uppercase',
          }}
          aria-label={altText}
        >
          {shortCode}
        </div>
      )}
    </div>
  )
}
