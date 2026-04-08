# Databricks Agent Skills

Skills for AI coding assistants (Claude Code, etc.) that provide Databricks-specific guidance.

## Structure

```
skills/
├── databricks-core/      # core skill: CLI, auth, data exploration
│   ├── SKILL.md
│   └── *.md (references)
├── databricks-apps/      # product skill: app development
│   ├── SKILL.md
│   └── references/
├── databricks-dabs/      # enabler skill: DABs deployment
├── databricks-jobs/      # product skill: job orchestration
├── databricks-lakebase/  # product skill: Lakebase OLTP
├── databricks-model-serving/  # product skill: model serving (experimental)
└── databricks-pipelines/ # product skill: ETL pipelines (DLT)
```

Hierarchy: `databricks-core` (core) → product skills → niche subskills

## Development

### Adding Skills

Create subskills that reference parent:

```markdown
---
name: "databricks-apps-chatbots"
parent: databricks-apps
---

# Chatbot Apps

**FIRST**: Use the parent `databricks-apps` skill for app development basics.

Then apply these patterns:
- Pattern 1
- Pattern 2
```

### Skills management

```bash
python3 scripts/skills.py              # generate manifest (default)
python3 scripts/skills.py validate     # check manifest is up to date (CI)
```

## Security

When documenting examples, obfuscate sensitive info:

- Workspace IDs: use `1111111111111111` not real IDs
- URLs: use `company-workspace.cloud.databricks.com`
- Never include real tokens, passwords, credentials
- Use placeholders for users, teams, resource IDs
