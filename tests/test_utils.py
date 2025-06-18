import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.utils import extractHeaders


def test_extract_headers_valid():
    headers = "Host: example.com\nContent-Type: text/html"
    assert extractHeaders(headers) == {
        "Host": "example.com",
        "Content-Type": "text/html",
    }


def test_extract_headers_invalid_lines_are_skipped(capfd):
    headers = "InvalidLine\nAccept: */*\nAnotherInvalid"
    result = extractHeaders(headers)
    out, _ = capfd.readouterr()
    assert "Skipping invalid header line: InvalidLine" in out
    assert "Skipping invalid header line: AnotherInvalid" in out
    assert result == {"Accept": "*/*"}
