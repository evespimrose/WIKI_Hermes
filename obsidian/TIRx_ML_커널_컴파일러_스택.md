---
tags: [llm-wiki, compiler-stack, ml-kernel, dsl, tvm]
date_created: 2026-06-24
last_modified: 2026-06-24
---

# TIRx — ML 커널용 Apache TVM 기반 오픈 컴파일러 스택

> 출처: https://aisparkup.com/wiki/tirx · 원문: https://tvm.apache.org/2026/06/22/tirx · 스카우트: 2026-06-23

Apache TVM 위에 구축된 하드웨어 네이티브 DSL + 컴파일러 스택. Triton 같은 고수준 커널 DSL의 생산성과 수동 CUDA/HIP 커널의 극한 제어 사이 경계를 낮춘다.

## 프로그래밍 모델 (핵심 구성)

| 구성 | 설명 |
|---|---|
| **Execution scope** | 연산이 어떤 하드웨어 역할 범위에서 실행될지 명시. |
| **Tensor layout** | global/shared/register/tensor memory/SRAM 중 배치를 storage-first 로 표현. |
| **Tile primitive dispatch** | operand layout과 target에 따라 copy/MMA/TMA 프리미티브를 네이티브 IR로 매핑. |

새 하드웨어 기능은 먼저 backend intrinsic으로 노출하고, 사용이 안정되면 tile primitive로 승격.

## 개념 요약

- **저수준 제어 유지 + 반복 패턴 자동화**: 전문가가 하드웨어 구조를 명시하고, 컴파일러는 tile primitive만 해석.
- **신속한 신규 기능 대응**: 신규 GPU(예: Blackwell)에서 빠르게 커널 실험 가능.
- **적용 대상**: 모델 서빙 엔지니어, attention/MoE/저정밀 연구, 자동 커널 최적화 루프.

## 볼트 내 위치

- [[Wiki_허브]] — 위키 메타시스템 내 일반 아키텍처 참고 사례로 등록.
- 인접 가능: [[asmdef_레이어_경계강제]] (저수준 경계 강제와 유사한 맥락).

## 외부 링크

- [Apache TVM 공식 블로그](https://tvm.apache.org/2026/06/22/tirx)
- [zml](https://aisparkup.com/wiki/zml/) — Zig 기반 ML 컴파일·런타임
- [vllm](https://aisparkup.com/wiki/vllm/) — LLM 서빙 엔진
