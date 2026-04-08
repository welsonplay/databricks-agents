# Databricks Agent Skills

Skills for AI coding assistants (Claude Code, Cursor, GitHub Copilot, etc.) that provide Databricks-specific guidance.

Published on [skills.sh](https://skills.sh) — the open agent skills directory.

## Installation

### Install all skills

```bash
npx skills add welsonplay/databricks-agents
```

### Install a specific skill

```bash
npx skills add welsonplay/databricks-agents --skill databricks-core
npx skills add welsonplay/databricks-agents --skill databricks-apps
npx skills add welsonplay/databricks-agents --skill databricks-pipelines
```

### Install for specific agents

```bash
# Claude Code only
npx skills add welsonplay/databricks-agents -a claude-code

# Claude Code and Cursor
npx skills add welsonplay/databricks-agents -a claude-code -a cursor

# All supported agents
npx skills add welsonplay/databricks-agents --all
```

### Global installation (available across all projects)

```bash
npx skills add welsonplay/databricks-agents -g
```

### Manage installed skills

```bash
# List installed skills
npx skills list

# Check for updates
npx skills check

# Update all
npx skills update

# Remove a skill
npx skills remove databricks-core

# Remove all
npx skills remove --all
```

## Available Skills

| Skill | Description | Status |
|-------|-------------|--------|
| **databricks-core** | Core CLI operations: auth, profiles, data exploration | Stable |
| **databricks-apps** | Build full-stack TypeScript apps using AppKit | Stable |
| **databricks-dabs** | Declarative Automation Bundles for resource deployment | Stable |
| **databricks-jobs** | Jobs orchestration and scheduling (Lakeflow Jobs) | Stable |
| **databricks-lakebase** | Lakebase Postgres Autoscaling (serverless OLTP) | Stable |
| **databricks-model-serving** | Model Serving endpoints for LLM/ML inference | Experimental |
| **databricks-pipelines** | Lakeflow Spark Declarative Pipelines (ETL/DLT) | Stable |

## Skill Hierarchy

```
databricks-core (foundation)
├── databricks-apps        (product)
├── databricks-jobs        (product)
├── databricks-dabs        (enabler)
├── databricks-lakebase    (product)
├── databricks-model-serving (product - experimental)
└── databricks-pipelines   (product)
```

The `databricks-core` skill is the foundation and should be loaded first. All other skills are product skills that depend on it.

## Structure

Each skill follows the [Agent Skills Specification](https://agentskills.io/specification):

```
skill-name/
├── SKILL.md           # Main file with YAML frontmatter + instructions
└── references/        # Additional documentation loaded on demand
```

## Development

### Creating New Skills

Create a subskill that references the parent skill:

```markdown
---
name: "ai-databricks-apps"
description: "Databricks apps with AI features"
parent: databricks-apps
---

# AI-powered Databricks Apps

First, load the base databricks-apps skill for foundational guidance.

Then apply these additional patterns:
- Custom pattern 1
- Custom pattern 2
```

Or use the init command to scaffold a template:

```bash
npx skills init my-new-skill
```

### Manifest Management

After adding or updating skills, regenerate the manifest:

```bash
python3 scripts/skills.py              # generate manifest (default)
python3 scripts/skills.py validate     # validate for CI
```

## Security

When writing examples, obfuscate sensitive information:

- Workspace IDs: use `1111111111111111` instead of real IDs
- URLs: use `company-workspace.cloud.databricks.com`
- Never include real tokens, passwords, or credentials
- Use placeholders for users, teams, and resource IDs

## Contributing

- Documentation examples must follow least-privilege defaults
- Obfuscate sensitive values: workspace IDs, URLs, credentials
