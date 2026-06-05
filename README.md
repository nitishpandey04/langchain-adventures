# Research Assistant

A simple 2-agent research system built with LangGraph.

## Architecture

```
START → Researcher → Writer → END
```

- **Researcher**: Takes a topic, searches the web using Tavily, and gathers relevant information.
- **Writer**: Takes the research findings and writes a polished, structured report.

## Setup

1. Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

2. Install dependencies:

```bash
uv sync
```

## Configuration

| Env Var | Required | Default | Description |
|---------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | — | OpenAI API key |
| `TAVILY_API_KEY` | Yes | — | Tavily search API key |
| `MODEL_NAME` | No | `gpt-4.1-mini` | OpenAI model to use |

## Run Locally

```bash
uv run langgraph dev
```

Opens on port 2024. Send input like:

```json
{"topic": "impact of AI on healthcare"}
```

The response will contain `research` (raw findings) and `report` (final written report).

## Get API Keys

- **OpenAI**: https://platform.openai.com/api-keys
- **Tavily**: https://tavily.com/