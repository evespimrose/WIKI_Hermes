---
tags: [llm-wiki, 행성허브, western-salon]
date_created: 2026-06-02
last_modified: 2026-06-14
---

# Western Salon 허브

Western Salon(ws) 게임 프로젝트 영역의 노트를 묶는 행성. 머지/가챠/큐브 기반 게임이며, [[Clean_Architecture_4계층]]을 채택한 Unity 프로젝트. 상위 항성 [[LLM_워크플로우_생태계]]에서 진입한다. 인접 행성은 [[RX_1_허브]](형제 프로젝트)·[[Architecture_허브]](적용 원리).

## 행성 정의

[[Architecture_허브]]가 정의한 일반 구조 원리가 ws에서 *어떻게 실코드로 구현되는가*의 사례 모음. RX_1과 형제 관계인 두 번째 프로젝트 행성으로, 아직 위성이 적지만 Phase가 진행되며 성장한다.

## 위성 카탈로그

### 아키텍처

- [[Western_Salon_Clean_Architecture]] — ws.core 4레이어 실구현 (BLK-001, Phase 1)

*(Phase 2~ gameplay/merge/gacha 모듈이 추가되면 위성이 늘어난다.)*

## 일반 패턴과의 대응

| 일반 (Architecture 행성) | ws 인스턴스 |
|---|---|
| [[Clean_Architecture_4계층]] | ws.Domain/Application/Service/Presentation |
| [[의존성_역전_DIP]] | ILogger 계약(Domain) ↔ UnityLogger 구현(Presentation) |
| [[asmdef_레이어_경계강제]] | ws.Domain `noEngineReferences:true` + DomainPurityTests |
| [[BLK_좌표_시스템]] | 모든 `.cs`에 `[BLK-XXX]` + dictionary 등재 |

## RX_1과의 차이

두 프로젝트 행성은 구조 전략이 다르다:

- **RX_1**: 모듈 어노테이션([[Block_Assembly_Part_Piece_컨벤션]]) 중심, manage/ DB 인덱스([[RX_1_manage_DB_스키마]])
- **Western Salon**: 레이어 분리([[Clean_Architecture_4계층]]) 중심, asmdef 경계 강제

같은 [[BLK_좌표_시스템]]·[[Sonar_Protocol]] 규약을 공유하되 코드 구조 철학이 갈린다 — 일반 원리 행성([[Architecture_허브]])이 두 갈래를 모두 수용한다.

## 인접 행성으로의 통로

- [[Architecture_허브]] — 본 프로젝트가 적용한 일반 원리
- [[RX_1_허브]] — 형제 프로젝트 (다른 구조 전략)
