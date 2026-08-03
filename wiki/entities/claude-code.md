---
title: Claude Code
type: entity
created: 2026-06-23
updated: 2026-08-03
sources: [youtube-dYXHJKnIT_I, youtube-Gb2VMWrUmZ0, youtube-BssPGKsP60s, youtube-hXlB1QstQ-Y, youtube-gol5jv4wcfs, youtube-f0hcByvsyjU, youtube-UClLUoGaCxU, youtube-6cr4PeilKJk]
tags: [도구, CLI, 에이전틱코딩, Anthropic]
---
# Claude Code

Claude Code는 Anthropic이 만든 터미널용 코딩 에이전트다. 편집기 옆에서 자동완성을 거드는 도구가 아니라, 코드베이스를 직접 읽고 고치고 명령까지 실행하며 작업을 스스로 계획해 진행한다. 컨텍스트 파일·스킬·훅 같은 확장 장치가 모두 이 도구 위에서 동작하기 때문에, 관련 개념 문서를 읽기 전에 알아 두면 좋은 배경 페이지다.

[[entities/anthropic|Anthropic]]가 만든 에이전틱 코딩 CLI 도구다. 터미널에서 동작하며 코드베이스를 읽고 수정하고 명령을 실행하는 에이전트로서, 단순 자동완성을 넘어 작업을 스스로 계획·수행한다.

## 이 위키에서의 등장
- 실전 워크플로우의 핵심 도구로 반복 소개된다 (→ [[sources/youtube-dYXHJKnIT_I|#2 Claudebot 실전 워크플로우]]).
- [[concepts/subagents-agent-teams|서브에이전트 & 에이전트 팀]](에이전트 팀)을 통해 "10배 똑똑하게" 쓰는 법이 다뤄진다 (→ [[sources/youtube-Gb2VMWrUmZ0|#3 Claude Code Teams]]).
- [[concepts/claude-md|CLAUDE.md]] 컨텍스트 파일, [[concepts/skills|스킬]], [[concepts/hooks|훅]], [[concepts/mcp|MCP]] 등 핵심 확장 기능의 호스트 환경이다 (→ [[sources/youtube-DCsv0rKKrN4|#7 메타 엔지니어 실전편]]).
- [[concepts/harness-engineering|하네스 엔지니어링]](하네스 엔지니어링)의 주 무대로, 동일 도구라도 하네스 설계에 따라 비용·성능이 크게 갈린다 ("`$9` vs `$200`" → [[sources/youtube-6cr4PeilKJk|#13 하네스의 비밀]]).
- [[entities/boris-cherny|보리스 체르니]](Claude Code 창시자)는 "거의 바닐라 세팅"으로 쓴다고 밝혀, 과도한 하네스 축적에 대한 긴장점을 만든다 (→ [[sources/youtube-hXlB1QstQ-Y|#17 800시간 9가지 팁]]).
- "Claude Code 단독이면 망한다"며 [[entities/codex|Codex]] 병행을 권하는 [[concepts/multi-model-workflow|멀티 모델 워크플로우]] 논의의 한 축이다 (→ [[sources/youtube-f0hcByvsyjU|#20 코덱스 멀티 모델]]).
- 800시간 사용 경험 기반의 필수 [[concepts/skills|스킬]] 소개에서도 핵심 대상이다 (→ [[sources/youtube-UClLUoGaCxU|#22 필수 스킬 6가지]]).
