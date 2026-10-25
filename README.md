# AI-Powered Web Scraper & Data Intelligence Engine

An autonomous, local Model Context Protocol (MCP) tool and Web Dashboard built to scrape web pages, generate AI-driven executive summaries, export content into professional formats (PDF, DOCX, Markdown), and index findings into a SQLite FTS5 Full-Text Search database.

---

## 🌟 Key Features

1. **Modular MCP Web Scraper**: Built using modern Python libraries (`httpx`, `BeautifulSoup4`) to extract clean content, structured headings, and metadata.
2. **Multi-Format Document Generator**: Converts scraped content and summaries directly into professional PDFs, Word (`.docx`) documents, or Markdown files.
3. **AI Executive Summary Engine**: Uses local AI processing logic to generate concise executive takeaways and structured reports.
4. **SQLite FTS5 Smart Search**: Built-in full-text search engine with BM25 relevance ranking to query content across all historically scraped documents.
5. **Interactive Flask Dashboard**:
   - Live metrics & statistics (Total Scrapes, PDF Count, Word Count).
   - Real-time semantic search input.
   - File format filtering.
   - One-click document preview/download.
   - Cascade record deletion (syncs disk files, SQLite database, and search index).

---

## 📁 System Architecture

```text
mcp-web-scraper/
│
├── core/
│   ├── __init__.py
│   ├── ai_summary.py         # AI Executive Summary Logic
│   └── search_engine.py      # SQLite FTS5 Search & Deletion Synchronization
│
├── scraped_outputs/
│   ├── scraped_database.db   # SQLite Storage & FTS5 Indexing
│   └── *.pdf, *.docx, *.md   # Generated Files Storage
│
├── templates/
│   └── index.html            # Flask Web Dashboard Interface
│
├── server.py                 # FastMCP Server Logic
├── app.py                    # Flask Web Application Interface
└── requirements.txt          # Python Dependencies
```

---

## ⚙️ Installation & Setup

### 1. Prerequisites
- Python 3.10 or higher installed.
- Claude Desktop installed.

### 2. Environment Setup
Clone or navigate to the project directory and install required dependencies:

```bash
cd "D:\Faizan Data\mcp-web-scraper"
python -m pip install -r requirements.txt
```

---

## 💻 Running the Components

### Running the MCP Server with Claude Desktop
Add the server configuration to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "web-scraper": {
      "command": "python",
      "args": [
        "D:\\Faizan Data\\mcp-web-scraper\\server.py"
      ]
    }
  }
}
```

### Running the Flask Web Dashboard
Start the local dashboard by executing:

```bash
python app.py
```

Access the Web Dashboard in your browser at:
`http://127.0.0.1:5000`

---

## 🛡️ License & Maintenance

Designed for autonomous AI data extraction, reporting, and intelligent search indexing.