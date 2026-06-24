# -*- coding: utf-8 -*-
"""
SNOWICK 부자재 Cafe24 등록 전용 스크립트
대상: 퍼퓸용기 / 캔들용기 / 디퓨저용기
실행: python script/register_material.py
"""

import os
import sys
import json
import base64
import requests
from dotenv import load_dotenv, set_key

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

ENV_FILE = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(ENV_FILE)

# ─────────────────────────────────────────────
# 고정값
# ─────────────────────────────────────────────
MALL_ID       = "snowick"
SUPPLIER_NAME = "스노윅"
MANUFACTURER  = "스노윅"
META_AUTHOR   = "스노윅"
ORIGIN_CODE   = "CHN"
ORIGIN_VALUE  = "중국산"

CLIENT_ID     = os.getenv("CAFE24_CLIENT_ID")
CLIENT_SECRET = os.getenv("CAFE24_CLIENT_SECRET")
API_BASE      = f"https://{MALL_ID}.cafe24api.com/api/v2/admin"
API_VERSION   = "2026-03-01"


# ─────────────────────────────────────────────
# 토큰
# ─────────────────────────────────────────────
def get_headers():
    token = os.getenv("CAFE24_ACCESS_TOKEN")
    if not token:
        print("[ERROR] CAFE24_ACCESS_TOKEN 없음. cafe24_auth.py 먼저 실행하세요.")
        sys.exit(1)
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Cafe24-Api-Version": API_VERSION,
    }


def refresh_token():
    refresh = os.getenv("CAFE24_REFRESH_TOKEN")
    if not refresh:
        print("[ERROR] CAFE24_REFRESH_TOKEN 없음. cafe24_auth.py 먼저 실행하세요.")
        sys.exit(1)
    cred = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    resp = requests.post(
        f"https://{MALL_ID}.cafe24api.com/api/v2/oauth/token",
        headers={"Authorization": f"Basic {cred}", "Content-Type": "application/x-www-form-urlencoded"},
        data={"grant_type": "refresh_token", "refresh_token": refresh},
    )
    if resp.status_code == 200:
        t = resp.json()
        set_key(ENV_FILE, "CAFE24_ACCESS_TOKEN", t["access_token"])
        set_key(ENV_FILE, "CAFE24_REFRESH_TOKEN", t["refresh_token"])
        os.environ["CAFE24_ACCESS_TOKEN"] = t["access_token"]
        os.environ["CAFE24_REFRESH_TOKEN"] = t["refresh_token"]
        print("[OK] 토큰 갱신 완료")
    else:
        print(f"[ERROR] 토큰 갱신 실패: {resp.text[:200]}")
        sys.exit(1)


def check_token():
    resp = requests.get(f"{API_BASE}/products/399", headers=get_headers())
    if resp.status_code == 401:
        print("[INFO] 토큰 만료 -- 자동 갱신 중...")
        refresh_token()
    elif resp.status_code in (200, 404):
        print("[OK] 토큰 유효")
    else:
        print(f"[WARN] 토큰 확인 응답: {resp.status_code}")


# ─────────────────────────────────────────────
# 입력 수집
# ─────────────────────────────────────────────
def collect_inputs():
    print("\n" + "=" * 60)
    print("  SNOWICK 부자재 Cafe24 등록")
    print("=" * 60)
    print(f"  [고정값] 공급사: {SUPPLIER_NAME} / 제조사: {MANUFACTURER} / 원산지: {ORIGIN_VALUE}")
    print("=" * 60)

    def ask(label, required=True):
        while True:
            val = input(f"  {label}: ").strip()
            if val or not required:
                return val
            print(f"  [필수] {label}을(를) 입력하세요.")

    d = {}
    d["product_name"]             = ask("상품명(한글)")
    d["eng_product_name"]         = ask("영문상품명")
    d["custom_product_code"]      = ask("관리용상품명")
    d["model_name"]               = ask("모델명", required=False)
    d["price"]                    = ask("판매가(숫자)")
    d["summary_description"]      = ask("요약설명(255자 이내)")
    d["simple_description"]       = ask("간략설명")
    d["nav_shopping_description"] = ask("네이버쇼핑추가홍보문구(50자 이내)")
    d["seo_title"]                = ask("브라우저타이틀")
    d["seo_description"]          = ask("메타태그 Description")
    d["seo_keywords"]             = ask("메타태그 Keywords(콤마 구분, 10개)")
    d["search_keywords_raw"]      = ask("검색어(콤마 구분, 20개)")
    d["main_image_url"]           = ask("대표이미지URL")
    d["detail_image_url1"]        = ask("상세이미지URL1")
    d["detail_image_url2"]        = ask("상세이미지URL2", required=False)
    d["detail_image_url3"]        = ask("상세이미지URL3", required=False)
    d["alt1"]                     = ask("이미지ALT1")
    d["alt2"]                     = ask("이미지ALT2", required=False)
    d["alt3"]                     = ask("이미지ALT3", required=False)

    d["search_keywords"] = [k.strip() for k in d["search_keywords_raw"].split(",") if k.strip()][:20]
    return d


# ─────────────────────────────────────────────
# 상세설명 HTML 자동 생성
# ─────────────────────────────────────────────
def build_detail_html(d):
    def img(url, alt):
        return f'<img src="{url}" alt="{alt or ""}" style="max-width:100%;display:block;margin:0 auto;">'

    parts = []
    if d["detail_image_url1"]:
        parts.append(img(d["detail_image_url1"], d["alt1"]))
    if d["detail_image_url2"]:
        parts.append(img(d["detail_image_url2"], d["alt2"]))
    if d["detail_image_url3"]:
        parts.append(img(d["detail_image_url3"], d["alt3"]))
    return '<div style="text-align:center;">' + "".join(parts) + "</div>"


# ─────────────────────────────────────────────
# 입력값 확인 출력
# ─────────────────────────────────────────────
def preview(d):
    print("\n" + "-" * 60)
    print("  [등록 예정 데이터 확인]")
    print("-" * 60)
    fields = [
        ("상품명",             d["product_name"]),
        ("영문상품명",         d["eng_product_name"]),
        ("관리용상품명",       d["custom_product_code"]),
        ("공급사상품명",       SUPPLIER_NAME),
        ("제조사",             MANUFACTURER),
        ("모델명",             d["model_name"] or "(없음)"),
        ("원산지",             ORIGIN_VALUE),
        ("판매가",             f"{d['price']}원"),
        ("요약설명",           d["summary_description"]),
        ("간략설명",           d["simple_description"]),
        ("네이버홍보문구",     d["nav_shopping_description"]),
        ("브라우저타이틀",     d["seo_title"]),
        ("Author",             META_AUTHOR),
        ("Meta Description",   d["seo_description"]),
        ("Meta Keywords",      d["seo_keywords"]),
        ("검색어",             f"{len(d['search_keywords'])}개 -- {', '.join(d['search_keywords'])}"),
        ("대표이미지URL",      d["main_image_url"]),
        ("상세이미지URL1",     d["detail_image_url1"]),
        ("상세이미지URL2",     d["detail_image_url2"] or "(없음)"),
        ("상세이미지URL3",     d["detail_image_url3"] or "(없음)"),
        ("ALT1",               d["alt1"]),
        ("ALT2",               d["alt2"] or "(없음)"),
        ("ALT3",               d["alt3"] or "(없음)"),
    ]
    for label, val in fields:
        print(f"  {label:20s}: {val}")
    print("-" * 60)


# ─────────────────────────────────────────────
# Cafe24 API 등록
# ─────────────────────────────────────────────
def register(d):
    print("\n[INFO] Cafe24 API 등록 시작...")

    # 1. 상품 등록
    payload = {
        "request": {
            "product_name":          d["product_name"],
            "eng_product_name":      d["eng_product_name"],
            "custom_product_code":   d["custom_product_code"],
            "supplier_product_name": SUPPLIER_NAME,
            "manufacturer_name":     MANUFACTURER,
            "origin_place_code":     ORIGIN_CODE,
            "price":                 d["price"],
            "supply_price":          "0",
            "display":               "T",
            "selling":               "T",
            "summary_description":   d["summary_description"],
            "simple_description":    d["simple_description"],
            "description":           build_detail_html(d),
            "product_tag":           d["search_keywords"],
            "market_sync":           "T",
        }
    }
    if d["model_name"]:
        payload["request"]["model_name"] = d["model_name"]

    r = requests.post(f"{API_BASE}/products", headers=get_headers(), json=payload)
    if r.status_code == 401:
        refresh_token()
        r = requests.post(f"{API_BASE}/products", headers=get_headers(), json=payload)
    if r.status_code != 201:
        print(f"[ERROR] 상품 등록 실패 {r.status_code}: {r.text[:300]}")
        sys.exit(1)

    pno = r.json()["product"]["product_no"]
    post_market = r.json()["product"].get("market_sync")
    print(f"[1/5] 상품 등록 완료 -- product_no: {pno} / market_sync(POST): {post_market}")

    # 1-1. market_sync PUT 보정 (POST에서 미반영 시 대비)
    r_ms = requests.put(f"{API_BASE}/products/{pno}", headers=get_headers(), json={
        "request": {"market_sync": "T"}
    })
    # GET으로 실제 반영 여부 검증
    r_chk = requests.get(f"{API_BASE}/products/{pno}", headers=get_headers())
    ms_actual = r_chk.json().get("product", {}).get("market_sync")
    print(f"[1-1] market_sync 적용 -- PUT:{r_ms.status_code} / 실제값:{ms_actual}")

    # 2. SEO
    r2 = requests.put(f"{API_BASE}/products/{pno}/seo", headers=get_headers(), json={
        "request": {
            "meta_title":       d["seo_title"],
            "meta_author":      META_AUTHOR,
            "meta_description": d["seo_description"],
            "meta_keyword":     d["seo_keywords"],
        }
    })
    print(f"[2/5] SEO 설정 -- {r2.status_code}")

    # 3. 네이버 홍보문구
    r3 = requests.put(f"{API_BASE}/products/{pno}", headers=get_headers(), json={
        "request": {"naverpay_product_name": d["nav_shopping_description"]}
    })
    print(f"[3/5] 네이버 홍보문구 -- {r3.status_code}")

    # 4. 대표이미지 (base64)
    try:
        img_bytes = requests.get(d["main_image_url"], timeout=15).content
        img_b64 = base64.b64encode(img_bytes).decode()
        r4 = requests.post(f"{API_BASE}/products/{pno}/images", headers=get_headers(), json={
            "request": {
                "image_upload_type": "B",
                "detail_image": img_b64,
                "list_image":   img_b64,
                "tiny_image":   img_b64,
                "small_image":  img_b64,
            }
        })
        img_url = r4.json().get("image", {}).get("detail_image", "(없음)")
        print(f"[4/5] 이미지 업로드 -- {r4.status_code}")
        print(f"       CDN: {img_url}")
    except Exception as e:
        print(f"[WARN] 이미지 업로드 실패: {e}")

    print("\n" + "=" * 60)
    print(f"  [등록 완료] product_no: {pno}")
    print(f"  상품명: {d['product_name']}")
    print(f"  URL: https://snowick.cafe24.com/product/detail.html?product_no={pno}")
    print("=" * 60)


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    check_token()
    data = collect_inputs()
    preview(data)

    confirm = input("\n  등록하시겠습니까? (y/n): ").strip().lower()
    if confirm == "y":
        register(data)
    else:
        print("\n  등록 취소.")


if __name__ == "__main__":
    main()
