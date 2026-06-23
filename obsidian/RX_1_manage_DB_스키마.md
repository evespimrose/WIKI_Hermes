---
tags: [llm-wiki, rx1, 인덱스, 프로젝트사례]
date_created: 2026-05-22
last_modified: 2026-06-16
---

# RX_1 — manage/ 통합 DB 스키마

[[manage_폴더_역할분리]]의 일반 패턴을 RX_1 프로젝트(`D:\Fork\RX_1\manage\`)에 실제로 적용한 인스턴스. *6개* 파일이 서로 역할을 분리하면서도 *하나의 지식 인덱스 데이터베이스*로 작동하는 방식을 보여준다.

## 6파일 구성

```
dictionary.md              ← 보완(fallback): 파일 경로 → BLK 조회 (codegraph 우선 후)
Block.md                   ← BLK 계층 구조 (Assembly / Part / Piece)
Function_Block_Archive.md  ← Part 교체 옵션 (다운그레이드 메뉴)
Management.md              ← 현재 Active Part 요약 + 다운그레이드 실행 이력
modular-architecture.md    ← 어노테이션 컨벤션 규칙
Feature_Spec_History.md    ← BLK-H 기능 명세 시간축 아카이브 (다운그레이드 앵커)
```

6번째 파일 `Feature_Spec_History.md` 는 다른 5파일이 *현재 상태 인덱스*인 것과 달리 *시간축 이력 아카이브*다. 그 표준 포맷·BLK-H 좌표 어휘는 [[feature_spec_history_format]] 에 정의되어 있다.

각 파일의 *일반적* 책임 정의는 [[manage_폴더_역할분리]]를, 계층 정의는 [[Block_Assembly_Part_Piece_컨벤션]]을 본다. 본 노트는 RX_1에 특화된 *조회 패턴과 BLK 명단*을 다룬다.

### Self-Describing 헤더 패턴

6파일 중 dictionary·Block·Function_Block_Archive·Management 네 파일은 본문 최상단에 "📌 이 문서의 역할" 표를 둔다 — *"열어야 할 때 / 열지 않아도 될 때 / 관련 문서"* 3행 표. [[manage_폴더_역할분리]] 가 일반론에서 정의한 라우팅이 *각 파일에 내장*된 형태로, 파일을 처음 여는 AI 에이전트가 *이 파일을 더 읽어야 하는지를 첫 줄에서 판단*할 수 있게 한다. modular-architecture·Feature_Spec_History 는 본문 자체가 규약·이력 그 자체이므로 이 헤더가 없다.

## RX_1 dictionary.md 실제 섹션 구조

RX_1 구현은 [[Dictionary_md_좌표_시스템]]의 일반 §0~§7 구조보다 단순화되어 있다.

| 섹션 | RX_1 실제 | 비고 |
|---|---|---|
| § 0 | Sonar Protocol | [[Sonar_Protocol]] 그대로 |
| § 0-1 | cxt 파일 검증 규칙 (BLK 태그 필수) | [[cxt_파일_포맷_컨벤션]] 강제 절 |
| § 1 | 파일 인덱스 (경로 → BLK → Assembly → 핵심 클래스) | 일반론의 § 1을 클래스 진입점까지 확장 |
| § 2 | BLK 의존성 맵 | 일반론에서는 § 4 위치 |
| § 3 | 키워드 인덱스 (한글 / 영문 동시) | 일반론은 § 3에 단일 키워드만 |

차이의 의미: 일반 워크플로 문서가 PRD 단계에서 그렸던 8섹션 청사진과 실제 운영 중인 RX_1 dictionary가 *다르게 진화*했다. 일반론을 그대로 받아쓰지 않고 프로젝트 규모(BLK-001~013 13개)에 맞춰 가지치기한 결과다.

## BLK 명단 (BLK-001 ~ BLK-013)

| BLK | 도메인 | 대표 파일 |
|---|---|---|
| BLK-001 | Pathfinding Domain | TurnAwareAStar, CellGrid, MinHeap, IOPort |
| BLK-002 | GPU Instancing Renderer | CellRenderer, Sort, Buffer, Shader |
| BLK-003 | DDA Picking | GridDDAPicker, RangeSelectionLogic |
| BLK-004 | Phase State Machine | PhaseStateMachine, Phase1/2/3 UI |
| BLK-005 | Obstacle Preset Panel | OpsFileManager, PresetCard, Thumbnail |
| BLK-006 | Preset Editor | PresetEditorController, PlacementPopupUI |
| BLK-007~013 | Camera, Layer View, Flow Control 등 | (세부는 Block.md 참조) |

BLK 코드 의미론은 [[BLK_좌표_시스템]]에, 어노테이션 규약은 [[Block_Assembly_Part_Piece_컨벤션]]에 정의되어 있다.

## 단일 DB로서의 5단계 조회 흐름

"CellRenderer 정렬 로직 어디 있어?" 같은 질문은 **codegraph(codegraph_context/search/impact)가 1차 경로**다. codegraph로 미해결이거나 BLK·다운그레이드 메타가 필요할 때, 아래처럼 5파일이 *보완으로 순차 활성화*된다:

```
Step 0: codegraph_context/search → 심볼·영역 / codegraph_impact → BLK→파일 엣지 (1차)
        └ 미해결·보완 시 아래 dictionary/manage 체인 ↓
Step 1: dictionary.md § 3 키워드 인덱스 (보완)
        "Sort | 정렬" → BLK-002
Step 2: dictionary.md § 1 파일 인덱스
        BLK-002 → Presentation/CellRenderer.cs
        ─ 여기서 멈추는 것이 기본. 필요시 Step 3~ ─
Step 3: Block.md
        BLK-002 / SortJob Assembly → BurstSortJobPart (ACTIVE)
Step 4: Function_Block_Archive.md
        BurstSortJobPart 대안 → MainThreadSortPart (DOWNGRADE 옵션)
Step 5: Management.md
        다운그레이드 실행 후 이력 기록
```

대부분의 작업은 Step 1~2에서 종료된다. Step 3~5는 *교체·다운그레이드 작업*에 한해 활성화된다 — [[manage_폴더_역할분리]] 표의 "열어야 할 때" 컬럼이 이 분기를 안내한다.

## SortJob Assembly 예시 (BLK-002 일부)

`Function_Block_Archive.md` 안에서 Part 옵션이 어떻게 정리되는지 한 예:

```markdown
## BLK-002 / SortJob Assembly
| Part 이름           | 상태       | 설명 |
|---------------------|-----------|----- |
| BurstSortJobPart    | ACTIVE    | NativeArray + Burst Job 비동기 정렬 |
| MainThreadSortPart  | DOWNGRADE | Array.Sort 동기, Burst 미지원 환경 |
```

이 표가 [[Block_Assembly_Part_Piece_컨벤션]]의 *Active ⇄ Downgrade* 추상 정의가 실제 코드에서 어떤 형태로 구체화되는지 보여주는 가장 명확한 사례다.

## Sonar Protocol 준수

RX_1 dictionary.md는 [[Sonar_Protocol]]의 *보완(fallback) 대상 인덱스*다(현행 codegraph-first — [[Sonar_Protocol]] 「Codegraph-First (3단계 진화 이후)」 절). RX_1에서 코드를 찾을 때 `find/grep -r` 사용은 금지되며, codegraph 우선 후 미해결 시 dictionary § 1·§ 3로 보완한다(RX_1 `CLAUDE.md` RULE-1과 동일).

```
❌ find / ls -r / grep -r / rg / fd
✅ codegraph_context/search/impact → (보완) dictionary § 1·§ 3 → Glob/Grep 도구
```

## 일반 패턴과의 관계

본 노트는 [[manage_폴더_역할분리]]의 *프로젝트 인스턴스*다. 다른 프로젝트(예: ArcynGame, 미래 신규 Unity 프로젝트)가 같은 패턴을 채택하면 동일 구조의 `XXX_manage_DB_스키마.md`가 생길 수 있다 — 일반론 노트와 인스턴스 노트의 분리가 그 확장성을 보장한다.

## 출처

- raw/RX_1/manage_folder_schema.md (2026-05-22 유입) — 원본 `D:\Fork\RX_1\manage\` 폴더 스키마 설명 (통합 단일 문서)
- raw/RX_1/{Block, Function_Block_Archive, Management, dictionary, modular-architecture, Feature_Spec_History}.md (2026-05-26 유입) — RX_1 manage 폴더 *6파일 실제 스냅샷*. 본 노트의 5→6파일 확장 근거.
