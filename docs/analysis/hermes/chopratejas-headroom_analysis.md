# Report — Headroom(chopratejas/headroom) 분석

> 생성일: 2026-06-22
> 대상: https://github.com/chopratejas/headroom (수집 시점: 2026-06-22)
> 조사 범위: GitHub README 전문 ✅ / 핵심 기능·구조·사용법 확인 ✅

## 1. 무엇을 위해 개발되었는가 (목적)

AI 에이전트(Claude Code·Codex·Cursor·Aider 등)가 LLM에 보내는 입력 전에 **tool outputs·logs·RAG chunks·파일·대화 히스토리를 압축**하여, 동일 답변을 60–95% 적은 토큰으로 전달하는 **컨텍스트 압축 레이어**이다.

한 줄 정의: LLM 컨텍스트를 지능형 6-알고리즘 파이프라인으로 압축하는 오픈소스 라이브러리·프록시·MCP 서버.

## 2. 어떻게 달성했는가 (구현)

구조: `ContentRouter → (SmartCrusher | CodeCompressor | Kompress-base) + CacheAligner + CCR`

| 모듈 | 역할 |
|---|---|
| ContentRouter | 콘텐츠 타입 감지 (JSON/code/text/RAG) → 해당 컴프레서 선택 |
| SmartCrusher | JSON 전용 범용 압축 (배열·중첩·혼합 타입) |
| CodeCompressor | AST 인식 Python/JS/Go/Rust/Java/C++ 코드 압축 |
| Kompress-base | HF agentic traces로 학습된 텍스트 압축 모델 |
| CacheAligner | KV-cache 프리픽스 안정화 → 실제 캐시 히트율 향상 |
| CCR | 원본 로컬 저장 + LLM 호출 시 `headroom_retrieve` 로 필요시 복원 |

사용 모드:
- Python/TS 라이브러리
- Proxy (zero-code, `headroom proxy --port 8787`)
- Agent Wrap (`headroom wrap claude/codex/cursor/aider/copilot`)
- MCP Server (`headroom mcp install`, 도구: headroom_compress/headroom_retrieve/headroom_stats)

출력 토큰 절감:
- `HEADROOM_OUTPUT_SHAPER=1` 시 output도 steering
- Verbosity steering + effort routing + per-user learning

## 3. "정말로" 그러한가 (적대적 검증)

**표방대로 작동하는 것:**
- GitHub public repo, 45.2k ⭐, 119명 contributors, 정기 릴리즈(v0.27.0) → 실제 사용 중인 오픈소스 ✅
- 입력 압축 로직은 다수 에이전트 래핑으로 검증 가능 ✅
- Library·Proxy·MCP·Wrap 4가지 진입점 제공 → 사용자 선택의 폭이 넓음 ✅

**표방하나 실제는 다른 것:**

| 주장 | 실제 |
|---|---|
| "60–95% fewer tokens · same answers" | 벤치마크는 GSM8K·TruthfulQA·SQuAD v2·BFCL (일반 NLP). 실제 coding agent의 복잡한 multi-step tool 사용 시나리오에서의 정확도는 명시되지 않음. README의 예시는 cherry-picked 가능성 |
| "Accuracy preserved" | "zero delta or improved scores" 라고 하나, 어떤 모델·어떤 task에서 zero delta 인지 하한 기술하지 않음. 복잡한 코드 추론은 압축으로 손실 위험 |
| "same answers" | "same"은 압축 전 원본을 재호출하지 않는 선에서만 유효 → CCR의 retrieve 메커니즘에 의존. 실제 환경에서 캐시 미스가 자주 나면 원본 접근 비용이 추가되어 순 절감이 줄어듦 |
| "Output shaping" | 기본 OFF, 실험적 기능. 출력 품질 영향은 공개 벤치마크 없음 |

**숨은 전제 / 결론:**
- 압축은 "캐시/원본 보관"이라는 로컬 저장소 비용을 전제로 함. 로컬 디스크·회수 로직이 복잡해지면 시스템 운영 비용이 상승
- 정확도 유지가 벤치마크 의존 → 사용자의 실제 워크플로우(특히 복잡한 코드 생성·디버깅)에서는 품질 저하 가능성을 항상 검증해야 함

## 4. LLM 위키 워크플로우에 무엇을 기여할 수 있는가

`schema/vault_mandate.md` 기준:
- **In-scope 교차점**:
  - `[[압축_안전경계]]`(압축 노드)와 직접 대응 가능 — Headroom은 압축의 실제 구현체이자 "어디까지 압축해도 되는가" 경계의 재검증 사례.
  - `[[doc_context_입력_워크플로우]]`(토큰 통제) — 입력 측 토큰 절감 팁의 구체적 도구 사례로서 가치 있음.
  - `[[Token_허브]]` — 토큰 관리 관점의 오픈소스 참조로 등록 적합.

- **구체적 기여 가능 개념**:
  1. 컨텍스트 압축 계층 아키텍처 패턴 (Router + 다중 compressor + reversible storage)
  2. Agent Wrap 패턴 (에이전트별 1회 명령 래핑)
  3. Output shaper 실험적 기능 (출력 토큰도 steering 가능성)

- **불일치점(out-of-scope 인접)**:
  - Headroom 설치·운용 튜토리얼·Docker 배포·커뮤니티 운영 가이드 → 설치 레시피는 out-of-scope. 아키텍처·패턴만 채택.

- 기여 판정: **개념 추출 조건부** — 압축 아키텍처 패턴과 Agent Wrap 패턴을 추출하면 in-scope. 설치·운용 절차는 보류.

## 5. 핵심 로직 100% 적용 시 턴당 토큰 증가 추정

상시 적용 아님. 특정 Compression 경계 노트 참고용으로만 사용 시:

| 호출 시점 | 스키마·컨텍스트 | 응답 크기 | 베이스 대비 증가 | 결론 |
|---|---|---|---|---|
| 압축 안전경계 노트에 `headroom` 인용 추가 | [[압축_안전경계]] + 5줄 | 0.5컨텍스트 | +5% | 1회성 수정, 턴당 증가 없음 |
| 상시 런타임 주입(예: compression 도구로 매 턴 사용) | full vault mandate + headroom context | 2~3컨텍스트 | +100~150% | 비추천. 상시 주입 대신 필요시 참조로만 사용 |

베이스 가정: Compile-wiki 후 raw/hermes에서 선별된 원자만 노트화. 상시 컨텍스트 주입이 아니라 MCP/툴 호출 시만 사용.

## 6. 기존 자산 재사용 적대 검증 & 구현 경제성

**적대 전제**: "이 원자는 기존 skill/hook/rule/command에 최소 줄만 더하면 흡수된다"를 참으로 가정하고 반증.

| Atom | 최소-diff 재사용 후보 | 추가 LOC | 턴당 토큰 Δ | 구현 비용 | 로드맵 충돌? | 적용 합의점 |
|---|---|---|---|---|---|---|
| 컨텍스트 압축 아키텍처 패턴 (Router+다중compressor) | `obsidian/압축_안전경계.md` +8줄 | +8 | +0% | 낮음 | 무 | 기존 압축 경계 노트에 Headroom 패턴을 "검증된 구현 예시"로 추가 |
| Agent Wrap 1회 래핑 패턴 | `obsidian/doc_context_입력_워크플로우.md` +4줄 | +4 | +0% | 낮음 | 무 | doc_context 노트에 "다중 에이전트 호환 래핑" 사례로 추가 |
| Output shaper 실험 기능 | `obsidian/Token_허브.md` +3줄 | +3 | +0% | 낮음 | 무 | 토큰 허브에 experimental 섹션으로 인용 |
| 전체 Compress-Cache-Retrieve 파이프라인 | 신규 노트 필요 | +30 | +0% | 중 | 비슷한 내용이 Codegraph_MCP_통합.md에 분산 → 신규 대신 분산 통합 권장 | 보류. 기존 Codegraph_MCP_통합.md를 참고 노트로 확장하는 방향으로 대체 |

자산 인벤토리:
- skill: 없음
- rule: vault_mandate.md / scout_lexicon.md
- command: move-to-raw / compile-wiki
- existing note: obsidian/압축_안전경계.md, obsidian/Token_허브.md, obsidian/doc_context_입력_워크플로우.md

## 종합

Headroom은 이 볼트의 토큰 통제 철학과 정면으로 교차하는 실증적 압축 아키텍처다. CacheAligner·CCR·다중 compressor 조합은 **토큰 경제성 패턴**의 구체적 구현 사례로서, `[[압축_안전경계]]` 노트에 +8줄로 흡수 가능하다. Agent Wrap 패턴도 `[[doc_context_입력_워크플로우]]`에 +4줄로 추가 가능. **설치·운용 절차는 out-of-scope로 제외**하고, 아키텍처·패턴·실험적 기능만을 원자 단위로 기여한다.

```

