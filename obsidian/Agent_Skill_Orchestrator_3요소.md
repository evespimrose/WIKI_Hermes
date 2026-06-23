---
tags: [llm-wiki, 하네스, 에이전트]
date_created: 2026-06-04
last_modified: 2026-06-17
---

# Agent · Skill · Orchestrator — 하네스 3요소

[[하네스_엔지니어링]]을 구성하는 3대 요소. 연사는 *이 셋이면 충분*하다고 본다. 본 볼트의 기존 에이전트 체계가 이 3요소에 1:1 매핑된다.

## 3요소 정의

| 요소 | 역할 | 구성 | 본 볼트 대응 |
|---|---|---|---|
| **Agent** | 일을 수행하는 주체. *코드 아닌 자연어 문서* | 역할·원칙·I/O 프로토콜·협업·에러대응 | [[3Tier_에이전트_스튜디오]] 에이전트들 |
| **Skill** | 반복작업을 *단일 책임*으로 분리한 도구/지식 | name + description, 프로세스·지식·체크리스트 | compile-wiki·[[move-to-raw]]·[[Try_Skill_타당성_검증]] |
| **Orchestrator** | PM. 워크플로 감시·조율. *마이크로매니징 금지* | 항상 1개 생성, "잘 진행되는가"만 체크 | Mastermind([[Mastermind_Architecture_Manifesto]]) |

## 스킬 = 단일 책임의 조합

"작은 스킬을 조합해 더 큰 시스템을 만든다"는 원칙은 [[LLM_통제_철학_6대원칙]] 원칙 5(단일 책임)·원칙 4(모듈 독립)와 동일. 본 볼트가 compile-wiki/move-to-raw를 *각각 하나의 책임*으로 쪼갠 것이 그 실천.

## Skill의 두 유형 — Capability vs Preference

스킬은 *왜 존재하는가*로 두 종류로 갈린다. 이 구분이 스킬의 *생애주기*를 결정한다.

| 유형 | 목적 | 예 | 생애 |
|---|---|---|---|
| **Capability Skill** | 에이전트가 네이티브로 *못 하는* 능력 보강 | .docx 파싱, PDF 처리 | 모델이 능력을 흡수하면 *은퇴* |
| **Preference Skill** | 팀 고유 *워크플로를 일관 준수* | compile-wiki·[[move-to-raw]]·distill-to-raw | 팀 규약인 한 *영속* |

본 볼트의 스킬 대부분은 Preference 계열 — "결정론적 워크플로 강제"가 목적이므로 모델이 발전해도 폐기 대상이 아니다. 반면 Capability 계열은 모델 능력 향상과 함께 가치를 잃는다(은퇴 원칙은 [[SKILL_md_작성원칙]] §5). 두 유형을 혼동해 Preference Skill에 은퇴를 적용하면 워크플로가 무너진다.

## 스킬을 어떻게 쓰는가

Skill 요소의 *작성 방식·로딩 구조·은퇴 시점*은 [[SKILL_md_작성원칙]]이 따로 다룬다 — 설명=트리거, 점진적 로딩(frontmatter 상시 / 본문 트리거 시 / references 온디맨드), 결과 지향 지시, 부정 케이스 명시 등. 본 노트가 Skill이 *무엇인가*라면, 그 노트는 Skill을 *어떻게 쓰는가*다.

## 오케스트레이터 = 마이크로매니징 금지

오케스트레이터는 세부를 들여다보지 않고 *흐름*만 본다 — [[Producer_QualitySentinel_Reporter_게이트]]에서 각 역할이 "절대 하지 않는 것"을 명시하는 정신, 그리고 [[Mastermind_Architecture_Manifesto]]의 "인간(과 최상위 오케스트레이터)은 Confirm/Deny만"과 같다.

## 생성 위치

메타 하네스가 이 3요소를 클로드 코드 `.claude/` 하위 `agents/`·`skills/`에 자동 생성한다. 에이전트 간 대화(에이전트 팀)는 실험 기능(`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAM=1`) — 본 볼트의 "세션 send"([[AI_네이티브_멀티에이전트_운영]])와 같은 계열.

## 출처

- raw/하네스_엔지니어링_심화__yt_iqoPgoYBVaM.md (2026-06-04 유입) — 3대 핵심 구성요소
- raw/agent_skills_입국심사.md (2026-06-17 편입) — Atom 1 Capability vs Preference 이분법. 작성·생애주기 원칙(Atom 2~6)은 [[SKILL_md_작성원칙]]으로 분리 편입
