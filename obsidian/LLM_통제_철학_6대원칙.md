---
tags: [llm-wiki, llm-워크플로우, 설계원칙]
date_created: 2026-05-22
last_modified: 2026-06-22
---

# LLM 통제 철학 6대 원칙

[[LLM_컨텍스트_5대_문제]]에 대한 설계 응답. [[LLM_워크플로우_생태계]] 전체가 이 여섯 원칙 위에 세워져 있다.

## 1. 토큰은 1급 자원이다 (Tokens are First-Class Resources)

모든 설계 결정에 "이 동작이 몇 토큰을 쓰는가?" 질문이 선행한다. "LLM이 모든 것을 기억해야 한다"는 가정을 거부하고 외부에 저장한 뒤 필요할 때만 가져온다.

대표 적용:
- Handover.md Reading Map: 1,600줄 → 필요한 100~300줄만
- BLK 인덱싱 → 전체 파일 Read 대신 grep 50자 스니펫 (→ [[BLK_좌표_시스템]])
- doc-context: 동일 텍스트 매 턴 재전송 차단 (→ [[doc_context_입력_워크플로우]])
- quality-sentinel: `git diff HEAD only` 강제 (→ [[Producer_QualitySentinel_Reporter_게이트]])

### 도구 스키마도 토큰이다 (MCP Schema Footprint)

토큰 회계는 도구 *호출*만이 아니라 도구의 *존재*에도 적용된다. MCP 도구는 호출하지 않아도 그 description(스키마)이 매 턴 context에 상주하는 고정 비용이다. 예로 sequentialthinking MCP의 tool description은 ≈ 600토큰 = 전형적 context의 약 3%를 *항시* 점유한다. "설명이 길수록 좋은 도구"라는 직관은 토큰 경제학적으로 나쁜 트레이드오프 — 도구를 늘릴수록 미사용 스키마가 누적되어 베이스라인을 잠식한다.

함의: 도구 채택은 schema 크기를 토큰 기준으로 평가하고, 상시 노출이 불필요한 도구는 allowlist로 등록 자체를 거른다. 자체 도구를 다수 등록하는 [[Codegraph_MCP_통합]]도 같은 비용 압력을 받는다.

이 비용은 *정량적으로* 무겁다. 도구 약 30개를 상시 노출하면 그 스키마만으로 턴당 ≈ 8k 토큰이 고정 소모된다 — 베이스 컨텍스트가 ~3k라면 도구 노출만으로 +260%다. 대응은 *allowlist 필터*다(code-review-graph의 `CRG_TOOLS` / `_apply_tool_filter` 사례): 그 턴에 쓸 도구만 노출하면 70~85%를 절감해 +30~60% 수준으로 떨어진다. "도구는 부를 때만 비용"이 아니라 "*존재만으로* 비용"이라는 회계가 [[최소컨텍스트_진입규약]]의 턴 예산과 짝을 이룬다 — 진입 조회량과 도구 노출량을 둘 다 통제해야 베이스라인이 지켜진다.

### 크기가 아니라 구성이다 (Context Budgeting)

토큰을 1급 자원으로 다룬다는 것은 *컨텍스트의 양*이 아니라 *구성*을 예산화한다는 뜻이다. Chroma Research의 대조 실험은 이를 극적으로 보였다 — 113k 토큰의 전체 히스토리를 그대로 넣었을 때보다 *짧게 정제한 프롬프트*가 성능에서 크게 앞섰다. 더 많이 넣을수록 좋은 게 아니라, *무엇을 넣고 무엇을 뺐는가*가 결과를 가른다.

함의: 컨텍스트는 "채우는" 대상이 아니라 *편성하는* 대상이다. 같은 토큰 예산이라면 방해 정보([[LLM_컨텍스트_5대_문제]] Context Rot)를 덜어내고 신호 밀도를 높이는 편성이 이긴다. 본 볼트의 [[doc_context_입력_워크플로우]]·핸드오버 Reading Map·BLK 좌표가 모두 "전체를 넣지 말고 정제분만 편성하라"의 구현이다.

### 프리픽스 안정화 = KV 캐시 (CacheAligner)

토큰 회계는 *캐시*에도 적용된다. 프로바이더의 KV 캐시는 프롬프트의 *불변 프리픽스*가 일치할 때 그 부분을 대폭 할인한다(예: Anthropic은 최소 1,024토큰 일치 시 캐시 히트). 따라서 "변하지 않는 것을 앞에, 변하는 것을 뒤에" 배치하면 같은 내용도 더 싸진다.

이는 본 볼트의 긴 고정 프리픽스 — CLAUDE.md·session-start 주입·CORE_RULES — 가 *왜 비용 효율적인가*의 이론적 근거다. 매 턴 동일하게 앞에 오는 이 블록들은 캐시 히트로 할인된다. 설계 규칙: 시스템 프롬프트의 안정 영역을 *동결*(hot-zone freeze)해 프리픽스를 흔들지 않는다(같은 정신의 산출물 레벨 구현은 [[결정론_검증_게이트]]의 불변식). 단 캐시 정책은 프로바이더별로 다르므로 수치는 참고치로 둔다.

이 원리는 이론에 그치지 않고 `cache-aligner` 스킬(HR5)로 *실증 구현*되어 SessionStart 훅의 프리픽스를 byte-equal로 동결한다 — 불변/가변 블록 분리·두 진입점 byte-equal·결정론 검증의 상세 규율은 [[CacheAligner_프리픽스_안정화]].

## 2. 상태는 LLM 밖에 저장한다 (Externalize State)

LLM 컨텍스트 윈도우는 휘발성이다. 영속 상태는 모두 파일로 외부화한다. AI는 "기억"하지 않고 "읽어서 확인"하는 패턴으로 전환한다.

외부화 대상:
- `.claude/memory-bank/.riper-state` — 현재 RIPER 모드·플랜 경로
- `manage/dictionary.md` — 프로젝트 구조 인덱스
- `docs/work.md` — 작업 이력
- `.claude/memory-bank/{branch}/plans/` — 플랜 영속화
- `.claude/memory-bank/pre_compact_backup.md` — 컴팩션 직전 백업

자세한 계층 구조는 [[4계층_메모리_아키텍처]]를 본다.

## 3. 프롬프트보다 훅이 강하다 (Hooks > Prompts)

프롬프트는 신뢰할 수 없다. 결정론적 강제가 필요하면 훅으로 구현한다. "AI가 잊을 수 있는 규칙"은 훅으로 옮긴다.

| 강제 대상 | 약한 방식 | 강한 방식 |
|---|---|---|
| bash 탐색 금지 | "find 쓰지 마세요" | `cave-man-guard.sh`가 PreToolUse:Bash 차단 |
| 컨텍스트 주입 | "CLAUDE.md 읽어주세요" | `session-start.sh` 자동 주입 |
| 컴팩션 보호 | "전에 저장하세요" | `pre-compact.sh` 자동 백업 |
| BLK 검증 | "BLK 태그 다세요" | `validate-cxt.sh` 검증 실패 차단 |

훅의 카탈로그는 [[컴팩션_생존_전략]]과 [[Sonar_Protocol]]에서 다룬다.

## 4. 모듈은 독립 설치 가능해야 한다 (Modular Composability)

워크플로는 4개 독립 모듈로 분해되고, 각 모듈은 단독·결합·부분 설치를 모두 허용한다 (skills only / full / light). 풀 패키지가 강제되지 않고 프로젝트 성격에 맞게 조합한다.

모듈 목록은 [[LLM_워크플로우_생태계]]의 4대 서브시스템 표를 참조한다.

## 5. 단일 책임을 강제한다 (Single Responsibility per Role)

역할의 모호함은 환각의 주된 원천이다. 모든 역할은 단 하나의 책임만 가지며, 역할 정의의 절반은 *무엇을 하지 않는가*다.

| 역할 | 단일 책임 | 절대 하지 않는 것 |
|---|---|---|
| quality-sentinel | 코드 컨벤션 검증 | 코드 수정·설계 결정 |
| reporter | work.md Entry 기록 | 코드 변경·아키텍처 결정 |
| writer | 플랜 작성 | 코드 구현·기술 결정 |
| ExternalHandOver AI | 텍스트 영문 구조화 | 원문 질문 답변·의견 추가 |
| doc-context skill | cxt 파일 즉시 실행 | 재확인 요청·요약 출력 |

이 원칙의 가장 구체적 구현은 [[Producer_QualitySentinel_Reporter_게이트]]와 [[External_AI_역할분리]]다.

## 6. 소형과 중·대형을 다르게 다룬다 (Scope-Differentiated Gates)

모든 작업에 동일 절차를 적용하는 것은 비용 낭비다. *플랜 파일 존재 여부*가 규모 판단의 단일 기준이며, 단순 작업에는 검증 게이트를 생략한다.

| 규모 | 기준 | 절차 |
|---|---|---|
| 소형 | 단일 함수, 버그픽스, 플랜 없음 | 직접 처리 → reporter 기본 모드 |
| 중·대형 | 멀티파일, 신규 시스템, 플랜 존재 | RIPER 풀워크플로 → quality-sentinel → reporter |

자세한 규모별 라우팅은 [[작업_규모별_워크플로]]를 본다.

## 의도된 트레이드오프

이 여섯 원칙은 다음을 *의도적으로* 포기한다.

- 자유로운 탐색 ↔ 좌표 기반 접근 — 일관된 토큰 비용·환각 차단을 얻는다
- 즉시성 ↔ 단계화 — RESEARCH→PLAN→EXECUTE의 품질을 얻는다 ([[RIPER_5단계_상태머신]])
- 범용성 ↔ 워크플로 강제 — 준수 프로젝트에서 극단적 효율을 얻는다
- 단순함 ↔ 모듈 분리 — 선택 설치 가능한 유연성을 얻는다

같은 철학을 다른 어조로 진술한 글은 [[Mastermind_Architecture_Manifesto]]에 있다.

## 외부 코딩 원칙과의 매핑

본 6원칙이 *vault 내부 운영 철학*이라면, 외부 일반 코딩 원칙으로 [[Karpathy_4대_코딩원칙]]이 동일 사상을 *행동 권고* 수준에서 진술한다. 두 체계가 어떻게 대응되는지(예: Surgical Changes ↔ Block 어셈블 단위 교체)는 그 노트의 §"매핑" 표를 본다 — 4원칙은 *공리*, 본 6원칙·게이트·어노테이션은 그 *시행 체계*다.

## 기계식 강제 (Automated Enforcement)

[[Mastermind_Architecture_Manifesto]]에서 선언한 "도덕적 지침 아닌 물리적 강제"의 구체적 구현.

### 훅 기반 강제

| 규칙 | 약한 방식 | 강한 방식 |
|---|---|---|
| bash 탐색 금지 | "find 쓰지 마세요"(권고) | `cave-man-guard.sh`가 PreToolUse 차단 |
| 컨텍스트 관리 | "CLAUDE.md 읽어주세요" | `session-start.sh` 자동 주입 |
| 컴팩션 보호 | "전에 저장하세요" | `pre-compact.sh` 자동 백업 |
| BLK 검증 | "BLK 태그 달아주세요" | `validate-cxt.sh` 검증 실패 시 차단 |

**의도**: 에이전트가 "잊을 수 있는 규칙"을 시스템이 물리적으로 강제한다. [[Try_Skill_타당성_검증]]과 함께 작동해 매 스킬 실행마다 의도를 검증한다.

### 모듈별 강제 메커니즘

| 원칙 | 강제 대상 | 구현 | 범위 |
|---|---|---|---|
| 원칙 3 (훅 > 프롬프트) | [[Sonar_Protocol]] | cave-man-guard.sh | 파일 탐색 |
| 원칙 5 (단일 책임) | [[Producer_QualitySentinel_Reporter_게이트]] | 역할별 권한 분리 | 에이전트 협업 |
| 원칙 2 (상태 외부화) | [[4계층_메모리_아키텍처]] | .riper-state, memory-bank/ | 컨텍스트 관리 |
| 원칙 1 (토큰 1급) | [[Dictionary_md_좌표_시스템]] | BLK 인덱싱, cave-man-guard | 코드 탐색 |

## 출처

- raw/Workflow-Design-Philosophy.md (2026-05-22 유입) — §2 6대 원칙, §12 의도된 트레이드오프
- raw/gemini-code-1779431417344.md (2026-05-22 유입) — 같은 원칙을 "기계식 통제 섀시" 비유로 진술
- raw/sequentialthinking_입국심사.md (2026-06-16 편입) — Atom 4 MCP Schema 토큰 footprint(≈600토큰=context 3%). docs/Try_AtomImport_DLC_vs_Workflow 결론(C분류=위키 노트)에 따른 편입
- raw/code-review-graph_입국심사.md (2026-06-17 편입) — Atom 3 MCP 도구 과잉 비용(30도구 ≈ 8k/턴)·allowlist 70~85% 절감(`_apply_tool_filter`)
- raw/aisparkup_context_rot_입국심사.md (2026-06-17 편입) — Atom 6 컨텍스트 예산화(크기≠구성, 113k 전체 vs 정제 프롬프트)
- raw/headroom_입국심사_2026-06-14.md (2026-06-17 편입) — Atom 5 CacheAligner 프리픽스 안정화 KV 캐시(원칙1 §프리픽스 안정화; 2026-06-22 실증 구현·상세는 [[CacheAligner_프리픽스_안정화]]로 분리)
