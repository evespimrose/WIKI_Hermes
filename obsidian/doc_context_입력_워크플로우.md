---
tags: [llm-wiki, llm-워크플로우, 입력]
date_created: 2026-05-22
last_modified: 2026-06-14
---

# doc-context 입력 워크플로우

[[LLM_워크플로우_생태계]]의 4대 서브시스템 중 *입력 측 토큰 절감*을 담당하는 모듈. 사용자의 긴 한국어 지시문을 AI 대화 히스토리에 누적시키지 않고, 외부 파일(`cxt[N].md`)에 저장한 뒤 *파일 경로만 매 턴 전송*하는 트릭이다.

## 메커니즘

```
사용자 → AI에게 긴 지시문 직접 입력
       → 대화 히스토리에 영구 저장
       → 매 턴 재전송 → 누적 비용 폭발

vs.

사용자 → 지시문을 cxt 파일에 저장
       → /doc-context docs/contextmd/cxt[N].md
       → 사용자 메시지는 "경로"만 남음 → 매 턴 토큰 절감
       → AI는 매번 파일을 읽지만 컨텍스트 내 참조 캐싱
```

## 전체 파이프라인

```
사용자의 날 것 한국어 요구사항
        │
        ▼
   [외부 AI — Trae + context-sharer skill]
   1. 원문 한국어 → 구조화 영어 Markdown 변환
   2. BLK 태그 추정 (dictionary § 3 참조 → [[BLK_좌표_시스템]])
   3. docs/contextmd/cxt[N].md 저장
   4. validate-cxt.ps1 실행 (BLK 검증)
   5. "/doc-context docs\contextmd\cxt[N].md" 클립보드 복사
        │ Ctrl+V
        ▼
   Claude Code: /doc-context docs\contextmd\cxt[N].md
        │
        ▼
   [Claude — doc-context skill]
   1. Read(cxt[N].md)
   2. 2행 BLK 태그 파싱
   3. dictionary § 1에서 BLK → 관련 파일 경로 확보
   4. 파일 내용을 직접 지시로 해석 → 즉시 실행
```

외부 AI의 역할 분담 자체는 [[External_AI_역할분리]]를 본다. cxt 파일의 구체 포맷은 [[cxt_파일_포맷_컨벤션]]을 본다.

## 환각 차단 규칙

doc-context skill은 *재확인 요청을 절대 금지*한다.

```
❌ "이 방향으로 진행하면 될까요?"
❌ "내용을 요약하면..."
❌ "이해했습니다. 확인해 주세요."

✅ cxt 파일 = 직접 지시. 읽는 즉시 작업 착수.
```

이유: 재확인을 허용하면 매번 사용자가 "네 진행하세요"를 입력해야 하고, 이는 doc-context 도입 목적(토큰 절감)을 *무효화*한다. 이 강제는 [[LLM_통제_철학_6대원칙]] 5번(Single Responsibility)의 doc-context skill 버전이다.

## BLK 인덱싱과의 결합

cxt 파일이 [[BLK_좌표_시스템]]을 활용하면 추가 자동화가 일어난다.

```
Line 1: # [제목]
Line 2: <!-- BLK: BLK-XXX -->   ← 좌표 태그
Line 3+: 내용
```

훅 `dict-blk-announce.sh`가 cxt 읽기 시:
1. BLK 태그 파싱
2. `manage/dictionary.md § 1`에서 해당 BLK 행 조회
3. 관련 파일 경로 목록을 컨텍스트에 자동 주입

→ "어떤 파일이 관련 있는지"를 AI에게 미리 알려줘서 탐색 비용([[Sonar_Protocol]] 위반 압력) 절감.

## 의미적 캐싱

매 턴 cxt 파일을 다시 읽지만, AI 컨텍스트 내부에서 *동일 파일 경로로의 두 번째 Read는 캐싱*된다. 결과적으로 *한 번 로드되면 매 턴 비용은 거의 0*. 이는 [[4계층_메모리_아키텍처]]의 L1(세션 컨텍스트)에 cxt 본문이 한 번만 들어간다는 의미.

## SessionStart 자동 주입과의 결합

`session-start.sh` 훅이 매 세션 시작 시 *최신 cxt 2개*를 자동으로 컨텍스트에 주입한다 (→ [[컴팩션_생존_전략]]). 사용자는 새 세션에서도 "방금 이야기하던 일"의 맥락을 다시 설명할 필요가 없다.

## 관련 노트

- 파일 포맷: [[cxt_파일_포맷_컨벤션]]
- 외부 AI의 역할: [[External_AI_역할분리]]
- 인덱싱 결합: [[Dictionary_md_좌표_시스템]] / [[BLK_좌표_시스템]]
- 세션 연속성: [[컴팩션_생존_전략]] / [[4계층_메모리_아키텍처]]

## 출처

- raw/Workflow-Design-Philosophy.md (2026-05-22 유입) — §6 doc-context 토큰 절감 트릭
- raw/ecosystem-atomic-analysis.md (2026-05-22 유입) — §2-A 워크플로 흐름, §2-B/2-C 원자 목록
