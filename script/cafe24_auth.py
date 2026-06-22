"""
Cafe24 OAuth 최초 인증 스크립트
최초 1회 실행 → access_token / refresh_token 발급 → .env에 저장
이후에는 cafe24_register.py가 자동으로 토큰을 갱신합니다.

사용법:
  python cafe24_auth.py
"""

import os
import json
import base64
import webbrowser
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
from dotenv import load_dotenv, set_key

load_dotenv()

MALL_ID       = os.getenv("CAFE24_MALL_ID", "snowick")
CLIENT_ID     = os.getenv("CAFE24_CLIENT_ID")
CLIENT_SECRET = os.getenv("CAFE24_CLIENT_SECRET")
REDIRECT_URI  = "http://localhost:3000/callback"
SCOPE         = "mall.read_product,mall.write_product,mall.read_category"
ENV_FILE      = os.path.join(os.path.dirname(__file__), ".env")

auth_code_holder = {}


class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        if "code" in params:
            auth_code_holder["code"] = params["code"][0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"<h2>인증 완료. 이 창을 닫아도 됩니다.</h2>")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"<h2>인증 코드를 받지 못했습니다.</h2>")

    def log_message(self, format, *args):
        pass


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
    print("✅ .env에 토큰이 저장됐습니다.")
    print(f"   access_token  : {token_data['access_token'][:20]}...")
    print(f"   expires_in    : {token_data.get('expires_in')}초")


def main():
    if not CLIENT_ID or not CLIENT_SECRET:
        print("❌ .env 파일에 CAFE24_CLIENT_ID / CAFE24_CLIENT_SECRET을 먼저 입력하세요.")
        return

    auth_url = get_auth_url()
    print(f"\n🔗 브라우저가 열립니다. 로그인 후 '허가' 버튼을 누르세요.")
    print(f"   {auth_url}\n")
    webbrowser.open(auth_url)

    server = HTTPServer(("localhost", 3000), CallbackHandler)
    print("⏳ 인증 대기 중... (브라우저에서 허가 완료 후 자동 진행)")
    server.handle_request()

    code = auth_code_holder.get("code")
    if not code:
        print("❌ 인증 코드를 받지 못했습니다.")
        return

    print("🔄 토큰 발급 중...")
    token_data = exchange_code_for_token(code)
    save_tokens(token_data)
    print("\n✅ 인증 완료. 이제 cafe24_register.py를 실행할 수 있습니다.")


if __name__ == "__main__":
    main()
