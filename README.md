# Databricks Agent Skills

Skills para assistentes de codificacao com IA (Claude Code, Cursor, GitHub Copilot, etc.) que fornecem orientacao especifica para Databricks.

Publicado no [skills.sh](https://skills.sh) — o diretorio aberto de skills para agentes IA.

## Instalacao

### Instalar todas as skills

```bash
npx skills add welsonplay/databricks-agents
```

### Instalar uma skill especifica

```bash
npx skills add welsonplay/databricks-agents --skill databricks-core
npx skills add welsonplay/databricks-agents --skill databricks-apps
npx skills add welsonplay/databricks-agents --skill databricks-pipelines
```

### Instalar para agentes especificos

```bash
# Apenas para Claude Code
npx skills add welsonplay/databricks-agents -a claude-code

# Para Claude Code e Cursor
npx skills add welsonplay/databricks-agents -a claude-code -a cursor

# Para todos os agentes suportados
npx skills add welsonplay/databricks-agents --all
```

### Instalacao global (disponivel em todos os projetos)

```bash
npx skills add welsonplay/databricks-agents -g
```

### Gerenciar skills instaladas

```bash
# Listar skills instaladas
npx skills list

# Verificar atualizacoes
npx skills check

# Atualizar todas
npx skills update

# Remover uma skill
npx skills remove databricks-core

# Remover todas
npx skills remove --all
```

## Skills Disponiveis

| Skill | Descricao | Status |
|-------|-----------|--------|
| **databricks-core** | Operacoes core da CLI: autenticacao, perfis, exploracao de dados | Estavel |
| **databricks-apps** | Construir apps full-stack TypeScript usando AppKit | Estavel |
| **databricks-dabs** | Declarative Automation Bundles para deploy de recursos | Estavel |
| **databricks-jobs** | Orquestracao e agendamento de Jobs (Lakeflow Jobs) | Estavel |
| **databricks-lakebase** | Lakebase Postgres Autoscaling (banco OLTP serverless) | Estavel |
| **databricks-model-serving** | Endpoints de Model Serving para inferencia LLM/ML | Experimental |
| **databricks-pipelines** | Lakeflow Spark Declarative Pipelines (ETL/DLT) | Estavel |

## Hierarquia de Skills

```
databricks-core (fundacao)
├── databricks-apps        (produto)
├── databricks-jobs        (produto)
├── databricks-dabs        (habilitador)
├── databricks-lakebase    (produto)
├── databricks-model-serving (produto - experimental)
└── databricks-pipelines   (produto)
```

A skill `databricks-core` e a base e deve ser carregada primeiro. As demais sao skills de produto que dependem dela.

## Estrutura

Cada skill segue a [Agent Skills Specification](https://agentskills.io/specification):

```
skill-name/
├── SKILL.md           # Arquivo principal com frontmatter YAML + instrucoes
└── references/        # Documentacao adicional carregada sob demanda
```

## Desenvolvimento

### Criando Novas Skills

Crie uma "subskill" que referencia a skill principal:

```markdown
---
name: "ai-databricks-apps"
description: "Databricks apps com recursos de IA"
parent: databricks-apps
---

# Databricks Apps com IA

Primeiro, carregue a skill base databricks-apps para orientacao fundamental.

Depois aplique estes padroes adicionais:
- Padrao customizado 1
- Padrao customizado 2
```

Ou use o comando init para criar o template:

```bash
npx skills init minha-nova-skill
```

### Gerenciamento do Manifest

Apos adicionar ou atualizar skills, gere o manifest:

```bash
python3 scripts/skills.py              # gerar manifest (padrao)
python3 scripts/skills.py validate     # validar para CI
```

## Seguranca

Ao documentar exemplos, ofusque informacoes sensiveis:

- Workspace IDs: use `1111111111111111` em vez de IDs reais
- URLs: use `company-workspace.cloud.databricks.com`
- Nunca inclua tokens, senhas ou credenciais reais
- Use placeholders para usuarios, equipes e IDs de recursos

## Contribuindo

- Exemplos na documentacao devem seguir o principio de menor privilegio
- Ofusque valores sensiveis: workspace IDs, URLs, credenciais
