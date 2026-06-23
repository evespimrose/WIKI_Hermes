---
tags: [llm-wiki, 아키텍처, 설계원칙]
date_created: 2026-06-02
last_modified: 2026-06-02
---

# Clean Architecture 4계층

관심사를 Domain / Application / Service / Presentation 네 레이어로 분리하고 *의존 방향을 안쪽 단방향*으로 강제하는 아키텍처. 각 레이어는 `*.asmdef` 어셈블리 1개에 대응하며, 경계는 [[asmdef_레이어_경계강제]]가 컴파일러로 지킨다. [[Architecture_허브]] 소속.

## 왜 레이어를 분리하는가

| 이유 | 효과 |
|---|---|
| 소스 이해 용이 | 레이어 = 책임 단위. "어디를 보면 되나"가 구조로 답해진다 |
| 변화 대응 | 엔진/프레임워크 교체가 바깥 레이어에 갇힘 (Domain 무영향) |
| 영향 최소화 | 의존이 안쪽 단방향이라 변경 파급이 차단됨 |
| 테스트 용이 | Domain/Application이 엔진 비종속 → 엔진 없이 단위 테스트 |

→ **높은 응집도 + 낮은 결합도**. 이는 [[LLM_통제_철학_6대원칙]] 원칙 5(단일 책임)를 *코드 구조* 차원에서 구현한 것이다. [[Karpathy_4대_코딩원칙]]의 Simplicity·Surgical Changes와도 같은 방향.

## 4레이어 구조

```
Presentation ─┐
              ├─→ Application ─→ Domain (최내층)
Service ──────┘

의존 방향: Presentation·Service → Application → Domain (단방향)
안쪽(Domain)은 바깥을 절대 모른다. 화살표는 역류하지 않는다.
```

| 레이어 | 책임 | 엔진 결합 | 비동기 |
|---|---|---|---|
| **Domain** | 핵심 비즈니스 로직, 순수 POCO | 0 (R3+BCL만) | — |
| **Application** | 유스케이스 조율, Domain만 참조 | 0 | `ValueTask` (BCL) |
| **Service** | 엔진-결합 서비스 (파일IO, 자원로딩) | 허용 | `UniTask` |
| **Presentation** | MonoBehaviour·UI·DI 합성루트 | 허용 | `UniTask` |

- 네임스페이스 규약: `ws.[module].[layer]` (예: `ws.core.Domain`).
- 레이어 = asmdef 1개. 모듈(core/gameplay/ui…)은 레이어 *내부의* 폴더+네임스페이스.

## 의존성 역전이 핵심 축

단방향 의존이 가능한 이유는 [[의존성_역전_DIP]] 덕분이다. 안쪽이 인터페이스(계약)를 정의하고 바깥이 구현하므로, 소스 의존은 항상 안쪽을 향한다.

## 신규 코드 배치 결정 트리

새 클래스를 어디 둘지 1초 판단:

```
엔진(UnityEngine) 타입이 필요한가?
├─ 아니오 → 비즈니스 규칙/엔티티/값인가?
│            ├─ 예 → Domain
│            └─ 아니오(유스케이스 조율) → Application  (비동기 ValueTask)
└─ 예 → MonoBehaviour/UI/DI 인가?
         ├─ 예 → Presentation
         └─ 아니오(엔진-결합 서비스) → Service
```

핵심 분기는 *"엔진이 필요한가"* — [[의존성_역전_DIP]]의 "엔진 필요하면 바깥" 규칙과 동일한 잣대다.

## 실 적용 사례

[[Western_Salon_Clean_Architecture]]가 이 구조의 실구현(ws.core, Phase 1)을 보여준다. RX_1의 [[Block_Assembly_Part_Piece_컨벤션]]이 *모듈 어노테이션*으로 구조를 잡았다면, 본 4계층은 *레이어 분리*로 잡는 다른 전략이다 — 둘 다 "구조적 프로그래밍" 목적은 같다.

## 출처

- raw/clean_architecture.md (2026-06-02 유입) — §1·2·8 레이어 구조·관심사분리·배치 트리
