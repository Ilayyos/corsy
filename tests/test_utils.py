import json
import tempfile

import pytest

from core.utils import host, load_json, format_result, collect_urls, extractHeaders


def test_host_returns_netloc():
    assert host('https://example.com/path') == 'example.com'


def test_host_returns_none_on_invalid():
    assert host(None) is None
    assert host('*.example.com') is None


def test_load_json_reads_file():
    data = {'a': 1}
    with tempfile.NamedTemporaryFile('w+', delete=False) as tmp:
        json.dump(data, tmp)
        tmp_path = tmp.name
    assert load_json(tmp_path) == data


def test_format_result_merges_dicts():
    result = [{'a': 1}, None, {'b': 2}]
    assert format_result(result) == {'a': 1, 'b': 2}


def test_collect_urls_from_source_and_target():
    lines = ['http://foo.com\n', 'https://bar.com\n', 'invalid\n']
    urls = collect_urls('http://target.com', lines)
    assert urls == ['http://foo.com', 'https://bar.com', 'http://target.com']


def test_collect_urls_handles_none():
    lines = ['not a url']
    assert collect_urls(None, lines) == []


def test_extract_headers_parses_multiline_string():
    headers = 'User-Agent: TestAgent\\nHost: example.com,\\nX-Other: value,'
    expected = {
        'User-Agent': 'TestAgent',
        'Host': 'example.com',
        'X-Other': 'value'
    }
    assert extractHeaders(headers) == expected
