---
tags: [llm-wiki, llm-워크플로우, 에이전트]
date_created: 2026-05-22
last_modified: 2026-05-22
---

# 3-Tier 에이전트 스튜디오

[[LLM_워크플로우_생태계]]의 4대 서브시스템 중 가장 큰 모듈. 비용·역할·책임을 *Tier*로 분리해 [[LLM_컨텍스트_5대_문제]] 5번(에이전트 디스패치 혼란)을 구조적으로 푼다.

## Tier 구조

```
Tier 1 (Opus, maxTurns 30) — 의사결정·조율
  producer            (멀티에이전트 허브)
  creative-director   (디자인 비전)
  technical-director  (기술 아키텍처)

Tier 2 (Sonnet, maxTurns 25) — 구현 총괄
  lead-programmer     (C# 피처 구현 리드)
  unity-specialist    (Unity 생태계)

Tier 3 (Sonnet/Haiku, maxTurns 20) — 실행·검증·문서화
  quality-sentinel    (품질 게이트)
  reporter            (이력 기록)
  writer              (PRD·플랜 작성)
  도메인 전문가들       (gameplay, shader, UI, perf 등)
```

Tier 1·2·3은 각각 책임 *높이*가 다르다. 세부 Unity 에이전트 16개 풀세트는 [[Unity_고정_스튜디오_구조]]를 본다. 세 고정 에이전트(producer/quality-sentinel/reporter)는 [[Producer_QualitySentinel_Reporter_게이트]]에서 단독으로 다룬다.

## 왜 3-Tier인가

### 비용·정확도의 균형

- Opus는 비싸지만 추론력이 강함 → *결정*에만 사용
- Sonnet은 저렴하고 빠름 → *실행·검증*에 사용
- 둘을 무차별 섞으면 비용 폭발, 분리하면 합리적

### 책임 경계의 명확성

- Tier 1 = *무엇을* 할지 결정
- Tier 2 = *어떻게* 할지 조율
- Tier 3 = *실제로* 수행

각 에이전트가 자기 Tier 밖의 일을 하면 위반으로 간주된다. 이 강제는 [[LLM_통제_철학_6대원칙]]의 "Single Responsibility per Role" 원칙의 직접 구현이다.

## 소통 경로 (Delegation Map)

```
사용자
  └→ producer (Tier 1)
       ├→ creative-director → writer (PRD/플랜)
       │                    → technical-director → prototyper
       ├→ technical-director → lead-programmer / unity-specialist / ...
       ├→ lead-programmer → gameplay-programmer / engine-programmer / systems-designer
       └→ [구현 에이전트 완료] → quality-sentinel → reporter → producer
```

사용자는 오직 producer와만 직접 소통한다. 이는 [[Mastermind_Architecture_Manifesto]]가 말하는 "통제실의 단일 인터페이스" 원칙의 인적 구현이다.

## Collaboration Protocol (공통 6단계)

모든 에이전트가 따르는 코드 작성 전 체크리스트:

1. 기존 코드·문서 파악 — 관련 파일 탐색, 기존 패턴 확인
2. 아키텍처 질문 — 설계 결정 지점마다 질문 (한 번에 하나)
3. 구조 제안 — 구현 전 클래스 구조·데이터 흐름·트레이드오프 제시
4. 투명한 구현 — 스펙 모호성 발견 시 STOP 후 질문
5. 파일 쓰기 전 승인 — "이를 [파일경로]에 작성해도 될까요?"
6. 다음 단계 제안 — 구현 완료 후 테스트·리뷰 옵션 제시

핵심 사상: *협력적 구현자, 자율 코드 생성기가 아니다.* 모든 아키텍처 결정과 파일 변경은 사용자가 승인한다.

## 라우팅 규칙 (자동 vs Producer 경유)

| 작업 유형 | 라우팅 | 이유 |
|---|---|---|
| 단순 질문·코드 설명·소형 버그픽스 | 전문가 직접 | 콜드 스타트 비용 회피 |
| 구현 착수·멀티에이전트·아키텍처 결정 | Producer 경유 | 결재·조율 필요 |
| 세션 완료 conclusion.md | Producer 경유 | 단일 인터페이스 강제 |

판단 기준: *파급 범위가 한 파일·한 에이전트를 초과하면 Producer 경유.* 자세한 규모별 워크플로는 [[작업_규모별_워크플로]]를 본다.

## 비Unity 프로젝트의 자유 설계

Tier 3 전문가는 프로젝트 도메인에 맞춰 최대 8개까지 자유 구성한다. 단 producer / creative-director / technical-director / lead-programmer / quality-sentinel / reporter / writer 일곱 자리는 *모든 프로젝트에서 고정*이다. Unity 프로젝트는 16개 전문가가 고정되며 자유 설계 단계를 건너뛴다 → [[Unity_고정_스튜디오_구조]].

## 관련 노트

- 게이트 에이전트 3종 단독 분석: [[Producer_QualitySentinel_Reporter_게이트]]
- Unity 풀세트: [[Unity_고정_스튜디오_구조]]
- 규모별 절차: [[작업_규모별_워크플로]]
- 상태머신 통합: [[RIPER_5단계_상태머신]]

## 출처

- raw/Workflow-Design-Philosophy.md (2026-05-22 유입) — §5 3-Tier Agent Studio
- raw/ecosystem-atomic-analysis.md (2026-05-22 유입) — §1 3-Tier 에이전트 코워크 스튜디오
- raw/generic-3tier-setup-prompt.md (2026-05-22 유입) — STEP 1~6 설치 가이드
