---
tags: [llm-wiki, 아키텍처, 설계원칙]
date_created: 2026-06-02
last_modified: 2026-06-02
---

# 의존성 역전 (DIP)

**안쪽 레이어가 인터페이스(계약)를 정의하고, 바깥 레이어가 구현한다.** 안쪽은 구현체를 전혀 모른다. [[Clean_Architecture_4계층]]의 단방향 의존을 가능하게 하는 축. [[Architecture_허브]] 소속.

## 계약은 안, 구현은 밖

```
ws.core.Domain.ILogger          (계약, Domain)
        ▲ implements
ws.core.Presentation.UnityLogger    (구현, Presentation → UnityEngine.Debug)
```

- **컴파일타임 화살표**: `Presentation → Domain` (단방향).
- **런타임 제어흐름**: Domain 코드가 `ILogger`를 통해 `UnityLogger`를 호출 — 흐름은 역류하지만 *소스 의존은 역류하지 않는다*. 이것이 "역전"의 의미.

## 테스트 가능성을 낳는다

Domain/Application이 인터페이스에만 의존하므로, 테스트에서 *가짜 구현*(`ManualClock`, 메모리 로거)을 주입해 엔진 없이 검증된다. [[Clean_Architecture_4계층]]의 "테스트 용이" 효과가 DIP에서 직접 나온다.

## "엔진이 필요하면 바깥"이 정확한 규칙

흔한 오해는 "구현은 무조건 바깥"이다. 정확히는 **"엔진이 필요하면 바깥"**이다.

> 순수 구현은 안쪽에 산다. ws의 `EventBus`는 R3 `Subject<T>` 기반인데 엔진 비종속(netstandard2.1)이라 *구현째로 Domain에 산다*. 반대로 로깅·시간은 `UnityEngine`이 필요하므로 계약만 Domain, 구현은 Presentation.

이 구분이 [[Western_Salon_Clean_Architecture]]에서 EventBus가 Domain에, UnityLogger가 Presentation에 나뉘어 사는 이유다.

## 물리적 강제와의 결합

DIP는 *규칙*이고, 그 규칙이 깨지지 않도록 [[asmdef_레이어_경계강제]]가 컴파일러로 막는다. 역방향 참조(Domain이 Presentation 참조)를 asmdef가 원천 차단하므로 DIP 위반이 물리적으로 불가능해진다. 이는 [[LLM_통제_철학_6대원칙]] 원칙 3(훅 > 프롬프트)의 "규칙은 강제 장치로 지킨다" 정신과 동형이다.

## 출처

- raw/clean_architecture.md (2026-06-02 유입) — §4 의존성 역전, EventBus 배치 근거
