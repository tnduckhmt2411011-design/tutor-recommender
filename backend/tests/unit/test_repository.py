"""Kiểm thử đơn vị cho lớp truy xuất dữ liệu hồ sơ gia sư (repository.py).

Mục tương ứng trong đề cương: Mục 3.5, Mục 4.2.
"""

import json
from pathlib import Path

import pytest

from app.core import config
from app.data.repository import TutorDataError, TutorRepository
from app.schemas.tutor import TutorProfile


def _valid_record(**overrides: object) -> dict:
    """Dựng một bản ghi hợp lệ theo Bảng 3.3 để ghi vào tệp tạm."""
    record = {
        "tutor_id": "GS-TEST",
        "subjects": ["Toán"],
        "districts": ["Quận 1"],
        "hourly_fee_vnd": 200000,
        "years_experience": 3,
        "teaching_mode": "both",
        "availability": ["T2-tối"],
        "avg_rating": 4.5,
        "data_source": "simulated",
    }
    record.update(overrides)
    return record


def _write_json(path: Path, payload: object) -> Path:
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return path


def test_default_repository_loads_16_tutor_profiles() -> None:
    """Đọc tutors.json mặc định phải trả đúng 16 hồ sơ."""
    tutors = TutorRepository().get_all()

    assert len(tutors) == 16


def test_loaded_records_are_tutor_profile_instances() -> None:
    """Mỗi bản ghi nạp vào phải là TutorProfile đã xác thực."""
    tutors = TutorRepository().get_all()

    assert all(isinstance(tutor, TutorProfile) for tutor in tutors)
    assert len({tutor.tutor_id for tutor in tutors}) == 16


def test_missing_rating_is_kept_as_none() -> None:
    """avg_rating = null trong dữ liệu phải giữ nguyên None, không thay bằng 0,5."""
    tutors = {t.tutor_id: t for t in TutorRepository().get_all()}

    assert tutors["GS-T06"].avg_rating is None
    assert tutors["GS006"].avg_rating == 4.6


def test_default_path_does_not_depend_on_working_directory(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Đổi thư mục chạy vẫn đọc được dữ liệu mặc định."""
    monkeypatch.chdir(tmp_path)

    assert len(TutorRepository().get_all()) == 16


def test_reads_custom_path_as_utf8(tmp_path: Path) -> None:
    """Tệp tạm UTF-8 chứa tiếng Việt có dấu phải được đọc đúng."""
    path = _write_json(
        tmp_path / "tutors.json",
        [_valid_record(subjects=["Toán", "Anh Văn"], districts=["Bình Thạnh"])],
    )

    tutors = TutorRepository(path).get_all()

    assert tutors[0].subjects == ["Toán", "Anh Văn"]
    assert tutors[0].districts == ["Bình Thạnh"]


def test_get_all_does_not_modify_data_file(tmp_path: Path) -> None:
    """Đọc dữ liệu không được ghi lại hay thay đổi tệp nguồn."""
    path = _write_json(tmp_path / "tutors.json", [_valid_record(avg_rating=None)])
    before = path.read_bytes()

    tutors = TutorRepository(path).get_all()

    assert path.read_bytes() == before
    assert tutors[0].avg_rating is None


def test_missing_file_raises_clear_error(tmp_path: Path) -> None:
    """Tệp không tồn tại: báo lỗi cụ thể nêu đường dẫn, không để lỗi hệ thống thô."""
    missing = tmp_path / "khong_ton_tai.json"

    with pytest.raises(TutorDataError, match="Không tìm thấy tệp dữ liệu gia sư"):
        TutorRepository(missing).get_all()


def test_malformed_json_raises_clear_error(tmp_path: Path) -> None:
    """Tệp không phải JSON hợp lệ: báo lỗi định dạng cụ thể."""
    path = tmp_path / "tutors.json"
    path.write_text("[{ không phải json", encoding="utf-8")

    with pytest.raises(TutorDataError, match="không phải JSON hợp lệ"):
        TutorRepository(path).get_all()


def test_non_utf8_file_raises_clear_error(tmp_path: Path) -> None:
    """Tệp không giải mã được bằng UTF-8 cũng báo lỗi định dạng."""
    path = tmp_path / "tutors.json"
    path.write_bytes(b"\xff\xfe\x00")

    with pytest.raises(TutorDataError, match="không phải JSON hợp lệ"):
        TutorRepository(path).get_all()


def test_json_root_must_be_a_list(tmp_path: Path) -> None:
    """JSON hợp lệ nhưng gốc không phải danh sách bản ghi thì báo lỗi."""
    path = _write_json(tmp_path / "tutors.json", {"tutor_id": "GS-TEST"})

    with pytest.raises(TutorDataError, match="danh sách"):
        TutorRepository(path).get_all()


def test_invalid_record_reports_position_and_tutor_id(tmp_path: Path) -> None:
    """Bản ghi sai schema: thông báo nêu vị trí bản ghi và mã gia sư."""
    path = _write_json(
        tmp_path / "tutors.json",
        [_valid_record(), _valid_record(tutor_id="GS-LOI", teaching_mode="khac")],
    )

    with pytest.raises(TutorDataError, match=r"Bản ghi số 2 \(GS-LOI\)"):
        TutorRepository(path).get_all()


def test_record_that_is_not_an_object_reports_position(tmp_path: Path) -> None:
    """Phần tử không phải đối tượng JSON vẫn báo lỗi theo vị trí, không crash."""
    path = _write_json(tmp_path / "tutors.json", [123])

    with pytest.raises(TutorDataError, match="Bản ghi số 1"):
        TutorRepository(path).get_all()


def test_default_path_comes_from_config() -> None:
    """Đường dẫn mặc định phải lấy từ config, không ghi cứng trong repository."""
    assert TutorRepository().path == config.TUTORS_JSON_PATH
