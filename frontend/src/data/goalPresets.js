/**
 * Bộ mức ưu tiên điền sẵn theo mục tiêu học tập.
 *
 * Nguồn: báo cáo giữa kỳ mục 4.2; ô không nêu = Trung bình; giá trị do nhóm đặt,
 * chưa kiểm chứng với người dùng.
 *
 * Chỉ dùng 3 giá trị báo cáo giữa kỳ đã nêu: Kinh nghiệm Cao và Đánh giá Cao cho mục
 * tiêu điểm cao / luyện thi chuyên; Học phí Cao cho mục tiêu đủ điểm đậu / lấy lại căn
 * bản. Mọi ô còn lại để "medium" vì báo cáo không nêu mức cụ thể.
 *
 * Đây chỉ là giá trị khởi tạo ở tầng giao diện: người học vẫn chỉnh được từng tiêu chí
 * và payload gửi API không đổi (vẫn đúng 5 khóa trong `priorities`).
 */
import { DEFAULT_PRIORITIES } from '../services/api'

export const GOAL_PRESETS = [
  {
    key: 'none',
    label: 'Không nêu mục tiêu',
    description: 'Giữ bộ mặc định: cả 5 tiêu chí ở mức Trung bình.',
    priorities: { ...DEFAULT_PRIORITIES },
  },
  {
    key: 'high_score',
    label: 'Điểm cao / luyện thi chuyên – học sinh giỏi',
    description: 'Kinh nghiệm và Đánh giá ở mức Cao; ba tiêu chí còn lại Trung bình.',
    priorities: {
      fee: 'medium',
      district: 'medium',
      experience: 'high',
      rating: 'high',
      availability: 'medium',
    },
  },
  {
    key: 'pass_basic',
    label: 'Đủ điểm đậu / lấy lại kiến thức căn bản',
    description: 'Học phí ở mức Cao; bốn tiêu chí còn lại Trung bình.',
    priorities: {
      fee: 'high',
      district: 'medium',
      experience: 'medium',
      rating: 'medium',
      availability: 'medium',
    },
  },
]
