# -*- coding: utf-8 -*-
"""
SNOWICK SEO Generate Script
기준: SNOWICK_PREFERENCES_MASTER V4 FINAL
확정본: 2026-06-14
실행: python script/seo_generate.py
"""

# ─────────────────────────────────────────────
# 고정값
# ─────────────────────────────────────────────
AUTHOR_FIXED = "스노윅"
SUPPLIER_FIXED = "스노윅"
BRAND_CAFE24 = "SNOWICK"

PERFUME_TYPE_KO = "오드뚜왈렛 퍼퓸"
PERFUME_TYPE_EN = "Eau de Toilette Parfum"
PERFUME_VOL = "30ml"

META_DESC_MIN = 80
META_DESC_MAX = 150

FORBIDDEN_WORDS = ["우드윅", "Eau de Parfum", "명품", "│"]

# ─────────────────────────────────────────────
# 부자재 규격 고정값
# ─────────────────────────────────────────────
FIXED_SPECS = {
    "왁스_실크소이":      ["1kg"],
    "왁스_비즈화이트":    ["1kg"],
    "왁스_비즈옐로우":    ["1kg"],
    "스톤_샤쉐":          ["500g", "1kg"],
    "스톤_레진":          ["500g", "1kg"],
    "베이스_디퓨저":      ["500ml", "1L"],
    "베이스_오드뚜왈렛":  ["500ml", "1L"],
    "베이스_섬유탈취":    ["500ml", "1L"],
    "스틱_블랙":          ["3mm*30cm", "4mm*30cm", "4mm*40cm", "5mm*60cm"],
    "스틱_화이트":        ["3mm*30cm", "4mm*30cm", "4mm*40cm", "5mm*60cm"],
    "스틱_브라운":        ["3mm*30cm", "4mm*30cm", "4mm*40cm", "5mm*60cm"],
}

NORMAL_SPECS = ["캔들용기", "디퓨저용기", "퍼퓸용기"]

MATERIAL_MAP = {
    "캔들용기":          ("06_부자재/캔들용기",               "캔들용기",              "캔들"),
    "디퓨저용기":        ("06_부자재/디퓨저용기",             "디퓨저용기",            "디퓨저"),
    "퍼퓸용기":          ("06_부자재/퍼퓸용기",               "퍼퓸용기",              "퍼퓸"),
    "스틱_블랙":         ("06_부자재/스틱/스틱_블랙",         "고밀도 디퓨저 스틱 블랙",   "스틱"),
    "스틱_화이트":       ("06_부자재/스틱/스틱_화이트",       "고밀도 디퓨저 스틱 화이트", "스틱"),
    "스틱_브라운":       ("06_부자재/스틱/스틱_브라운",       "고밀도 디퓨저 스틱 브라운", "스틱"),
    "베이스_디퓨저":     ("06_부자재/베이스/베이스_디퓨저",     "디퓨저 베이스",       "베이스"),
    "베이스_오드뚜왈렛": ("06_부자재/베이스/베이스_오드뚜왈렛", "오드뚜왈렛 베이스",   "베이스"),
    "베이스_섬유탈취":   ("06_부자재/베이스/베이스_섬유탈취",   "섬유탈취 베이스",     "베이스"),
    "왁스_실크소이":     ("06_부자재/왁스/왁스_실크소이",   "실크소이왁스",          "왁스"),
    "왁스_비즈화이트":   ("06_부자재/왁스/왁스_비즈화이트", "비즈 화이트왁스",       "왁스"),
    "왁스_비즈옐로우":   ("06_부자재/왁스/왁스_비즈옐로우", "비정제 비즈 옐로우왁스","왁스"),
    "스톤_샤쉐":         ("06_부자재/스톤/스톤_샤쉐",   "샤쉐스톤",              "스톤"),
    "스톤_레진":         ("06_부자재/스톤/스톤_레진",   "레진스톤",              "스톤"),
}

KW_BASE = {
    "캔들":  ["캔들용기", "유리캔들용기", "캔들만들기용기", "DIY캔들용기", "캔들제작용기",
              "소이캔들용기", "원형캔들용기", "향캔들용기", "인테리어캔들용기", "수제캔들용기"],
    "디퓨저":["디퓨저용기", "디퓨저병", "유리디퓨저병", "DIY디퓨저용기", "룸디퓨저용기",
              "디퓨저제작용기", "향디퓨저용기", "인테리어디퓨저용기", "디퓨저만들기용기", "확산용기"],
    "퍼퓸":  ["퍼퓸용기", "향수병", "소용량향수병", "DIY향수병", "퍼퓸제작용기",
              "스프레이향수병", "유리향수병", "향수만들기용기", "30ml향수병", "퍼퓸만들기"],
    "스틱":  ["디퓨저스틱", "고밀도스틱", "확산스틱", "룸디퓨저스틱", "DIY디퓨저스틱",
              "향스틱", "디퓨저리드스틱", "모세관스틱", "우드스틱디퓨저", "스틱디퓨저재료"],
    "베이스":["디퓨저베이스", "향료베이스", "퍼퓸베이스", "섬유탈취베이스", "DIY베이스",
              "향수베이스", "캐리어베이스", "무향베이스", "향만들기재료", "베이스오일"],
    "왁스":  ["소이왁스", "캔들왁스", "천연왁스", "DIY캔들왁스", "캔들만들기왁스",
              "수제캔들왁스", "비즈왁스", "코코넛왁스대안", "천연왁스캔들", "캔들재료왁스"],
    "스톤":  ["디퓨저스톤", "샤쉐스톤", "레진스톤", "향스톤", "방향스톤",
              "DIY향스톤", "인테리어스톤", "아로마스톤", "드라이플라워스톤", "향기스톤"],
}

FILL_SUFFIX = " 스노윅 공식 제품입니다."

def fix_meta_desc(text: str) -> str:
    text = text.strip()
    if len(text) > META_DESC_MAX:
        sentences = text.split(".")
        compressed = ""
        for s in sentences:
            candidate = (compressed + s + ".").strip()
            if len(candidate) <= META_DESC_MAX:
                compressed = candidate
            else:
                break
        text = compressed if compressed else text[:META_DESC_MAX]
    if len(text) < META_DESC_MIN:
        text = text.rstrip(".") + FILL_SUFFIX
    return text

def check_forbidden(text: str) -> list:
    hits = [w for w in FORBIDDEN_WORDS if w in text]
    return [f"[경고] 금지어 포함: {hits}"] if hits else []

def char_count(text: str) -> str:
    return f"{text}  ({len(text)}자)"

def fmt_price(price: str) -> str:
    try:
        return f"{int(price):,}원"
    except:
        return price

def detect_type(raw: str) -> dict:
    parts = [p.strip() for p in raw.strip().split("/")]
    if len(parts) < 2:
        return {"error": f"입력 형식 오류: '{raw}'"}
    if "캔들" in parts:
        idx = parts.index("캔들")
        return {"type": "캔들", "scent": parts[0],
                "vol": parts[idx+1] if idx+1 < len(parts) else "",
                "price": parts[idx+2] if idx+2 < len(parts) else ""}
    if "퍼퓸" in parts:
        idx = parts.index("퍼퓸")
        return {"type": "퍼퓸", "scent": parts[0], "vol": PERFUME_VOL,
                "price": parts[idx+1] if idx+1 < len(parts) else ""}
    if "디퓨저" in parts:
        idx = parts.index("디퓨저")
        return {"type": "디퓨저", "scent": parts[0],
                "vol": parts[idx+1] if idx+1 < len(parts) else "",
                "price": parts[idx+2] if idx+2 < len(parts) else ""}
    if "스타윅" in parts:
        idx = parts.index("스타윅")
        return {"type": "스타윅",
                "diameter": parts[idx+1] if idx+1 < len(parts) else "",
                "price": parts[idx+2] if idx+2 < len(parts) else ""}
    if "오일" in parts:
        idx = parts.index("오일")
        return {"type": "오일", "scent": parts[0],
                "vol": parts[idx+1] if idx+1 < len(parts) else "",
                "price": parts[idx+2] if idx+2 < len(parts) else ""}
    key = parts[0]
    if key in MATERIAL_MAP:
        if key in FIXED_SPECS:
            valid = FIXED_SPECS[key]
            spec  = parts[1] if len(parts) > 1 else ""
            price = parts[2] if len(parts) > 2 else ""
            if spec not in valid:
                return {"error": f"'{key}' 규격 오류: '{spec}'\n  허용값: {', '.join(valid)}"}
            return {"type": "부자재", "key": key, "spec": spec, "price": price}
        if key in NORMAL_SPECS:
            item_name = parts[1] if len(parts) > 1 else ""
            vol       = parts[2] if len(parts) > 2 else ""
            price     = parts[3] if len(parts) > 3 else ""
            return {"type": "부자재", "key": key,
                    "spec": f"{item_name} {vol}".strip(), "price": price}
    return {"error": f"타입 판별 불가: '{raw}'\n  부자재 키: {', '.join(MATERIAL_MAP.keys())}"}

def _result(names, summary, brief, keywords, promo_naver, promo_daum,
            browser_title, meta_desc, meta_keywords, alt_texts, detail_copy, price=""):
    return {
        "names": names, "summary": summary, "brief": brief,
        "keywords": keywords, "promo_naver": promo_naver, "promo_daum": promo_daum,
        "browser_title": browser_title, "author": AUTHOR_FIXED,
        "meta_desc": meta_desc, "meta_keywords": meta_keywords,
        "alt_texts": alt_texts, "detail_copy": detail_copy,
        "price": price,
        "_warnings": check_forbidden(names["cafe24"] + meta_desc),
    }

def generate_candle(info: dict) -> dict:
    scent = info["scent"]
    vol   = info["vol"]
    names = {
        "cafe24":   f"스노윅 시그니처 대나무 캔들 {scent} 향 {vol} 별모양심지 터널링0% 천연왁스",
        "en":       f"SNOWICK {scent} Bamboo Scented Candle {vol} Star Wick Natural Wax",
        "admin":    f"스노윅 시그니처 대나무 {scent} 캔들 {vol}",
        "supplier": SUPPLIER_FIXED,
    }
    summary = (f"대나무 용기에 담은 터널링 0% 별모양 우드심지 {scent} 향 캔들 {vol}. "
               f"특허받은 STAR WICK SYSTEM으로 완전한 멜트풀과 크랙클링 사운드를 구현합니다.")
    brief   = f"터지는 불꽃 소리, 터널링 없는 완전한 연소. 스노윅 대나무 {scent} 캔들"
    keywords = {
        "cafe24": [f"{scent}캔들","대나무캔들","별모양심지캔들","터널링없는캔들","천연왁스캔들",
                   "크랙클링캔들","우드심지캔들","멜트풀캔들","향캔들","인테리어캔들",
                   "스노윅캔들","SNOWICK캔들",f"{vol}캔들","별모양우드심지",
                   "연소안정성캔들","STARWICK","특허캔들",f"{scent}향캔들","선물용캔들","홈캔들"],
        "coupang":[f"{scent}캔들","대나무 캔들","별모양심지 캔들","터널링없는 캔들","천연왁스 캔들",
                   "크랙클링 캔들","우드심지 캔들","멜트풀 캔들","향캔들",
                   "스노윅 캔들",f"{vol} 캔들","별모양 우드심지","연소안정성 캔들",
                   "특허 캔들",f"{scent}향 캔들","선물 캔들","인테리어 캔들","홈 캔들","소이캔들","수제캔들"],
        "naver":  [f"{scent}캔들","대나무캔들","별모양심지캔들","터널링없는캔들","크랙클링캔들",
                   "우드심지캔들","스노윅",f"{vol}캔들","천연왁스캔들","특허캔들"],
    }
    promo_naver   = f"터널링 0% 별모양 우드심지 대나무 {scent} 향 캔들 {vol}"[:50]
    promo_daum    = (f"스노윅 시그니처 대나무 {scent} 캔들 {vol}. 특허받은 별모양 우드심지 STAR WICK SYSTEM으로 "
                     f"터널링 없는 완전 연소, 안정적인 멜트풀, 크랙클링 사운드를 경험하세요. "
                     f"용기별 커스텀 심지 설계로 반복 재현성을 보장합니다.")[:200]
    browser_title = f"대나무 {scent} 향 캔들 {vol} 별모양심지 터널링0% | SNOWICK 스노윅"
    meta_desc     = fix_meta_desc(f"스노윅 시그니처 대나무 {scent} 향 캔들 {vol}. 특허받은 별모양 우드심지로 터널링 없는 완전한 멜트풀과 크랙클링 사운드를 구현합니다. 반복 재현성 보장 연소 설계.")
    meta_keywords = [f"{scent}캔들","대나무캔들","별모양심지","터널링없는캔들","크랙클링캔들","우드심지캔들","스노윅","SNOWICK","멜트풀","향캔들"]
    alt_texts     = [f"스노윅 시그니처 대나무 {scent} 향 캔들 {vol} 별모양 우드심지",f"SNOWICK 대나무 {scent} 캔들 터널링 0% 멜트풀",f"스노윅 별모양심지 대나무 캔들 크랙클링 {scent} {vol}"]
    detail_copy   = {
        "01_설득":        "캔들이 다 타기도 전에 터널링으로 버린 적 있으신가요?",
        "02_구조":        "별모양 우드심지 STAR WICK SYSTEM — 특허받은 연소 구조로 터널링 0%, 완전한 멜트풀을 만듭니다.",
        "03_Why_SNOWICK": f"일반 심지는 중심만 녹입니다. 스노윅 별모양 우드심지는 용기 전면을 균일하게 녹여 {scent} 향을 공간으로 확산시킵니다.",
        "04_상세_메인":   f"대나무 {scent} 향 캔들 {vol} — 불꽃, 사운드, 향 확산까지 설계된 연소 경험.",
        "05_상세_구조":   "별모양심지 / 커스텀 심지클립 / 용기별 최적 설계 / 터널링 0% 보장",
        "06_구매유도":    f"스노윅 시그니처 대나무 {scent} 캔들 {vol}. 한 번 켜면 기억됩니다.",
    }
    return _result(names, summary, brief, keywords, promo_naver, promo_daum,
                   browser_title, meta_desc, meta_keywords, alt_texts, detail_copy, info.get("price",""))

def generate_perfume(info: dict) -> dict:
    scent = info["scent"]
    vol   = PERFUME_VOL
    names = {
        "cafe24":   f"SNOWICK 스노윅 {scent} {PERFUME_TYPE_KO} {vol}",
        "en":       f"SNOWICK {scent} {PERFUME_TYPE_EN} {vol}",
        "admin":    f"스노윅 {scent} 퍼퓸 {vol}",
        "supplier": SUPPLIER_FIXED,
    }
    summary = f"스노윅 {scent} 오드뚜왈렛 퍼퓸 {vol}. 향 라인 상표등록 완료."
    brief   = f"{scent}의 향, 그대로 담은 스노윅 퍼퓸 {vol}"
    keywords = {
        "cafe24": [f"{scent}퍼퓸",f"{scent}향수","오드뚜왈렛","스노윅퍼퓸","SNOWICk퍼퓸",
                   f"{vol}퍼퓸","국산퍼퓸","향수선물",f"{scent}오드뚜왈렛","향수30ml",
                   "소용량향수","여성향수","남녀공용향수","은은한향수","잔향향수",
                   "스노윅향수",f"{scent}향","가벼운향수","데일리향수","프리미엄향수"],
        "coupang":[f"{scent} 퍼퓸",f"{scent} 향수","오드뚜왈렛","스노윅 퍼퓸",
                   f"{vol} 향수","국산 퍼퓸","향수 선물",f"{scent} 오드뚜왈렛",
                   "소용량 향수","은은한 향수","잔향 향수","스노윅 향수","데일리 향수",
                   "가벼운 향수","프리미엄 국산향수","남녀공용 향수","여성 향수","향수 30ml","트왈렛 향수","향수 추천"],
        "naver":  [f"{scent}퍼퓸","오드뚜왈렛","스노윅퍼퓸",f"{vol}향수","국산퍼퓸",
                   "향수선물",f"{scent}향수","은은한향수","데일리향수","소용량향수"],
    }
    promo_naver   = f"{scent} 오드뚜왈렛 퍼퓸 {vol} 스노윅 향 라인"[:50]
    promo_daum    = (f"스노윅 {scent} 오드뚜왈렛 퍼퓸 {vol}. 스노윅 향 라인 상표등록 완료 제품. 가볍고 은은한 잔향. 데일리 향수로 추천합니다.")[:200]
    browser_title = f"{scent} 오드뚜왈렛 퍼퓸 {vol} | SNOWICK 스노윅"
    meta_desc     = fix_meta_desc(f"스노윅 {scent} 오드뚜왈렛 퍼퓸 {vol}. 향 라인 상표등록 완료. 은은하고 가벼운 잔향의 데일리 향수.")
    meta_keywords = [f"{scent}퍼퓸","오드뚜왈렛","스노윅퍼퓸",f"{vol}향수","국산퍼퓸","은은한향수","데일리향수","잔향향수","스노윅","SNOWICK"]
    alt_texts     = [f"스노윅 {scent} 오드뚜왈렛 퍼퓸 {vol}",f"SNOWICK {scent} {PERFUME_TYPE_EN} {vol}",f"스노윅 {scent} 향수 {vol} 데일리퍼퓸"]
    detail_copy   = {
        "01_설득":        "향수는 많은데 일상에서 부담 없이 쓸 향을 찾고 계신가요?",
        "02_구조":        f"스노윅 {scent} — 향 라인 상표등록 완료. 일관된 향 경험 설계.",
        "03_Why_SNOWICK": f"스노윅 {scent} 퍼퓸은 향 라인 전용 상표로 등록된 제품입니다. 과장 없이, 체감되는 잔향.",
        "04_상세_메인":   f"{scent} 오드뚜왈렛 퍼퓸 {vol} — 분사, 정착, 잔향까지.",
        "05_상세_구조":   f"오드뚜왈렛 / {vol} / 스프레이 타입 / {scent} 향조",
        "06_구매유도":    f"스노윅 {scent} 퍼퓸 {vol}. 매일 쓰는 향을 바꾸는 선택.",
    }
    return _result(names, summary, brief, keywords, promo_naver, promo_daum,
                   browser_title, meta_desc, meta_keywords, alt_texts, detail_copy, info.get("price",""))

def generate_diffuser(info: dict) -> dict:
    scent = info["scent"]
    vol   = info["vol"]
    names = {
        "cafe24":   f"SNOWICK 스노윅 {scent} 디퓨저 {vol}",
        "en":       f"SNOWICK {scent} Room Diffuser {vol}",
        "admin":    f"스노윅 {scent} 디퓨저 {vol}",
        "supplier": SUPPLIER_FIXED,
    }
    summary = f"스노윅 {scent} 룸 디퓨저 {vol}. 균일 확산 구조, 지속력 중심 설계."
    brief   = f"공간을 바꾸는 향 확산. 스노윅 {scent} 디퓨저 {vol}"
    keywords = {
        "cafe24": [f"{scent}디퓨저","룸디퓨저","향디퓨저","스노윅디퓨저","SNOWICk디퓨저",
                   f"{vol}디퓨저","인테리어디퓨저","공간향디퓨저","확산디퓨저","지속력디퓨저",
                   f"{scent}룸디퓨저","무화디퓨저","국산디퓨저","선물디퓨저","홈디퓨저",
                   "거실디퓨저","침실디퓨저","사무실디퓨저","향기디퓨저","스틱디퓨저"],
        "coupang":[f"{scent} 디퓨저","룸 디퓨저","향 디퓨저","스노윅 디퓨저",f"{vol} 디퓨저",
                   "인테리어 디퓨저","공간향 디퓨저","지속력 디퓨저",f"{scent} 룸디퓨저",
                   "무화 디퓨저","국산 디퓨저","선물 디퓨저","홈 디퓨저","거실 디퓨저",
                   "침실 디퓨저","사무실 디퓨저","향기 디퓨저","스틱 디퓨저","확산 디퓨저","천연향 디퓨저"],
        "naver":  [f"{scent}디퓨저","룸디퓨저","스노윅디퓨저",f"{vol}디퓨저","향디퓨저",
                   "인테리어디퓨저","지속력디퓨저","공간향","무화디퓨저","홈디퓨저"],
    }
    promo_naver   = f"{scent} 균일 확산 룸 디퓨저 {vol} 스노윅"[:50]
    promo_daum    = (f"스노윅 {scent} 룸 디퓨저 {vol}. 무화 구조 기반 균일 확산. 빠른 확산 속도와 지속력. 거실, 침실, 사무실 등 공간별 사용 가능.")[:200]
    browser_title = f"{scent} 룸 디퓨저 {vol} 균일 확산 지속력 | SNOWICK 스노윅"
    meta_desc     = fix_meta_desc(f"스노윅 {scent} 룸 디퓨저 {vol}. 무화 구조 기반 균일 확산, 빠른 확산 속도와 긴 지속력. 공간 향기 설계 디퓨저.")
    meta_keywords = [f"{scent}디퓨저","룸디퓨저","스노윅디퓨저",f"{vol}디퓨저","무화디퓨저","지속력디퓨저","확산디퓨저","스노윅","SNOWICK","향디퓨저"]
    alt_texts     = [f"스노윅 {scent} 룸 디퓨저 {vol}",f"SNOWICK {scent} Room Diffuser {vol}",f"스노윅 {scent} 디퓨저 균일확산 지속력"]
    detail_copy   = {
        "01_설득":        "디퓨저를 켜뒀는데 공간에 향이 안 느껴지신 적 있으신가요?",
        "02_구조":        "스노윅 디퓨저 — 무화 구조 기반 균일 확산 설계. 스틱이 향을 공간으로 고르게 올립니다.",
        "03_Why_SNOWICK": f"일반 디퓨저는 스틱 주변만 향이 납니다. 스노윅 {scent} 디퓨저는 확산 속도와 지속력을 동시에 설계합니다.",
        "04_상세_메인":   f"{scent} 룸 디퓨저 {vol} — 확산, 공간감, 지속력.",
        "05_상세_구조":   f"무화 구조 / 스틱 확산 / {vol} / 공간 향기 설계",
        "06_구매유도":    f"스노윅 {scent} 디퓨저 {vol}. 공간이 달라집니다.",
    }
    return _result(names, summary, brief, keywords, promo_naver, promo_daum,
                   browser_title, meta_desc, meta_keywords, alt_texts, detail_copy, info.get("price",""))

def generate_starwick(info: dict) -> dict:
    diameter = info["diameter"]
    names = {
        "cafe24":   f"SNOWICK 스노윅 별모양 우드심지 STAR WICK SYSTEM {diameter}",
        "en":       f"SNOWICK Star Shaped Wood Wick STAR WICK SYSTEM {diameter}",
        "admin":    f"스노윅 별모양심지 {diameter}",
        "supplier": SUPPLIER_FIXED,
    }
    summary = (f"특허받은 별모양 우드심지 STAR WICK SYSTEM {diameter}. "
               f"터널링 0% 연소 구조. 캔들용기 지름 {diameter} 전용.")
    brief   = f"터널링 없는 연소의 시작. 스노윅 별모양 우드심지 {diameter}"
    keywords = {
        "cafe24": ["별모양심지","별모양우드심지","STARWICK","우드심지","캔들심지",
                   "터널링없는심지","크랙클링심지","특허심지","스노윅심지",f"{diameter}심지",
                   "별모양캔들심지","연소안정심지","멜트풀심지","DIY캔들심지","캔들용심지",
                   "SNOWICk심지","천연심지","자작나무심지","수제캔들심지","별심지"],
        "coupang":["별모양 심지","별모양 우드심지","우드 심지","캔들 심지","터널링없는 심지",
                   "크랙클링 심지","특허 심지","스노윅 심지",f"{diameter} 심지","별모양 캔들심지",
                   "연소안정 심지","멜트풀 심지","DIY 캔들심지","캔들용 심지","천연 심지",
                   "자작나무 심지","수제캔들 심지","별심지","나무심지","캔들만들기 심지"],
        "naver":  ["별모양심지","별모양우드심지","우드심지","캔들심지","터널링없는심지",
                   "특허심지","스노윅심지",f"{diameter}심지","크랙클링심지","DIY캔들심지"],
    }
    promo_naver   = f"특허 별모양 우드심지 STAR WICK {diameter} 터널링0%"[:50]
    promo_daum    = (f"스노윅 별모양 우드심지 STAR WICK SYSTEM {diameter}. 특허받은 연소 구조로 터널링 0%, 안정적인 멜트풀, 크랙클링 사운드. 캔들 용기 지름 {diameter} 전용 커스텀 설계.")[:200]
    browser_title = f"별모양 우드심지 STAR WICK {diameter} 특허 터널링0% | SNOWICK 스노윅"
    meta_desc     = fix_meta_desc(f"스노윅 별모양 우드심지 STAR WICK SYSTEM {diameter}. 특허받은 연소 구조. 터널링 0%, 멜트풀, 크랙클링 사운드 구현. 캔들 용기 지름 {diameter} 전용.")
    meta_keywords = ["별모양심지","별모양우드심지","STARWICK","우드심지","특허심지","터널링없는심지","크랙클링심지","스노윅","SNOWICK",f"{diameter}심지"]
    alt_texts     = [f"스노윅 별모양 우드심지 STAR WICK {diameter}",f"SNOWICK Star Wick System {diameter} 특허 연소 구조",f"스노윅 별모양심지 {diameter} 터널링 없는 캔들심지"]
    detail_copy   = {
        "01_설득":        "심지 선택이 잘못되면 터널링, 연기, 향 손실이 생깁니다.",
        "02_구조":        "별모양 우드심지 STAR WICK SYSTEM — 특허받은 별 단면 구조로 용기 전면을 균일하게 연소합니다.",
        "03_Why_SNOWICK": f"일반 심지는 중심을 파고듭니다. 스노윅 별모양심지는 {diameter} 용기에 맞게 설계된 커스텀 연소 구조입니다.",
        "04_상세_메인":   f"별모양 우드심지 {diameter} — 불꽃, 멜트풀, 크랙클링까지 설계된 심지.",
        "05_상세_구조":   f"별 단면 / {diameter} 전용 / 특허 제10-2014829·제10-1919388 / 디자인등록 제30-0995853",
        "06_구매유도":    f"스노윅 별모양심지 {diameter}. 심지 하나가 캔들 전체를 바꿉니다.",
    }
    return _result(names, summary, brief, keywords, promo_naver, promo_daum,
                   browser_title, meta_desc, meta_keywords, alt_texts, detail_copy, info.get("price",""))

def generate_oil(info: dict) -> dict:
    scent = info["scent"]
    vol   = info["vol"]
    names = {
        "cafe24":   f"SNOWICK 스노윅 {scent} 프래그런스 오일 {vol}",
        "en":       f"SNOWICK {scent} Fragrance Oil {vol}",
        "admin":    f"스노윅 {scent} 오일 {vol}",
        "supplier": SUPPLIER_FIXED,
    }
    summary = f"스노윅 {scent} 프래그런스 오일 {vol}. 향조·확산속도·잔향밸런스 중심 설계."
    brief   = f"향조부터 잔향까지 계산된 향. 스노윅 {scent} 프래그런스 오일 {vol}"
    keywords = {
        "cafe24": [f"{scent}프래그런스오일",f"{scent}향오일","프래그런스오일","캔들오일",
                   "디퓨저오일","향료오일","스노윅오일",f"{vol}오일","DIY캔들오일","확산오일",
                   "잔향오일","SNOWICk오일","국산향오일","공간향오일","룸향오일",
                   f"{scent}향료","아로마오일","천연향오일","수제캔들향료","인테리어향오일"],
        "coupang":[f"{scent} 프래그런스오일",f"{scent} 향오일","프래그런스 오일","캔들 오일",
                   "디퓨저 오일","향료 오일","스노윅 오일",f"{vol} 오일","DIY 캔들오일",
                   "확산 오일","잔향 오일","국산 향오일","공간향 오일","룸 향오일",
                   f"{scent} 향료","아로마 오일","천연향 오일","수제캔들 향료","인테리어 향오일","향기 오일"],
        "naver":  [f"{scent}프래그런스오일","프래그런스오일","캔들오일","스노윅오일",
                   f"{vol}오일","DIY캔들오일","디퓨저오일","향오일","잔향오일","확산오일"],
    }
    promo_naver   = f"{scent} 프래그런스 오일 {vol} 확산 잔향밸런스 스노윅"[:50]
    promo_daum    = (f"스노윅 {scent} 프래그런스 오일 {vol}. 향조·확산속도·잔향밸런스 중심 설계. 캔들·디퓨저 DIY 제작, 공간 향기 연출에 사용 가능.")[:200]
    browser_title = f"{scent} 프래그런스 오일 {vol} 확산 잔향밸런스 | SNOWICK 스노윅"
    meta_desc     = fix_meta_desc(f"스노윅 {scent} 프래그런스 오일 {vol}. 향조·확산속도·잔향밸런스 중심 설계. 캔들·디퓨저 DIY 및 공간 향기 연출용.")
    meta_keywords = [f"{scent}프래그런스오일","프래그런스오일","캔들오일","디퓨저오일","스노윅오일",f"{vol}오일","DIY캔들향료","향오일","스노윅","SNOWICK"]
    alt_texts     = [f"스노윅 {scent} 프래그런스 오일 {vol}",f"SNOWICK {scent} Fragrance Oil {vol}",f"스노윅 {scent} 향오일 확산 잔향밸런스"]
    detail_copy   = {
        "01_설득":        "향오일을 써봤는데 향이 금방 날아가거나 공간에 퍼지지 않은 적 있으신가요?",
        "02_구조":        f"스노윅 {scent} 오일 — 향조·확산속도·잔향밸런스를 동시에 설계합니다.",
        "03_Why_SNOWICK": "스노윅 프래그런스 오일은 공간 적합성까지 고려한 향 설계 제품입니다. 연소·확산 전용 오일.",
        "04_상세_메인":   f"{scent} 프래그런스 오일 {vol} — 향조, 확산, 잔향.",
        "05_상세_구조":   f"향조 설계 / 확산속도 최적화 / 잔향밸런스 / {vol} / {scent}",
        "06_구매유도":    f"스노윅 {scent} 오일 {vol}. 향을 직접 설계하세요.",
    }
    return _result(names, summary, brief, keywords, promo_naver, promo_daum,
                   browser_title, meta_desc, meta_keywords, alt_texts, detail_copy, info.get("price",""))

def generate_material(info: dict) -> dict:
    key  = info["key"]
    spec = info["spec"]
    folder_path, item_name, kw_cat = MATERIAL_MAP[key]
    kw_base = KW_BASE.get(kw_cat, [])
    names = {
        "cafe24":   f"SNOWICK 스노윅 {item_name} {spec}",
        "en":       f"SNOWICK {item_name} {spec}",
        "admin":    f"스노윅 {item_name} {spec}",
        "supplier": SUPPLIER_FIXED,
    }
    summary = f"스노윅 {item_name} {spec}. 캔들·디퓨저 제작용 부자재."
    brief   = f"스노윅 공식 부자재 — {item_name} {spec}"
    kw_item = [item_name, f"{item_name} {spec}", f"스노윅{item_name}",
               f"DIY{item_name}", f"캔들{item_name}", "스노윅부자재",
               f"{spec}{item_name}", "수제캔들재료", "캔들만들기재료", "SNOWICk부자재"]
    kw_item_cp = [item_name, f"{item_name} {spec}", f"스노윅 {item_name}",
                  f"DIY {item_name}", f"캔들 {item_name}", "스노윅 부자재",
                  f"{spec} {item_name}", "수제캔들 재료", "캔들만들기 재료", "캔들 부자재"]
    keywords = {
        "cafe24":  (kw_item + kw_base)[:20],
        "coupang": (kw_item_cp + kw_base)[:20],
        "naver":   [item_name, f"{item_name} {spec}", f"스노윅{item_name}","스노윅부자재",
                    "DIY캔들재료","캔들만들기재료","수제캔들재료","캔들부자재","스노윅","SNOWICK"],
    }
    promo_naver   = f"스노윅 {item_name} {spec} 캔들 제작 부자재"[:50]
    promo_daum    = (f"스노윅 {item_name} {spec}. 캔들·디퓨저 DIY 제작용 부자재. 스노윅 공식 취급 품목.")[:200]
    browser_title = f"{item_name} {spec} 캔들 부자재 | SNOWICK 스노윅"
    meta_desc     = fix_meta_desc(f"스노윅 {item_name} {spec}. 캔들·디퓨저 제작용 부자재. 스노윅 공식 품목.")
    meta_keywords = [item_name, f"{item_name} {spec}", f"캔들{item_name}", "스노윅부자재",
                     "DIY캔들재료","캔들재료","수제캔들","캔들만들기","스노윅","SNOWICK"]
    alt_texts     = [f"스노윅 {item_name} {spec}", f"SNOWICK {item_name} {spec}", f"스노윅 {item_name} 캔들 부자재 {spec}"]
    detail_copy   = {
        "01_설득":        f"캔들 제작에 맞는 {item_name}을 찾고 계신가요?",
        "02_구조":        f"스노윅 {item_name} {spec} — 캔들·디퓨저 제작 전용 부자재.",
        "03_Why_SNOWICK": f"스노윅 공식 취급 부자재. 규격과 품질이 검증된 {item_name}.",
        "04_상세_메인":   f"{item_name} {spec} — 캔들 제작의 기본 재료.",
        "05_상세_구조":   f"{item_name} / {spec} / 스노윅 공식 부자재",
        "06_구매유도":    f"스노윅 {item_name} {spec}. 제대로 된 재료로 시작하세요.",
    }
    result = _result(names, summary, brief, keywords, promo_naver, promo_daum,
                     browser_title, meta_desc, meta_keywords, alt_texts, detail_copy, info.get("price",""))
    result["_folder"] = folder_path
    return result

SEP = "─" * 60

def print_output(result: dict, product_type: str):
    n  = result["names"]
    alt = result["alt_texts"]
    dc  = result["detail_copy"]
    print(f"\n{'═'*60}")
    print(f"  SNOWICK SEO OUTPUT — {product_type}")
    if result.get("_folder"):
        print(f"  폴더: {result['_folder']}")
    if result.get("price"):
        print(f"  단가: {fmt_price(result['price'])}")
    print(f"{'═'*60}")
    print(f"\n{SEP}")
    print("【 1. 제품명 Cafe24 (50자 이내) 】")
    print(char_count(n["cafe24"]))
    print(f"\n{SEP}")
    print("【 2. 영문 상품명 】")
    print(n["en"])
    print(f"\n{SEP}")
    print("【 3. 상품명 관리용 (50자 이내) 】")
    print(char_count(n["admin"]))
    print(f"\n{SEP}")
    print("【 4. 공급사 상품명 】")
    print(n["supplier"])
    print(f"\n{SEP}")
    print("【 5. 상품 요약설명 (255자 이내) 】")
    print(f"{result['summary']}  ({len(result['summary'])}자)")
    print(f"\n{SEP}")
    print("【 6. 상품 간략설명 】")
    print(result["brief"])
    print(f"\n{SEP}")
    print("【 7. 검색어 】")
    print("▶ Cafe24 (20개):")
    print(", ".join(result["keywords"]["cafe24"]))
    print("\n▶ 쿠팡 (20개):")
    print(", ".join(result["keywords"]["coupang"]))
    print("\n▶ 네이버 스마트스토어 (10개):")
    print(", ".join(result["keywords"]["naver"]))
    print(f"\n{SEP}")
    print("【 8. 네이버 쇼핑 추가 홍보문구 (50자 이내) 】")
    print(char_count(result["promo_naver"]))
    print(f"\n{SEP}")
    print("【 9. 다음 쇼핑하우 추가 홍보문구 (200자 이내) 】")
    print(f"{result['promo_daum']}  ({len(result['promo_daum'])}자)")
    print(f"\n{SEP}")
    print("【 10. 브라우저 타이틀 】")
    print(result["browser_title"])
    print(f"\n{SEP}")
    print("【 11. 메타태그 Author (고정) 】")
    print(result["author"])
    print(f"\n{SEP}")
    print("【 12. 메타태그 Description 】")
    print(f"{result['meta_desc']}  ({len(result['meta_desc'])}자)")
    print(f"\n{SEP}")
    print("【 13. 메타태그 Keywords (10개) 】")
    print(", ".join(result["meta_keywords"]))
    print(f"\n{SEP}")
    print("【 14. ALT 텍스트 3종 】")
    for i, a in enumerate(alt, 1):
        print(f"  ALT{i}: {a}")
    print(f"\n{SEP}")
    print("【 15. 상세페이지 6단계 카피 】")
    for k, v in dc.items():
        print(f"  [{k}] {v}")
    if result.get("_warnings"):
        print(f"\n{'⚠'*40}")
        for w in result["_warnings"]:
            print(f"  {w}")
        print(f"{'⚠'*40}")
    print(f"\n{'═'*60}\n")

GENERATORS = {
    "캔들":   generate_candle,
    "퍼퓸":   generate_perfume,
    "디퓨저": generate_diffuser,
    "스타윅": generate_starwick,
    "오일":   generate_oil,
    "부자재": generate_material,
}

def main():
    print("\n" + "═"*60)
    print("  SNOWICK seo_generate.py  (확정본 2026-06-14)")
    print("─"*60)
    print("  완제품:  향명/타입/용량/단가(선택)")
    print("    예) 동백꽃/캔들/200ml")
    print("        한라봉/퍼퓸")
    print("        비자림/디퓨저/100ml")
    print("        스타윅/60mm")
    print("        매화꽃/오일/100ml")
    print("─"*60)
    print("  부자재 고정규격: 품목키/규격/단가(선택)")
    print("    왁스:  왁스_실크소이/1kg")
    print("    스톤:  스톤_샤쉐/500g  또는  스톤_레진/1kg")
    print("    베이스: 베이스_디퓨저/1L")
    print("    스틱:  스틱_블랙/4mm*30cm")
    print("  부자재 노멀: 품목키/제품명/용량/단가(선택)")
    print("    용기:  캔들용기/원형유리용기/200ml")
    print("           디퓨저용기/사각유리병/100ml")
    print("           퍼퓸용기/스프레이병/30ml")
    print("─"*60)
    print("  단가 미입력 시 헤더에 단가 행 미출력")
    print("  종료: q 또는 빈 엔터")
    print("═"*60)
    while True:
        try:
            raw = input("\n입력 > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n종료합니다.")
            break
        if not raw or raw.lower() in ("q", "quit", "exit"):
            print("종료합니다.")
            break
        info = detect_type(raw)
        if "error" in info:
            print(f"  ❌ {info['error']}")
            continue
        ptype  = info["type"]
        gen_fn = GENERATORS.get(ptype)
        if not gen_fn:
            print(f"  ❌ 지원하지 않는 제품 타입: {ptype}")
            continue
        result = gen_fn(info)
        print_output(result, ptype)

if __name__ == "__main__":
    main()
