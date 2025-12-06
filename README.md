# arXiv MCP Server

MCP Server for searching and reading arXiv papers directly from Claude Code.

## Installation

```bash
# Using uvx (recommended)
uvx arxiv-mcp-server

# Or install with pip
pip install arxiv-mcp-server
```

## Usage with Claude Code

```bash
claude mcp add arxiv-server -- uvx arxiv-mcp-server
```

Or manually add to your Claude Code MCP settings:

```json
{
  "mcpServers": {
    "arxiv": {
      "command": "uvx",
      "args": ["arxiv-mcp-server"]
    }
  }
}
```

### Available Tools

| Tool | Description |
|------|-------------|
| `search` | Search arXiv papers by title, keywords, or arXiv ID |
| `get_paper` | Download and read paper full text |
| `list_downloaded_papers` | List locally cached papers |

### Examples

```
User: 帮我看一下 PIS: Linking Importance Sampling... 这篇论文

Claude Code:
  1. search("PIS Importance Sampling Prompt Compression")
  2. get_paper("2504.16574")
  3. 分析论文内容...
```

## Configuration

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| `ARXIV_STORAGE_DIR` | Directory for downloaded papers | `~/.arxiv-mcp/papers` |

## Development

```bash
# Install dependencies
uv sync

# Run server directly
uv run arxiv-mcp-server
```
