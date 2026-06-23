---
tags: [llm-wiki, wiki관리, 보안]
date_created: 2026-06-15
last_modified: 2026-06-15
---

# 외부 API 전송 안전장치

파일 내용을 제3자 LLM API로 보내기 전 거쳐야 할 **방어 체크리스트**. 위키 파일을 외부 모델에 압축·정제 위탁하는 자동화(헤르메스 자율 스카우팅 등)를 붙일 때, 자격증명 유출·원본 파손을 막는 하드 게이트. [[맥락_오염_방지]]가 *들어오는* 오염을 막는다면, 본 장치는 *나가는* 데이터 경계를 지킨다.

## 3대 장치 (caveman-compress 사례)

1. **민감파일 하드 거부** — 읽기 *전에* denylist로 차단: `.env`·`credentials`·`secrets`·`*.pem`·`*.key`, 그리고 `.ssh`/`.aws`/`.gnupg`/`.kube`/`.docker` 경로. 자격증명을 API로 보내느니 *시끄럽게 실패*한다(오탐이면 사용자가 파일명 변경).
2. **frontmatter verbatim 보존** — LLM은 YAML frontmatter를 rewrite하는 습성이 있다. 압축 *전에* 분리해 두고 결과에 그대로 재부착, 본문만 변환.
3. **백업 readback 검증 + 크기 상한** — 백업을 소스 디렉토리 *밖*에 저장(스킬 오토로더가 `.original` 사본을 재수집하지 않게) 후 readback으로 바이트 일치 확인, 불일치면 백업 삭제·중단(반쪽 압축 방지). 500KB 초과 거부.

## 볼트에서의 위치

볼트의 [[에이전트_자는시간_학습루프]]·헤르메스가 위키 파일을 외부 API에 위탁하기 시작하면 본 체크리스트가 *필수* 전제다. [[위키_저장_5대필터]]가 위키 *승격* 게이트라면, 본 장치는 위키 *송출* 게이트. [[맥락_오염_방지]]의 "통제 없는 저장은 오염을 진실로 굳힌다"의 송신측 대응 — 통제 없는 송출은 비밀을 유출한다.

## 출처

- raw/caveman_입국심사.md — Atom 6(caveman-compress 안전장치)
- docs/analysis/caveman_analysis.md — §2 구현(is_sensitive_path·frontmatter·readback)
- 상류: github.com/JuliusBrussee/caveman (caveman-compress compress.py · SECURITY.md)
