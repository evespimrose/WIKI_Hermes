---
tags: [llm-wiki, 행성허브, 아키텍처]
date_created: 2026-06-02
last_modified: 2026-06-02
---

# Architecture 허브

일반 소프트웨어 아키텍처 개념을 묶는 행성. 특정 프로젝트가 아니라 *프로젝트 무관하게 재사용되는* 구조 설계 지식이 여기 모인다. 상위 항성 [[LLM_워크플로우_생태계]]에서 진입한다. 인접 행성은 [[Token_허브]]·[[Western_Salon_허브]]·[[RX_1_허브]].

## 행성 정의

[[Token_허브]]가 *LLM 통제*, 프로젝트 행성들이 *실 구현 인스턴스*라면, 본 행성은 그 구현들이 따르는 *일반 구조 원리*를 담는다. 코드를 "우연이 아닌 규칙으로" 배치하기 위한 설계 자산.

## 위성 카탈로그

### Clean Architecture 계열

- [[Clean_Architecture_4계층]] — Domain/Application/Service/Presentation 단방향 의존
- [[의존성_역전_DIP]] — 안쪽 계약, 바깥 구현
- [[asmdef_레이어_경계강제]] — 컴파일러 물리 강제

### 모듈·코딩 원칙 (Token 행성과 공유)

- [[Block_Assembly_Part_Piece_컨벤션]] — 모듈 어노테이션 아키텍처
- [[Karpathy_4대_코딩원칙]] — Think/Simplicity/Surgical/One-thing

위 둘은 [[Token_허브]]에도 적을 둔 *공유 위성*이다 — 코드 구조이면서 동시에 토큰 통제 철학의 일부라 양 행성을 잇는 별다리 역할.

## 프로젝트 인스턴스로의 적용

일반 원리가 실제로 어떻게 구현되는지:

| 일반 원리 | 적용 인스턴스 |
|---|---|
| [[Clean_Architecture_4계층]] | [[Western_Salon_Clean_Architecture]] (ws.core, 레이어 분리) |
| [[Block_Assembly_Part_Piece_컨벤션]] | [[RX_1_manage_DB_스키마]] (BLK 어노테이션) |

ws는 *레이어 분리*, RX_1은 *모듈 어노테이션* — 같은 "구조적 프로그래밍" 목적의 두 전략이다.

## 물리적 강제라는 가교

[[asmdef_레이어_경계강제]]는 본 행성에서 [[Token_허브]]의 [[L1_Hard_Gate_훅체계]]로 직결되는 다리다. 컴파일러 게이트와 hook 게이트는 *비결정성을 결정성으로 가두는* 동일 발상([[LLM_통제_철학_6대원칙]] 원칙 3)의 두 구현이다.

## 인접 행성으로의 통로

- [[Token_허브]] — 공유 위성(Block_Assembly·Karpathy) + 물리강제 철학
- [[Western_Salon_허브]] — 본 행성 원리를 적용한 프로젝트
- [[RX_1_허브]] — 또 다른 적용 프로젝트
