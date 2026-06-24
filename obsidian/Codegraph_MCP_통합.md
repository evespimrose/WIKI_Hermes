---
tags: [llm-wiki, 검색, 코드인텔리전스, 인덱스]
date_created: 2026-05-28
last_modified: 2026-06-17
---

# Codegraph MCP 통합

tree-sitter 기반의 sub-ms 코드 심볼 인덱스. [[Sonar_Protocol]]의 3단계 진화에서 dictionary.md 수기 인덱스를 대체·보완한 코드 인텔리전스 레이어.

## 무엇인가

Codegraph는 SQLite로 저장되는 코드 심볼 지식 그래프다. 프로젝트의 모든 심볼·엣지·파일을 tree-sitter 파서로 추출해 sub-millisecond로 조회할 수 있다. file watcher가 약 500ms debounce로 인덱스를 자동 갱신한다.

[[Dictionary_md_좌표_시스템]]이 *사람이 수기로 관리하는 좌표 지도*라면, codegraph는 *자동 파싱되는 관계 그래프*다. 두 시스템은 보완 관계이며, 현재 워크플로우(3단계, [[Workflow_진화_3단계]])는 codegraph를 primary로 dictionary를 보완 인덱스로 사용한다.

## 핵심 도구 (codegraph_*)

| 도구 | 질문 | 사용 시점 |
|---|---|---|
| `codegraph_status` | "인덱스 준비됐나?" | 세션 초기 health check |
| `codegraph_search` | "X라는 심볼은 어디?" | 심볼 이름으로 위치 조회 |
| `codegraph_context` | "이 작업/영역의 맥락은?" | 종합 컨텍스트 (PRIMARY) |
| `codegraph_node` | "Y의 시그니처/소스/docstring" | 단일 심볼 상세 |
| `codegraph_explore` | "여러 관련 심볼의 소스" | 묶음 조회 (capped) |
| `codegraph_callers` | "무엇이 이 함수를 호출?" | 역방향 분석 |
| `codegraph_callees` | "이 함수가 무엇을 호출?" | 정방향 분석 |
| `codegraph_trace` | "X에서 Y로 가는 경로?" | 호출 흐름 + 동적 디스패치 |
| `codegraph_impact` | "Z를 바꾸면 무엇이 깨짐?" | 변경 영향 범위 |
| `codegraph_files` | "이 디렉토리에 뭐가 있나?" | 파일 목록 |

`codegraph_trace`는 콜백, React 재렌더, JSX children 같은 동적 디스패치 hop을 한 번에 잇기 때문에 grep으로는 추적 불가능한 경로도 한 호출로 해결된다.

## 왜 grep/Read보다 우선인가

[[LLM_통제_철학_6대원칙]] 원칙 1(토큰 1급)의 정량 근거:

- **구조적 질문**(누가 호출하나, 무엇이 깨지나, 어디에 정의됐나) → codegraph가 압도적으로 저렴
- **텍스트 질문**(문자열 내용, 주석, 로그 메시지) → grep/Read가 정답
- **재검증 금지**: codegraph 결과는 AST 파싱 산출물이라 grep으로 재확인하면 손해

전형적 안티패턴: `codegraph_search` 직후 같은 심볼을 grep으로 또 찾는 것. 한 번의 신뢰가 N개의 grep을 절약한다.

## 적용 경계 — 벤치마크 정직성

위 "우선" 주장에는 경계가 있다. codegraph류 구조화 인덱스가 *항상* grep보다 싼 것은 아니며, 자기 인덱스의 효용을 측정할 때 빠지는 함정이 있다.

- **순환 ground truth**: 그래프가 만든 관계를 그래프 자신으로 채점하면 점수가 자기충족적으로 부풀려진다. 외부 기준 없는 자가 벤치는 신뢰할 수 없다.
- **소형 변경 역효과**: 1홉·단일 파일 수정에서는 인덱스 조회 오버헤드가 grep·raw Read보다 *오히려 비쌀* 수 있다 — "작은 변경일수록 토큰이 줄어든다"는 가정의 반례.
- **실측 한계**: 외부 검증에서 검색 품질이 MRR ≈ 0.35에 그친 사례도 있다. "구조화 = 무조건 정확"이 아니다.

**교훈**: 구조화의 이득은 *다중 홉 추적*(누가 호출 → 무엇이 깨짐 → 어디로 흐름)에 집중된다. 1홉·소형 작업은 [[First_Grep_실전사례]]처럼 grep·raw가 우위다. 도구 효용은 정직하게 측정하고 적용 구간을 가려 쓴다 — 이는 [[LLM_통제_철학_6대원칙]] 원칙 1(토큰 1급)의 "동작당 토큰" 회계를 도구 선택 자체에 적용하는 것이다.

## 설치 종속성

[[L1_Hard_Gate_훅체계]]의 `codegraph-gate.sh`가 codegraph MCP에 **완전 종속**이다. codegraph 미설치 환경에서는 L1 차단이 작동하지 않아 보장률이 0%로 회귀한다.

### 설치 5단계

```
1. npm install -g @codegraph/cli      (CLI)
2. claude mcp add codegraph -- codegraph mcp   (MCP 등록)
3. cd <project_root> && codegraph init -i     (.codegraph/ 생성 + 인덱싱)
4. echo ".codegraph/" >> .gitignore           (저장소 오염 방지)
5. codegraph_status로 검증
```

각 프로젝트 루트마다 별도 `.codegraph/`가 필요하다. 글로벌 인덱스는 지원하지 않는다.

### 생성 산출물

```
<project_root>/
  .codegraph/
    db.sqlite       ← 심볼 인덱스 (tree-sitter 결과)
    config.json     ← 인덱싱 설정
    .gitignore
```

## 자주 쓰는 체인

### "이 기능이 어떻게 동작하나?" (탐색)

```
codegraph_context (영역 종합)
  ↓
codegraph_explore (핵심 심볼 묶음 소스)
  ↓
(보완 시) codegraph_node / Read
```

3번 호출 안에 답이 나온다. grep+Read 루프로 같은 답에 가려면 수십 번 필요하다.

### "X에서 Y로 어떻게 흐르나?" (트레이스)

```
codegraph_trace X → Y (한 번에 경로 전체)
  ↓
codegraph_explore (경로 위 심볼들 본문)
```

`codegraph_search` + `codegraph_callers` 루프로 경로를 재구성하지 않는다 — trace 한 호출이 동적 hop까지 잇는다.

### "Z 변경하면 뭐가 깨지나?" (안전성)

```
codegraph_impact Z (파급 범위)
  ↓
codegraph_callers Z (회귀 점검 대상)
```

[[RIPER_5단계_상태머신]]의 Review 단계에서 이 체인이 표준화된다 ([[Workflow_Ecosystem_버전계보]] v3.5).

## 인덱스 신뢰성 주의사항

- 파일 변경 후 ~500ms debounce 동안 인덱스가 lag한다. 같은 턴에 Edit→codegraph 재조회는 stale 결과를 받을 수 있다.
- `.codegraph/`가 부재하면 "not initialized" 응답. 사용자에게 `codegraph init -i` 제안.
- 인덱스 크기가 0이면 언어 지원 확인 (`codegraph languages`).

## 관련 노트

- 차단 메커니즘: [[L1_Hard_Gate_훅체계]]
- 사용 규약: [[Sonar_Protocol]]
- 보완 인덱스 (1단계 유산): [[Dictionary_md_좌표_시스템]]
- 진입 예산 규약(최소→확대): [[최소컨텍스트_진입규약]]
- 진화 맥락: [[Workflow_진화_3단계]]
- 토큰 통제 근거: [[LLM_통제_철학_6대원칙]]

## 출처

- raw/workflow_policy_change_notification.md (2026-05-28 유입) — § 0-2/0-3 codegraph 도입 및 의무 설치
- raw/CHANGELOG.md (2026-05-28 유입) — v3.4 codegraph L1 강제 도입 배경
- raw/code-review-graph_입국심사.md (2026-06-16 편입) — Atom 4 벤치마크 정직성(순환 ground truth·소형 변경 역효과·MRR 0.35). docs/Try_AtomImport_DLC_vs_Workflow 결론(C분류=위키 노트)에 따른 편입
