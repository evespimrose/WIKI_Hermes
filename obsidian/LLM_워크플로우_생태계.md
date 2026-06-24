---
tags: [llm-wiki, hub, llm-워크플로우]
date_created: 2026-05-22
last_modified: 2026-06-14
---

# LLM 워크플로우 생태계 (Hub)

이 vault의 최상위 허브 노트. 비결정론적(stochastic) LLM을 결정론적 인프라로 통제해 장기 운용에서 토큰 효율과 일관성을 유지하기 위한 워크플로 생태계 전체의 진입점이다.

## 한 줄 요약

LLM의 컨텍스트 윈도우를 한정 자원으로 간주하고, 그 자원의 낭비를 구조적으로 차단하기 위한 모든 장치의 집합. 토큰 절약, 환각 차단, 세션 연속성, 다중 AI 협업이 풀고자 하는 4대 문제다.

## 세 행성 (그래프 진입점)

본 항성 아래에 세 행성이 위성들을 클러스터링한다. 영역별 위성 목록은 각 행성 노트에서 다룬다.

- [[Token_허브]] — 토큰 통제 + 워크플로우 영역 (28 위성)
- [[RX_1_허브]] — RX_1 프로젝트 인스턴스 영역 (11 위성)
- [[Wiki_허브]] — vault 자체 운영 정책 영역 (3 위성)

행성 간 cross-link(예: `Sonar_Protocol` ↔ `First_Grep_실전사례`)는 그대로 유지되어, 그래프 뷰에서는 행성 클러스터 + 행성 간 *별다리*가 동시에 보인다.

## 핵심 진입점

이 시스템의 존재 이유를 이해하려면 먼저 [[LLM_컨텍스트_5대_문제]]를 보고, 이어서 그에 대한 응답인 [[LLM_통제_철학_6대원칙]]을 읽는다. 같은 철학을 보다 비유적·선언적 어조로 진술한 글은 [[Mastermind_Architecture_Manifesto]]에 있다.

## 4대 서브시스템

생태계는 직교하지만 상호 보강하는 네 개의 서브시스템으로 분해된다.

| 서브시스템 | 풀어주는 문제 | 진입 노트 |
|----|----|----|
| 3-Tier Agent Studio | 에이전트 디스패치 혼란·역할 모호성 | [[3Tier_에이전트_스튜디오]] |
| Dictionary-First Search | 토큰 비용 폭발·환각 탐색 | [[Sonar_Protocol]] / [[Dictionary_md_좌표_시스템]] |
| doc-context 입력 | 매 턴 지시문 재전송·외부 AI 환각 | [[doc_context_입력_워크플로우]] |
| RIPER 상태머신 | 플랜 없는 구현·단계 누락 | [[RIPER_5단계_상태머신]] |

각 서브시스템은 부분 설치 가능하며 일부는 독립 사용도 가능하다. 결합도와 분리 가능성은 각 노트에서 다룬다.

## 진화 3단계와 현재 위치

이 생태계는 정적이지 않다. [[Workflow_진화_3단계]]가 추적하는 3세대 진화 위에 현재 단계가 얹혀 있다:

- **1단계** — 로컬 dictionary 의존 (수기 인덱스, 탈옥 취약)
- **2단계** — codegraph 도입 + L1~L5 다중 방어선 (물리적 차단, BUT 토큰 +827/턴)
- **3단계** — 외부 Wiki + 최적화 L1 (-62% 토큰, 94% 보장률, 현재)

각 세대의 정량 효과 누적은 [[Workflow_Ecosystem_버전계보]]에 v3.0~v3.5로 기록된다. 본 wiki 자체가 3단계의 "외부 Wiki" 축이며, [[LLM_Wiki_운영체계]]가 그 운영 인프라다.

## 코드 인텔리전스 & 강제 레이어

3단계에서 추가된 두 핵심 레이어 — Dictionary-First Search 서브시스템과 직교 보완:

- [[Codegraph_MCP_통합]] — tree-sitter 기반 sub-ms 심볼 그래프 (현재의 primary 인덱스)
- [[L1_Hard_Gate_훅체계]] — PreToolUse hook 트리오 (텍스트 규칙의 LLM 무시 불가능)
- [[L1_L5_다층방어선_역사]] — 5중 → 1+1+외부의 절충 과정

## Wiki 관리 인프라

[[LLM_Wiki_운영체계]] — 지식 저장소의 3단계 파이프라인 (move-to-raw, compile-wiki, archive)
[[Git_기반_다중PC_동기화]] — obsidian/ 동기화 전략 및 다중 PC 워크플로우
[[LLM_Wiki_지식자산_현황]] — 현재 축적된 노트의 맵핑 및 진화 방향

## 보강 계층

서브시스템들을 떠받치는 공통 인프라:

- 상태의 외부화: [[4계층_메모리_아키텍처]]
- 컴팩션 생존: [[컴팩션_생존_전략]]
- 모듈 단위 어노테이션: [[Block_Assembly_Part_Piece_컨벤션]] / [[BLK_좌표_시스템]]
- 작업 규모 분기: [[작업_규모별_워크플로]]
- 외부 AI 협업: [[External_AI_역할분리]]
- 게이트 에이전트: [[Producer_QualitySentinel_Reporter_게이트]]

## 어디서부터 읽을지

처음 접한다면 다음 순서를 권한다:

1. [[LLM_컨텍스트_5대_문제]] — 왜 이 시스템이 필요한가
2. [[LLM_통제_철학_6대원칙]] — 어떤 가치관으로 풀었는가
3. [[3Tier_에이전트_스튜디오]] — 가장 큰 서브시스템의 골조
4. [[Sonar_Protocol]] — 가장 잘 작동하는 단일 규칙
5. [[RIPER_5단계_상태머신]] — 작업 진행의 표준 절차

## 출처

- raw/Workflow-Design-Philosophy.md (2026-05-22 유입)
- raw/ecosystem-atomic-analysis.md (2026-05-22 유입)
- raw/gemini-code-1779431417344.md (2026-05-22 유입)
- raw/dictionary-first-grep-workflow.md (2026-05-22 유입)
- raw/generic-3tier-setup-prompt.md (2026-05-22 유입)
- raw/modular-architecture.md (2026-05-22 유입)
