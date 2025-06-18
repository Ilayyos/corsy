import urllib3
import requests
import aiohttp
from core.colors import bad

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

session = requests.Session()

# Added better error handling.
# Added verbose options.

def requester(url, scheme, headers, origin, timeout=10, verify=True):
    """Send a request with the supplied origin and return response headers."""
    request_headers = headers.copy()
    request_headers['Origin'] = origin
    try:
        response = session.get(
            url, headers=request_headers, verify=verify, timeout=timeout
        )
        headers = response.headers
        return headers
    except requests.exceptions.RequestException as e:
        if 'Failed to establish a new connection' in str(e):
            print('%s %s is unreachable' % (bad, url))
        elif 'TooManyRedirects' in str(e):
            print('%s %s has too many redirects' % (bad, url))
        return {}


async def requester_async(url, scheme, headers, origin, timeout=10, verify=True):
    """Asynchronous version of requester using aiohttp."""
    request_headers = headers.copy()
    request_headers['Origin'] = origin
    timeout_obj = aiohttp.ClientTimeout(total=timeout)
    try:
        async with aiohttp.ClientSession(timeout=timeout_obj) as session:
            async with session.get(url, headers=request_headers, ssl=verify) as response:
                return response.headers
    except aiohttp.ClientError as e:
        if 'Failed to establish a new connection' in str(e) or 'ClientConnectorError' in str(e):
            print('%s %s is unreachable' % (bad, url))
        elif 'TooManyRedirects' in str(e):
            print('%s %s has too many redirects' % (bad, url))
        return {}
