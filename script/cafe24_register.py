"""
SNOWICK Cafe24 상품 자동 등록 스크립트

사전 준비:
  1. pip install requests python-dotenv
  2. script/.env.example → script/.env 복사 후 값 입력
  3. python cafe24_auth.py 실행해 토큰 발급
  4. python cafe24_register.py 실행

기능:
  - 상품명 / 상세설명 / 검색어(태그) / 이미지 자동 등록
  - access_token 만료 시 refresh_token으로 자동 갱신
"""

import os
import json
import base64
import time
import requests
from dotenv import load_dotenv, set_key

ENV_FILE = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(ENV_FILE)

MALL_ID       = os.getenv("CAFE24_MALL_ID", "snowick")
CLIENT_ID     = os.getenv("CAFE24_CLIENT_ID")
CLIENT_SECRET = os.getenv("CAFE24_CLIENT_SECRET")
BASE_URL      = f"https://{MALL_ID}.cafe24api.com/api/v2"
API_VERSION   = "2024-03-01"

# ──────────────────────────────────────────────
# 스노윅 캔들 8종 상품 데이터
# ──────────────────────────────────────────────

COMMON_DESCRIPTION = """캔들이 다 쓰기도 전에 가운데만 녹고 가장자리는 그대로 남아 버리신 적 있나요?

일반 캔들은 심지 하나라 열이 중앙에만 집중됩니다.
스노윅은 자작나무 심지 3P를 별모양으로 엇갈려 도킹하여
불이 용기 가장자리까지 열이 골고루 전달되어 벽면까지 남김없이 녹입니다.
터널링 0%의 이유입니다.

유리 용기는 열이 외부로 전달돼 용기가 뜨겁습니다.
대나무는 열전도율이 낮아 왁스가 다 녹아도 용기 겉은 따뜻한 정도.
우드코스터 없이 바로 씁니다."""

COMMON_TAGS = [
    "대나무캔들", "별모양심지캔들", "터널링없는캔들", "소이캔들",
    "우드심지캔들", "스노윅", "200g캔들", "천연왁스캔들", "특허캔들", "크랙클링캔들"
]

PRODUCTS = [
    {
        "product_name": "스노윅 대나무캔들 200g 비자림숲속",
        "scent": "비자림숲속",
        "scent_desc": "제주 비자림 숲의 첫 숨을 담았습니다.",
        "tags": ["비자림숲속캔들", "비자림향캔들", "제주향캔들"] + COMMON_TAGS,
        "image_url": "",  # 이미지 URL 입력 (공란 시 등록 생략)
    },
    {
        "product_name": "스노윅 대나무캔들 200g 동백꽃",
        "scent": "동백꽃",
        "scent_desc": "겨울 한가운데 피는 붉은 동백을 담았습니다.",
        "tags": ["동백꽃캔들", "동백꽃향캔들", "겨울캔들"] + COMMON_TAGS,
        "image_url": "",
    },
    {
        "product_name": "스노윅 대나무캔들 200g 매화꽃",
        "scent": "매화꽃",
        "scent_desc": "눈 녹기 전 가장 먼저 피는 봄을 담았습니다.",
        "tags": ["매화꽃캔들", "매화향캔들", "봄캔들"] + COMMON_TAGS,
        "image_url": "",
    },
    {
        "product_name": "스노윅 대나무캔들 200g 철쭉꽃",
        "scent": "철쭉꽃",
        "scent_desc": "능선을 물들이는 연분홍 봄을 담았습니다.",
        "tags": ["철쭉꽃캔들", "철쭉향캔들", "봄꽃캔들"] + COMMON_TAGS,
        "image_url": "",
    },
    {
        "product_name": "스노윅 대나무캔들 200g 한라봉",
        "scent": "한라봉",
        "scent_desc": "톡 터지는 제주 한라봉 향을 담았습니다.",
        "tags": ["한라봉캔들", "한라봉향캔들", "시트러스캔들"] + COMMON_TAGS,
        "image_url": "",
    },
    {
        "product_name": "스노윅 대나무캔들 200g 오리엔탈템플우디",
        "scent": "오리엔탈템플우디",
        "scent_desc": "오래된 사찰의 고요한 향을 담았습니다.",
        "tags": ["오리엔탈캔들", "우디캔들", "사찰향캔들"] + COMMON_TAGS,
        "image_url": "",
    },
    {
        "product_name": "스노윅 대나무캔들 200g 우디프레스티지",
        "scent": "우디프레스티지",
        "scent_desc": "가죽 서재에 스민 묵직한 향을 담았습니다.",
        "tags": ["우디프레스티지캔들", "고급캔들", "우디향캔들"] + COMMON_TAGS,
        "image_url": "",
    },
    {
        "product_name": "스노윅 대나무캔들 200g 레몬가든플뢰르",
        "scent": "레몬가든플뢰르",
        "scent_desc": "화사하다 차분해지는 두 얼굴의 향입니다.",
        "tags": ["레몬가든캔들", "플뢰르캔들", "레몬향캔들"] + COMMON_TAGS,
        "image_url": "",
    },
]

# ──────────────────────────────────────────────
# 토큰 관리
# ──────────────────────────────────────────────

def get_access_token():
    return os.getenv("CAFE24_ACCESS_TOKEN")


def refresh_access_token():
    refresh_token = os.getenv("CAFE24_REFRESH_TOKEN")
    if not refresh_token:
        raise RuntimeError("CAFE24_REFRESH_TOKEN이 없습니다. cafe24_auth.py를 먼저 실행하세요.")

    url = f"https://{MALL_ID}.cafe24api.com/api/v2/oauth/token"
    credentials = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    headers = {
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    resp = requests.post(url, headers=headers, data=data)
    resp.raise_for_status()
    token_data = resp.json()

    set_key(ENV_FILE, "CAFE24_ACCESS_TOKEN",  token_data["access_token"])
    set_key(ENV_FILE, "CAFE24_REFRESH_TOKEN", token_data["refresh_token"])
    os.environ["CAFE24_ACCESS_TOKEN"]  = token_data["access_token"]
    os.environ["CAFE24_REFRESH_TOKEN"] = token_data["refresh_token"]

    print("🔄 토큰 갱신 완료")
    return token_data["access_token"]


def get_headers():
    return {
        "Authorization": f"Bearer {get_access_token()}",
        "Content-Type": "application/json",
        "X-Cafe24-Api-Version": API_VERSION,
    }


def api_call(method, endpoint, payload=None, retry=True):
    url = f"{BASE_URL}{endpoint}"
    resp = getattr(requests, method)(url, headers=get_headers(), json=payload)

    if resp.status_code == 401 and retry:
        refresh_access_token()
        return api_call(method, endpoint, payload, retry=False)

    if not resp.ok:
        print(f"  ❌ API 오류 {resp.status_code}: {resp.text[:200]}")
        resp.raise_for_status()

    return resp.json()

# ──────────────────────────────────────────────
# 상품 등록
# ──────────────────────────────────────────────

def build_description(product):
    return f"""{COMMON_DESCRIPTION}

오늘은 {product['scent']} — {product['scent_desc']}"""


def register_product(product):
    tags = list(dict.fromkeys(product["tags"]))[:20]  # 중복 제거, 최대 20개

    payload = {
        "request": {
            "product_name": product["product_name"],
            "description": build_description(product),
            "summary_description": f"특허심지 터널링 0% 대나무 소이캔들 200g — {product['scent']}",
            "product_tag": ",".join(tags),
            "display": "T",     # 진열
            "selling": "T",     # 판매
            "product_weight": "300.00",
            "manufacturer_code": "M0000000",
            "origin_place_no": 1826,    # 대한민국
        }
    }

    result = api_call("post", "/products", payload)
    product_no = result["product"]["product_no"]
    print(f"  ✅ 상품 등록 완료 — product_no: {product_no}")
    return product_no


def upload_image(product_no, image_url):
    if not image_url:
        print("  ⏭  이미지 URL 없음 — 이미지 등록 생략")
        return

    payload = {
        "request": {
            "image_upload_type": "U",
            "detail_image":      image_url,
            "list_image":        image_url,
            "tiny_image":        image_url,
            "small_image":       image_url,
        }
    }
    api_call("post", f"/products/{product_no}/images", payload)
    print(f"  🖼  이미지 등록 완료")


def set_seo(product_no, product):
    payload = {
        "request": {
            "meta_title":       product["product_name"],
            "meta_author":      "스노윅 SNOWICK",
            "meta_description": f"특허심지 터널링0% 대나무 소이캔들 200g {product['scent']}. "
                                f"별모양우드심지 구조로 벽면까지 균일 연소. 스노윅.",
            "meta_keywords":    ",".join(product["tags"][:10]),
        }
    }
    api_call("put", f"/products/{product_no}/seo", payload)
    print(f"  🔍 SEO 설정 완료")

# ──────────────────────────────────────────────
# 메인 실행
# ──────────────────────────────────────────────

def main():
    if not CLIENT_ID or not CLIENT_SECRET:
        print("❌ script/.env 파일에 CAFE24_CLIENT_ID / CAFE24_CLIENT_SECRET을 입력하세요.")
        return
    if not get_access_token():
        print("❌ CAFE24_ACCESS_TOKEN이 없습니다. python cafe24_auth.py를 먼저 실행하세요.")
        return

    print(f"\n🚀 스노윅 캔들 {len(PRODUCTS)}종 Cafe24 자동 등록 시작\n")
    results = []

    for i, product in enumerate(PRODUCTS, 1):
        print(f"[{i}/{len(PRODUCTS)}] {product['product_name']}")
        try:
            product_no = register_product(product)
            upload_image(product_no, product["image_url"])
            set_seo(product_no, product)
            results.append({"scent": product["scent"], "product_no": product_no, "status": "성공"})
        except Exception as e:
            print(f"  ❌ 실패: {e}")
            results.append({"scent": product["scent"], "product_no": None, "status": f"실패: {e}"})

        time.sleep(0.5)  # API 호출 간격

    print("\n──────────────────────────────────────")
    print("📋 등록 결과")
    print("──────────────────────────────────────")
    for r in results:
        icon = "✅" if r["status"] == "성공" else "❌"
        print(f"  {icon} {r['scent']:20s} | product_no: {r['product_no']} | {r['status']}")

    success = sum(1 for r in results if r["status"] == "성공")
    print(f"\n총 {len(PRODUCTS)}종 중 {success}종 성공\n")


if __name__ == "__main__":
    main()
