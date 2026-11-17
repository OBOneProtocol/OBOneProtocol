<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.svg">
    <img src="assets/header-light.svg" alt="Jesse / O-B-ONE: cloud and application engineer, multi-agent AI systems, defensive security" width="880">
  </picture>
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/now-dark.svg">
    <img src="assets/now-light.svg" alt="Now: building a supervised multi-agent system and an AI service desk prototype, running it on Claude Code and Copilot CLI among other tools, shipping gated upstream fixes" width="744">
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

More than four years on the service desk taught me that a failure people can
see is easier to fix than one that stays hidden, and I build AI automation and
cloud tooling around that idea. The multi-agent systems I design keep the human
in the lead, so the agents draft and test the work and nothing goes out under my
name until I approve it. The proof is below: an LLMOps infrastructure guide and
upstream pull requests, merged and in review, backed by regression tests.

**Open to:** AI automation, cloud security and technical support roles · Los Angeles / Long Beach area or remote

## Selected work

### [llmops-infra-guide](https://github.com/OBOneProtocol/llmops-infra-guide)

A generate-and-validate loop: an LLM drafts a Dockerfile, `docker build`
acts as the ground-truth validator, and build errors feed the next attempt.
Documented samples cover Flask, Node.js and Go.

### Merged upstream

- **[career-ops #7098](https://github.com/career-ops-hq/career-ops/pull/7098)** <img src="https://img.shields.io/github/pulls/detail/state/career-ops-hq/career-ops/7098?style=flat&label=PR" height="18" alt="PR #7098 state"><br>
  The updater reported "up to date" on the main channel when the commit
  lookup failed (an API rate limit, for example). It now reports drift; a test
  stubs the failed lookup.
- **[sure #5038](https://github.com/we-promise/sure/pull/5038)** <img src="https://img.shields.io/github/pulls/detail/state/we-promise/sure/5038?style=flat&label=PR" height="18" alt="PR #5038 state"><br>
  Stored Brandfetch logo URLs resolve with the current client ID, so rotating
  the ID in settings repairs existing merchant and security logos without a
  data backfill.
- **[ttt #1601](https://github.com/eugenioenko/ttt/pull/1601)** <img src="https://img.shields.io/github/pulls/detail/state/eugenioenko/ttt/1601?style=flat&label=PR" height="18" alt="PR #1601 state"><br>
  New untitled buffers inherit the editor's `insertSpaces` and `tabSize`
  settings, covered by a regression test and verified against the built binary.
- **[career-ops #3711](https://github.com/career-ops-hq/career-ops/pull/3711)** <img src="https://img.shields.io/github/pulls/detail/state/career-ops-hq/career-ops/3711?style=flat&label=PR" height="18" alt="PR #3711 state"><br>
  Detect project-scoped Playwright MCP installs, with precedence-aware config
  resolution and regression tests.
- **[career-ops #3591](https://github.com/career-ops-hq/career-ops/pull/3591)** <img src="https://img.shields.io/github/pulls/detail/state/career-ops-hq/career-ops/3591?style=flat&label=PR" height="18" alt="PR #3591 state"><br>
  Harden context-budget prompt assembly and tracker-path handling.

### In review upstream (opened November 2026)

- **[conductor #1831](https://github.com/conductor-oss/conductor/pull/1831)** <img src="https://img.shields.io/github/pulls/detail/state/conductor-oss/conductor/1831?style=flat&label=PR" height="18" alt="PR #1831 state"><br>
  Keep the MySQL queue's unack sweep scheduled after a failed run, so a
  dropped database connection no longer strands workflows until restart.
  Review feedback addressed; awaiting maintainer review.
- **[agent-browser #2549](https://github.com/vercel-labs/agent-browser/pull/2549)** <img src="https://img.shields.io/github/pulls/detail/state/vercel-labs/agent-browser/2549?style=flat&label=PR" height="18" alt="PR #2549 state"><br>
  `frame "#selector"` resolves cross-origin iframes, covered by an
  end-to-end test against real Chrome.

### Building now (private)

- **AI-assisted IT service desk.** Agents handle intake, triage and
  first-line remediation. A fix that fails review gets up to three examined
  fixes, each driven by the reviewer's findings, before the ticket escalates
  to a technician. Privileged actions such as password resets require a human
  approver.
- **Operator console for the agent team.** Halt a run, preserve its session,
  and review the report every run produces.

## What I work on

**Supervised agent systems.** Permission boundaries for agent actions, failure
handling that recovers or halts in a known state, and oversight that keeps a
human in the lead through approval gates and per-run reports instead of log
review.

**Upstream contributions.** Every fix starts with evidence: reproduce the
issue, confirm it is unclaimed and that maintainers want it, follow the
project's contribution and AI policies, and land a failing regression test
before changing code.

**Cloud and defensive security.** Container build pipelines, AWS reliability,
threat modeling, and hardening against common attack paths: prompt injection,
over-privileged CI tokens, unpinned dependencies.

## The system I run

A multi-agent system, a lead orchestrator with specialist roles, running on Claude
Code and Copilot CLI, among other tools. Its operating model borrows from IT
service management.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/system-dark.svg">
    <img src="assets/system-light.svg" alt="Flow diagram: a human in the lead briefs a personal agent, which briefs a lead orchestrator. The orchestrator fans work out to four specialists (build and test, security review, reproduction, product and content). Results return through the orchestrator to the personal agent, which presents them to the human for approval; approved work goes back to the specialists to finish." width="880">
  </picture>
</p>

- **Human in the lead.** External writes (pull requests, public posts,
  anything that spends money) are gated on my approval of the exact item.
  Agent confidence is not authorization.
- **Independent verification.** The final reviewer reruns the test suite and
  reads the diff directly. A summary from another agent is not evidence.
- **Examined fixes, not blind retries.** On failure, the agent records what
  failed, the likely root cause and what the next attempt changes, bounded at
  three attempts. With no new hypothesis, it halts and escalates with the
  evidence.
- **Resumable take-over.** Any run can be stopped and handed to a person at
  the same step, with its session history intact.

## Engineering principles

- A bug report becomes a failing test before it becomes a diff.
- "Works on my machine" is an environment finding, not a fix.
- A mismatch between code and docs may be intentional; I confirm with the
  maintainers before changing either.
- Every external action is non-idempotent until proven otherwise: gate it,
  don't retry it.
- If another contributor claims an issue first, my fix stays local.
- Decisions and lessons are written down, dated, and revised when they prove
  wrong.

## Activity

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/OBOneProtocol/OBOneProtocol/output/impact-dark.svg">
    <img src="https://raw.githubusercontent.com/OBOneProtocol/OBOneProtocol/output/impact-light.svg" alt="Impact, updated daily from GitHub: merged upstream pull requests, open-source projects with my merged fixes, and pull requests awaiting maintainer review" width="880">
  </picture>
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/OBOneProtocol/OBOneProtocol/output/github-contribution-grid-snake-dark.svg">
    <img src="https://raw.githubusercontent.com/OBOneProtocol/OBOneProtocol/output/github-contribution-grid-snake.svg" alt="My GitHub contribution graph for the last year, with a snake eating the days I contributed" width="880">
  </picture>
</p>

---

<p align="center">
  <a href="https://oboneprotocol.github.io"><img src="https://img.shields.io/badge/Portfolio-0d1117?style=flat&logo=githubpages&logoColor=white" height="22" alt="Portfolio"></a>
  <a href="https://www.linkedin.com/in/oboneprotocol"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white" height="22" alt="LinkedIn"></a>
</p>
