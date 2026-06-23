---
tags: [llm-wiki, 워크플로우, 버전, 역사]
date_created: 2026-05-28
last_modified: 2026-06-14
---

# Workflow Ecosystem 버전 계보

Universal Workflow Ecosystem(Handover.md 배포 시스템)의 v3.0~v3.5 변경 누적 기록. 각 버전이 어떤 한계를 해결하며 등장했는지의 *세대 단위* 진화 추적.

## 버전 요약표

| 버전 | 적용일 | 핵심 변화 | 해결한 한계 |
|---|---|---|---|
| v3.0 | (초기) | 위저드 방식 도입 (단일 Q&A 후 분기 설치) | 설치 모호성 |
| v3.1 | (이후) | 자급 방식 — 빈 폴더 + Handover.md 단독 설치 | 의존성 부담 |
| v3.2 | (이후) | Reading Map 추가 — Handover.md 자체 토큰 문제 해결 | 대형 문서 비용 |
| v3.3 | 2026-05 | C1/C2 분리 + Update 모드 + RULE-7 PRD Spatial Mapping | 단일 설치 불가, 덮어쓰기 |
| v3.4 | 2026-05-27 | codegraph L1 강제 + shadow hook 제거 + CLAUDE.md 압축 | 토큰 +827/턴, 보장률 한계 |
| v3.5 | 2026-05-28 | RIPER 7개 커맨드 `## Codebase Navigation` 명시 | RIPER 단계 codegraph 암묵적 허용 |

## v3.3 — 모듈 분리와 좌표 강제

### C1/C2 분리

기존 워크플로 C(RIPER + 3-tier agents)가 단일 단위였던 것을 분리:

| 코드 | 내용 | 의존 |
|---|---|---|
| C1 | RIPER ([[RIPER_5단계_상태머신]]) | 독립 |
| C2 | 3-tier studio ([[3Tier_에이전트_스튜디오]]) | C1 권장, 독립 가능 |

[[LLM_통제_철학_6대원칙]] 원칙 4(모듈 독립 설치)의 가장 강한 사례.

### Update 모드 도입

`HANDOVER-MANAGED-START/END` 마커로 CLAUDE.md의 관리 영역만 교체하고 사용자 커스터마이징을 보존. `.riper-state`가 MODE≠NONE이면 덮어쓰기 차단 — 진행 중 세션 보호.

### RULE-7 PRD Spatial Mapping

PLAN 단계의 모든 Action Item에 BLK 좌표 + 파일 경로 + 라인 범위 의무화. [[RULE7_PRD_Spatial_Mapping]]이 이 규칙의 단독 노트.

Plan Scope Lock 7개 필드:
```
Symbol / CodeGraph / File / Scope / BLK / Action / Success criterion
```

### Reading Map

Handover.md가 2,000줄+로 비대해진 문제를 *부분 읽기 명세*로 해결. 설치 조합별 Read 호출 범위를 상단 테이블로 명시 — Phase 0b 이후 최소 읽기 패턴.

## v3.4 — codegraph 강제와 토큰 최적화

### 추가된 hook 3종

[[L1_Hard_Gate_훅체계]]의 핵심 구성:

| Hook | 트리거 | 역할 |
|---|---|---|
| `codegraph-gate.sh` | PreToolUse:Read\|Glob | tool-history 검증, codegraph 미사용 시 차단 |
| `cave-man-guard-powershell.sh` | PreToolUse:PowerShell | PS 우회 차단 (이전엔 Bash만) |
| `tool-history-recorder.sh` | PostToolUse 전체 | 도구 호출 이력 (L1 검증 기반) |

### 신규 디렉토리

```
.claude/state/
  tool-history.log
  violation-count.log
```

### 제거된 shadow hook 3종 + 이벤트 2종

```
hooks/auto-route-reminder.sh   (L2)
hooks/audit-footer.sh          (L4)
hooks/meta-reminder.sh         (L5 — context-sharer로 외부 이전)
rules/cave-man-protocol.md     (CLAUDE.md에 통합)

settings.json:
  - UserPromptSubmit 이벤트 전체
  - Stop 이벤트 전체
```

자세한 절충 배경은 [[L1_L5_다층방어선_역사]].

### CLAUDE.md 압축

| 지표 | v3.3 | v3.4 |
|---|---|---|
| 라인 수 | ~250 | 106 |
| 세션 시작 주입 | ~2,140 토큰 | ~900 토큰 |
| 규칙 파일 수 | 11 | 5 |

### cxt 3행 CAVE-MAN-REMINDER 의무

trae context-sharer가 cxt 파일 생성 시 3행에 자동 임베드:
```markdown
# [제목]
<!-- BLK: BLK-XXX -->
<!-- CAVE-MAN-REMINDER: codegraph 우선 ... -->
```

L5 책임의 외부 이전 — [[External_AI_역할분리]]의 단일 책임 원칙 안.

### 정량 효과

| 지표 | Before(v3.3) | After(v3.4) | 변화 |
|---|---|---|---|
| 턴당 고정 토큰 | +827 | +310 | -62% |
| Sonar 보장률 | ~80% (텍스트) | 94% (L1 Hook) | +14%p |
| 정책 파일 수 | 11 | 5 | -55% |
| PowerShell 차단 | ❌ | ✅ | 신규 |
| 소스 Read 차단 | ❌ | ✅ | 신규 |

## v3.5 — RIPER codegraph-first 명시

### 문제 인식

L1 Hook이 Bash/PowerShell/소스 Read는 차단했지만, RIPER 커맨드 본문에는 "금지 조항"만 있고 *올바른 탐색 순서*는 부재였다. RESEARCH/PLAN 단계에서 codegraph 미사용 후 Glob/Grep 폴백이 *암묵적으로 허용*되는 모호성.

### 추가: 7개 커맨드 `## Codebase Navigation` 섹션

| 커맨드 | 추가 내용 |
|---|---|
| `research.md` | context/search → callers/impact → node/explore → 보완 Read/Grep |
| `innovate.md` | context/search → explore + 기존 패턴 참조 |
| `plan.md` | context → impact/callers → node(라인) → Read(offset+limit) |
| `execute.md` | codegraph_node 우선 + 전체 파일 Read 금지(1000자+ = 실패) |
| `review.md` | impact(파급) + callers(회귀) 의무 |
| `strict.md` | "Sonar Protocol DEADLY active in all modes" + nav 섹션 |
| `workflow.md` | 전 단계 공통 nav 섹션 (코드블록) |

### 변경 없음

- L1 Hook 구성 (v3.4와 동일)
- settings.json
- CLAUDE.md
- session-start.sh

### 효과

| 지표 | v3.4 | v3.5 |
|---|---|---|
| RIPER codegraph 명시 | ❌ 금지 조항만 | ✅ 순서 + 허용 도구 |
| 탐색 단계 토큰 절감 | L1 hook 의존 | 커맨드 레벨 확장: -80~90% |
| 모호성 | "금지 외 모든 것 가능" | "명시된 순서 외 차단" |

L1 hook이 *도구 단위*에서 강제하고, v3.5는 *커맨드 단위*에서 강제. 두 레이어가 직교 보완.

### Handover.md 갱신

- VERSION: 3.4 → 3.5
- 총 줄 수: 2,016 → 2,121
- Phase 3 임베디드 바디 7개 모두 Codebase Navigation 포함
- 부록 F (v3.5 마이그레이션 가이드) 신설

### v3.5 후속 패치 — try 스킬 이중 방어 (버전 유지)

v3.5가 RIPER *커맨드*에 codegraph-first를 명시했지만, [[Try_Skill_타당성_검증]] 스킬은 여전히 탐색 단계에서 탈옥했다. 두 층의 공백이 원인이었다 — 스킬 텍스트(soft)에 codegraph 언급 부재 + `codegraph-gate.sh` 매처에서 Grep 누락(hard). 버전을 올리지 않는 후속 패치로 양쪽을 동시에 막았다:

- **Soft**: try SKILL.md에 `Stage 0 EXPLORE (codegraph-first)` 신설 ([[구체지시_우선_원칙]] 적용)
- **Hard**: 매처 `Read|Glob` → `Read|Glob|Grep`, 소스 필터 걸린 Grep만 차단 ([[외과적_게이팅]])

이 패치가 [[이중방어_Defense_in_Depth]]의 정식 사례다. 변경 파일은 `try/SKILL.md`, `codegraph-gate.sh`, `settings.json`, `Handover.md`(전파), `CHANGELOG.md`(패치노트). RIPER 커맨드 명시(v3.5)가 *커맨드 단위*였다면, 본 패치는 동일 원칙을 *스킬 단위*로 확장한 것이다.

## 진화 패턴

| 세대 | 해결 방식 | 비용 |
|---|---|---|
| v3.0~v3.2 | UX 개선 (위저드, 자급, Reading Map) | 사용성↑ |
| v3.3 | 구조 분리 + 좌표 강제 | 유연성↑ |
| v3.4 | 텍스트 → Hook 전환 + 절충 | 토큰 절감 + 보장률 절충 |
| v3.5 | 커맨드 레벨 명시 | 토큰 추가 절감 + 모호성 제거 |

각 세대는 직전 세대의 *남은 모호성*을 해소한다 — 한 번에 끝나지 않는 점진 진화. 다음 v3.6 후보는 [[Mastermind_Architecture_Manifesto]] 진화 단계가 가리킨다.

## 관련 노트

- 진화 단계 요약: [[Workflow_진화_3단계]]
- v3.4 hook 시스템: [[L1_Hard_Gate_훅체계]]
- v3.4 절충 결정: [[L1_L5_다층방어선_역사]]
- v3.3 좌표 규칙: [[RULE7_PRD_Spatial_Mapping]]
- v3.5 codegraph: [[Codegraph_MCP_통합]]
- RIPER 본체: [[RIPER_5단계_상태머신]]

## 출처

- raw/CHANGELOG.md (2026-05-28 유입) — v3.0~v3.5 누적 변경 이력 원본
- raw/workflow_policy_change_notification.md (2026-05-28 유입) — v3.4 정책 변경 상세 배경
- raw/wiki-raw_try-codegraph-jailbreak-fix.md (2026-05-29 유입) — v3.5 후속 패치 (try 이중 방어)
