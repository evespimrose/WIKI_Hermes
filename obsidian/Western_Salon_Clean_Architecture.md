---
tags: [llm-wiki, western-salon, 아키텍처, 프로젝트사례]
date_created: 2026-06-02
last_modified: 2026-06-02
---

# Western Salon — Clean Architecture 실구현

[[Clean_Architecture_4계층]] 일반 패턴을 Western Salon(ws) 프로젝트에 실제로 적용한 인스턴스. `[BLK-001]` ws.core 인프라 골격, Phase 1 기준. [[Western_Salon_허브]] 소속이며, RX_1의 [[RX_1_manage_DB_스키마]]와 병렬되는 프로젝트 사례다.

## 레이어별 실 구현

### Domain (`ws.core.Domain`) — 엔진 0

| 심볼 | 종류 |
|---|---|
| `ILogger` / `ITimeService` / `IEventBus` | interface (계약) |
| `EventBus` | class `: IEventBus, IDisposable` |

`EventBus`는 R3 `Subject<T>` 기반 순수 구현 — 타입별 Subject 사전, `lock` 스레드 안전, 재진입 데드락 방지(콜백 밖 발행), `Dispose` 시 전체 정리. 엔진 비종속이라 [[의존성_역전_DIP]]의 "엔진 필요하면 바깥" 규칙에 따라 *구현째로 Domain에 산다*.

### Application / Service — 골격 시드

Phase 1에선 어셈블리 골격만(.cs 없음). Application은 Phase 2 머지 보드 유스케이스부터, Service는 엔진-결합 구현이 필요할 때 채워진다. EntryPoint(`IStartable/ITickable`)는 Presentation 어댑터가 구현하고 순수 Application 유스케이스에 위임.

### Presentation (`ws.core.Presentation`)

| 심볼 | 역할 |
|---|---|
| `UnityLogger : ILogger` | `UnityEngine.Debug` 백엔드 |
| `UnityTimeService : ITimeService` | `UnityEngine.Time` 백엔드 |
| `RootLifetimeScope : LifetimeScope` | VContainer 전역 합성 루트 |
| `GameBootstrap` | 코드 부트 (`[RuntimeInitializeOnLoadMethod]`) |

## DI 합성 루트 (VContainer)

`RootLifetimeScope.Configure`가 전역 서비스를 Singleton 바인딩:

```csharp
builder.Register<IEventBus, EventBus>(Lifetime.Singleton);   // IDisposable 자동 정리
builder.Register<ILogger, UnityLogger>(Lifetime.Singleton);
builder.Register<ITimeService, UnityTimeService>(Lifetime.Singleton);
```

`GameBootstrap`은 씬·프리팹 없이 코드로 루트를 세운다: `[RuntimeInitializeOnLoadMethod(BeforeSceneLoad)]` → GameObject 생성 → `DontDestroyOnLoad` → `AddComponent<RootLifetimeScope>()`.

> **편차[승인]**: 플랜은 VContainerSettings+부트 씬을 명시했으나 헤드리스 환경 씬 저작 불가로 코드 부트 채택. 동등·가역(추후 씬 기반 전환 가능).

## 테스트 (실증)

엔진 비종속 레이어라 EditMode 즉시 검증:

- `EventBusTests` (3): Publish→Receive / 구독자 없음 드롭 / Dispose 후 `ObjectDisposedException`.
- `DomainPurityTests` (3): `ws.Domain`이 `UnityEngine`·`UniTask` 미참조임을 리플렉션 단언 — [[asmdef_레이어_경계강제]] 경계의 회귀 자동 감시.

→ Phase 1 검증: 컴파일 0에러 · EditMode 6 green · Play 부트 정상.

## 이벤트 전략 (A3 하이브리드)

다대다 크로스모듈 브로드캐스트만 `IEventBus`, 기능 내부는 R3 직접 주입. 모든 신규 `.cs`는 `[BLK-XXX]` 헤더 + `manage/dictionary.md` 등재 필수 — RX_1과 동일한 [[BLK_좌표_시스템]] 규약을 ws도 채택했다.

## 출처

- raw/clean_architecture.md (2026-06-02 유입) — §3·6·7 실구현 심볼·DI 합성루트·테스트
