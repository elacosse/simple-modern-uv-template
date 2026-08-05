from devtools.install_agent_skills import build_commands


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
