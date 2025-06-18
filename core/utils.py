import os
import json
import tempfile
import subprocess

from urllib.parse import urlparse

def host(string):
    if string and '*' not in string:
        return urlparse(string).netloc


def load_json(file):
    with open(file) as f:
        return json.load(f)


def format_result(result):
    new_result = {}
    for each in result:
        if each:
            for i in each:
                new_result[i] = each[i]
    return new_result


def collect_urls(target_url=None, source=None):
    """Return a list of URLs from a target string or iterable source.

    Parameters
    ----------
    target_url : str or None
        Single URL supplied via the command line.
    source : iterable or None
        Iterable containing newline-separated URLs (e.g. file or sys.stdin).
    """
    urls = []
    if source:
        for line in source:
            if line.startswith(("http://", "https://")):
                urls.append(line.rstrip("\n"))
    if target_url and target_url.startswith(("http://", "https://")):
        urls.append(target_url)
    return urls

def prompt(default=None):
    editor = os.environ.get('EDITOR', 'nano')
    with tempfile.NamedTemporaryFile(mode='r+') as tmpfile:
        if default:
            tmpfile.write(default)
            tmpfile.flush()

        subprocess.call([editor, tmpfile.name])
        tmpfile.seek(0)
        return tmpfile.read().strip()


def extractHeaders(headers: str, warn: bool = False):
    """Return a dictionary of HTTP headers from a string.

    Lines without a colon are ignored. If ``warn`` is ``True`` and such
    lines are encountered, a warning message is printed.
    """

    # Support both escaped ``\n`` sequences (as provided via the command line)
    # and real newlines (as produced by ``prompt()``).
    headers = headers.replace("\\n", "\n")

    sorted_headers = {}
    for line in headers.split("\n"):
        if ":" not in line:
            if warn and line.strip():
                from core.colors import bad
                print(f"{bad} ignoring invalid header line: {line.strip()}")
            continue
        name, value = line.split(":", 1)
        name = name.strip()
        value = value.strip()
        if value.endswith(','):
            value = value[:-1]
        sorted_headers[name] = value
    return sorted_headers
