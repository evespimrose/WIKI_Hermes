---
tags: [Onboarding, Simulation, Scenario, Minimal-Setup]
date_created: 2026-06-16
last_modified: 2026-06-16
---

# Claude 대규모 리팩토링 시뮬레이션 시나리오 (최소 설정 버전)

## 🎬 시나리오 개요
**상황**: Unity 기반 2D 플랫포머 게임 프로젝트의 **캐릭터 로직 대규모 리팩토링**을 Claude Desktop의 Code 탭에서 진행합니다.
- 기존 문제: `PlayerController.cs`에 모든 로직(입력, 이동, 점프, 애니메이션, 충돌, 사운드)이 몰려있음 (800줄)
- 리팩토링 목표: 각 책임을 별도의 MonoBehaviour로 분리 (단일 책임 원칙 적용)
- **사용 환경**: **최소한의 설정만 추가한 Claude Desktop** →
  - `.claude/settings.json`: 기본 Rule 1개, Commit-Pre Hook 1개 설정
  - `docs/CommitMessageGuide.md`: 커밋 메시지 가이드 (commit-message Skill용)
  - *Custom Agent는 없고, 기본 Tool만 사용*

### 📋 최소 설정 목록
| 요소                | 내용                                                                 |
|---------------------|----------------------------------------------------------------------|
| **Rule 1**          | "기존 코드에 없는 기능은 절대 추가하지 마세요!"                        |
| **Hook 1 (Commit-Pre)** | "커밋 전에 git status와 git diff를 사용자에게 보여주고 확인 받기"     |
| **Skill 1**         | commit-message: `docs/CommitMessageGuide.md`를 기반으로 양식에 맞는 커밋 메시지 자동 작성 |
| **Command**         | 기본으로 내장된 /clear, /compact만 사용                               |

---

## 📝 시뮬레이션 대본 (Step by Step)

---

### 🟢 Step 1: 사용자가 Claude Desktop 열고 프로젝트 폴더 열기
- **사용자 행동**: Claude Desktop 실행 → Code 탭 → "Open Folder"로 `C:\Projects\MyPlatformerGame` 선택
- **Claude 내부 프로세스**:
  1. **자동 탐색**: LS Tool로 프로젝트 루트 폴더 내용 자동 확인 → `.claude/` 폴더 발견
  2. **Hook (Session-Start, 기본 제공)**: `.claude/settings.json` 자동 Read
  3. **Rule 로드**: Rule 1 ("기존 기능 추가 금지")를 메모리에 로드
  4. **인사 메시지**: "안녕하세요! `MyPlatformerGame` 프로젝트를 열었어요. 설정 파일을 확인했어요: '기존 기능 추가 금지' Rule이 적용 중이에요. 어떤 작업을 도와드릴까요?"
- **이 때 개입한 요소**: ✅ **Hook (Session-Start)**, ✅ **Rule 로드**

---

### 🟢 Step 2: 사용자의 최초 요청 입력
- **사용자 입력**: "이 프로젝트의 Player 관련 코드가 너무 커서 리팩토링하고 싶어. PlayerController.cs에 모든 게 다 들어있어. 각 기능을 별도 파일로 분리해줘."
- **Claude 내부 프로세스**:
  1. **Intent 분석**: "대규모 리팩토링, PlayerController 분리"로 이해
  2. **Tool Search**: Glob → Read 순서로 사용하기로 결정
  3. **Tool Use (Glob)**: `Glob("Assets/Scripts/**/Player*.cs")` 실행
  4. **결과 확인**: `Assets/Scripts/Player/PlayerController.cs`, `Assets/Scripts/Player/PlayerStats.cs` 검색
  5. **Tool Use (Read)**: 두 파일 전체 Read
  6. **분석**: PlayerController.cs가 800줄, 모든 로직이 들어있음 확인
  7. **초기 질문**: "PlayerController.cs와 PlayerStats.cs를 확인했어요! 분리할 기능 리스트를 제안해드릴까요?"
- **이 때 개입한 요소**: 없음 (Tool Search/Tool Use만)

---

### 🟢 Step 3: 분리 계획 제안 & 사용자 승인
- **Claude의 계획**:
  1. `PlayerInput.cs`: 키보드/조이스틱 입력 처리
  2. `PlayerMovement.cs`: 이동, 점프 물리 처리
  3. `PlayerAnimation.cs`: 애니메이션 파라미터 제어
  4. `PlayerCollision.cs`: 충돌 이벤트 처리
  5. `PlayerSound.cs`: 사운드 재생
  6. 기존 PlayerController는 각 컴포넌트 참조 관리자로 축소
- **사용자 응답**: "좋아, 그대로 해줘."
- **이 때 개입한 요소**: 없음

---

### 🟢 Step 4: 새 파일 생성 시작 (PlayerInput.cs)
- **Claude 내부 프로세스**:
  1. **Tool Search**: PlayerController.cs에서 입력 관련 코드 추출
  2. **Tool Use (Write)**: `Assets/Scripts/Player/PlayerInput.cs` 작성
- **Claude의 메시지**: "PlayerInput.cs를 만들었어요! 입력 관련 코드를 옮겼어요."
- **이 때 개입한 요소**: 없음

---

### 🟢 Step 5: PlayerMovement.cs 생성 → Rule이 환각 차단! ✅
- **Claude 내부 프로세스**:
  1. **Tool Search**: PlayerController.cs에서 물리 관련 코드 추출
  2. **자연스레 Dash() 메서드를 추가하려고 함** →
  3. **Rule 1 개입!**: "기존 코드에 없는 기능은 절대 추가하지 마세요!" Rule이 트리거
  4. **자체 검토**: PlayerController.cs에 Dash() 메서드가 없었음을 확인 → Dash() 빼고 작성
  5. **Tool Use (Write)**: `PlayerMovement.cs` 작성 (Dash 기능 없음!)
- **Claude의 메시지**: "PlayerMovement.cs를 만들었어요! 물리 관련 코드를 옮겼어요."
- **이 때 개입한 요소**: ✅ **Rule 1 (환각 차단)**

---

### 🟢 Step 6: 나머지 파일 생성 & PlayerController 축소
- **Claude 내부 프로세스**:
  1. **Tool Use (Write)**: `PlayerAnimation.cs`, `PlayerCollision.cs`, `PlayerSound.cs` 순서대로 작성
  2. **Tool Use (Edit)**: 기존 PlayerController.cs 축소 → 각 컴포넌트 Reference 변수만 남기고 로직 삭제
- **Claude의 메시지**: "모든 파일을 만들고 PlayerController를 축소했어요! 확인해보세요."
- **이 때 개입한 요소**: 없음

---

### 🟢 Step 7: 컴파일 오류 발견 → 사용자가 힌트 줌
- **사용자 피드백**: "Unity에서 NullReferenceException이 나! PlayerAnimation.cs에서 Animator 찾는 부분이 문제야."
- **Claude 내부 프로세스**:
  1. **Tool Use (Read)**: PlayerAnimation.cs 다시 Read
  2. **문제 발견**: `GetComponent<Animator>()`인데, Animator가 Child Object에 있음
  3. **Tool Use (Edit)**: `GetComponentInChildren<Animator>()`로 수정
- **Claude의 메시지**: "수정했어요! Child Object의 Animator를 찾도록 변경했어요."
- **이 때 개입한 요소**: 없음 (TRAE-debugger Skill은 없어서 수동으로 분석)

---

### 🟢 Step 8: 최종 확인 & git commit → Hook & Skill 개입! ✨
- **사용자 피드백**: "이제 오류가 없어! git으로 커밋해줘."
- **Claude 내부 프로세스**:
  1. **Hook 1 (Commit-Pre) 개입!**:
     - **Tool Use (Run)**: `git status`, `git diff` 실행
     - 사용자에게 변경 사항 보여주고 확인 요청: "커밋 전 변경 사항을 확인해주세요! [git diff 결과 표시] 계속할까요?"
  2. **사용자 확인**: "응, 계속해."
  3. **Skill 1 (commit-message) 개입!**:
     - **Tool Use (Read)**: `docs/CommitMessageGuide.md` Read
     - 가이드에 맞춰 커밋 메시지 자동 작성:
       ```
       refactor: Player 로직을 개별 컴포넌트로 분리

       - PlayerInput.cs: 입력 처리 분리
       - PlayerMovement.cs: 물리 처리 분리
       - PlayerAnimation.cs: 애니메이션 처리 분리
       - PlayerCollision.cs: 충돌 처리 분리
       - PlayerSound.cs: 사운드 처리 분리
       - PlayerController.cs: 컴포넌트 관리자로 축소
       ```
  4. **Tool Use (Run)**: `git add Assets/Scripts/Player/`, `git commit -m "[자동 생성 메시지]"` 실행
- **Claude의 메시지**: "커밋이 완료됐어요!"
- **이 때 개입한 요소**: ✅ **Hook (Commit-Pre)**, ✅ **Skill (commit-message)**

---

### 🟢 Step 9: 세션 종료 전 → /compact로 컨텍스트 압축!
- **사용자 입력**: "오늘 작업 끝! 컨텍스트 정리해줘."
- **Claude 내부 프로세스**:
  1. **Command /compact 개입!**:
     - 현재 대화 내용을 핵심 정보로 요약: "Player 리팩토링 완료, 5개 새 파일 생성, PlayerController 축소, git 커밋 완료"
     - 요약 내용만 남기고 나머지 컨텍스트 정리
- **Claude의 메시지**: "컨텍스트를 압축했어요! 핵심 내용만 남겼어요: [요약 내용]"
- **이 때 개입한 요소**: ✅ **Command (/compact)**

---

### 🟢 Step 10: 다음 날 세션 다시 열기 → 세션 단절은 여전히 있음
- **사용자 행동**: Claude Desktop 닫고 다음 날 다시 열기
- **Claude 내부 프로세스**:
  - 새로운 Session 시작 → 이전 대화 내용 기억 못함
  - "안녕하세요! `MyPlatformerGame` 프로젝트를 열었어요. 어떤 작업을 도와드릴까요?"
- **이 때 개입했어야 할 요소**: ❌ **Agent (Reporter)**, ❌ **Command (/resume)** (설정에 없어서 없음)

---

## 📊 각 요소가 개입한 시점 정리

| 단계 | 개입한 요소                | 설명                                                                 |
|------|-----------------------------|----------------------------------------------------------------------|
| Step 1 | Hook (Session-Start), Rule | 설정 파일 읽고 Rule 로드                                             |
| Step 5 | Rule 1                     | Dash 기능 추가하려는 환각 차단                                       |
| Step 8 | Hook (Commit-Pre), Skill   | git 변경 사항 확인, 좋은 커밋 메시지 자동 작성                       |
| Step 9 | Command (/compact)         | 컨텍스트 압축                                                         |

---

## 📝 Claude의 Tool 사용 순서 요약
1. **LS**: 프로젝트 폴더 탐색
2. **Glob**: Player 관련 파일 검색
3. **Read**: PlayerController.cs, PlayerStats.cs, CommitMessageGuide.md 읽기
4. **Write**: 5개 새 파일 작성
5. **Edit**: PlayerController.cs, PlayerAnimation.cs 수정
6. **Run**: git status, git diff, git add, git commit 실행

---

## 🎯 Key Takeaways
1. **Rule이 환각을 막아줌**: Step 5에서 Rule 1이 없었으면 Dash 기능이 추가됐을 것
2. **Hook이 안전성을 높여줌**: Commit-Pre Hook으로 실수로 잘못된 파일 커밋하는 것 방지
3. **Skill이 시간을 절약해줌**: commit-message Skill으로 좋은 커밋 메시지 빠르게 작성
4. **여전히 부족한 점**: Agent가 없어서 작업 기록이 안 남고, /resume이 없어서 세션 단절 문제가 있음
