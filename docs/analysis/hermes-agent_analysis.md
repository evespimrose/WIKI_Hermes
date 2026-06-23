# Report — Hermes Agent (NousResearch) 분석

> 생성일: 2026-06-20
> 대상: https://github.com/nousresearch/hermes-agent (수집 시점: 2026-06-20, ref `main`)
> 조사 범위: README(en/zh/ur) ✅ / providers·middleware·observability 설계 문서 ✅ / 메모리 플러그인 README 8종(honcho·hindsight·holographic·mem0·supermemory·byterover·openviking·retaindb) ✅ / 플랫폼·관측 플러그인(photon·nemo_relay·langfuse·security-guidance·disk-cleanup) ✅ / TUI·web·desktop README ✅ / creative skill README(ascii-video 등) ✅
> **출처 한계(정직성)**: 본 분석은 레포가 노출한 **README/설계 문서 38종(약 240KB)** 을 근거로 한다. `.py` 구현 소스는 수집 번들에 포함되지 않았다(레포 4,895파일 중 문서 계층만 수집됨). 따라서 §3의 "표방 vs 실제"는 *구현 코드 대조*가 아니라 **문서 간 내부 정합성 + 마케팅 문구 대 설계 문서의 괴리**로 수행한다. 코드 레벨 단정은 하지 않는다.

## 1. 무엇을 위해 개발되었는가 (목적)

한 줄 정의: **"써 가며 스스로 학습하는" 메신저 상주형 범용 AI 에이전트 — CLI·게이트웨이(Telegram/Discord/Slack/WhatsApp/Signal)·데스크톱을 한 런타임으로 묶고, 메모리·스킬·관측을 모두 플러그인으로 외부화한 에이전트 프레임워크.**

README가 표방하는 핵심 가치는 세 가지다: (1) **닫힌 학습 루프**(경험에서 스킬 생성, 사용 중 스킬 자가 개선, 메모리 넛지, 과거 세션 검색, 세션 간 사용자 모델 심화), (2) **장소 비종속**(노트북이 아닌 $5 VPS/서버리스에서 상주, 메신저로 호출), (3) **모델·도구 비종속**(OpenRouter·Nous Portal 등 임의 프로바이더, 임의 MCP). 타깃은 "나를 점점 알아가는 24시간 개인 에이전트"를 원하는 개인 사용자 + 트래젝토리 생성·압축을 원하는 연구자다.

계보상 **OpenClaw의 포크·리브랜드**다(`hermes claw migrate`가 `~/.openclaw`의 `SOUL.md`·`MEMORY.md`·`USER.md`·스킬·허용목록·API키를 이식). "Nous Research가 만든 자가개선 에이전트"라는 정체성은 일부 선행 에이전트(OpenClaw) 설계 위에 서 있다.

## 2. 어떻게 달성했는가 (구현)

진입점은 두 개 — 터미널 UI(`hermes`)와 게이트웨이 프로세스(`hermes gateway`)이며, 둘 다 동일한 Python 코어(세션·도구·모델호출·커맨드)를 구동한다. 설계 문서가 드러내는 핵심 골격:

- **플러그인 확장면 2종 분리(핵심)**: `docs/observability`(관측 훅, 읽기 전용 텔레메트리)와 `docs/middleware`(미들웨어, 동작 변경). 관측 훅은 "무슨 일이 일어났는가"를 보고만 하고, 미들웨어는 "무슨 일이 일어날지"를 바꾼다(요청 재작성·실행 콜백 래핑). 둘 다 `register(ctx)`에서 등록, 스키마 버전(`hermes.observer.v1`/`hermes.middleware.v1`)으로 계약화, **fail-open**(콜백 예외는 경고 후 계속).
- **상관 ID 체계**: `session_id`·`task_id`·`turn_id`·`api_request_id`·`tool_call_id` + 서브에이전트 `parent/child_session_id`로 중첩 트래젝토리를 콜백 순서 의존 없이 조인.
- **프로바이더 레지스트리**: 프로바이더를 `ProviderProfile` 데이터클래스 1곳에 선언하면 auth·models·doctor·config·transport가 전부 레지스트리에서 읽는다. 신규 프로바이더 추가 = `plugins/model-providers/<name>/` 디렉터리 1개. 사용자 플러그인이 동명 번들을 덮어쓴다(last-writer-wins).
- **메모리 추상화**: 단일 인터페이스 뒤에 8개 백엔드(로컬 SQLite/FTS5 `holographic`부터 클라우드 `honcho`·`hindsight`·`mem0`·`supermemory`까지). `memory_mode`는 `hybrid`(자동주입+도구)/`context`(주입만)/`tools`(도구만) 3종. auto-recall/auto-retain 케이던스로 턴당 비용을 조절.
- **컨텍스트 주입 위치(honcho 사례)**: 메모리를 **시스템 프롬프트가 아니라 user 메시지에 API 호출 시점 주입**하고 `<memory-context>` 펜스로 감싸 "배경 데이터"임을 명시 — **프롬프트 캐시 보존**이 명시적 설계 의도. 시스템 프롬프트에는 정적 헤더만. 다음 턴 입력에서 누출된 `<memory-context>` 블록은 재처리 전 sanitize.
- **트래젝토리 관측(nemo_relay)**: 동일 관측 훅을 NVIDIA NeMo Relay 스코프/스팬으로 매핑하고 ATOF(JSONL 이벤트 스트림)→ATIF(트래젝토리 교환 포맷, 서브에이전트를 중첩 트래젝토리로 임베드)로 내보내 replay·평가·학습용 데이터화.
- **보안 가드(security-guidance)**: `write_file`/`patch` 내용이 위험 패턴(eval·pickle.load·shell=True·dangerouslySetInnerHTML·`torch.load(weights_only 누락)` 등 25룰)에 매치되면 도구 결과에 경고를 append. **파일은 그대로 쓰이고**, 모델이 다음 턴에 보고 스스로 고친다. 로컬 정규식 = **LLM 토큰 0**. Anthropic `claude-plugins-official`의 패턴을 Apache-2.0로 포크.

## 3. "정말로" 그러한가 (적대적 검증)

문서 계층만 본 한계 안에서, 마케팅 문구(README 상단)와 설계 문서의 정합을 대조한다.

**문서로 뒷받침되는 것:**
- 미들웨어/관측 훅의 계약·실행순서·fail-open 의미론은 설계 문서에 구체적으로 명세됨 ✅
- 프로바이더 레지스트리의 "1파일 추가" 확장성은 `plugins/model-providers/README`의 예제로 확인 ✅
- honcho의 "캐시 보존을 위한 user-메시지 주입"은 설계 의도로 명시됨 ✅
- 보안 가드의 "warn-by-default, 파일은 쓰임, 토큰 0"은 README에 명시 ✅

**표방하나 (문서 근거가) 다른/약한 것:**

| 주장 | 실제(문서 기준) |
|---|---|
| "the **only** agent with a built-in learning loop" | 검증 불가한 최상급 마케팅. 동류 에이전트(OpenClaw 포함)도 유사 메모리/스킬을 가짐. 배타성 주장은 근거 없음 |
| "self-improving / 닫힌 학습 루프" | 학습의 실체 대부분이 **외부 메모리 SaaS 플러그인**(honcho·hindsight·mem0·supermemory — 다수가 유료 클라우드)으로 위임됨. 자체 학습 알고리즘이 아니라 "스킬 파일화 + 외부 메모리 추출/재주입 + 주기적 넛지"의 조합. 신규성은 *통합*에 있지 *학습 메커니즘*에 있지 않음 |
| "Nous Research가 만든" 신규 에이전트 | 상당 부분이 **OpenClaw 포크**(migrate가 SOUL/MEMORY/USER.md를 그대로 이식). 정체성·파일 규약이 선행 에이전트 계승 |
| 보안 가드가 코드를 안전하게 함 | README 스스로 인정: "best-effort, 오탐 mediocre, SAST·리뷰 대체 아님". layer 2·3(LLM diff 리뷰·커밋 리뷰)은 **비용 때문에 미포팅** |
| "research-ready 트래젝토리" | ATOF/ATIF는 NeMo Relay 런타임 설치를 전제(`nemo-relay` 미설치 시 fail-open으로 무동작). 기본 동작이 아니라 옵트인 통합 |

**숨은 전제 / 결론:** Hermes의 실제 엔지니어링 가치는 "자가학습"이라는 서사가 아니라 **확장면을 깨끗이 분리한 플러그인 아키텍처**(관측↔미들웨어, 프로바이더 레지스트리, 메모리 추상화)와 **프롬프트-캐시를 의식한 컨텍스트 주입 규율**에 있다. "self-improving"은 다수의 외부 메모리/스킬 서비스를 한 런타임으로 *통합*한 결과의 마케팅 명명이다. 즉, **가치는 통합 레이어 설계에서 오지, 새로운 학습 알고리즘에서 오지 않는다.** (이 결론은 본 볼트의 기존 Hermes 유튜브 raw가 강조한 "통합 레이어 전략"과도 일치.)

## 4. LLM 위키 워크플로우에 무엇을 기여할 수 있는가

> 주: 이 볼트에 `schema/vault_mandate.md`는 실재하지 않아, 기존 `docs/analysis/*`(superclaude·claudecode_skill_seminar·sequentialthinking)와 입국심사 노트들이 드러내는 **북극성 — "LLM/AI 에이전트 결정론적 통제 + 워크플로우 엔지니어링 + 메모리 외재화 + 토큰 통제"** 를 기준으로 심사한다.

**In-scope 교차점:**
- **훅 통제 철학** — 관측↔미들웨어 분리("보고" vs "변경")는 [[LLM_통제_철학_6대원칙]]의 "훅 > 프롬프트" 원칙과 정면 대응. 이 볼트의 PreToolUse 차단 훅(sonar-guard·codegraph-gate)·Stop 훅과 같은 계열의 *형식화된 계약*.
- **프롬프트 캐시 규율** — honcho의 "메모리를 user 메시지에 주입, 시스템 프롬프트 불변 유지"는 본 볼트의 캐시 안정성 강박(cache-aligner 스킬·session-start 불변 prefix 규율)과 **직접 대응**하는 외부 실증 사례.
- **메모리 외재화** — `memory_mode`(hybrid/context/tools)·다단 케이던스·"observations(통합 신념) vs raw facts(원증거)"는 [[4계층_메모리_아키텍처]]·[[위키_저장_5대필터]]의 "원자적·통합된 지식" 철학과 교차.
- **토큰 경제학** — Tool Search(BM25 지연-도구 브리지)·케이던스 기반 비용 통제·"관측 페이로드는 훅 있을 때만 구성"은 [[맥락_오염_방지]]의 토큰 footprint 통제와 연결.
- **자가학습 스킬 루프** — "결과물 → SKILL.md 자가생성 → 피드백 개선"은 [[Agent_Skill_Orchestrator_3요소]] 및 **기존 raw `헤르메스_에이전트_자가학습_설치활용__yt_wiVd1CwfBls.md`** 와 부분 중복(아래 불일치점 참조).

**구체적 기여 가능 개념:**
1. **관측 vs 미들웨어 2면 분리** — 에이전트 확장면을 "읽기전용 텔레메트리"와 "동작변경 래퍼"로 가르는 계약 패턴(fail-open·스키마버전·상관ID).
2. **캐시 보존형 컨텍스트 주입** — 가변 메모리는 user 메시지에, 시스템 프롬프트는 불변. `<memory-context>` 펜스 + 입력 sanitize.
3. **observations vs raw facts** — 주입은 통합·중복제거된 신념(증거수·신선도 포함)을, 원증거는 별도. 토큰당 밀도 우선.
4. **layer-1 패턴 가드** — 토큰 0의 로컬 정규식이 도구 결과에 경고 append, 파일은 쓰이고 모델이 다음 턴 자가수정. 경로필터·lookbehind로 오탐 저감.

**불일치점(out-of-scope 인접):**
- 설치·배포 절차(Railway·install.sh·OpenRouter/Telegram 세팅) → mandate의 "설치 튜토리얼" 경계. **이미 기존 Hermes 유튜브 raw가 이 영역을 덮음** → 신규 노트 금지, 중복.
- 메신저 플랫폼 배관(Photon/iMessage 사이드카·Matrix·google_meet), creative 스킬(ascii-video·manim·p5js·comfyui) → 제품 레시피, off-axis.
- 도구·제품 자체 도입 → 이 볼트는 자체 워크플로우(RIPER·codegraph·훅)를 이미 보유, 중복.

**기여 판정: 개념 추출 조건부 채택** — 도구·제품이 아니라 **4개 설계 패턴(§4 구체 1–4)** 이 볼트에 편입 가능. 1·2·4는 기존 노트 확장이 적합, 3은 메모리 노트 보강.

## 5. 핵심 로직 100% 적용 시 턴당 토큰 증가 추정

**상시 적용 여부:** 채택 후보 4패턴은 모두 *개념 노트*로 추출 시 **런타임 +0%**(설계 학습일 뿐 도구 미도입). 단, 일부를 실제 메커니즘으로 도입할 경우의 비용을 분리 추정한다.

| 패턴 | 채택 형태 | 턴당 토큰 영향(베이스 20K 가정) |
|---|---|---|
| 관측↔미들웨어 분리 | 개념 노트 | +0% (이미 이 볼트의 훅이 동형) |
| 캐시 보존형 주입 | 개념 노트 / 규율 채택 | +0% — 오히려 **캐시 적중률↑로 비용 절감** 방향 |
| observations vs raw | 메모리 노트 보강 | +0% (개념). 실제 주입 메커니즘화 시 통합신념 주입이 raw 대비 **토큰 절감** |
| layer-1 패턴 가드 | 개념/경량 훅 | +0% LLM 토큰(로컬 정규식). 경고 append 시 도구결과 +수십 토큰/매치 |

**결론:** `+0%` (4패턴 모두 개념 추출). 본 볼트의 토큰 강박과 **상충하지 않으며**, 특히 "캐시 보존형 주입"과 "observations 우선"은 *비용 절감 방향*의 외부 실증이다. 도구·제품 자체 도입은 OpenClaw 포크 + 외부 SaaS 의존이라 부적합(중복·고정비용).

## 종합

Hermes Agent는 "자가학습"이라는 서사로 포장됐지만, 문서 계층이 드러내는 실체는 **확장면을 깨끗이 분리한 플러그인 에이전트 프레임워크**(관측 vs 미들웨어, 프로바이더 레지스트리, 8백엔드 메모리 추상화)와 **프롬프트-캐시를 의식한 컨텍스트 주입 규율**이다. 학습 루프 자체는 외부 메모리 SaaS와 스킬 파일화의 *통합*이지 신규 알고리즘이 아니며(OpenClaw 포크 계보), 이는 본 볼트 기존 Hermes 유튜브 raw의 "통합 레이어" 관점과 일치한다. 채택 조건: **제품이 아닌 4개 설계 패턴**(관측/미들웨어 분리, 캐시 보존형 주입, observations vs raw, layer-1 패턴 가드)만 개념 노트로 추출 — 모두 런타임 +0%이며 일부는 캐시·토큰 비용을 *낮추는* 외부 실증. 설치·운용·메신저 배관·creative 스킬은 out-of-scope이며 설치 영역은 기존 유튜브 raw와 중복이므로 **compile 시 두 문서를 함께 정합**해야 한다.
