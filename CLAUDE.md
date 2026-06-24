# SNOWICK Claude Code 운영 규칙 완성본
> 모든 세션에 자동 적용. 수정 시 버전 기록 필수.

---

## ■ 1. 자동 실행 설정

- PowerShell 명령어: 항상 자동 허용
- 파일 생성/수정: 항상 자동 허용
- API 호출: 실행 전 내용 출력 → 확인(y/n) 후 실행
- 매번 허용 묻지 말 것 (API 호출 제외)

---

## ■ 2. 응답 규칙 — 추측 절대 금지

| 금지 | 대응 |
|------|------|
| 추측 답변 ("아마 ~일 것") | "확인이 필요합니다. 캡처 화면을 보내주세요." |
| 미확인 UI/경로 안내 | "직접 확인 필요합니다." |
| API 파라미터 임의 추정 | "공식 문서 확인 후 진행합니다." |
| 확인 없이 파일·API 수정 | 변경 내용 전체 출력 → y/n 확인 후 실행 |
| 오류 추측 해결 | 오류 원문 그대로 출력 후 중단 |

**불확실하면 반드시 "모릅니다 / 확인 필요" 명시 후 중단.**

---

## ■ 3. Cafe24 상품 등록 필수 규칙

### 3-1. 마켓연동 — 모든 상품 등록/수정 시 필수 포함

```json
"naver_shopping_info": {
    "use_naverpay": "T"
}
```

누락 시 롯데ON·스마트스토어·쿠팡 자동연동 비활성화됨. 절대 빠뜨리지 말 것.

### 3-2. 필수 파라미터 전체 체크리스트

```
product_name              상품명
eng_product_name          영문상품명
custom_product_code       관리용상품명
supplier_product_name     공급사상품명 (고정: 스노윅)
manufacturer_name         제조사 (고정: 스노윅)
model_name                모델명
origin_place_code         원산지 코드 (국내: KOR / 중국: CHN)
origin_place_value        원산지 표기 (국내산 / 중국산)
price                     판매가
summary_description       요약설명
simple_description        간략설명
description               상세설명 HTML (이미지 img 태그 포함)
nav_shopping_description  네이버쇼핑 추가 홍보문구
naver_shopping_info       {"use_naverpay": "T"}
seo_title                 브라우저타이틀
seo_author                메타태그 Author (고정: 스노윅)
seo_description           메타태그 Description
seo_keywords              메타태그 Keywords
search_keywords           검색어
detail_image              대표이미지 URL
detail_image_alt          대표이미지 ALT
```

### 3-3. 상세설명 HTML 구조

```html
<div style="text-align:center;">
  <img src="{이미지URL1}" alt="{ALT1}" style="max-width:100%;display:block;margin:0 auto;">
  <img src="{이미지URL2}" alt="{ALT2}" style="max-width:100%;display:block;margin:0 auto;">
  <img src="{이미지URL3}" alt="{ALT3}" style="max-width:100%;display:block;margin:0 auto;">
</div>
```

### 3-4. 고정값 (스크립트 내 하드코딩)

```
supplier_product_name = "스노윅"
manufacturer_name     = "스노윅"
seo_author            = "스노윅"
naver_shopping_info   = {"use_naverpay": "T"}
```

---

## ■ 4. 작업 출력 규칙

- 핵심 작업 결과물은 .md 또는 .py 파일로 생성
- 채팅 장문 텍스트 출력 금지
- 실행 전 변경 내용 전체 출력 → 확인(y/n) 후 실행

---

## ■ 5. 금지 사항

- 캔들 8종 수정 금지 (명시적 지시 없는 한)
- cafe24_register.py 사용 금지 (레거시)
- 추측·예상·가정 문구 사용 금지
- 파이프( │ ) 상품명 사용 금지

---

## ■ 브랜드 정체성

스노윅(SNOWICK)은 감성 향 브랜드가 아닙니다.
구조 설계 기반 향·연소 시스템 브랜드입니다.

```
구조 > 재현성 > 안전성 > 플랫폼 정확성 > 감성 표현
```

### 승인된 브랜드 용어

```
SNOWICK / 스노윅
Structure-Engineered Fragrance
STAR WICK SYSTEM
별모양심지 / 별모양우드심지 / 스타윅
자작나무심지 / 터널링 0% / 멜트풀 / 크랙클링
대나무 용기 / 천연 소이왁스
```

### 금지 용어

```
스노위 (오타) / 우드윅
명품향수 같다 / 고급 향수와 동일
무조건 안전 / 완전 무해 / 효능 보장 / 치료 / 항균 보장
검증 없는 기능성 표현 / 확인되지 않은 인증·수상 표현
감성만 강조하는 과장 표현
```

---

## ■ 확정 캔들 8종

```
대나무 비자림숲속 / 대나무 동백꽃 / 대나무 매화꽃 / 대나무 철쭉꽃
대나무 한라봉 / 대나무 오리엔탈템플우디 / 대나무 우디프레스티지 / 대나무 레몬가든플뢰르
```

공통 스펙: 200g / 대나무 용기 / 자작나무심지 / 천연 소이왁스

---

## ■ 공통 캡션 본문 (확정 — 2026-06-22)

```
캔들이 다 쓰기도 전에 가운데만 녹고 가장자리는 그대로 남아 버리신 적 있나요?

일반 캔들은 심지 하나라 열이 중앙에만 집중됩니다.
스노윅은 자작나무 심지 3P를 별모양으로 엇갈려 도킹하여
불이 용기 가장자리까지 열이 골고루 전달되어 벽면까지 남김없이 녹입니다.
터널링 0%의 이유입니다.

유리 용기는 열이 외부로 전달돼 용기가 뜨겁습니다.
대나무는 열전도율이 낮아 왁스가 다 녹아도 용기 겉은 따뜻한 정도.
우드코스터 없이 바로 씁니다.
```

---

## ■ 운영 플랫폼

```
카페24 — 단일 원장 기준
마켓플러스 — 플랫폼 전송 허브
카카오톡스토어 / 네이버 스마트스토어 / 쿠팡
```

플랫폼별 상품명·SEO·설명 문장·태그 반드시 분리 운영. 카페24 원장 문장 복붙 금지.

---

## ■ 수정 이력

| 버전 | 일자 | 내용 |
|------|------|------|
| v1 | 2026-06-23 | 최초 통합 완성본 작성 |
