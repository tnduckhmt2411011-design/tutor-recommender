/**
 * Module dịch vụ gọi API khuyến nghị gia sư từ Backend FastAPI.
 *
 * Trách nhiệm:
 * - Cấu hình base URL từ biến môi trường Vite (VITE_API_URL)
 * - Chuẩn hóa dữ liệu biểu mẫu theo Hợp đồng API (docs/design/api-contract.md)
 * - Gửi POST request tới /api/recommend và xử lý lỗi mạng / HTTP an toàn
 */

export const API_BASE_URL = (
  import.meta.env.VITE_API_URL ||
  import.meta.env.VITE_API_BASE_URL ||
  'http://localhost:8000'
).replace(/\/+$/, '')

export const SUBJECT_OPTIONS = [
  'Toán',
  'Lý',
  'Hóa',
  'Sinh',
  'Văn',
  'Anh Văn',
  'Anh Văn GT',
  'Tin học',
  'Tiếng Nhật',
  'Tiếng Trung',
]

export const LEARNING_MODE_OPTIONS = [
  { value: 'in_person', label: 'Trực tiếp (In-person)' },
  { value: 'online', label: 'Trực tuyến (Online)' },
  { value: 'any', label: 'Không yêu cầu (Cả hai)' },
]

export const DISTRICT_OPTIONS = [
  'Quận 1',
  'Quận 2',
  'Quận 3',
  'Quận 7',
  'Quận 8',
  'Quận 9',
  'Quận 10',
  'Quận 11',
  'Bình Thạnh',
  'Gò Vấp',
  'Phú Nhuận',
  'Tân Bình',
  'Tân Phú',
  'Thủ Đức',
  'Bình Chánh',
  'Nhà Bè',
]

export const DAYS_OF_WEEK = [
  { code: 'T2', label: 'Thứ 2' },
  { code: 'T3', label: 'Thứ 3' },
  { code: 'T4', label: 'Thứ 4' },
  { code: 'T5', label: 'Thứ 5' },
  { code: 'T6', label: 'Thứ 6' },
  { code: 'T7', label: 'Thứ 7' },
  { code: 'CN', label: 'Chủ nhật' },
]

export const SESSIONS_OF_DAY = [
  { code: 'sáng', label: 'Sáng' },
  { code: 'chiều', label: 'Chiều' },
  { code: 'tối', label: 'Tối' },
]

export const PRIORITY_OPTIONS = [
  { value: 'none', label: 'Không quan tâm', shortLabel: 'Bỏ qua', weight: 0 },
  { value: 'low', label: 'Thấp', shortLabel: 'Thấp', weight: 1 },
  { value: 'medium', label: 'Trung bình', shortLabel: 'Trung bình', weight: 2 },
  { value: 'high', label: 'Cao', shortLabel: 'Cao', weight: 3 },
]

export const CRITERIA_LIST = [
  {
    key: 'fee',
    label: 'Học phí',
    description: 'Mức độ phù hợp giữa học phí của gia sư và ngân sách tối đa/giờ',
  },
  {
    key: 'district',
    label: 'Khu vực',
    description: 'Mức độ khớp khu vực dạy trực tiếp với quận/huyện mong muốn',
  },
  {
    key: 'experience',
    label: 'Kinh nghiệm',
    description: 'Số năm kinh nghiệm giảng dạy của gia sư (chuẩn hóa trên mốc 8 năm)',
  },
  {
    key: 'rating',
    label: 'Đánh giá',
    description: 'Điểm đánh giá trung bình của gia sư (thang 5, trung tính 0,5 nếu chưa có)',
  },
  {
    key: 'availability',
    label: 'Lịch rảnh',
    description: 'Tỷ lệ khung giờ mong muốn của người học được gia sư đáp ứng',
  },
]

export const DEFAULT_PRIORITIES = {
  fee: 'medium',
  district: 'medium',
  experience: 'medium',
  rating: 'medium',
  availability: 'medium',
}

/**
 * Chuẩn hóa dữ liệu từ trạng thái biểu mẫu sang payload hợp lệ theo API Contract.
 */
export function buildRecommendationPayload(formValues) {
  const isOnline = formValues.learningMode === 'online'
  const trimmedDistrict = (formValues.preferredDistrict || '').trim()
  const preferredDistrict =
    !isOnline && trimmedDistrict.length > 0 ? trimmedDistrict : null

  let maxBudgetVnd = null
  const rawBudget = String(formValues.maxBudgetVnd ?? '').trim()
  if (rawBudget !== '') {
    maxBudgetVnd = Number.parseInt(rawBudget, 10)
  }

  const timeSlots =
    Array.isArray(formValues.timeSlots) && formValues.timeSlots.length > 0
      ? formValues.timeSlots
      : null

  const topK = Number.parseInt(String(formValues.topK ?? 3), 10)

  return {
    subject: String(formValues.subject || '').trim(),
    learning_mode: formValues.learningMode,
    preferred_district: preferredDistrict,
    max_budget_vnd: maxBudgetVnd,
    time_slots: timeSlots,
    priorities: {
      ...DEFAULT_PRIORITIES,
      ...(formValues.priorities || {}),
    },
    top_k: Number.isNaN(topK) ? 3 : topK,
  }
}

/**
 * Gửi yêu cầu POST /api/recommend tới Backend FastAPI.
 */
export async function fetchRecommendations(payload) {
  let response
  try {
    response = await fetch(`${API_BASE_URL}/api/recommend`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    })
  } catch {
    throw new Error(
      'Không thể kết nối tới máy chủ gợi ý gia sư. Vui lòng kiểm tra dịch vụ Backend đang chạy.'
    )
  }

  let data = null
  try {
    data = await response.json()
  } catch {
    throw new Error(`Phản hồi từ máy chủ không hợp lệ (HTTP ${response.status}).`)
  }

  if (!response.ok) {
    const detail =
      typeof data?.detail === 'string'
        ? data.detail
        : 'Dữ liệu đầu vào không hợp lệ (HTTP 422). Vui lòng kiểm tra lại các trường đã nhập.'
    throw new Error(detail)
  }

  return data
}
