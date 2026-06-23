---
tags: [llm-wiki, 토큰, 캐시, 하네스]
date_created: 2026-06-22
last_modified: 2026-06-22
---

# CacheAligner — 프리픽스 KV캐시 안정화 (HR5)

토큰 비용의 *캐시 축*. 프로바이더 KV 캐시는 프롬프트의 **불변 프리픽스가 byte-equal일 때만** 재사용된다(예: Anthropic 최소 1,024토큰 일치 시 히트). "변하지 않는 것을 앞에, 변하는 것을 뒤에" 배치하면 같은 내용도 캐시 히트로 대폭 싸진다. [[LLM_통제_철학_6대원칙]] 원칙1(토큰 1급 자원)의 *캐시 측* 구현이며, 출력 축 [[출력_표현_압축]]·입력 접근 축 [[Sonar_Protocol]]과 **직교·가산**하는 세 번째 토큰 축이다.

## 핵심 위험 — prefix churn

SessionStart 훅이 매 세션 주입하는 컨텍스트의 *선두(불변 구역)* 가 한 글자라도 흔들리면(churn) 캐시가 깨져, 같은 내용을 매 세션 full-price로 재처리한다. 캐시 절감은 전적으로 "프리픽스를 흔들지 않는 규율"에 달려 있다.

## 실증 구현 — HR5 규율 (cache-aligner 스킬)

이 원리는 본 볼트([[LLM_워크플로우_생태계]])가 정의한 워크플로우의 실증 프로젝트 `claude-personal-integrated-workflow`에 **`cache-aligner` 스킬(HR5)** 로 구현되어 있다. `.claude/hooks/session-start.sh`·`post-compact.sh`의 컨텍스트 주입을 네 불변식으로 강제한다:

1. **INVARIANT BLOCK 우선** — 주입 프리픽스 선두는 매 세션 동일: `[SESSION-START] 헤더 → CORE_RULES → CLAUDE.md`. 이 구역에 `.riper-state`·cxt·위반이력 등 *세션마다 달라지는 내용*을 끼우지 않는다.
2. **VARIABLE BLOCK은 항상 뒤** — `.riper-state` → 플랜 → cxt → 위반이력은 전부 불변 구역 *뒤*에 온다. 앞으로 옮기면 프리픽스가 churn한다.
3. **두 진입점 byte-equal** — `session-start.sh`와 `post-compact.sh`의 CORE_RULES RULE-1~5는 글자 단위로 동일(RULE-6만 진입점별 상이: 최초 `/memory:save`, 컴팩션 후 `/memory:recall`). 한쪽을 고치면 반드시 다른 쪽도 동일하게.
4. **cxt 안정 정렬** — mtime(정수 초 양자화) + 파일명 2차로 정렬. 내용 무변경 `touch`의 sub-second 흔들림만으로 주입 순서가 뒤집히지 않게 한다.

## 결정론 검증

규율은 선언이 아니라 *검사*로 강제한다 — 동일 입력 2회 실행 → 불변 프리픽스 diff 0이면 `PREFIX_STABLE`, 아니면 `PREFIX_CHURN`. 두 진입점의 RULE-1~5 byte-equal도 별도 회귀 검사한다. 이는 [[결정론_검증_게이트]]의 "같은 입력 → 같은 출력" 불변식을 *프롬프트 프리픽스* 레벨에 적용한 사례(hot-zone freeze와 동형).

## 경계

헌법급 텍스트(CORE_RULES·CLAUDE.md)를 "캐시 때문에" lossy 압축하지 않는다 — 프리픽스 안정화는 *동결*이지 *압축*이 아니다([[압축_안전경계]]). 캐시 정책·할인율은 프로바이더별로 다르므로 수치는 참고치로 둔다.

## 출처

- raw/headroom_입국심사_2026-06-14.md (2026-06-22 편입) — Atom 5 CacheAligner(프리픽스 안정화 → KV 캐시 히트, hot-zone freeze 연동)
- 실증 구현: `claude-personal-integrated-workflow` — `.claude/skills/cache-aligner/SKILL.md`(HR5 규율) · `.claude/hooks/{session-start,post-compact}.sh`
- 상류: github.com/chopratejas/headroom
