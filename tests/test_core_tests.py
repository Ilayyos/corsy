import pytest

from core import tests as core_tests


def test_passive_tests_wildcard_credentials():
    url = 'https://example.com'
    headers = {'access-control-allow-origin': '*', 'access-control-allow-credentials': 'true'}
    result = core_tests.passive_tests(url, headers)
    assert result[url]['class'] == 'wildcard credentials'


def test_passive_tests_third_party():
    url = 'https://example.com'
    headers = {'access-control-allow-origin': 'https://evil.com'}
    result = core_tests.passive_tests(url, headers)
    assert result[url]['class'] == 'third party allowed'


def test_active_tests_no_acao(monkeypatch):
    def fake_requester(*args, **kwargs):
        return {}
    monkeypatch.setattr(core_tests, 'requester', fake_requester)
    result = core_tests.active_tests('https://example.com', 'example.com', 'https', {}, 0)
    assert result is None


def test_active_tests_origin_reflected(monkeypatch):
    responses = [
        {'access-control-allow-origin': 'https://example.com'},
        {'access-control-allow-origin': 'https://example.com'}
    ]

    def fake_requester(url, scheme, header_dict, origin, timeout=10, verify=True):
        return responses.pop(0)

    monkeypatch.setattr(core_tests, 'requester', fake_requester)
    monkeypatch.setattr(core_tests.time, 'sleep', lambda x: None)
    result = core_tests.active_tests('https://example.com', 'example.com', 'https', {}, 0)
    assert result['https://example.com']['class'] == 'origin reflected'
