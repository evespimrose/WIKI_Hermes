# Try — 신경계 로드맵 §7 미해결 결정 3건 분석

> 작성일: 2026-06-04
> 대상 작업: `docs/Roadmap_NervousSystemEvolution.md` §7의 미해결 결정 3건(Track B 인덱스 재사용 여부 · INDEX.md 포맷 · 의도 질의 트리거)을 이행했을 때의 결과·위험·더 나은 경로 분석
> 성격: 사전 분석(/try). **코드·노트·인덱스 미작성.** 읽기·판단만.
> 조사 근거: 로드맵 본문 + `schema/`(vault_mandate·scout_lexicon·LOG·README) + `docs/Try_Hermes*`·`Try_Harness*` + mdAddOn PLAN(`D:\Unity\codegraph\.claude\memory-bank\mdAddOn\plans\...md`) + 게이트 철학 노트([[Cave_Man_Protocol]]·[[맥락_오염_방지]]·[[위키_저장_5대필터]]·[[Raw_Wiki_Schema_3레이어]]) + codegraph 인덱스 상태 실조회

---

## 1. 현황 (As-Is)

### 1.1 파일 구조

```
D:\Unity\WIKI\
├─ obsidian\            56개 .md (루트) + RX_1\ 하위 행성  ← Wiki 레이어(가공)
├─ raw\ / archive\                                         ← Raw 레이어(불변)
├─ schema\             ← Schema 레이어(헌법), 2026-06-04 신설
│   ├─ vault_mandate.md     (북극성, 사람가독 표)
│   ├─ scout_lexicon.md     (판례 단어장, 사람가독 표)
│   ├─ LOG.md               (타임라인, 사람가독)
│   ├─ README.md
│   └─ INDEX.md         ❌ 미생성 ← 결정 2의 대상
└─ docs\               Roadmap·Try_Hermes·Try_Harness

외부 엔진: D:\Unity\codegraph\  (mdAddOn PLAN — 미승인)
원본 모듈: D:\Fork\codegraph-mdast\ (db/embed/parse/search/watch/mcp 6×.mjs)
```

세 결정의 공통 무대는 `schema/` 레이어다. 로드맵 §4가 지적하듯 INDEX·벡터인덱스·트리거가 모두 이 한 레이어로 수렴한다.

### 1.2 병목·문제 정량화 (수치 포함)

| 항목 | 측정/근거치 | 출처 |
|---|---|---|
| obsidian 루트 노트 수 | **56개** (로드맵 자칭 "60+", 실측 56) | 본 세션 실측 |
| schema/ 완성도 | 4/5 파일 (INDEX.md 결손) | 실측 |
| WIKI codegraph 인덱스 | **없음**(`.codegraph/` 미존재) | status 실조회 |
| mdAddOn 엔진 임베딩 | MiniLM 384d + sqlite-vec vec0, 단일 `codegraph.db` | mdAddOn PLAN §목표 |
| mdAddOn 관련성 게이트 비용 | context +6~12% · node +14~28% · impact +18~35% (governing 존재 시에만) | mdAddOn PLAN §출력비용 |
| mdAddOn 승인 상태 | **PLAN 미승인** ("본 문서 승인 전 소스 수정 금지") | mdAddOn PLAN 헤더 |
| 멀티에이전트 토큰 | +30% (every-turn 주입의 위험 상한 참고치) | [[하네스_엔지니어링]] 인용 |
| 프롬프트 캐시 TTL | 5분 (every-turn 훅이 캐시 밖 비용 유발 가능, 추정) | 일반 추정 |

**핵심 병목**: 저장(Raw/Wiki)·헌법(Schema 일부)은 갖췄으나 *런타임 소비 회로*가 전무 — 로드맵이 부르는 "빠진 마지막 1마일". 세 결정이 곧 이 1마일의 설계 분기다.

### 1.3 결정적 발견

세 결정은 독립 문제가 아니라 **하나의 축 — "자동의 힘 vs 토큰·오염 통제" — 의 세 단면**이다. 그리고 이 축의 해답이 *이미 볼트 안에 두 번 구현*돼 있다:

1. **쓰기 방향**: `compile-wiki a` 입국심사 = [[위키_저장_5대필터]]·[[맥락_오염_방지]]의 실행형 게이트. ([2][3] 보류가 실증)
2. **읽기 방향(코드-문서)**: mdAddOn의 *관련성 게이트* — "governing 문서 있을 때만 첨부, 아니면 침묵(silent beats wrong)". `search/callers/trace` 제외로 노이즈 차단.

→ **결정 원리는 새로 발명할 필요가 없다. 기존 게이트 패턴을 읽기 방향으로 이식하면 세 결정이 동시에 풀린다.** (§5 결론의 토대)

부수 발견: mdAddOn의 게이트 키는 `BLK/code_refs`(코드 지배 문서)인데, 위키의 좌표는 `행성/[[wikilink]]`다. **게이트 *의미론*이 호환되지 않는다** — 엔진은 재사용 가능하나 게이트 로직은 재설계 대상(결정 1의 핵심).

---

## 2. 제안 구조 (To-Be)

### 2.1 구조 다이어그램 (현재 vs 제안)

```
[현재] 사람 → move-to-raw → compile-wiki → obsidian(56노트)
        에이전트 ──(런타임 참조 회로 없음)──✗

[제안] obsidian 노트(frontmatter=단일 진실원)
          │ 생성(1방향)              │ 임베딩(1방향)
          ▼                          ▼
        schema/INDEX.md          wiki.db (전용, sqlite-vec)
        (사람뷰 표=생성물)        (기계 질의)
                                     ▲
        프롬프트 의도 ── 사전필터(저비용) ──┘  ← 트리거
          │ (임계 미달이면 침묵)
          ▼ (임계 초과 시에만)
        행성 시맨틱 검색 → 관련성 게이트 → 주입
```

세 결정의 제안 요지:

- **결정 1 (인덱스)** → **전용 `wiki.db` + 엔진 코드만 재사용**. `codegraph.db`에 편입하지 않는다. 원본 `codegraph-mdast`의 6×.mjs를 벤더링해 위키 좌표(행성/wikilink)로 게이트 재구성. codegraph의 *미승인 TS 통합*에 의존하지 않음.
- **결정 2 (INDEX 포맷)** → **거짓 이분법. "표 vs JSON"이 아니라 "손작성 vs 생성".** frontmatter(기계 진실원) → INDEX.md(생성된 사람뷰 표). 드리프트 차단이 본질.
- **결정 3 (트리거)** → **2단계: skill 먼저 → 게이트형 hook 나중.** "hook vs skill"이 아니라 "무조건 주입 vs 게이트 주입". 무조건 every-turn은 Q1 위반이므로 금지.

### 2.2 새 파일 목록 (제안 — 본 /try에서 생성하지 않음)

| 파일 | 역할 | 결정 |
|---|---|---|
| `schema/INDEX.md` | frontmatter에서 **생성**되는 전역 인덱스(사람뷰 표) | 2 |
| (노트 frontmatter 확장) | `planet:` `summary:` 필드 추가 — 기계 진실원 | 2 |
| `tools/wiki_index.mjs` (벤더링) | parse+embed+indexer → `wiki.db` | 1 |
| `wiki.db` | sqlite-vec 전용 위키 벡터 인덱스 (git-ignore) | 1 |
| `.claude/skills/wiki-query/SKILL.md` | 명시 의도 질의 스킬(1단계) | 3 |
| `.claude/hooks/wiki-intent-gate.*` | 게이트형 UserPromptSubmit 훅(2단계) | 3 |

### 2.3 핵심 개념 코드 (의사 코드 수준)

**결정 2 — frontmatter 단일 진실원 → INDEX 생성:**
```yaml
# 각 노트 상단(기계 진실원). 표/JSON 논쟁 불요 — 여기서 파생.
---
tags: [llm-wiki, wiki관리]
planet: Wiki            # ← 신규: 행성 좌표
summary: "맥락 오염의 3대 안전장치"   # ← 신규: 1줄 요약
---
```
```
generate_index():                      # 손작성 금지, 항상 생성
  for note in obsidian/**/*.md:
    fm = read_frontmatter(note)
    rows.append(name, fm.planet, fm.tags, fm.summary)
  write schema/INDEX.md  = render_table(rows)   # 사람뷰(안정 컬럼=기계 파싱 가능)
  # Track B는 INDEX가 아니라 note 본문에서 직접 임베딩
```

**결정 1 — 전용 wiki.db (codegraph.db 비편입):**
```
wiki.db
  notes(path, planet, summary, content_hash, wikilinks[])
  note_vectors  vec0(float[384])         # MiniLM, mdAddOn과 동일 엔진
search_wiki(intent, topk):
  v = embed(intent)                      # 엔진 재사용
  hits = knn(note_vectors, v, topk)
  return gate(hits)                      # ↓ 위키용 게이트(코드 게이트와 다름)
```

**결정 3 — 게이트형 트리거(침묵 우선):**
```
on_user_prompt(p):                       # 2단계: hook
  if cheap_prefilter(p) < θ: return SILENT   # 대다수 턴 0 비용 (Q1 준수)
  hits = search_wiki(p, topk=3)
  if max(hits.score) < θ_inject: return SILENT  # silent beats wrong
  inject(compress(hits, summary≤200))    # 표적 주입만
# 1단계는 동일 search_wiki를 /wiki-query 스킬로 명시 호출(임계·자동화 없음)
```

---

## 3. 장단점 비교

### 3-A. 아키텍처 명확성

| 결정 | 선택지 | 명확성 평가 |
|---|---|---|
| 1 | **전용 wiki.db** | ✅ 투-트랙 분리가 깨끗(Track A=코드/BLK, Track B=위키/행성). 로드맵 §2 표 자체가 인덱스를 이미 둘로 나눔 → 전용이 표와 정합 |
| 1 | codegraph.db 편입 | ⛔ 코드 키(BLK/code_refs) 위에 위키(행성/wikilink)를 얹어 의미론 충돌. 게이트 재사용 불가 |
| 2 | **생성형(frontmatter→INDEX)** | ✅ 단일 진실원. 드리프트 구조적 차단 |
| 2 | 손작성 표 / 손작성 JSON | ⛔ 56노트와 즉시 드리프트. [[Cave_Man_Protocol]] dictionary §6 동기화 훅이 경계한 그 문제 |
| 3 | **skill→게이트hook 2단계** | ✅ 검증 후 자동화. 능동 신경계 목표(hook)와 토큰경제(Q1)를 단계로 화해 |
| 3 | 즉시 무조건 hook | ⛔ every-turn 주입 = Q1 직접 위반 |

### 3-B. 컴파일·빌드 영향

- 본 볼트는 빌드 산출물이 없는 *지식 저장소* → 컴파일 영향 **해당 없음**.
- 단 결정 1의 *엔진*은 네이티브 의존(`sqlite-vec`, `@xenova/transformers`)을 끌어온다. mdAddOn PLAN이 이를 `optionalDependencies`+lazy+opt-in으로 처리한 패턴을 그대로 차용하면 위키 도구도 미설치 시 graceful skip 가능.
- `wiki.db`는 반드시 **git-ignore**(바이너리·대용량·재생성 가능). 미설정 시 동기화 저장소 오염.

### 3-C. 현재 작업과의 연관성

- 세 결정 모두 [[Try_HermesKnowledgeScout]]·[[Try_HarnessWorkflowIntegration]]와 *동일 1마일*을 공유. 특히 결정 1의 `wiki.db`는 헤르메스의 `scout_lexicon` 기계소비(scout_lexicon "미배선" 절)와 하네스 생성 에이전트의 볼트 참조(Harness §6 "런타임 배선 선결")가 **공통으로 기다리는 인프라**다.
- 결정 3의 게이트 패턴은 입국심사(쓰기)·mdAddOn(코드읽기)에 이은 *세 번째 게이트(위키읽기)* — 볼트 게이트 철학의 자연 확장.

### 3-D. 단기 비용 — 위험도 표

| 위험 | 등급 | 내용 | 완화 |
|---|---|---|---|
| mdAddOn 승인 대기에 결정 1을 묶음 | 🔴고 | 외부 repo의 미승인 PLAN에 위키 신경계 일정이 종속 | **원본 `codegraph-mdast` .mjs를 직접 벤더링** → codegraph TS 통합 승인과 디커플 |
| codegraph.db 스키마 결합 | 🔴고 | 위키가 코드툴 DB 마이그레이션(v5…)에 깨짐 | 전용 wiki.db로 의존 방향 차단(§4) |
| every-turn 훅 토큰 난사 | 🔴고 | Q1·Pro 토큰 보호 위반, 캐시 밖 비용 | 게이트형 훅 + 2단계(skill 우선) |
| frontmatter 정규화 누락 | 🟡중 | 56노트 다수가 `planet/summary` 미보유 → 생성 INDEX 빈칸 | 컴파일 시 frontmatter 보강을 선행 작업화 |
| 읽기 오염(피드백 루프) | 🟡중 | 훅이 모델 자기출력을 맥락으로 재주입 → [[맥락_오염_방지]] 읽기판 | 관련성 게이트 임계 + summary≤200 압축 |
| 정책 충돌 점검 | 🟢저 | CLAUDE.md "고립 노트 금지"가 INDEX·schema에 적용되나? | schema/는 obsidian/ **밖** → 양방향링크 의무 비대상. 충돌 없음 |

### 3-E. 장기 유지보수

- **결정 1 전용 인덱스**: 엔진을 벤더링하면 원본 업스트림과 드리프트 가능 → 버전 핀 + 출처 주석으로 관리. 그래도 codegraph.db 결합보다 *유지보수 표면이 작다*(위키만 책임).
- **결정 2 생성형**: 노트 추가/삭제가 자동 반영 → 10MB·수백 노트로 커져도 인덱스 손유지 비용 0. 가장 장기 친화적.
- **결정 3 2단계**: skill은 영구 저비용 폴백으로 남고, 훅은 임계 튜닝이 끝나야 승격 → 운영 리스크를 시간축으로 분산.

---

## 4. 순환 의존성·방향 위험 분석

핵심 위험은 *순환*이 아니라 **의존 방향(direction)** 이다.

```
❌ 잘못된 방향:  WIKI(지식자산) ──depends on──▶ codegraph.db(코드툴 내부스키마)
   → 하위 도구가 상위 자산을 인질로. codegraph v5 마이그레이션이 위키 신경계를 깨뜨림.

✅ 올바른 방향:  WIKI ──owns──▶ wiki.db
                 WIKI ──vendors(복사)──▶ codegraph-mdast/*.mjs  (런타임 의존 아님)
   → 위키가 자기 인덱스를 소유. 엔진은 '복사된 코드'일 뿐 살아있는 의존이 아님.
```

추가 방향 위험 2건:
- **INDEX 드리프트 순환**: 손작성 INDEX ↔ 56노트 양방향 갱신 → 영구 불일치. **생성(노트→INDEX 1방향)** 으로 순환 절단.
- **훅 피드백 순환**: 무조건 주입 훅 → 모델 출력이 다음 턴 맥락 → 자기강화 오염. 관련성 게이트가 임계로 순환을 끊음.

세 결정의 올바른 선택이 모두 *1방향·디커플* 로 수렴한다 — 이것이 본 분석의 구조적 일관성.

---

## 5. 종합 평가 및 추천

### 결론 (한 문단)

세 미해결 결정은 겉보기에 별개지만 실은 "자동의 힘을 토큰·오염 통제와 어떻게 화해시키는가"라는 단일 축의 세 단면이며, 그 해법은 볼트가 이미 두 번(입국심사·mdAddOn 관련성 게이트) 구현한 *게이트 패턴의 읽기 방향 이식*이다. 따라서 **(1) 인덱스는 codegraph.db에 편입하지 말고 원본 .mjs 엔진만 벤더링한 전용 `wiki.db`로, (2) INDEX.md는 표/JSON 택일이 아니라 frontmatter에서 생성되는 사람뷰 산출물로, (3) 트리거는 즉시 훅이 아니라 skill→게이트형 훅 2단계로** 가는 것이 세 결정 모두에서 위험 최소·정합 최대의 경로다. 단 어느 것도 지금 착수 대상이 아니며(로드맵은 "확정 아님"), 본 문서는 결정을 *사용자에게 제출*할 뿐이다.

### 단계별 추천 순서

```
Phase 0 (무비용 선결):
  - frontmatter에 planet/summary 필드 정규화 정책 확정 (결정 2 전제)
  - wiki.db git-ignore 등록 (결정 1 위생)

Phase 1 (결정 2 — 가장 낮은 위험, 가장 즉시 유용):
  - frontmatter→INDEX.md 생성 스크립트 1개 (손작성 금지)
  - 56노트 frontmatter 보강 → INDEX.md 첫 생성
  → Track B 없이도 사람·에이전트 가독 전역 인덱스 즉시 확보

Phase 2 (결정 3 1단계 — skill):
  - /wiki-query 스킬로 명시 시맨틱 질의 (자동화·임계 없음)
  → 검색 품질·관련성 임계를 저위험으로 실측

Phase 3 (결정 1 — 전용 wiki.db):
  - codegraph-mdast .mjs 벤더링 → wiki.db PoC (codegraph 승인 무관)
  - 행성/wikilink 게이트로 재구성 (BLK 게이트 아님)

Phase 4 (결정 3 2단계 — 게이트형 훅):
  - Phase 2에서 튠한 임계로 UserPromptSubmit 게이트 훅 승격
  - silent-beats-wrong 검증 후에만 상시화
```

기존 두 try(헤르메스·하네스)의 "입국심사 승인분 먼저 컴파일" 선결과 동일 철학 — *저위험·고검증 단계부터*.

---

## 6. 미결 사항 연계

| # | 내용 | 결정자 |
|---|---|---|
| 1 | mdAddOn PLAN 승인 여부 — 승인되면 TS 포팅본을, 미승인이면 원본 .mjs를 벤더링 (어느 쪽이든 결정 1은 디커플 권장) | 사용자 + codegraph 오너 |
| 2 | frontmatter `planet/summary` 정규화를 컴파일 파이프라인 의무로 격상할지 | 사용자 |
| 3 | `wiki.db` 위치·동기화 정책 (git-ignore 확정 시 다중 PC에서 각자 재생성 vs 1곳 생성 공유) — [[Git_기반_다중PC_동기화]] 연계 | 사용자 |
| 4 | 게이트형 훅의 관련성 임계(θ) — Phase 2 실측 후 수치 확정 | Phase 2 데이터 |
| 5 | INDEX.md를 사람뷰 표로만 둘지, Track B용 `INDEX.json` 사이드카를 추가할지(추가 시 2진실원 드리프트 위험 재발) | 사용자 |
| 6 | 본 3결정은 [[Try_HermesKnowledgeScout]] `scout_lexicon` 기계소비·[[Try_HarnessWorkflowIntegration]] 볼트참조와 동일 인프라(wiki.db) 공유 — 통합 착수 시점 조율 | 사용자 |

> 다음: 본 분석은 결정 제출용. 채택 시 Phase 0~1부터 (전부 read/생성 중심·저위험). 실제 착수는 별도 지시로.
