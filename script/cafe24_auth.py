"""
Cafe24 OAuth 최초 인증 스크립트
최초 1회 실행 -> access_token / refresh_token 발급 -> .env에 저장
이후에는 cafe24_register.py가 자동으로 토큰을 갱신합니다.

사용법:
  python cafe24_auth.py
"""

import os
import sys
import base64
import webbrowser
import urllib.parse
import requests
from dotenv import load_dotenv, set_key

load_dotenv()

MALL_ID       = os.getenv("CAFE24_MALL_ID", "snowick")
CLIENT_ID     = os.getenv("CAFE24_CLIENT_ID")
CLIENT_SECRET = os.getenv("CAFE24_CLIENT_SECRET")
# 카페24 개발자센터 앱에 등록된 HTTPS redirect URI와 동일해야 합니다.
REDIRECT_URI  = "https://snowick.cafe24.com/"
SCOPE         = "mall.read_application,mall.write_application,mall.read_product,mall.write_product"
ENV_FILE      = os.path.join(os.path.dirname(__file__), "..", ".env")


def get_auth_url():
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "state": "snowick_auth",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
    }
    base = f"https://{MALL_ID}.cafe24api.com/api/v2/oauth/authorize"
    return base + "?" + urllib.parse.urlencode(params)


def exchange_code_for_token(code):
    url = f"https://{MALL_ID}.cafe24api.com/api/v2/oauth/token"
    credentials = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    headers = {
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    resp = requests.post(url, headers=headers, data=data)
    resp.raise_for_status()
    return resp.json()


def save_tokens(token_data):
    set_key(ENV_FILE, "CAFE24_ACCESS_TOKEN",  token_data["access_token"])
    set_key(ENV_FILE, "CAFE24_REFRESH_TOKEN", token_data["refresh_token"])
    print("[OK] .env에 토큰이 저장됐습니다.")
    print(f"   access_token  : {token_data['access_token'][:20]}...")
    print(f"   expires_in    : {token_data.get('expires_in')}초")


def main():
    if not CLIENT_ID or not CLIENT_SECRET:
        print("[ERROR] .env 파일에 CAFE24_CLIENT_ID / CAFE24_CLIENT_SECRET을 먼저 입력하세요.")
        return

    auth_url = get_auth_url()
    print("\n[STEP 1] 아래 URL을 브라우저에서 열어 로그인 후 '허가' 버튼을 누르세요.")
    print(f"\n  {auth_url}\n")
    webbrowser.open(auth_url)

    print("[STEP 2] 허가 후 브라우저 주소창에 표시된 URL을 복사해 붙여넣으세요.")
    print("  (예: https://snowick.cafe24.com/oauth/callback?code=XXXX&state=...)")
    print()

    redirected_url = input("  리디렉션된 URL 붙여넣기: ").strip()

    parsed = urllib.parse.urlparse(redirected_url)
    params = urllib.parse.parse_qs(parsed.query)

    if "code" not in params:
        # code만 직접 입력했을 경우도 처리
        if len(redirected_url) > 10 and "?" not in redirected_url:
            code = redirected_url
        else:
            print("[ERROR] URL에서 code 파라미터를 찾을 수 없습니다.")
            return
    else:
        code = params["code"][0]

    print(f"\n[INFO] code 확인: {code[:10]}...")
    print("[INFO] 토큰 발급 중...")

    token_data = exchange_code_for_token(code)
    save_tokens(token_data)
    print("\n[OK] 인증 완료. 이제 cafe24_register.py를 실행할 수 있습니다.")


if __name__ == "__main__":
    main()
