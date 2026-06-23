# Try — Harness 플러그인 × 통합 워크플로우 (ready-to-order 에이전트 생성)

> 작성일: 2026-06-04
> 대상 작업: revfactory/harness를 claude-personal-integrated-workflow에 *레이어드 통합*해, "X 만들고 싶다"(의도) → RIPER 준수 에이전트팀+오케스트레이터 자동 생성 → EXECUTE 게이트에서 ready-to-order로 대기시키는 UX의 타당성 검증
> 조사 근거: revfactory/harness README 실조사(2026-06-04) + 볼트 컴파일 지식([[Workflow_Ecosystem_버전계보]], [[RIPER_5단계_상태머신]], [[3Tier_에이전트_스튜디오]])

## 1. 현황 (As-Is)

`claude-personal-integrated-workflow`(Handover v3.5)의 현 구조:

| 요소 | 역할 |
|---|---|
| [[RIPER_5단계_상태머신]] | Research→Innovate→Plan→Execute→Review 실행 상태머신 |
| C1 / C2 | RIPER(C1) + [[3Tier_에이전트_스튜디오]](C2: Producer/QualitySentinel/Reporter) |
| Mastermind | 최상위 오케스트레이션 개념([[Mastermind_Architecture_Manifesto]]) |
| hooks | [[L1_Hard_Gate_훅체계]] (cave-man·codegraph-gate) |
| [[Try_Skill_타당성_검증]] | 착수 전 타당성 |

**핵심 문제**: 에이전트는 *프로젝트마다 수작업 저작*된다. 사용자의 "X 만들고 싶다"는 의도가 곧장 *에이전트팀 구성*으로 이어지는 자동 회로가 없다. 의도 → 팀 스캐폴딩 사이가 수동 공백.

## 2. 제안 구조 (To-Be)

revfactory/harness = **"team-architecture factory"** (자연어 → 에이전트팀+스킬+오케스트레이터).

- 설치: `/plugin marketplace add revfactory/harness` → `/plugin install harness@harness-marketplace` (또는 `cp -r skills/harness ~/.claude/skills/`)
- 생성 6단계: 도메인분석 → 팀설계 → 에이전트생성(`.claude/agents/`) → 스킬생성(`.claude/skills/`) → 통합·오케스트레이션 → 검증
- 6패턴: Pipeline · Fan-out/in · Expert Pool · **Producer-Reviewer** · Supervisor · Hierarchical
- 요건: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` (실험적)
- 자매: Harness 100 (10도메인 100구성 기성품)

**통합 발상 — 공장 ⊂ 헌법**:
```
harness = 팀을 찍어내는 공장 (HOW to build the team)
워크플로우 = 그 팀이 따라야 할 헌법 (HOW the team works = RIPER)
→ 두 워크플로우는 다른 레이어. 경쟁 아님.
```

**ready-to-order 합성 경로**:
```
"X 만들고 싶다"(의도 — harness 의도입력 ∩ doc-context ∩ Mastermind Confirm/Deny)
  → harness가 RIPER-시드된 팀+오케스트레이터 생성
  → 오케스트레이터가 .riper-state = RESEARCH 초기화
  → R→I→P 자동 수행
  → EXECUTE 게이트 정지 = "ready-to-order" (사용자 Confirm 대기)
```

## 3. 장단점 비교

### 3-A. 통합 아키텍처 명확성
✅ **강한 정합**. harness 구성요소가 기존 워크플로우에 1:1 매핑된다:

| harness | 워크플로우 대응 |
|---|---|
| Orchestrator | Mastermind |
| Producer-Reviewer 패턴 | [[Producer_QualitySentinel_Reporter_게이트]] |
| Supervisor / Hierarchical | [[3Tier_에이전트_스튜디오]] |
| 6단계 생성 | (신규 — 현재 수작업인 부분) |

매핑이 깨끗해 개념 충돌이 적다. harness는 *비어 있던 자동 생성 레이어*만 채운다.

### 3-B. 런타임·토큰 영향
⚠ 멀티에이전트 = **+30% 토큰**(KIST 발표 [5] 정량치, 에이전트 간 대화 시 특히). 이 워크플로우는 토큰 강박([[L1_L5_다층방어선_역사]]의 -62% 최적화)이라 *철학적 긴장*. 실험 플래그 동적 로딩 실패 시 격리 에이전트로 떨어져 팀 모드 무력화 리스크.

### 3-C. 현 워크플로우 정합성
⚠ **최대 리스크 — 구체지시 덮어쓰기**. 방금 컴파일한 [[구체지시_우선_원칙]]에 의해: harness가 생성한 `agent.md`(좁은 구체 지시)가 전역 RIPER·cave-man 규칙(넓은 일반)을 **덮어쓴다**. 생성 에이전트는 기본적으로 *일반적*이라 RIPER/cave-man을 모른다. → 생성 시점에 RIPER+cave-man+볼트참조를 **각 에이전트에 재주입**해야 한다(= [[이중방어_Defense_in_Depth]]의 soft 층 강제).

### 3-D. 단기 도입비용
중. 플러그인 설치는 분 단위. 진짜 비용은 ①*재주입 템플릿* 제작(harness가 RIPER-준수 에이전트를 뽑도록 시드 프롬프트 작성), ②1개 프로젝트 파일럿. 기존 수작업 에이전트와의 병행 운영 기간 필요.

### 3-E. 장기 유지보수
⚠ 생성 보일러플레이트가 손튜닝 에이전트와 *드리프트*. 두 워크플로우(harness 6단계 생성 vs RIPER 실행) 개념 병존이 신규 기여자 온보딩 부담. 단 Harness 100 패턴 재사용으로 신규 도메인 진입은 빨라짐.

## 4. 통합 방향·충돌 위험 분석

| 위험 | 내용 | 완화 |
|---|---|---|
| 구체지시 덮어쓰기 | 생성 agent.md가 RIPER 무시 | RIPER/cave-man 재주입([[구체지시_우선_원칙]]) |
| 워크플로우 이중화 | 6단계 생성 ↔ RIPER 실행 혼동 | "생성 레이어  vs 실행 레이어" 명시 분리 |
| 자율완주 | harness가 EXECUTE까지 무인 진행 | EXECUTE 승인 게이트 강제(Mastermind Confirm/Deny) |
| 토큰 역행 | +30% vs -62% 최적화 철학 | [[작업_규모별_워크플로]]로 대형만 멀티에이전트 |
| 실험 플래그 | AGENT_TEAMS 로딩 실패 | 파일럿서 안정성 측정, 폴백 단일에이전트 |

방향 위험의 핵심은 *순환*이 아니라 *덮어쓰기*다 — 생성물이 헌법을 이기지 않도록 재주입이 단일 차단점.

## 5. 종합 평가 및 추천

**🟡 조건부 추천** — harness를 *워크플로우 헌법 아래의 공장*으로 얹는 레이어드 통합. 대체가 아니라 보강.

**4대 조건**:
1. **재주입**: 생성 에이전트에 RIPER+cave-man+볼트참조 시드 (덮어쓰기 차단).
2. **승인 게이트 유지**: EXECUTE 전 정지. harness 자율완주 금지.
3. **토큰 인지 스코핑**: [[작업_규모별_워크플로]] — 소형=단일, 멀티에이전트는 대형만.
4. **1 프로젝트 파일럿**: 신규 Western Salon 모듈 1개로 검증 후 전역화.

**단계별 추천 순서**:
```
1. 입국심사 승인분 [5]하네스·[4]위키 먼저 컴파일 → 개념 토대 확보
2. harness user-scope 설치 + AGENT_TEAMS 플래그 테스트
3. 재주입 시드 템플릿 1개 작성 (RIPER-준수 에이전트 생성용)
4. WS 신규 모듈 1개로 "만들고 싶다 → ready-to-order" 파일럿
5. 토큰·안정성·드리프트 측정 → 전역 채택 여부 결정
```

## 6. 미결 사항 연계

- **입국심사 의존**: 본 통합의 개념 토대인 [5]하네스 엔지니어링·[4]카파시 위키는 현재 raw/ 대기 중(미컴파일). try 우선 처리 방침에 따라, 컴파일 후 본 문서의 [[하네스_엔지니어링]]·[[Agent_Skill_Orchestrator_3요소]] 링크가 활성화될 예정(현재는 미래 노트).
- **Mastermind 4단계**: 본 통합은 [[Mastermind_Architecture_Manifesto]]의 진화 Phase 2(자율 오케스트레이션)의 구체적 실현 경로다.
- **Q1 런타임 배선과 결합**: 생성된 에이전트가 볼트를 헌법으로 참조하려면 Q2의 "런타임 배선" 격차가 선결 또는 병행되어야 한다.
