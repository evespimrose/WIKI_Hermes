---
tags: [llm-wiki, 행성허브, rx1]
date_created: 2026-05-29
last_modified: 2026-06-14
---

# RX_1 허브

RX_1 3D Pipe Pathfinding 프로젝트 영역의 모든 노트를 묶는 행성. vault root에서의 진입점이며, RX_1 폴더 내부 실무 인덱스인 [[RX_1_인덱스]]와 역할이 다르다 — 본 노트는 *외부 진입용 행성*, 그쪽은 *내부 운영 인덱스*.

상위 항성 [[LLM_워크플로우_생태계]]에서 진입한다. 인접 행성은 [[Token_허브]]·[[Wiki_허브]].

## 행성 정의

[[Token_허브]]가 정의한 일반 도구(Sonar, Dictionary, Codegraph, RIPER)가 한 Unity 프로젝트에 *어떻게 구체화되는가*의 사례 모음. 일반 패턴과 프로젝트 인스턴스를 분리해두면 다른 프로젝트도 같은 구조로 노트를 키울 수 있다.

## 위성 카탈로그

### 진입

- [[RX_1_인덱스]] — RX_1 폴더 내부 실무 인덱스 (6대 상태 노트, 현재 진행 상태)

### DB 스키마

- [[RX_1_manage_DB_스키마]] — 5파일 통합 DB 인스턴스, BLK-001~013

### 상태 추적 (6대 상태 노트)

- [[state_claude_mem]] — 아키텍처 메모리 스냅샷
- [[state_riper]] — RIPER 상태머신 현 위치
- [[state_plan]] — 활성 플랜 + 기술 결정 이력
- [[state_dictionary]] — BLK 인덱스 (Sonar Protocol 조회 기준)
- [[state_query_logs]] — 트레이드오프 + 미결 질문
- [[state_update_history]] — 다운그레이드 이력 + 롤백 레시피

### 컨벤션

- [[code_style_lexicon]] — 코드 스타일 어휘집

### Graveyard (폐기 패턴 박제)

- [[Graveyard_안티패턴_원칙]]
- [[export-graveyard-log_스킬명세]]

## RX_1과 일반 패턴의 대응

| 일반 (Token 행성 위성) | RX_1 인스턴스 |
|---|---|
| [[manage_폴더_역할분리]] (5파일 패턴) | [[RX_1_manage_DB_스키마]] (BLK-001~013 적용) |
| [[Block_Assembly_Part_Piece_컨벤션]] | RX_1 SortJob Assembly, Burst/MainThread Part |
| [[Dictionary_md_좌표_시스템]] §0~§7 | RX_1 dictionary § 0 / 0-1 / 1 / 2 / 3 (단순화) |
| [[Sonar_Protocol]] RULE 1~3 | RX_1에서 find/rg/fd 금지 + Glob/Grep 허용 |
| [[RIPER_5단계_상태머신]] | `.claude/memory-bank/.riper-state` |

다른 프로젝트가 같은 패턴을 채택하면 `XXX_manage_DB_스키마.md`, `XXX_허브.md` 형태로 동일 구조 노트가 추가될 수 있다.

## 인접 행성으로의 통로

- [[Token_허브]] — 일반 워크플로우 도구의 본거지 (이곳의 적용 대상)
- [[Wiki_허브]] — 본 행성의 노트가 보관·동기화되는 메타 인프라
