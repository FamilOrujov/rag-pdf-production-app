# 📄 RAG Production App

A powerful RAG (Retrieval-Augmented Generation) application that lets you upload PDFs and ask questions about them using AI.

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Qdrant](https://img.shields.io/badge/Qdrant-FF4F64?logo=qdrant&logoColor=white)](https://qdrant.tech/)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?logo=openai&logoColor=white)](https://openai.com/)
[![Inngest](https://img.shields.io/badge/Inngest-6366F1?logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNMTIgMjRDMTguNjI3NCAyNCAyNCAxOC42Mjc0IDI0IDEyQzI0IDUuMzcyNTggMTguNjI3NCAwIDEyIDBDNS4zNzI1OCAwIDAgNS4zNzI1OCAwIDEyQzAgMTguNjI3NCA1LjM3MjU4IDI0IDEyIDI0WiIgZmlsbD0id2hpdGUiLz48L3N2Zz4=&logoColor=white)](https://inngest.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)](https://hub.docker.com/r/familorujov/rag-app)

---

## 📑 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Demo](#-demo)
- [Installation](#-installation)
  - [With Docker (Recommended)](#option-1-with-docker-recommended)
  - [Without Docker](#option-2-without-docker)
- [Usage](#-usage)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Environment Variables](#-environment-variables)
- [Commands Reference](#-commands-reference)

---

## ✨ Features

- 📄 **PDF Upload** — Upload any PDF document instantly
- 🔍 **Smart Chunking** — Automatically splits documents into searchable chunks
- 🧠 **AI Embeddings** — Uses OpenAI's text-embedding-3-large for semantic search
- 💬 **Natural Q&A** — Ask questions in plain English and get AI-powered answers
- 📊 **Workflow Dashboard** — Monitor ingestion jobs with Inngest
- 🎨 **Modern UI** — Beautiful Streamlit interface
- 🐳 **One-Command Deploy** — Run everything with a single Docker command

---

## 🏗️ Architecture

<p align="center">
  <img src="https://github.com/user-attachments/assets/1107a26e-1cc2-4957-97bf-20e35e7e7cb2" alt="RAG App Architecture" width="100%"/>
</p>

### Data Flow

**PDF Ingestion:**
```
PDF → Load → Chunk → Embed (OpenAI) → Store (Qdrant)
```

**Question Answering:**
```
Question → Embed (OpenAI) → Search (Qdrant) → Context + Question → GPT-4 → Answer
```

---

## 🎬 Demo

| Upload PDF | Ask Questions |
|------------|---------------|
| Upload any PDF document | Get AI-powered answers |

**Live URLs after running:**

| Service | URL |
|---------|-----|
| 📊 Main App | http://localhost:8501 |
| 📈 Inngest Dashboard | http://localhost:8288 |

---

## 🚀 Installation

### Prerequisites

- [OpenAI API Key](https://platform.openai.com/api-keys)

---

### Option 1: With Docker (Recommended)

> **Requirements:** [Docker](https://docs.docker.com/get-docker/) installed

#### Step 1: Create environment file

```bash
mkdir rag-app && cd rag-app
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

#### Step 2: Run

```bash
docker volume create rag_data
docker run -it --rm --name rag-app \
  -p 8501:8501 -p 8288:8288 \
  --env-file .env \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v rag_data:/qdrant/storage \
  familorujov/rag-app
```

#### Step 3: Open

Access the editor at  **http://localhost:8501** 

---

### Option 2: Without Docker

> **Requirements:** Python 3.13+, Node.js, [uv](https://github.com/astral-sh/uv), [Docker](https://docs.docker.com/get-docker/) (only for Qdrant)

#### Step 1: Clone the repository

```bash
git clone https://github.com/familorujov/RAG-Production-App.git
cd RAG-Production-App
```

#### Step 2: Start Qdrant database

```bash
docker run -d --name qdrant -p 6333:6333 -v ./qdrant_storage:/qdrant/storage qdrant/qdrant
```

#### Step 3: Install dependencies

```bash
uv sync
```

#### Step 4: Configure environment

```bash
cp env.example .env
# Edit .env and add your OPENAI_API_KEY
```
Or just create `.env` file, and place your OpenAI API key inside it (`OPENAI_API_KEY=sk-proj-...`).

#### Step 5: Start the application

Open **3 separate terminals**:

**Terminal 1 — FastAPI Backend:**
```bash
uv run uvicorn main:app --reload
```

**Terminal 2 — Inngest Dev Server:**
```bash
npx inngest-cli@latest dev -u http://127.0.0.1:8000/api/inngest --no-discovery
```

**Terminal 3 — Streamlit Frontend:**
```bash
uv run streamlit run streamlit_app.py
```

#### Step 6: Open

Go to **http://localhost:8501** 

---

## 📖 Usage

1. **Upload a PDF** — Click "Browse files" and select your PDF
2. **Wait for processing** — The document will be chunked and embedded
3. **Ask questions** — Type your question in the input box
4. **Get answers** — AI will respond based on your document content

> 💡 **Tip:** Monitor processing progress at http://localhost:8288 (Inngest Dashboard)

---

## 🔧 Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Frontend | [Streamlit](https://streamlit.io/) | Web UI |
| Backend | [FastAPI](https://fastapi.tiangolo.com/) | REST API |
| Workflows | [Inngest](https://inngest.com/) | Background jobs |
| Vector DB | [Qdrant](https://qdrant.tech/) | Semantic search |
| Embeddings | OpenAI text-embedding-3-large | Text vectorization |
| LLM | GPT-4o-mini | Answer generation |
| Package Manager | [uv](https://github.com/astral-sh/uv) | Python dependencies |

---

## 📁 Project Structure

```
RAG-Production-App/
├── main.py              # FastAPI app + Inngest workflows
├── streamlit_app.py     # Streamlit frontend
├── vector_db.py         # Qdrant database wrapper
├── data_loader.py       # PDF processing & embeddings
├── custom_types.py      # Pydantic models
├── Dockerfile           # Container build
├── docker-entrypoint.sh # Startup script
├── docker-compose.yml   # Alternative setup
├── pyproject.toml       # Python dependencies
└── env.example          # Environment template
```


## 📋 Commands Reference

### Docker Commands

```bash
# Run (foreground)
docker run -it --rm --name rag-app -p 8501:8501 -p 8288:8288 --env-file .env -v /var/run/docker.sock:/var/run/docker.sock -v rag_data:/qdrant/storage familorujov/rag-app

# Run (background)
docker run -d --name rag-app -p 8501:8501 -p 8288:8288 --env-file .env -v /var/run/docker.sock:/var/run/docker.sock -v rag_data:/qdrant/storage familorujov/rag-app

# View logs
docker logs -f rag-app

# Stop
docker stop rag-app rag-qdrant

# Remove
docker rm -f rag-app rag-qdrant

# Remove data
docker volume rm rag_data
```

### Local Development Commands

```bash
# Install dependencies
uv sync

# Run FastAPI
uv run uvicorn main:app --reload

# Run Streamlit
uv run streamlit run streamlit_app.py

# Run Inngest
npx inngest-cli@latest dev -u http://127.0.0.1:8000/api/inngest --no-discovery
```

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/familorujov">familorujov</a>
</p>
