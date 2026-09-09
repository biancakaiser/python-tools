import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pdf_to_json.extractor import extract_pdf


class FakePage:
    def __init__(self, text: str):
        self.text = text

    def extract_text(self) -> str:
        return self.text


class FakeReader:
    metadata = {"/Title": "Example", "/Author": None}
    pages = [FakePage("First page"), FakePage("Second page")]

    def __init__(self, path: str):
        self.path = path

    def get_fields(self):
        return {"customer": {"/V": "Ada"}}


class ExtractPdfTests(unittest.TestCase):
    def test_extracts_pages_metadata_and_form_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "example.pdf"
            path.touch()
            with patch("pdf_to_json.extractor.PdfReader", FakeReader):
                result = extract_pdf(path)

        self.assertEqual(result["file"], "example.pdf")
        self.assertEqual(result["pages_count"], 2)
        self.assertEqual(result["metadata"], {"Title": "Example"})
        self.assertEqual(result["form_fields"], {"customer": "Ada"})
        self.assertEqual(result["pages"][1]["text"], "Second page")


if __name__ == "__main__":
    unittest.main()