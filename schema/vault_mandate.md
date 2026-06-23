# vault_mandate — 볼트 지향 북극성

> 이 볼트가 "무엇에 관한 곳인가". 입국심사(`compile-wiki a`)의 방향성 판정과 자율 스카우팅(헤르메스)의 1차 수집 기준이 되는 단일 기준 문서. `scout_lexicon.md`와 짝.
> **최종 진화형 레퍼런스**: `docs/Roadmap/Workflow_End_To_End_LoadMap.md` — 이 볼트가 지향하는 완성 상태의 공식 설계도.

## 한 줄 정의

**LLM/AI 에이전트를 결정론적으로 통제하는 워크플로우 엔지니어링 + 그 지식을 누적·공유하는 위키 메타시스템**의 지식 베이스.

## 최종 진화형 (목표 상태)

`docs/Roadmap/Workflow_End_To_End_LoadMap.md` §2~5 요약:

> **"LLM의 태생적 한계를 기계적 아키텍처와 프로토콜로 완전히 통제하는 닫힌 생태계"**
>
> - 코드베이스: asmdef + Clean Architecture + BLK 인덱싱 → 에이전트가 "어디에 무엇이 있는지" 절대 잊지 않는 환경
> - 위키: 마크다운 벡터DB 온디맨드 시맨틱 질의 → 매 턴 주입 없이 필요 시만 참조하는 능동 신경망
> - AI: 서브에이전트 Conclusion → 압축 마크다운 저장 → Codegraph 노드 등록 → 500턴+ Massive 윈도우에서 환각 0
> - UX: "~~ 해줘" 한 줄 → Mastermind가 팀 동적 빌드 → end-to-end 초미세 토큰 완수

---

## 핵심 관심사 (in-scope)

- 토큰 통제 — Cave-Man Protocol, Dictionary/Codegraph 인덱싱, L1 hook 강제
- 통제 철학 — 6대원칙, Mastermind 기계식 통제 섀시, Karpathy
- 에이전트 오케스트레이션 — 3-Tier 스튜디오, 하네스 엔지니어링, 멀티에이전트 검증
- 메모리·상태 — 4계층 메모리, 컴팩션 생존, RIPER 상태머신
- 위키 메타시스템 — 카파시 위키 패턴, 저장 5대필터, 맥락 오염 방지, 3레이어
- 프로젝트 인스턴스 — RX_1(경로탐색), Western Salon(클린 아키텍처)
- 일반 소프트웨어 아키텍처 — Clean Architecture, DIP, asmdef 강제

---

## 현황 갭 분석 (2026-06-12 기준)

### ✅ 이미 있는 것 (obsidian 보유)

**토큰 통제·탐색 기반:**
- [[Cave_Man_Protocol]] — 무차별 탐색 금지, BLK 좌표 접근 강제
- [[BLK_좌표_시스템]] / [[Dictionary_md_좌표_시스템]] — 기능명세 공간 매핑
- [[Codegraph_MCP_통합]] — Codegraph grep 기반 코드 접근
- [[L1_Hard_Gate_훅체계]] — 결정론적 훅 강제 구조

**통제 철학·원칙:**
- [[LLM_통제_철학_6대원칙]] — 6대 원칙 전체
- [[LLM_컨텍스트_5대_문제]] — 풀어야 할 문제 정의
- [[Mastermind_Architecture_Manifesto]] — 통제 철학 선언 (원칙/철학 레벨)
- [[Karpathy_4대_코딩원칙]]

**에이전트 오케스트레이션:**
- [[3Tier_에이전트_스튜디오]] — Mastermind·Worker·Specialist 계층
- [[AI_네이티브_멀티에이전트_운영]] — 10-에이전트 운영 패턴
- [[하네스_엔지니어링]] / [[Agent_Skill_Orchestrator_3요소]] — 에이전트 실행 환경
- [[Producer_QualitySentinel_Reporter_게이트]] — QS·Reporter 역할 분리
- [[프롬프트_컨텍스트_하네스_패러다임]]

**메모리·상태 관리:**
- [[4계층_메모리_아키텍처]] — L1~L4 메모리 레이어
- [[RIPER_5단계_상태머신]] — 워크플로우 단계 제어
- [[컴팩션_생존_전략]] — 컴팩션 전후 핵심 상태 보존 (기본)
- [[doc_context_입력_워크플로우]] — 세션 시작 컨텍스트 주입

**위키 메타시스템:**
- [[카파시_LLM_위키_패턴]] / [[Raw_Wiki_Schema_3레이어]] / [[위키_저장_5대필터]]
- [[맥락_오염_방지]] / [[위키_기반_에이전트_맥락공유]]
- `schema/` 레이어(vault_mandate · scout_lexicon · LOG) — 헌법 레이어

**코드베이스 기반:**
- [[Clean_Architecture_4계층]] / [[asmdef_레이어_경계강제]] / [[의존성_역전_DIP]]
- [[Western_Salon_Clean_Architecture]] — 인스턴스 구현 사례

---

### ❌ 필요한 것 (미구현·미존재 — 로드맵 요구사항)

아래 항목은 `docs/Roadmap/Workflow_End_To_End_LoadMap.md`가 요구하나 볼트에 없거나 설계 문서만 존재하고 실체가 없는 것들이다.

#### 🔴 Priority 1 — 환각 0 파이프라인의 핵심 병목

| 필요 항목 | 로드맵 근거 | 현재 상태 |
|---|---|---|
| **Subagent Conclusion 파싱 표준화** | §8.1 — 출력 스키마, 필수 메타데이터(출력 유형·BLK 좌표·생성 시간), 파싱 실패 fallback | ❌ 노트 없음 |
| **Conclusion → Codegraph 노드 등록 파이프라인** | §2.3, §6.2 — 서브에이전트 결과를 극소 마크다운으로 저장 + Codegraph 노드 자동 등록 | ❌ 노트 없음 |
| **압축 키워드 자동 추출 규약** | §7.2, §8.2 — 컴팩션 시 "질의 트리거용 키워드" 자동 추출 후 L2/L3 보존 | 🟡 컴팩션_생존_전략 기본만 있음 |

#### 🟠 Priority 2 — 에이전트 팀 실현 인프라

| 필요 항목 | 로드맵 근거 | 현재 상태 |
|---|---|---|
| **Mastermind 오케스트레이터 구현 규약** | §5, §6 — .claude/agents/ 실제 에이전트 정의, /goal+/loop 통합, 동적 팀 빌드 | 🟡 Manifesto(원칙)만, 구현 규약 없음 |
| **에이전트 간 BLK-only 통신 규약** | §7.1 "주방 작업대 원칙" — 에이전트 간 파일 통째 전달 금지, BLK 좌표+API 명세만 교환 | ❌ 노트 없음 |
| **Prototype ↔ 적대적 검증자 Cross-talk 설계** | §6.2 — CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAM=1, 격리 없는 대화 채널 | ❌ 노트 없음 |
| **강제 컴팩션 트리거 Hook** | §7.2 — /loop 중 토큰 임계값 도달 시 자동 /compact 실행 훅 | ❌ 구현 없음 |

#### 🟡 Priority 3 — 위키 신경망 완성

| 필요 항목 | 로드맵 근거 | 현재 상태 |
|---|---|---|
| **Track B: 위키 벡터 DB (sqlite-vec)** | §2.2 — obsidian 전체를 벡터 임베딩, 온디맨드 시맨틱 질의 실현 | 🟡 Roadmap_NervousSystemEvolution 설계만, 실체 없음 |
| **웹 링크 지식 정제 자동화 (Hermes)** | §2.2 — 웹링크 → 원자 단위 정제 → 위키 통합 자동화 | 🟡 Try_HermesKnowledgeScout 타당성 검토만, 구현 없음 |
| **schema/INDEX.md (기계 가독 행성 인덱스)** | §2.2, Roadmap_NervousSystemEvolution §6.1 — Track B 벡터 인덱스의 메타 골격 | ❌ 노트 없음 |

---

## 경계 밖 (out-of-scope)

- 특정 제품의 *설치 튜토리얼*(요금·API키 발급 절차 등 휘발성 how-to)
- 도구 *활용 레시피*(NotebookLM 챗봇 만들기 등) — 통제·워크플로우 축과 무관
- 도구 단순 비교(n8n vs X) — 인사이트가 이미 통제 철학에 내재된 경우

---

## 판정 규칙

후보 지식은 in-scope 관심사에 부합하고 [[위키_저장_5대필터]] 중 ≥1을 충족해야 위키 승격 자격. 경계 밖이면 ⛔보류(폐기·별도 베이스·재distill). 상세 판례는 `scout_lexicon.md`.

**갭 분석 활용**: 위 "필요한 것" 표의 항목을 채우는 지식이 들어오면 Priority 1부터 우선 채용.

## 갱신 규약

관심사가 확장되면(예: 새 프로젝트 행성 추가) 본 mandate의 in-scope에 1줄 추가. 입국심사가 반복적으로 같은 주제를 보류하면 out-of-scope에 명문화.
갭 분석의 항목이 obsidian에 생성되면 ✅로 전환하고 날짜 기록.
