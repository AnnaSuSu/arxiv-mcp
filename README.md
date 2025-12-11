# arXiv MCP Server

[![PyPI version](https://badge.fury.io/py/arxiv-paper-mcp-server.svg)](https://pypi.org/project/arxiv-paper-mcp-server/)
[![Python](https://img.shields.io/pypi/pyversions/arxiv-paper-mcp-server.svg)](https://pypi.org/project/arxiv-paper-mcp-server/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Model Context Protocol (MCP) server that enables LLMs to search, download, and read arXiv papers. Gives AI assistants direct access to scientific literature.

## Features

- **Search papers** - Search by title, keywords, author, or arXiv ID
- **Read full text** - Download PDFs and extract text automatically
- **Section extraction** - Get specific sections (abstract, introduction, methods, conclusion)
- **Local caching** - Downloaded papers are cached locally for fast re-access
- **Zero configuration** - Works out of the box with sensible defaults

## Getting Started

### Prerequisites

This MCP server uses `uvx` to run. First, install `uv`:

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using Homebrew
brew install uv
```

After installation, restart your terminal.

### Installation

Install the arXiv MCP server with your client.

Standard config works in most tools:

```json
{
  "mcpServers": {
    "arxiv": {
      "command": "uvx",
      "args": ["arxiv-paper-mcp-server"]
    }
  }
}
```

<details>
<summary>Amp</summary>

```bash
amp mcp add arxiv -- uvx arxiv-paper-mcp-server
```
</details>

<details>
<summary>Claude Code</summary>

```bash
claude mcp add arxiv-server -- uvx arxiv-paper-mcp-server
```
</details>

<details>
<summary>Claude Desktop</summary>

Add to your `claude_desktop_config.json`:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "arxiv": {
      "command": "uvx",
      "args": ["arxiv-paper-mcp-server"]
    }
  }
}
```
</details>

<details>
<summary>Codex</summary>

```bash
codex mcp add arxiv -- uvx arxiv-paper-mcp-server
```
</details>

<details>
<summary>Cursor</summary>

Add to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "arxiv": {
      "command": "uvx",
      "args": ["arxiv-paper-mcp-server"]
    }
  }
}
```
</details>

<details>
<summary>Factory</summary>

Add to Factory MCP settings:

```json
{
  "mcpServers": {
    "arxiv": {
      "command": "uvx",
      "args": ["arxiv-paper-mcp-server"]
    }
  }
}
```
</details>

<details>
<summary>Gemini CLI</summary>

```bash
gemini mcp add arxiv -- uvx arxiv-paper-mcp-server
```
</details>

<details>
<summary>Goose</summary>

Run `goose configure`, then add to `~/.config/goose/config.yaml`:

```yaml
extensions:
  arxiv:
    command: uvx
    args:
      - arxiv-paper-mcp-server
```
</details>

<details>
<summary>Kiro</summary>

Add to Kiro MCP settings:

```json
{
  "mcpServers": {
    "arxiv": {
      "command": "uvx",
      "args": ["arxiv-paper-mcp-server"]
    }
  }
}
```
</details>

<details>
<summary>LM Studio</summary>

Add to LM Studio MCP settings:

```json
{
  "mcpServers": {
    "arxiv": {
      "command": "uvx",
      "args": ["arxiv-paper-mcp-server"]
    }
  }
}
```
</details>

<details>
<summary>opencode</summary>

```bash
opencode mcp add arxiv -- uvx arxiv-paper-mcp-server
```
</details>

<details>
<summary>Qodo Gen</summary>

Add to Qodo Gen MCP configuration:

```json
{
  "mcpServers": {
    "arxiv": {
      "command": "uvx",
      "args": ["arxiv-paper-mcp-server"]
    }
  }
}
```
</details>

<details>
<summary>VS Code</summary>

Add to `.vscode/mcp.json` in your workspace:

```json
{
  "mcpServers": {
    "arxiv": {
      "command": "uvx",
      "args": ["arxiv-paper-mcp-server"]
    }
  }
}
```
</details>

<details>
<summary>Warp</summary>

Add to Warp MCP settings:

```json
{
  "mcpServers": {
    "arxiv": {
      "command": "uvx",
      "args": ["arxiv-paper-mcp-server"]
    }
  }
}
```
</details>

<details>
<summary>Windsurf</summary>

Add to `~/.windsurf/mcp.json`:

```json
{
  "mcpServers": {
    "arxiv": {
      "command": "uvx",
      "args": ["arxiv-paper-mcp-server"]
    }
  }
}
```
</details>

<details>
<summary>Using pip</summary>

```bash
pip install arxiv-paper-mcp-server
arxiv-mcp-server
```
</details>

## Tools

| Tool | Description |
|------|-------------|
| `search` | Search arXiv papers by title, keywords, or arXiv ID (e.g., `2401.12345`) |
| `get_paper` | Download and read the full text of a paper, with optional section filtering |
| `list_downloaded_papers` | List all locally cached papers |

### Tool Details

#### `search(query, max_results=10)`

Search for papers on arXiv. Supports:
- Keywords: `"transformer attention mechanism"`
- Paper ID: `"2401.12345"` or `"arXiv:2401.12345"`
- Author: `"Yann LeCun"`

Returns paper ID, title, authors, publication date, and abstract preview.

#### `get_paper(paper_id, section="all")`

Download and extract text from a paper.

| Section | Description |
|---------|-------------|
| `all` | Full paper text (default) |
| `abstract` | Abstract only |
| `introduction` | Introduction section |
| `method` | Methods/Approach section |
| `conclusion` | Conclusion/Discussion section |

#### `list_downloaded_papers()`

List all papers that have been downloaded and cached locally.

## Configuration

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| `ARXIV_STORAGE_DIR` | Directory for downloaded papers | `~/.arxiv-mcp/papers` |

## Usage Examples

**Search for papers:**
```
User: Find recent papers about prompt compression

Claude: [Uses search("prompt compression", max_results=5)]
Found 5 papers:
- 2504.16574: PIS: Linking Importance Sampling...
- ...
```

**Read a specific paper:**
```
User: Read the introduction of paper 2401.12345

Claude: [Uses get_paper("2401.12345", section="introduction")]
[Returns the introduction section]
```

**Review cached papers:**
```
User: What papers have I downloaded?

Claude: [Uses list_downloaded_papers()]
You have 3 papers cached locally:
- 2401.12345: Paper Title...
```

## Development

```bash
# Clone the repository
git clone https://github.com/AnnaSuSu/arxiv-mcp.git
cd arxiv-mcp

# Install dependencies
uv sync

# Run server locally
uv run arxiv-mcp-server
```

## Requirements

- Python 3.10+
- Dependencies: `mcp`, `arxiv`, `pymupdf`

## License

MIT License - see [LICENSE](LICENSE) for details.
