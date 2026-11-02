"""Điểm khởi chạy ứng dụng FastAPI, đăng ký middleware và gắn kết các router API.

Trách nhiệm:
- Khởi tạo instance FastAPI
- Cấu hình CORS và các middleware phục vụ kết nối Frontend ReactJS
- Đăng ký API router gợi ý gia sư

Mục tương ứng trong đề cương:
- Mục 3.7. Kiến trúc hệ thống và luồng xử lý
- Mục 4.4. Xây dựng API gợi ý
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.recommend import router as recommend_router

app = FastAPI(
    title="Hệ thống khuyến nghị gia sư đa tiêu chí (Tutor Recommender API)",
    description=(
        "API RESTful hỗ trợ tìm kiếm và xếp hạng gia sư dựa trên mức độ phù hợp đa tiêu chí "
        "(Weighted Scoring) kèm giải thích mức đóng góp từng tiêu chí."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recommend_router)


@app.get("/health", tags=["Health"], summary="Kiểm tra trạng thái hoạt động của dịch vụ")
def health_check() -> dict[str, str]:
    """Trả về trạng thái sẵn sàng của dịch vụ backend."""
    return {"status": "ok"}
