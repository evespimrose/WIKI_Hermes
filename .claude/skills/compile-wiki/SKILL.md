---
name: compile-wiki
description: Use when the user invokes /compile-wiki. Analyzes raw knowledge in the LLM Wiki vault's raw/ (vault location auto-resolved via the WIKI git remote, never hardcoded), compiles it into atomic, bi-directionally linked notes inside obsidian/, then moves processed sources into archive/YYYY-MM. The `/compile-wiki a` variant runs a READ-ONLY fitness/admission review instead — scans and extracts concepts but writes nothing, judging whether each raw doc belongs in the knowledge base. Triggers on requests to compile, sync, build, or vet/assess/admit the LLM Wiki vault.
---

# Compile Wiki — Raw 지식을 Obsidian 볼트로 컴파일

## Overview

`/compile-wiki` 호출 시 LLM Wiki 파이프라인의 컴파일 단계를 실행한다. `raw/`에 들어온 미가공 지식을 분석·추상화하여 `obsidian/` 볼트에 원자적·상호 연결된 노트로 빌드하고, 처리 완료된 원본은 `archive/`로 격리한다.

**위키 위치 해석 (git 추적 · 하드코딩 금지):**

위키는 PC마다 절대경로가 다른 단일 git 레포다. 경로를 하드코딩하지 않고 **git remote 신원(`github.com/evespimrose/WIKI`)으로 추적**해 상대경로를 쓴다. 스캔 전(단계 0)에 `resolve_wiki_raw.py`로 **WIKI_ROOT를 확보**하고 나머지는 그 하위로 derive 한다. `<SKILL_DIR>` = 이 SKILL.md 디렉토리.

```bash
WIKI_ROOT=$(python "<SKILL_DIR>/scripts/resolve_wiki_raw.py" --subdir .)   # 현재 머신의 WIKI 클론 루트 (자동 탐색)
```

| 논리 경로 | 값 | 비고 |
|---|---|---|
| **WIKI_ROOT** | 리졸버 결과 | codegraph `-p` · `.codegraph/codegraph.db` 기준 |
| **RAW_DIR** | `<WIKI_ROOT>/raw` | 입력 |
| **OBSIDIAN_DIR** | `<WIKI_ROOT>/obsidian` | 출력 |
| **ARCHIVE_DIR** | `<WIKI_ROOT>/archive/<YYYY-MM>` | 보관 |
| **FOLLOWUP_DIR** | `<WIKI_ROOT>/.claude/memory-bank/main/follow-up` | 워크플로우 연계 문서 |

- **쓰기 경로 생성**: 컴파일 모드에서 쓰기 직전 `--subdir obsidian|archive|.claude/memory-bank/main/follow-up` 로 호출하면 폴더가 자동 생성된다. **평가 모드(`a`)는 WIKI_ROOT만 쓰고 어떤 폴더도 만들지 않는다**(read-only 불변식 보호).
- **현재 작업 클론이 곧 위키**다(리졸버 cwd 우선). 머신마다 위치가 달라도 remote 신원으로 자동 정착.
- 해석 실패 시에만(예외) 사용자에게 클론 경로 1회 질의 후 `--root <경로>` 재실행. 결과는 `.wiki_root_cache`에 캐시.

## 실행 모드 (2가지)

| 호출 | 모드 | 쓰기 | 동작 |
|---|---|---|---|
| `/compile-wiki` (무인자) | **컴파일** | obsidian 생성·raw 이관 | raw → 원자 노트 빌드 → archive 이관 |
| `/compile-wiki a` | **정합성 평가(입국심사)** | **없음(read-only)** | 스캔 → **기능별 원자 분해** → **원자별** 적합성 심사·보고 (파일 미변경) |

`a` 외에 `audit`·`assess`·`심사`·`fit` 도 평가 모드로 받는다. 평가 모드는 **베이스를 절대 변경하지 않으며**, 어떤 문서를 들일지는 사람이 판단하도록 심사 리포트만 출력한다.

## 볼트 탐색 — CodeGraph 질의 (필수 · Grep/Glob/Read 전수 스캔 대체)

obsidian 볼트의 기존 지식을 탐색할 때 **직접 Grep/Glob/Read 로 볼트를 훑지 않는다.** 대신 wiki 루트 하위 `.codegraph/codegraph.db`(마크다운 지식 그래프 — `doc` 노드 146 + `doc_link` 엣지 = `[[위키링크]]`)에 `codegraph` 커맨드로 질의한다. 링크 후보·중복·충돌·방향성은 모두 이 인덱스에서 끌어온다.

> 아래 모든 `codegraph` 커맨드에는 `-p "<WIKI_ROOT>"`(「위키 위치 해석」에서 확보) 를 붙여 루트를 명시한다(cwd 무관).

| 목적 | 커맨드 | 산출 |
|---|---|---|
| **DB 신선도** (질의 전 필수) | `codegraph status -j` → `pendingChanges` > 0 이면 `codegraph sync` | docsIndexed·edgeCount / 최신화 |
| **개념→노트 검색** (링크 후보·중복 탐지) | `codegraph query "<개념>" -j -l 8` | doc 노드[]: `name`·`filePath`·`score` |
| **백링크** (이 노트를 가리키는 노트) | `codegraph callers "<노트명>" -j` | 역참조 노트 목록 |
| **아웃링크** (이 노트가 가리키는 노트) | `codegraph callees "<노트명>" -j` | 순참조 노트 목록 |
| **이웃군** (중복·충돌 클러스터) | `codegraph impact "<노트명>"` | 연결된 노트 전이 폐포 |

**전체 노트 인벤토리**(방향성 파악용 · 전수 파일 나열 없이 인덱스에서 제목만 — Bash 도구로 실행):

```bash
WIKI_ROOT=$(python "<SKILL_DIR>/scripts/resolve_wiki_raw.py" --subdir .)
node --input-type=module -e "import{DatabaseSync}from'node:sqlite';const db=new DatabaseSync(process.argv[1]+'/.codegraph/codegraph.db',{readOnly:true});for(const r of db.prepare(\"SELECT name FROM nodes WHERE kind='doc' AND file_path LIKE 'obsidian/%' ORDER BY name\").all())console.log(r.name)" "$WIKI_ROOT"
```

원칙:
- **전수 Grep/Glob/Read 금지**: 개념 매칭·중복·충돌·링크 후보 탐색은 위 질의로만 해결한다.
- **타깃 Read만 허용**: query/impact 가 짚은 **특정 노트 1개**를 실제로 확장·병합·충돌통합할 때만 그 파일을 Read 한다(탐색이 아니라 편집 대상 로드).
- **DB 부재 시**: `.codegraph/codegraph.db` 가 없으면 `codegraph init -i -p "<WIKI_ROOT>"` 로 인덱스를 먼저 빌드한 뒤 질의한다.

## 실행 프로토콜 — 컴파일 모드 (`/compile-wiki`, 무인자)

> **인자 분기**: 인자가 `a`(또는 audit·assess·심사·fit)면 아래를 건너뛰고 **「정합성 평가 모드」** 섹션을 실행한다. 무인자면 이 컴파일 프로토콜을 실행한다.

```
WHEN /compile-wiki (무인자) 수신:

[단계 1: 스캔]
1. raw 폴더 존재 확인. 없거나 비어있으면 "처리 대상 없음" 보고 후 중단
2. raw 하위 전체 파일·폴더 목록 수집
   - 사용자가 특정 문서/원자(예: `a` 심사의 승인 원자 ID·제목)를 지정했으면 그 범위만 대상으로 삼는다(나머지는 raw 유지).
   - granularity: atomic 문서는 `### [A#]` 원자 경계를 따라 노트로 분리한다.
3. 링크 후보 풀은 직접 파일 나열 대신 **CodeGraph 질의**로 확보 — 먼저 `codegraph status`(필요 시 `sync`)로 신선도 보장. 전역 후보가 필요하면 「볼트 탐색」의 전체 인벤토리, 개념별 후보는 단계 7의 `codegraph query` 로 끌어온다.

[단계 2: 컴파일 — obsidian 쓰기]
4. raw의 각 입력에서 핵심 개념 추출 → 1개념 1노트 원칙으로 분할
5. 파일명: 명사형 + 언더바 (예: Unity_ECS_동작원리.md)
6. 모든 신규/수정 노트 최상단에 YAML 프론트매터 삽입:
   ---
   tags: [llm-wiki, <분류태그>]
   date_created: <오늘 YYYY-MM-DD>
   last_modified: <오늘 YYYY-MM-DD>
   ---
7. 본문 개념마다 `codegraph query "<개념>"` 로 매칭 노트 탐색 → 히트가 있으면 [[연관_노트]] 링크 삽입. `callers`/`callees` 로 인접 노트까지 링크 후보 확장(Grep 금지)
8. 동일 개념 중복은 `codegraph query` 의 이름·score 로 판정 → 이미 있으면 신규 생성 금지, 해당 노트 1개만 Read 후 확장 + last_modified 갱신
9. 충돌 후보는 `codegraph query`/`impact` 로 관련 노트군을 식별 → 그 노트만 Read 후 "## 논쟁 및 관점 차이" 섹션으로 통합
10. 어떤 노트와도 링크되지 않는 고립 노드 생성 금지 — 최소 1개 이상의 양방향 링크 보장

[단계 3: 아카이브]
11. obsidian에 완벽히 반영된 raw 원본을 archive/<YYYY-MM>/ 로 이동
12. 폴더 계층은 보존 또는 연-월 단위로 격리
13. 컴파일 에러·미완료 파일은 raw에 그대로 남기고 사용자에게 보고

[단계 4: 보고]
14. 신규/수정/이동된 파일 목록 출력
15. 고립 가능성이 의심되는 노트 있으면 경고
16. 워크플로우 연계 팔로우업 요청 — 노드가 변동됐으면(신규/수정 >= 1) claude-personal-integrated-workflow 팔로우업(RIPER 플랜/지시 문서, 구현 규모에 따라) 생성 여부를 사용자에게 묻는다(「워크플로우 연계 팔로우업」절). 승인 시 FOLLOWUP_DIR(<WIKI_ROOT>/.claude/memory-bank/main/follow-up/) 에 작성.
```

## 워크플로우 연계 팔로우업 (노드 변동 후 · claude-personal-integrated-workflow)

컴파일 모드가 **obsidian 노드를 실제로 변동**(신규/수정 노트 ≥ 1)시킨 직후, 그 새 지식이 **가동 중인 개인 통합 워크플로우(claude-personal-integrated-workflow — `.claude/`의 skill·hook·rule·command)**에 반영될 여지가 있는지 사용자에게 확인한다. **위키(지식)와 워크플로우(구현)를 잇는 연결 고리**다.

- **트리거**: 노드 변동 보고(단계 14~15) 직후. 평가 모드(`a`)는 노드를 변동시키지 않으므로 **트리거하지 않는다**.
- **행동**: *"이번 노드 변동을 claude-personal-integrated-workflow에 반영하는 팔로우업 문서를 생성할까요?"* 를 **사용자에게 요청**한다. 생성은 **승인 후에만**(거절 시 미생성 — 노드 변동 자체는 유지).
- **형식은 구현 규모에 따라 유동 결정**:
  - 크거나 구조적(새 skill/hook, 다파일·다단계 구현) → **RIPER 플랜 문서** (Research·Innovate·Plan·Execute·Review 골격, [[RIPER_5단계_상태머신]]).
  - 작거나 국소적(기존 자산 +최소줄) → **지시 문서** (무엇을·어디에·왜 — 체크리스트형).
- **저장 위치**: FOLLOWUP_DIR = `<WIKI_ROOT>/.claude/memory-bank/main/follow-up/<YYYY-MM-DD>_<주제>.md` (`--subdir`가 폴더 자동 생성).
- **재사용 우선**: 팔로우업에 구현 비용·턴당 토큰 Δ를 적되, 신규 자산보다 **기존 skill/hook/rule/command +최소줄** 흡수를 먼저 검토한다([[distill-to-raw]] §6 재사용 경제성과 동일 원칙).

## 정합성 평가 모드 (`/compile-wiki a`) — 입국심사

`a`(또는 audit·assess·심사·fit) 인자가 붙으면 **쓰기 없는 read-only 정합성 평가**만 수행한다. obsidian·archive·raw 그 무엇도 생성·수정·이동·삭제하지 않는다. raw 문서가 지식 베이스에 "입국"할 자격이 있는지 심사하는 단계다.

비유: 공항 입국심사 / 팀-핏 면접 — "이 지식이 우리 베이스의 시민이 될 자격이 있는가?"

```
WHEN /compile-wiki a (또는 audit·assess·심사·fit) 수신:

[심사 1: 스캔 — 컴파일 모드 단계 1과 동일]
1. raw 목록 수집. 비어 있으면 "심사 대상 없음" 보고 후 중단.
2. 베이스의 "지향 방향성"을 **CodeGraph 질의로** 파악(직접 Grep/Read 금지).
   - 「볼트 탐색」 전체 인벤토리(노트 제목 목록) + `codegraph status -j`(docs·doc_link 규모)로 주제 클러스터·무게중심 추론.
   - 허브 노트(`callers`/`callees` 多)와 CLAUDE.md 편집원칙을 합쳐 이 베이스가 "무엇에 관한 곳"인지 추론.

[심사 2: 기능별 원자 분해 — 쓰기 직전까지만]
3. 각 raw 문서를 **기능별 원자 단위로 분해**한다(가상 원자화). 노트로 저장하지 않는다.
   - 원자 = compile 시 1노트가 될 독립·완결 개념. "이 조각만 위키에 넣어도 말이 되는가?"가 기준.
   - distill `a` 가 만든 '원자 구획 문서'(granularity: atomic, `### [A#]`)면 그 구획을 그대로 원자로 채택.
   - 그 외 문서는 여기서 원자 후보로 분해하고, 각 원자에 ID(문서약칭-A#)를 부여한다.

[심사 3: 원자별 정합성 평가 — 5대 기준]
4. **문서 전체가 아니라 각 원자**를 아래 기준으로 판정한다(출처 기준·왜곡 금지):
   - **각 원자는 `codegraph query "<원자 개념>"` 로 기존 노트와 대조**한다 — Novelty·Linkage·Conflict 판정의 근거. 링크 후보·중복/충돌 노트는 query 히트 + `callers`/`callees` 로 수집(obsidian 전수 스캔 금지).
   - 방향성 적합도(Fit): 베이스 지향과 부합하는가? 엉뚱한 주제는 아닌가?
   - 신규성(Novelty): 새로운 지식인가, 기존 노트와 단순 중복인가?
   - 연결성(Linkage): 기존 노트와 [[양방향 링크]] 가능한가? 고립 위험은?
   - 충돌(Conflict): 기존 지식과 모순되는가? (있으면 '논쟁 및 관점 차이' 통합 후보로 표시)
   - 품질·출처(Quality): 정제가 충분하고 provenance 가 명확한가?
   - 원자별로 예상 노트명·링크 후보·중복/충돌 대상을 적는다.

[심사 4: 원자별 판정 — 입국 등급]
5. **원자 단위** 판정(같은 문서라도 원자마다 등급이 갈릴 수 있다):
   - ✅ 승인(APPROVE): compile 가치 충분. 예상 노트·링크 후보 제시.
   - 🟡 조건부(CONDITIONAL): 가치 있으나 보완 필요(인접 원자와 병합·정제 부족·링크 빈약). 조건 명시.
   - ⛔ 보류(HOLD): 방향성 불일치·저품질·무신호. 사유·대안 제시.
   - **목적**: 사용자가 "위키에 넣고 싶은 원자만" 분리·선택할 수 있게 한다.

[심사 5: 원자 단위 보고서 출력 — 파일 미생성]
6. 화면에 **원자 단위** 심사 리포트만 출력한다. 어떤 파일도 쓰지 않는다.
   - 문서별로 묶되 그 아래 **원자별 등급·예상노트·링크·사유**. 충돌·중복 경고.
   - 승인 원자 ID를 따로 모은 **'승인 원자 목록(컴파일 후보)'** 을 제시한다.
   - 마지막: "승인 원자만 골라 무인자 `/compile-wiki` 로 컴파일하세요(원자 ID·제목으로 범위 지정 가능)" 안내.
```

### 심사 보고서 포맷 (예 — 원자 단위)

```
🛂 정합성 심사 (read-only · 베이스 미변경)
지향 방향성(추론): <태그·주제 클러스터 요약>

📄 <raw 파일명 1>  (원자 3개)
  ├ [A1] <원자 제목>  ✅ 승인 | Fit 5 · Novelty 4 · Linkage 5 · Conflict 없음 · Quality 4
  │      예상 [[개념A]](신규) · 링크 [[기존노트X]],[[기존노트Y]] · 사유 <한 줄>
  ├ [A2] <원자 제목>  🟡 조건부 — [[기존노트Z]]와 중복, 병합 권장
  └ [A3] <원자 제목>  ⛔ 보류 — 설치·비용 절차(기반지식), 베이스 부적합

📄 <raw 파일명 2>  (원자 2개)
  ├ [B1] <원자 제목>  ✅ 승인 | ...
  └ [B2] <원자 제목>  ✅ 승인 | ...

── 승인 원자 목록(컴파일 후보) ──
[A1] <제목> · [B1] <제목> · [B2] <제목>

요약: 원자 승인 N · 조건부 M · 보류 K   (문서 X건 → 원자 Y개 심사)
다음: 승인 원자만 무인자 `/compile-wiki` 로 컴파일 (원자 ID·제목으로 범위 지정 가능)
```

### 평가 모드 불변식
- **쓰기 절대 금지**: obsidian·archive·raw 생성·수정·이동·삭제 일절 없음. 순수 판정·보고.
- **원자 단위 심사**: 판정·분리의 최소 단위는 문서가 아니라 **원자**다. 같은 문서의 원자도 등급이 갈릴 수 있고, 사용자가 원자만 골라 들일 수 있게 한다.
- **distill `a` 구획 존중**: granularity: atomic 문서면 그 `### [A#]` 경계를 임의로 다시 쪼개지 말고 그대로 심사 단위로 쓴다.
- **왜곡 금지**: raw 에 있는 내용으로만 평가. 없는 근거로 점수 매기지 않는다.
- **방향성은 추론**: 기존 노트·태그·CLAUDE.md 에서 베이스 지향을 추론하되, 단정이 어려우면 불확실성을 보고에 명시한다.
- **결정은 사람**: 승인/보류는 권고일 뿐, 실제 컴파일 여부·범위는 사용자가 무인자 `/compile-wiki` 로 결정한다.

## 규칙

- **원자성**: 한 노트 한 개념. 복합 개념이 들어오면 분할.
- **양방향 링크**: 새 노트는 최소 1개 이상의 기존 노트와 `[[...]]` 로 연결. 기존 노트에도 역참조 추가.
- **요약·추상화 의무**: raw 원문 복사·붙여넣기 절대 금지. 정제된 핵심만 기록.
- **누적 보존**: 기존 노트 업데이트 시 과거 맥락·타임라인을 파괴적으로 덮어쓰지 않음. 누적·조화.
- **프론트매터 엄격 준수**: 대시 3개 시작/끝, `tags` 리스트 형식, 날짜는 `YYYY-MM-DD`.
- **순수 마크다운**: Dataview·Callout 등 옵시디언 플러그인 전용 문법 과용 금지.
- **불완전 시 raw 유지**: 분석이 덜 끝났거나 에러가 난 파일은 archive로 옮기지 말 것.
- **archive 무결성**: 이동된 원본의 내부 내용은 절대 수정·압축하지 않음.
- **노드 변동 → 워크플로우 팔로우업**: 컴파일로 노드가 변동되면 claude-personal-integrated-workflow 연계 팔로우업(RIPER 플랜/지시 문서, 규모 유동) 생성을 사용자에게 요청한다(「워크플로우 연계 팔로우업」절). 평가 모드(`a`)는 비대상.
- **볼트 탐색은 CodeGraph로**: 개념 매칭·중복·충돌·링크 후보·방향성 탐색은 `.codegraph` 질의(「볼트 탐색」)로만 수행한다. obsidian 전수 Grep/Glob/Read 스캔 금지 — 편집 대상 노트 1개를 로드할 때만 Read.

## 금지 사항

- 독립 노드(orphan note) 생성
- 원본 복사 붙여넣기
- 파괴적 덮어쓰기
- **obsidian 볼트 전수 Grep/Glob/Read 스캔** (CodeGraph 질의로 대체)
- 불완전한 상태로 아카이브 이동
- **평가 모드(`a`)에서 obsidian·archive·raw 의 생성·수정·이동·삭제** (평가는 read-only 보고만)

## 예시

```
사용자: /compile-wiki
Claude: [raw 스캔 → 3개 파일 발견]
        [obsidian 기존 22개 노트 목록 로드]
        [개념 추출 → 5개 신규 노트 생성, 2개 기존 노트 확장]
        [상호 링크 삽입: [[BLK_좌표_시스템]], [[RIPER_5단계_상태머신]] 등]
        [원본 3개 → archive/2026-05/로 이동]
        [보고: 신규 5, 수정 2, 이동 3]
```

## 연계 스킬

- 입력 단계는 [[move-to-raw]] 가 담당. raw에 원본 적재 후 본 스킬 호출이 일반적인 워크플로.
