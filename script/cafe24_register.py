"""
SNOWICK Cafe24 상품 자동 등록 스크립트

사전 준비:
  1. pip install requests python-dotenv
  2. script/.env.example → script/.env 복사 후 값 입력
  3. python cafe24_auth.py 실행해 토큰 발급

실행:
  python cafe24_register.py            -- 캔들 8종 등록
  python cafe24_register.py --material -- 부자재 상품 등록
  python cafe24_register.py --all      -- 전체 등록
"""

import os
import sys
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
# 캔들 8종 데이터
# ──────────────────────────────────────────────

_CANDLE_BODY = """캔들이 다 쓰기도 전에 가운데만 녹고 가장자리는 그대로 남아 버리신 적 있나요?

일반 캔들은 심지 하나라 열이 중앙에만 집중됩니다.
스노윅은 자작나무 심지 3P를 별모양으로 엇갈려 도킹하여
불이 용기 가장자리까지 열이 골고루 전달되어 벽면까지 남김없이 녹입니다.
터널링 0%의 이유입니다.

유리 용기는 열이 외부로 전달돼 용기가 뜨겁습니다.
대나무는 열전도율이 낮아 왁스가 다 녹아도 용기 겉은 따뜻한 정도.
우드코스터 없이 바로 씁니다."""

_CANDLE_COMMON_TAGS = [
    "대나무캔들", "별모양심지캔들", "터널링없는캔들", "소이캔들",
    "우드심지캔들", "스노윅", "200g캔들", "천연왁스캔들", "특허캔들", "크랙클링캔들",
]

CANDLE_PRODUCTS = [
    {
        "product_name":    "스노윅 대나무캔들 200g 비자림숲속",
        "description":     f"{_CANDLE_BODY}\n\n오늘은 비자림숲속 — 제주 비자림 숲의 첫 숨을 담았습니다.",
        "summary_description": "특허심지 터널링 0% 대나무 소이캔들 200g — 비자림숲속",
        "tags":            ["비자림숲속캔들", "비자림향캔들", "제주향캔들"] + _CANDLE_COMMON_TAGS,
        "price":           "19000",
        "display":         "T",
        "selling":         "T",
        "image_url":       "",
        "seo": {
            "meta_title":       "스노윅 대나무캔들 200g 비자림숲속",
            "meta_author":      "스노윅 SNOWICK",
            "meta_description": "특허심지 터널링0% 대나무 소이캔들 200g 비자림숲속. 별모양우드심지 구조로 벽면까지 균일 연소. 스노윅.",
            "meta_keywords":    "대나무캔들,비자림숲속캔들,터널링없는캔들,소이캔들,스노윅",
        },
    },
    {
        "product_name":    "스노윅 대나무캔들 200g 동백꽃",
        "description":     f"{_CANDLE_BODY}\n\n오늘은 동백꽃 — 겨울 한가운데 피는 붉은 동백을 담았습니다.",
        "summary_description": "특허심지 터널링 0% 대나무 소이캔들 200g — 동백꽃",
        "tags":            ["동백꽃캔들", "동백꽃향캔들", "겨울캔들"] + _CANDLE_COMMON_TAGS,
        "price":           "19000",
        "display":         "T",
        "selling":         "T",
        "image_url":       "",
        "seo": {
            "meta_title":       "스노윅 대나무캔들 200g 동백꽃",
            "meta_author":      "스노윅 SNOWICK",
            "meta_description": "특허심지 터널링0% 대나무 소이캔들 200g 동백꽃. 별모양우드심지 구조로 벽면까지 균일 연소. 스노윅.",
            "meta_keywords":    "대나무캔들,동백꽃캔들,터널링없는캔들,소이캔들,스노윅",
        },
    },
    {
        "product_name":    "스노윅 대나무캔들 200g 매화꽃",
        "description":     f"{_CANDLE_BODY}\n\n오늘은 매화꽃 — 눈 녹기 전 가장 먼저 피는 봄을 담았습니다.",
        "summary_description": "특허심지 터널링 0% 대나무 소이캔들 200g — 매화꽃",
        "tags":            ["매화꽃캔들", "매화향캔들", "봄캔들"] + _CANDLE_COMMON_TAGS,
        "price":           "19000",
        "display":         "T",
        "selling":         "T",
        "image_url":       "",
        "seo": {
            "meta_title":       "스노윅 대나무캔들 200g 매화꽃",
            "meta_author":      "스노윅 SNOWICK",
            "meta_description": "특허심지 터널링0% 대나무 소이캔들 200g 매화꽃. 별모양우드심지 구조로 벽면까지 균일 연소. 스노윅.",
            "meta_keywords":    "대나무캔들,매화꽃캔들,터널링없는캔들,소이캔들,스노윅",
        },
    },
    {
        "product_name":    "스노윅 대나무캔들 200g 철쭉꽃",
        "description":     f"{_CANDLE_BODY}\n\n오늘은 철쭉꽃 — 능선을 물들이는 연분홍 봄을 담았습니다.",
        "summary_description": "특허심지 터널링 0% 대나무 소이캔들 200g — 철쭉꽃",
        "tags":            ["철쭉꽃캔들", "철쭉향캔들", "봄꽃캔들"] + _CANDLE_COMMON_TAGS,
        "price":           "19000",
        "display":         "T",
        "selling":         "T",
        "image_url":       "",
        "seo": {
            "meta_title":       "스노윅 대나무캔들 200g 철쭉꽃",
            "meta_author":      "스노윅 SNOWICK",
            "meta_description": "특허심지 터널링0% 대나무 소이캔들 200g 철쭉꽃. 별모양우드심지 구조로 벽면까지 균일 연소. 스노윅.",
            "meta_keywords":    "대나무캔들,철쭉꽃캔들,터널링없는캔들,소이캔들,스노윅",
        },
    },
    {
        "product_name":    "스노윅 대나무캔들 200g 한라봉",
        "description":     f"{_CANDLE_BODY}\n\n오늘은 한라봉 — 톡 터지는 제주 한라봉 향을 담았습니다.",
        "summary_description": "특허심지 터널링 0% 대나무 소이캔들 200g — 한라봉",
        "tags":            ["한라봉캔들", "한라봉향캔들", "시트러스캔들"] + _CANDLE_COMMON_TAGS,
        "price":           "19000",
        "display":         "T",
        "selling":         "T",
        "image_url":       "",
        "seo": {
            "meta_title":       "스노윅 대나무캔들 200g 한라봉",
            "meta_author":      "스노윅 SNOWICK",
            "meta_description": "특허심지 터널링0% 대나무 소이캔들 200g 한라봉. 별모양우드심지 구조로 벽면까지 균일 연소. 스노윅.",
            "meta_keywords":    "대나무캔들,한라봉캔들,터널링없는캔들,소이캔들,스노윅",
        },
    },
    {
        "product_name":    "스노윅 대나무캔들 200g 오리엔탈템플우디",
        "description":     f"{_CANDLE_BODY}\n\n오늘은 오리엔탈템플우디 — 오래된 사찰의 고요한 향을 담았습니다.",
        "summary_description": "특허심지 터널링 0% 대나무 소이캔들 200g — 오리엔탈템플우디",
        "tags":            ["오리엔탈캔들", "우디캔들", "사찰향캔들"] + _CANDLE_COMMON_TAGS,
        "price":           "19000",
        "display":         "T",
        "selling":         "T",
        "image_url":       "",
        "seo": {
            "meta_title":       "스노윅 대나무캔들 200g 오리엔탈템플우디",
            "meta_author":      "스노윅 SNOWICK",
            "meta_description": "특허심지 터널링0% 대나무 소이캔들 200g 오리엔탈템플우디. 별모양우드심지 구조로 벽면까지 균일 연소. 스노윅.",
            "meta_keywords":    "대나무캔들,오리엔탈캔들,우디캔들,터널링없는캔들,스노윅",
        },
    },
    {
        "product_name":    "스노윅 대나무캔들 200g 우디프레스티지",
        "description":     f"{_CANDLE_BODY}\n\n오늘은 우디프레스티지 — 가죽 서재에 스민 묵직한 향을 담았습니다.",
        "summary_description": "특허심지 터널링 0% 대나무 소이캔들 200g — 우디프레스티지",
        "tags":            ["우디프레스티지캔들", "고급캔들", "우디향캔들"] + _CANDLE_COMMON_TAGS,
        "price":           "19000",
        "display":         "T",
        "selling":         "T",
        "image_url":       "",
        "seo": {
            "meta_title":       "스노윅 대나무캔들 200g 우디프레스티지",
            "meta_author":      "스노윅 SNOWICK",
            "meta_description": "특허심지 터널링0% 대나무 소이캔들 200g 우디프레스티지. 별모양우드심지 구조로 벽면까지 균일 연소. 스노윅.",
            "meta_keywords":    "대나무캔들,우디프레스티지캔들,터널링없는캔들,소이캔들,스노윅",
        },
    },
    {
        "product_name":    "스노윅 대나무캔들 200g 레몬가든플뢰르",
        "description":     f"{_CANDLE_BODY}\n\n오늘은 레몬가든플뢰르 — 화사하다 차분해지는 두 얼굴의 향입니다.",
        "summary_description": "특허심지 터널링 0% 대나무 소이캔들 200g — 레몬가든플뢰르",
        "tags":            ["레몬가든캔들", "플뢰르캔들", "레몬향캔들"] + _CANDLE_COMMON_TAGS,
        "price":           "19000",
        "display":         "T",
        "selling":         "T",
        "image_url":       "",
        "seo": {
            "meta_title":       "스노윅 대나무캔들 200g 레몬가든플뢰르",
            "meta_author":      "스노윅 SNOWICK",
            "meta_description": "특허심지 터널링0% 대나무 소이캔들 200g 레몬가든플뢰르. 별모양우드심지 구조로 벽면까지 균일 연소. 스노윅.",
            "meta_keywords":    "대나무캔들,레몬가든캔들,터널링없는캔들,소이캔들,스노윅",
        },
    },
]

# ──────────────────────────────────────────────
# 부자재 상품 데이터
# ──────────────────────────────────────────────

MATERIAL_PRODUCTS = [
    {
        "product_name":       "SNOWICK 스노윅 스퀘어 블랙 퍼퓸용기 12ml 분사형 스프레이 휴대용",
        "eng_product_name":   "SNOWICK Square Black Perfume Bottle 12ml Spray",
        "custom_product_code": "스노윅 퍼퓸용기 스퀘어블랙 12ml",
        "description": (
            "스노윅 스퀘어 블랙 퍼퓸용기 12ml.\n\n"
            "미세분사 스프레이 타입으로 향수를 정밀하게 분사합니다.\n"
            "휴대가 간편한 12ml 슬림 스퀘어 디자인.\n"
            "향수 DIY·공방 소분·샘플 제작에 적합한 부자재입니다.\n\n"
            "[ 제품 사양 ]\n"
            "- 용량: 12ml\n"
            "- 색상: 블랙\n"
            "- 타입: 분사형 스프레이\n"
            "- 용도: 향수 DIY·공방·샘플 소분\n\n"
            "[ 주의사항 ]\n"
            "- 어린이 손에 닿지 않는 곳에 보관하세요.\n"
            "- 직사광선 및 고온 장소 보관 금지.\n"
            "- 눈·피부 직접 접촉 시 물로 세척하세요."
        ),
        "summary_description": "스노윅 스퀘어 블랙 퍼퓸용기 12ml. 미세분사 스프레이. 향수 DIY·공방·샘플 소분용 부자재.",
        "simple_description":  "간편한 휴대, 섬세한 분사. 스노윅 스퀘어 블랙 퍼퓸용기 12ml",
        "tags": [
            "퍼퓸용기", "퍼퓸용기12ml", "스노윅퍼퓸용기", "DIY퍼퓸용기",
            "향수용기", "스노윅부자재", "12ml퍼퓸용기", "스퀘어퍼퓸용기",
            "블랙퍼퓸용기", "분사형용기", "휴대용향수용기", "향수소분용기",
            "공방퍼퓸용기", "향수DIY용기", "미세분사용기", "스프레이용기",
            "향수부자재", "소분용기", "선물용향수용기", "퍼퓸소분용기",
        ],
        "price":          "2000",
        "tax_type":       "A",   # A=과세, B=면세, C=영세
        "stock_quantity": 999,
        "display":        "T",
        "selling":        "T",
        "image_url":      "https://ecimg.cafe24img.com/pg861b64307312015/snowick/web/product/big/20260623/temp_shop1_17821518032309.png",
        "promotion_phrase": "스노윅 스퀘어 블랙 퍼퓸용기 12ml 분사형 부자재",
        "seo": {
            "meta_title":       "스퀘어 블랙 퍼퓸용기 12ml 분사형 휴대용 — SNOWICK 스노윅",
            "meta_author":      "스노윅",
            "meta_description": "스노윅 스퀘어 블랙 퍼퓸용기 12ml. 미세분사 스프레이 타입. 향수 DIY·공방·샘플 소분 전용 부자재. 간편 휴대, 손쉬운 리필 구조.",
            "meta_keywords":    "퍼퓸용기,퍼퓸용기12ml,향수용기,DIY퍼퓸용기,스노윅퍼퓸용기,휴대용향수용기,스퀘어퍼퓸용기,향수소분용기,분사형용기,스노윅부자재",
        },
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
    data = {"grant_type": "refresh_token", "refresh_token": refresh_token}
    resp = requests.post(url, headers=headers, data=data)
    resp.raise_for_status()
    token_data = resp.json()
    set_key(ENV_FILE, "CAFE24_ACCESS_TOKEN",  token_data["access_token"])
    set_key(ENV_FILE, "CAFE24_REFRESH_TOKEN", token_data["refresh_token"])
    os.environ["CAFE24_ACCESS_TOKEN"]  = token_data["access_token"]
    os.environ["CAFE24_REFRESH_TOKEN"] = token_data["refresh_token"]
    print("토큰 갱신 완료")
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
        print(f"  API 오류 {resp.status_code}: {resp.text[:300]}")
        resp.raise_for_status()
    return resp.json()

# ──────────────────────────────────────────────
# 상품 등록 (범용)
# ──────────────────────────────────────────────

def register_product(product):
    tags = list(dict.fromkeys(product["tags"]))[:20]

    req = {
        "product_name":       product["product_name"],
        "description":        product.get("description", ""),
        "summary_description": product.get("summary_description", ""),
        "product_tag":        ",".join(tags),
        "display":            product.get("display", "T"),
        "selling":            product.get("selling", "T"),
        "origin_place_no":    1826,  # 대한민국
    }

    # 선택 필드 — 값이 있을 때만 포함
    if product.get("price"):
        req["price"] = product["price"]
    if product.get("tax_type"):
        req["tax_type"] = product["tax_type"]
    if product.get("eng_product_name"):
        req["eng_product_name"] = product["eng_product_name"]
    if product.get("custom_product_code"):
        req["custom_product_code"] = product["custom_product_code"]
    if product.get("simple_description"):
        req["simple_description"] = product["simple_description"]
    if product.get("promotion_phrase"):
        req["promotion_phrase"] = product["promotion_phrase"]

    result = api_call("post", "/products", {"request": req})
    product_no = result["product"]["product_no"]
    print(f"  상품 등록 완료 — product_no: {product_no}")

    # 재고 설정
    if product.get("stock_quantity") is not None:
        _set_stock(product_no, product["stock_quantity"])

    return product_no


def _set_stock(product_no, quantity):
    payload = {
        "request": {
            "stock_quantity": quantity,
            "stock_safety_quantity": 0,
        }
    }
    try:
        api_call("put", f"/products/{product_no}/variants/R", payload)
        print(f"  재고 설정 완료 — {quantity}개")
    except Exception as e:
        print(f"  재고 설정 실패 (수동 입력 필요): {e}")


def upload_image(product_no, image_url):
    if not image_url:
        print("  이미지 URL 없음 — 이미지 등록 생략")
        return
    payload = {
        "request": {
            "image_upload_type": "U",
            "detail_image": image_url,
            "list_image":   image_url,
            "tiny_image":   image_url,
            "small_image":  image_url,
        }
    }
    api_call("post", f"/products/{product_no}/images", payload)
    print("  이미지 등록 완료")


def set_seo(product_no, product):
    seo = product.get("seo")
    if not seo:
        return
    api_call("put", f"/products/{product_no}/seo", {"request": seo})
    print("  SEO 설정 완료")

# ──────────────────────────────────────────────
# 실행 묶음
# ──────────────────────────────────────────────

def run_products(products, label):
    print(f"\n스노윅 {label} {len(products)}종 Cafe24 자동 등록 시작\n")
    results = []
    for i, product in enumerate(products, 1):
        name = product["product_name"]
        print(f"[{i}/{len(products)}] {name}")
        try:
            product_no = register_product(product)
            upload_image(product_no, product.get("image_url", ""))
            set_seo(product_no, product)
            results.append({"name": name, "product_no": product_no, "status": "성공"})
        except Exception as e:
            print(f"  실패: {e}")
            results.append({"name": name, "product_no": None, "status": f"실패: {e}"})
        time.sleep(0.5)

    print("\n──────────────────────────────────────")
    print(f"등록 결과 — {label}")
    print("──────────────────────────────────────")
    for r in results:
        tag = "OK" if r["status"] == "성공" else "NG"
        print(f"  [{tag}] product_no={r['product_no']} | {r['name'][:40]} | {r['status']}")
    success = sum(1 for r in results if r["status"] == "성공")
    print(f"\n총 {len(products)}종 중 {success}종 성공\n")
    return results


def main():
    if not CLIENT_ID or not CLIENT_SECRET:
        print("script/.env 파일에 CAFE24_CLIENT_ID / CAFE24_CLIENT_SECRET을 입력하세요.")
        return
    if not get_access_token():
        print("CAFE24_ACCESS_TOKEN이 없습니다. python script/cafe24_auth.py를 먼저 실행하세요.")
        return

    args = sys.argv[1:]
    if "--all" in args:
        run_products(CANDLE_PRODUCTS, "캔들")
        run_products(MATERIAL_PRODUCTS, "부자재")
    elif "--material" in args:
        run_products(MATERIAL_PRODUCTS, "부자재")
    else:
        run_products(CANDLE_PRODUCTS, "캔들")


if __name__ == "__main__":
    main()
