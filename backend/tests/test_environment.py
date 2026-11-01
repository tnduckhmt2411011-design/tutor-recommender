"""Kiểm tra môi trường Python và các thư viện bắt buộc của backend (US-01)."""

import sys

import fastapi
import pydantic


def test_python_version_is_312() -> None:
    """Môi trường phát triển thống nhất dùng Python 3.12 theo Issue #1."""
    assert sys.version_info[:2] == (3, 12)


def test_core_dependencies_are_importable() -> None:
    """FastAPI và Pydantic phải import được sau khi cài requirements."""
    assert fastapi.__version__
    assert pydantic.VERSION


def test_app_package_is_importable() -> None:
    """Gói app phải import được khi chạy pytest từ thư mục backend."""
    import app

    assert app.__name__ == "app"
