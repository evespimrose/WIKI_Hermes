---
tags: [llm-wiki, llm-워크플로우, 모듈러아키텍처, 컨벤션]
date_created: 2026-05-22
last_modified: 2026-06-14
---

# Block · Assembly · Part · Piece 컨벤션

코드를 *어셈블·플러그인 교체* 단위로 분해해 *언제든 다운그레이드 가능한* 구조로 만드는 4계층 모듈러 아키텍처 컨벤션. [[BLK_좌표_시스템]]의 좌표 어휘가 가리키는 *실체*가 이 계층 정의다.

## 4계층 정의

```
Block (BLK-XXX)
  └ Assembly      : 연관 Part들의 묶음 — 한 Block의 한 기능 축
      └ Part      : 교체 가능 부품. Active ⇄ Downgrade 전환 단위
          └ Piece : 최소 단위 소스 파일·함수·데이터 구조
```

| 계층 | 교체 단위 | 예 |
|---|---|---|
| **Block** | 기능 전체 ON/OFF | GPU 렌더러 전체를 CPU 메시 베이크로 교체 |
| **Assembly** | 기능의 한 축 교체 | 렌더 파이프라인만 교체, 데이터 버퍼는 유지 |
| **Part** | 구체적 구현 교체 | Burst Sort → Main Thread Sort |
| **Piece** | 최소 수정 | 단일 상수·함수 변경 |

## 소스 파일 헤더 어노테이션

모든 소스 파일 상단에 해당 파일이 속한 계층을 명시한다:

```csharp
// [BLK-XXX] BlockName
// [1] Assembly : AssemblyName
// [1] Part     : ActivePartName (ACTIVE)
//             Downgrade → DowngradePartName (설명)
// Piece    : 이 파일의 구체적 역할 한 줄 설명
```

### 단일 Assembly 예시 (BLK-001)

```csharp
// [BLK-001] Turn-Aware A* Pathfinding
// [1] Assembly : PathSolver Assembly
// [1] Part     : TurnAwareAStarPart (ACTIVE)
//             Downgrade → BasicAStarPart (회전 코스트 제거)
// Piece    : 멀티소스 A* 탐색 — 전임자 DAG + DFS K경로 열거
```

### 다중 Assembly 예시 (BLK-002)

```csharp
// [BLK-002] GPU Instancing Cell Renderer
// [1] Assembly : RenderPipeline Assembly
// [1] Part     : GPUInstancedPart (ACTIVE)
//             Downgrade → CPUMeshBakedPart (저사양 대응)
// ──────────────────────────────────────────────
// [2] Assembly : SortJob Assembly
// [1] Part     : BurstSortJobPart (ACTIVE)
//             Downgrade → MainThreadSortPart
// ──────────────────────────────────────────────
// [3] Assembly : BufferUpload Assembly
// [1] Part     : PartialUploadPart (ACTIVE)
//             Downgrade → FullUploadPart
```

## 파일 내 기능 블록 구분

단일 파일에 여러 Part/Piece가 섞이면 주석 구분선과 좌표 번호로 분리한다:

```csharp
// [BLK-001][1][1]
// Description: 그리드 초기화 및 인덱스 계산
public CellGrid(int width, int height, int depth) { ... }

// [BLK-001][1][2]
// Description: 이웃 셀 조회 (경계 검사 포함)
public bool TryGetNeighbor(CellIndex cell, Direction dir, out CellIndex neighbor) { ... }
```

`[BLK-XXX][Assembly번호][Part번호]` 형식이 [[BLK_좌표_시스템]]에서 다루는 *함수 단위 좌표*다.

## 어노테이션이 가능하게 하는 것

### 1. Grep 정밀 검색

```powershell
# BLK-001 전체
grep -r "// \[BLK-001\]" Assets/Core/Scripts/

# BLK-001 Assembly 1 Part 1만
grep -r "// \[BLK-001\]\[1\]\[1\]" Assets/Core/Scripts/
```

[[Sonar_Protocol]]의 RULE 1을 위반하지 않는 정밀 검색이 가능한 이유는 이 어노테이션이 *grep-friendly 식별자*를 코드에 새겨두기 때문.

### 2. 다운그레이드 시스템

각 Part는 *Active 상태*와 *Downgrade Target*을 명시한다. 환경/성능 제약에 따라 Active와 Downgrade를 교체할 수 있다. 교체 절차는 [[manage_폴더_역할분리]]의 `Block.md` + `Function_Block_Archive.md` + `Management.md` 트리오로 추적된다.

### 3. Surgical Changes 강제

Part 교체 시 *해당 파일만* 수정하고 다른 Block/Assembly 파일은 건드리지 않는다. 인터페이스(진입점)는 유지하고 *구현만* 교체한다. 이는 [[Mastermind_Architecture_Manifesto]]의 카파시 정신의 가장 구체적 시행 사례.

## Part 전환 절차 (Downgrade / Upgrade)

```
1. 전환 대상 확인
   Block.md의 해당 BLK → Assembly → Part 항목에서 Downgrade Target과 난이도 확인
2. 영향 파일 목록 추출
   Block.md Pieces 목록에서 수정 대상 파일 확인
   DowngradeManagement.md (Management.md)에 전환 전 상태 기록
3. 전환 실행
   - 해당 파일만 수정 (다른 Block/Assembly 파일 수정 금지)
   - 인터페이스 유지, 구현만 교체
   - 기존 Active Part는 #if 가드 또는 별도 파일로 보존
4. 검증
   - 컴파일 통과
   - 기존 기능 재현 시나리오 확인
   - DowngradeManagement.md 갱신
```

## 전환 난이도 등급

| 등급 | 설명 |
|---|---|
| ★☆☆ | 상수·플래그·단일 함수 교체. 컴파일 에러 없이 즉시 적용 |
| ★★☆ | 인터페이스 구현 교체. 관련 2~5개 파일 수정 |
| ★★★ | 시스템 단위 교체. 연동 시스템 수정·씬 재설정 필요 |

## 신규 Block 추가 절차

1. `Block.md`에 `BLK-XXX` 항목 추가 (Assemblies/Parts/Pieces 포함)
2. 해당 소스 파일 상단에 헤더 어노테이션 추가
3. `DowngradeManagement.md` 블록 테이블에 행 추가
4. `docs/work.md`에 Entry 기록 ([[Producer_QualitySentinel_Reporter_게이트]] reporter)
5. `Review.md` 갱신 (필요 시)

## 관련 노트

- 좌표 인덱싱: [[BLK_좌표_시스템]] / [[Dictionary_md_좌표_시스템]]
- manage 폴더 5파일: [[manage_폴더_역할분리]]
- 정밀 검색 컨텍스트: [[Sonar_Protocol]]
- 절제력 철학: [[Mastermind_Architecture_Manifesto]]
- RX_1 어휘집 인덱스 (BLK 의무화·asmdef 레이어 통제): [[code_style_lexicon]]
- 외부 사상 매핑 (Surgical Changes 본체): [[Karpathy_4대_코딩원칙]]

## 출처

- raw/modular-architecture.md (2026-05-22 유입) — 전문 (계층 정의·어노테이션·전환 절차·난이도)
- raw/ecosystem-atomic-analysis.md (2026-05-22 유입) — §3-D 모듈러 아키텍처 어노테이션 원자
