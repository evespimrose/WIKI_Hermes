---
tags: [llm-wiki, llm-워크플로우, 에이전트, unity]
date_created: 2026-05-22
last_modified: 2026-05-22
---

# Unity 고정 스튜디오 구조

[[3Tier_에이전트_스튜디오]]의 Unity 프로젝트 전용 16개 에이전트 풀세트. Unity 프로젝트로 판정되면 자유 설계 단계(STEP 2)를 건너뛰고 이 구조를 그대로 사용한다.

## Unity 판정 조건

`Packages/manifest.json`이 존재하고 `"com.unity."` 패키지를 포함하면 Unity 프로젝트로 판정한다. 이 단순 검사가 *Tier 3 자유 설계 vs 고정 구조*의 분기점이다.

## 전체 명단 (16개)

### Tier 1 (Opus, maxTurns 30)
- **producer** — 사용자 유일 소통 창구
- **creative-director** — 게임 디자인·UX·내러티브 최종 결정
- **technical-director** — Unity 6/URP 파이프라인·패키지·메모리/프레임 예산

### Tier 2 (Sonnet, maxTurns 25)
- **lead-programmer** — C# 아키텍처 총괄, 2개 이상 서브시스템 연동 시 필수
- **unity-specialist** — 씬·프리팹·ScriptableObject·Editor 확장·메타파일

### Tier 3 (Sonnet, maxTurns 20)
- **quality-sentinel** — 품질 게이트 ([[Producer_QualitySentinel_Reporter_게이트]])
- **reporter** — 작업 기록·동기화 게이트
- **writer** — PRD + RIPER 플랜 작성
- **gameplay-programmer** — Units/Gameloop/Map/Item/Fragments
- **engine-programmer** — PlayerLoop·씬 생명주기·핫 패스·플랫폼 분기
- **systems-designer** — 서브시스템 경계·SO 데이터 모델·이벤트 버스
- **prototyper** — `Assets/Prototypes/` 격리 공간 빠른 검증
- **unity-dots-specialist** — ECS/Burst/Jobs
- **unity-addressables-specialist** — 동적 로딩·CDN·Remote Catalog
- **unity-shader-specialist** — ShaderGraph/HLSL/VFX/URP Renderer Feature
- **unity-ui-specialist** — UGUI/UI Toolkit/Input Action

## 기본 경로 매핑

각 에이전트의 *프로젝트 컨텍스트* 섹션은 STEP 1 분석 결과로 채우되, 기본 매핑은 다음과 같다.

| 에이전트 | 담당 경로 |
|---|---|
| gameplay-programmer | `Assets/Core/Scripts/{Units,Gameloop,Map,Item,Fragments}/` |
| engine-programmer | `Assets/Core/Scripts/{Frame,Objects,Utils}/`, `ProjectSettings/` |
| systems-designer | `docs/design/`, `Assets/Core/Data/`, `Assets/Core/Events/` |
| unity-dots-specialist | DOTS 서브폴더 (manifest `com.unity.entities`) |
| unity-addressables-specialist | Addressables 그룹 (manifest `com.unity.addressables`) |
| unity-shader-specialist | `Assets/Shaders/`, `VFX/`, URP 설정 |
| unity-ui-specialist | `Assets/Core/Scripts/UI/`, UGUI 또는 UI Toolkit |
| prototyper | `Assets/Prototypes/` (없으면 생성) |
| writer | `docs/specs/`, `.claude/memory-bank/{branch}/plans/` |

## 왜 고정 구조인가

Unity 생태계는 패키지·렌더 파이프라인·DOTS 도입 여부·UI 시스템 선택지가 *비교적 좁고 잘 알려져* 있다. 자유 설계의 가치보다 *예측 가능한 협업 경로*의 가치가 크다. 모든 Unity 프로젝트가 같은 16개 에이전트 명단을 갖는다는 규약이 멀티프로젝트 인지 부하를 절감한다.

이는 [[LLM_통제_철학_6대원칙]]의 "Modular Composability"가 *플러그형 자유*가 아닌 *도메인 규약*으로 구현된 사례다.

## 설치 검증 체크리스트 (STEP 6)

16개 파일이 모두 `.claude/agents/` 아래에 존재해야 한다:

```
□ producer  □ creative-director  □ technical-director
□ lead-programmer  □ unity-specialist
□ quality-sentinel  □ reporter  □ writer
□ gameplay-programmer  □ engine-programmer  □ systems-designer
□ prototyper
□ unity-dots-specialist  □ unity-addressables-specialist
□ unity-shader-specialist  □ unity-ui-specialist
□ performance-analyst
```

(performance-analyst 포함 시 17개. 원본 두 raw 문서 간 표기가 16~17개로 흔들리며, 일반 명단에는 16, Unity 고정 목록에는 performance-analyst까지 17 표기.)

## 관련 노트

- 상위: [[3Tier_에이전트_스튜디오]]
- 게이트 3종: [[Producer_QualitySentinel_Reporter_게이트]]
- 라우팅: [[작업_규모별_워크플로]]

## 출처

- raw/generic-3tier-setup-prompt.md (2026-05-22 유입) — Unity 고정 스튜디오 섹션, STEP 1 판정, STEP 3-A 경로 매핑, STEP 6 체크리스트
- raw/ecosystem-atomic-analysis.md (2026-05-22 유입) — §1-B Tier 1·2·3 명단
