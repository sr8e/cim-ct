import requests


VERSION_STRING = 'v1.0.0'


def compare_version(c, r):
    c_part = [int(cp) for cp in  c.lstrip('v').split('.')]
    r_part = [int(rp) for rp in  r.lstrip('v').split('.')]

    if (cl := len(c_part)) > (rl := len(r_part)):
        r_part += [0] * (cl - rl)

    for i, cp in enumerate(c_part):
        if cp < r_part[i]:
            return True

    if cl < rl:
        return True

    return False


def check_version():
    try:
        r = requests.get('https://api.github.com/repos/sr8e/cim-ct/releases/latest')
        rel = r.json()
        tag = rel['tag_name']
    except KeyError:
        return
    except requests.exceptions.ConnectionError:
        return

    if compare_version(VERSION_STRING, tag):
        return tag, rel['html_url']
