---
name: distill-to-raw
description: Use when the user invokes /distill-to-raw <url>, or hands over a YouTube / article / GitHub link to dissect into the LLM Wiki. Clones or extracts the source (GitHub repo·subdir, video transcript, or page text) and produces TWO files — a 7-section teardown analysis report in docs/analysis/ (incl. a reuse-economics adversarial check: can each atom be absorbed by adding minimal lines to an existing skill/hook/rule/command?), and an atom-by-atom admission review (⭐1–5 evidence-based recommendation, judged against schema/vault_mandate.md) in raw/. Runs SILENTLY — no main-context output during work, only "정제 완료" at the very end. Wiki location resolved by tracking the WIKI git remote, never hardcoded.
---

# Distill to Raw — 링크 한 개를 해체 분석 + 입국심사 2문서로

## Overview

`/distill-to-raw <URL>` 수신 시, **출처 원문(레포 소스 / 영상 스크립트 / 본문)을 유일 근거로** 대상을 해체 분석하고, 그 지식이 이 볼트에 들일 가치가 있는지 원자 단위로 심사한다. 산출은 **항상 2개 파일**이다.

| 산출 | 위치 | 내용 |
|---|---|---|
| **해체 분석 보고서** | `docs/analysis/<slug>_analysis.md` | 7섹션(목적·구현·적대검증·기여·토큰·**재사용경제성**·종합) |
| **입국심사 문서** | `raw/<slug>_입국심사.md` | 원자별 ⭐1–5 추천 + 토큰경제학 + 근거 (선택 대기) |

모범 사례(이 스킬의 출력 명세): `docs/analysis/sequentialthinking_analysis.md` + `raw/sequentialthinking_입국심사.md`. 동일 구조·톤을 따른다.

파이프라인 위치:
- [[move-to-raw]]: 로컬 파일을 **그대로** raw에 복사 (무가공)
- **distill-to-raw**(본 스킬): URL을 **해체·심사**해 2문서 생성 (분석 보고 + 입국심사)
- [[compile-wiki]]: raw 입국심사의 **승인 원자**를 obsidian 노트로 컴파일

## 출력 억제 (필수 · 최우선 규칙)

**이 스킬 실행 중 메인 대화창 출력을 0으로 한다.** 진행 상황·수집 로그·분석 본문·요약·파일 경로를 대화에 쓰지 않는다. 모든 산출은 **파일(docs/analysis, raw)에만** 기록한다. 도구는 조용히 호출하고, 사고는 thinking에서만 한다. 모든 작업이 끝나면 **정확히 한 마디** —

```
정제 완료
```

— 만 출력한다. (그 외 텍스트·표·경로 나열 금지. 실패·질의가 불가피할 때만 예외적으로 최소 출력.)

## 위키 위치 해석 (git 추적 · 하드코딩 금지)

위키는 PC마다 경로가 다른 단일 git 레포다. 경로를 하드코딩하지 않고 **git remote 신원으로 추적**한 뒤 상대경로를 쓴다. 정규 신원: **`github.com/evespimrose/WIKI`**.

```bash
python "<SKILL_DIR>/scripts/resolve_wiki_raw.py"                      # → <root>/raw
python "<SKILL_DIR>/scripts/resolve_wiki_raw.py" --subdir docs/analysis  # → <root>/docs/analysis
```

`<SKILL_DIR>` = 이 SKILL.md의 디렉토리. 두 경로(raw·docs/analysis)를 단계 0에서 확보한다. 해석 실패 시에만(예외) 사용자에게 클론 경로 1회 질의 후 `--root <경로>` 재실행.

## 볼트 탐색 — CodeGraph 질의 (기존 노트 대조용 · Grep/Read 금지)

§4(볼트 기여)·입국심사에서 **기존 obsidian 노트와의 대응·중복·링크 후보**를 찾을 때 직접 Grep/Glob/Read 로 볼트를 훑지 않는다. wiki 루트 하위 `.codegraph/codegraph.db`(마크다운 지식 그래프 — `doc` 노드 + `doc_link` 엣지 = `[[위키링크]]`)에 `codegraph` 커맨드로 질의한다. **외부 출처 원문 수집(GitHub/유튜브/웹)은 종전대로** — 이 절은 **볼트 쪽 대조**에만 적용한다.

WIKI_ROOT 확보(하드코딩 금지 · remote 추적):

```bash
WIKI_ROOT=$(python "<SKILL_DIR>/scripts/resolve_wiki_raw.py" --subdir .)
```

아래 모든 `codegraph` 커맨드에 `-p "<WIKI_ROOT>"` 를 붙인다.

| 목적 | 커맨드 |
|---|---|
| 신선도 | `codegraph status -j` → `pendingChanges` > 0 이면 `codegraph sync` |
| 원자 개념 → 기존 노트 | `codegraph query "<원자 개념>" -j -l 8` |
| 백링크 / 아웃링크 | `codegraph callers \| callees "<노트명>" -j` |
| 이웃군(중복·충돌) | `codegraph impact "<노트명>"` |

원칙: in-scope 교차점·기존 [[노트]] 대응·중복은 `query` 히트로 판정한다. obsidian 전수 Grep/Read 금지. DB 없으면 `codegraph init -i -p "<WIKI_ROOT>"` 로 빌드 후 진행. (governance 스펙인 `schema/vault_mandate.md`·`scout_lexicon.md` 직접 읽기는 탐색이 아니므로 종전대로.)

## 워크플로우 자산 탐색 — 기존 skill/hook/rule/command 인벤토리 (§6 재사용 검증용)

분석 §6(재사용 적대 검증)에서 "기존 자산에 최소 줄 수로 흡수 가능한가"를 판정하려면 현재 가동 중인 **개인 통합 워크플로우(claude-personal-integrated-workflow)** 자산을 근거로 봐야 한다. **전수 재귀 스캔은 CAVE-MAN 위반**이자 그 자체로 토큰 낭비(vault_mandate 토큰 통제 위반) — **바운디드 조회만** 한다.

| 자산 | 위치 | 조회 방식 |
|---|---|---|
| skill | `.claude/skills/*/SKILL.md` | Glob → 원자별 후보 1–2개만 Read |
| command | `.claude/commands/*.md` | Glob → 후보만 Read |
| hook | `.claude/hooks/*.sh` + `.claude/settings.json`(hooks 블록) | Glob + settings 1회 Read |
| rule | CORE_RULES(session-start 주입) · `CLAUDE.md` · `schema/` | 직접 Read(governance) |

원칙: 원자 1개당 **가장 그럴듯한 재사용 후보 1–2개만** 열어 최소-diff 가능성을 본다. 전체 자산을 매 분석마다 정독하지 않는다(그 자체가 토큰 낭비).

## 실행 프로토콜

```
WHEN /distill-to-raw <URL> 수신:   (전 과정 무출력 — 끝에 "정제 완료"만)

[단계 0: 경로 해석]
0. resolve_wiki_raw.py 로 RAW_DIR + ANALYSIS_DIR(--subdir docs/analysis) + WIKI_ROOT(--subdir .) 확보.
   - WIKI_ROOT 로 `codegraph status -j` 확인(필요 시 `sync`). 이후 볼트 대조는 「볼트 탐색」 질의로만.

[단계 1: 입력 판별 — garbage in 의 출처 결정]
1. URL 분류:
   - github.com/<owner>/<repo>[/tree|blob/<ref>/<subpath>] → "코드/문서 레포" 경로
   - 유튜브(watch·youtu.be·shorts·embed·live) → "영상 스크립트" 경로
   - 그 외 일반 링크 → "텍스트(본문)" 경로

[단계 2: 원문 수집 — 왜곡의 원천 제거]
2a. (GitHub) fetch_github.py 실행:
    python "<SKILL_DIR>/scripts/fetch_github.py" "<URL>"
    - 얕은 clone → README + 핵심 소스(index/lib/server/package.json 등) 수집.
    - JSON: {owner,repo,ref,subpath,description,readme_path,file_count,files?|bundle_file,ok}.
    - files 인라인이 있으면 그대로 정독. 없고 bundle_file 만 있으면(큰 레포) → Read 로 그 파일
      전체를 읽어 분석. 절대 잘린/일부 소스로 단정하지 않는다.
    - clone 실패(비공개·네트워크) → 사용자에게 소스/URL 재요청. 지어내지 않는다.
2b. (유튜브) fetch_youtube.py "<URL>" --langs ko,en --auto-install
    - transcript 인라인이 있으면 그대로, transcript_file 만 있으면 Read 로 전문 정독.
2c. (일반 링크) WebFetch 로 본문+메타 추출 → 빈약하면 exa(mcp__exa__web_fetch_exa) → 사용자 요청.
2d. 원문 언어 무관, 산출 문서는 한국어. 의미 보존·왜곡 금지.

[단계 3: 해체 분석 보고서 작성 → docs/analysis]
3. 원문을 완전히 소화한 뒤 "분석 보고서 포맷"의 7섹션을 작성한다.
   - 1.목적 2.구현 3.적대적 검증 4.볼트 기여(vault_mandate 기준) 5.토큰 추정 6.재사용 경제성 7.종합
   - 3(적대검증)은 "표방 vs 실제" 대조가 핵심 — 마케팅/주장과 실제 코드·내용의 괴리를 짚는다.
   - 4(볼트 기여)의 "기존 [[노트]] 대응·in-scope 교차점"은 **CodeGraph 질의**(`codegraph query`/`callers`)로 근거를 잡는다 — 볼트 Grep/Read 금지.
   - 6(재사용 경제성)은 원자별로 "기존 skill/hook/rule/command +최소줄로 흡수 가능한가"를 적대적으로(가능 가정→반증) 검증하고, 추가 LOC·턴당 토큰 Δ·구현 비용·로드맵 충돌·적용 합의점을 표로 낸다. 자산 인벤토리는 「워크플로우 자산 탐색」의 바운디드 조회로만(전수 스캔 금지).
   - ANALYSIS_DIR/<slug>_analysis.md 로 저장(Write). 대화 출력 없음.

[단계 4: 원자별 입국심사 작성 → raw]
4. schema/vault_mandate.md(필요 시 scout_lexicon.md 판례)를 기준으로, 대상을 기능별
   원자로 분해하고 각 원자를 ⭐1–5 로 심사한다("입국심사 포맷").
   - 원자별: 추천도 ⭐ · 기여도(워크플로우 적합도·신규성) · 토큰경제학(턴당비용·조건·Benefit·Risk)
     · 근거(기여이유·토큰계산·리스크) · 판정 코멘트.
   - 각 원자의 신규성·중복·기존노트 확장 위치는 `codegraph query "<원자 개념>"` 히트(+`callers`/`callees` 링크 후보)로 판정한다. 볼트 전수 스캔 금지.
   - 각 원자에 **재사용 합의점**(§6 연계: 기존 skill/hook/rule/command +k줄 / 신규 / 보류 + 턴당 토큰 Δ + 로드맵 불훼손 근거)을 1줄 명시.
   - verdict: pending_selection (사용자 선택 대기). RAW_DIR/<slug>_입국심사.md 로 저장(Write).

[단계 5: 종료 — 단 한 마디]
5. 두 파일 저장 확인 후, 대화에 정확히 "정제 완료" 만 출력. 그 외 일절 무출력.
   (임시 bundle/transcript 파일은 정리.)
```

## 정제 철학 (garbage in · find gold · garbage out)

1. **Garbage in** — 출처 원문이 **유일 근거**. 외부지식·추측·일반론 주입 금지. 주장·정의·수치·인과를 의미 그대로 보존.
2. **Find gold** — 군더더기(홍보·인사·설치 절차·반복)·기반지식을 버리고, 새롭고 이전 가능한 핵심만 취한다.
3. **Garbage out** — 버린 것은 두 산출물에 나타나지 않는다.

적대적 검증 원칙: 분석 §3은 "출처가 **표방하는 것**"과 "코드/내용이 **실제 하는 것**"을 분리해 대조한다. 마케팅 언어를 사실로 옮기지 않는다.

## 분석 보고서 포맷 (`docs/analysis/<slug>_analysis.md`)

```markdown
# Report — <대상> 분석

> 생성일: <오늘 YYYY-MM-DD>
> 대상: <URL> (clone/수집 시점: <YYYY-MM-DD>)
> 조사 범위: <README ✅ / 핵심 소스 파일들 ✅ / 영상 자막 ✅ 등 실제 본 것만>

## 1. 무엇을 위해 개발되었는가 (목적)
<한 줄 정의 + 타깃·핵심 가치. 출처가 표방하는 목적을 사실 그대로.>

## 2. 어떻게 달성했는가 (구현)
<진입점 → 핵심 모듈/제어 파라미터 흐름. 코드·구조 근거로.>

## 3. "정말로" 그러한가 (적대적 검증)
**표방대로 작동하는 것:** <코드로 확인된 것 ✅>
**표방하나 실제는 다른 것:** | 주장 | 실제 | 표로 대조
**숨은 전제 / 결론:** <구조화 이점이 어디서 오는가 등>

## 4. LLM 위키 워크플로우에 무엇을 기여할 수 있는가
`schema/vault_mandate.md` 기준:
- **In-scope 교차점**: <기존 [[노트]]와의 직접 대응>
- **구체적 기여 가능 개념**: <1, 2 …>
- **불일치점(out-of-scope 인접)**: <설치 튜토리얼/레시피 경계>
- 기여 판정: <전체 채택 / 개념 추출 조건부 / 보류>

## 5. 핵심 로직 100% 적용 시 턴당 토큰 증가 추정
<상시 적용 여부 + 호출당 비용 표(schema·호출·응답) + 베이스(가정) 대비 % 증가 + 결론>

## 6. 기존 자산 재사용 적대 검증 & 구현 경제성 (claude-personal-integrated-workflow 기준)
**적대 전제**: "이 원자는 기존 skill/hook/rule/command에 **최소 줄만 더하면 흡수된다**"를 참으로 가정하고, 반증되는 원자만 신규 자산 후보로 승격한다. (새로 만들기 편향 차단 = vault_mandate 재사용·토큰 통제 목표.)

| Atom | 최소-diff 재사용 후보(기존 skill/hook/rule/command) | 추가 LOC | 턴당 토큰 Δ(상시/조건부) | 구현 비용(난이도·위험) | 로드맵 충돌? | 적용 합의점 |
|---|---|---|---|---|---|---|
| <개념> | <예: compile-wiki +N줄 / cave-man-guard.sh +N줄 / CORE_RULES +1줄 / 신규 불가피> | <±N> | <+0% / +N%> | <낮음·중·높음 + 위험> | <無 / vault_mandate ○○ 항목과 긴장> | <기존 X에 +k줄 / 신규 자산 / 보류> |

- **적용 합의점**이란: vault_mandate 목표(토큰 통제·환각0·재사용 우선)를 **해치지 않으면서** 최소 footprint로 효과를 내는 지점. 신규 자산은 "기존 +최소줄로 불가능"이 입증된 원자에만 권한다.
- 자산 인벤토리 조회는 「워크플로우 자산 탐색」 절의 바운디드 방식만(원자당 후보 1–2개, 전수 재귀 스캔 금지).

## 종합
<해체 결론 1문단 + 채택 조건>
```

## 입국심사 포맷 (`raw/<slug>_입국심사.md`)

```markdown
---
source_type: git            # git | youtube | web
source_url: <URL>
captured: <오늘 YYYY-MM-DD>
status: raw
verdict: pending_selection
analysis_mode: atomic
atoms_total: <N>
---

# 입국심사 — <대상> (원자 선택 모드)

> **사용자 가이드**: 각 원자를 `[ ]`/`[x]`로 선택. 토큰 비용·리스크·기여도를 근거로 의사결정 지원.

## 지향 방향성(기준)
`schema/vault_mandate.md` 북극성 요약 + in/out-of-scope 한 줄.

## 원자 단위 체크리스트 (선택 가능)

### ☐ Atom 1: <원자 제목>
**추천도**: ⭐⭐⭐⭐⭐ 5/5
**기여도**: 워크플로우 적합도 <…> · 신규성 <…>
**토큰 경제학**: 턴당 비용 <+0%/+N%> · 조건 <일회성/상시> · Benefit <…> · Risk <…>
**재사용 합의점**: <기존 [[skill/hook/rule/command]]에 +k줄 / 신규 자산 불가피 / 보류> · 턴당 토큰 Δ <…> · 구현 비용 <난이도·위험> · 로드맵 불훼손 근거 <vault_mandate 목표 대조> (상세 분석 §6)
**근거**: 기여 이유 <…> · 토큰 계산 <…> · 리스크 평가 <…>
**판정 코멘트**: <단독 노트 / 기존 [[노트]] 확장 / 제외 등 구체 위치 제안>

### ☐ Atom 2: …

## 종합 평가
| 지표 | 평가 |  (총 원자 수 · ⭐5 개수 · 조건부 · 비추천 · 예상 채용 시나리오)

## 최종 판정
- **정식 verdict**: pending_selection (사용자 선택 후 재입력 대기)
- **AI 추천**: <어느 원자를 어디로 — 신규 노트/기존 확장/제외 + 총 런타임 토큰 증가>

## 분석 보고서 연계
- 상세는 `docs/analysis/<slug>_analysis.md` 참조.
```

### ⭐ 추천도 루브릭 (근거 기반)
- ⭐5: vault_mandate in-scope 정면 + 신규 + 런타임 +0%(개념 추출). 갭분석 Priority 항목이면 가산.
- ⭐4: in-scope + 유용하나 기존 노트 확장이 적합 / 또는 저비용 경고·사례.
- ⭐3: 참고 가치 있으나 통제 철학과 긴장 or 부분 중복 → 조건부.
- ⭐2: 주변부·이미 보유 기능과 중복.
- ⭐1: out-of-scope(설치·운용 절차) 또는 토큰 비용이 값어치 초과 → 비추천.
- ⭐ 가산/감점(재사용 경제성, §6): 기존 자산 **+최소줄**로 흡수 + 턴당 +0~소량이면 채택 매력↑(재사용 우선). 신규 자산 다수 필요 + 상시 토큰 증가면 ↓.

## 규칙

- **출처가 유일 근거**: 소스/본문/자막에 없는 것은 쓰지 않는다. 불확실은 명시.
- **2문서 고정**: 분석 보고서(docs/analysis) + 입국심사(raw). 둘 다 1파일씩.
- **하드코딩 금지**: 경로는 resolve_wiki_raw.py(remote 추적)로만.
- **볼트 대조는 CodeGraph로**: 기존 노트 대응·중복·링크 후보는 `.codegraph` 질의(「볼트 탐색」)로만. obsidian 전수 Grep/Glob/Read 금지(외부 출처 수집은 무관).
- **vault_mandate 기준 심사**: 기여·추천은 `schema/vault_mandate.md`의 in/out-of-scope·갭분석에 근거.
- **적대적 검증 의무**: 표방과 실제를 분리. 마케팅을 사실로 옮기지 않는다.
- **재사용 우선 적대 검증(§6)**: '새로 만들기' 전에 '기존 skill/hook/rule/command +최소줄로 같은 효과'를 반증하지 못하면 신규 자산을 권하지 않는다. 구현 비용·턴당 토큰 Δ·로드맵(vault_mandate) 불훼손을 근거로 atom별 합의점을 명시.
- **한국어 산출**: 원문 언어 무관, 왜곡 없이 한국어로.
- **출력 억제**: 작업 중 무출력, 끝에 "정제 완료"만.
- **충돌 무음 금지**: 동명 파일은 접미사로 고유화, 덮어쓰지 않는다.
- **정직한 실패**: 수집 실패 시 지어내지 말고(예외적 최소 출력으로) 사용자에게 요청.

## 금지 사항

- 메인 컨텍스트에 분석 본문·진행 로그·파일 경로 출력 (출력 억제 위반)
- 출처에 없는 내용 생성·추정·일반론 주입 (왜곡)
- 위키 절대경로 하드코딩
- **obsidian 볼트 전수 Grep/Read 로 기존 노트 대조** (CodeGraph 질의로 대체)
- **§6 재사용 검증을 위한 `.claude/` 전수 재귀 스캔** (원자당 후보 1–2개 바운디드 조회로 대체)
- 설치·운용 절차를 핵심 지식인 양 옮겨 적기 (정제 실패)
- obsidian/archive 수정, 파일 무음 덮어쓰기

## 연계 스킬

- [[compile-wiki]]: 입국심사의 **승인 원자**(사용자 선택 후)를 obsidian 노트로 컴파일. `/compile-wiki a` 는 raw 입국심사를 베이스 정합성 관점에서 재심사.
- [[move-to-raw]]: 로컬 파일 **무가공** 적재.
