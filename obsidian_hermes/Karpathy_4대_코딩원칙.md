---
tags: [llm-wiki, 외부사상, 코딩원칙, 설계원칙]
date_created: 2026-05-22
last_modified: 2026-05-22
---

# Andrej Karpathy 4대 코딩 원칙

LLM 기반 코드 작성·수정 작업에서 *적용·확인·검증* 사이의 사이클을 단단히 잡기 위한 외부 일반 원칙. [[LLM_통제_철학_6대원칙]]이 본 vault 내부의 운영 철학이라면, 본 4원칙은 그 운영 철학이 *코드 변경 단위*에서 어떻게 행동으로 환원되는지를 다룬다.

## 원칙 1. Think Before Coding — 가정 표면화

> "Don't assume. Don't hide confusion. Surface tradeoffs."

- 구현 시작 전 *문제 정의 / 비목표 / 성공 기준 / 영향 파일*을 먼저 명시
- 해석이 여러 갈래면 *옵션과 트레이드오프*를 먼저 제시, 임의 선택 금지
- 불확실한 요건은 *추정으로 덮지 않고* 재질문 우선
- 더 단순한 방법이 있으면 발화

이 원칙은 [[RIPER_5단계_상태머신]]의 RESEARCH·PLAN 단계가 구조적으로 강제하려는 행동의 *추상 진술*이다.

## 원칙 2. Simplicity First — 요청된 것만

> "Minimum code that solves the problem. Nothing speculative."

- 요청을 충족하는 *최소 변경*만 수행
- 단일 사용 코드에 *추상화·미래 대비 설정·미요청 기능* 추가 금지
- 200줄로 길어지면 50줄로 다시 줄임 — 시니어 엔지니어가 "과설계"라 말할 만하면 단순화
- "Would a senior engineer say this is overcomplicated?" 가 자기 점검 질문

[[Mastermind_Architecture_Manifesto]]의 *카파시 정신*이 같은 사상을 비유적으로 진술한다.

## 원칙 3. Surgical Changes — 인접 코드 무수정

> "Touch only what you must. Clean up only your own mess."

- 요청 범위 밖 *리팩토링·스타일 정리·주변 코드 개선* 금지
- 기존 dead code는 *발견 보고만*, 삭제 금지
- 변경으로 *내가 만든* orphan(unused import/변수/함수)만 정리
- 기존 코딩 스타일과 다르더라도 일치시킴
- 검증 기준: *변경된 모든 줄이 사용자 요청으로 직접 추적 가능해야 한다*

본 원칙의 *시행 메커니즘*은 [[Block_Assembly_Part_Piece_컨벤션]]의 §"Surgical Changes 강제" 절에 코드 어노테이션 수준에서 구현돼 있다 — Part 교체 시 *해당 파일만* 수정.

## 원칙 4. Goal-Driven Execution — 검증까지 반복

> "Define success criteria. Loop until verified."

- 작업을 *검증 가능한 목표*로 변환
- 다단계 작업은 짧은 계획으로 쪼개 각 단계의 확인 방법 명시
- 구현 직후 *컴파일·진단·재현 시나리오*로 결과 확인, 통과까지 반복

이 사이클은 [[Producer_QualitySentinel_Reporter_게이트]]의 3-Phase 워크플로(Phase 2 검증 루프)에 *게이트* 형태로 결정론적으로 박혀 있다.

## 작업 시작 체크리스트

| 항목 | 확인 |
|---|---|
| 문제 정의가 한 문장으로 고정되었는가 | ☐ |
| 비목표(하지 않을 것)가 명시되었는가 | ☐ |
| 성공 기준이 검증 가능하게 정의되었는가 | ☐ |
| 영향 파일이 명확한가 | ☐ |
| 변경이 최소 범위인가 | ☐ |

원칙이 작동하고 있다는 신호:
- diff에서 *불필요한 변경 감소*
- 과설계로 인한 *재작성 감소*
- 실수 후 사후 질문이 아니라 구현 *전*의 명확화 질문이 늘어남

## [[LLM_통제_철학_6대원칙]] 과의 매핑

| Karpathy 4원칙 | 본 vault의 대응 |
|---|---|
| 1. Think Before Coding | 6대 원칙 ②~③ (외부화·훅 강제) — 가정 표면화를 *훅·게이트*로 결정론화 |
| 2. Simplicity First | 6대 원칙 ⑤ (단일 책임) — 역할당 책임 1개로 단순성 강제 |
| 3. Surgical Changes | [[Block_Assembly_Part_Piece_컨벤션]] — 어셈블 단위 교체로 인접 무수정 강제 |
| 4. Goal-Driven Execution | 6대 원칙 ⑥ + [[Producer_QualitySentinel_Reporter_게이트]] — 검증 게이트 직렬화 |

Karpathy 4원칙이 *행동 권고* 수준이라면, 본 vault의 6원칙·게이트·어노테이션은 그 권고를 *프롬프트 신뢰 없이* 결정론적으로 시행하는 방식을 다룬다. 즉 4원칙은 *공리*, 6원칙·게이트는 그 *시행 체계*다.

## 관련 노트

- 내부 운영 철학: [[LLM_통제_철학_6대원칙]]
- 행동 단계 매핑: [[RIPER_5단계_상태머신]]
- Surgical Changes 시행: [[Block_Assembly_Part_Piece_컨벤션]]
- 검증 게이트: [[Producer_QualitySentinel_Reporter_게이트]]
- 같은 사상 비유: [[Mastermind_Architecture_Manifesto]]

## 출처

- raw/Andrej Karpathy Skills.md (2026-05-22 유입) — 4원칙 원본 정의·작업 시작 체크리스트
