import json
from core import utils


def test_host_extracts_netloc():
    assert utils.host('https://example.com/path') == 'example.com'


def test_host_ignores_wildcard():
    assert utils.host('https://*.example.com') is None


def test_load_json(tmp_path):
    data = {'a': 1}
    f = tmp_path / 'data.json'
    f.write_text(json.dumps(data))
    assert utils.load_json(str(f)) == data


def test_format_result_merges_dicts():
    result = [{'a': {'acao header': '*'}}, None, {'b': {'acao header': '*'}}]
    assert utils.format_result(result) == {
        'a': {'acao header': '*'},
        'b': {'acao header': '*'},
    }


def test_collect_urls_from_source_and_target():
    source = ['https://one.com\n', 'ftp://bad.com\n', 'http://two.com\n']
    urls = utils.collect_urls('https://target.com', source)
    assert urls == ['https://one.com', 'http://two.com', 'https://target.com']


def test_extract_headers():
    header_str = 'User-Agent: Foo\\nCookie: BAR,\\nX-Test: Value,'
    expected = {'User-Agent': 'Foo', 'Cookie': 'BAR', 'X-Test': 'Value'}
    assert utils.extractHeaders(header_str) == expected
