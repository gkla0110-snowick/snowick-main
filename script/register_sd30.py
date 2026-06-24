import os, sys, requests, base64
from dotenv import load_dotenv
load_dotenv('script/.env')
sys.stdout.reconfigure(encoding='utf-8')
token = os.getenv('CAFE24_ACCESS_TOKEN')
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json', 'X-Cafe24-Api-Version': '2026-03-01'}
BASE = 'https://snowick.cafe24api.com/api/v2/admin'

DESCRIPTION_HTML = '<div style="text-align:center;"><img src="https://ecimg.cafe24img.com/pg861b64307312015/snowick/ChatGPT%20Image%202026%EB%85%84%206%EC%9B%94%2023%EC%9D%BC%20%EC%98%A4%EC%A0%84%2007_52_35%20%282%29.png" alt="스노윅 실버 다이아 퍼퓸용기 30ml 분사형 스프레이 공병" style="max-width:100%;"><img src="https://ecimg.cafe24img.com/pg861b64307312015/snowick/ChatGPT%20Image%202026%EB%85%84%206%EC%9B%94%2023%EC%9D%BC%20%EC%98%A4%EC%A0%84%2007_52_36%20%283%29.png" alt="SNOWICK 실버 다이아 퍼퓸용기 다이아컷 유리 실버 메탈 캡" style="max-width:100%;"><img src="https://ecimg.cafe24img.com/pg861b64307312015/snowick/ChatGPT%20Image%202026%EB%85%84%206%EC%9B%94%2023%EC%9D%BC%20%EC%98%A4%EC%A0%84%2007_52_35%20%281%29.png" alt="스노윅 퍼퓸용기 30ml DIY 향수 제작 공방용 공병" style="max-width:100%;"></div>'

# 1. 상품 등록
payload = {
    'request': {
        'product_name': '스노윅 실버 다이아 퍼퓸용기 30ml 분사형 스프레이 DIY 향수 공병',
        'eng_product_name': 'SNOWICK Silver Diamond Perfume Bottle 30ml Spray',
        'custom_product_code': '스노윅 퍼퓸용기 실버다이아 30ml',
        'supplier_product_name': '스노윅',
        'manufacturer_name': '스노윅',
        'model_name': 'SNOWICK-PB-SD-30',
        'origin_place_code': 'CHN',
        'price': '3000',
        'supply_price': '0',
        'display': 'T',
        'selling': 'T',
        'summary_description': '스노윅 실버 다이아 퍼퓸용기 30ml. 입체 다이아컷 유리 바디와 메탈릭 실버 캡. 조향 공방·DIY 향수 제작·샘플·선물 구성 전용 스프레이 공병.',
        'simple_description': '다이아컷 유리, 실버 메탈 캡. 스노윅 실버 다이아 퍼퓸용기 30ml',
        'description': DESCRIPTION_HTML,
        'product_tag': [
            '퍼퓸용기','퍼퓸용기30ml','스노윅퍼퓸용기','DIY퍼퓸용기','향수공병',
            '30ml공병','실버다이아퍼퓸용기','다이아컷퍼퓸용기','분사형용기','스프레이공병',
            '향수소분용기','DIY향수공병','조향공방용기','샘플향수공병','선물용공병',
            '고급퍼퓸용기','유리퍼퓸용기','실버캡공병','스노윅부자재','향수부자재'
        ],
    }
}
r = requests.post(f'{BASE}/products', headers=headers, json=payload)
if r.status_code != 201:
    print(f'[ERROR] {r.status_code}: {r.text[:300]}')
    exit(1)
pno = r.json()['product']['product_no']
print(f'[1/4] 상품 등록 완료 — product_no: {pno}')

# 2. SEO
r2 = requests.put(f'{BASE}/products/{pno}/seo', headers=headers, json={
    'request': {
        'meta_title': '실버 다이아 퍼퓸용기 30ml 분사형 DIY 공병 — 스노윅',
        'meta_author': '스노윅',
        'meta_description': '스노윅 실버 다이아 퍼퓸용기 30ml. 입체 다이아컷 유리 바디에 메탈릭 실버 캡 조합. 조향 공방·DIY 향수 제작·샘플 소분·선물 구성 전용 스프레이 공병. 내용물 미포함.',
        'meta_keyword': '퍼퓸용기,퍼퓸용기30ml,향수공병,DIY퍼퓸용기,실버다이아퍼퓸용기,스노윅퍼퓸용기,분사형공병,향수소분용기,다이아컷용기,스노윅부자재',
    }
})
print(f'[2/4] SEO 설정 완료 — {r2.status_code}')

# 3. 네이버 홍보문구
r3 = requests.put(f'{BASE}/products/{pno}', headers=headers, json={
    'request': {'naverpay_product_name': '스노윅 실버 다이아 퍼퓸용기 30ml 분사형 DIY 공병'}
})
print(f'[3/4] 네이버 홍보문구 — {r3.status_code}')

# 4. 대표이미지 (base64)
img_url = 'https://ecimg.cafe24img.com/pg861b64307312015/snowick/ChatGPT%20Image%202026%EB%85%84%206%EC%9B%94%2023%EC%9D%BC%20%EC%98%A4%EC%A0%84%2007_52_36%20%283%29.png'
img_b64 = base64.b64encode(requests.get(img_url).content).decode()
r4 = requests.post(f'{BASE}/products/{pno}/images', headers=headers, json={
    'request': {
        'image_upload_type': 'B',
        'detail_image': img_b64,
        'list_image': img_b64,
        'tiny_image': img_b64,
        'small_image': img_b64,
    }
})
img = r4.json().get('image', {})
print(f'[4/4] 이미지 업로드 — {r4.status_code}')
print(f'  detail_image: {img.get("detail_image")}')
print(f'\n완료 — product_no: {pno}')
