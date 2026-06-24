---
tags: [llm-wiki, 워크플로우, 역사, 아키텍처]
date_created: 2026-05-28
last_modified: 2026-05-28
---

# Workflow 진화 3단계

LLM 코드 탐색 워크플로우의 3세대 진화. 로컬 dictionary 의존 → codegraph + L1~L5 다중 방어선 → 외부 Wiki + 최적화 L1. 각 단계의 한계가 다음 단계의 도입 계기가 됐다.

## 1단계: 로컬 dictionary 의존 (Legacy, ~2026-05-27 이전)

### 구조

저장소마다 `manage/dictionary.md` 한 파일에 모든 심볼·BLK 위치를 *사람이 수기*로 관리. Claude 세션은 dictionary 조회 → Read/Grep 3단계로 탐색.

```
사용자: FlowController.HandlePhase1Confirm 찾아줘
  ↓
Claude: dictionary.md 열어 BLK-001 확인
  ↓
Claude: Read(FlowController.cs)
  ↓
Claude: 전체 파일 로드 후 텍스트 검색
```

[[Dictionary_md_좌표_시스템]]이 이 단계의 핵심 자산.

### 한계

| 문제 | 설명 |
|---|---|
| 수기 동기화 부담 | 파일 이동·리팩터링 시 dictionary 수동 갱신. 누락 즉시 탐색 오류 |
| 관계 정보 부재 | "무엇이 이 함수를 호출?", "이 변경이 무엇을 깨나?" 파악 불가 |
| 저장소 간 단절 | 각 저장소 독립 dictionary → 공유 지식 없음 |
| 탈옥 취약 | dictionary 미조회 후 `find`/`grep -r` 패턴 반복 발생 |
| 구조 정보 한계 | 시그니처·상속·의존 관계를 텍스트만으로 표현 |

특히 *탈옥 취약성*이 누적되어 세션당 3회 이상 위반이 관측됐다. 텍스트 규칙(CLAUDE.md)만으로는 LLM의 attention drop을 막을 수 없다는 결론이 2단계 도입의 직접 계기.

## 2단계: Codegraph + L1~L5 다중 방어선 (2026-05-27)

### 도입된 두 축

**축 A — 코드 인텔리전스**: codegraph MCP ([[Codegraph_MCP_통합]])
- tree-sitter 기반 자동 파싱
- `codegraph_context/callers/impact` 체인으로 관계 정보 확보
- sub-ms 조회

**축 B — 물리적 차단**: L1~L5 다중 hook ([[L1_L5_다층방어선_역사]])
- L1 Hard Gate가 `find`/`grep -r`을 PreToolUse에서 봉쇄
- 텍스트 규칙의 LLM 무시 불가능 (hook은 OS 레벨)

### 효과와 새로운 문제

| 측면 | 효과 |
|---|---|
| 관계 정보 | codegraph로 확보 (1단계 한계 해소) |
| 탐색 차단 | hook으로 물리 강제 (보장률 99.2%) |
| 토큰 비용 | 매 턴 +827 (L2/L4/L5 누수) |
| 정책 분산 | 11개 파일 관리 부담 |

L2/L4/L5는 L1과 *shadow 관계*임이 드러났다 — L1이 즉시 차단하므로 L2 안내·L4 사후통지·L5 매 턴 reminder는 효과 미미하면서 토큰만 소비.

## 3단계: 외부 Wiki + 최적화된 L1 (2026-05-27, 최적화 이후)

### 동시 진화 두 축

**축 A — 정책 최적화**:
- L2/L4 제거, L5는 trae context-sharer로 외부 이전
- 결과: 턴당 토큰 +827 → +310 (-62%), 정책 파일 11 → 5
- 보장률 99.2% → 94% (5%p 감수)
- 자세한 절충 과정은 [[L1_L5_다층방어선_역사]]

**축 B — 외부 Wiki 통합** (`D:\Fork\WIKI\obsidian\`):
- 폐쇄적 저장소 문서 → 개방형 지식 공유
- 설계 결정·컨벤션·워크플로우의 Single Source of Truth
- 저장소 간 컨벤션 동기화: RX_1 변경이 WIKI에 반영 → 다른 프로젝트에도 적용 가능
- 이 wiki 운영 체계는 [[LLM_Wiki_운영체계]]가 다룬다

### 현재 메모리 아키텍처

```
L1: CLAUDE.md + session-start.sh         ← 세션 즉시 주입
L2: .claude/memory-bank/.riper-state     ← RIPER 상태
L3: /memory:save|recall                  ← 장기 기억
L4: manage/dictionary.md                 ← 구조 인덱스 (보완용)
L5: D:\Fork\WIKI\obsidian\               ← Single Source of Truth
코드 인텔리전스: codegraph MCP            ← 실시간 심볼 그래프
```

이 5계층은 [[4계층_메모리_아키텍처]]의 진화형이다. L5의 외부 wiki 위치 부여가 이번 단계의 새로움.

## 진화 도식

```
1단계 (Legacy):
  로컬 dictionary.md 단일 의존
  └─ 수기 동기화, 관계 정보 없음, 탈옥 취약

      ↓ (탈옥 누적 → 텍스트 규칙 한계 인식)

2단계 (Multi-Defense):
  codegraph + L1~L5 5중 방어선
  └─ 물리적 차단, 구조 조회 가능, BUT 토큰 +827/턴

      ↓ (shadow 관계 발견 + 토큰 비용 부담)

3단계 (Current):
  외부 Wiki + 최적화 L1 + L3 + 외부 이전 L5
  └─ 개방형 지식 공유, -62% 토큰, 94% 보장률
```

## 각 단계가 남긴 자산

- 1단계 → [[Dictionary_md_좌표_시스템]] (보완용으로 잔존)
- 2단계 → [[Codegraph_MCP_통합]], [[L1_Hard_Gate_훅체계]] (현재 핵심)
- 3단계 → 본 wiki 전체 ([[LLM_Wiki_지식자산_현황]])

폐기된 것이 아니라 *재배치*됐다는 점이 중요하다. dictionary는 더 이상 primary 인덱스가 아니지만 [[manage_폴더_역할분리]]에서 정의한 5파일 DB의 한 축으로 유지된다.

## 다음 진화 후보 (4단계 추정)

[[Mastermind_Architecture_Manifesto]]가 그리는 미래 단계:
- Self-Healing Wiki (dictionary 자동 갱신 초안 제안)
- Mastermind 자율 오케스트레이션 (스킬 라우팅 자동화)
- Multi-Vault 연합 (프로젝트 간 wiki 동기화)

4단계는 현재의 정량적 절감을 넘어 *자동화 수준*의 도약이 핵심.

## 관련 노트

- 1단계 자산: [[Dictionary_md_좌표_시스템]]
- 2단계 자산: [[Codegraph_MCP_통합]], [[L1_Hard_Gate_훅체계]]
- 2→3단계 절충: [[L1_L5_다층방어선_역사]]
- 3단계 wiki 인프라: [[LLM_Wiki_운영체계]], [[LLM_Wiki_지식자산_현황]]
- 버전 이력: [[Workflow_Ecosystem_버전계보]]
- 4단계 비전: [[Mastermind_Architecture_Manifesto]]

## 출처

- raw/workflow_policy_change_notification.md (2026-05-28 유입) — § 0 워크플로 진화 3단계
- raw/CHANGELOG.md (2026-05-28 유입) — 버전별 진화 누적
