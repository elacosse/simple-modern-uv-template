from devtools.install_agent_skills import (
    ADDY_OSMANI_SKILLS,
    BUNDLES,
    DEFAULT_AGENTS,
    MATT_POCOCK_SKILLS,
    SKILLS,
    build_commands,
)


def test_build_commands_groups_skills_by_source() -> None:
    commands = build_commands(
        ["blueprint", "api-and-interface-design", "test-driven-development"],
        ["codex"],
        remove=False,
    )

    assert commands == [
        [
            "npx",
            "--yes",
            "skills",
            "add",
            "imbue-ai/blueprint",
            "--agent",
            "codex",
            "--copy",
            "--skill",
            "blueprint",
            "--yes",
        ],
        [
            "npx",
            "--yes",
            "skills",
            "add",
            "addyosmani/agent-skills",
            "--agent",
            "codex",
            "--copy",
            "--skill",
            "api-and-interface-design",
            "--skill",
            "test-driven-development",
            "--yes",
        ],
    ]


def test_build_commands_deduplicates_shared_agent_directory() -> None:
    commands = build_commands(["blueprint"], ["codex", "antigravity-cli"], remove=False)

    assert commands[0].count("codex") == 1
    assert "antigravity-cli" not in commands[0]


def test_default_agents_target_codex_and_claude_code() -> None:
    commands = build_commands(["blueprint"], list(DEFAULT_AGENTS), remove=False)

    assert commands[0].count("codex") == 1
    assert commands[0].count("claude-code") == 1


def test_build_commands_supports_matt_pocock_skills() -> None:
    commands = build_commands(["codebase-design"], ["codex"], remove=False)

    assert commands == [
        [
            "npx",
            "--yes",
            "skills",
            "add",
            "mattpocock/skills",
            "--agent",
            "codex",
            "--copy",
            "--skill",
            "codebase-design",
            "--yes",
        ]
    ]


def test_bundles_include_every_skill_once() -> None:
    all_bundle = BUNDLES["all"]

    assert BUNDLES["planning-with-blueprint"] == ("blueprint", "blueprint-generate")
    assert BUNDLES["addy-engineering-skills"] == ADDY_OSMANI_SKILLS
    assert BUNDLES["mattpocock-workflows"] == MATT_POCOCK_SKILLS
    assert len(all_bundle) == len(set(all_bundle))
    assert set(all_bundle) == SKILLS.keys()
