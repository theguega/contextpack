# 📦 contextpack-md

A dead-simple tool to extract high-quality Markdown from any URL for LLMs.

## 🚀 Quick Start

```bash
# Get context to stdout
uvx contextpack-md https://docs.python.org/3/

# Download a PDF and convert to Markdown (extra deps)
uvx --with "contextpack-md[pdf]" contextpack-md pdf https://arxiv.org/pdf/1706.03762.pdf
```

## Install the binary directly

```bash
# without pdf feature
uv tool install contextpack-md

# With pdf feature (extra deps)
uv tool install contextpack-md --with "contextpack-md[pdf]"
```

## ✨ Features

- **Single Purpose**: Get clean, LLM-ready Markdown from a URL.
- **PDF Support**: Convert online PDFs to high-quality Markdown using `marker-pdf`.
- **Optional Local Storage**: Save results to a `.contextpack-md` folder.
- **Zero Configuration**: No complex ranking, crawling, or embedding setups.
