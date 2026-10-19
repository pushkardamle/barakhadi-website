"""Read-only TalentLMS API client.

Only HTTP GET is possible: there is no code path that sends POST/PUT/PATCH/DELETE.
The API key is read from barakhadi-web/.env (git-ignored) and never printed.
"""
import base64, json, pathlib, sys, time, urllib.request, urllib.error

ROOT = pathlib.Path(__file__).resolve().parents[3]          # barakhadi-web/
ENV = dict(l.split('=', 1) for l in (ROOT / '.env').read_text().split() if '=' in l)
DOMAIN = ENV.get('TALENTLMS_DOMAIN', 'marathi.talentlms.com')
_AUTH = 'Basic ' + base64.b64encode((ENV['TALENTLMS_API_KEY'] + ':').encode()).decode()

def get(path: str, retries: int = 3):
    """GET https://<domain>/api/v1/<path> and return parsed JSON."""
    url = f'https://{DOMAIN}/api/v1/{path.lstrip("/")}'
    req = urllib.request.Request(url, method='GET', headers={'Authorization': _AUTH, 'Accept': 'application/json'})
    assert req.get_method() == 'GET'
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries - 1:
                time.sleep(5 * (attempt + 1)); continue
            raise SystemExit(f'GET {path} -> HTTP {e.code}: {e.read()[:200]!r}')

if __name__ == '__main__':
    print(json.dumps(get(sys.argv[1]), ensure_ascii=False, indent=1)[:3000])


def get_page(url: str):
    """GET a page on the same TalentLMS domain (e.g. a unit's apiview URL). Returns (status, content-type, text). GET only."""
    assert url.startswith(f'https://{DOMAIN}/'), 'only the Barakhadi TalentLMS domain'
    req = urllib.request.Request(url, method='GET', headers={'Authorization': _AUTH})
    assert req.get_method() == 'GET'
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, r.headers.get('Content-Type', ''), r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get('Content-Type', ''), e.read()[:500].decode('utf-8', 'replace')
