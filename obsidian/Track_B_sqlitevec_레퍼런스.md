---
tags: [llm-wiki, wiki관리, 벡터DB, 레퍼런스]
date_created: 2026-06-22
last_modified: 2026-06-22
---

# Track B — sqlite-vec 위키 벡터 메모리 레퍼런스

[[Raw_Wiki_Schema_3레이어]]의 Schema 레이어 로드맵 "Track B: 위키 벡터 DB(sqlite-vec)"는 오래 *설계만 있고 실체가 없던*(🟡) 항목이었다. Headroom의 메모리 구현이 바로 그 *작동하는 레퍼런스* — [[LLM_Wiki_지식자산_현황]]이 진단한 "빠진 마지막 1마일"의 벡터 인덱스 축을 채울 검증된 예제다.

## 참조 포인트 (그대로 차용 가능한 설계)

- **백엔드**: `sqlite-vec` — 단일 SQLite 파일에 벡터를 얹는다. torch 불요·경량이라 본 볼트의 MD+hooks 경량 운영 철학과 정합.
- **임베딩**: 384차원 `bge-small-en-v1.5`(fastembed).
- **기능 완비**: 진짜 CRUD·영속성·user/session 필터·`min_similarity` 임계·배치 단일 커넥션.

설계와 구현 사이의 공백을 메우는, "만들려는 바로 그것"의 동작 예제라는 점이 핵심 가치다.

## 결정론 교훈 — 임베딩 바이트 일치

Rust/Python 두 구현이 *동일 fastembed*를 써서 임베딩 바이트까지 일치시킨다. 이는 [[결정론_검증_게이트]]의 "같은 입력 → 같은 출력" 불변식을 *벡터화* 단계까지 끌고 간 사례 — 임베딩조차 비결정 요소가 아니라 재현 가능한 결정론 산출물로 다룬다.

## 볼트 정합 — 이미 절반은 와 있다

본 볼트는 [[Codegraph_MCP_통합]]의 codegraph DB가 마크다운을 인덱싱하며 *이미 sqlite 기반 벡터 테이블*(mdast_vectors)을 운용한다. 즉 "sqlite + 벡터"의 하부 구조는 검증 완료. Track B가 더할 것은 *전용 위키/메모리 벡터 스토어*의 CRUD·필터·persistence 계층이며, 본 레퍼런스가 그 청사진이다. [[카파시_LLM_위키_패턴]]의 영속 누적 위에 온디맨드 시맨틱 질의를 얹는 마지막 조각.

## 리스크

낮음. 의존성은 `sqlite-vec`·`fastembed`, 그리고 임베딩 모델 1회 다운로드(~30MB)·임베더 런타임뿐. 본 입국심사가 *가장 즉시 실행 가능*하다고 평가한 원자다.

## 출처

- raw/headroom_입국심사_2026-06-14.md (2026-06-22 편입) — Atom 4 sqlite-vec 위키 벡터 메모리(384d bge-small-en-v1.5·CRUD·user/session 필터·min_similarity·Rust/Python 임베딩 바이트 일치)
- 상류: github.com/chopratejas/headroom
