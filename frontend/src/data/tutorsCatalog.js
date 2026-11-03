/**
 * Danh mục hồ sơ gia sư chuẩn hóa (đồng bộ từ data/processed/tutors.json - Phụ lục A)
 * và các hàm định dạng hiển thị cho thẻ gia sư (TutorCard) & thanh xếp chồng (StackedBarScore).
 *
 * Lưu ý kiến trúc:
 * - Hợp đồng API (docs/design/api-contract.md) quy định POST /api/recommend trả về
 *   tutor_id, full_name, rank, total_score, criteria_scores, contributions, reason, notes.
 * - Tệp này cung cấp thông tin thuộc tính hồ sơ tĩnh theo tutor_id để hiển thị đầy đủ
 *   thẻ gia sư theo Hình 3.5 đề cương mà không làm thay đổi Hợp đồng API.
 */

export const TUTORS_LIST = [
  {
    tutor_id: 'GS-T06',
    full_name: 'Gia sư GS-T06',
    subjects: ['Toán', 'Lý', 'Hóa'],
    districts: ['Bình Thạnh', 'Gò Vấp', 'Phú Nhuận', 'Tân Bình', 'Tân Phú'],
    hourly_fee_vnd: 400000,
    years_experience: 20,
    teaching_mode: 'in_person',
    availability: ['T2-tối', 'T4-tối', 'T6-tối'],
    avg_rating: null,
    data_source: 'public_collected',
  },
  {
    tutor_id: 'GS-T07',
    full_name: 'Gia sư GS-T07',
    subjects: ['Anh Văn', 'Anh Văn GT'],
    districts: ['Bình Chánh', 'Nhà Bè', 'Quận 7', 'Quận 8'],
    hourly_fee_vnd: 190000,
    years_experience: 6,
    teaching_mode: 'in_person',
    availability: ['T3-tối', 'T5-tối', 'T7-sáng'],
    avg_rating: null,
    data_source: 'public_collected',
  },
  {
    tutor_id: 'GS006',
    full_name: 'Gia sư GS006',
    subjects: ['Lý', 'Hóa'],
    districts: [],
    hourly_fee_vnd: 190000,
    years_experience: 5,
    teaching_mode: 'online',
    availability: ['T2-tối', 'T3-tối', 'T4-tối', 'T5-tối'],
    avg_rating: 4.6,
    data_source: 'simulated',
  },
  {
    tutor_id: 'GS020',
    full_name: 'Gia sư GS020',
    subjects: ['Lý', 'Hóa'],
    districts: [],
    hourly_fee_vnd: 240000,
    years_experience: 5,
    teaching_mode: 'online',
    availability: ['T2-tối', 'T3-tối', 'T4-tối', 'T5-tối'],
    avg_rating: 4.6,
    data_source: 'simulated',
  },
  {
    tutor_id: 'GS-G01',
    full_name: 'Gia sư GS-G01',
    subjects: ['Toán'],
    districts: ['Bình Thạnh'],
    hourly_fee_vnd: 180000,
    years_experience: 6,
    teaching_mode: 'both',
    availability: ['T2-tối', 'T4-tối', 'T7-sáng'],
    avg_rating: 5.0,
    data_source: 'simulated',
  },
  {
    tutor_id: 'GS-G02',
    full_name: 'Gia sư GS-G02',
    subjects: ['Toán'],
    districts: ['Bình Thạnh'],
    hourly_fee_vnd: 300000,
    years_experience: 3,
    teaching_mode: 'both',
    availability: ['T2-tối', 'T4-tối', 'T7-sáng'],
    avg_rating: 3.0,
    data_source: 'simulated',
  },
  {
    tutor_id: 'GS-G03',
    full_name: 'Gia sư GS-G03',
    subjects: ['Anh Văn'],
    districts: ['Gò Vấp'],
    hourly_fee_vnd: 200000,
    years_experience: 4,
    teaching_mode: 'online',
    availability: ['T3-sáng', 'T5-sáng'],
    avg_rating: 4.5,
    data_source: 'simulated',
  },
  {
    tutor_id: 'GS-G04',
    full_name: 'Gia sư GS-G04',
    subjects: ['Văn'],
    districts: ['Quận 1', 'Quận 3'],
    hourly_fee_vnd: 170000,
    years_experience: 7,
    teaching_mode: 'in_person',
    availability: ['T2-chiều', 'T5-chiều'],
    avg_rating: 4.3,
    data_source: 'simulated',
  },
  {
    tutor_id: 'GS-G05',
    full_name: 'Gia sư GS-G05',
    subjects: ['Sinh'],
    districts: ['Thủ Đức', 'Quận 9'],
    hourly_fee_vnd: 190000,
    years_experience: 4,
    teaching_mode: 'both',
    availability: ['T3-tối', 'T6-tối'],
    avg_rating: 4.0,
    data_source: 'simulated',
  },
  {
    tutor_id: 'GS-G06',
    full_name: 'Gia sư GS-G06',
    subjects: ['Hóa'],
    districts: ['Quận 10', 'Quận 11'],
    hourly_fee_vnd: 210000,
    years_experience: 8,
    teaching_mode: 'in_person',
    availability: ['T4-sáng', 'T7-sáng'],
    avg_rating: 4.7,
    data_source: 'simulated',
  },
  {
    tutor_id: 'GS-G07',
    full_name: 'Gia sư GS-G07',
    subjects: ['Tin học'],
    districts: ['Bình Thạnh', 'Thủ Đức'],
    hourly_fee_vnd: 220000,
    years_experience: 5,
    teaching_mode: 'online',
    availability: ['T2-tối', 'T4-tối', 'T6-tối'],
    avg_rating: 4.4,
    data_source: 'simulated',
  },
  {
    tutor_id: 'GS-G08',
    full_name: 'Gia sư GS-G08',
    subjects: ['Tiếng Nhật'],
    districts: ['Phú Nhuận', 'Tân Bình'],
    hourly_fee_vnd: 260000,
    years_experience: 6,
    teaching_mode: 'both',
    availability: ['T3-chiều', 'T5-chiều'],
    avg_rating: 4.8,
    data_source: 'simulated',
  },
  {
    tutor_id: 'GS-G09',
    full_name: 'Gia sư GS-G09',
    subjects: ['Toán'],
    districts: ['Quận 7'],
    hourly_fee_vnd: 350000,
    years_experience: 2,
    teaching_mode: 'in_person',
    availability: ['T2-tối', 'T4-tối'],
    avg_rating: 3.5,
    data_source: 'simulated',
  },
  {
    tutor_id: 'GS-G10',
    full_name: 'Gia sư GS-G10',
    subjects: ['Toán'],
    districts: ['Quận 7'],
    hourly_fee_vnd: 130000,
    years_experience: 12,
    teaching_mode: 'in_person',
    availability: ['T2-tối', 'T4-tối'],
    avg_rating: 4.9,
    data_source: 'simulated',
  },
  {
    tutor_id: 'GS-G11',
    full_name: 'Gia sư GS-G11',
    subjects: ['Anh Văn'],
    districts: ['Quận 2', 'Bình Thạnh'],
    hourly_fee_vnd: 200000,
    years_experience: 5,
    teaching_mode: 'in_person',
    availability: ['T3-sáng', 'T6-sáng'],
    avg_rating: 4.5,
    data_source: 'simulated',
  },
  {
    tutor_id: 'GS-G12',
    full_name: 'Gia sư GS-G12',
    subjects: ['Anh Văn'],
    districts: ['Quận 2', 'Thủ Đức'],
    hourly_fee_vnd: 200000,
    years_experience: 5,
    teaching_mode: 'in_person',
    availability: ['T3-sáng', 'T6-sáng'],
    avg_rating: 4.5,
    data_source: 'simulated',
  },
]

export const TUTORS_BY_ID = Object.fromEntries(
  TUTORS_LIST.map((tutor) => [tutor.tutor_id, tutor])
)

export function getTutorProfile(tutorId) {
  return TUTORS_BY_ID[tutorId] || null
}

export const CRITERIA_META = [
  {
    key: 'fee',
    label: 'Học phí',
    shortLabel: 'Học phí',
    color: '#10b981', // Emerald
    bgLight: 'rgba(16, 185, 129, 0.15)',
  },
  {
    key: 'district',
    label: 'Khu vực',
    shortLabel: 'Khu vực',
    color: '#0ea5e9', // Sky Blue
    bgLight: 'rgba(14, 165, 233, 0.15)',
  },
  {
    key: 'experience',
    label: 'Kinh nghiệm',
    shortLabel: 'Kinh nghiệm',
    color: '#8b5cf6', // Violet
    bgLight: 'rgba(139, 92, 246, 0.15)',
  },
  {
    key: 'rating',
    label: 'Đánh giá',
    shortLabel: 'Đánh giá',
    color: '#f59e0b', // Amber
    bgLight: 'rgba(245, 158, 11, 0.15)',
  },
  {
    key: 'availability',
    label: 'Lịch rảnh',
    shortLabel: 'Lịch rảnh',
    color: '#f43f5e', // Rose
    bgLight: 'rgba(244, 63, 94, 0.15)',
  },
]

export const PRIORITY_WEIGHT_MAP = {
  none: 0,
  low: 1,
  medium: 2,
  high: 3,
}

export const PRIORITY_LABEL_MAP = {
  none: 'Không quan tâm (w=0)',
  low: 'Thấp (w=1)',
  medium: 'Trung bình (w=2)',
  high: 'Cao (w=3)',
}

export function formatScoreVi(value, digits = 3) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) {
    return '-'
  }
  return Number(value).toFixed(digits).replace('.', ',')
}

export function formatCurrencyVnd(amount) {
  if (amount === null || amount === undefined || Number.isNaN(Number(amount))) {
    return 'Chưa cập nhật'
  }
  return `${Number(amount).toLocaleString('vi-VN')} VNĐ/giờ`
}

export function formatTeachingMode(mode) {
  if (mode === 'in_person') return 'Trực tiếp (In-person)'
  if (mode === 'online') return 'Trực tuyến (Online)'
  if (mode === 'both') return 'Trực tiếp & Trực tuyến'
  if (mode === 'any') return 'Không yêu cầu (Cả hai)'
  return mode || 'Chưa xác định'
}
