import os
import json
import tempfile

from urllib.parse import urlparse


def host(string):
    """Return the hostname portion of ``string``.

    Parameters
    ----------
    string : str or None
        URL or origin string to parse.

    Returns
    -------
    str or None
        Hostname extracted from ``string`` or ``None`` if ``string`` is empty
        or contains a wildcard.
    """
    if string and "*" not in string:
        return urlparse(string).netloc


def load_json(file):
    """Load and parse a JSON file.

    Parameters
    ----------
    file : str
        Path to the JSON file on disk.

    Returns
    -------
    dict
        Parsed JSON data.
    """
    with open(file) as f:
        return json.load(f)


def format_result(result):
    """Combine dictionaries from CORS checks into one mapping.

    Parameters
    ----------
    result : iterable
        Iterable containing dictionaries of test results.

    Returns
    -------
    dict
        Flattened dictionary with URLs as keys and issue details as values.
    """
    new_result = {}
    for each in result:
        if each:
            for i in each:
                new_result[i] = each[i]
    return new_result


def collect_urls(target_url=None, source=None):
    """Collect target URLs from a command line value or stream.

    Parameters
    ----------
    target_url : str or None
        Single URL supplied via the command line.
    source : Iterable[str] or None
        Iterable yielding newline separated URLs such as a file handle.

    Returns
    -------
    list[str]
        A list of validated URLs.
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
    """Open a temporary file in ``nano`` and return the user's input.

    Parameters
    ----------
    default : str or None, optional
        Initial text to populate the editor with.

    Returns
    -------
    str
        The text entered by the user.
    """
    editor = "nano"
    with tempfile.NamedTemporaryFile(mode="r+") as tmpfile:
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
    """Parse a block of HTTP headers into a dictionary.

    Parameters
    ----------
    headers : str
        Raw header string separated by newlines.

    Returns
    -------
    dict
        Mapping of header names to values.
    """
    sorted_headers = {}
    for header in headers.split("\\n"):
        name, value = header.split(":", 1)
        name = name.strip()
        value = value.strip()
        if len(value) >= 1 and value[-1] == ",":
            value = value[:-1]
        sorted_headers[name] = value
    return sorted_headers
