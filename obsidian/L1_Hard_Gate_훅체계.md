---
tags: [llm-wiki, 훅, 검색, 강제]
date_created: 2026-05-28
last_modified: 2026-06-21
---

# L1 Hard Gate 훅 체계

PreToolUse hook으로 LLM의 탐색 행위를 *물리적으로* 차단하는 시스템. [[Sonar_Protocol]]의 텍스트 규칙이 신뢰될 수 없다는 인식에서 출발한 [[LLM_통제_철학_6대원칙]] 원칙 3(훅 > 프롬프트)의 가장 강력한 구현체.

## 왜 텍스트 규칙으로는 부족한가

CLAUDE.md에 "find 쓰지 마세요"라고 적어도 LLM은 attention drop, 컴팩션 직후, 새 패턴 등에서 위반한다. 위반 분석 결과 *세션당 3회 이상* 반복되는 패턴이라 [[Workflow_진화_3단계]] 2단계 전환의 직접 계기가 되었다.

해결: 규칙을 텍스트가 아니라 **hook으로 강제**한다. hook은 LLM이 무시할 수 없다 — 도구 호출 자체가 차단된다.

## 트리오 구성

3개 hook이 PreToolUse 단계에서 차단한다:

| Hook | 트리거 | 차단 패턴 |
|---|---|---|
| `cave-man-guard.sh` | PreToolUse:Bash | `find`, `grep -r`, `ls -r`, `rg`, `fd`, `cat *.cs` 등 재귀 탐색 |
| `cave-man-guard-powershell.sh` | PreToolUse:PowerShell | `Get-ChildItem -Recurse`, `Select-String -Path *` 등 PS 우회 |
| `codegraph-gate.sh` | PreToolUse:Read\|Glob\|Grep | codegraph_* 최근 미사용 시 소스 파일 Read/Grep 차단 |

PowerShell hook은 v3.4에서 추가됐다. 이전엔 Bash만 차단했기 때문에 사용자가 PS로 우회하면 무방비였다. Grep 매처는 그 뒤 try 스킬 탈옥을 계기로 추가됐다(아래 § Grep 매처 확장).

## codegraph-gate.sh의 검증 로직

소스 Read가 들어왔을 때 다음을 확인한다:

```
1. .claude/state/tool-history.log 읽기
2. 최근 5회 도구 호출 중 codegraph_* 도구 사용 여부 확인
3. 없으면 → permissionDecision: "ask" (사용자 승인 요구)
4. 있으면 → permissionDecision: "allow" (통과)
```

즉 "Read 전에 codegraph로 위치를 확인했는가?"를 묻는다. 사람이 매번 확인하는 것이 아니라 hook이 자동 검증한다. 이 검증의 근거가 되는 도구 이력은 [[tool-history-recorder.sh의 역할]]이 담당한다.

### 실측 동작 확인

```
# codegraph 미사용 후 .cs Read 시도
echo '{"tool_name":"Read","tool_input":{"file_path":"...CellRenderer.cs"}}' \
  | bash codegraph-gate.sh
→ permissionDecision: "ask"   (차단)

# codegraph 사용 후 .cs Read 시도
echo "codegraph_context" > tool-history.log
echo '{"tool_name":"Read","tool_input":{"file_path":"...CellRenderer.cs"}}' \
  | bash codegraph-gate.sh
→ permissionDecision: "allow" (통과)
```

`permissionDecision: "ask"`는 *완전 차단*이 아니라 *사용자 승인 요구*다. 의도된 우회는 가능하지만, 그 우회 자체가 명시적 행위가 되어 위반 통계에 기록된다.

## 화이트리스트 (차단 예외)

코드 탐색이 아닌 *메타 작업*은 차단되지 않는다:

| 카테고리 | 허용 대상 |
|---|---|
| 메타 파일 확장자 | `.json`, `.md`, `.txt`, `.sh`, `.ps1`, `.yml` |
| 인프라 디렉터리 | `.claude/`, `.trae/`, `docs/`, `manage/`, `raw/` |
| 예외 파일 | `CLAUDE.md`, `AGENTS.md`, `dictionary.md` |

소스 코드(`.cs`, `.py`, `.ts` 등)의 직접 Read만 codegraph 선행을 요구한다. 설정 파일과 wiki 문서는 자유롭게 읽을 수 있어야 워크플로우 자체의 디버깅이 가능하다.

Glob의 경우 `**/*.cs` 같은 *코드 검색 패턴*은 `codegraph_files` 권장으로 안내된다 — 차단까지는 아니지만 의식적 선택을 유도한다.

## Grep 매처 확장 (외과적 게이팅)

초기 `codegraph-gate.sh`는 `Read|Glob` 매처로만 등록돼 **Grep 도구가 게이트 밖**이었다. bash `grep -r`은 `cave-man-guard.sh`가 막지만 Claude의 Grep 도구는 아무도 막지 않아, [[Try_Skill_타당성_검증]] 스킬이 Grep으로 20개 스크립트를 자유롭게 훑는 탈옥구가 됐다. 이는 [[이중방어_Defense_in_Depth]]의 매처 합집합 원칙(막을 행위가 가능한 *모든* 도구를 매처에 넣어야 함)이 깨진 사례다.

해결: settings.json 매처를 `Read|Glob` → `Read|Glob|Grep`으로 확장하고, gate에 Grep 분기를 추가했다. 단 Grep을 *전면* 차단하지 않는다 — [[외과적_게이팅]] 원칙에 따라 소스 타입 필터가 걸린 Grep만 차단한다:

```
Grep의 type(cs/py/ts…) 또는 glob(*.cs…)이 소스를 가리킴
  + 직전 이력에 codegraph_* 없음
  → permissionDecision: "ask" (구조적 검색으로 판정)

필터 없는 Grep
  → 통과 (리터럴 텍스트 검색으로 판정, 대체재 없음)
```

전면 차단은 리터럴 검색까지 막아 불필요한 codegraph 호출을 유발(약 +52% 토큰 역효과)하므로 피한다. 차단 메시지에는 *"리터럴 검색이면 type/glob 필터를 빼면 통과"*라는 탈출구를 함께 안내한다.

## tool-history-recorder.sh

PostToolUse에 매처 없이 등록되어 *모든 도구 호출*을 기록한다:

```
.claude/state/
  tool-history.log       ← 최근 100개 호출 (세션마다 초기화)
  violation-count.log    ← Sonar Protocol 위반 누적
```

`tool-history.log`는 codegraph-gate의 검증 근거다. 이게 없으면 gate가 작동 불가. `violation-count.log`는 세션 시작 시 [[Workflow_Ecosystem_버전계보]] v3.4 session-start.sh가 최근 10개를 출력해 사용자에게 패턴을 노출한다.

## 보조 hook (Write/Edit 보호)

L1 트리오는 *탐색*을 차단하고, 다음 hook은 *변경*을 통제한다:

| Hook | 트리거 | 역할 |
|---|---|---|
| `write-approval-reminder.sh` | PreToolUse:Write\|Edit | 소스 수정 직전 사용자 승인 환기 |
| `dict-sync-check.sh` | PostToolUse:Write\|Edit | dictionary § 1 갱신 필요 알림 ([[Dictionary_md_좌표_시스템]] § 6) |
| `gate-check.sh` | PostToolUse:Write\|Edit | 게이트 검증 |

`dict-sync-check.sh`는 자동 수정이 아니라 자동 알림이다 — [[Dictionary_md_좌표_시스템]]의 동기화 메커니즘 절에서 다룬 원칙(인덱스 갱신은 사람 판단 영역)을 따른다.

## 보장률

| 환경 | 보장률 | 근거 |
|---|---|---|
| 텍스트 규칙만 (1단계, [[Workflow_진화_3단계]]) | ~80% | CLAUDE.md 의존, LLM attention drop |
| L1~L5 다층 (2단계) | 99.2% | 5중 방어선, 매 턴 +827 토큰 |
| L1 + L3 + 외부 이전 (3단계) | 94% | 5% 감수 + 토큰 62% 절감 |

94%로의 5%p 회귀는 [[L1_L5_다층방어선_역사]]의 절충 결정이다. 잔여 6% 위반 패턴은 `violation-count.log`로 모니터링되어 hook 패턴 업데이트의 근거가 된다.

## 의존성

- **codegraph MCP 필수**: [[Codegraph_MCP_통합]] 미설치 시 codegraph-gate가 검증 불가 → 보장률 0%로 회귀. Phase 0(codegraph 설치)이 모든 다른 적용 단계의 선행 조건이다.
- **bash 환경**: 모든 hook이 `.sh` 파일. PowerShell만 있는 환경에서는 bash 인터프리터가 필요하다 (Git Bash 등).

## 보장률의 단계별 측정

L1 단독 운용으로도 의미 있는 차단이 일어난다. 단계 추가에 따른 한계 효용은 빠르게 체감한다:

| 활성 계층 | 보장률 |
|---|---|
| L1만 | 70% |
| L1 + L3 reminder | 92% |
| L1 + L3 + L5 매 턴 reminder | 97% |
| L1~L5 전체 | 99.2% |

현 시스템은 *시나리오 X*([[L1_방어선_시나리오X_결정]])에 따라 L1 + L3 + 외부 이전 L5로 94%를 운영한다. 99.2%에서 5%p를 포기하고 토큰 62%를 회수하는 절충.

## 우회 시나리오 (잔존 6%)

100%가 불가능한 본질적 이유:
- 사용자가 명시적으로 우회 요청 ("이번엔 그냥 grep으로 해줘")
- 신규 도구가 hook 매처에서 빠진 경우
- 시스템 버그
- 컴팩션 직후 첫 응답 (컨텍스트 일시적 손실)

이 위반들은 hook 패턴 미커버일 뿐 *철학의 실패*는 아니다.

## 관련 노트

- 차단 대상 규약: [[Sonar_Protocol]]
- 인덱스 의존성: [[Codegraph_MCP_통합]]
- 다층 방어선 역사: [[L1_L5_다층방어선_역사]]
- 최적화 배경: [[Workflow_Ecosystem_버전계보]] v3.4
- 통제 철학 원칙 3: [[LLM_통제_철학_6대원칙]]
- 이중 방어 설계: [[이중방어_Defense_in_Depth]]
- 과잉 차단 회피: [[외과적_게이팅]]
- 우회 벡터·허용 채널 원칙: [[탐색_게이트_우회_벡터]]

## 출처

- raw/workflow_policy_change_notification.md (2026-05-28 유입) — § 1, § 4 L1 Hard Gate 트리오 + 보조 hook
- raw/CHANGELOG.md (2026-05-28 유입) — v3.4 hook 3종 추가
- raw/cave_man_protocol_L1_L5_enforcement.md (2026-05-28 유입) — 화이트리스트, 차단 메커니즘 실측 예시
- raw/cxt145_escape_prevention_optimization.md (2026-05-28 유입) — 보장률 단계별 측정 원본
- raw/wiki-raw_try-codegraph-jailbreak-fix.md (2026-05-29 유입) — Grep 매처 확장, 외과적 게이팅
