import sys
import time

from core.requester import requester
from core.utils import host, load_json

details = load_json(sys.path[0] + '/db/details.json')

def passive_tests(url, headers):
    root = host(url)
    acao_header, acac_header = headers.get('access-control-allow-origin', None), headers.get('access-control-allow-credentials', None)
    if acao_header == '*' and acac_header and acac_header.lower() == 'true':
        info = details['wildcard credentials'].copy()
        info['acao header'] = acao_header
        info['acac header'] = acac_header
        return {url: info}
    if acao_header == '*':
        info = details['wildcard value'].copy()
        info['acao header'] = acao_header
        info['acac header'] = acac_header
        return {url: info}
    if root:
        if host(acao_header) and root != host(acao_header):
            info = details['third party allowed'].copy()
            info['acao header'] = acao_header
            info['acac header'] = acac_header
            return {url : info}


def active_tests(url, root, scheme, header_dict, delay, timeout=10, verify=True):
    origin = scheme + '://' + root
    headers = requester(url, header_dict, origin, timeout=timeout, verify=verify)
    acao_header, acac_header = headers.get('access-control-allow-origin', None), headers.get('access-control-allow-credentials', None)
    if acao_header is None:
        return
    
    origin = scheme + '://' + 'example.com'
    headers = requester(url, header_dict, origin, timeout=timeout, verify=verify)
    acao_header, acac_header = headers.get('access-control-allow-origin', None), headers.get('access-control-allow-credentials', None)
    if acao_header and acao_header == (origin):
        info = details['origin reflected'].copy()
        info['acao header'] = acao_header
        info['acac header'] = acac_header
        return {url : info}
    time.sleep(delay)

    origin = scheme + '://' + root + '.example.com'
    headers = requester(url, header_dict, origin, timeout=timeout, verify=verify)
    acao_header, acac_header = headers.get('access-control-allow-origin', None), headers.get('access-control-allow-credentials', None)
    if acao_header and acao_header == (origin):
        info = details['post-domain wildcard'].copy()
        info['acao header'] = acao_header
        info['acac header'] = acac_header
        return {url : info}
    time.sleep(delay)

    origin = scheme + '://d3v' + root
    headers = requester(url, header_dict, origin, timeout=timeout, verify=verify)
    acao_header, acac_header = headers.get('access-control-allow-origin', None), headers.get('access-control-allow-credentials', None)
    if acao_header and acao_header == (origin):
        info = details['pre-domain wildcard'].copy()
        info['acao header'] = acao_header
        info['acac header'] = acac_header
        return {url : info}
    time.sleep(delay)

    origin = 'null'
    headers = requester(url, header_dict, origin, timeout=timeout, verify=verify)
    acao_header, acac_header = headers.get('access-control-allow-origin', None), headers.get('access-control-allow-credentials', None)
    if acao_header and acao_header == 'null':
        info = details['null origin allowed'].copy()
        info['acao header'] = acao_header
        info['acac header'] = acac_header
        return {url : info}
    time.sleep(delay)

    origin = scheme + '://' + root + '_.example.com'
    headers = requester(url, header_dict, origin, timeout=timeout, verify=verify)
    acao_header, acac_header = headers.get('access-control-allow-origin', None), headers.get('access-control-allow-credentials', None)
    if acao_header and acao_header == origin:
        info = details['unrecognized underscore'].copy()
        info['acao header'] = acao_header
        info['acac header'] = acac_header
        return {url : info}
    time.sleep(delay)

    origin = scheme + '://' + root + '%60.example.com'
    headers = requester(url, header_dict, origin, timeout=timeout, verify=verify)
    acao_header, acac_header = headers.get('access-control-allow-origin', None), headers.get('access-control-allow-credentials', None)
    if acao_header and '`.example.com' in acao_header:
        info = details['broken parser'].copy()
        info['acao header'] = acao_header
        info['acac header'] = acac_header
        return {url : info}
    time.sleep(delay)

    if root.count('.') > 1:
        origin = scheme + '://' + root.replace('.', 'x', 1)
        headers = requester(url, header_dict, origin, timeout=timeout, verify=verify)
        acao_header, acac_header = headers.get('access-control-allow-origin', None), headers.get('access-control-allow-credentials', None)
        if acao_header and acao_header == origin:
            info = details['unescaped regex'].copy()
            info['acao header'] = acao_header
            info['acac header'] = acac_header
            return {url : info}
        time.sleep(delay)
    origin = 'http://' + root
    headers = requester(url, header_dict, origin, timeout=timeout, verify=verify)
    acao_header, acac_header = headers.get('access-control-allow-origin', None), headers.get('access-control-allow-credentials', None)
    if acao_header and acao_header.startswith('http://'):
        info = details['http origin allowed'].copy()
        info['acao header'] = acao_header
        info['acac header'] = acac_header
        return {url : info}
    else:
        return passive_tests(url, headers)
