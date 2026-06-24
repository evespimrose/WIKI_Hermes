---
tags: [llm-wiki, llm-워크플로우, 매니페스토]
date_created: 2026-05-22
last_modified: 2026-06-14
---

# Mastermind Architecture Manifesto

[[LLM_워크플로우_생태계]] 전체를 설계자의 관점에서 선언적으로 진술한 매니페스토. 동일한 시스템을 [[LLM_통제_철학_6대원칙]]은 분석적으로, 이 문서는 비유적·철학적 어조로 다룬다. 부제는 "Determinism over Stochasticity: A Blueprint for Sovereign LLM Control".

## 핵심 비유: 기계식 통제 섀시 (Mechanical Control Chassis)

AI의 자율성을 억압하는 감옥이 아니라, 비결정론적 지능이 가질 수 있는 *최상의 정밀도와 반복 가능성*을 확보하기 위해 정밀하게 설계된 고도화된 기계식 통제 섀시. 야생성을 자유도라는 이름으로 방임하지 않고, 철저히 통제된 기계식 레일 위에 가둔다.

## 세 가지 설계 철학

### 결정론적 인터페이스를 통한 비결정론의 지배 (Deterministic Harnessing)

LLM의 확률적 판단을 신뢰하지 않는다. 에이전트가 조작할 수 있는 환경을 규격화된 물리적 계기판 — Spatial BLK 태그([[BLK_좌표_시스템]]), `.riper-state`([[RIPER_5단계_상태머신]]), 하드웨어 훅 스크립트 — 으로 한정한다. AI는 통제실 내부의 레버만 당기며, 레버 작동 결과는 기계적으로 예측 가능해야 한다.

### 카파시 정신의 기계적 강제 (Automated Karpathy-Mindset)

안드레 카파시의 'Think Before Coding', 'Simplicity First', 'Surgical Changes'는 도덕적 지침이 되어서는 안 된다. 시스템 프롬프트와 가드레일 쉘 스크립트(`sonar-guard.sh`, `write-approval-reminder.sh`)로 물리적으로 강제해 에이전트가 *최소한의 변경으로 문제를 해결하는 지적 절제력*을 갖추도록 강제 보조 장치(Harness)를 채운다. 동일 사상의 구현체가 [[Sonar_Protocol]]과 [[Try_Skill_타당성_검증]]이다.

### 클립보드 미니멀리즘과 뇌 용량의 보존 (UX Abstraction)

인간 개발자의 뇌는 아키텍처적 의사결정과 크리에이티브에만 집중해야 한다. 상태 추적, 핸드오버 문서 작성, 컨텍스트 주입 등의 메타 프로세스는 외부 스킬로 완전 자동화한다. 인간은 *클립보드 복사-붙여넣기*와 *최종 승인(Confirm/Deny)*이라는 최상위 제어권만 행사한다.

## 아키텍처적 설계 의도

### 마스터마인드를 위한 물리 포석

향후 배정될 최상위 자율 오케스트레이션 에이전트(Mastermind)에게 무한 런타임 권한을 주는 것은 자살 행위다. 대신 에이전트가 프로젝트를 지휘할 때 사용할 수 있는 고정밀 대시보드([[Dictionary_md_좌표_시스템]] / [[RIPER_5단계_상태머신]] 상태머신)를 미리 깎아둔다. Mastermind는 별도 학습·추론 비용 없이 제공된 레버 매뉴얼대로 하위 에이전트를 라우팅하고 시스템을 관리한다.

### 시공간 좌표로의 번역 (Spatial Mapping)

"전투 시스템의 폭발 로직을 수정해줘" 같은 추상적·모호한 지시를 받았을 때, Mastermind는 이 요청을 `manage/dictionary.md`라는 인덱스 지도를 경유한다. 지시는 즉시 `[BLK-042] Assets/Core/Scripts/Gameloop/ExplosionSystem.cs`라는 명확한 공간 좌표로 번역되며, 에이전트는 시야가 제한된 상태(Scope Lock)로 해당 라인 범위만 정밀 타격(Surgical Edit)한다. 이 원리의 형식적 강제가 [[RULE7_PRD_Spatial_Mapping]]이다.

### 자가 치유형 지식 인프라 (Self-Healing Wiki)

코드 변경 시 개발자가 위키/딕셔너리를 수동으로 수정하면 인덱스는 반드시 붕괴한다. RIPER의 Review 단계에 `check-sync.sh` 및 의존성 갱신 스크립트를 파이프라인으로 바인딩해, 에이전트가 코드를 고치면 자동으로 지도(Dictionary)와 흐름도의 수정 초안을 인간에게 바치는 자가 치유 루프를 구성한다.

## 공학적 목표 (Performance Targets)

| 목표 | 지표 |
|---|---|
| O(1) 시간 복잡도의 소스 추적 | 코드베이스 검색 비용 O(N) → 딕셔너리 키-값 조회 O(1) |
| 턴당 토큰 소모량 극단적 감축 | 회당 토큰 90% 이상 절감 (무제한 Read 대비) |
| 컨텍스트 생명 연장 | 120턴 이상에서도 지능 저하·상태 붕괴·방향성 상실 없음 |
| 완벽한 상태 격리 | 인수인계·컴팩션 전후 컨텍스트 손실율 0%에 수렴 |

## 논쟁 및 관점 차이

매니페스토는 같은 시스템을 [[LLM_통제_철학_6대원칙]]보다 더 *선언적·정치적* 어조로 진술한다. 분석적 정리가 필요하면 6대원칙으로, 설계 의도의 무게감과 비유적 프레이밍이 필요하면 이 문서로 진입하는 것을 권한다. 두 문서는 동일 실체의 두 얼굴이다.

## 다음 진화 단계 (3-Year Roadmap)

[[Mastermind_Architecture_Manifesto]]는 현재의 기초 위에서 3단계 진화를 상정한다.

### Phase 1: Self-Healing Wiki (자가 치유 루프)

**현재**: 수동으로 dictionary를 갱신. 알림만 제공.

**진화 목표**: RIPER의 Review 단계에서 dictionary 갱신 초안을 **자동 제안**.

```
코드 변경 감지
  ↓ (check-sync.sh)
영향받는 BLK 파악
  ↓ (의존성 분석)
dictionary 갱신 초안 생성
  ↓ (사람의 Review)
자동 병합 (승인 시)
```

**효과**: dictionary 붕괴 위험 극소화. 지식 인프라의 반자동 유지보수.

### Phase 2: Mastermind Agent (최상위 오케스트레이션)

**현재**: 사용자가 매번 compile-wiki, move-to-raw 스킬을 명시적으로 호출.

**진화 목표**: Mastermind가 RIPER 상태머신을 자동으로 관리하고 하위 에이전트/스킬을 라우팅.

```
유저: "전투 시스템 폭발 로직 수정해줘"
  ↓
Mastermind (Request)
  → dictionary 참조, "BLK-042 확인됨"
  ↓
Mastermind (Investigate)
  → Specialist agents (코드 분석)
  ↓
Mastermind (Plan)
  → 수정 계획 자동 생성
  ↓
Mastermind (Execute)
  → 코드 수정 + dictionary 갱신 제안
  ↓
Mastermind (Review)
  → QualitySentinel 자동 검증 + 컴팩션 자동화
```

**효과**: 사용자는 "해줘" 정도의 지시만 하면 나머지는 자동. [[RIPER_5단계_상태머신]] 완전 자동화.

### Phase 3: Multi-Vault 연합 (프로젝트 초월)

**현재**: 단일 vault (`D:\Fork\WIKI`). RX_1은 그 내부의 프로젝트 인스턴스.

**진화 목표**: 다중 vault의 느슨한 연합. 일반 개념은 공유, 프로젝트 특화는 독립.

```
MetaVault (상위 협조 계층)
├─ WIKI/           (LLM 워크플로우 중앙 - 일반 개념)
├─ RX_1/           (RX_1 프로젝트 - BLK-001~013)
├─ ArcynGame/      (게임 프로젝트 - 독립 dictionary)
└─ [신규 프로젝트]/  (새로운 프로젝트)
    └─ 일반 노트 재사용 + 프로젝트 특화 추가
```

**효과**: 
- 중앙의 원칙 및 패턴 일원화
- 각 프로젝트는 자신의 BLK, dictionary, 상태 기계 보유
- 신규 프로젝트 온보딩 가속

---

## 성숙도 지표 (Maturity Metrics)

| 항목 | Phase 1 (현재) | Phase 2 (1-2년) | Phase 3 (2-3년) |
|---|---|---|---|
| 자동화 수준 | 수동 입력 | 반자동 라우팅 | 완전 자동 오케스트레이션 |
| dictionary 동기화 | 알림 | 자동 초안 제안 | 자동 병합 |
| 에이전트 판단 | 사람 결정 | 상황 분석 후 제안 | 자동 결정 (사후 보고) |
| 프로젝트 수 | 1~2개 | 3~5개 | 10+ (연합 가능) |
| 토큰 효율 | 90% 절감 | 95% 절감 | 98% 절감 (초과 비용 무시) |

## 출처

- raw/gemini-code-1779431417344.md (2026-05-22 유입) — 원문 전체 (Background / Philosophy / Intent / Goals)
