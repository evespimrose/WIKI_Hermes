---
tags: [llm-wiki, llm-워크플로우, 에이전트]
date_created: 2026-05-22
last_modified: 2026-06-17
---

# Producer · Quality-Sentinel · Reporter — 3대 고정 게이트

[[3Tier_에이전트_스튜디오]]의 7개 고정 에이전트 중 *흐름 게이트* 역할을 맡는 세 에이전트. 모든 구현 작업은 이 셋의 체인을 순차 통과해야 conclusion에 도달한다.

```
구현 에이전트 → quality-sentinel → reporter → producer.conclusion
```

세 자리가 모두 [[LLM_통제_철학_6대원칙]]의 "Single Responsibility per Role"의 가장 엄격한 적용 대상이다.

## Producer (Tier 1, Opus) — 멀티에이전트 조율 허브

### 단일 책임

사용자의 *유일한* 소통 창구. 중형 이상 작업의 결재·조율·conclusion 작성.

### Triage 플로우

```
요청 수신
  ├ 소형 (단일 함수·버그픽스·플랜 없음) → 전문가 안내 후 종료
  └ 중형 이상 → 위임 계획 수립 → 사용자 승인 → 위임
```

### 결재 요청 양식

```markdown
## 결재 요청: [주제]
배경 / 옵션 A·B / 권고 / 영향 에이전트 / 결재 후 진행
```

### Conclusion.md 양식

```markdown
# Conclusion: [작업명]
날짜 / 브랜치 / 관련 에이전트 / 완료 항목 / 주요 결정 이력
/ 생성된 파일·변경사항 / 미해결 항목·다음 세션 인계사항
```

### 절대 금지

- quality-sentinel all-pass 없이 conclusion.md 작성 또는 다음 단계 진행
- 소형 작업에 대해 자기 자신을 경유시키는 형식주의

## Quality-Sentinel (Tier 3, Sonnet) — 품질 게이트

### 단일 책임

구현 에이전트 작업 완료 직후 두 가지를 순차 검증: **(1) [[RIPER_5단계_상태머신]] 워크플로 순서 준수**, **(2) 코드 컨벤션 all-pass**까지 반복 검증.

### 3-Phase 워크플로

**Phase 1 — RIPER 감사**
- `.claude/memory-bank/{branch}/plans/`에서 작업 플랜 로드
- Plan→Execute→Review 순서 준수 확인
- 위반 발견 시 producer 보고, 통과 시 Phase 2
- 소형 작업(플랜 없음)은 Phase 1 생략

**Phase 2 — 코드 컨벤션 검증 루프**
```
git diff HEAD로 변경 파일 추출 (전체 파일 읽기 금지)
  → /code-review 실행
  → all-pass: Phase 3
  → 위반: 원인 에이전트 피드백 → 재작업 → 루프 재시작
  → 3회 실패 시 producer 에스컬레이션
```

**Phase 3 — Producer 보고**
- 통과/차단 보고서를 양식대로 작성

### 토큰 절약 제약

검증 대상 파일을 *통째로 읽지 않는다*. 오직 `git diff HEAD`만 사용. [[LLM_통제_철학_6대원칙]]의 "Tokens are First-Class Resources" 원칙의 가장 강한 적용 사례.

### 절대 금지

- 코드 직접 수정 (피드백만, 수정은 원인 에이전트)
- RIPER 위반을 사용자 모르게 통과 처리
- 3회 실패 후 자의적 통과 처리 (반드시 에스컬레이션)
- 코드 변경 없는 작업(설계 문서·README 등)에 개입
- 플랜 없는 소형 작업에 RIPER 위반 판정

## Reporter (Tier 3, Sonnet) — 기록·동기화 게이트

### 단일 책임

quality-sentinel all-pass 직후 호출. 기록·플랜·스펙 동기화 4종을 처리.

### 매 호출 워크플로

1. 컨텍스트 수집 — 직전 완료 작업 파악
2. `work.md` 기록 — Entry 번호 확인 후 새 Entry 작성
3. 플랜 영향 체크 — PRD·플랜 관련 서브시스템 영향 판단
4. `update-queue` 기록 — 영향 있으면 큐에 항목 추가
5. 큐 순회·승인 — 자체 승인 가능 항목 Approved 처리 후 PRD 반영
6. 연관 스펙 갱신 — Workflow/Setting/Review 반영
7. Producer 보고

### Entry 번호 산출 제약

`grep -c "^## Entry" docs/work.md`로만 번호를 확인. *work.md 전체 읽기 금지* — 누적 파일은 수만 토큰. 이 또한 토큰 자원 원칙의 적용.

### 큐 항목 자체 승인 기준

자체 승인 가능 (전부 충족):
- 코드에 이미 구현 완료
- PRD와 논리적 일관 (충돌 없음)
- 사용자가 직접 지시 또는 묵시적 승인

반드시 에스컬레이션 (하나라도 해당):
- PRD 핵심 목표(Goal/G-번호) 변경
- 기존 사용자 결재 번복
- 영향 범위가 PRD 섹션 3개 이상
- 구현 미완료 상태

### 절대 금지

- 코드 파일(.cs, .shader 등) 직접 수정
- 아키텍처·설계 결정 독단 수행
- 승인 기준 불명확 항목을 사용자 결재 없이 PRD 반영
- quality-sentinel 통과 전 호출
- work.md Entry 번호를 파일 읽기 없이 추정

## 세 게이트의 직렬화가 가지는 의미

직렬 체인은 *각 게이트의 통과 사실*을 다음 게이트의 호출 조건으로 못박는다. 이는 [[LLM_통제_철학_6대원칙]]의 "Hooks > Prompts"의 에이전트 버전이다 — 게이트 통과 여부를 프롬프트가 아니라 *호출 그래프 구조*로 강제한다. 한 게이트가 sloppy하게 통과되면 다음 게이트가 그 결과를 사용할 수 없게 만드는 것이 설계 의도다.

## 관련 노트

- 전체 구조: [[3Tier_에이전트_스튜디오]]
- RIPER 감사 대상: [[RIPER_5단계_상태머신]]
- 규모별 게이트 적용: [[작업_규모별_워크플로]]
- 산출물 레벨 게이트: [[결정론_검증_게이트]] — 에이전트 체인 대신 단일 LLM 산출물을 구조 불변식으로 강제하는 같은 철학의 다른 입도
- 완료 증거 규약(REVIEW): [[증거_기반_완료_검증]] — 실행·출력 확인 후에만 완료 선언

## 출처

- raw/Workflow-Design-Philosophy.md (2026-05-22 유입) — §5-3, §5-4
- raw/generic-3tier-setup-prompt.md (2026-05-22 유입) — STEP 3-B (quality-sentinel), STEP 3-C (reporter), STEP 4 (producer)
- raw/ecosystem-atomic-analysis.md (2026-05-22 유입) — §1-B Tier 1·3 책임 경계
