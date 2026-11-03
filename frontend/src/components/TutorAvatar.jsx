import Avatar from 'boring-avatars'

/**
 * TutorAvatar — Avatar nhận diện sinh động, chuẩn mực cho 16 hồ sơ gia sư.
 * Sử dụng thư viện `boring-avatars` (variant `beam`) với bảng màu Academic / Dark Studio:
 * - 100% SVG inline, zero network request, hoạt động hoàn hảo offline.
 * - Giải quyết triệt để vấn đề ảnh AI giả/uncanny hay bản quyền.
 * - Đồng bộ tuyệt đối phong cách thiết kế trên toàn bộ hệ thống.
 */

// Bảng màu 5 tông học thuật hài hòa: Emerald, Sky, Indigo, Amber, Teal
const ACADEMIC_PALETTE = ['#10b981', '#0ea5e9', '#6366f1', '#f59e0b', '#14b8a6', '#0f766e', '#8b5cf6']

export default function TutorAvatar({ tutorId = '', fullName = '', size = 48, className = '' }) {
  // Định danh hạt giống (seed) duy nhất từ tutorId và fullName
  const avatarSeed = fullName ? `${tutorId}-${fullName}` : tutorId || 'tutor-default'

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
        boxShadow: '0 2px 8px -2px rgba(0, 0, 0, 0.25)',
      }}
      title={`Gia sư: ${fullName || tutorId}`}
    >
      <Avatar
        size={size}
        name={avatarSeed}
        variant="beam"
        colors={ACADEMIC_PALETTE}
      />
    </div>
  )
}
