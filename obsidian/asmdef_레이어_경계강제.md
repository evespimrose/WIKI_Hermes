---
tags: [llm-wiki, 아키텍처, 강제]
date_created: 2026-06-02
last_modified: 2026-06-02
---

# asmdef 레이어 경계 강제

레이어 경계를 *말(컨벤션)이 아니라 컴파일러*가 지키게 만드는 Unity `*.asmdef` 설정 기법. [[Clean_Architecture_4계층]]의 단방향 의존과 [[의존성_역전_DIP]]를 물리적으로 보증한다. [[Architecture_허브]] 소속.

## 강제표 (Enforcement Table)

| asmdef | `noEngineReferences` | references | precompiled |
|---|---|---|---|
| **ws.Domain** | `true` | `[]` | R3.dll + BCL 4종 |
| **ws.Application** | `true` | `[ws.Domain]` | R3 + BCL (UniTask 제외) |
| **ws.Service** | `false` | `[ws.Application, ws.Domain, UniTask]` | auto |
| **ws.Presentation** | `false` | `[ws.Application, ws.Domain, UniTask, VContainer]` | auto |

## 어떻게 물리 강제가 되는가

- `noEngineReferences:true` → Domain/Application이 `UnityEngine`을 참조하면 **컴파일 실패**. 순수성이 의지가 아니라 빌드 조건으로 보장된다.
- `overrideReferences:true` → R3.dll auto-ref 누수를 차단. Domain/App은 R3만 보이고 **UniTask는 컴파일 불가**.
- references 목록에 없는 역방향 참조(Domain → Presentation)는 asmdef상 **불가능** → 시도 즉시 컴파일 에러.
- ⚠ R3.dll은 BCL 의존 → precompiled에 BCL 4종(`System.Threading.Channels`, `Microsoft.Bcl.AsyncInterfaces`, `Microsoft.Bcl.TimeProvider`, `System.ComponentModel.Annotations`) 동반 명시 필수. 누락 시 빌드 실패.

## 회귀 자동 감시

경계가 *나중에* 깨지는 것도 막는다. `DomainPurityTests`가 리플렉션으로 `ws.Domain` 어셈블리에 `UnityEngine`·`UniTask` 참조가 없음을 단언 → 경계 위반이 테스트 실패로 즉시 드러난다. [[Western_Salon_Clean_Architecture]]의 EditMode 테스트에 실재한다.

## "물리적 강제"라는 공통 철학

이 기법은 본 vault의 핵심 사상과 정확히 동형이다 — *규칙을 텍스트로 적지 말고 강제 장치로 막아라*.

| 영역 | 텍스트 규칙(약함) | 물리 강제(강함) |
|---|---|---|
| 레이어 경계 | "Domain에서 엔진 쓰지 마세요" | asmdef `noEngineReferences` 컴파일 실패 |
| 코드 탐색 | "find 쓰지 마세요" | [[L1_Hard_Gate_훅체계]] PreToolUse 차단 |

[[LLM_통제_철학_6대원칙]] 원칙 3(훅 > 프롬프트)이 LLM 워크플로우에서 한 일을, asmdef는 코드 아키텍처에서 한다. 강제 수단만 다를 뿐(컴파일러 ↔ hook) *비결정성을 결정성으로 가두는* 발상은 같다 — [[Mastermind_Architecture_Manifesto]]의 "기계식 통제 섀시"와 통한다.

## 출처

- raw/clean_architecture.md (2026-06-02 유입) — §5 asmdef 강제표, §7 DomainPurityTests
