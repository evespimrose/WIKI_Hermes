# Report — SuperClaude Framework 분석

> 생성일: 2026-06-20
> 대상: https://github.com/SuperClaude-Org/SuperClaude_Framework (clone/수집 시점: 2026-06-20, v4.3.0 / master)
> 조사 범위: README(en·ja·kr·zh) ✅ / developer-guide·memory·reference README ✅ / `src/superclaude/cli/main.py` ✅ / SKILL.md 6종(confidence-check·brainstorm·deep-research·pm·token-efficiency·troubleshoot) ✅ / CLAUDE.md·AGENTS.md ✅ / pyproject.toml·package.json·.mcp.json ✅ / PROJECT_INDEX(json·md) ✅ / CHANGELOG ✅

## 1. 무엇을 위해 개발되었는가 (목적)

한 줄 정의: **Claude Code를 "구조화된 개발 플랫폼"으로 바꾸기 위해, 행동 지시를 담은 `.md` 문서(커맨드·에이전트·모드·스킬)를 `~/.claude/`에 주입하는 메타프로그래밍 설정 프레임워크.**

타깃은 Claude Code 사용자이며, 핵심 가치 표방은 "행동 지시 주입(behavioral instruction injection)과 컴포넌트 통제를 통해 체계적 워크플로우 자동화를 제공"이다. 스타 23.3k, MIT, 저자 3인(Kazuki Nakai·NomenAK·Mithun Gowda B), 배포는 PyPI(`superclaude`) + npm 래퍼(`@bifrost_inc/superclaude`). README 첫머리에 **"Anthropic과 무관·비승인"** 면책을 명시한다.

표방 통계(README): **커맨드 30 · 에이전트 16 · 모드 7 · MCP 서버 8.** (단, 문서마다 수치가 다르다 — §3 참조.)

## 2. 어떻게 달성했는가 (구현)

**두 층위로 구성된다.** (a) Claude Code가 읽는 `.md` 지시 문서 묶음, (b) 그 묶음을 설치·검증하는 얇은 Python 패키지(pytest 플러그인).

**진입점 → 핵심 모듈 흐름:**

- `src/superclaude/cli/main.py` — Click 기반 CLI. 서브커맨드: `install`(커맨드·에이전트를 `~/.claude/commands/sc/`·`~/.claude/agents/`로 복사), `mcp`(MCP 서버 설치), `update`, `install_skill`, `doctor`, `version`. **CLI는 파일 복사·헬스체크만 한다 — 워크플로우 로직은 들어있지 않다.**
- `pyproject.toml` — 두 엔트리포인트: `superclaude` CLI + **pytest11 자동 로드 플러그인**(`superclaude.pytest_plugin`). 즉 설치 즉시 pytest에 픽스처/마커가 붙는다.
- `src/superclaude/pm_agent/` — **PM Agent 3대 패턴**(실제 Python):
  - `confidence.py` `ConfidenceChecker` — 착수 전 신뢰도 5항목 가중 평가(중복없음 25% · 아키텍처 부합 25% · 공식문서 확인 20% · OSS 참조 15% · 근본원인 15%). ≥90% 진행 / 70–89% 대안제시 / <70% 질문. ROI 표방 25–250×(100–200토큰 써서 5K–50K 절감).
  - `self_check.py` `SelfCheckProtocol` — 구현 후 증거기반 검증. **Assert → Verify → Report.**
  - `reflexion.py` `ReflexionPattern` — 교차세션 오류 학습·패턴 매칭.
  - `token_budget.py` — 복잡도별 토큰 예산: simple 200 / medium 1,000 / complex 2,500.
- `src/superclaude/execution/` — `parallel.py`(**Wave → Checkpoint → Wave**, 3.5× 표방), `reflection.py`, `self_correction.py`.
- `docs/memory/` — **ReflexionMemory** 데이터 저장소. `reflexion.jsonl`(JSON Lines)에 `{ts, task, mistake, evidence, rule, fix, tests, status}` 형식으로 과거 오류·근본원인·해결을 누적. `workflow_metrics.jsonl`(토큰·시간·성공률), `patterns_learned.jsonl`. 검색 <10ms(<1MB).
- `plugins/superclaude/skills/*/SKILL.md` — 7개 스킬. YAML frontmatter(`name`+`description`로 자동 트리거) + 본문(행동 프로토콜) + `Apply this to: $ARGUMENTS`로 끝. 매우 얇다(681B~3.4KB).
- `plugins/superclaude/.mcp.json` — **실제 동봉 MCP는 context7 + sequential-thinking 2종뿐.** 나머지 6종(Tavily·Serena·Mindbase·Playwright·Magic·Chrome DevTools)은 외부 `airis-mcp-gateway`(Docker) 경유.

**제어 흐름의 본질:** 설치 = `.md` 복사. 런타임 동작 = Claude Code가 그 `.md`를 읽고 행동을 바꾸는 것. Python 코드(PM Agent·execution)는 대부분 **pytest 픽스처/마커**로서 테스트 시점에 동작하며, 대화 턴마다 실행되는 엔진이 아니다.

## 3. "정말로" 그러한가 (적대적 검증)

**표방대로 작동하는 것 (코드로 확인):**
- pytest 플러그인 자동 로드 — `pyproject.toml` `[project.entry-points.pytest11]` ✅
- PM Agent 3패턴이 실제 Python 모듈로 존재 ✅ (v4.3.0부터 — 단서는 아래)
- ReflexionMemory의 JSONL 스키마·검색은 실재 ✅
- CLI 설치/닥터 동작 ✅

**표방하나 실제는 다른 것:**

| 주장 | 실제 |
|---|---|
| "Claude Code를 **구조화 개발 플랫폼으로 변환**(2–3× 빠름·30–50% 토큰 절감)" | developer-guide README가 **스스로 부정**: *"SuperClaude is NOT a CLI tool or executable software… ❌ Not Software ❌ Not Testable ❌ Not Optimizable ❌ Not Persistent."* `/sc:` 은 터미널 명령이 아닌 "context trigger pattern". 성능 수치는 SuperClaude가 아니라 **제3자 MCP(Serena·Sequential)를 airis-gateway로 붙였을 때**의 값. |
| "30개 커맨드" | pip 패키지가 실제 설치하는 커맨드는 `agent·index-repo·recommend·research·sc` **5개**(README 설치 안내 + `src/superclaude/commands/README.md`). 30은 아직 **미출시** 플러그인(v5.0 #419) 기준 카운트. |
| "16 에이전트"(README 통계) | CLAUDE.md·plugin README는 **20**, 구버전은 14. CHANGELOG 4.3.0이 자인: *"Feature counts — Commands 21→30, Agents 14/16→20, Modes 6→7, MCP 6→8."* 수치 자체가 문서 간 표류. |
| confidence-check "Precision 1.000 / Recall 1.000 / 8-of-8"(2025-10-21) | CHANGELOG 4.3.0(2026-03-22): *"ConfidenceChecker placeholders — Replaced **4 stub methods** with real implementations."* 즉 그 100% 주장 시점엔 5항목 중 **4개가 스텁**. 표본도 8케이스. |
| "프로덕션 검증된 안전한 프레임워크" | CHANGELOG 4.3.0: *"SECURITY: shell=True removal"* — 2026-03-22까지 셸 인젝션 벡터 존재. 같은 릴리스에서 `intelligent_execute()`의 변수 섀도잉 버그(루프변수가 task 파라미터 덮어씀)도 수정. `__version__` 0.4.0 ↔ 패키지 4.3.0 불일치도 그때 동기화. |

**숨은 전제:** 이 프레임워크가 유용하려면 LLM이 주입된 `.md` 지시를 충실히 따라야 한다. 구조화 이점은 **실행 소프트웨어가 아니라 LLM의 반응 방식**에서 온다 — [[Codegraph_MCP_통합]] 분석과 동일한 결론. 실제 코드가 있는 곳(pytest 플러그인·PM Agent 헬퍼)조차 얇은 스캐폴딩이다.

**결론:** SuperClaude는 본질적으로 **컨텍스트 주입식 행동 프로그래밍**이며, 그 점을 개발자 문서에서 자인한다. 마케팅 README의 성능·규모 주장과 개발자 문서의 자기부정 사이에 **내적 모순**이 있고, 출시본이 표방 규모(30/20/8)의 일부만 담는다. 가져올 가치는 *제품*이 아니라 **몇 개의 설계 패턴**과 **오버셀 반례 그 자체**다.

## 4. LLM 위키 워크플로우에 무엇을 기여할 수 있는가

`schema/vault_mandate.md` 기준. 볼트 대조는 codegraph 질의로 확인(Grep/Read 미사용).

**In-scope 교차점 (codegraph 히트로 검증):**
- **ReflexionMemory(교차세션 실패학습)** ↔ [[4계층_메모리_아키텍처]] — 볼트는 memory:save/recall·feedback 메모리는 있으나 `mistake→evidence→rule→fix→prevention`의 **구조화된 실패학습 루프가 없다**. 신규 기여.
- **ConfidenceChecker(점수화 사전 게이트)** ↔ [[작업_규모별_워크플로]] / [[L1_Hard_Gate_훅체계]] — 볼트 게이트는 *탐색 오용을 훅으로 결정론 차단*. 이쪽은 *착수 전 의미론적 준비도 점수*라는 다른 축. 단 [[LLM_통제_철학_6대원칙]] 원칙3(훅>프롬프트)과 긴장: 자가평가 점수는 프롬프트급이라 통제력이 약하다.
- **SelfCheckProtocol(Assert→Verify→Report)** ↔ [[증거_기반_완료_검증]] — **거의 동일**(Evidence-First Verification). 이미 보유.
- **PROJECT_INDEX(인덱스=컨텍스트, 94% 절감 표방)** ↔ [[Codegraph_MCP_통합]] — 중복. 볼트의 codegraph(tree-sitter 심볼 그래프)가 정적 JSON보다 우월. 이미 보유·상위호환.
- **Token Budget 티어(200/1000/2500)** ↔ [[작업_규모별_워크플로]] — 부분 중복. 명시적 *턴당 토큰 예산 배정* 개념만 소폭 신규.
- **Deep Research(멀티홉 ≤5 + 품질 스코어링 0.0–1.0, 최소 0.6/목표 0.8)** ↔ mandate 갭 Priority 3 *"웹링크 지식 정제 자동화(Hermes)"* — 정제 파이프라인에 붙일 수 있는 **구체적 신뢰도 채점 루브릭**. 갭 충전형.
- **"설정은 소프트웨어가 아니다" 자기선언** ↔ [[Agent_Skill_Orchestrator_3요소]] / [[하네스_엔지니어링]] / [[프롬프트_컨텍스트_하네스_패러다임]] — Agent=자연어 문서라는 볼트 명제의 강한 외부 방증.

**불일치점 (out-of-scope 인접 / 충돌):**
- pipx·install.sh·airis-gateway(Docker) 설치 절차 → mandate "설치 튜토리얼" 경계.
- **Wave→Checkpoint→Wave 병렬(3.5×)** → 볼트 Output Arm(CLAUDE.md RULE-9)의 **서브에이전트 디스패치 금지**(콜드스타트 ~100× 토큰세)와 정면 충돌. 채용 아닌 *논쟁/경고* 소재.
- 마케팅 vs 실제 괴리(성능 출처 전가·규모 인플레)는 그 자체가 볼트의 정직한 토큰 회계 윤리에 대한 **반면교사**.

**기여 판정: 개념 추출 조건부.** 도구 전체 도입은 비추천(볼트에 더 결정론적인 등가물 다수 존재). 채용 가치 있는 것은 (1) Reflexion 실패학습 루프, (2) Deep Research 품질 채점, (3) "설정≠소프트웨어" 방증, (4) 오버셀 경고 사례 — 모두 **개념 노트(런타임 +0%)**.

## 5. 핵심 로직 100% 적용 시 턴당 토큰 증가 추정

**상시 적용 여부:** PM Agent 로직(confidence/self-check/reflexion)은 **pytest 픽스처** — 테스트 시점 실행이라 대화 턴 비용 ≈ 0. 대화 턴에 상주하는 것은 (a) 스킬 frontmatter(자동 트리거 description), (b) 등록된 MCP 스키마, (c) 호출된 `/sc:` 커맨드/`@agent` 문서다.

**비용 추정 (베이스 가정: RIPER 1턴 ≈ 20,000토큰):**

| 항목 | 토큰 | 조건 |
|---|---|---|
| 스킬 7종 frontmatter(자동 트리거 노출) | ~350 | 상시 |
| 동봉 MCP 2종(context7+sequential) 스키마 | ~600–900 | 상시(등록 시) |
| `/sc:` 커맨드 1개 로드 | ~500–2,000 | 호출 턴 1회 |
| `@agent` 디스패치 | **서브에이전트 콜드스타트(별도 컨텍스트, 수천+)** | 디스패치 시 |
| confidence check 실행 | ~100–200 | 착수 전 1회 |

**증가 추정:**
- 개념만 추출(노트화): **+0%** — 런타임 도구 미도입.
- 스킬+MCP 상시 등록: **약 +5~7%**(~1,000–1,300/20K).
- `@agent` 적극 사용 시: 콜드스타트 비용이 지배적 — Output Arm이 금지하는 바로 그 비용.

**결론:** `개념 추출 +0% ~ 도구 상시화 +5–7% ~ 에이전트 디스패치 적극화 시 그 이상`. 볼트의 토큰 강박(−62% 최적화 역사)과 anti-subagent 정책을 감안하면 **도구 전면 도입은 부적합**하고, 비용이 0인 설계 패턴만 선택 차용하는 것이 유일하게 정당화된다.

## 종합

SuperClaude Framework는 `.md` 지시 주입으로 Claude Code의 행동을 재프로그래밍하는 대형(23k★) 메타 프레임워크로, 그 정체를 개발자 문서에서 "소프트웨어가 아니다"라고 자인한다. 마케팅(2–3×·30커맨드·100% 정밀도)과 실제(성능은 제3자 MCP 몫·출시본 5커맨드·v4.3.0 전까지 4개 스텁) 사이의 괴리가 뚜렷하다. 볼트엔 이미 RIPER·Output Arm·codegraph·3-Tier 스튜디오·증거기반 검증이라는 더 결정론적인 등가물이 있어 **도구 도입은 중복**이다. 채택 조건: 도구 전체가 아닌 **(1) Reflexion 교차세션 실패학습 루프(신규·최고가치), (2) Deep Research 품질 채점 루브릭(Hermes 갭 충전), (3) "설정≠소프트웨어" 외부 방증, (4) 프레임워크 오버셀 경고 사례** — 4개를 개념 노트로 추출(런타임 +0%). Confidence 게이트는 훅>프롬프트 긴장을 명시한 논쟁 노트로, Wave 병렬은 anti-subagent 충돌 경고로 위치시킨다.
