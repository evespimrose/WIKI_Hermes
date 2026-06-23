---
tags: [llm-wiki, wiki관리, 아키텍처]
date_created: 2026-06-04
last_modified: 2026-06-22
---

# Raw / Wiki / Schema 3레이어

[[카파시_LLM_위키_패턴]]의 물리 구현 골격. 지식 베이스를 *불변 원본 / 가공 영역 / 규칙*의 세 레이어로 분리한다. 본 볼트의 폴더 구조가 이 3레이어에 거의 1:1 대응한다.

## 3레이어 정의

| 레이어 | 역할 | 규칙 | 본 볼트 대응 |
|---|---|---|---|
| **Raw** | 마크다운 변환 원본·스크린샷 등 참고자료 | 에이전트가 *절대 고치거나 삭제 불가* | `raw/` + `archive/` |
| **Wiki** | 에이전트가 마음껏 정리하는 작업공간 (일지·결정사유·에러노트, 유기적 연결) | 자유 가공 | `obsidian/` |
| **Schema** | 에이전트의 '헌법' — 규칙·인덱스·로그 | CLAUDE.md · INDEX.md · LOG.md | `CLAUDE.md` + (신설) `schema/` |

## 본 볼트와의 정합·격차

- **Raw·Wiki는 이미 완비** — archive 불변 보존([[Sonar_Protocol]] Raw 불변과 동형), obsidian 자유 가공.
- **Schema는 부분** — 루트 `CLAUDE.md`는 있으나 *INDEX.md(전역 기계 인덱스)·LOG.md(타임라인)*가 없다. 행성 허브([[LLM_워크플로우_생태계]] 등)가 사람용 인덱스를 일부 대신하지만 에이전트 질의용은 미비. 이 격차가 [[LLM_Wiki_지식자산_현황]]에서 진단한 "빠진 마지막 1마일"의 Schema 축이다.

## Schema 레이어 신설

본 볼트는 이 진단에 따라 `schema/` 레이어를 신설한다 — INDEX·LOG에 더해 자율 스카우팅용 *볼트 지향 mandate*·*판례 단어장*까지 한 레이어로 수렴시킨다. 상세 진화 경로는 `docs/Roadmap_NervousSystemEvolution`.

그 로드맵의 **Track B(위키 벡터 DB, sqlite-vec)** 는 오래 설계만 있었으나, 이제 [[Track_B_sqlitevec_레퍼런스]]가 작동하는 구현 레퍼런스를 제공해 Schema 레이어의 벡터 인덱스 축을 채운다.

## 한글-영문 하이브리드 (운영 팁)

사람이 읽는 가이드라인(금지표현·톤·기준)은 한국어, 에이전트가 인식하는 *명령어 키워드*(save·ingest·query·reference·lint)는 오작동 방지를 위해 영어로 고정. 본 볼트의 스킬명(compile-wiki·move-to-raw)이 영어인 것과 같은 원리.

## 출처

- raw/옵시디언_위키_비즈니스OS_구축__yt_WcmQPMrCYV8.md (2026-06-04 유입) — 3레이어, 한글-영문 하이브리드
