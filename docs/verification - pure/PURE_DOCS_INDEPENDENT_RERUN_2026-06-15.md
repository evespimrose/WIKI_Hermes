# 순수 문서/Obsidian Vault — 독립 재현 검증 보고서 (`.codegraphignore` + 문서 그래프)

**문서 성격**: `PURE_DOCS_TEST_PROCEDURE.md` / `PURE_DOCS_VERIFICATION_GUIDE.md` 절차를 **처음부터 직접 재실행**한 독립 검증 기록.
기존 `PURE_DOCS_VERIFICATION_REPORT.md`(사전 기입본)를 신뢰하지 않고, 모든 수치를 라이브로 재측정해 대조했다.

**검증자**: Claude Code (독립 재현) · **검증 일자**: 2026-06-15
**대상**: WIKI (LLM 지식 Vault) · BLADE (Obsidian 무협소설 Vault)
**검증 목표**: ① 기능 작동 · ② 적대적 검증(누출/스코프) · ③ 기능개발 종결 성과

---

## 0. 환경 (실측)

| 항목 | 요구 | 실측 | 판정 |
|------|------|------|------|
| Node | 22+ | **v24.14.1** | ✅ |
| CodeGraph | 0.9.8.x | **0.9.8.1** (`C:\Users\Jang\AppData\Roaming\npm\codegraph.ps1`) | ✅ |
| WIKI DB | 존재 | `D:/Unity/WIKI/.codegraph/codegraph.db` (2,142,208 B ≈ 2.04 MB) | ✅ |
| BLADE DB | 존재 | `D:/Unity/BLADE/.codegraph/codegraph.db` (1,843,200 B ≈ 1.76 MB) | ✅ |
| 백엔드 | node:sqlite WAL | node:sqlite 내장(full WAL), journal=wal | ✅ |
| 인덱스 상태 | up to date | 양 Vault 모두 `[OK] Index is up to date` | ✅ |

> 재인덱싱은 수행하지 않음(GUIDE 명시: 준비 단계는 유저가 완료, 재실행 불요). 검증은 전부 **읽기 전용**.

---

## 1. 인덱스 현황 (라이브 재측정)

`SELECT … FROM mdast_metadata`, `nodes`, `edges` 직접 조회 + `codegraph status` 교차 확인.

| 지표 | WIKI | BLADE | 사전기입본 | 일치 |
|------|------|-------|-----------|------|
| Code Files (`files`) | 0 | 0 | 0 | ✅ |
| Markdown docs (`mdast_metadata`) | **76** | **36** | 76 / 36 | ✅ |
| doc 노드 (`nodes` kind=doc) | 76 | 36 | 76 / 36 | ✅ |
| doc_link 엣지 (`edges` kind=doc_link) | **573** | **84** | 573 / 84 | ✅ |
| `status` 표기 (Docs / Concepts / Governs) | 76 / 76 / 573 | 36 / 36 / 84 | — | ✅ |

> **용어 주의(중요)**: `codegraph status` 는 doc 노드를 **"Concepts"**, doc_link 엣지를 **"Governs"** 로 *표시*한다.
> 그러나 DB 원시 `kind` 기준으로는 `concept` 노드 = **0**, `governs` 엣지 = **0**이고, 전부 `doc` / `doc_link` 다.
> 즉 사전기입본 §6 "concept 노드 0" 은 **원시 kind 기준으로 정확**하며, CLI의 "Concepts/Governs" 라벨은 doc/doc_link의 별칭일 뿐이다. 결함 아님.

---

## 2. 테스트 결과 요약

| # | 분류 | 테스트 | WIKI | BLADE | 비고 |
|---|------|--------|------|-------|------|
| T1 | 기능 | `.codegraphignore` 제외 적용 | ✅ | ✅ | 제외 prefix 인덱스 0건 |
| T2 | 기능 | 인덱싱 스코프(Vault 본문) 포함 | ✅ | ✅ | 중첩 하위까지 포함 |
| T3 | 기능 | doc 노드 + doc_link 엣지 | ✅ 76/573 | ✅ 36/84 | 노드=문서수, 엣지≥1 |
| T4 | 기능 | 백링크 양방향 + depth 확장 | ✅ | ✅ | 역/정참조·depth 확장·무한루프 없음 |
| T5 | 기능 | 시멘틱 docs 검색 | ✅ | ⚠️ **부분** | 아래 §4 참조 |
| A1 | 적대 | **누출 0** (채워진 제외 디렉토리) | ✅ **강** | ✅ **강** | 제외 .md 다수 존재·인덱스 0 |
| ③ | 성과 | 코드 0줄 → 실그래프 | ✅ | ✅ | — |

**전체**: 🟢 **핵심 전 항목 통과**, 단 T5(BLADE)는 ⚠️ **부분 통과**(기능 동작 / 랭킹 기준 미충족).

---

## 3. 적대적 검증 — A1 누출 0 (결정적, 강한 증거)

제외가 "빈 디렉토리라서 안 나온 것"이 아님을 증명하기 위해 **디스크 실재 .md 수**와 **인덱스 유입 0**을 동시 측정.

### WIKI `.codegraphignore` (실파일)
```
/docs/  /.vscode/  /.git/  /.vs/  /.claude/  /.codex/  /.trae/  /.obsidian/
/raw/  /schema/  !/obsidian/*.md  /obsidian/.obsidian/  /.codegraph/  /docs/  /archive/
```

| 제외 디렉토리 | 디스크 실재 `.md` | 인덱스 유입 | 판정 |
|---------------|------------------|------------|------|
| `raw/` | **7** (예: GraphRAG__yt_…, headroom_입국심사_2026-06-14.md …) | 0 | ✅ |
| `archive/` | **28** | 0 | ✅ |
| `schema/` | **4** | 0 | ✅ |
| `docs/` | **20** | 0 | ✅ |
| `.obsidian/` | 0 (.md 없음, 설정뿐) | 0 | ✅ |
| **합계** | **59 개 실재 .md** | **0** | ✅ **누출 0** |

### BLADE `.codegraphignore`
```
/docs/  /.vscode/  /.git/  /.vs/  /.claude/  /.codex/  /.trae/  /.obsidian/  /.cursor/
```

| 제외 디렉토리 | 디스크 실재 `.md` | 인덱스 유입 | 판정 |
|---------------|------------------|------------|------|
| `docs/` | **8** | 0 | ✅ |
| `.obsidian/` | 0 | 0 | ✅ |

**DB 직접 대조** (`SELECT file_path … WHERE startswith(prefix)`):
- WIKI: `{raw/:0, archive/:0, schema/:0, docs/:0, .obsidian/:0}` / 전체 76
- BLADE: `{docs/:0, .obsidian/:0}` / 전체 36

> **판정**: 실제로 **WIKI 59개 / BLADE 8개의 .md가 채워진** 제외 디렉토리에서 인덱스로 **단 한 건도 새지 않음**.
> 누출 0이 "빈 디렉토리 효과"가 아니라 **실데이터 정밀 차단**임을 강하게 입증. A1 ✅(강).

---

## 4. 기능 테스트 상세 + 증거

### T1·T2 — 제외/스코프 (WIKI)
인덱싱 76건 = root md **3** (`AGENTS.md`·`CLAUDE.md`·`README.md`) + `obsidian/**` **73**.
중첩 하위 `obsidian/RX_1/**`, `obsidian/RX_1/conventions/**`, `obsidian/RX_1/graveyard/**` **모두 포함**.
→ 과소제외(원하는 문서 누락) **0**, 제외 prefix **0**. ✅
BLADE도 동일 패턴: `character/ detail/ power/ root/ world/` 36건 전부 포함, `docs/`·`.obsidian/` 0. ✅

### T3·T4 — 문서 그래프 + 백링크 (WIKI, `obsidian/Architecture_허브.md`)
| depth | Backlinks(역참조) | Forward(정참조) |
|-------|------------------|-----------------|
| d=1 | **4** (asmdef_레이어_경계강제 · Clean_Architecture_4계층 · Western_Salon_허브 · 의존성_역전_DIP) | **13** |
| d=2 | 4 (동일) | **≈70** (전 Vault 허브로 재귀 확장) |

→ 역/정 양방향 반환 ✅, depth 증가 시 정참조 탐색 범위 **13 → 70 확장** ✅, 무한 루프 없이 종료 ✅.
**BLADE** (`power/세력_비화문(秘花門).md`, d=2): Backlinks 2 (`root/blade.md`·`power/Power.md`) / Forward 1 (`character/인물_비화문_수장.md`) — 양방향 정상 ✅.

> 📌 **관찰(결함 아님)**: WIKI d=2 정참조에 `형제 프로젝트.md`·`적용 원리.md`·`tool-history-recorder.sh의 역할.md` 등 **인덱스에 없는 dangling 위키링크 타깃**이 섞여 나온다. 이는 허브 노트의 `[[…]]` 가 가리키는 미생성/섹션성 링크 타깃으로, **제외 디렉토리 출처가 아니며**(mdast_metadata 76건에 없음) 누출이 아니다. Zettelkasten 의 정상적 미해결 링크.

### T5 — 시멘틱 검색
**WIKI** `"멀티에이전트 메모리 아키텍처"` (l=5) — 사전기입본과 **완전 일치**:
| 순위 | 문서 | distance |
|------|------|----------|
| 1 | `obsidian/Architecture_허브.md` | **1.0237** |
| 2 | `obsidian/Western_Salon_Clean_Architecture.md` | 1.0644 |
| 3 | `obsidian/Unity_고정_스튜디오_구조.md` | 1.0767 |
| 4 | `obsidian/Western_Salon_허브.md` | 1.0906 |
| 5 | `obsidian/3Tier_에이전트_스튜디오.md` | 1.1018 |

→ 정본(Architecture 허브) 1위, 결과 전부 `obsidian/**` 스코프 내. ✅
(참고: 더 직접적인 `4계층_메모리_아키텍처.md` 는 top-5 밖 — 임베딩 품질상의 사소한 관찰, 판정엔 영향 없음.)

**BLADE** `"비화문 삼년독화 독공"` (l=5) — ⚠️ **사전기입본과 불일치**:
| 순위 | 문서 | distance |
|------|------|----------|
| 1 | `detail/디테일_저질금창약.md` | **0.7713** |
| 2 | `detail/디테일_관부와무림의경계.md` | 0.8747 |
| 3 | `detail/디테일_누더기내공.md` | 0.9052 |
| 4 | `detail/디테일_정파_대의와희생.md` | 0.9116 |
| 5 | **`detail/디테일_비화문_삼년독화.md`** | **0.935** |

> **불일치(중요)**: 사전기입본은 정답 문서 `디테일_비화문_삼년독화.md` 를 **"1위 (d=0.935) ← 최상위권"** 으로 기재했으나,
> 실제 재현에서는 **5위(꼴찌), d=0.935 가 반환 5건 중 최대 거리**다. 1위는 질의와 느슨하게만 관련된 `저질금창약`(d=0.7713).
> **해석**: 시멘틱 엔진 자체는 동작하고(결과 전부 `detail/` 스코프 내 ✅, 관련 무공·디테일 노트 반환), **정답 문서가 top-5에 포함**되긴 한다. 그러나 성공 기준 "정본 문서가 **상위(작은 거리)** 로 반환" 은 **미충족**(정답이 최대 거리로 꼴찌). → T5(BLADE) **부분 통과**로 판정, 사전기입본의 랭킹 주장은 **재현되지 않음**.

---

## 5. 사전기입본(`PURE_DOCS_VERIFICATION_REPORT.md`)과의 차이

| 항목 | 사전기입본 | 독립 재현 측정 | 영향 |
|------|-----------|----------------|------|
| 핵심 수치(76/573, 36/84, 코드 0, 누출 0) | 기재 | **전부 동일 재현** | 영향 없음(검증됨) |
| WIKI T4 정참조 수 | "20건" | d=1 **13** / d=2 **≈70** | 정성 동작 동일, 수치는 부분 스냅샷이었음 |
| **BLADE T5 랭킹** | 삼년독화 **1위** d=0.935 | 삼년독화 **5위(꼴찌)** d=0.935, 1위=저질금창약 0.7713 | **과대기술** — 기능은 OK, 랭킹 주장 미재현 |
| concept 노드 | "0" | 0(원시 kind) ✓, CLI는 "Concepts 76" 라벨 | 용어 혼동 소지, 결함 아님 |

---

## 6. 목표별 판정

### ① 기능 작동 — ✅ 달성
`.codegraphignore` 제외/스코프, doc·doc_link 그래프, 백링크 양방향+depth 확장, 시멘틱 검색이 두 Vault에서 동작.
(시멘틱 검색은 **BLADE에서 랭킹 품질이 약함** — 기능 가용성은 충족하나 정밀도는 질의 의존적.)

### ② 적대적 검증 — ✅ 통과 (강)
- **누출 0**: WIKI **59개** / BLADE **8개**의 실재 제외 .md → 인덱스 유입 **0**.
- **스코프 정확**: `obsidian/**`·Vault 본문 중첩 하위까지 포함, 제외 prefix 0.
- **과소제외 0**: 76 / 36 전부 포함.

### ③ 기능개발 종결 성과 — ✅ 달성
코드 0줄 프로젝트가 무의미 그래프 → doc_link 실그래프(WIKI 573 · BLADE 84)로 전환. CodeGraph 가 순수 문서/Obsidian Vault에서도 유효한 지식 그래프 도구임을 재확인.

---

## 7. 발견된 이슈 / 한계

1. **[중간] BLADE 시멘틱 랭킹 정밀도** — 정답 문서(`삼년독화`)가 top-5엔 들지만 **최하위**. 임베딩이 표층 어휘(금창약·관부 등)에 끌려 정본을 밀어냄. 기능 종결엔 무방하나, **사전기입본의 "정답 1위" 주장은 사실과 다름** → 보고서 정정 필요.
2. **[정보] `status` 라벨링** — doc/doc_link 를 "Concepts/Governs" 로 표시. 원시 kind엔 concept/governs 0. 사용자 혼동 방지를 위해 라벨 명확화 여지.
3. **[정보] dangling 위키링크** — depth=2 정참조에 미해결 링크 타깃 노출. 누출 아님(스코프 외 파일 미인덱스). 정상.
4. **[정보] WIKI 시멘틱 거리 1.0+** — WIKI 질의 거리대가 BLADE(0.77~)보다 높음(덜 유사). 순위 자체는 합리적.

---

## 8. 결론

**WIKI·BLADE — 핵심 기능 전 항목 검증 통과.** `.codegraphignore` 가 **채워진 제외 디렉토리(WIKI 59·BLADE 8 개 .md) 기준 누출 0** 으로 정확히 차단하고, doc_link 그래프(573·84)·백링크 양방향·depth 확장이 모두 정상 재현됐다. 사전기입본의 정량 핵심 수치는 **독립 재측정으로 전부 일치 확인**.

다만 **BLADE 시멘틱 검색은 ⚠️ 부분 통과**다 — 엔진은 동작하고 정답 문서가 top-5에 포함되나, 사전기입본이 주장한 **"정답 1위"는 재현되지 않고 실제로는 최하위(d=0.935)** 였다. 이는 기능 종결을 막을 수준은 아니나, **보고서의 해당 증거 블록은 정정**해야 하고, 임베딩 랭킹 정밀도는 후속 개선 후보다.

**종합**: 적대적 누출 0 ✅ · 문서 그래프/백링크 ✅ · 시멘틱 검색 기능 ✅(BLADE 랭킹 정밀도 ⚠️). 세 목표 중 ①은 가용성 기준 충족(정밀도 단서 부기), ②·③ 완전 달성 → **기능 개발 종결 가능, 단 BLADE 시멘틱 랭킹 정정·관찰 권고.**

---

**검증자**: Claude Code (독립 재현) · **일자**: 2026-06-15 · **CodeGraph**: 0.9.8.1 · **Node**: 24.14.1
**한 줄 결론**: 누출 0(WIKI 59·BLADE 8 실차단) ✅ / 그래프·백링크 ✅ / 시멘틱 WIKI ✅·BLADE ⚠️(정답 5위, 사전기입본 "1위" 미재현)
