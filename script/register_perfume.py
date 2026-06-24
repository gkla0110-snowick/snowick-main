import os, sys, requests, base64
from dotenv import load_dotenv
load_dotenv('script/.env')
sys.stdout.reconfigure(encoding='utf-8')
token = os.getenv('CAFE24_ACCESS_TOKEN')
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json', 'X-Cafe24-Api-Version': '2026-03-01'}
BASE = 'https://snowick.cafe24api.com/api/v2/admin'

# 1. 삭제
r = requests.delete(f'{BASE}/products/398', headers=headers)
print(f'[삭제] 398: {r.status_code}')

# 2. 상품 등록
payload = {
    'request': {
        'product_name': '스노윅 스퀘어 블랙 퍼퓸용기 12ml 분사형 스프레이 휴대용',
        'eng_product_name': 'SNOWICK Square Black Perfume Bottle 12ml Spray',
        'custom_product_code': '스노윅 퍼퓸용기 스퀘어블랙 12ml',
        'supplier_product_name': '스노윅',
        'manufacturer_name': '스노윅',
        'origin_place_code': 'KR',
        'price': '2000',
        'supply_price': '0',
        'display': 'T',
        'selling': 'T',
        'summary_description': '스노윅 스퀘어 블랙 퍼퓸용기 12ml. 미세분사 스프레이. 향수 DIY·공방·샘플 소분용 부자재.',
        'simple_description': '간편한 휴대, 섬세한 분사. 스노윅 스퀘어 블랙 퍼퓸용기 12ml',
        'product_tag': [
            '퍼퓸용기','퍼퓸용기12ml','스노윅퍼퓸용기','DIY퍼퓸용기','향수용기',
            '스노윅부자재','12ml퍼퓸용기','스퀘어퍼퓸용기','블랙퍼퓸용기','분사형용기',
            '휴대용향수용기','향수소분용기','공방퍼퓸용기','향수DIY용기','미세분사용기',
            '스프레이용기','향수부자재','소분용기','선물용향수용기','퍼퓸소분용기'
        ],
    }
}
r2 = requests.post(f'{BASE}/products', headers=headers, json=payload)
pno = r2.json()['product']['product_no']
print(f'[등록] product_no: {pno}')

# 3. SEO
seo = {
    'request': {
        'meta_title': '스퀘어 블랙 퍼퓸용기 12ml 분사형 휴대용 — 스노윅',
        'meta_author': '스노윅',
        'meta_description': '스노윅 스퀘어 블랙 퍼퓸용기 12ml. 미세분사 스프레이 타입. 향수 DIY·공방·샘플 소분 전용 부자재. 간편 휴대, 손쉬운 리필 구조.',
        'meta_keyword': '퍼퓸용기,퍼퓸용기12ml,향수용기,DIY퍼퓸용기,스노윅퍼퓸용기,휴대용향수용기,스퀘어퍼퓸용기,향수소분용기,분사형용기,스노윅부자재',
    }
}
r3 = requests.put(f'{BASE}/products/{pno}/seo', headers=headers, json=seo)
print(f'[SEO] {r3.status_code}')

# 4. 네이버 홍보문구
r4 = requests.put(f'{BASE}/products/{pno}', headers=headers, json={
    'request': {'naverpay_product_name': '스노윅 스퀘어 블랙 퍼퓸용기 12ml 분사형 부자재'}
})
print(f'[네이버홍보문구] {r4.status_code}')

# 5. 이미지 (base64)
img_url = 'https://ecimg.cafe24img.com/pg861b64307312015/snowick/web/product/big/20260623/temp_shop1_17821518032309.png'
img_b64 = base64.b64encode(requests.get(img_url).content).decode()
r5 = requests.post(f'{BASE}/products/{pno}/images', headers=headers, json={
    'request': {
        'image_upload_type': 'B',
        'detail_image': img_b64,
        'list_image': img_b64,
        'tiny_image': img_b64,
        'small_image': img_b64,
    }
})
img = r5.json().get('image', {})
print(f'[이미지] {r5.status_code}')
print(f'  detail_image: {img.get("detail_image")}')
