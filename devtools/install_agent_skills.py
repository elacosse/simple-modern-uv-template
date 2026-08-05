"""Install selected AI-agent skills into this repository with the skills CLI."""

from __future__ import annotations

import argparse
import os
import shlex
import subprocess
from collections import defaultdict

BLUEPRINT_SOURCE = "imbue-ai/blueprint"
ADDY_OSMANI_SOURCE = "addyosmani/agent-skills"
MATT_POCOCK_SOURCE = "mattpocock/skills"
SUPPORTED_AGENTS = ("codex", "antigravity-cli")

ADDY_OSMANI_SKILLS = (
    "api-and-interface-design",
    "browser-testing-with-devtools",
    "ci-cd-and-automation",
    "code-review-and-quality",
    "code-simplification",
    "context-engineering",
    "debugging-and-error-recovery",
    "deprecation-and-migration",
    "documentation-and-adrs",
    "doubt-driven-development",
    "frontend-ui-engineering",
    "git-workflow-and-versioning",
    "idea-refine",
    "incremental-implementation",
    "interview-me",
    "observability-and-instrumentation",
    "performance-optimization",
    "planning-and-task-breakdown",
    "security-and-hardening",
    "shipping-and-launch",
    "source-driven-development",
    "spec-driven-development",
    "test-driven-development",
    "using-agent-skills",
)

MATT_POCOCK_SKILLS = (
    "ask-matt",
    "batch-grill-me",
    "claude-handoff",
    "code-review",
    "codebase-design",
    "design-an-interface",
    "diagnosing-bugs",
    "domain-modeling",
    "edit-article",
    "git-guardrails-claude-code",
    "grill-me",
    "grill-with-docs",
    "grilling",
    "handoff",
    "implement",
    "improve-codebase-architecture",
    "loop-me",
    "migrate-to-shoehorn",
    "obsidian-vault",
    "prototype",
    "qa",
    "request-refactor-plan",
    "research",
    "resolving-merge-conflicts",
    "scaffold-exercises",
    "setup-matt-pocock-skills",
    "setup-pre-commit",
    "setup-ts-deep-modules",
    "tdd",
    "teach",
    "to-questionnaire",
    "to-spec",
    "to-tickets",
    "triage",
    "ubiquitous-language",
    "wayfinder",
    "wizard",
    "writing-beats",
    "writing-fragments",
    "writing-great-skills",
    "writing-shape",
)

SKILLS = {
    "blueprint": (BLUEPRINT_SOURCE, "blueprint"),
    "blueprint-generate": (BLUEPRINT_SOURCE, "blueprint-generate"),
    **{skill: (ADDY_OSMANI_SOURCE, skill) for skill in ADDY_OSMANI_SKILLS},
    **{skill: (MATT_POCOCK_SOURCE, skill) for skill in MATT_POCOCK_SKILLS},
}


def _effective_agents(agents: list[str]) -> list[str]:
    """Avoid duplicate installs because Codex and Antigravity share `.agents/skills`."""
    if set(agents) == set(SUPPORTED_AGENTS):
        return ["codex"]
    return agents


def build_commands(skill_names: list[str], agents: list[str], *, remove: bool) -> list[list[str]]:
    """Build one skills-CLI command per source repository."""
    grouped_skills: dict[str, list[str]] = defaultdict(list)
    for skill_name in skill_names:
        source, upstream_name = SKILLS[skill_name]
        grouped_skills[source].append(upstream_name)

    commands: list[list[str]] = []
    for source, upstream_names in grouped_skills.items():
        command = ["npx", "--yes", "skills", "remove" if remove else "add"]
        if not remove:
            command.append(source)
        for agent in _effective_agents(agents):
            command.extend(("--agent", agent))
        if not remove:
            command.append("--copy")
        for upstream_name in upstream_names:
            command.extend(("--skill", upstream_name))
        command.append("--yes")
        commands.append(command)
    return commands


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skills", nargs="*", metavar="SKILL", help="Exact skill names to install or remove")
    parser.add_argument("--list", action="store_true", help="List the curated skill catalog")
    parser.add_argument("--dry-run", action="store_true", help="Print commands without running them")
    parser.add_argument("--remove", action="store_true", help="Remove selected project-local skills")
    parser.add_argument(
        "--agent",
        action="append",
        choices=SUPPORTED_AGENTS,
        default=[],
        help="Target agent; repeat for multiple agents (default: codex)",
    )
    return parser


def main() -> None:
    args = _parser().parse_args()
    if args.list:
        for name, (source, _) in sorted(SKILLS.items()):
            print(f"{name:36} {source}")
        return
    if not args.skills:
        _parser().error("choose one or more skills, or use --list")

    unknown_skills = sorted(set(args.skills) - SKILLS.keys())
    if unknown_skills:
        _parser().error(f"unknown skill(s): {', '.join(unknown_skills)}")

    agents = args.agent or ["codex"]
    commands = build_commands(args.skills, agents, remove=args.remove)
    if len(agents) == 2:
        print("Codex and Antigravity CLI share `.agents/skills`; installing once for Codex.")

    environment = os.environ.copy()
    environment["DISABLE_TELEMETRY"] = "1"
    for command in commands:
        print("+", shlex.join(command))
        if not args.dry_run:
            subprocess.run(command, check=True, env=environment)


if __name__ == "__main__":
    main()
