import pytest

from app.errors import ValidationError
from app.services.storage_service import StorageService


class TestValidateFileSignature:

    def test_valid_jpeg_passes(self):
        StorageService().validate_file_signature(b"\xff\xd8\xff" + b"x" * 100, "image/jpeg")

    def test_valid_png_passes(self):
        StorageService().validate_file_signature(b"\x89PNG\r\n\x1a\n" + b"x" * 100, "image/png")

    def test_valid_pdf_passes(self):
        StorageService().validate_file_signature(b"%PDF" + b"x" * 100, "application/pdf")

    def test_valid_docx_passes(self):
        StorageService().validate_file_signature(
            b"PK\x03\x04" + b"x" * 100,
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

    def test_wrong_magic_bytes_raises(self):
        with pytest.raises(ValidationError) as exc:
            StorageService().validate_file_signature(b"MZ\x90\x00" + b"x" * 100, "application/pdf")
        assert exc.value.code == "INVALID_FILE_TYPE"

    def test_unknown_content_type_raises(self):
        with pytest.raises(ValidationError) as exc:
            StorageService().validate_file_signature(b"%PDF" + b"x" * 100, "text/plain")
        assert exc.value.code == "INVALID_FILE_TYPE"

    def test_jpeg_disguised_as_pdf_raises(self):
        with pytest.raises(ValidationError) as exc:
            StorageService().validate_file_signature(b"\xff\xd8\xff" + b"x" * 100, "application/pdf")
        assert exc.value.code == "INVALID_FILE_TYPE"

    def test_empty_content_raises(self):
        with pytest.raises(ValidationError) as exc:
            StorageService().validate_file_signature(b"", "application/pdf")
        assert exc.value.code == "INVALID_FILE_TYPE"
