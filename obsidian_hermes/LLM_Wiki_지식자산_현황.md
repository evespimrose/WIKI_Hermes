---
tags: [llm-wiki, 지식현황, 아키텍처]
date_created: 2026-05-26
last_modified: 2026-06-14
---

# LLM Wiki 지식자산 현황

현재 중앙 지식 저장소에 축적된 개념들의 맵과 확장 방향.

## 현재 지식 그래프: 32개 노트

### 중추 개념 (일반 영역, 21개)

```
┌─────────────────────────────────────────┐
│  LLM_워크플로우_생태계 (허브)             │
│  전체 생태계의 구조와 진화 맥락          │
└──────────────┬──────────────────────────┘
               │
      ┌────────┼────────┐
      │        │        │
   A) 토큰     B) 설계  C) 협업
   통제        원칙    워크플로우
      │        │        │
```

#### A. 토큰 통제 영역 (5개 노트)

인간의 뇌 용량과 LLM의 컨텍스트 윈도우라는 공통의 유한 자원 관리.

```
LLM_컨텍스트_5대_문제 (문제 정의)
  ↓
Dictionary_md_좌표_시스템 (압축 전략)
  ├─ Sonar_Protocol (탐색 규칙)
  └─ BLK_좌표_시스템 (의미론)

4계층_메모리_아키텍처 (계층화)
  └─ 컴팩션_생존_전략 (생명 연장)
```

**핵심**: 무제한 Read → Dictionary + BLK로 O(N) → O(1) 변환

#### B. 설계 원칙 영역 (4개 노트)

무한성을 거부하고 결정론적 시스템으로 강제하는 철학.

```
LLM_통제_철학_6대원칙 (분석적 원칙)
  ↔ Mastermind_Architecture_Manifesto (철학적 매니페스토)

Karpathy_4대_코딩원칙 (행동 권고)
  └─ Block_Assembly_Part_Piece_컨벤션 (구체적 구현)
```

**핵심**: "도덕적 지침"이 아니라 훅과 구조로 물리적 강제

#### C. 협업 워크플로우 영역 (5개 노트)

다중 에이전트 또는 외부 AI와의 안전한 협력.

```
3Tier_에이전트_스튜디오 (계층 구조)
  └─ Producer_QualitySentinel_Reporter_게이트 (역할 게이트)

External_AI_역할분리 (외부 AI 권한)
  └─ Try_Skill_타당성_검증 (검증 프로토콜)

작업_규모별_워크플로우 (규모별 라우팅)
```

**핵심**: 단일 책임 + 자동 게이트로 에이전트 야생성 차단

#### D. 운영 체계 영역 (4개 노트)

상태 기계와 입출력 파이프라인 표준화.

```
RIPER_5단계_상태머신 (작업 상태)
  └─ RULE7_PRD_Spatial_Mapping (지시 번역)

doc_context_입력_워크플로우 (입력 형식)
  └─ cxt_파일_포맷_컨벤션 (파일 규칙)
```

**핵심**: 모든 작업이 추적 가능한 상태 기계 위에서 진행

#### E. 관리 정책 영역 (3개 노트) — 신규

```
LLM_Wiki_운영체계 (3단계 파이프라인)
  ├─ Git_기반_다중PC_동기화 (동기화 전략)
  └─ manage_폴더_역할분리 (파일 역할)
```

**핵심**: vault 입출력의 표준화 + 다중 PC 공유

---

### 프로젝트 특화 지식 (RX_1, 11개)

[[RX_1_manage_DB_스키마]]를 중심으로 한 실제 프로젝트 인스턴스.

```
RX_1_manage_DB_스키마 (프로젝트 인덱스)
  │
  ├─ BLK-001~013 (13개 도메인)
  ├─ manage/ 5파일 통합 DB
  │  ├─ dictionary.md § 0/0-1/1/2/3 (실제 섹션)
  │  ├─ Block.md (Assembly/Part)
  │  ├─ Function_Block_Archive.md (다운그레이드 옵션)
  │  ├─ Management.md (실행 이력)
  │  └─ modular-architecture.md (컨벤션)
  │
  └─ 상태 추적 폴더
     ├─ RX_1/RX_1_인덱스.md
     ├─ RX_1/state_claude_mem.md
     ├─ RX_1/state_riper.md
     ├─ RX_1/state_plan.md
     ├─ RX_1/state_dictionary.md
     ├─ RX_1/state_query_logs.md
     ├─ RX_1/state_update_history.md
     ├─ RX_1/conventions/code_style_lexicon.md
     └─ RX_1/graveyard/Graveyard_*.md (폐기 패턴)
```

**특징**:
- 일반 개념은 obsidian/root에
- 프로젝트 특화는 obsidian/RX_1/에 계층화
- 상태 추적으로 프로젝트 진화 기록

---

## 개념 간 연결 강도

### 중추 허브

| 노트 | 인링크 | 설명 |
|---|---|---|
| `LLM_워크플로우_생태계` | 15+ | 모든 개념의 진입점 |
| `Dictionary_md_좌표_시스템` | 8+ | 토큰 통제의 핵심 |
| `LLM_통제_철학_6대원칙` | 12+ | 설계 철학의 근거 |
| `RIPER_5단계_상태머신` | 6+ | 작업 흐름의 표준 |

### 양방향 링크 분포

**강한 연결** (양쪽 모두 상대 참조):
- Dictionary ↔ Sonar_Protocol
- RIPER ↔ RULE7_PRD_Spatial_Mapping
- 6대원칙 ↔ Mastermind_Manifesto
- Karpathy_4대 ↔ Block_Assembly_Part

**약한 연결** (한쪽만 참조):
- 대부분의 프로젝트 특화 → 일반 개념

---

## 다음 진화 방향 3단계

### 1단계: Self-Healing Wiki (자가 치유 루프)

**현재**: 수동으로 dictionary 갱신 (알림만)

**진화**: RIPER의 Review 단계에서 dictionary 갱신 초안 **자동 제안**
- 코드 변경 감지 → 영향받는 BLK 파악
- 새로운 모듈 추가 감지 → dictionary § 1 갱신 후보 제시
- 사용자 검토 후 자동 병합

### 2단계: Mastermind Agent (최상위 오케스트레이션)

**현재**: 사용자가 compile-wiki, move-to-raw 매번 호출

**진화**: Mastermind가 자동으로 필요한 스킬 라우팅
```
유저: "코드 수정해줘"
  ↓
Mastermind: RIPER → Investigate (dictionary 참조)
  ↓
Mastermind: Plan (플랜 생성)
  ↓
Mastermind: Execute (코드 수정 + 자동 dictionary 갱신 제안)
  ↓
Mastermind: Review (검증 + 컴팩션 자동화)
```

### 3단계: Multi-Vault 확장 (다중 저장소 연합)

**현재**: 단일 vault (D:\Fork\WIKI)

**진화**: ArcynGame, 미래 신규 Unity 프로젝트 등 다중 vault 지원
```
MetaVault/
├─ WIKI/ (LLM 워크플로우 중앙)
├─ RX_1/ (RX_1 프로젝트)
├─ ArcynGame/ (게임 프로젝트)
└─ [새로운 프로젝트]/
```

각 vault는 독립적이면서도 일반 개념을 공유.

---

## 자산 규모 현황

| 항목 | 수량 | 크기 |
|---|---|---|
| 일반 노트 | 21개 | ~500KB |
| 프로젝트 특화 노트 | 11개 | ~200KB |
| archive/ (원본) | ~10개 파일 | ~50KB |
| 총 wiki 크기 | - | ~750KB |
| git 저장소 크기 | - | ~2MB (메타데이터 포함) |

**평가**: 
- 2026년 5월 시점 극히 가볍고 효율적
- 10년 보관 기준 10MB 이상 가능 (여전히 관리 가능)

---

## 알려진 한계와 개선 기회

### 현재 한계

1. **자동 검증 부재**: dictionary 갱신을 사람이 수동으로 결정
2. **Mastermind 없음**: 모든 스킬을 사용자가 명시적으로 호출
3. **단일 프로젝트**: RX_1만 구체적 사례 (일반화 부족)

### 개선 기회

1. **dictionary 동기화 자동화** (1단계)
   - 파이프라인 통합: Edit → detect change → dictionary update suggestion
   
2. **에이전트 학습 가속** (2단계)
   - claude-mem이 자동으로 BLK 지식 로드
   - Mastermind가 dictionary → BLK → file 번역 자동화

3. **다중 프로젝트 사례 추가** (3단계)
   - ArcynGame manage/ 통합
   - 신규 프로젝트 온보딩 가이드 작성

---

## 관련 노트

- 생태계 전체 개요: [[LLM_워크플로우_생태계]]
- 토큰 통제: [[LLM_통제_철학_6대원칙]]
- 매니페스토: [[Mastermind_Architecture_Manifesto]]
- 실제 사례: [[RX_1_manage_DB_스키마]]
- 진화 맥락: [[Mastermind_Architecture_Manifesto#논쟁 및 관점 차이]]

## 출처

- `raw/knowledge_state_report.md` (2026-05-26 유입) — Part G 지식자산 현황, Part H 진화 방향
