---
tags: [llm-wiki, llm-워크플로우, 상태머신, 인덱스]
date_created: 2026-05-22
last_modified: 2026-05-22
---

# RULE-7 — PRD Spatial Mapping

[[RIPER_5단계_상태머신]]의 PLAN 단계에서 모든 Action Item에 [[BLK_좌표_시스템]] 좌표를 의무화하는 규칙. [[Mastermind_Architecture_Manifesto]]의 "Spatial Mapping" 사상을 *플랜 작성 단계*에 못박는다.

## 형식

```
❌ "ExplosionSystem의 로직을 수정한다"
✅ "[BLK-042] Assets/Core/Scripts/Gameloop/ExplosionSystem.cs 내 데미지 함수 수정"
```

좌표가 없으면 EXECUTE 단계에서 LLM은 *어디 있는지 모르겠으니 일단 파일 전체를 보자*로 폴백한다. 이는 [[LLM_컨텍스트_5대_문제]] 3번(토큰 폭발)을 즉시 트리거한다. 좌표가 있으면 `Read(offset+limit)` 또는 `grep -A 20 -B 20`으로 최소 로드한다.

## RULE-1 확장 — EXECUTE Scope Lock

RULE-7과 짝을 이루는 EXECUTE 단계 열람 권한 제약:

- 좌표 있음 → `Read(offset+limit)` 또는 `grep -A 20 -B 20`
- 신규 파일 → Read 생략, 즉시 Write
- 파일 전체 Read → **실패**로 간주

이는 "Read-to-Understand"에서 "Index-to-Edit"으로의 패러다임 전환이다.

## 두 규칙의 직조

```
PLAN 단계 (RULE-7)           EXECUTE 단계 (RULE-1 확장)
  ─ BLK 좌표 의무화           ─ 좌표 주변만 Read 허용
        ↓                            ↓
  ────────────── 좌표 좌표 좌표 ──────────────
  플랜이 미리 좌표를 박지 않으면 EXECUTE에서 Read 폴백 발생
```

이 결합이 [[LLM_통제_철학_6대원칙]] 1번(Tokens are First-Class)을 *RIPER 사이클 전체*에 걸쳐 강제하는 메커니즘이다.

## 좌표 확보의 책임 사슬

```
writer 에이전트 → 플랜 작성 시 [[Dictionary_md_좌표_시스템]] § 1·§ 3을 조회해 좌표 부여
  ↓
quality-sentinel → RIPER 감사 시 모든 Action Item에 좌표가 있는지 검증
  ↓
EXECUTE 에이전트 → 좌표 외 영역 접근 시 실패
```

좌표가 없는 Action Item은 *플랜 자체가 무효*다. quality-sentinel의 Phase 1 RIPER 감사가 이를 잡아낸다 → [[Producer_QualitySentinel_Reporter_게이트]].

## "Spatial Coordinate"라는 메타포

좌표라는 어휘는 단순한 BLK 코드 이상의 의미를 담는다. 작업 단위를 *시공간상의 한 점*으로 다루면:

- 시야가 자동으로 제한됨 (한 점 주변만 보기)
- 작업 위치를 잊을 수 없음 (좌표 자체가 위치)
- 두 작업이 같은 위치인지 즉시 비교 가능 (좌표 동등성)

이는 [[Mastermind_Architecture_Manifesto]]의 "Sovereign LLM Control" 철학이 *공간적 어휘*로 구체화된 사례.

## 신규 파일의 예외

신규 파일 작성은 Read가 불필요하므로 좌표 의무에서 예외다. 단 *작성 직후* dictionary § 1에 BLK 행을 추가해야 한다. [[Dictionary_md_좌표_시스템]]의 동기화 훅(`dict-sync-check.sh`)이 이를 알림화한다.

## 관련 노트

- 상위 상태머신: [[RIPER_5단계_상태머신]]
- 좌표 의미론: [[BLK_좌표_시스템]]
- 인덱스 본체: [[Dictionary_md_좌표_시스템]]
- 감사 게이트: [[Producer_QualitySentinel_Reporter_게이트]]
- 토큰 자원 원칙: [[LLM_통제_철학_6대원칙]] §1

## 출처

- raw/Workflow-Design-Philosophy.md (2026-05-22 유입) — §4-4 RULE-7, §4-5 RULE-1 확장
- raw/gemini-code-1779431417344.md (2026-05-22 유입) — Spatial Mapping intent
