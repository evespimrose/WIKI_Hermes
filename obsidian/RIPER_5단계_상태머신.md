---
tags: [llm-wiki, llm-워크플로우, 상태머신]
date_created: 2026-05-22
last_modified: 2026-06-17
---

# RIPER 5단계 상태머신

[[LLM_워크플로우_생태계]]의 4대 서브시스템 중 *단계화된 사고*를 담당하는 모듈. 일반적으로 "카파시(Karpathy) 방식"으로 불리는 단계적·측정 중심 개발 철학을 Claude Code 워크플로우로 구현한 것이다. 핵심 사상: *먼저 이해하고, 측정하고, 단순하게 시작하고, 단계별로 검증한다.*

## 5단계 구조

```
RESEARCH → INNOVATE → PLAN → EXECUTE → REVIEW
 (읽기)    (브레인스토밍)  (명세)   (구현)   (검증)
```

각 단계는 명시적 슬래시 명령으로만 전환되며, 전환 시 `.claude/memory-bank/.riper-state` 파일이 갱신된다. 이 파일이 [[4계층_메모리_아키텍처]] L2 계층의 본체다.

## 단계별 권한 매트릭스

| 모드 | Read | Source Write | Bash Exec | Plan Docs |
|---|---|---|---|---|
| RESEARCH | ✅ | ❌ | ❌ | ❌ |
| INNOVATE | ✅ | ❌ | ❌ | ❌ |
| PLAN | ✅ | ❌ | ❌ | ✅ |
| EXECUTE | ✅ | ✅ | ✅ | ❌ |
| REVIEW | ✅ | review docs만 | ✅ (verify) | ❌ |

권한이 *상승적이지 않다*. EXECUTE는 plan docs를 쓸 수 없고, PLAN은 소스를 쓸 수 없다. 단계 간 권한이 명확히 분리되어 있어 [[LLM_컨텍스트_5대_문제]] 2번(환각)이 권한 위반의 형태로 빠르게 감지된다.

## 왜 모드를 강제하는가

자유로운 LLM은 다음 실수를 한다:

- **연구 단계에서 코드를 수정** → 사용자의 검토 기회 박탈
- **플랜 없이 구현** → 방향 잃음 → 재작업
- **구현 직후 다음 작업으로 점프** → 검증 누락 → 결함 누적

RIPER는 *단계 간 전환을 명시적 행위*로 만든다. 모드 변경에는 사용자의 슬래시 명령이 필요하다. 이 설계는 [[LLM_통제_철학_6대원칙]] 6번(Scope-Differentiated Gates)과 결합해 *체계적 사고를 시스템 차원에서 강제*한다.

## Pre-Flight Check — EXECUTE 진입 차단

`/riper:execute` 호출 시 다음을 검증한다:

```
1. .riper-state 읽기
2. PLAN_FILE 필드 확인
3. PLAN_FILE이 비어 있거나 파일 부재 → STOP
   "Complete /riper:plan first"
```

→ *플랜 없는 구현*을 구조적으로 차단. 이는 [[Producer_QualitySentinel_Reporter_게이트]] quality-sentinel의 Phase 1 RIPER 감사와 짝을 이룬다.

## 두 가지 모드 변형

| 명령 | 역할 |
|---|---|
| `/riper:strict` | RIPER 프로토콜 엄격 강제 — 각 단계 금지 행동 즉시 차단 |
| `/riper:workflow` | R→I→P→(승인 게이트)→E→R 전체 플로우 자동 안내 |

## 플랜 파일 저장 규약

```
.claude/memory-bank/{branch}/plans/YYYY-MM-DD-{작업명}.md
```

작성 주체: writer 에이전트. 감사 주체: quality-sentinel. *작성·감사의 분리*는 [[LLM_통제_철학_6대원칙]] 5번(Single Responsibility) 원칙의 RIPER 적용.

## PLAN 태스크 세분화 — 2~5분 단위

PLAN 단계의 플랜은 *실행 가능*해야 한다. 좋은 세분화 기준은 **각 태스크가 2~5분 단위**로 떨어지고, **모든 단계에 placeholder가 아닌 실제 코드/명령**이 들어가는 것이다. "여기에 로직 추가" 같은 빈칸은 EXECUTE에서 다시 추론을 유발해 환각을 부른다 — placeholder 금지가 곧 [[위키_저장_5대필터]]의 품질 기준을 플랜에 적용한 것.

단 세분화는 *비용*이다. 더 잘게 쪼갤수록 PLAN 단계 토큰이 +20~50% 늘어난다. 한 줄 버그픽스에 2~5분 태스크 분해를 강제하면 과하다 — [[작업_규모별_워크플로]]의 중·대형 플랜에만 적용하고, 소형은 직접 처리한다. EXECUTE의 실행 가능성과 PLAN의 작성 비용 사이의 균형점이다.

## RULE-7 — 플랜의 좌표 정밀화

RIPER 플랜의 모든 Action Item은 BLK 좌표를 의무화한다. 자세한 내용은 [[RULE7_PRD_Spatial_Mapping]]을 본다. 좌표 없는 플랜은 [[LLM_컨텍스트_5대_문제]] 3번(토큰 폭발)을 EXECUTE 단계에서 트리거하기 때문.

## 단계 누락의 비용

RIPER 5단계 전체를 진행하는 비용은 *단순 작업 비용의 수십 배*다. 그래서 [[작업_규모별_워크플로]]는 *플랜 파일이 없는 소형 작업*에 대해 RIPER 풀사이클을 명시적으로 건너뛴다. 절차의 비용이 절차의 가치를 초과하지 않도록.

## 관련 노트

- 좌표 강제: [[RULE7_PRD_Spatial_Mapping]]
- 사전 타당성 검증: [[Try_Skill_타당성_검증]]
- 감사 에이전트: [[Producer_QualitySentinel_Reporter_게이트]]
- 규모별 적용: [[작업_규모별_워크플로]]
- 상태 영속화: [[4계층_메모리_아키텍처]] L2
- 컴팩션 시 보호: [[컴팩션_생존_전략]]
- REVIEW 단계 증거 규약: [[증거_기반_완료_검증]]
- RESEARCH의 디버깅 특화: [[루트_원인_우선_디버깅]]
- 단계 분리의 사고 레벨 확장: [[사고_외재화_패턴]]

## 출처

- raw/Workflow-Design-Philosophy.md (2026-05-22 유입) — §4 RIPER 워크플로우
- raw/ecosystem-atomic-analysis.md (2026-05-22 유입) — §4 RIPER 원자 목록
- raw/superpowers_입국심사.md (2026-06-17 편입) — Atom 5 TDD 강제 계획 작성(2~5분 태스크 단위·placeholder 금지)
