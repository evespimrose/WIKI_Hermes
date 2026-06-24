---
tags: [llm-wiki, llm-워크플로우, 인덱스]
date_created: 2026-05-22
last_modified: 2026-06-16
---

# manage/ 폴더 역할 분리

프로젝트 루트의 `manage/` 폴더에 들어가는 다섯 파일의 역할 매핑. 한때 역할이 혼재했으나 *명확한 단일 책임 분리*를 통해 [[LLM_통제_철학_6대원칙]] 5번(Single Responsibility) 원칙을 적용했다.

## 다섯 파일의 확정 역할

| 파일 | 확정 역할 | 열어야 하는 상황 |
|---|---|---|
| `dictionary.md` | **보완(fallback) 탐색 인덱스** — "어디에 있는가?" (codegraph 우선 후 보완) | codegraph 미해결 시 참조 |
| `Block.md` | **구조 레지스트리** — "이 BLK는 어떤 Assembly로 구성되어 있는가?" | Assembly/Part 계층 확인 시 |
| `Function_Block_Archive.md` | **기능 이해 + 다운그레이드 옵션** — "이 기능은 무엇이고 어떻게 교체하는가?" | 기능 설계·교체 시 |
| `Management.md` | **다운그레이드 실행 추적** — "현재 무엇이 다운그레이드되어 있는가?" | 다운그레이드 관리 시 |
| `modular-architecture.md` | **컨벤션 규칙 레퍼런스** — "새 파일을 어떻게 어노테이션하는가?" | 신규 파일 작성 시 |

## 혼재의 역사

| 파일 | 원래 가지고 있던 중복 | 정리 방향 |
|---|---|---|
| `dictionary.md` | BLK 설명을 Function_Block_Archive와 중복 보유 | dictionary는 *인덱스만* 유지, 기능 설명은 Archive로 |
| `Block.md` | modular-architecture와 계층 정의 중복 | 계층 정의는 modular-architecture로 일원화, Block은 *레지스트리만* |
| `Function_Block_Archive.md` | dictionary § 2 클래스 인덱스와 진입점 중복 | dictionary § 2를 primary, Archive는 *기능 + 다운그레이드만* |

이 정리는 [[LLM_통제_철학_6대원칙]] 5번의 적용 사례이며, 정리 후 각 파일이 *언제 열어야 하는지* 명료해졌다.

## 닫혀야 할 때의 가이드

각 파일 상단에 *역할 + 열지 않아도 되는 상황*을 명시한다. 예를 들어 `modular-architecture.md`의 헤더:

```
열어야 할 때: 신규 파일 작성 시. 어노테이션 규칙 확인 시.
열지 않아도 될 때: BLK 계층 구조 조회 → Block.md / 파일 경로 탐색 → dictionary.md
```

*무엇을 안 하는가*를 명시하는 패턴은 [[Producer_QualitySentinel_Reporter_게이트]] 에이전트들의 "절대 금지" 섹션, [[External_AI_역할분리]]의 6대 금지 항목과 동일한 정신이다.

## 어느 파일을 먼저 열어야 하는가

코드 위치·구조 질의의 **1차 진입점은 [[Codegraph_MCP_통합]]**(codegraph_context/search/impact)이다. codegraph로 풀리지 않거나 BLK 좌표 보완이 필요할 때 `dictionary.md`를 연다 — [[Dictionary_md_좌표_시스템]]의 § 1·§ 3에서 BLK 좌표 확보 후, 필요에 따라 다음 단계로 분기한다. dictionary는 [[4계층_메모리_아키텍처]] L4의 *보완(fallback) 인덱스*다([[Sonar_Protocol]]의 codegraph-first 순서):

```
codegraph (1차) → 미해결·보완 시 ↓
dictionary.md (§ 1 파일·§ 3 키워드, 보완)
  ├─ "이 BLK가 어떻게 구성되어 있나?" → Block.md
  ├─ "이 기능이 뭐하는 거고 다운그레이드 옵션은?" → Function_Block_Archive.md
  ├─ "지금 무엇이 다운그레이드 상태인가?" → Management.md
  └─ "어노테이션 어떻게 다나?" → modular-architecture.md
```

## 다운그레이드 시스템과의 결합

`Block.md` / `Function_Block_Archive.md` / `Management.md` 세 파일은 *모듈러 아키텍처의 다운그레이드 시스템*과 함께 동작한다. Part 단위 교체 절차는 [[Block_Assembly_Part_Piece_컨벤션]]의 "Part 전환 절차" 섹션을 본다.

## 프로젝트 인스턴스

위에서 다룬 다섯 파일은 *일반 패턴*이다. 실제 프로젝트에서 어떻게 BLK 명단과 5단계 조회 흐름으로 구체화되는지는 [[RX_1_manage_DB_스키마]]에 RX_1 사례로 정리되어 있다. 새 프로젝트가 같은 패턴을 채택하면 동일 구조의 인스턴스 노트가 추가될 수 있다.

## 관련 노트

- 인덱스 본체: [[Dictionary_md_좌표_시스템]]
- 계층 정의: [[Block_Assembly_Part_Piece_컨벤션]]
- BLK 코드 의미론: [[BLK_좌표_시스템]]
- 탐색 규약: [[Sonar_Protocol]]
- 적용 사례: [[RX_1_manage_DB_스키마]]

## 출처

- raw/dictionary-first-grep-workflow.md (2026-05-22 유입) — §3 manage/ 역할 재정립
- raw/ecosystem-atomic-analysis.md (2026-05-22 유입) — §3-B manage/ 폴더 원자
- raw/modular-architecture.md (2026-05-22 유입) — "이 문서의 역할" 헤더 패턴
