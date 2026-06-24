---
tags: [llm-wiki, llm-워크플로우, 입력, 포맷]
date_created: 2026-05-22
last_modified: 2026-05-22
---

# cxt 파일 포맷 컨벤션

[[doc_context_입력_워크플로우]]에서 사용하는 컨텍스트 전달 파일의 표준 포맷. 외부 AI가 작성하고 Claude Code가 소비하는 *2자 인터페이스*다.

## 표준 포맷

```markdown
# [작업 제목]
<!-- BLK: BLK-XXX -->

## Task
[구조화된 영어 지시사항]

> All work must deadly and strictly follow the rules defined in SKILL.md and CLAUDE.md.
```

## 줄별 의미

| 줄 | 내용 | 강제성 |
|---|---|---|
| 1행 | 제목 (한국어 또는 영어) | 필수 |
| 2행 | BLK 태그 — `<!-- BLK: ... -->` | 필수 |
| 본문 | 구조화 영어 지시 | 필수 |
| 마지막 행 | compliance footer | 필수 |

## BLK 태그 어휘

| 형식 | 사용 시점 | 예 |
|---|---|---|
| `BLK-XXX` | 단일 코드 대상 | `BLK: BLK-042` |
| `BLK-001, BLK-002` | 복수 코드 대상 | (콤마 구분) |
| `인프라` | 코드 아닌 인프라 작업 | `BLK: 인프라` |

BLK 코드 의미론은 [[BLK_좌표_시스템]]에서, 좌표 인덱스 본체는 [[Dictionary_md_좌표_시스템]]에서 다룬다.

## 파일명 규칙

- 형식: `cxt[N].md` (`cxt123.md`, `cxt124.md` ...)
- 위치: `docs/contextmd/`
- 번호: 순차 증가, 절대 재사용 금지
- 갱신 주기: 새 요구사항마다 신규 파일 (덮어쓰기 금지)

## 검증 훅 (validate-cxt)

| 파일 | 역할 |
|---|---|
| `.trae/hooks/validate-cxt.ps1` | Windows용 BLK 태그 검증 |
| `.trae/hooks/validate-cxt.sh` | Linux/macOS용 동일 |
| `.trae/rules/validate-cxt.md` | 검증 규칙 명세 (4개 규칙) |

검증 실패 시(2행 BLK 태그 없음 등) exit 1로 차단한다. 이는 [[LLM_통제_철학_6대원칙]]의 "Hooks > Prompts"의 외부 AI 측 구현체다 — 외부 AI가 BLK 태그를 잊더라도 *훅이 결정론적으로 거부*한다.

## 왜 영어로 변환하는가

원문 한국어를 그대로 cxt에 넣으면 두 문제가 생긴다.

1. LLM의 영어 추론 성능이 한국어보다 일반적으로 안정적
2. 사용자 입력의 *비형식 산문* 톤이 그대로 들어오면 지시 해석의 모호성이 증가

외부 AI(Trae 등)는 *공증 번역사* 역할을 수행해 한국어 산문 → 구조화 영어로 변환한다. 이 분리는 [[External_AI_역할분리]]를 본다.

## compliance footer의 의도

```
> All work must deadly and strictly follow the rules defined in SKILL.md and CLAUDE.md.
```

마지막 행에 *모든 cxt가 반드시 갖는* 정형 문장을 두는 이유: 파일 내용이 길어도 마지막 줄이 항상 같은 명령으로 끝나면 Claude가 *지시 해석 경계*를 명확히 인지한다. 또한 "deadly"·"strictly" 같은 강한 어휘가 [[LLM_컨텍스트_5대_문제]] 2번(환각)에 대한 *언어 차원의 보조 가드*가 된다.

## 관련 노트

- 사용 워크플로: [[doc_context_입력_워크플로우]]
- 인덱스 결합: [[BLK_좌표_시스템]] / [[Dictionary_md_좌표_시스템]]
- 외부 AI 역할: [[External_AI_역할분리]]

## 출처

- raw/ecosystem-atomic-analysis.md (2026-05-22 유입) — §2-B cxt 파일 포맷 원자
- raw/dictionary-first-grep-workflow.md (2026-05-22 유입) — §2-E cxt 컨벤션
