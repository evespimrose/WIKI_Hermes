---
tags: [llm-wiki, llm-워크플로우, 훅, 검색]
date_created: 2026-05-22
last_modified: 2026-06-22
---

# Sonar Protocol

[[LLM_컨텍스트_5대_문제]] 3번(토큰 폭발)에 대한 가장 강력한 단일 방어 규칙. 무차별 탐색 대신 codegraph로 *음파(핑)를 쏘아 구조화된 메아리만 받고 이동*한다는 소나(sonar) 비유에서 이름을 땄다. 구 명칭은 *Cave-Man Protocol*이며, 개명 경위는 아래 「개명 이력」에 정리한다.

## 3대 규칙

> ⚠️ **원형(1단계) 규칙 — 보존용.** 아래 RULE 1~3은 dictionary.md를 primary로 가정한 [[Workflow_진화_3단계]] 1단계의 원형이다. **현행 정본은 codegraph-first** — 아래 「Codegraph-First (3단계 진화 이후)」 절이 갱신된 탐색 순서를 정의한다. RULE 1(bash 탐색 금지)은 그대로 유효하나, RULE 2·3은 "dictionary만으로"가 아니라 **"codegraph 우선, dictionary 보완"**으로 읽는다.

```
RULE 1: 탐색 시 bash find/grep/ls를 사용하지 않는다 (현행 유효)
RULE 2: (원형) manage/dictionary.md § 1 파일 인덱스만으로 파일 경로를 특정한다
         → 현행: codegraph_context/search 우선, dictionary § 1은 보완(fallback)
RULE 3: (원형) § 1에서 찾을 수 없으면 § 3 키워드 인덱스로 BLK 추정 → § 1 재시도
         → 현행: codegraph로 미해결 시 dictionary § 3 키워드로 BLK 추정(보완)
```

자세한 dictionary 섹션 구조는 [[Dictionary_md_좌표_시스템]]에서, BLK 코드 자체는 [[BLK_좌표_시스템]]에서 다룬다.

## 금지 명령

```
❌ find Assets -name "*.cs"     ── 디렉토리 전수 조사
❌ ls -r docs/                  ── 재귀 나열
❌ grep -r "ClassName" .        ── 전체 텍스트 검색
❌ rg "pattern"                 ── 동일
❌ fd "*.md"                    ── 동일
❌ node/sqlite3/bash로 직접 .codegraph/codegraph.db 쿼리 ── codegraph DB 직접 접근 탈옥
```

이 명령들은 *수천~수만 줄의 결과*를 컨텍스트에 흡수시켜 [[LLM_컨텍스트_5대_문제]] 3번을 즉시 트리거한다.

## 허용 대안

```
✅ codegraph_context / search   ── 현행 primary (구조화된 메아리만 수신)
✅ manage/dictionary.md § 1     ── 보완: BLK 코드로 정확한 경로
✅ Glob("Assets/**/*.cs")        ── 도구 사용 (출력만 받음)
✅ Grep("ClassName", glob="*.cs") ── 패턴 매칭 (필요 부분만)
```

도구 호출은 *출력만 컨텍스트로 들어오고 명령 자체는 들어오지 않는다*는 점에서 bash 탐색과 결정적으로 다르다. 출력은 또한 구조화되어 있어 진입량이 통제된다.

## 정량 효과

| 비교 축 | bash 탐색 | dictionary-first | 절감 |
|---|---|---|---|
| 단일 파일 특정 | 600~1,200 토큰 | ~30 토큰 | 75~97% |
| 15턴 누적 | 20,000~30,000 토큰 | 2,000~4,000 토큰 | ~85% |

장기 세션일수록 절감 폭이 비선형으로 커진다. 매 턴의 노이즈가 컴팩션 절벽([[LLM_컨텍스트_5대_문제]] 1번)을 앞당기기 때문.

## 훅 강제

[[LLM_통제_철학_6대원칙]]의 "Hooks > Prompts"가 가장 두드러지는 곳. 현재 [[L1_Hard_Gate_훅체계]]의 트리오가 Bash, PowerShell, 소스 Read 세 경로 모두를 PreToolUse에서 차단한다:

```
cave-man-guard.sh             → find/grep -r/ls -r/rg/fd/cat *.cs (Bash)
cave-man-guard-powershell.sh  → Get-ChildItem -Recurse 등 PS 우회
codegraph-gate.sh             → tool-history 검증, codegraph 미사용 시 소스 Read 차단
```

프롬프트로 "find 쓰지 마세요"를 명시해도 LLM은 장기 세션에서 결국 위반한다. 훅으로 *행동 자체를 가로채는* 결정론이 필요하다. 이전엔 Bash hook만 있어 PS 우회가 가능했고, 소스 파일을 직접 Read하는 경로는 무방비였다 — [[Workflow_Ecosystem_버전계보]] v3.4에서 이 두 누수가 동시에 메워졌다.

## Codegraph-First (3단계 진화 이후)

본 프로토콜의 원형(RULE 1~3)은 dictionary.md를 primary 인덱스로 가정한 [[Workflow_진화_3단계]] 1단계의 산물이다. 3단계로 진화한 현재는 [[Codegraph_MCP_통합]]이 primary, dictionary는 보완 인덱스다. 탐색 순서가 다음과 같이 갱신됐다:

```
1. codegraph_context (영역 종합) / codegraph_search (심볼 위치)
2. codegraph_node / codegraph_explore (소스 본문)
3. codegraph_callers/callees/impact/trace (관계 분석)
4. (보완) dictionary.md § 1·§ 3 → Read/Grep
```

원형의 RULE 1(bash 탐색 금지)은 그대로 유효하지만, RULE 2·3은 "dictionary만으로"가 아니라 "codegraph 우선, dictionary 보완"으로 읽어야 한다. [[Workflow_Ecosystem_버전계보]] v3.5는 이 순서를 RIPER 7개 커맨드 본문에 모두 명시함으로써 *커맨드 레벨의 모호성*까지 제거했다.

## 검색 워크플로 (탐색 시 따를 순서)

> **현행(3단계) 순서 — codegraph-first.** 위 「Codegraph-First (3단계 진화 이후)」 절과 동일한 우선순위를 실무 순서로 편 것이다. 원형(1단계)의 dictionary-first 순서는 아래 「보존」 블록에 남긴다.

```
1. codegraph_context (영역 종합) / codegraph_search (심볼 위치)
     → 닿으면 → codegraph_node·explore로 소스 본문 → 작업 착수
2. codegraph_impact / callers / callees / trace (BLK→파일 엣지·관계·영향 분석)
3. (보완) dictionary.md § 1 파일 인덱스에서 BLK 코드로 경로 조회 → Read/Grep
4. (보완) dictionary.md § 3 키워드 인덱스로 BLK 추정 → Step 3 복귀
     → 추정 불가 → "BLK 태그 없음: § 3 키워드 인덱스 확인 필요" 출력 → 계속 진행
```

**보존 — 원형(1단계) dictionary-first 순서** (현행 아님):

```
1. dictionary.md § 1 파일 인덱스에서 BLK 코드로 경로 직접 조회
     → 찾으면 → 해당 파일 Read → 작업 착수
     → 못 찾으면 → Step 2
2. dictionary.md § 3 키워드 인덱스에서 작업 키워드로 BLK 추정
     → BLK 특정 → Step 1로 복귀
3. BLK 추정 불가 → "BLK 태그 없음: § 3 키워드 인덱스 확인 필요" 출력 → 계속 진행
```

## 개명 이력 (Cave-Man → Sonar)

원래 이름은 **Cave-Man Protocol**이었다. "원시인 같은 무차별 `find`·`grep` 탐색"을 금지한다는 자조적 별칭으로, 사용자가 bash 탐색을 떠올릴 때마다 *자기 자신을 원시인이라 부르게* 만들어 행동 억제력을 높이려는 의도였다 — [[LLM_통제_철학_6대원칙]] 어디에도 명시되지 않았지만 [[Mastermind_Architecture_Manifesto]]의 "기계적 강제" 정신과 일맥상통하는 부수 효과.

2026-06-12, 입력측(읽기) 규율인 이 프로토콜을 **Sonar Protocol**로 개명했다. 두 가지 이유다:

1. **이름 양보**: 신규 *출력측(쓰기)* 압축 스킬이 "caveman"을 쓰기로 하면서, 입력 arm이 충돌을 피해 이름을 내줬다. 두 arm 모두 토큰 게이트지만 방향이 다르다(읽기측 진입량 통제 vs 쓰기측 출력량 통제).
2. **더 정확한 비유**: codegraph로 *음파(핑)를 쏘고 → 구조화된 메아리를 받은 뒤 → 이동*하는 동작이 소나(sonar)와 동형이다. 무차별 탐색의 반대편에 있는 "측정 후 이동"을 직접 표현한다.

훅 파일명(`cave-man-guard.sh`·`cave-man-guard-powershell.sh`)은 변경 비용·위험 대비 효용이 낮아 **그대로 유지**한다 — 위 「훅 강제」 절의 코드 레퍼런스가 옛 이름을 쓰는 이유다. `archive/**`의 과거 정본 스냅샷·CHANGELOG 등 역사 기록도 불변으로 둔다([[맥락_오염_방지]]).

## 관련 노트

- 좌표 시스템 본체: [[Dictionary_md_좌표_시스템]]
- BLK 코드 의미론: [[BLK_좌표_시스템]]
- manage 폴더 전체: [[manage_폴더_역할분리]]
- 코드 인텔리전스 (3단계 primary): [[Codegraph_MCP_통합]]
- 탐색 결과의 런타임 캐시(시간축 확장): [[탐색_후_스킬_캐시_패턴]]
- 진입 토큰 예산 규약: [[최소컨텍스트_진입규약]]
- 입력 *내용* 압축(직교 상보 축): [[CCR_가역압축_패턴]]
- 훅 강제 메커니즘: [[L1_Hard_Gate_훅체계]]
- 다층 방어선 절충 역사: [[L1_L5_다층방어선_역사]]
- 실전 사례: [[First_Grep_실전사례]]
- 우회 벡터(탈옥 계열): [[탐색_게이트_우회_벡터]]
- 진화 맥락: [[Workflow_진화_3단계]]
- 관련 PRD: 이 프로토콜의 단계별 도입 현황은 dictionary-first-grep PRD에 추적

## 출처

- raw/dictionary-first-grep-workflow.md (2026-05-22 유입) — §1 Background, 정량 비교
- raw/Workflow-Design-Philosophy.md (2026-05-22 유입) — §7 Cave-Man Protocol (구 명칭)
- raw/ecosystem-atomic-analysis.md (2026-05-22 유입) — §3-A Cave-Man Protocol(구 명칭), §3-F 검색 워크플로
- raw/caveman_to_sonar_rename.md (2026-06-12 유입) — Cave-Man → Sonar 개명 결정·범위·백링크 재정합
- raw/cxt146_sonar_protocol_jailbreak_verification.md (2026-06-17 유입) — 「금지 명령」 codegraph DB 직접 접근 탈옥 항목의 검증 근거 ([[탐색_게이트_우회_벡터]]로 원리 분리)
