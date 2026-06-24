---
tags: [llm-wiki, llm-워크플로우, 검색, 인덱스]
date_created: 2026-05-22
last_modified: 2026-06-16
---

# Dictionary.md 좌표 시스템

`manage/dictionary.md`의 8개 섹션(§0~§7)으로 구성된 *프로젝트 전체의 인덱스 지도*. [[4계층_메모리_아키텍처]] L4 계층의 본체이며, [[Sonar_Protocol]]의 RULE 2·3이 가리키는 대상이다 — 단 현행 정본은 codegraph-first이므로, dictionary는 codegraph로 미해결 시 여는 **보완(fallback) 인덱스**로 읽는다.

## 8개 섹션 구조

| 섹션 | 역할 | 내용 |
|---|---|---|
| § 0 | Sonar Protocol | RULE 1~3 + 위반 탐지 규칙 ([[Sonar_Protocol]]) |
| § 1 | 파일 인덱스 | `BLK 태그 \| 파일 경로 \| 의존성` 매핑 |
| § 2 | 클래스 인덱스 | 클래스명 → 파일 경로 |
| § 3 | 키워드 인덱스 | 기능 키워드(전투/UI 등) → BLK 코드 |
| § 4 | BLK 의존성 맵 | BLK 간 의존 관계 |
| § 5 | 검색 워크플로 | 탐색 시 순서 (§ 1 → § 3 → ...) |
| § 6 | 동기화 규칙 | dictionary 갱신 트리거 조건 |
| § 7 | Context Index | cxt 파일 번호 → BLK 매핑 (→ [[cxt_파일_포맷_컨벤션]]) |

위 8섹션은 *PRD 단계의 청사진*이며, 실제 프로젝트에서는 가지치기되어 더 단순한 형태로 운영될 수 있다. 예컨대 [[RX_1_manage_DB_스키마]]는 § 0 / § 0-1 / § 1 / § 2 / § 3 네 개로 압축한 RX_1 실 구현을 보여준다.

## § 1 — 파일 인덱스 (dictionary 내 PRIMARY 섹션)

```
| BLK Tag   | File Path                      | Dependencies |
|-----------|--------------------------------|--------------|
| BLK-001   | Assets/Core/PlayerUI.cs        | BLK-010      |
| BLK-010   | Assets/Core/CombatSystem.cs    | BLK-025      |
```

50줄(~400토큰)로 *전체 프로젝트 구조 전체를 압축*한다. AI는 dictionary 한 번 읽고 BLK 좌표로 직접 점프한다.

## 왜 50줄로 충분한가

[[BLK_좌표_시스템]]에서 BLK 코드 한 줄은 *한 파일 또는 한 기능 단위 전체*를 가리킨다. 8,000+ 라인 프로젝트의 1만 개 식별자가 아니라 ~50개 BLK로 압축되기 때문에 dictionary 자체가 컨텍스트 윈도우 안에 가뿐히 들어간다. 이 압축비가 [[Sonar_Protocol]]의 정량 효과(75~97% 절감)의 근거다.

## § 7 Context Index — doc-context와의 결합

cxt 파일 번호와 BLK 코드를 양방향으로 매핑한다. [[doc_context_입력_워크플로우]]가 cxt 파일을 로드할 때 `dict-blk-announce.sh` 훅이 § 7을 참조해 *관련 파일 목록을 컨텍스트에 자동 주입*한다.

## 동기화 메커니즘 (§ 6)

dictionary는 *코드가 바뀌면 인덱스가 깨진다*는 위험을 안고 있다. 세 종류의 훅이 이 동기화를 자동 알림화한다.

| 훅 | 트리거 | 동작 |
|---|---|---|
| `dict-sync-check.sh` | PostToolUse:Write\|Edit (.cs 등) | "manage/dictionary.md § 1 갱신 여부 확인" 알림 |
| `dict-blk-announce.sh` | PostToolUse:Read (cxtN.md) | BLK 파싱 → § 1 grep → 관련 파일 목록 주입 |
| `post-commit-dict-sync.sh` | git post-commit | 동기화 필요 여부 알림 |

훅은 *자동 수정이 아니라 자동 알림*임을 주의한다. 인덱스 갱신은 사람이 결정해야 하는 영역이라 자동화의 위험이 더 크다고 판단한 결과다.

## "Self-Healing Wiki" 야망

[[Mastermind_Architecture_Manifesto]]는 더 나아가 RIPER의 [[RIPER_5단계_상태머신]] Review 단계에서 dictionary 갱신 초안을 *자동 제안*하는 자가 치유 루프를 그린다. 현재 구현은 알림 단계이고, 자동 초안은 차세대 진화 방향이다.

## 단일 파일 유지 결정

dictionary는 한때 다중 파일 분할 후보였으나, 현재 규모에서는 *50줄 단일 파일 + 검색 워크플로 § 5*가 충분하다는 결론. dictionary 500행 초과 시점에 레이어 계층형 분할(Phase 6-B) 재검토 예정. 이는 [[LLM_통제_철학_6대원칙]]의 "Simplicity First" 적용 사례.

## 관련 노트

- 사용 규약: [[Sonar_Protocol]]
- 좌표 의미론: [[BLK_좌표_시스템]]
- manage 폴더의 다른 4개 파일: [[manage_폴더_역할분리]]
- doc-context와의 결합: [[doc_context_입력_워크플로우]] / [[cxt_파일_포맷_컨벤션]]
- RIPER 통합: [[RULE7_PRD_Spatial_Mapping]]
- 실 프로젝트 적용 사례: [[RX_1_manage_DB_스키마]]

## 출처

- raw/dictionary-first-grep-workflow.md (2026-05-22 유입) — §2 구현 현황, §3 manage 역할
- raw/ecosystem-atomic-analysis.md (2026-05-22 유입) — §3-B/3-C/3-E
- raw/Workflow-Design-Philosophy.md (2026-05-22 유입) — §8 first-grep dictionary indexing
