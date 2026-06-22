# SNOWICK CODEX RULES

## File Role

This file defines the strict operating boundary, validation rules, and platform-specific constraints for Codex in the SNOWICK repository.

If this file conflicts with a user request, Codex must follow this file unless the user explicitly states that the master rule is being updated.

## Decision Hierarchy

Apply rules in this order:

```text
1. Explicit current user instruction
2. CODEX_RULES.md
3. AGENTS.md
4. README.md
5. Existing system files
6. Existing product files
7. Existing draft files
```

Exception:

```text
Legal, IP, safety, price, and confirmed product specification changes require human approval even if requested indirectly.
```

## Absolute Prohibitions

Codex must not:

```text
merge pull requests
delete files
create repositories
fork repositories
publish to external platforms
change confirmed product prices
change confirmed product names
change confirmed product specifications
invent patent numbers
invent trademark numbers
invent certification claims
invent test results
invent safety claims
invent efficacy claims
invent platform registration status
treat candidate search terms as confirmed terms
```

## Approved Work Types

Codex may assist with:

```text
SEO text
Cafe24 field drafts
Naver Smart Store search term documents
Coupang search term documents
product descriptions
SNS captions
label copy
Markdown cleanup
CSV structure review
GitHub document maintenance
PR summaries
change validation
```

## SNOWICK Fixed Brand Definition

Use the following definition as the fixed brand basis:

```text
SNOWICK is a structure-engineered fragrance brand.
It treats fragrance, combustion, diffusion, wick structure, melt pool behavior, and sound character as design variables.
```

Do not reduce SNOWICK to a simple emotional candle brand.

## Confirmed IP Statements

Use only confirmed IP statements already present in the repository or explicitly provided by the user.

Known confirmed IP references:

```text
특허 제10-2014829호
특허 제10-1919388호
디자인등록 제30-0995853호
상표등록 제40-1684514호
```

Rules:

```text
Do not invent additional patent numbers.
Do not invent additional trademark numbers.
Do not expand IP claims beyond confirmed wording.
Do not state that an unconfirmed scent name is trademarked.
Do not apply Bijarim-related description to unrelated scent lines unless the user confirms the rule update.
```

## Confirmed Candle Product Set

```text
대나무 비자림숲속
대나무 동백꽃
대나무 매화꽃
대나무 철쭉꽃
대나무 한라봉
대나무 오리엔탈템플우디
대나무 우디프레스티지
대나무 레몬가든플뢰르
```

## Confirmed Candle Specifications

```text
용량: 200g
용기: 대나무 용기
심지: 자작나무 별모양 우드심지
구조: 별모양심지 / 별모양우드심지 / 스타윅
연소 표현: 터널링 0%, 멜트풀, 크랙클링
```

If a file contains different data, mark it for human review instead of silently changing all values.

## Confirmed Candle English Names

```text
비자림숲속 = Bijarim Forest
동백꽃 = Camellia
매화꽃 = Plum Blossom
철쭉꽃 = Azalea
한라봉 = Hallabong
오리엔탈템플우디 = Oriental Temple Woody
우디프레스티지 = Woody Prestige
레몬가든플뢰르 = Lemon Garden Fleur
```

## Forbidden Final Copy

Do not use the following in final customer-facing copy:

```text
스노위
우드윅
명품향수 같다
고급 향수와 동일
감성만으로 만든
무조건 안전
완전 무해
효능 보장
치료
항균 보장
탈취 보장
검증된 효과
인증 완료
특허받은 향
```

Allowed only in documentation/checklists:

```text
스노위
우드윅
```

## Product Copy Structure

All product descriptions must follow this order:

```text
1. 소비자 문제
2. 스노윅 구조 차이
3. 제품 근거
4. 사용 환경
5. 구매 이유
6. 행동 유도
```

Required question:

```text
왜 일반 제품이 아니라 스노윅인가
```

If this question is not answered, the copy is incomplete.

## Naver Smart Store Search Term Rules

Confirmed registerable terms only:

```text
소이캔들
생일선물
우드심지
집들이선물
```

Candidate terms must be labeled as candidates.

Candidate terms may include:

```text
별모양심지
비자림숲속
동백꽃
매화꽃
철쭉꽃
한라봉
오리엔탈템플우디
우디프레스티지
레몬가든플뢰르
향조 연상어
```

Rules:

```text
Do not call candidate terms final.
Do not combine confirmed and candidate terms under a final-only heading.
Do not replace confirmed terms unless the user confirms new registered terms.
If a seller center term fails to register, remove it or move it to candidate status.
```

Required Naver format:

```text
확정 검색어:
소이캔들, 생일선물, 우드심지, 집들이선물

후보 검색어:
[판매자센터에서 등록 확인된 경우에만 채택]
```

## Coupang Search Term Rules

Coupang terms:

```text
maximum 20 terms
comma-separated
free-input allowed
do not exceed 20
do not add unsupported claims
do not add unrelated brand names
```

Recommended pattern:

```text
{향}캔들
대나무 캔들
별모양심지 캔들
터널링없는 캔들
천연왁스 캔들
크랙클링 캔들
우드심지 캔들
멜트풀 캔들
향캔들
스노윅 캔들
200g 캔들
별모양 우드심지
연소안정성 캔들
특허 캔들
{향}향 캔들
선물 캔들
인테리어 캔들
홈 캔들
소이캔들
수제캔들
```

If platform rules change, mark the section for human review.

## Cafe24 Rules

Product fields must preserve confirmed data.

Do not invent:

```text
price
origin
manufacturer
supplier
product code
patent text
certification text
capacity
```

Product name rule:

```text
No pipe character: |
No arbitrary reordering unless requested
No brand typo
```

## Markdown Editing Rules

When editing Markdown:

```text
preserve headings unless instructed
preserve tables unless instructed
preserve code blocks
do not break fenced code blocks
do not mix confirmed and candidate values
do not duplicate sections
do not create dead files
move deprecated drafts to archive only when instructed
```

Archive rule:

```text
Do not delete old files.
If archival is requested, move to 99_ARCHIVE or an existing _archive folder.
```

## Pull Request Requirements

Every PR must include:

```text
## 변경 파일
- [file path]

## 변경 내용
- [specific sections changed]

## 변경 이유
- [why the change was needed]

## 검수 기준
- AGENTS.md 확인
- CODEX_RULES.md 확인
- 네이버 확정/후보 검색어 분리 확인
- 스노윅 오타 확인
- 금지어 확인
- 파일 삭제 없음
- 관련 없는 파일 수정 없음

## 대표 승인 필요 항목
- [yes/no and reason]
```

## Required Self-Check

Before PR, Codex must check:

```text
1. Did I read AGENTS.md?
2. Did I read CODEX_RULES.md?
3. Did I edit only the requested file or section?
4. Did I preserve confirmed product data?
5. Did I avoid inventing claims?
6. Did I separate confirmed and candidate Naver terms?
7. Did I keep Coupang terms under 20?
8. Did I avoid deleting files?
9. Did I avoid merging PRs?
10. Did I clearly mark human approval items?
```

## Failure Handling

If Codex cannot verify a required value, it must write:

```text
확인 불가 : [항목]
대표 승인 필요 : [이유]
```

If required input is missing, return only:

```text
입력값 부족 : [부족한 항목]
```

Do not guess.
Do not fabricate.
Do not silently normalize unconfirmed values.
