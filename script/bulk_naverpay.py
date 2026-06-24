import os, sys, requests, base64
from dotenv import load_dotenv, set_key
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
sys.stdout.reconfigure(encoding='utf-8')

MALL_ID = 'snowick'
CLIENT_ID = os.getenv('CAFE24_CLIENT_ID')
CLIENT_SECRET = os.getenv('CAFE24_CLIENT_SECRET')
API_VERSION = '2026-03-01'
ENV_FILE = os.path.join(os.path.dirname(__file__), '.env')


def get_headers():
    return {
        'Authorization': f'Bearer {os.getenv("CAFE24_ACCESS_TOKEN")}',
        'Content-Type': 'application/json',
        'X-Cafe24-Api-Version': API_VERSION,
    }


def refresh():
    rt = os.getenv('CAFE24_REFRESH_TOKEN')
    cred = base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode()
    r = requests.post(
        f'https://{MALL_ID}.cafe24api.com/api/v2/oauth/token',
        headers={'Authorization': f'Basic {cred}', 'Content-Type': 'application/x-www-form-urlencoded'},
        data={'grant_type': 'refresh_token', 'refresh_token': rt}
    )
    if r.status_code == 200:
        t = r.json()
        set_key(ENV_FILE, 'CAFE24_ACCESS_TOKEN', t['access_token'])
        set_key(ENV_FILE, 'CAFE24_REFRESH_TOKEN', t['refresh_token'])
        os.environ['CAFE24_ACCESS_TOKEN'] = t['access_token']
        os.environ['CAFE24_REFRESH_TOKEN'] = t['refresh_token']
        print('[OK] 토큰 갱신 완료')
    else:
        print(f'[ERROR] 갱신 실패: {r.text[:200]}')
        sys.exit(1)


BASE = f'https://{MALL_ID}.cafe24api.com/api/v2/admin'

# 토큰 확인
r = requests.get(f'{BASE}/products/190', headers=get_headers())
if r.status_code == 401:
    print('[INFO] 토큰 만료 -- 갱신 중...')
    refresh()
print(f'[OK] 토큰 유효 ({r.status_code})')

# 전체 상품 목록 수집 (페이징)
all_products = []
offset = 0
limit = 100
while True:
    r = requests.get(
        f'{BASE}/products',
        headers=get_headers(),
        params={'limit': limit, 'offset': offset}
    )
    if r.status_code != 200:
        print(f'[ERROR] 상품 조회 실패: {r.status_code} {r.text[:200]}')
        sys.exit(1)
    items = r.json().get('products', [])
    all_products.extend(items)
    if len(items) < limit:
        break
    offset += limit

print(f'[INFO] 전체 상품 수: {len(all_products)}개')

# use_naverpay != "T" 대상 필터
targets = []
for p in all_products:
    info = p.get('naver_shopping_info') or {}
    if info.get('use_naverpay') != 'T':
        targets.append(p)

print(f'[INFO] 수정 대상: {len(targets)}개\n')

if not targets:
    print('[완료] 모든 상품이 이미 use_naverpay=T 입니다.')
    sys.exit(0)

# 일괄 수정
updated = []
failed = []
for p in targets:
    pno = p['product_no']
    pname = p.get('product_name', '(이름없음)')
    r = requests.put(
        f'{BASE}/products/{pno}',
        headers=get_headers(),
        json={'request': {'market_sync': 'T'}}
    )
    if r.status_code == 200:
        updated.append((pno, pname))
        print(f'  [OK] {pno} {pname}')
    else:
        failed.append((pno, pname, r.status_code))
        print(f'  [FAIL] {pno} {pname} -- {r.status_code}: {r.text[:100]}')

print(f'\n{"="*50}')
print(f'[결과] 성공: {len(updated)}개 / 실패: {len(failed)}개')
if updated:
    print('\n[수정 완료 목록]')
    for pno, pname in updated:
        print(f'  {pno}  {pname}')
if failed:
    print('\n[실패 목록]')
    for pno, pname, code in failed:
        print(f'  {pno}  {pname}  ({code})')
