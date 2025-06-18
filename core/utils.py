import os
import json
import tempfile

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
    editor = 'nano'
    with tempfile.NamedTemporaryFile(mode='r+') as tmpfile:
        if default:
            tmpfile.write(default)
            tmpfile.flush()

        child_pid = os.fork()
        is_child = child_pid == 0

        if is_child:
            os.execvp(editor, [editor, tmpfile.name])
        else:
            os.waitpid(child_pid, 0)
            tmpfile.seek(0)
            return tmpfile.read().strip()


def extractHeaders(headers: str):
    sorted_headers = {}
    for header in headers.split('\\n'):
        name, value = header.split(":", 1)
        name = name.strip()
        value = value.strip()
        if len(value) >= 1 and value[-1] == ',':
            value = value[:-1]
        sorted_headers[name] = value
    return sorted_headers
