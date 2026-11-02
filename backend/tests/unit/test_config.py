"""Kiểm thử đơn vị cho cấu hình tham số thuật toán và đường dẫn dữ liệu (config.py)."""

from pathlib import Path

from app.core import config


def test_algorithm_parameters_match_scoring_spec() -> None:
    """Ba tham số thuật toán phải đúng giá trị đã chốt ở Mục 3.6 và Bảng 3.6."""
    assert config.DELTA == 0.5
    assert config.E_MAX == 8
    assert config.RATING_DEFAULT == 0.5


def test_priority_weights_match_table_3_5() -> None:
    """Bốn mức ưu tiên ánh xạ đúng trọng số của Bảng 3.5."""
    assert config.PRIORITY_WEIGHTS == {
        "none": 0,
        "low": 1,
        "medium": 2,
        "high": 3,
    }
    assert config.DEFAULT_PRIORITY == "medium"


def test_criteria_keys_are_complete() -> None:
    """Tên khóa 5 tiêu chí dùng thống nhất với mô hình dữ liệu."""
    assert config.CRITERIA_KEYS == (
        "fee",
        "district",
        "experience",
        "rating",
        "availability",
    )


def test_data_paths_point_to_existing_files() -> None:
    """Đường dẫn dữ liệu phải trỏ đúng tệp trong repo khi chạy pytest từ backend/."""
    assert config.TUTORS_JSON_PATH.is_file()
    assert config.TUTORS_CSV_PATH.is_file()


def test_data_paths_do_not_depend_on_working_directory(
    monkeypatch, tmp_path: Path
) -> None:
    """Đổi thư mục chạy vẫn phải tìm thấy dữ liệu nhờ đường dẫn tuyệt đối."""
    monkeypatch.chdir(tmp_path)

    assert config.TUTORS_JSON_PATH.is_file()
    assert config.TUTORS_CSV_PATH.is_file()
    assert config.TUTORS_JSON_PATH.is_absolute()
