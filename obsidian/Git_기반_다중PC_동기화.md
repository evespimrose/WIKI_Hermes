---
tags: [llm-wiki, wiki관리, git, 동기화]
date_created: 2026-05-26
last_modified: 2026-05-26
---

# Git 기반 다중 PC 동기화

중앙 LLM Wiki를 여러 PC에서 공유·동기화하는 전략과 git 저장소 구조.

## 저장소 구조 및 추적 정책

```
D:\Fork\WIKI (Git 저장소)
├── .git/              ← git 메타데이터
├── obsidian/          ✓ 추적 (최종 지식 그래프)
├── archive/           ✓ 추적 (감시 목적)
├── raw/               ✗ 무시 (임시 입수소, 로컬 전용)
├── CLAUDE.md          ✓ 추적 (편집 규칙)
└── .gitignore
```

### .gitignore 정책

```gitignore
# raw/ 폴더는 추적하지 않음
# 이유: 각 PC에서 다른 자료를 입수할 수 있음
raw/

# Obsidian 내부 캐시 (로컬 메타데이터)
.obsidian/cache/
.obsidian/workspace/
```

**의도**: 
- `obsidian/`만 동기화하면 모든 PC가 동일한 지식 그래프 유지
- 각 PC는 독립적으로 `raw/`에 자료 수집 후 컴파일
- 컴파일된 결과만 공유하면 중복 없음

## 동기화 시나리오

### 시나리오 1: 신규 노트 컴파일 후 공유

```
PC-A (데스크탑)
├─ 1. raw/에 새 자료 입수 (move-to-raw)
├─ 2. compile-wiki 실행
│  └─ obsidian/에 신규 노트 생성
├─ 3. git add obsidian/ + archive/
├─ 4. git commit -m "..."
└─ 5. git push origin main

    ↓ (Git 싱크)

PC-B (노트북)
└─ git pull origin main
   → obsidian/ 신규 노트 자동 수령
   → 모든 양방향 링크도 함께 로드
   → Obsidian 그래프 뷰 즉시 반영
```

### 시나리오 2: 기존 노트 수정 및 동기화

```
PC-B에서 기존 노트 수정
│
├─ obsidian/foo.md 변경
├─ git add obsidian/foo.md
├─ git commit "Update foo.md: ..."
└─ git push

    ↓ (Git 싱크)

PC-A에서 git pull
├─ obsidian/foo.md 최신화
└─ Obsidian 재로드 (⌘R 또는 자동 감지)
```

### 시나리오 3: 충돌 (드물지만 가능)

```
동시 편집:
  PC-A: obsidian/foo.md 변경 후 push
  PC-B: 같은 파일 변경 후 push
  
  → Git 병합 충돌 발생
  → 수동으로 해결: 두 변경사항 통합
  → git add, commit, push
```

## 다중 PC 워크플로우 예시

### PC-A (데스크탑 — 주요 작업)

```
매일:
1. git pull (다른 PC의 변경사항 수령)
2. PC-A에서 새 자료 수집 (move-to-raw)
3. compile-wiki 실행
4. obsidian/ 결과 검토
5. git add + commit + push
   → PC-B, PC-C에 자동 전파
```

### PC-B (노트북 — 보조 작업)

```
필요할 때:
1. git pull (PC-A의 최신 노트 수령)
2. PC-B에서만 필요한 로컬 자료 수집
3. compile-wiki 실행 (로컬 전용)
4. git pull && git push (P-A의 변경 있으면 병합)
```

### PC-C (태블릿 또는 3번째 디바이스)

```
읽기 주로:
1. git pull (항상 최신 obsidian/)
2. Obsidian 그래프 뷰로 검색·탐색
3. 필요시 노트 수정 → git push
```

## 동기화 베스트 프랙티스

### 1. 빈번한 커밋

```bash
# 좋음 ✓
git commit -m "Add First_Grep_실전사례: RX_1 사용 예시"

# 나쁨 ✗
git commit -m "Update"  # 너무 모호
```

**이유**: git 로그가 지식 진화 이력이 됨. 검색·감사에 필수.

### 2. raw/ 입수는 커밋하지 않기

```bash
# ✓ obsidian/ + archive/ 만 커밋
git add obsidian/ archive/
git commit -m "..."

# ✗ raw/ 까지 커밋 금지 (이미 .gitignore)
```

### 3. 주기적 pull-before-push

```bash
# PC-B에서 작업 후 푸시하기 전:
git pull  # 다른 PC의 변경 먼저 받기
# (충돌 확인)
git push
```

### 4. archive/ 는 추적하되 수정 금지

```bash
# archive/ 파일은 절대 Edit 금지
# 따라서 자동으로 충돌 가능성 0
# 하지만 추적함으로써 "어떤 자료를 언제 처리했나" 기록 남음
```

## 브랜치 전략 (선택사항)

단순 운영: main 브랜치만 사용

심화 운영 (다중 편집자):
```
main               ← 안정화된 노트 (릴리스용)
├─ feature/semantic-enhancement
├─ feature/new-project-instance
└─ hotfix/broken-link-fix
```

**권장**: wiki 관리는 보통 단일 main 브랜치로 충분.

---

## 트러블슈팅

### 문제: "git pull" 후 Obsidian에 변경이 안 보임

**해결**:
1. Obsidian의 settings에서 "vault auto-save" 확인 (보통 기본 ON)
2. 필요시 Obsidian 수동 재로드: ⌘⇧R (또는 Menu → Reload vault)
3. Obsidian을 종료했다가 다시 열기

### 문제: 충돌 메시지 "both modified: obsidian/foo.md"

**해결**:
```bash
# 1. 충돌 파일 열기
cat obsidian/foo.md | less  # 충돌 마커 <<<<<<< 확인

# 2. 수동 병합 (텍스트 에디터)
# 또는 git의 병합 도구 사용:
git mergetool

# 3. 병합 완료 후
git add obsidian/foo.md
git commit
git push
```

### 문제: "git push" 거부 "non-fast-forward"

**해결**:
```bash
# 원격에 더 새로운 커밋이 있음
git pull  # 먼저 가져오기
# (충돌 없으면 자동 병합)
git push
```

---

## 성능 고려사항

| 항목 | 현황 | 영향 |
|---|---|---|
| 노트 수 | 32개 | git 성능 무시 (< 1MB) |
| archive/ 크기 | ~100KB | git 성능 무시 |
| 월간 증가 | 수십 개 노트 | 1년에 ~1MB (무시 가능) |

**결론**: 현 규모에서 git 성능 문제 없음. 향후 3~5년 후에도 충분.

---

## 관련 노트

- Vault 운영 체계: [[LLM_Wiki_운영체계]]
- compile-wiki 스킬: [[compile-wiki]]
- move-to-raw 스킬: [[move-to-raw]]

## 출처

- `raw/wiki_management_policy.md` (2026-05-26 유입) — § 4 동기화 전략, 다중 PC 워크플로우
