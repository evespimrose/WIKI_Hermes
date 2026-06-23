# Roadmap — 볼트의 신경계 진화 (도서관 → 신경망)

> 작성일: 2026-06-04
> 목적: 이 볼트를 *수동 도서관*에서 *에이전트들이 온디맨드로 참조하는 능동적 공유 신경계*로 진화시키는 설계 로드맵. 사용자 사전 지시(2026-06-04)를 정식 등록.
> 성격: 설계 문서(분석). 컴파일 산출물 아님. 신경계 진화 *설계도 예시 중 하나*로 취급(확정 아님).

## 1. 비전과 격차

**현 진단**([[LLM_Wiki_지식자산_현황]]): 훌륭한 "도서관"이지만 아직 "신경계"는 아니다.

| 레이어 | 상태 |
|---|---|
| Raw / Wiki | ✅ 완비 (`raw`·`archive`·`obsidian`, 60+ 원자노트, 5행성) |
| Schema | 🟡 부분 → **2026-06-04 `schema/` 신설** (mandate·lexicon·LOG; INDEX 미완) |
| **런타임 배선** | ❌ **빠진 마지막 1마일** — 에이전트가 위키를 자동 소비하는 회로 부재 |

목표: [[위키_기반_에이전트_맥락공유]]가 말하는 "모델보다 중요한 맥락 공유"를 *런타임에서* 실현. 단 [[Q1 결론]] — "every-turn 주입" 아닌 **온디맨드 시맨틱 질의**(토큰 경제 = [[Cave_Man_Protocol]] 정신).

## 2. 투-트랙 아키텍처

기술 엔진은 `D:\Fork\codegraph` 의 `mdAddOn` 플랜(sqlite-vec vec0 + MiniLM 384d, 거버닝 문서 관련성 게이트). 이를 두 스코프로 재사용:

| | Track A — 로컬 질의 | Track B — 위키 신경망 |
|---|---|---|
| 인덱스 | `codegraph.db`(프로젝트 코드+md) | `obsidian/` 벡터 인덱스 |
| 범위 | 단일 프로젝트 | **범프로젝트** |
| 질의 의도 | "이 코드베이스 어디 / 거버닝 문서" | **"사용자 개발철학·컨텍스트 의도 파악"** |
| 좌표 | BLK / code_refs | 행성 / `[[wikilink]]` (이미 존재) |
| 엔진 | mdAddOn 그대로 | 동일 sqlite-vec 재사용 |

**핵심 상속**: mdAddOn의 *관련성 게이트*("거버닝 문서 있을 때만 첨부, 아니면 침묵 — silent beats wrong")를 Track B도 계승. 이것이 Q1의 "every-turn 금지"와 Pro 토큰 보호를 *기술 레벨*에서 보증한다 — `search/callers/trace` 제외처럼, 위키 노출도 표적 호출에서만.

## 3. 선결 → 배선 → 소비 (시퀀스)

```
[선결] ✅ 입국심사 승인분 [4]카파시위키·[5]하네스·[1]AI네이티브 컴파일 (2026-06-04 완료)
          → 개념 토대: [[위키_저장_5대필터]]·[[맥락_오염_방지]]·[[하네스_엔지니어링]]·[[Raw_Wiki_Schema_3레이어]]
   ↓
[배선] 🟡 schema/ 신설 (2026-06-04 부분완료: mandate·lexicon·LOG)
          → 남은 것: INDEX.md(전역 기계 인덱스) + sqlite-vec 위키 벡터 인덱스
   ↓
[Track B] ❌ sqlite-vec 위키 질의 DB → 프롬프트 키워드/의도 감지 → 행성 시맨틱 grep
   ↓
[소비] ❌ 프로젝트 세션 + 헤르메스가 온디맨드 의도 질의 (Q1·Q3)
```

## 4. 수렴 포인트 — schema가 3갈래의 합류점

`schema/` 레이어 하나가 세 갈래 과제를 동시에 받는다:
1. **Q2의 INDEX/LOG** — 카파시 3레이어의 Schema(헌법). LOG ✅, INDEX 미완.
2. **헤르메스 판례단어장·mandate** — `docs/Try_HermesKnowledgeScout` §2-1. → `schema/scout_lexicon.md`·`vault_mandate.md` ✅ 시드.
3. **Track B 벡터 인덱스 위치** — 위키 의미검색 DB. 미배선.

→ 따로 설계하지 않고 `schema/`에 수렴시킨 것이 본 로드맵의 구조적 결정.

## 5. 두 입력·실행 레이어 연계

신경계는 저장만으로 살지 않는다. 세 try/제안이 입력·실행을 채운다:
- **입력(자율 스카우팅)**: `docs/Try_HermesKnowledgeScout` — 헤르메스가 `scout_lexicon` 가중치로 사전필터 → `raw/_scout/` → 배치 입국심사. 권한은 사람.
- **실행(ready-to-order)**: `docs/Try_HarnessWorkflowIntegration` — "만들고 싶다" → 하네스가 RIPER-시드 팀 생성 → 볼트를 헌법으로 참조 → EXECUTE 게이트 대기.
- **소비(공유 두뇌)**: 본 로드맵 Track B.

```
[Hermes 스카우트] → raw/_scout/ → [입국심사] → compile → obsidian(신경망)
                                      │                        │
                              [scout_lexicon 환류]   [Track B 시맨틱 질의]
                                                               ↓
[프로젝트 세션 / Harness 생성 에이전트] ← 온디맨드 의도·철학 질의 ←┘
```

## 6. 다음 작업 (우선순위)

1. **INDEX.md 설계** — `schema/INDEX.md`. 행성 허브를 기계 가독 형태로 집약(노트명·태그·행성·요약). Track B 벡터 인덱스의 메타 골격.
2. **Track B PoC** — `obsidian/`를 sqlite-vec로 임베딩하는 최소 인덱서(mdAddOn `parse`/`embed`/`indexer` 포팅 재사용). 별도 `wiki.db` 또는 codegraph 패턴 차용 결정.
3. **의도 질의 인터페이스** — 프롬프트 키워드 → 행성 시맨틱 검색 → 관련성 게이트 주입. hook vs skill 선택(토큰 경제 고려, every-turn 금지).
4. **헤르메스 파일럿** — `raw/_scout/` 1주 1주제 → 배치 입국심사 → `scout_lexicon` 환류 정확도 측정.
5. **harness 파일럿** — `docs/Try_HarnessWorkflowIntegration` 4조건 하에 WS 모듈 1개.

## 7. 미해결 결정

- Track B 인덱스: mdAddOn 재사용 vs 위키 전용 독립 인덱스 (엔진 mdAddOn 자체가 미승인 PLAN — 성숙 의존성 있음).
- INDEX.md 포맷: 사람가독 표 vs 기계 JSON/frontmatter.
- 의도 질의 트리거: hook(자동·토큰비용) vs skill(명시·저비용).

## 관련

- 진단: [[LLM_Wiki_지식자산_현황]] / [[위키_기반_에이전트_맥락공유]]
- Schema 이론: [[Raw_Wiki_Schema_3레이어]] · 실체: `schema/`
- 게이트 철학: [[맥락_오염_방지]] / [[위키_저장_5대필터]] / [[Cave_Man_Protocol]]
- 입력·실행 try: `docs/Try_HermesKnowledgeScout` · `docs/Try_HarnessWorkflowIntegration`
- 엔진: `D:\Fork\codegraph\.claude\memory-bank\mdAddOn\plans\mdAddOn-2026-06-02-markdown-vectordb-integration.md` or `D:\Unity\codegraph\.claude\memory-bank\mdAddOn\plans\mdAddOn-2026-06-02-markdown-vectordb-integration.md`
