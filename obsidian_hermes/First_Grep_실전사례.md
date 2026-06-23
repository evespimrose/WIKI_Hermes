---
tags: [llm-wiki, 검색, 토큰통제, 사례]
date_created: 2026-05-26
last_modified: 2026-06-16
---

# First-Grep 워크플로우 실전 사례

[[Sonar_Protocol]]과 [[Dictionary_md_좌표_시스템]]을 실제 코드 탐색에 적용한 사례들.

## 일반 프로젝트: 전투 시스템 수정 사례

### 상황

**유저**: "전투 시스템에서 폭발 로직의 대미지 계산 과정을 수정해줘"

### First-Grep 워크플로우

#### Step 1: Dictionary 읽기 (§3 키워드 인덱스)

```
dictionary.md § 3 키워드 인덱스 조회:

"폭발 | 대미지" → BLK-042
```

**토큰 소모**: 10토큰

#### Step 2: § 1 파일 인덱스 조회

```
BLK-042 → Assets/Core/Scripts/Gameloop/ExplosionSystem.cs
```

**토큰 소모**: 5토큰
**누적**: 15토큰

#### Step 3: Glob으로 확인 (선택사항)

```bash
Glob: Assets/Core/Scripts/Gameloop/**/*.cs
결과: ExplosionSystem.cs, DamageFormula.cs, ...
```

**토큰 소모**: 10토큰
**누적**: 25토큰

#### Step 4: 필요한 파일만 Read

```
Read: ExplosionSystem.cs (전체 파일, 필요함)
Read: DamageFormula.cs (필요 부분만)
```

**토큰 소모**: ~300토큰
**누적**: ~325토큰

#### Step 5: Edit으로 정밀 수정

```
Edit: ExplosionSystem.cs의 DamageCalculate() 메서드 수정
```

**최종 토큰**: ~325토큰

### 비교: 전통적 Grep 방식

```
무제한 Read: 프로젝트 모든 파일 스캔
├─ Assets/Core/ 폴더 전부 읽음
├─ Gameloop/ 폴더 전부 읽음
├─ UI, Physics, AI 폴더도 "혹시 모르니" 읽음
└─ 총 1000+ 파일, 5000 토큰 소모

결과: 관련 없는 정보 95% 이상 (토큰 낭비)
```

### 효과

| 지표 | First-Grep | Grep 무제한 | 개선율 |
|---|---|---|---|
| 토큰 소모 | 325 | 5000 | **93% 절감** |
| 조회 시간 | 5초 | 30초 | **83% 단축** |
| 정확도 | 100% (좌표 보증) | ~60% (관련 없는 파일) | **67% 향상** |

---

## RX_1 프로젝트: 셀 렌더러 정렬 로직 찾기

### 상황

**유저**: "CellRenderer 정렬 로직 어디 있어?"

### First-Grep 단계별 진행

#### Step 1: dictionary.md § 3 조회

```
RX_1의 dictionary.md 키워드 인덱스 (한글 + 영문):

"Sort | 정렬" → BLK-002
```

**토큰**: 8토큰

#### Step 2: § 1 파일 인덱스 확인

```
BLK-002 (GPU Instancing Renderer)
  → Presentation/CellRenderer.cs
  → Rendering/Sort/SortJob.cs
  → Rendering/Sort/Buffer.cs
```

**토큰**: 5토큰
**누적**: 13토큰

#### Step 3: Read CellRenderer.cs

```
파일에서 "정렬" 관련 메서드 발견:
  - RenderSorted()
  - ApplySortJob()
```

**토큰**: ~150토큰
**누적**: ~163토큰

#### Step 4: (필요시) Block.md 참조

```
Block.md에서 BLK-002 / SortJob Assembly 확인:

Assembly: SortJob
  ├─ BurstSortJobPart (ACTIVE)
  └─ MainThreadSortPart (DOWNGRADE)
```

**토큰**: 50토큰 (선택사항)

### 결과

**조회 완료**: CellRenderer.cs의 RenderSorted() → SortJob 연결 파악

**토큰 총합**: ~163토큰 (Step 4 선택 시 ~213)

**비교**:
- Grep 무제한: 400+ 토큰
- **개선율**: 60% 이상 절감

---

## Sonar Protocol 준수 체크리스트

### ✓ 올바른 사용

```
Step 1: dictionary.md 먼저 읽기
Step 2: § 1 또는 § 3에서 BLK 좌표 확보
Step 3: Glob/Grep으로 정확한 파일 조회
Step 4: Read로 필요한 파일만 로드
Result: O(1) 시간 복잡도, 토큰 극소화
```

### ✗ 금지된 사용

```
❌ find / grep -r / rg (전체 코드 검색)
❌ "일단 모든 파일 읽어보자"
❌ Glob 없이 임의로 파일 접근
❌ dictionary 건너뛰기
```

---

## 워크플로우 효과 정리

### 토큰 절감 (회당)

| 작업 | 전통 방식 | First-Grep | 절감율 |
|---|---|---|---|
| 파일 위치 특정 | 1000+ | 25 | 97.5% |
| 메서드 위치 확인 | 2000+ | 150 | 92.5% |
| 아키텍처 이해 | 3000+ | 200 | 93.3% |

### 컨텍스트 생명 연장

| 지표 | 무제한 Read | First-Grep |
|---|---|---|
| 회당 토큰 | 500~1000 | 50~300 |
| 120턴 총 토큰 | 60,000~120,000 | 6,000~36,000 |
| 단축율 | baseline | **70~90% 절감** |

**결과**: 120턴 이상의 장시간 운영에서도 상태 붕괴 없음 (([[4계층_메모리_아키텍처]]))

---

## 실제 RX_1 dictionary.md 예시 (축약)

```markdown
## § 3 — 키워드 인덱스

| 키워드 | BLK | 비고 |
|---|---|---|
| 경로 | BLK-001 | TurnAwareAStar, CellGrid |
| GPU | BLK-002 | Renderer, Instancing |
| 정렬 | BLK-002 | Sort, Burst |
| DDA | BLK-003 | Picking, Range |
| 페이즈 | BLK-004 | StateMachine, Phase1/2/3 |
| ...| ... | ... |
```

**한 줄 조회로 목표 BLK 확보 → 이어서 § 1로 파일 위치**

---

## 관련 노트

- 좌표 의미론: [[BLK_좌표_시스템]]
- 탐색 규칙: [[Sonar_Protocol]]
- Dictionary 구조: [[Dictionary_md_좌표_시스템]]
- RX_1 사례: [[RX_1_manage_DB_스키마]]
- 토큰 통제: [[LLM_통제_철학_6대원칙]]
- codegraph 적용 경계(언제 grep이 이기나): [[Codegraph_MCP_통합]]

## 출처

- `raw/knowledge_state_report.md` (2026-05-26 유입) — Part C 일반 케이스, RX_1 적용 사례
