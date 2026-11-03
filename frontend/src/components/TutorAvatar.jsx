import { useState } from 'react'

/**
 * TutorAvatar — Avatar đại diện sinh động cho 16 hồ sơ gia sư.
 * Sử dụng hình vector DiceBear Lorelei kết hợp cơ chế Fallback SVG Monogram Gradient
 * đảm bảo 100% không bao giờ bị vỡ hình kể cả khi offline.
 */

// Bảng màu gradient sang trọng cho từng gia sư
const AVATAR_GRADIENTS = [
  'linear-gradient(135deg, #10b981 0%, #047857 100%)', // Emerald
  'linear-gradient(135deg, #0ea5e9 0%, #0369a1 100%)', // Sky
  'linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%)', // Violet
  'linear-gradient(135deg, #f59e0b 0%, #b45309 100%)', // Amber
  'linear-gradient(135deg, #ec4899 0%, #be185d 100%)', // Pink
  'linear-gradient(135deg, #06b6d4 0%, #0e7490 100%)', // Cyan
  'linear-gradient(135deg, #6366f1 0%, #4338ca 100%)', // Indigo
  'linear-gradient(135deg, #14b8a6 0%, #0f766e 100%)', // Teal
]

function getAvatarColor(tutorId = '') {
  let hash = 0
  for (let i = 0; i < tutorId.length; i++) {
    hash = (hash << 5) - hash + tutorId.charCodeAt(i)
    hash |= 0
  }
  const idx = Math.abs(hash) % AVATAR_GRADIENTS.length
  return AVATAR_GRADIENTS[idx]
}

export default function TutorAvatar({ tutorId = '', fullName = '', size = 48, className = '' }) {
  const [imgError, setImgError] = useState(false)

  // Seed cho DiceBear từ mã gia sư
  const dicebearUrl = `https://api.dicebear.com/9.x/lorelei/svg?seed=${encodeURIComponent(
    tutorId || 'tutor'
  )}&backgroundColor=b6e3f4,c0aede,d1d4f9,ffd5dc,ffdfbf`

  // Chữ viết tắt monogram fallback (ví dụ "T06" hoặc "G01")
  const shortCode = tutorId.replace(/^GS-?/, '') || 'GS'
  const gradient = getAvatarColor(tutorId)

  return (
    <div
      className={`tutor-avatar-wrap ${className}`}
      style={{
        width: size,
        height: size,
        borderRadius: '10px',
        overflow: 'hidden',
        flexShrink: 0,
        position: 'relative',
        boxShadow: '0 2px 6px -1px rgba(0,0,0,0.2)',
      }}
      title={`${fullName || `Gia sư ${tutorId}`}`}
    >
      {!imgError ? (
        <img
          src={dicebearUrl}
          alt={`Avatar ${fullName || tutorId}`}
          width={size}
          height={size}
          loading="lazy"
          onError={() => setImgError(true)}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            display: 'block',
          }}
        />
      ) : (
        <div
          className="tutor-avatar-monogram"
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
        >
          {shortCode}
        </div>
      )}
    </div>
  )
}
