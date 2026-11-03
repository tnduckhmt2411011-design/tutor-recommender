# Triển khai Hệ thống Tutor Recommender lên Cloud (Vercel + Render) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Đóng gói và thiết lập sẵn sàng cấu hình triển khai hệ thống khuyến nghị gia sư đa tiêu chí lên môi trường Cloud công cộng hoàn toàn miễn phí ($0): Backend FastAPI trên Render.com và Frontend React trên Vercel.

**Architecture:** 
- **Backend (Render.com Web Service):** FastAPI chạy trực tiếp từ `backend/requirements.txt` bằng lệnh `uvicorn app.main:app --host 0.0.0.0 --port $PORT`. Cấu hình tự động bằng Blueprint `render.yaml` tại thư mục gốc, health check endpoint tại `/health`.
- **Frontend (Vercel Static SPA):** React + Vite build tĩnh ra `frontend/dist/`. Tích hợp tệp `frontend/vercel.json` để chuyển tiếp tất cả request về `index.html` (tránh lỗi 404 khi F5). Đọc URL backend thông qua biến môi trường `VITE_API_URL`.
- **Kết nối API & CORS:** Backend đã mở `allow_origins=["*"]` trong `app/main.py`, sẵn sàng tiếp nhận request an toàn từ tên miền `https://*.vercel.app`.

**Tech Stack:** FastAPI (Python 3.12), Uvicorn, React 19, Vite 8, Vercel, Render.

**Spec:** `docs/design/api-contract.md`, `docs/scrum/sprints/sprint-06/planning.md`.

---

## Global Constraints

- Không sửa đổi công thức chấm điểm toán học, 16 hồ sơ gia sư và 14 kịch bản thực nghiệm.
- Toàn bộ 190 backend test cases phải tiếp tục pass 100%.
- Không can thiệp vào main working tree `d:\Use Antigravity\Recommendation System Gia Sư\tutor-recommender` (vẫn giữ sạch trên `chore/2-ci-github-actions`). Mọi chỉnh sửa thực hiện trong worktree `$env:TEMP\wt-live-demo` trên nhánh PR #76.

---

## Tasks

- [ ] **Task 1: Cấu hình Blueprint Render cho Backend (`render.yaml`)**
  - [ ] Tạo tệp `render.yaml` tại thư mục gốc của repository định nghĩa dịch vụ `tutor-recommender-api` (runtime python, rootDir `backend`, buildCommand `pip install -r requirements.txt`, startCommand `uvicorn app.main:app --host 0.0.0.0 --port $PORT`, healthCheckPath `/health`).
  - [ ] Kiểm tra tính hợp lệ của `render.yaml` theo schema chuẩn của Render.

- [ ] **Task 2: Cấu hình định tuyến SPA Vercel cho Frontend (`frontend/vercel.json`)**
  - [ ] Tạo tệp `frontend/vercel.json` chứa cấu hình rewrites `[{ "source": "/(.*)", "destination": "/" }]`.
  - [ ] Kiểm tra và bổ sung fallback hỗ trợ cả `VITE_API_URL` và `VITE_API_BASE_URL` trong `frontend/src/services/api.js`.

- [ ] **Task 3: Soạn thảo Cẩm nang Hướng dẫn Triển khai Chi tiết (`docs/deployment/deploy-vercel-render.md`)**
  - [ ] Hướng dẫn Bước 1: Deploy Backend lên Render (tạo Web Service từ GitHub, đặt Name, Root Directory `backend`, Start Command, lấy URL backend).
  - [ ] Hướng dẫn Bước 2: Deploy Frontend lên Vercel (kết nối repo GitHub, Root Directory `frontend`, đặt biến `VITE_API_URL = <render-url>`, bấm Deploy).
  - [ ] Hướng dẫn Bước 3: Nghiệm thu toàn trình và xử lý cold-start của Render Free Tier.

- [ ] **Task 4: Kiểm thử Cục bộ & Nghiệm thu**
  - [ ] Chạy `npm run lint` (`oxlint`) và `npm run build` trong `frontend/`.
  - [ ] Chạy `pytest tests -q` trong `backend/` (190 passed).
  - [ ] Kiểm tra build preview frontend mô phỏng môi trường production.

- [ ] **Task 5: Commit & Đẩy lên GitHub**
  - [ ] Commit với message chuẩn: `ci(deploy): bổ sung cấu hình triển khai Vercel (Frontend) và Render (Backend)`
  - [ ] Đẩy commit lên `origin/docs/cap-nhat-bao-cao-tien-do-giua-ky` (PR #76).
