import asyncio
from pathlib import Path
import time

import streamlit as st
import inngest
from dotenv import load_dotenv
import os
import requests

load_dotenv()

st.set_page_config(
    page_title="RAG Ingest PDF",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Modern custom CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,100..1000;1,9..40,100..1000&family=JetBrains+Mono:wght@400;500&display=swap');
    
    :root {
        --bg-primary: #0a0a0f;
        --bg-secondary: #12121a;
        --bg-card: #1a1a24;
        --accent-primary: #6366f1;
        --accent-secondary: #818cf8;
        --accent-glow: rgba(99, 102, 241, 0.15);
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --border-color: #2a2a3a;
        --success: #22c55e;
        --success-bg: rgba(34, 197, 94, 0.1);
    }
    
    .stApp {
        background: linear-gradient(180deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
    }
    
    .stApp > header {
        background: transparent;
    }
    
    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 800px;
    }
    
    /* Typography */
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        font-family: 'DM Sans', sans-serif !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }
    
    p, span, label, .stMarkdown p {
        font-family: 'DM Sans', sans-serif !important;
        color: var(--text-secondary);
    }
    
    /* Hero section styling */
    .hero-container {
        text-align: center;
        padding: 2rem 0 3rem 0;
        margin-bottom: 1rem;
    }
    
    .hero-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        display: inline-block;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .hero-title {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #f1f5f9 0%, #6366f1 50%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem !important;
        letter-spacing: -0.02em;
    }
    
    .hero-subtitle {
        color: var(--text-muted) !important;
        font-size: 1.1rem !important;
        font-weight: 400 !important;
    }
    
    /* Card styling */
    .custom-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .custom-card:hover {
        border-color: var(--accent-primary);
        box-shadow: 0 4px 32px var(--accent-glow);
    }
    
    .card-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 1.5rem;
    }
    
    .card-icon {
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
    }
    
    .card-title {
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        color: var(--text-primary) !important;
        margin: 0 !important;
    }
    
    .card-description {
        color: var(--text-muted) !important;
        font-size: 0.9rem !important;
        margin: 0 !important;
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        background: var(--bg-secondary) !important;
        border: 2px dashed var(--border-color) !important;
        border-radius: 12px !important;
        padding: 2rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stFileUploader > div:hover {
        border-color: var(--accent-primary) !important;
        background: var(--accent-glow) !important;
    }
    
    .stFileUploader label {
        color: var(--text-secondary) !important;
    }
    
    /* Form styling */
    .stForm {
        background: transparent !important;
        border: none !important;
    }
    
    .stTextInput > div > div {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
    }
    
    .stTextInput > div > div:focus-within {
        border-color: var(--accent-primary) !important;
        box-shadow: 0 0 0 3px var(--accent-glow) !important;
    }
    
    .stTextInput input {
        color: var(--text-primary) !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    
    .stTextInput input::placeholder {
        color: var(--text-muted) !important;
    }
    
    .stNumberInput > div > div {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 10px !important;
    }
    
    .stNumberInput input {
        color: var(--text-primary) !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary)) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 2rem !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 16px var(--accent-glow) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 24px var(--accent-glow) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    .stFormSubmitButton > button {
        width: 100% !important;
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.875rem 2rem !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        letter-spacing: 0.02em !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 16px var(--accent-glow) !important;
        margin-top: 1rem !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
    }
    
    .stFormSubmitButton > button p, .stFormSubmitButton > button span {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    
    .stFormSubmitButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 24px var(--accent-glow) !important;
    }
    
    /* Success/Alert styling */
    .stSuccess {
        background: var(--success-bg) !important;
        border: 1px solid var(--success) !important;
        border-radius: 10px !important;
        color: var(--success) !important;
    }
    
    .stAlert {
        border-radius: 10px !important;
    }
    
    /* Spinner styling */
    .stSpinner > div {
        border-color: var(--accent-primary) !important;
    }
    
    /* Divider styling */
    hr {
        border-color: var(--border-color) !important;
        margin: 2.5rem 0 !important;
    }
    
    /* Caption styling */
    .stCaption {
        color: var(--text-muted) !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    
    /* Answer section styling */
    .answer-container {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1.5rem;
    }
    
    .answer-label {
        font-size: 0.85rem !important;
        color: var(--accent-secondary) !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.75rem !important;
        font-weight: 600 !important;
    }
    
    .answer-text {
        color: var(--text-primary) !important;
        font-size: 1.05rem !important;
        line-height: 1.7 !important;
    }
    
    .sources-container {
        background: var(--bg-secondary);
        border-radius: 10px;
        padding: 1rem 1.25rem;
        margin-top: 1rem;
    }
    
    .source-item {
        color: var(--text-secondary) !important;
        font-size: 0.9rem !important;
        padding: 0.25rem 0;
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* Number input buttons */
    .stNumberInput button {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
    }
    
    /* Slider styling */
    .stSlider > div > div {
        background: var(--accent-primary) !important;
    }
    
    /* Label styling */
    .stTextInput label, .stNumberInput label, .stFileUploader label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Smooth animations */
    * {
        transition: background-color 0.2s ease, border-color 0.2s ease;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_inngest_client() -> inngest.Inngest:
    return inngest.Inngest(app_id="rag_app", is_production=False)


def save_uploaded_pdf(file) -> Path:
    uploads_dir = Path("uploads")
    uploads_dir.mkdir(parents=True, exist_ok=True)
    file_path = uploads_dir / file.name
    file_bytes = file.getbuffer()
    file_path.write_bytes(file_bytes)
    return file_path


async def send_rag_ingest_event(pdf_path: Path) -> None:
    client = get_inngest_client()
    await client.send(
        inngest.Event(
            name="rag/ingest_pdf",
            data={
                "pdf_path": str(pdf_path.resolve()),
                "source_id": pdf_path.name,
            },
        )
    )


# Hero Section
st.markdown("""
<div class="hero-container">
    <div class="hero-icon">📄</div>
    <h1 class="hero-title">RAG Document Intelligence</h1>
    <p class="hero-subtitle">Upload PDFs and get AI-powered insights from your documents</p>
</div>
""", unsafe_allow_html=True)

# Upload Section
st.markdown("""
<div class="custom-card">
    <div class="card-header">
        <div class="card-icon">⬆️</div>
        <div>
            <p class="card-title">Upload Document</p>
            <p class="card-description">Drag and drop or click to upload a PDF file</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

uploaded = st.file_uploader("", type=["pdf"], accept_multiple_files=False, label_visibility="collapsed")

if uploaded is not None:
    with st.spinner("Processing your document..."):
        path = save_uploaded_pdf(uploaded)
        asyncio.run(send_rag_ingest_event(path))
        time.sleep(0.3)
    st.success(f"✓ Successfully queued **{path.name}** for ingestion")
    st.caption("Ready for another upload? Drop a new file above.")

st.markdown("<br>", unsafe_allow_html=True)

# Query Section
st.markdown("""
<div class="custom-card">
    <div class="card-header">
        <div class="card-icon">🔍</div>
        <div>
            <p class="card-title">Ask Your Documents</p>
            <p class="card-description">Get AI-powered answers from your uploaded PDFs</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


async def send_rag_query_event(question: str, top_k: int) -> None:
    client = get_inngest_client()
    result = await client.send(
        inngest.Event(
            name="rag/query_pdf_ai",
            data={
                "question": question,
                "top_k": top_k,
            },
        )
    )

    return result[0]


def _inngest_api_base() -> str:
    return os.getenv("INNGEST_API_BASE", "http://localhost:8288/v1")


def fetch_runs(event_id: str) -> list[dict]:
    url = f"{_inngest_api_base()}/events/{event_id}/runs"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    return data.get("data", [])


def wait_for_run_output(event_id: str, timeout_s: float = 120.0, poll_interval_s: float = 0.5) -> dict:
    start = time.time()
    last_status = None
    while True:
        runs = fetch_runs(event_id)
        if runs:
            run = runs[0]
            status = run.get("status")
            last_status = status or last_status
            if status in ("Completed", "Succeeded", "Success", "Finished"):
                return run.get("output") or {}
            if status in ("Failed", "Cancelled"):
                raise RuntimeError(f"Function run {status}")
        if time.time() - start > timeout_s:
            raise TimeoutError(f"Timed out waiting for run output (last status: {last_status})")
        time.sleep(poll_interval_s)


with st.form("rag_query_form"):
    question = st.text_input("Your question", placeholder="e.g., What are the main findings in this document?")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        top_k = st.number_input("Context chunks", min_value=1, max_value=20, value=5, step=1, help="Number of document chunks to retrieve for context")
    
    submitted = st.form_submit_button("Ask Question", use_container_width=True)

    if submitted and question.strip():
        with st.spinner("Analyzing documents and generating answer..."):
            event_id = asyncio.run(send_rag_query_event(question.strip(), int(top_k)))
            output = wait_for_run_output(event_id)
            answer = output.get("answer", "")
            sources = output.get("sources", [])

        # Display answer with custom styling
        st.markdown("""
        <div class="answer-container">
            <p class="answer-label">📝 Answer</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""<p class="answer-text">{answer or "No answer could be generated."}</p>""", unsafe_allow_html=True)
        
        if sources:
            st.markdown("""
            <div class="sources-container">
                <p class="answer-label" style="margin-bottom: 0.5rem !important;">📚 Sources</p>
            </div>
            """, unsafe_allow_html=True)
            for s in sources:
                st.markdown(f"""<p class="source-item">• {s}</p>""", unsafe_allow_html=True)
