<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.svg">
    <img src="assets/header-light.svg" alt="Jesse / O-B-ONE — cloud and application engineer, multi-agent AI systems, defensive security" width="880">
  </picture>
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/now-dark.svg">
    <img src="assets/now-light.svg" alt="Now: building a supervised 10-agent system and an AI service desk prototype, running it on Claude Code and Copilot CLI among other tools, shipping gated upstream fixes" width="720">
  </picture>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white" height="22" alt="Python">
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white" height="22" alt="TypeScript">
  <img src="https://img.shields.io/badge/Node.js-339933?style=flat&logo=nodedotjs&logoColor=white" height="22" alt="Node.js">
  <img src="https://img.shields.io/badge/C-00599C?style=flat&logo=c&logoColor=white" height="22" alt="C">
  <img src="https://img.shields.io/badge/Bash-4EAA25?style=flat&logo=gnubash&logoColor=white" height="22" alt="Bash">
  <img src="https://img.shields.io/badge/AWS-232F3E?style=flat&logo=amazonwebservices&logoColor=white" height="22" alt="AWS">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white" height="22" alt="Docker">
  <img src="https://img.shields.io/badge/Playwright-2EAD33?style=flat&logo=playwright&logoColor=white" height="22" alt="Playwright">
  <img src="https://img.shields.io/badge/Claude_Code-D97757?style=flat&logo=anthropic&logoColor=white" height="22" alt="Claude Code">
  <img src="https://img.shields.io/badge/Copilot_CLI-24292F?style=flat&logo=githubcopilot&logoColor=white" height="22" alt="Copilot CLI">
</p>

---

Engineer in Los Angeles / Long Beach. I build software that has to be trusted
before it's clever: multi-agent systems with real approval gates, cloud
automation that fails loudly, and fixes that arrive with the test that proves
them.

## What I work on

**Agent systems people can actually supervise.** Most of my time goes to the
parts that decide whether an AI system is safe to leave running: who is allowed
to act, what happens when a step fails, and how a person stays in the loop
without reading every log.

**Upstream fixes, evidence first.** Before I touch someone else's project I
check that the issue is real, unclaimed and wanted, read the contribution
rules, and write the failing test. Then the fix.

**Cloud and defensive security.** Container builds, AWS reliability work, threat modelling and hardening of
common attack paths.

## The system I run

A 10-agent team that runs on Claude Code and GitHub Copilot CLI, among other
tools. I run it the way a good service desk runs:

- **Nothing leaves the machine without me.** Pull requests to other people's
  projects and anything that spends money wait for my approval of the exact
  item. An agent's confidence is not approval.
- **Checked work.** The final reviewer reruns the tests and reads the diff
  itself. A summary from another agent isn't evidence.
- **Human take-over.** Any run can be stopped and handed to a person at the
  same point, with its history intact.

## Selected work

### [llmops-infra-guide](https://github.com/OBOneProtocol/llmops-infra-guide)

A local LLM writes a Dockerfile, `docker build` judges it, and the build
errors feed the next attempt. A small loop with a ground-truth validator;
documented samples cover Flask, Node.js and Go.

### Merged upstream

- **[career-ops #3711](https://github.com/career-ops-hq/career-ops/pull/3711)**
  — detect project-scoped Playwright MCP installs, with precedence-aware config
  and regression tests.
- **[career-ops #3591](https://github.com/career-ops-hq/career-ops/pull/3591)**
  — harden context-budget prompt assembly and tracker-path handling.
- **[ttt #1601](https://github.com/eugenioenko/ttt/pull/1601)**
  — new untitled files now follow the editor's `insertSpaces` and `tabSize`
  settings, with a regression test and a before-and-after check on the real
  binary.

### In review upstream (opened November 2026)

- **[conductor #1831](https://github.com/conductor-oss/conductor/pull/1831)**
  — keep the MySQL queue's unack sweep running after one failed run, so a
  dropped connection doesn't strand workflows until restart. Review feedback
  addressed; waiting on a maintainer.
- **[agent-browser #2549](https://github.com/vercel-labs/agent-browser/pull/2549)**
  — let `frame "#selector"` resolve cross-origin iframes, with an end-to-end
  test against real Chrome.

### Building now (private)

- **An AI-assisted IT service desk prototype.** Agents take intake, triage
  and a first fix; a reviewer gets one retry before the ticket goes to a
  person, and privileged actions such as a password reset wait for a human
  approver.
- **A supervision panel for my own agent team.** Stop keeps the session, take
  over hands it to a person at the same point, and every run leaves a report.

## How I work, specifically

- A bug report becomes a failing test before it becomes a diff
- "Works on my machine" is an environment finding, not a fix
- A mismatch between code and docs might be a design decision; I ask first
- Every external action is non-idempotent until proven otherwise: gate it,
  don't retry it
- If someone else claims an issue first, my fix stays local, even when it's
  finished
- Notes are part of the system: decisions and lessons get written down, dated,
  and corrected when they turn out wrong

---

<p align="center">
  <a href="https://www.linkedin.com/in/oboneprotocol"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white" height="22" alt="LinkedIn"></a>
</p>
