---
tags: [llm-wiki, llm-워크플로우, 인덱스]
date_created: 2026-05-22
last_modified: 2026-06-14
---

# BLK 좌표 시스템

프로젝트 코드 전체에 부여되는 *공간 좌표 식별자*. `BLK-XXX` 형식의 짧은 코드가 [[Dictionary_md_좌표_시스템]] § 1을 통해 파일 경로로 번역된다. [[Mastermind_Architecture_Manifesto]]의 "Spatial Mapping" 사상의 가장 구체적 구현물이다.

## 좌표 어휘

| 형식 | 의미 | 예 |
|---|---|---|
| `BLK-XXX` | 단일 Block (기능 단위 ON/OFF) | `BLK-001` Turn-Aware A* |
| `[BLK-XXX][A][P]` | Block 안의 Assembly·Part 좌표 | `[BLK-001][1][1]` 그리드 초기화 |
| `인프라` | 코드 대상 아닌 인프라 작업 | (BLK 없음) |
| `BLK-001, BLK-002` | 복수 좌표 | (cxt 헤더에서 사용) |

세 단어(Block / Assembly / Part / Piece)의 계층 정의는 [[Block_Assembly_Part_Piece_컨벤션]]을 본다.

## 짧은 코드가 가져오는 이점

### 1. 컨텍스트 진입량 압축

`Assets/Core/Scripts/Gameloop/Pathfinding/TurnAwareAStar.cs` (60자) → `BLK-001` (7자). 50배 압축. 자주 언급되는 파일일수록 효과가 누적된다.

### 2. 의미적 안정성

파일이 이동·이름 변경되어도 *BLK 코드는 같다*. 리팩토링 후에도 과거 [[doc_context_입력_워크플로우]] cxt 파일과 메모리 뱅크 참조가 깨지지 않는다.

### 3. 검색 가능성

소스 파일 안에 `// [BLK-001][1][1]` 같은 주석으로 새겨져 있어 [[Sonar_Protocol]] 위반 없이도 grep으로 정밀 검색이 가능하다:

```powershell
# BLK-001 전체 기능 검색
grep -r "// \[BLK-001\]" Assets/Core/Scripts/

# BLK-001 Assembly 1 Part 1만
grep -r "// \[BLK-001\]\[1\]\[1\]" Assets/Core/Scripts/
```

### 4. Scope Lock

[[RIPER_5단계_상태머신]] EXECUTE 단계의 권한이 *좌표 주변으로* 제한된다. 좌표가 있으면 `Read(offset+limit)` 또는 `grep -A 20 -B 20`으로 최소 로드한다. 좌표 없으면 파일 전체 Read는 실패로 간주된다. 이 강제가 [[RULE7_PRD_Spatial_Mapping]]이다.

## 어디에 등장하는가

| 등장 위치 | 형식 | 용도 |
|---|---|---|
| `manage/dictionary.md § 1` | `BLK-XXX \| 경로` | 좌표→파일 매핑 |
| 소스 파일 헤더 | `// [BLK-XXX] BlockName ...` | 파일→좌표 역매핑 |
| 소스 파일 본문 | `// [BLK-XXX][A][P]` | 함수 단위 좌표 |
| cxt 파일 2행 | `<!-- BLK: BLK-XXX -->` | doc-context 진입 좌표 |
| RIPER 플랜 Action Item | `[BLK-042] {지시}` | 계획의 정밀화 |

## 인덱싱 비용의 위치

BLK 좌표를 새로 부여·갱신하는 비용은 *코드 변경 시점*에 집중된다. 검색 시 비용은 거의 0. 즉 *읽기 빈도 ≫ 쓰기 빈도*인 LLM 워크플로 특성에 맞춰 비용을 미리 지불하는 구조다. dictionary 갱신은 [[Dictionary_md_좌표_시스템]] § 6 동기화 훅을 통해 알림화되어 사람이 잊지 않게 보호된다.

## 어노테이션 컨벤션

소스 파일에 BLK 좌표를 새기는 표준 형식은 [[Block_Assembly_Part_Piece_컨벤션]]에서 상세 다룬다.

## 관련 노트

- 인덱스 본체: [[Dictionary_md_좌표_시스템]]
- 탐색 금지 규약: [[Sonar_Protocol]]
- 계층 정의: [[Block_Assembly_Part_Piece_컨벤션]]
- RIPER 통합: [[RULE7_PRD_Spatial_Mapping]]
- cxt 헤더 적용: [[cxt_파일_포맷_컨벤션]]

## 출처

- raw/modular-architecture.md (2026-05-22 유입) — BLK 어노테이션 형식
- raw/dictionary-first-grep-workflow.md (2026-05-22 유입) — BLK 인덱스 § 1
- raw/Workflow-Design-Philosophy.md (2026-05-22 유입) — §4-4 RULE-7, §4-5 Scope Lock
- raw/gemini-code-1779431417344.md (2026-05-22 유입) — Spatial Mapping
