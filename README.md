# README.md

# News Semantic Search Prototype

This project is a News Scraper & Semantic Search tool using GenAI. It extracts news articles from URLs, summarizes them, categorizes their topics, stores them in a vector database, and provides a semantic (vector-based) search over the news.

## Features

- Scrapes full news articles and titles.
- Summarizes and extracts main topics using GenAI (OpenAI GPT-4o-mini).
- Stores embeddings in a local ChromaDB vector database.
- Provides interactive, context-aware semantic search via command line.
- Flexible: add new articles, change search parameters interactively.

---

## Setup

### 1. Clone the repo

```bash
git clone <your-github-repo-url>
cd <repo-folder>
```

### 2. Install dependencies

It is recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

pip install -r requirements.txt
```

**Example `requirements.txt`:**
```
chromadb
langchain
langchain-openai
openai
newspaper3k
pydantic
```

---

### 3. Set up your OpenAI API key

Create a `data.json` file in the project root with your key and (if you wish) list of URLs:
```json
{
  "api-key": "sk-....",
  "urls": [
    "https://edition.cnn.com/2026/02/03/politics/epstein-files-trump-clinton-musk-blanche-analysis",
    "https://edition.cnn.com/2026/02/04/science/colossal-dire-wolf-biovault-endangered-species-spc"
  ]
}
```

---

## Usage

### **Parsing and Searching**

#### Parse and store all news from URLs in `data.json`, then start interactive search:
```bash
python main.py --parse
```
- Or, specify URLs on the command line:
```bash
python main.py --parse --urls URL1 URL2 ...
```

#### Directly enter semantic search mode (without parsing):
```bash
python main.py --search
```

#### Interactive Search Console Commands

- Type a query to find news articles.
- `/max-results N` - change the number of search results (e.g. `/max-resulst 5`)
- `/thresh X` - set distance threshold (e.g. `/thresh 0.7`)
- `/exit` - quit

---

## Example

```bash
$ python main.py --parse
Parsing 2 URLs and storing summaries...

Parsing: https://edition.cnn.com/2026/02/03/politics/epstein-files-trump-clinton-musk-blanche-analysis
Title: Analysis: New files deepen a critical mystery about those who partied with Jeffrey Epstein
Summary: The article discusses ...

--- Interactive Semantic Search ---
Type your search query, /max-results N to adjust result count, /thresh X to adjust threshold (or /exit to quit):
[max-results=3 thresh=0.5] > trump
Analysis: New files deepen ...
...
```

---

## Notes

- Articles and embeddings are stored in the `./chromadb/` directory for persistence.
- Your API key is read from `data.json`.
- Tested on Python 3.12+, Linux with articles from CNN.

---

## Author

Semen Chupin

---
